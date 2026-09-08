import json
import hashlib
import re
import shutil
import subprocess
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


class GenerationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.preview_model = json.loads(
            (ROOT / "examples" / "complete-study" / "preview-model.json").read_text()
        )
        cls.preview_pages = {page["id"]: page for page in cls.preview_model["pages"]}

    @staticmethod
    def rule_matches(rule, answers, condition):
        if not rule:
            return True
        if "all" in rule:
            return all(GenerationContractTests.rule_matches(r, answers, condition) for r in rule["all"])
        if "any" in rule:
            return any(GenerationContractTests.rule_matches(r, answers, condition) for r in rule["any"])
        actual = condition if rule["field"] == "condition" else answers.get(rule["field"])
        if "equals" in rule:
            return actual == rule["equals"]
        if "not_equals" in rule:
            return actual != rule["not_equals"]
        if actual is None:
            return False
        for name, function in (
            ("lt", lambda expected: float(actual) < expected),
            ("lte", lambda expected: float(actual) <= expected),
            ("gt", lambda expected: float(actual) > expected),
            ("gte", lambda expected: float(actual) >= expected),
        ):
            if name in rule:
                return function(rule[name])
        return False

    def preview_next(self, page_id, answers, condition="control"):
        page = self.preview_pages[page_id]
        for route in page.get("routes", []):
            if self.rule_matches(route["when"], answers, condition):
                return route["to"]
        return page.get("next")

    def test_reference_ai_state_matches_published_schemas(self):
        schema_dir = ROOT / "schemas" / "ai"
        state_dir = ROOT / "examples" / "complete-study" / ".greedyq"
        for schema_path in schema_dir.glob("*.schema.json"):
            state_path = state_dir / schema_path.name.replace(".schema", "")
            schema = json.loads(schema_path.read_text())
            state = json.loads(state_path.read_text())
            errors = list(Draft202012Validator(schema).iter_errors(state))
            self.assertEqual([], errors, state_path.name)

    def test_state_schema_supports_interactive_preview_checkpoint(self):
        schema = json.loads(
            (ROOT / "schemas" / "ai" / "study-state.schema.json").read_text()
        )
        checkpoints = schema["properties"]["checkpoint"]["enum"]
        self.assertIn("interactive_preview_reviewed", checkpoints)
        self.assertIn("governance_consent_confirmed", checkpoints)

    def test_reference_qmd_uses_display_label_on_the_left(self):
        qmd = (ROOT / "examples" / "complete-study" / "survey.qmd").read_text()
        vectors = re.findall(r"(?:option|row)\s*=\s*c\((.*?)\n\s*\)", qmd, re.DOTALL)
        reversed_pairs = []
        for vector in vectors:
            reversed_pairs.extend(
                re.findall(
                    r'^\s*([a-z][a-z0-9_]*)\s*=\s*"([^"\n ]+(?: [^"\n]+)+)"\s*,?$',
                    vector,
                    flags=re.MULTILINE,
                )
            )
        self.assertEqual([], reversed_pairs)
        self.assertIn('"Yes, I consent" = "yes"', qmd)
        self.assertIn('"No, I do not consent" = "no"', qmd)

    def test_reversed_option_fixture_is_detectable(self):
        qmd = (
            ROOT / "tests" / "fixtures" / "reversed-option" / "survey.qmd"
        ).read_text()
        self.assertRegex(qmd, r'(?m)^\s*agree\s*=\s*"I agree"')
        expected = json.loads(
            (
                ROOT
                / "tests"
                / "fixtures"
                / "reversed-option"
                / "expected-diagnostics.json"
            ).read_text()
        )
        self.assertEqual("GQ011", expected[0]["code"])

    def test_canonical_migration_contains_required_safety_contracts(self):
        sql = (
            ROOT
            / "examples"
            / "complete-study"
            / "supabase"
            / "migrations"
            / "001_initial.sql"
        ).read_text()
        for required in (
            "gq_withdraw_and_delete",
            "for update",
            "security definer",
            "revoke all on function",
            "create policy gq_analyst_sessions_read",
            "create policy gq_analyst_answers_read",
            "gq_analysis_export",
            "not s.is_test",
        ):
            self.assertIn(required, sql.lower())

    def test_full_guides_embed_the_canonical_bundle_verbatim(self):
        bundled_files = (
            "docs/preview-ui-spec.md",
            "web/greedyq-core.js",
            "web/greedyq-runtime.css",
            "templates/browser/respondent.html",
            "templates/browser/preview.html",
            "templates/browser/studio.html",
            "examples/complete-study/supabase/migrations/001_initial.sql",
            "examples/complete-study/vercel.json",
            "schemas/ai/study-state.schema.json",
            "schemas/ai/decision-log.schema.json",
            "schemas/ai/unresolved-decisions.schema.json",
            "schemas/ai/generation-manifest.schema.json",
            "schemas/preview-model.schema.json",
        )
        for guide_name in ("greedyq-guide.md", "greedyq-guide(kor).md"):
            guide = (ROOT / "guides" / guide_name).read_text()
            for relative in bundled_files:
                source = (ROOT / relative).read_text().rstrip("\n")
                digest = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
                self.assertIn(f"### FILE: `{relative}`", guide)
                self.assertIn(f"SHA-256: `{digest}`", guide)
                self.assertIn(source, guide)

    def test_preview_bundle_is_local_and_safe_by_default(self):
        preview = (ROOT / "templates/browser/preview.html").read_text()
        core = (ROOT / "web/greedyq-core.js").read_text()
        self.assertIn('src="greedyq-core.js"', preview)
        self.assertNotIn("fetch(", preview)
        self.assertNotIn("eval(", core)
        self.assertIn("NO EXTERNAL WRITES", preview)
        self.assertIn('id="greedyq-model"', preview)
        self.assertIn("Content-Security-Policy", preview)
        self.assertIn("connect-src 'none'", preview)
        self.assertNotIn("XMLHttpRequest", core)
        self.assertNotIn("WebSocket", core)

    def test_preview_template_contains_required_ui_states(self):
        preview = (ROOT / "templates/browser/preview.html").read_text()
        core = (ROOT / "web/greedyq-core.js").read_text()
        for required in (
            "responsive preview", "NO EXTERNAL WRITES", 'id="desktop"',
            'id="mobile"', 'id="condition"', 'id="page"', 'id="state"',
        ):
            self.assertIn(required, preview)
        for required in ('role="alert"', "prefers-reduced-motion", "gq-matrix"):
            self.assertIn(required, core if required != "prefers-reduced-motion" else (ROOT / "web/greedyq-runtime.css").read_text())

    def test_condition_switch_clears_post_assignment_answers(self):
        preview = (ROOT / "templates/browser/preview.html").read_text()
        self.assertIn("desktop.state.condition", preview)
        self.assertRegex(preview, r"desktop\.state\.history\s*=\s*\[\]")

    def test_preview_styles_cover_required_responsive_breakpoints(self):
        preview = (ROOT / "templates/browser/preview.html").read_text()
        styles = (ROOT / "web/greedyq-runtime.css").read_text()
        self.assertRegex(preview, r"@media\s*\(max-width:\s*1050px\)")
        self.assertIn("390px", preview)
        self.assertRegex(styles, r"max-width:\s*760px")

    def test_preview_runtime_javascript_parses(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("node executable is not on PATH")
        result = subprocess.run(
            [node, "--check", str(ROOT / "web/greedyq-core.js")], text=True, capture_output=True, check=False
        )
        self.assertEqual(0, result.returncode, result.stderr)

    def test_golden_preview_model_matches_schema(self):
        schema = json.loads((ROOT / "schemas" / "preview-model.schema.json").read_text())
        errors = list(Draft202012Validator(schema).iter_errors(self.preview_model))
        self.assertEqual([], errors)

    def test_golden_preview_ids_are_unique_and_references_resolve(self):
        page_ids = [page["id"] for page in self.preview_model["pages"]]
        self.assertEqual(len(page_ids), len(set(page_ids)))
        question_ids = [q["id"] for p in self.preview_model["pages"] for q in p["questions"]]
        self.assertEqual(len(question_ids), len(set(question_ids)))
        self.assertFalse(set(page_ids) & set(question_ids))
        self.assertIn(self.preview_model["start_page"], page_ids)
        self.assertIn(self.preview_model["assignment_page"], page_ids)
        for page in self.preview_model["pages"]:
            if page.get("next"):
                self.assertIn(page["next"], page_ids)
            for route in page.get("routes", []):
                self.assertIn(route["to"], page_ids)

    def test_golden_preview_covers_qmd_pages_and_questions(self):
        qmd = (ROOT / "examples" / "complete-study" / "survey.qmd").read_text()
        qmd_pages = set(re.findall(r"(?m)^--- ([a-z][a-z0-9_]*)$", qmd))
        qmd_questions = set(re.findall(r'(?m)^\s*id\s*=\s*"([a-z][a-z0-9_]*)"', qmd))
        self.assertEqual(qmd_pages, set(self.preview_pages))
        preview_questions = {q["id"] for p in self.preview_model["pages"] for q in p["questions"]}
        self.assertEqual(qmd_questions, preview_questions)

    def test_preview_display_and_stored_options_match_qmd(self):
        qmd = (ROOT / "examples" / "complete-study" / "survey.qmd").read_text()
        qmd_options, qmd_rows = {}, {}
        for chunk in re.findall(r"```\{r\}(.*?)```", qmd, re.S):
            qid = re.search(r'id\s*=\s*"([a-z][a-z0-9_]*)"', chunk)
            if not qid:
                continue
            for key, target in (("option", qmd_options), ("row", qmd_rows)):
                vector = re.search(rf"{key}\s*=\s*c\((.*?)\n\s*\)", chunk, re.S)
                if not vector:
                    continue
                pairs = re.findall(r'^\s*"([^"]+)"\s*=\s*("[^"]+"|-?\d+(?:\.\d+)?)\s*,?$', vector.group(1), re.M)
                target[qid.group(1)] = [(label, json.loads(value)) for label, value in pairs]
        for page in self.preview_model["pages"]:
            for question in page["questions"]:
                if question["id"] in qmd_options:
                    actual = [(o["label"], o["value"]) for o in question["options"]]
                    self.assertEqual(qmd_options[question["id"]], actual, question["id"])
                if question["id"] in qmd_rows:
                    actual = [(o["label"], o["value"]) for o in question["rows"]]
                    self.assertEqual(qmd_rows[question["id"]], actual, question["id"])

    def test_happy_paths_route_through_each_condition(self):
        answers = {"consent_choice": "yes", "age": 30, "withdraw_now": "submit"}
        for condition, stimulus in (("control", "stimulus_control"), ("treatment", "stimulus_treatment")):
            self.assertEqual("eligibility", self.preview_next("consent", answers, condition))
            self.assertEqual("baseline", self.preview_next("eligibility", answers, condition))
            self.assertEqual(stimulus, self.preview_next("baseline", answers, condition))
            self.assertEqual("complete", self.preview_next("participant_control", answers, condition))

    def test_consent_refusal_and_minor_screenout_routes(self):
        self.assertEqual("consent_refused", self.preview_next("consent", {"consent_choice": "no"}))
        self.assertEqual("screened_out", self.preview_next("eligibility", {"age": 17}))
        self.assertEqual("baseline", self.preview_next("eligibility", {"age": 18}))

    def test_withdrawal_route_and_deletion_question(self):
        answers = {"withdraw_now": "withdraw"}
        self.assertEqual("withdrawn", self.preview_next("participant_control", answers))
        deletion = next(q for q in self.preview_pages["participant_control"]["questions"] if q["id"] == "deletion_request")
        self.assertTrue(deletion["required"])
        self.assertTrue(self.rule_matches(deletion["show_if"], answers, "control"))
        self.assertFalse(self.rule_matches(deletion["show_if"], {"withdraw_now": "submit"}, "control"))

    def test_conditional_questions_cover_both_states(self):
        opposition = next(q for q in self.preview_pages["outcomes"]["questions"] if q["id"] == "opposition_reason")
        self.assertTrue(self.rule_matches(opposition["show_if"], {"support_post": 3}, "control"))
        self.assertFalse(self.rule_matches(opposition["show_if"], {"support_post": 4}, "control"))
        self_description = next(q for q in self.preview_pages["demographics"]["questions"] if q["id"] == "gender_self_description")
        self.assertTrue(self.rule_matches(self_description["show_if"], {"gender": "self_describe"}, "control"))
        self.assertFalse(self.rule_matches(self_description["show_if"], {"gender": "woman"}, "control"))

    def test_all_terminal_outcomes_are_reachable_or_jump_testable(self):
        outcomes = {p.get("terminal") for p in self.preview_model["pages"] if p.get("terminal")}
        self.assertEqual({"completed", "screened_out", "consent_refused", "withdrawn", "technical_error"}, outcomes)

    def test_preview_model_contains_no_redirect_or_secret_material(self):
        raw = json.dumps(self.preview_model).lower()
        for forbidden in ("https://", "service_role", "api_key", "password", "bearer "):
            self.assertNotIn(forbidden, raw)

    def test_built_reference_preview_contains_exact_model(self):
        built = (ROOT / "examples" / "complete-study" / "preview.html").read_text()
        match = re.search(r'<script id="greedyq-model" type="application/json">(.*?)</script>', built, re.S)
        self.assertIsNotNone(match)
        self.assertEqual(self.preview_model, json.loads(match.group(1)))

    def test_progress_paths_are_condition_specific_and_resolve(self):
        paths = self.preview_model["progress_paths"]
        self.assertIn("stimulus_control", paths["control"])
        self.assertNotIn("stimulus_treatment", paths["control"])
        self.assertIn("stimulus_treatment", paths["treatment"])
        self.assertNotIn("stimulus_control", paths["treatment"])
        for path in paths.values():
            self.assertTrue(all(page in self.preview_pages for page in path))
            self.assertEqual("complete", path[-1])

    def test_required_questions_match_qmd_front_matter(self):
        qmd = (ROOT / "examples" / "complete-study" / "survey.qmd").read_text()
        front = qmd.split("---", 2)[1]
        block = re.search(r"required:\n((?:\s+- [a-z0-9_]+\n)+)", front)
        required_qmd = set(re.findall(r"- ([a-z0-9_]+)", block.group(1)))
        required_preview = {q["id"] for p in self.preview_model["pages"] for q in p["questions"] if q.get("required")}
        # deletion_request is conditionally required by greedyq.yml only when withdrawing.
        self.assertEqual(required_qmd | {"deletion_request"}, required_preview)
        config = (ROOT / "examples" / "complete-study" / "greedyq.yml").read_text()
        self.assertIn("not answered(deletion_request)", config)

    def test_question_and_matrix_values_are_unique(self):
        for page in self.preview_model["pages"]:
            for question in page["questions"]:
                for key in ("options", "rows"):
                    values = [item["value"] for item in question.get(key, [])]
                    self.assertEqual(len(values), len(set(values)), f"{question['id']}.{key}")

    def test_nonterminal_pages_have_a_forward_route(self):
        for page in self.preview_model["pages"]:
            if not page.get("terminal"):
                self.assertTrue(page.get("next") or page.get("routes"), page["id"])

    def test_terminal_pages_have_no_outgoing_navigation(self):
        for page in self.preview_model["pages"]:
            if page.get("terminal"):
                self.assertFalse(page.get("next"), page["id"])
                self.assertFalse(page.get("routes"), page["id"])

    def test_numeric_eligibility_has_plausibility_bounds(self):
        age = next(q for q in self.preview_pages["eligibility"]["questions"] if q["id"] == "age")
        self.assertEqual(0, age["min"])
        self.assertEqual(120, age["max"])

    def test_show_if_fields_reference_known_answers(self):
        question_ids = {q["id"] for p in self.preview_model["pages"] for q in p["questions"]}
        def fields(rule):
            if "all" in rule:
                return set().union(*(fields(r) for r in rule["all"]))
            if "any" in rule:
                return set().union(*(fields(r) for r in rule["any"]))
            return {rule["field"]}
        for page in self.preview_model["pages"]:
            for question in page["questions"]:
                if question.get("show_if"):
                    self.assertTrue(fields(question["show_if"]) <= question_ids | {"condition"})

    def test_generation_manifest_hashes_match_preview_artifacts(self):
        manifest = json.loads((ROOT / "examples" / "complete-study" / ".greedyq" / "generation-manifest.json").read_text())
        entries = {entry["path"]: entry for entry in manifest["artifacts"]}
        for relative in ("preview-model.json", "preview.html"):
            data = (ROOT / "examples" / "complete-study" / relative).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), entries[relative]["sha256"])
            self.assertEqual("validated", entries[relative]["status"])

    def test_preview_ui_spec_has_all_acceptance_sections(self):
        spec = (ROOT / "docs" / "preview-ui-spec.md").read_text()
        for heading in (
            "Default layout", "Respondent page anatomy", "Question presentation",
            "Validation and feedback", "Progress and navigation", "Researcher controls",
            "Preview safety", "Accessibility baseline", "Responsive and visual acceptance",
            "Required scenario suite", "Review evidence",
        ):
            self.assertIn(heading, spec)

    def test_markdown_documents_have_language_pairs(self):
        for path in ROOT.rglob("*.md"):
            if ".git" in path.parts:
                continue
            peer = path.with_name(path.name.replace("(kor).md", ".md")) if path.name.endswith("(kor).md") else path.with_name(path.stem + "(kor).md")
            self.assertTrue(peer.exists(), str(path))


if __name__ == "__main__":
    unittest.main()
