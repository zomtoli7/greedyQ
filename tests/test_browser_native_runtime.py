import json
import copy
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from greedyq.build import build, load_study
from greedyq.compiler import compile_preview
from greedyq.validator import validate


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
        for name in ("complete-study", "simple-satisfaction-study", "control-gallery"):
            base = ROOT / "examples" / name
            actual = self.node(script, base)
            _, parsed, config = load_study(base)
            self.assertEqual("passed", actual["report"]["status"], actual["report"])
            self.assertEqual(compile_preview(parsed, config), actual["model"])
            self.assertEqual(len(parsed["pages"]), actual["pages"])
            self.assertEqual(sum(len(p["questions"]) for p in parsed["pages"]), actual["questions"])

    def test_js_validator_matches_python_reference_diagnostics(self):
        _, parsed0, config0 = load_study(ROOT / "examples/complete-study")
        cases = []
        parsed, config = copy.deepcopy(parsed0), copy.deepcopy(config0); parsed["front_matter"]["unknown"] = True; cases.append((parsed, config))
        parsed, config = copy.deepcopy(parsed0), copy.deepcopy(config0); parsed["pages"][2]["questions"][0]["options"] = [{"label":"A","value":"x"},{"label":"B","value":"x"}]; cases.append((parsed, config))
        parsed, config = copy.deepcopy(parsed0), copy.deepcopy(config0); parsed["pages"][0]["questions"].append({"id":parsed["pages"][0]["id"],"type":"text","label":"Overlap","_line":1}); cases.append((parsed, config))
        parsed, config = copy.deepcopy(parsed0), copy.deepcopy(config0); config["randomization"][0]["persistence_key"] = None; cases.append((parsed, config))
        parsed, config = copy.deepcopy(parsed0), copy.deepcopy(config0); config["consent"]["accept_value"] = "missing"; cases.append((parsed, config))
        parsed, config = copy.deepcopy(parsed0), copy.deepcopy(config0); config["outcomes"]["complete"]["redirect"] = "http://unsafe.test"; cases.append((parsed, config))
        script = 'const gq=require("./web/greedyq-core.js"),x=JSON.parse(require("fs").readFileSync(0,"utf8"));console.log(JSON.stringify(gq.validateSurvey(x.parsed,x.config)));'
        for parsed, config in cases:
            expected = validate(parsed, config)
            proc = subprocess.run([str(NODE), "-e", script], cwd=ROOT, input=json.dumps({"parsed":parsed,"config":config}), text=True, capture_output=True, check=True)
            actual = json.loads(proc.stdout)
            self.assertEqual([(x["code"],x["message"]) for x in expected["issues"]], [(x["code"],x["message"]) for x in actual["issues"]])

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

    def test_local_mock_resumes_after_refresh_and_rejects_stale_tab_writes(self):
        script = r'''const values=new Map();global.localStorage={getItem:key=>values.get(key)||null,setItem:(key,value)=>values.set(key,value),removeItem:key=>values.delete(key)};
const gq=require("./web/greedyq-core.js"),first=gq.createLocalMockBackend("tabs"),second=gq.createLocalMockBackend("tabs"),a={page:"one",answers:{q:"a"},_revision:0};
const saved=first.save("person",a),stale=second.load("person"),fresh=first.load("person");fresh.page="two";first.save("person",fresh);stale.page="three";const conflict=second.save("person",stale),refreshed=gq.createLocalMockBackend("tabs").load("person");
console.log(JSON.stringify({saved,conflict,refreshed}));'''
        result = self.node(script)
        self.assertEqual("saved", result["saved"]["status"])
        self.assertEqual("conflict", result["conflict"]["status"])
        self.assertEqual("two", result["refreshed"]["page"])
        self.assertEqual(2, result["refreshed"]["_revision"])

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
        self.assertIn('id="structure-open"', html)
        self.assertIn('id="structure-dialog"', html)
        self.assertIn("question.type", html)
        compact = "".join(html.split())
        self.assertIn('mode:"desktop"', compact)
        self.assertIn('mode:"mobile"', compact)

    def test_browser_renderer_enforces_numeric_bounds_before_navigation(self):
        core = (ROOT / "web/greedyq-core.js").read_text()
        self.assertIn("function mountRespondentSafe", core)
        self.assertIn("tooLow", core)
        self.assertIn("tooHigh", core)
        self.assertIn("stopImmediatePropagation", core)

    def test_browser_renderer_defers_assignment_until_declared_boundary(self):
        core = (ROOT / "web/greedyq-core.js").read_text()
        compact = "".join(core.split())
        self.assertIn("assignmentAllowed=!model.assignment_page", compact)
        self.assertIn("model.assignment_page===page?.id", compact)
        self.assertIn("remote.assign(sid,conditions)", compact)
        self.assertNotIn("assigned=loaded?.condition||await remote.assign", core)

    def test_studio_parses_source_text_in_browser(self):
        html = (ROOT / "templates/browser/studio.html").read_text()
        html = "".join(html.split())
        for token in ("parseSurvey(qmd)", "parseYaml(yml)", "validateSurvey(parsed,config)", "compileSurvey(parsed,config)", "FileReader"):
            self.assertIn(token, html)

    def test_supabase_adapter_fails_closed_without_public_configuration(self):
        script = r'''const gq=require("./web/greedyq-core.js");let errors=[];for(const x of [{},{url:"http://bad",anonKey:"x"},{url:"https://ok"}])try{gq.createSupabaseBackend(x)}catch(e){errors.push(e.message)}console.log(JSON.stringify(errors));'''
        self.assertEqual(3, len(self.node(script)))

    def test_browser_prolific_contract_and_stable_session_support(self):
        core = (ROOT / "web/greedyq-core.js").read_text()
        respondent = (ROOT / "templates/browser/respondent.html").read_text()
        for token in ("PROLIFIC_PID", "STUDY_ID", "SESSION_ID"):
            self.assertIn(token, core)
        self.assertIn("parseProlificLaunch(location.search", "".join(respondent.split()))
        self.assertIn("stableSessionId", respondent)
        result = self.node('const gq=require("./web/greedyq-core.js");console.log(JSON.stringify(gq.parseProlificLaunch("?PROLIFIC_PID=p&STUDY_ID=s&SESSION_ID=x","test")));')
        self.assertEqual("passed", result["status"])

    def test_accessibility_and_mobile_contract_is_present(self):
        core = (ROOT / "web/greedyq-core.js").read_text()
        css = (ROOT / "web/greedyq-runtime.css").read_text()
        html = (ROOT / "templates/browser/respondent.html").read_text()
        for token in ('<html lang="en">', 'name="viewport"'):
            self.assertIn(token, html)
        for token in ("<fieldset", "<legend", 'role="alert"', "aria-live"):
            self.assertIn(token, core)
        self.assertIn("min-height: 48px", css)
        self.assertIn("prefers-reduced-motion", css)

    def test_canonical_ui_fixes_and_slider_controls_are_present(self):
        core = (ROOT / "web/greedyq-core.js").read_text()
        css = (ROOT / "web/greedyq-runtime.css").read_text()
        preview = (ROOT / "templates/browser/preview.html").read_text()
        studio = (ROOT / "templates/browser/studio.html").read_text()
        for token in ("model.organization", 'type=\"range\"', "data-slider-kind", "mc_buttons", "mc_image", "daterange", "matrix_multiple", "data-range-index", "requestAnimationFrame", "scrollTo({", "!p.terminal"):
            self.assertIn(token, core)
        self.assertIn("color: #344054", css)
        self.assertIn("min-height: 0", css)
        self.assertIn("writing-mode:vertical-lr", "".join(css.split()))
        self.assertIn("<table><colgroup>", core)
        self.assertIn('scope="row"', core)
        self.assertIn('scope="col"', core)
        self.assertIn("position: sticky", css)
        for html in (preview, studio):
            compact = "".join(html.split())
            self.assertIn("width:min(390px,100%)", compact)
            self.assertNotIn(".mobile{max-width:none", compact)


if __name__ == "__main__":
    unittest.main()
