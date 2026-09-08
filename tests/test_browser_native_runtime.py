import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from greedyq.build import build, load_study
from greedyq.compiler import compile_preview


ROOT = Path(__file__).resolve().parents[1]
NODE = Path("/Users/dongsookim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node")


@unittest.skipUnless(NODE.is_file(), "bundled Node runtime is unavailable")
class BrowserNativeRuntimeTests(unittest.TestCase):
    def node(self, script, *args):
        result = subprocess.run([str(NODE), "-e", script, *map(str, args)], cwd=ROOT, text=True, capture_output=True, check=True)
        return json.loads(result.stdout)

    def test_js_core_matches_python_compiler_for_both_golden_studies(self):
        script = r'''const fs=require("fs"),gq=require("./web/greedyq-core.js"),base=process.argv[1];
const parsed=gq.parseSurvey(fs.readFileSync(base+"/survey.qmd","utf8"));
const config=gq.parseYaml(fs.readFileSync(base+"/greedyq.yml","utf8"));
console.log(JSON.stringify({report:gq.validateSurvey(parsed,config),model:gq.compileSurvey(parsed,config),pages:parsed.pages.length,questions:parsed.pages.flatMap(p=>p.questions).length}));'''
        for name in ("complete-study", "simple-satisfaction-study"):
            base = ROOT / "examples" / name
            actual = self.node(script, base)
            _, parsed, config = load_study(base)
            self.assertEqual("passed", actual["report"]["status"], actual["report"])
            self.assertEqual(compile_preview(parsed, config), actual["model"])
            self.assertEqual(len(parsed["pages"]), actual["pages"])
            self.assertEqual(sum(len(p["questions"]) for p in parsed["pages"]), actual["questions"])

    def test_mock_backend_persists_assignment_balances_and_withdraws(self):
        script = r'''const gq=require("./web/greedyq-core.js"),b=gq.createMemoryBackend(),cs=["control","treatment"],assigned=[];
for(let i=0;i<16;i++)assigned.push(b.assign("p"+i,cs));
b.save("p0",{page:"two",answers:{q:"yes"}});const resumed=b.load("p0");const stable=b.assign("p0",cs);b.clear("p0");
console.log(JSON.stringify({assigned,resumed,stable,deleted:b.load("p0"),inspect:b.inspect()}));'''
        result = self.node(script)
        self.assertEqual(8, result["assigned"].count("control"))
        self.assertEqual(8, result["assigned"].count("treatment"))
        self.assertEqual(result["assigned"][0], result["stable"])
        self.assertEqual({"q": "yes"}, result["resumed"]["answers"])
        self.assertIsNone(result["deleted"])

    def test_device_detection_covers_desktop_mobile_and_touch(self):
        script = r'''const gq=require("./web/greedyq-core.js");const fake=(match,touch,width)=>({matchMedia:()=>({matches:match}),navigator:{maxTouchPoints:touch},innerWidth:width});console.log(JSON.stringify([gq.detectDevice(fake(false,0,1400)),gq.detectDevice(fake(true,0,390)),gq.detectDevice(fake(false,5,700))]));'''
        self.assertEqual(["desktop", "mobile", "mobile"], self.node(script))

    def test_build_emits_fixed_static_bundle_without_node_or_python_dependency(self):
        source = ROOT / "examples" / "simple-satisfaction-study"
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "study"
            shutil.copytree(source, target, ignore=shutil.ignore_patterns("preview.html", "preview-model.json", "index.html", "greedyq-core.js", "greedyq-runtime.css", ".greedyq"))
            report, model = build(target)
            self.assertEqual("passed", report["status"])
            for name in ("index.html", "preview.html", "studio.html", "greedyq-core.js", "greedyq-runtime.css", "preview-model.json"):
                self.assertTrue((target / name).is_file(), name)
            self.assertEqual((ROOT / "web/greedyq-core.js").read_bytes(), (target / "greedyq-core.js").read_bytes())
            self.assertIn(json.dumps(model, ensure_ascii=False, separators=(",", ":")), (target / "index.html").read_text())

    def test_preview_has_two_renderers_and_no_external_connection(self):
        html = (ROOT / "templates/browser/preview.html").read_text()
        self.assertIn('id="desktop"', html)
        self.assertIn('id="mobile"', html)
        self.assertIn("connect-src 'none'", html)
        self.assertIn('mode:"desktop"', html)
        self.assertIn('mode:"mobile"', html)

    def test_browser_renderer_enforces_numeric_bounds_before_navigation(self):
        core = (ROOT / "web/greedyq-core.js").read_text()
        self.assertIn("function mountRespondentSafe", core)
        self.assertIn("tooLow", core)
        self.assertIn("tooHigh", core)
        self.assertIn("stopImmediatePropagation", core)

    def test_studio_parses_source_text_in_browser(self):
        html = (ROOT / "templates/browser/studio.html").read_text()
        for token in ("parseSurvey(qmd)", "parseYaml(yml)", "validateSurvey(parsed,config)", "compileSurvey(parsed,config)", "FileReader"):
            self.assertIn(token, html)

    def test_supabase_adapter_fails_closed_without_public_configuration(self):
        script = r'''const gq=require("./web/greedyq-core.js");let errors=[];for(const x of [{},{url:"http://bad",anonKey:"x"},{url:"https://ok"}])try{gq.createSupabaseBackend(x)}catch(e){errors.push(e.message)}console.log(JSON.stringify(errors));'''
        self.assertEqual(3, len(self.node(script)))


if __name__ == "__main__":
    unittest.main()
