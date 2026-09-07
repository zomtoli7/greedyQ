import hashlib
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "examples" / "simple-satisfaction-study"


def read_json(relative):
    return json.loads((STUDY / relative).read_text())


def digest(relative):
    return hashlib.sha256((STUDY / relative).read_bytes()).hexdigest()


def rule_matches(rule, answers):
    if "all" in rule:
        return all(rule_matches(item, answers) for item in rule["all"])
    if "any" in rule:
        return any(rule_matches(item, answers) for item in rule["any"])
    actual = answers.get(rule["field"])
    if "equals" in rule:
        return actual == rule["equals"]
    if actual is None:
        return False
    if "lt" in rule:
        return float(actual) < rule["lt"]
    if "lte" in rule:
        return float(actual) <= rule["lte"]
    if "gt" in rule:
        return float(actual) > rule["gt"]
    if "gte" in rule:
        return float(actual) >= rule["gte"]
    return False


class SimpleSatisfactionStudyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = read_json("preview-model.json")
        cls.pages = {page["id"]: page for page in cls.model["pages"]}
        cls.questions = {question["id"]: question for page in cls.model["pages"] for question in page["questions"]}
        cls.qmd = (STUDY / "survey.qmd").read_text()

    def next_page(self, page_id, answers):
        page = self.pages[page_id]
        for route in page.get("routes", []):
            if rule_matches(route["when"], answers):
                return route["to"]
        return page.get("next")

    def test_object_is_simple_and_lock_matches_resolver(self):
        study = read_json("greedyq.study.json")
        object_schema = json.loads((ROOT / "schemas" / "greedyq-study.schema.json").read_text())
        self.assertEqual([], list(Draft202012Validator(object_schema).iter_errors(study)))
        self.assertEqual("greedyQSimple", study["object"])
        self.assertEqual("simple", study["profile"])
        self.assertNotIn("preregistration", study["modules"])
        self.assertNotIn("prolific", study["modules"])
        output = subprocess.run(
            [sys.executable, "tools/resolve_guide.py", "--profile", "simple", "--module", "consent", "--module", "deployment-vercel-supabase"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        )
        self.assertEqual(json.loads(output.stdout), read_json(".greedyq/guide-lock.json"))

    def test_all_internal_state_files_match_schemas(self):
        for schema_path in (ROOT / "schemas" / "ai").glob("*.schema.json"):
            state_path = STUDY / ".greedyq" / schema_path.name.replace(".schema", "")
            schema = json.loads(schema_path.read_text())
            self.assertTrue(state_path.exists(), state_path.name)
            self.assertEqual([], list(Draft202012Validator(schema).iter_errors(json.loads(state_path.read_text()))), state_path.name)

    def test_preview_model_matches_schema(self):
        schema = json.loads((ROOT / "schemas" / "preview-model.schema.json").read_text())
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(self.model)))

    def test_qmd_and_preview_have_identical_pages_and_questions(self):
        qmd_pages = set(re.findall(r"(?m)^--- ([a-z][a-z0-9_]*)$", self.qmd))
        qmd_questions = set(re.findall(r'(?m)^\s*id\s*=\s*"([a-z][a-z0-9_]*)"', self.qmd))
        self.assertEqual(qmd_pages, set(self.pages))
        self.assertEqual(qmd_questions, set(self.questions))
        self.assertEqual(len(self.model["pages"]), len(self.pages))
        self.assertEqual(sum(len(page["questions"]) for page in self.model["pages"]), len(self.questions))
        for page in self.model["pages"]:
            if page.get("terminal"):
                self.assertFalse(page.get("next") or page.get("routes"), page["id"])
            else:
                self.assertTrue(page.get("next") or page.get("routes"), page["id"])
            for target in [page.get("next")] + [route["to"] for route in page.get("routes", [])]:
                if target:
                    self.assertIn(target, self.pages)

    def test_display_labels_and_stored_values_match_qmd(self):
        qmd_vectors = {}
        qmd_rows = {}
        for chunk in re.findall(r"```\{r\}(.*?)```", self.qmd, re.S):
            qid = re.search(r'id\s*=\s*"([a-z][a-z0-9_]*)"', chunk)
            if not qid:
                continue
            for key, target in (("option", qmd_vectors), ("row", qmd_rows)):
                vector = re.search(rf"{key}\s*=\s*c\((.*?)\n\s*\)", chunk, re.S)
                if vector:
                    pairs = re.findall(r'^\s*"([^"]+)"\s*=\s*("[^"]+"|-?\d+(?:\.\d+)?)\s*,?$', vector.group(1), re.M)
                    target[qid.group(1)] = [(label, json.loads(value)) for label, value in pairs]
        for question_id, question in self.questions.items():
            if question_id in qmd_vectors:
                self.assertEqual(qmd_vectors[question_id], [(item["label"], item["value"]) for item in question["options"]], question_id)
            if question_id in qmd_rows:
                self.assertEqual(qmd_rows[question_id], [(item["label"], item["value"]) for item in question["rows"]], question_id)

    def test_simple_study_has_no_randomization_or_condition_routes(self):
        config = (STUDY / "greedyq.yml").read_text()
        self.assertNotRegex(config, r"(?m)^randomization:")
        self.assertEqual(["default"], self.model["conditions"])
        self.assertFalse(any(route["when"].get("field") == "condition" for page in self.model["pages"] for route in page.get("routes", [])))

    def test_eligible_happy_path_and_early_exit_routes(self):
        self.assertEqual("eligibility", self.next_page("consent", {"consent_choice": "yes"}))
        self.assertEqual("consent_refused", self.next_page("consent", {"consent_choice": "no"}))
        self.assertEqual("screened_out", self.next_page("eligibility", {"age": 17, "used_greedyq": "yes"}))
        self.assertEqual("screened_out", self.next_page("eligibility", {"age": 25, "used_greedyq": "no"}))
        self.assertEqual("usage", self.next_page("eligibility", {"age": 25, "used_greedyq": "yes"}))
        self.assertEqual("complete", self.next_page("participant_control", {"withdraw_now": "submit"}))
        self.assertEqual("withdrawn", self.next_page("participant_control", {"withdraw_now": "withdraw"}))

    def test_feedback_questions_follow_consent_and_eligibility(self):
        path = self.model["progress_paths"]["default"]
        self.assertLess(path.index("consent"), path.index("eligibility"))
        self.assertLess(path.index("eligibility"), path.index("usage"))
        self.assertLess(path.index("usage"), path.index("evaluation"))

    def test_conditional_followups_cover_show_and_hide_states(self):
        self.assertTrue(rule_matches(self.questions["primary_use_other"]["show_if"], {"primary_use": "other"}))
        self.assertFalse(rule_matches(self.questions["primary_use_other"]["show_if"], {"primary_use": "new_survey"}))
        self.assertTrue(rule_matches(self.questions["low_satisfaction_reason"]["show_if"], {"overall_satisfaction": 3}))
        self.assertFalse(rule_matches(self.questions["low_satisfaction_reason"]["show_if"], {"overall_satisfaction": 4}))
        for question_id in ("problem_area", "problem_detail"):
            self.assertTrue(rule_matches(self.questions[question_id]["show_if"], {"had_problem": "yes"}))
            self.assertFalse(rule_matches(self.questions[question_id]["show_if"], {"had_problem": "no"}))
        self.assertTrue(rule_matches(self.questions["deletion_request"]["show_if"], {"withdraw_now": "withdraw"}))
        self.assertFalse(rule_matches(self.questions["deletion_request"]["show_if"], {"withdraw_now": "submit"}))
        for question in self.questions.values():
            if question.get("show_if"):
                self.assertIn(question["show_if"]["field"], self.questions)

    def test_numeric_bounds_and_conditional_requirements_are_explicit(self):
        self.assertEqual((0, 120), (self.questions["age"]["min"], self.questions["age"]["max"]))
        self.assertEqual((0, 10), (self.questions["recommend_score"]["min"], self.questions["recommend_score"]["max"]))
        self.assertTrue(self.questions["problem_area"]["required"])
        self.assertTrue(self.questions["deletion_request"]["required"])
        config = (STUDY / "greedyq.yml").read_text()
        self.assertIn('not answered(problem_area)', config)
        self.assertIn('not answered(deletion_request)', config)
        front = self.qmd.split("---", 2)[1]
        block = re.search(r"required:\n((?:\s+- [a-z0-9_]+\n)+)", front)
        required_qmd = set(re.findall(r"- ([a-z0-9_]+)", block.group(1)))
        required_preview = {question["id"] for question in self.questions.values() if question.get("required")}
        self.assertEqual(required_qmd | {"problem_area", "deletion_request"}, required_preview)

    def test_all_five_outcomes_exist_and_no_redirects_are_embedded(self):
        outcomes = {page.get("terminal") for page in self.model["pages"] if page.get("terminal")}
        self.assertEqual({"completed", "screened_out", "consent_refused", "withdrawn", "technical_error"}, outcomes)
        self.assertNotIn("https://", json.dumps(self.model).lower())
        self.assertEqual(5, (STUDY / "greedyq.yml").read_text().count("redirect: null"))

    def test_preview_is_reproducible_and_embeds_exact_model(self):
        before = (STUDY / "preview.html").read_bytes()
        result = subprocess.run(
            [sys.executable, "tools/build_reference_preview.py", "--study-dir", "examples/simple-satisfaction-study"],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(before, (STUDY / "preview.html").read_bytes())
        match = re.search(r'<script id="greedyq-model" type="application/json">(.*?)</script>', before.decode(), re.S)
        self.assertEqual(self.model, json.loads(match.group(1)))

    def test_manifest_covers_every_declared_artifact_with_current_hash(self):
        manifest = read_json(".greedyq/generation-manifest.json")
        entries = {item["path"]: item for item in manifest["artifacts"]}
        state = read_json(".greedyq/study-state.json")
        self.assertEqual(set(state["artifact_paths"]), set(entries))
        for path, entry in entries.items():
            self.assertEqual(digest(path), entry["sha256"], path)
        decision_ids = {item["decision_id"] for item in read_json(".greedyq/decision-log.json")["decisions"]}
        for entry in entries.values():
            self.assertTrue(set(entry["based_on_decision_ids"]) <= decision_ids, entry["path"])

    def test_consent_hash_matches_config(self):
        config = (STUDY / "greedyq.yml").read_text()
        self.assertIn(f"sha256: {digest('consent.md')}", config)

    def test_analysis_language_is_descriptive_not_causal(self):
        analysis = (STUDY / "analysis" / "README.md").read_text().lower()
        self.assertIn("exploratory", analysis)
        self.assertIn("avoid causal language", analysis)
        self.assertIn("do not exclude completed responses merely because they are unfavorable", analysis)

    def test_instrument_does_not_request_direct_identifiers(self):
        labels = " ".join(question["label"].lower() for question in self.questions.values())
        for prohibited in ("your name", "email address", "your institution", "api key", "password"):
            self.assertNotIn(prohibited, labels)


if __name__ == "__main__":
    unittest.main()
