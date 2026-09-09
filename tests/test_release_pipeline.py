import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from greedyq.build import build, load_study
from greedyq.deployment import preflight
from greedyq.exporter import generate as generate_export
from greedyq.preregistration import generate as generate_preregistration
from greedyq.prolific import completion_url, parse_launch

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
            self.assertEqual((study / "survey.qmd").read_bytes(), (output / "survey.qmd").read_bytes())
            self.assertFalse(report["equivalence_claimed"])
            self.assertEqual("generated_unverified", report["generator_status"])

    def test_static_build_passes_offline_deployment_preflight(self):
        with tempfile.TemporaryDirectory() as tmp:
            study = self.copy_study(tmp)
            report, _ = build(study)
            self.assertEqual("passed", report["status"])
            deployment = preflight(study)
            self.assertEqual("passed", deployment["status"], deployment)

    def test_rpc_migration_requires_capability_tokens_and_locked_assignment(self):
        sql = (ROOT / "templates/supabase/002_browser_rpc.sql").read_text().lower()
        for token in ("greedyq_create_session", "p_access_token", "p_greedyq_version", "digest(p_access_token", "pg_advisory_xact_lock", "security definer", "research data cannot be saved before consent", "greedyq_register_external", "duplicate participant", "for update", "research_data_deleted", "grant execute"):
            self.assertIn(token, sql)
        self.assertNotIn("grant select on public.gq_answers to anon", sql)

    def test_browser_connection_tester_uses_only_synthetic_public_configuration(self):
        tester = (ROOT / "templates/supabase/connection-test.html").read_text().lower()
        for token in ("greedyq_create_session", "greedyq_assign_condition", "greedyq_save_session", "greedyq_register_external", "greedyq_withdraw_session", "is_test: true", "synthetic"):
            self.assertIn(token, tester)
        self.assertNotIn("service_role_key", tester)
        self.assertNotIn("database_password", tester)

    def test_runtime_uses_only_public_supabase_configuration(self):
        template = (ROOT / "templates/browser/respondent.html").read_text().lower()
        self.assertIn("supabase_anon_key", template)
        self.assertNotIn("service_role", template)
        self.assertNotIn("database_password", template)
        self.assertIn("externalidentifiers", template)


if __name__ == "__main__": unittest.main()
