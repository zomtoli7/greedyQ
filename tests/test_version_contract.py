import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_VERSION = "0.2"
ACTIVE_RELEASE = "0.2.0-draft.1"
LEGACY_TOKEN = "0." + "1"


class VersionContractTests(unittest.TestCase):
    def test_current_surveys_carry_a_release_identifier(self):
        pattern = re.compile(r'^0\.2_\d{4}-\d{2}-\d{2}_[0-9a-f]{7,12}$')
        readme_match = re.search(r'^- \*\*Current release:\*\* `([^`]+)`', (ROOT / "README.md").read_text(), re.MULTILINE)
        self.assertIsNotNone(readme_match)
        current_release = readme_match.group(1)
        self.assertRegex(current_release, pattern)
        for path in ROOT.glob("examples/*/survey.qmd"):
            match = re.search(r'^\s+version:\s+"([^"]+)"$', path.read_text(), re.MULTILINE)
            self.assertIsNotNone(match, path)
            self.assertRegex(match.group(1), pattern, path)
            self.assertEqual(current_release, match.group(1), path)
        self.assertIn(f"**Current release identifier:** `{current_release}`", (ROOT / "guides/core/guide.md").read_text())

    def test_new_study_requires_question_authoring_mode(self):
        start = (ROOT / "START-HERE.md").read_text()
        core = (ROOT / "guides/core/guide.md").read_text()
        for text in (start, core):
            self.assertIn("from scratch", text)
            self.assertIn("AI-assisted", text)
        self.assertIn("opening page and an ending page", start)

    def test_active_specification_and_archive_exist(self):
        self.assertTrue((ROOT / "docs/greedyq-v0.2-spec.md").is_file())
        self.assertTrue((ROOT / "docs/greedyq-v0.2-spec(kor).md").is_file())
        archive = ROOT / "docs/archive" / ("v" + LEGACY_TOKEN)
        self.assertTrue((archive / "README.md").is_file())
        self.assertTrue((archive / ("greedyq-v" + LEGACY_TOKEN + "-spec.md")).is_file())

    def test_registry_uses_only_the_active_release(self):
        registry = json.loads((ROOT / "registry/guide-index.json").read_text())
        self.assertEqual(ACTIVE_RELEASE, registry["release"])
        for component in registry["components"].values():
            self.assertEqual(ACTIVE_RELEASE, component["version"])

    def test_active_tree_contains_no_legacy_version_reference(self):
        excluded_roots = {
            ROOT / ".git",
            ROOT / ".greedyq",
            ROOT / "docs/archive" / ("v" + LEGACY_TOKEN),
        }
        # Match the retired greedyQ version as a version token, not an
        # unrelated decimal substring such as the surveydown DOI 10.1371/....
        legacy_version = re.compile(r"(?<![0-9])(?:v)?0[.]1(?:[._-]|(?![0-9]))", re.IGNORECASE)
        offenders = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or any(root in path.parents for root in excluded_roots):
                continue
            try:
                text = path.read_text()
            except UnicodeDecodeError:
                continue
            if legacy_version.search(text):
                offenders.append(str(path.relative_to(ROOT)))
        self.assertEqual([], offenders)

    def test_active_ai_schemas_use_the_active_version(self):
        for path in (ROOT / "schemas/ai").glob("*.schema.json"):
            schema = json.loads(path.read_text())
            version = schema.get("properties", {}).get("schema_version", {})
            if "const" in version:
                self.assertEqual(ACTIVE_VERSION, version["const"], path.name)


if __name__ == "__main__":
    unittest.main()
