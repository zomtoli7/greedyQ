import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from greedyq.build import build, load_study
from greedyq.deployment import preflight
from greedyq.exporter import generate as generate_export
from greedyq.validator import validate_state_artifacts
from greedyq.preregistration import generate as generate_preregistration
from greedyq.prolific import completion_url, parse_launch, resolve_launch

ROOT = Path(__file__).resolve().parents[1]


class ReleasePipelineTests(unittest.TestCase):
    def copy_study(self, tmp, name="complete-study"):
        target = Path(tmp) / "study"
        shutil.copytree(ROOT / "examples" / name, target, ignore=shutil.ignore_patterns(".greedyq", "preview.html", "index.html", "studio.html", "greedyq-core.js", "greedyq-runtime.css"))
        return target

    def test_prolific_launch_requires_all_three_identifiers(self):
        good = parse_launch("?PROLIFIC_PID=p1&STUDY_ID=s1&SESSION_ID=x1", "test")
        self.assertEqual("passed", good["status"])
        bad = parse_launch("?PROLIFIC_PID=p1", "production")
        self.assertEqual("failed", bad["status"])
        self.assertEqual({"STUDY_ID", "SESSION_ID"}, {x["message"].split()[0] for x in bad["issues"]})

    def test_prolific_completion_is_https_and_encoded(self):
        self.assertEqual("https://app.prolific.com/submissions/complete?cc=A%2FB", completion_url("https://app.prolific.com/submissions/complete", "A/B"))
        with self.assertRaises(ValueError): completion_url("http://example.test", "OK")

    def test_parameter_free_test_launch_is_recorded_as_direct(self):
        direct = resolve_launch("", "test")
        self.assertEqual("passed", direct["status"])
        self.assertEqual("direct_test", direct["source"])
        self.assertIsNone(direct["identifiers"])
        self.assertEqual("failed", resolve_launch("", "production")["status"])
        self.assertEqual("failed", resolve_launch("?PROLIFIC_PID=partial", "test")["status"])

    def test_preregistration_is_draft_hashes_exact_sources_and_never_submits(self):
        with tempfile.TemporaryDirectory() as tmp:
            study = self.copy_study(tmp)
            _, _, config = load_study(study)
            result = generate_preregistration(study, config)
            data = json.loads(result["json"].read_text())
            manifest = json.loads(result["manifest"].read_text())
            self.assertEqual("draft_unapproved", data["status"])
            self.assertFalse(data["researcher_approved"])
            self.assertFalse(data["fielding_allowed"])
            for item in manifest["artifacts"]:
                self.assertEqual(hashlib.sha256((study / item["path"]).read_bytes()).hexdigest(), item["sha256"])

    def test_exporter_generates_runnable_shape_and_truthful_mismatches(self):
        with tempfile.TemporaryDirectory() as tmp:
            study = self.copy_study(tmp)
            _, parsed, config = load_study(study)
            output, report = generate_export(study, parsed, config)
            self.assertIn("shiny::shinyApp", (output / "app.R").read_text())
            self.assertEqual((study / "survey.qmd").read_text(), (output / "survey.qmd").read_text().replace("  mode: preview\n", "", 1))
            self.assertFalse(report["equivalence_claimed"])
            if shutil.which("Rscript"):
                subprocess.run(["Rscript", "-e", f"parse(file={json.dumps(str(output / 'app.R'))})"], check=True, capture_output=True, text=True)
            self.assertEqual("generated_unverified", report["generator_status"])
            exported_qmd = (output / "survey.qmd").read_text()
            self.assertRegex(exported_qmd, r"survey-settings:\n\s+mode: preview")
            app = (output / "app.R").read_text()
            for token in ("sd_show_if(", "sd_skip_if(", "sd_stop_if(", 'sd_value("gender")', "sd_is_answered", "assignment_condition <- sample", "sd_store_value(assignment_condition)"):
                self.assertIn(token, app)
            skip_section = app.split("sd_skip_if(", 1)[1].split("sd_stop_if(", 1)[0]
            self.assertNotIn("assignment_condition", skip_section)

    def test_exporter_translates_greedyq_controls_to_surveydown_custom_controls(self):
        with tempfile.TemporaryDirectory() as tmp:
            study = self.copy_study(tmp, "control-gallery")
            _, parsed, config = load_study(study)
            output, report = generate_export(study, parsed, config)
            qmd = (output / "survey.qmd").read_text()
            app = (output / "app.R").read_text()
            for qid in ("rank_example", "sbs_example", "nps_example", "timing_example", "sum_example", "group_rank_example", "drill_example", "audio_example", "video_example", "custom_example"):
                self.assertIn(f'id = "{qid}"', qmd)
                self.assertIn(f'output = "gq_{qid}_output"', qmd)
                self.assertIn(f'value = "gq_{qid}_value"', qmd)
                self.assertIn(f"output$gq_{qid}_output", app)
                self.assertIn(f"gq_{qid}_value", app)
            self.assertNotIn('type = "rank_order"', qmd)
            self.assertNotIn('type = "constant_sum"', qmd)
            self.assertGreaterEqual(qmd.count("sd_question_custom("), 10)
            self.assertTrue((output / "images/blue.svg").is_file())
            custom = next(x for x in report["features"] if x["id"] == "greedyq_custom_controls")
            self.assertEqual("generated_custom", custom["classification"])
            self.assertFalse(report["equivalence_claimed"])

    def test_static_build_passes_offline_deployment_preflight(self):
        with tempfile.TemporaryDirectory() as tmp:
            study = self.copy_study(tmp)
            report, _ = build(study)
            self.assertEqual("passed", report["status"])
            deployment = preflight(study)
            self.assertEqual("passed", deployment["status"], deployment)

    def test_rpc_migration_requires_capability_tokens_and_locked_assignment(self):
        sql = (ROOT / "templates/supabase/002_browser_rpc.sql").read_text().lower()
        for token in ("greedyq_create_session", "p_access_token", "p_greedyq_version", "extensions.digest(p_access_token", "pg_advisory_xact_lock", "security definer", "research data cannot be saved before consent", "greedyq_register_external", "duplicate participant", "for update", "research_data_deleted", "grant execute"):
            self.assertIn(token, sql)
        self.assertNotIn("grant select on public.gq_answers to anon", sql)
        self.assertIn("respondent_source='prolific'", sql)

    def test_results_dashboard_is_built_with_server_only_database_access(self):
        dashboard = (ROOT / "templates/browser/results.html").read_text()
        api = (ROOT / "templates/vercel/api/results.js").read_text()
        migration = (ROOT / "templates/supabase/003_results_dashboard.sql").read_text()
        for token in ("Real responses", "Test responses", "Direct", "Prolific", "Download CSV", "Where participants stopped", "Conditions", "Answer summary", "Variable guide", "questionColumns", "flattenQuestion", "seconds_on_page", ".group", ".rank"):
            self.assertIn(token, dashboard)
        self.assertIn("SUPABASE_SECRET_KEY", api)
        self.assertNotIn("SUPABASE_SECRET_KEY", dashboard)
        self.assertIn("respondent_source", migration)
        self.assertIn("is_test", api)
        self.assertIn("studyModel.pages", dashboard)
        self.assertIn('"completed_at"', dashboard)
        self.assertIn('"condition"', dashboard)
        with tempfile.TemporaryDirectory() as tmp:
            study = self.copy_study(tmp)
            build(study)
            rendered = (study / "results.html").read_text()
            embedded = re.search(r'<script id="greedyq-model" type="application/json">(.*?)</script>', rendered, re.S)
            self.assertIsNotNone(embedded)
            model = json.loads(embedded.group(1))
            expected = {q["id"] for page in model["pages"] for q in page["questions"]}
            self.assertIn("support_post", expected)
            self.assertIn("gender_self_description", expected)

    def test_state_artifacts_match_their_contracts_and_hashes(self):
        report = validate_state_artifacts(ROOT / "examples" / "complete-study")
        self.assertEqual("passed", report["status"], report)
        with tempfile.TemporaryDirectory() as tmp:
            study = self.copy_study(tmp)
            (study / ".greedyq").mkdir()
            (study / ".greedyq" / "study-state.json").write_text("{}")
            broken = validate_state_artifacts(study)
            self.assertEqual("failed", broken["status"])
            self.assertTrue(all(issue["code"] == "GQ012" for issue in broken["issues"]))

    def test_preflight_reports_broken_data_contract_as_gq013(self):
        with tempfile.TemporaryDirectory() as tmp:
            study = self.copy_study(tmp)
            build(study)
            migration = study / "supabase/migrations/002_browser_rpc.sql"
            migration.write_text(migration.read_text().replace("greedyq_withdraw_session", "removed_withdrawal"))
            report = preflight(study)
            self.assertEqual("failed", report["status"])
            self.assertTrue(any(issue["code"] == "GQ013" for issue in report["issues"]))

    def test_build_records_and_preflight_verifies_migration_checksums(self):
        with tempfile.TemporaryDirectory() as tmp:
            study = self.copy_study(tmp)
            build(study)
            manifest = json.loads((study / "supabase/migrations/manifest.json").read_text())
            self.assertEqual(["001_initial.sql", "002_browser_rpc.sql", "003_results_dashboard.sql"], [item["name"] for item in manifest["migrations"]])
            self.assertEqual("passed", preflight(study)["status"])
            migration = study / "supabase/migrations/003_results_dashboard.sql"
            migration.write_text(migration.read_text() + "\n-- changed after build\n")
            report = preflight(study)
            self.assertTrue(any("checksum" in item["message"] for item in report["issues"]))

    def test_browser_connection_tester_uses_only_synthetic_public_configuration(self):
        tester = (ROOT / "templates/supabase/connection-test.html").read_text().lower()
        for token in ("greedyq_create_session", "greedyq_assign_condition", "greedyq_save_session", "greedyq_register_external", "greedyq_withdraw_session", "is_test: true", "synthetic"):
            self.assertIn(token, tester)
        self.assertNotIn("service_role_key", tester)
        self.assertNotIn("database_password", tester)
        self.assertIn('lifecycle: "created"', tester)
        self.assertNotIn('lifecycle: "active"', tester)

    def test_runtime_uses_only_public_supabase_configuration(self):
        template = (ROOT / "templates/browser/respondent.html").read_text().lower()
        self.assertIn("supabase_anon_key", template)
        self.assertNotIn("service_role", template)
        self.assertNotIn("database_password", template)
        self.assertIn("externalidentifiers", template)


if __name__ == "__main__": unittest.main()
