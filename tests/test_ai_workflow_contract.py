import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AIWorkflowContractTests(unittest.TestCase):
    def test_all_researcher_journey_scenarios_are_normatively_covered(self):
        scenarios = json.loads((ROOT / "tests/fixtures/ai-workflow-scenarios.json").read_text())["scenarios"]
        corpus = "\n".join((ROOT / path).read_text() for path in (
            "guides/core/guide.md", "guides/core/communication.md", "guides/core/checkpoints.json",
        ))
        missing = {scenario["id"]: [phrase for phrase in scenario["requires"] if phrase.lower() not in corpus.lower()] for scenario in scenarios}
        missing = {key: value for key, value in missing.items() if value}
        self.assertEqual({}, missing)

    def test_scenarios_cover_new_modify_fork_and_both_authoring_modes(self):
        ids = {item["id"] for item in json.loads((ROOT / "tests/fixtures/ai-workflow-scenarios.json").read_text())["scenarios"]}
        self.assertTrue({"new_researcher_written", "new_ai_assisted", "modify", "fork"} <= ids)


if __name__ == "__main__": unittest.main()
