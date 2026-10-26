"""Independent regression cases from an external agent's first-study review."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from greedyq.build import build, load_study
from greedyq.compiler import condition
from greedyq.runtime import matches
from greedyq.scaffold import initialize
from greedyq.deployment import preflight
from greedyq.__main__ import show_report
from greedyq.exporter import _condition_r
ROOT=Path(__file__).resolve().parents[1]
NODE=Path('/Users/dongsookim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node')

class ClaudeReviewTests(unittest.TestCase):
    def test_fresh_draft_is_complete_local_package_but_not_approved_deployment(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=initialize(Path(tmp)/'study','review_study','simple',language='ko')
            self.assertEqual('passed',preflight(root)['status'],preflight(root))
            self.assertEqual('failed',preflight(root,stage='deployment')['status'])
            _,parsed,_=load_study(root)
            self.assertEqual(['welcome','complete'],[p['id'] for p in parsed['pages']])
            self.assertFalse(any(p['questions'] for p in parsed['pages']))
            self.assertEqual(8,len(list((root/'supabase/migrations').glob('*.sql'))))
            self.assertIn('local-preview-banner',(root/'index.html').read_text())
            self.assertEqual('in_progress',json.loads((root/'.greedyq/study-state.json').read_text())['status'])
            with self.assertRaises(FileExistsError):initialize(root,'review_study','simple')
    def test_deployment_stage_checks_prepared_candidate_and_researcher_approvals(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=initialize(Path(tmp)/'study','review_candidate','simple')
            state=root/'.greedyq/study-state.json';data=json.loads(state.read_text())
            for gate in ('instrument','deployment'):data['gates'][gate]['status']='approved'
            state.write_text(json.dumps(data))
            pending=root/'.greedyq/unresolved-decisions.json';data=json.loads(pending.read_text());data['items'][0]['status']='resolved';pending.write_text(json.dumps(data))
            html=(root/'index.html').read_text().replace('{ "mode": "mock", "supabase_url": null, "supabase_anon_key": null }','{ "mode": "supabase", "supabase_url": "https://synthetic.supabase.co", "supabase_anon_key": "sb_publishable_synthetic" }')
            candidate=Path(tmp)/'prepared.html';candidate.write_text(html)
            report=preflight(root,stage='deployment',deployment_index=candidate)
            self.assertEqual('passed',report['status'],report)
            candidate.write_text(html.replace('"study_id":"review_candidate"','"study_id":"other_study"'))
            self.assertEqual('failed',preflight(root,stage='deployment',deployment_index=candidate)['status'])

    def test_missing_study_metadata_and_declared_consent_block_handoff(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=initialize(Path(tmp)/'study','review_consent','simple',['consent'])
            self.assertEqual('passed',preflight(root)['status'],preflight(root))
            (root/'consent.md').unlink()
            self.assertEqual('failed',preflight(root)['status'])
            (root/'greedyq.study.json').unlink()
            self.assertEqual('failed',preflight(root)['status'])
    def test_source_change_invalidates_approval_and_updates_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=initialize(Path(tmp)/'study','review_change','simple')
            state=root/'.greedyq/study-state.json';data=json.loads(state.read_text());data['gates']['instrument']['status']='approved';state.write_text(json.dumps(data))
            qmd=root/'survey.qmd';qmd.write_text(qmd.read_text().replace('# Welcome','# Changed opening'))
            build(root)
            self.assertEqual('pending',json.loads(state.read_text())['gates']['instrument']['status'])
            self.assertEqual('passed',preflight(root)['status'],preflight(root))
    def test_manifest_cannot_read_outside_study(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=initialize(Path(tmp)/'study','review_path','simple')
            file=root/'.greedyq/generation-manifest.json';data=json.loads(file.read_text());data['artifacts'][0]['path']='../private.txt';(root.parent/'private.txt').write_text('synthetic');file.write_text(json.dumps(data))
            self.assertEqual('failed',preflight(root)['status'])
    def test_research_specific_randomization_is_documented_without_claiming_builtin_allocator(self):
        guide=(ROOT/'RANDOMIZATION.md').read_text()
        self.assertIn('four-group random assignment',guide)
        self.assertIn('not a newly verified built-in',guide)
        self.assertIn('simultaneous arrivals',guide)
        content=json.loads((ROOT/'website/content.json').read_text())
        for language in ('en','ko','zh'):
            topic=next(t for t in content[language]['guide'] if t['id']=='random')
            self.assertIn('4' if language=='ko' else ('四' if language=='zh' else 'four'),topic['prompt'])

    def test_cli_warning_is_visible_and_not_counted_as_error(self):
        output=io.StringIO()
        with contextlib.redirect_stdout(output):show_report({'status':'failed','issues':[{'message':'fix','code':'GQ001'},{'message':'notice','severity':'warning'}]},'deployment')
        self.assertIn('1 change(s)',output.getvalue());self.assertIn('Warnings (1',output.getvalue());self.assertIn('notice',output.getvalue())
    def test_core_bootstrap_does_not_require_premature_profile(self):
        result=subprocess.run(['python3','tools/resolve_guide.py','--core-only'],cwd=ROOT,capture_output=True,text=True,check=True)
        data=json.loads(result.stdout);self.assertIsNone(data['profile']);self.assertEqual('greedyQObject',data['object'])
    @unittest.skipUnless(NODE.is_file(),'Node unavailable')
    def test_expression_parser_and_evaluator_match_javascript(self):
        cases=[('contains(tools, "other")',{'tools':['other','gpt']},True),('contains(tools, "other")',{'tools':['gpt']},False),('length(tools) >= 2',{'tools':['a','b']},True),('length(name) == 2',{'name':'\U0001f600x'},True),('group in ["a", "b"]',{'group':'b'},True),('group not in ["a", "b"]',{'group':'c'},True),('not (age < 18 or not answered(name))',{'age':20,'name':'a'},True),('not answered(tools)',{'tools':[]},True),('age >= 18 and (group == "a" or group == "b")',{'age':17,'group':'a'},False),('age > 18',{},False),('group == null',{},True),('age == true',{'age':1},False)]
        script='const g=require("./web/greedyq-core.js"),xs=JSON.parse(require("fs").readFileSync(0,"utf8"));console.log(JSON.stringify(xs.map(([e,a])=>[g.condition(e),g.matchesCondition(g.condition(e),a,"default")])));'
        result=subprocess.run([str(NODE),'-e',script],input=json.dumps(cases),cwd=ROOT,capture_output=True,text=True,check=True)
        for (expression,answers,expected),(node,actual) in zip(cases,json.loads(result.stdout)):
            with self.subTest(expression=expression):self.assertEqual(condition(expression),node);self.assertEqual(expected,matches(node,answers,'default'));self.assertEqual(expected,actual)
    @unittest.skipUnless(NODE.is_file(),'Node unavailable')
    def test_invalid_condition_diagnostics_match_and_name_rule(self):
        from greedyq.validator import validate
        import copy
        _,parsed,config=load_study(ROOT/'examples/complete-study')
        for expression in ('contains(age, "other")','length(age) >= 2','contains(consent_choice, ["yes"])','tools[0] == "a"'):
            c=copy.deepcopy(config);c['logic']['show']=[{'id':'rule_review','question':'gender_self_description','if':expression}]
            expected=validate(parsed,c)
            result=subprocess.run([str(NODE),'-e','const g=require("./web/greedyq-core.js"),x=JSON.parse(require("fs").readFileSync(0,"utf8"));console.log(JSON.stringify(g.validateSurvey(x.p,x.c)))'],cwd=ROOT,input=json.dumps({'p':parsed,'c':c}),text=True,capture_output=True,check=True)
            actual=json.loads(result.stdout)
            self.assertEqual('failed',actual['status'])
            self.assertEqual([(i['code'],i['message']) for i in expected['issues']],[(i['code'],i['message']) for i in actual['issues']])
            self.assertTrue(any("Rule 'rule_review'" in i['message'] for i in actual['issues']))

    def test_native_export_uses_collection_values_and_no_arbitrary_execution(self):
        self.assertIn('assignment_condition ==',_condition_r('assignment_condition == "treatment"',{'assignment_condition'}))
        self.assertNotIn('sd_value("condition")',_condition_r('assignment_condition == "treatment"',{'assignment_condition'}))
        self.assertIn('gq_collection(sd_value("tools"))',_condition_r('contains(tools, "other")'))
        self.assertIn('length(gq_collection',_condition_r('length(tools) >= 2',question_types={'tools':'mc_multiple'}))
        self.assertIn('nchar',_condition_r('length(name) >= 2'))
        for expression in ('__import__("os")','tools[0] == "a"','sum(tools) > 0'):
            self.assertIn('unsupported',condition(expression))
            with self.assertRaises(ValueError):_condition_r(expression)
        if shutil.which('Rscript'):
            code='f <- function() '+_condition_r('contains(tools, "other") and not (length(name) < 2)')
            subprocess.run(['Rscript','-e','parse(text='+json.dumps(code)+')'],capture_output=True,check=True)
