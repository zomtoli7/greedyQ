import json
import subprocess
import shutil
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from greedyq.build import build, load_study
from greedyq.compiler import compile_preview
from greedyq.parser import ParseError, parse_qmd
from greedyq.validator import validate


ROOT = Path(__file__).resolve().parents[1]
SUPPORTED_TYPES_FOR_TEST = {"text", "textarea", "numeric", "mc", "mc_multiple", "mc_buttons", "mc_multiple_buttons", "mc_image", "mc_multiple_image", "select", "slider", "slider_numeric", "date", "daterange", "matrix", "matrix_multiple", "audio", "video", "rank_order", "side_by_side", "nps", "timing", "constant_sum", "pick_group_rank", "drill_down", "custom"}


class RuntimePipelineTests(unittest.TestCase):
    def test_both_golden_studies_parse_validate_and_compile(self):
        schema = json.loads((ROOT / "schemas/preview-model.schema.json").read_text())
        for name, pages, questions in (("complete-study", 15, 16), ("simple-satisfaction-study", 13, 23)):
            study, parsed, config = load_study(ROOT / "examples" / name)
            self.assertEqual(pages, len(parsed["pages"]))
            self.assertEqual(questions, sum(len(page["questions"]) for page in parsed["pages"]))
            report = validate(parsed, config, study / "survey.qmd", study / "greedyq.yml")
            self.assertEqual("passed", report["status"], report)
            model = compile_preview(parsed, config)
            self.assertEqual([], list(Draft202012Validator(schema).iter_errors(model)))

    def test_golden_manifests_track_parser_outputs(self):
        for name in ("complete-study", "simple-satisfaction-study"):
            manifest = json.loads((ROOT / "examples" / name / ".greedyq/generation-manifest.json").read_text())
            paths = {item["path"] for item in manifest["artifacts"]}
            self.assertIn(".greedyq/normalized-survey.json", paths)
            self.assertIn(".greedyq/validation-report.runtime.json", paths)

    def test_build_is_deterministic_and_embeds_exact_model(self):
        source = ROOT / "examples/simple-satisfaction-study"
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "study"
            shutil.copytree(source, target, ignore=shutil.ignore_patterns("preview.html", "preview-model.json", ".greedyq"))
            first_report, first = build(target)
            first_html = (target / "preview.html").read_bytes()
            second_report, second = build(target)
            self.assertEqual("passed", first_report["status"])
            self.assertEqual(first_report, second_report)
            self.assertEqual(first, second)
            self.assertEqual(first_html, (target / "preview.html").read_bytes())
            self.assertTrue((target / ".greedyq/normalized-survey.json").is_file())
            self.assertTrue((target / ".greedyq/validation-report.runtime.json").is_file())

    def test_reversed_choices_are_blocked_with_plain_guidance(self):
        parsed = parse_qmd(ROOT / "tests/fixtures/reversed-option/survey.qmd")
        report = validate(parsed, {"spec_version": "0.2"})
        issue = next(item for item in report["issues"] if item["code"] == "GQ011")
        self.assertEqual("failed", report["status"])
        self.assertIn("Displayed label", issue["message"])
        self.assertIn("stored_value", issue["message"])

    def test_missing_question_id_is_blocked_before_writing_preview(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "survey.qmd").write_text('''---\ntitle: "Broken"\ngreedyq:\n  spec_version: "0.2"\nsurvey-settings:\n  start-page: welcome\n---\n\n--- welcome\n\n# Welcome\n\n```{r}\nsd_question(type = "text", label = "Your answer")\n```\n''')
            (target / "greedyq.yml").write_text('spec_version: "0.2"\nstudy:\n  id: broken_study\n  title: Broken\n')
            report, model = build(target)
            self.assertEqual("failed", report["status"])
            self.assertIsNone(model)
            self.assertFalse((target / "preview.html").exists())
            self.assertTrue(any("missing its id" in item["message"] for item in report["issues"]))

    def test_missing_route_target_is_blocked(self):
        study, parsed, config = load_study(ROOT / "examples/simple-satisfaction-study")
        config["logic"]["skip"][0]["to"] = "page_that_does_not_exist"
        report = validate(parsed, config)
        self.assertEqual("failed", report["status"])
        self.assertTrue(any("points to missing page" in item["message"] for item in report["issues"]))

    def test_condition_routes_and_conditional_questions_compile(self):
        _, parsed, config = load_study(ROOT / "examples/complete-study")
        model = compile_preview(parsed, config)
        pages = {page["id"]: page for page in model["pages"]}
        self.assertEqual(["control", "treatment"], model["conditions"])
        self.assertEqual("stimulus_control", pages["baseline"]["routes"][0]["to"])
        opposition = next(q for q in pages["outcomes"]["questions"] if q["id"] == "opposition_reason")
        self.assertEqual({"field": "support_post", "lte": 3}, opposition["show_if"])

    def test_preview_runtime_includes_supported_input_and_safety_behaviors(self):
        core = (ROOT / "web/greedyq-core.js").read_text()
        preview = (ROOT / "templates/browser/preview.html").read_text()
        for required in ("mc_multiple", "createLocalMockBackend", "createSupabaseBackend", "localStorage"):
            self.assertIn(required, core)
        for required in ('id="desktop"', 'id="mobile"', "connect-src 'none'"):
            self.assertIn(required, preview)
        for forbidden in ("XMLHttpRequest", "WebSocket", "eval("):
            self.assertNotIn(forbidden, core)

    def test_malformed_call_reports_its_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            qmd = Path(tmp) / "survey.qmd"
            qmd.write_text('''---\ngreedyq:\n  spec_version: "0.2"\n---\n\n--- welcome\n```{r}\nsd_question(id = "q1", type = "text", label = "Question"\n```\n''')
            with self.assertRaises(ParseError) as caught:
                parse_qmd(qmd)
            self.assertIsNotNone(caught.exception.line)
            self.assertIn("closing parenthesis", str(caught.exception))

    def test_supported_question_types_compile_from_qmd(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "survey.qmd").write_text('''---
title: "Question types"
greedyq:
  spec_version: "0.2"
  version: "0.2_2026-09-09_9d9ffe9"
survey-settings:
  start-page: questions
  required: [single, multiple, grid]
---

--- questions

# Try every input

```{r}
sd_question(id = "short", type = "text", label = "Short answer")
```
```{r}
sd_question(id = "long", type = "textarea", label = "Long answer")
```
```{r}
sd_question(id = "number", type = "numeric", label = "Number", min = 0, max = 10)
```
```{r}
sd_question(id = "single", type = "mc", label = "Choose one", option = c("Alpha" = "a", "Beta" = "b"))
```
```{r}
sd_question(id = "multiple", type = "mc_multiple", label = "Choose several", option = c("Alpha" = "a", "Beta" = "b"))
```
```{r}
sd_question(id = "buttons", type = "mc_buttons", label = "Buttons", option = c("Alpha" = "a", "Beta" = "b"), direction = "vertical", justified = TRUE)
```
```{r}
sd_question(id = "multi_buttons", type = "mc_multiple_buttons", label = "Several buttons", option = c("Alpha" = "a", "Beta" = "b"))
```
```{r}
sd_question(id = "picture", type = "mc_image", label = "Picture", option = c("Cat" = "cat", "Dog" = "dog"), image = c("images/cat.png", "images/dog.png"))
```
```{r}
sd_question(id = "pictures", type = "mc_multiple_image", label = "Pictures", option = c("Cat" = "cat", "Dog" = "dog"), image = c("images/cat.png", "images/dog.png"))
```
```{r}
sd_question(id = "menu", type = "select", label = "Menu", option = c("Alpha" = "a", "Beta" = "b"))
```
```{r}
sd_question(id = "scale", type = "slider", label = "Scale", option = c("Low" = 1, "High" = 2), orientation = "vertical")
```
```{r}
sd_question(id = "amount", type = "slider_numeric", label = "Amount", option = seq(0, 10, 1), default = c(3, 5), sep = " to ")
```
```{r}
sd_question(id = "day", type = "date", label = "Day")
```
```{r}
sd_question(id = "days", type = "daterange", label = "Date range")
```
```{r}
sd_question(id = "grid", type = "matrix", label = "Grid", row = c("First" = "r1"), option = c("No" = 0, "Yes" = 1))
```
```{r}
sd_question(id = "multi_grid", type = "matrix_multiple", label = "Grid multiple", row = c("First" = "r1"), option = c("No" = 0, "Yes" = 1))
```
```{r}
sd_question(id = "audio_clip", type = "audio", label = "Audio clip", src = "media/clip.mp3", controls = TRUE, transcript = "Sample transcript")
```
```{r}
sd_question(id = "video_clip", type = "video", label = "Video clip", src = "https://example.org/clip.mp4", poster = "images/poster.png", controls = TRUE)
```
```{r}
sd_question(id = "rank", type = "rank_order", label = "Rank", option = c("A" = "a", "B" = "b"))
```
```{r}
sd_question(id = "side", type = "side_by_side", label = "Side", column = c("Now" = "now", "Later" = "later"), row = c("A" = "a"), option = c("Low" = 1, "High" = 2))
```
```{r}
sd_question(id = "recommend", type = "nps", label = "Recommend")
```
```{r}
sd_question(id = "page_time", type = "timing", label = "Timing")
```
```{r}
sd_question(id = "allocation", type = "constant_sum", label = "Allocate", option = c("A" = "a", "B" = "b"), total = 100)
```
```{r}
sd_question(id = "organize", type = "pick_group_rank", label = "Organize", option = c("A" = "a", "B" = "b"), group = c("First" = "first", "Second" = "second"))
```
```{r}
sd_question(id = "location", type = "drill_down", label = "Location", option = c("Asia > Korea" = "kr", "Europe > France" = "fr"))
```
```{r}
sd_question(id = "customized", type = "custom", base_type = "mc_buttons", label = "Customized", option = c("A" = "a", "B" = "b"), customization = "Confirmed")
```

--- done

# Done
''')
            (target / "greedyq.yml").write_text('''spec_version: "0.2"
study:
  id: question_types
  title: Question types
outcomes:
  complete:
    page: done
    lifecycle_state: completed
''')
            report, model = build(target)
            self.assertEqual("passed", report["status"], report)
            types = {q["type"] for q in model["pages"][0]["questions"]}
            self.assertEqual(SUPPORTED_TYPES_FOR_TEST, types)
            questions = {q["id"]: q for q in model["pages"][0]["questions"]}
            self.assertEqual("vertical", questions["scale"]["orientation"])
            self.assertEqual([3, 5], questions["amount"]["default"])
            self.assertEqual(0, questions["amount"]["options"][0]["value"])
            self.assertEqual("vertical", questions["buttons"]["direction"])
            schema = json.loads((ROOT / "schemas/preview-model.schema.json").read_text())
            self.assertEqual([], list(Draft202012Validator(schema).iter_errors(model)))
            node = Path("/Users/dongsookim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node")
            if node.is_file():
                script = '''const fs=require("fs"),gq=require("./web/greedyq-core.js"),p=process.argv[1];const parsed=gq.parseSurvey(fs.readFileSync(p+"/survey.qmd","utf8"));const config=gq.parseYaml(fs.readFileSync(p+"/greedyq.yml","utf8"));console.log(JSON.stringify({report:gq.validateSurvey(parsed,config),model:gq.compileSurvey(parsed,config)}));'''
                result = subprocess.run([str(node), "-e", script, str(target)], cwd=ROOT, text=True, capture_output=True, check=True)
                browser = json.loads(result.stdout)
                self.assertEqual("passed", browser["report"]["status"], browser["report"])
                self.assertEqual(model, browser["model"])

    def test_raw_html_is_rejected_before_preview(self):
        _, parsed, config = load_study(ROOT / "examples/simple-satisfaction-study")
        parsed["pages"][0]["body"] += "<script>bad()</script>"
        report = validate(parsed, config)
        self.assertEqual("failed", report["status"])
        self.assertTrue(any("raw HTML" in item["message"] for item in report["issues"]))


if __name__ == "__main__":
    unittest.main()
