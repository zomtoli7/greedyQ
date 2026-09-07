import hashlib
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load_json(relative):
    return json.loads((ROOT / relative).read_text())


def digest(relative):
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def load_resolver():
    spec = importlib.util.spec_from_file_location("resolve_guide", ROOT / "tools" / "resolve_guide.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ModularGuideTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = load_json("registry/guide-index.json")
        cls.components = cls.registry["components"]
        cls.resolver = load_resolver()

    def test_registry_matches_schema(self):
        schema = load_json("schemas/guide/guide-index.schema.json")
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(self.registry)))

    def test_registered_manifests_and_files_match_hashes(self):
        for component in self.components.values():
            self.assertEqual(digest(component["manifest"]), component["manifest_sha256"])
            for file in component["files"]:
                self.assertEqual(digest(file["path"]), file["sha256"])

    def test_registry_build_is_reproducible(self):
        before = (ROOT / "registry" / "guide-index.json").read_bytes()
        result = subprocess.run([sys.executable, "tools/build_guide_registry.py"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(before, (ROOT / "registry" / "guide-index.json").read_bytes())

    def test_initial_profiles_are_simple_and_experiment(self):
        profiles = {key for key, value in self.components.items() if value["kind"] == "profile"}
        self.assertEqual({"simple", "experiment"}, profiles)
        self.assertEqual("greedyQSimple", self.components["simple"]["object_name"])
        self.assertEqual("greedyQExperiment", self.components["experiment"]["object_name"])

    def test_simple_resolution_contains_only_core_and_profile(self):
        lock = self.resolver.resolve("simple", [])
        self.assertEqual(["core", "simple"], [item["id"] for item in lock["resolved_components"]])
        self.assertEqual([], lock["modules"])

    def test_experiment_resolution_includes_transitive_dependencies(self):
        lock = self.resolver.resolve("experiment", ["prolific"])
        ids = [item["id"] for item in lock["resolved_components"]]
        self.assertEqual(["core", "experiment", "governance-irb", "consent", "prolific"], ids)
        self.assertEqual(["consent", "governance-irb", "prolific"], lock["modules"])

    def test_resolver_rejects_unknown_and_wrong_kind_modules(self):
        with self.assertRaisesRegex(ValueError, "unknown profile"):
            self.resolver.resolve("cbc", [])
        with self.assertRaisesRegex(ValueError, "unknown module"):
            self.resolver.resolve("experiment", ["simple"])

    def test_all_dependencies_exist_and_graph_is_acyclic(self):
        visited = set()
        active = set()
        def visit(component_id):
            self.assertNotIn(component_id, active)
            if component_id in visited:
                return
            active.add(component_id)
            for dependency in self.components[component_id]["dependencies"]:
                self.assertIn(dependency, self.components)
                visit(dependency)
            active.remove(component_id)
            visited.add(component_id)
        for component_id in self.components:
            visit(component_id)

    def test_golden_study_object_matches_schema_and_profile(self):
        study = load_json("examples/complete-study/greedyq.study.json")
        schema = load_json("schemas/greedyq-study.schema.json")
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(study)))
        self.assertEqual(self.components[study["profile"]]["object_name"], study["object"])

    def test_golden_guide_lock_is_current_and_schema_valid(self):
        study = load_json("examples/complete-study/greedyq.study.json")
        lock = load_json("examples/complete-study/.greedyq/guide-lock.json")
        schema = load_json("schemas/guide/guide-lock.schema.json")
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(lock)))
        expected = self.resolver.resolve(study["profile"], study["modules"])
        self.assertEqual(expected, lock)

    def test_golden_object_artifacts_are_manifested_with_current_hashes(self):
        manifest = load_json("examples/complete-study/.greedyq/generation-manifest.json")
        artifacts = {item["path"]: item for item in manifest["artifacts"]}
        for relative in ("greedyq.study.json", "study-plan.md", ".greedyq/guide-lock.json", ".greedyq/validation-report.json"):
            self.assertEqual(digest("examples/complete-study/" + relative), artifacts[relative]["sha256"])
            self.assertEqual("validated", artifacts[relative]["status"])

    def test_internal_validation_report_matches_schema(self):
        report = load_json("examples/complete-study/.greedyq/validation-report.json")
        schema = load_json("schemas/ai/validation-report.schema.json")
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(report)))
        self.assertEqual("incomplete", report["overall_status"])
        self.assertTrue(any(gate["id"] == "interactive_preview" and gate["status"] == "pending" for gate in report["manual_gates"]))

    def test_researcher_plan_avoids_internal_diagnostics(self):
        plan = (ROOT / "examples" / "complete-study" / "study-plan.md").read_text().lower()
        for term in ("schema", "manifest", "referential integrity", "route graph", "rls", "csp"):
            self.assertNotIn(term, plan)
        positioning_files = (
            "README.md", "START-HERE.md", "docs/product-brief.md",
            "docs/greedyq-v0.1-spec.md", "docs/modular-guide-architecture.md",
            "guides/core/guide.md",
        )
        for relative in positioning_files:
            text = (ROOT / relative).read_text()
            self.assertIn("agent-executable application specification", text, relative)
            self.assertRegex(text, r"greedyQ (itself )?is not an agent", relative)


if __name__ == "__main__":
    unittest.main()
