import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]


class GenerationContractTests(unittest.TestCase):
    def test_reference_ai_state_matches_published_schemas(self):
        schema_dir = ROOT / "schemas" / "ai"
        state_dir = ROOT / "examples" / "complete-study" / ".greedyq"
        for schema_path in schema_dir.glob("*.schema.json"):
            state_path = state_dir / schema_path.name.replace(".schema", "")
            schema = json.loads(schema_path.read_text())
            state = json.loads(state_path.read_text())
            errors = list(Draft202012Validator(schema).iter_errors(state))
            self.assertEqual([], errors, state_path.name)

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


if __name__ == "__main__":
    unittest.main()
