import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ACTIVE_VERSION = "0.2"
ACTIVE_RELEASE = "0.2.0-draft.1"
LEGACY_TOKEN = "0." + "1"


class VersionContractTests(unittest.TestCase):
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
        offenders = []
        for path in ROOT.rglob("*"):
            if not path.is_file() or any(root in path.parents for root in excluded_roots):
                continue
            try:
                text = path.read_text()
            except UnicodeDecodeError:
                continue
            if LEGACY_TOKEN in text:
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
