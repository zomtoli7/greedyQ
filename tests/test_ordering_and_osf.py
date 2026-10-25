import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import shutil

from greedyq.build import load_study
from greedyq.compiler import compile_preview, condition
from greedyq.randomization import option_plan, option_order, page_plan, page_order
from greedyq.preregistration import generate
from greedyq.osf_fields import FIELDS
from greedyq.redirects import redirect_plan, redirect_url
from tools.upgrade_study import upgrade
from greedyq.formatting import inline

ROOT = Path(__file__).resolve().parents[1]
NODE = '/Users/dongsookim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'


class OrderingTests(unittest.TestCase):
    def test_formatting_is_escaped_and_matches_browser(self):
        for text in ('**Bold** and *italic* and ***both***','`**literal**`','<img src=x onerror=alert(1)>','\x000\x00',"apostrophe's & quote\"",0):
            self.assertEqual(inline(text),self.js('inlineMarkdown',[text])['value'])
        self.assertNotIn('<img',inline('<img src=x>'))
    def test_condition_literals_and_boolean_precedence(self):
        for expr in ('choice == "rock and roll"','age > 20 or age < 5 and choice == "no"','not answered(choice)'):
            self.assertEqual(condition(expr),self.js('condition',[expr])['value'])
        self.assertEqual({'field':'choice','equals':'rock and roll'},condition('choice == "rock and roll"'))
        self.assertIn('any',condition('age > 20 or age < 5 and choice == "no"'))
    def fixture(self):
        _, parsed, config = load_study(ROOT / 'examples/control-gallery')
        return parsed, config

    def js(self, function, value):
        proc = subprocess.run([NODE, '-e', 'const g=require("./web/greedyq-core.js"); const x=JSON.parse(require("fs").readFileSync(0,"utf8")); try {console.log(JSON.stringify({value:g[process.argv[1]](...x)}))} catch(e) {console.log(JSON.stringify({error:e.message}))}', function], cwd=ROOT, input=json.dumps(value), capture_output=True, text=True, check=True)
        return json.loads(proc.stdout)

    def test_indexed_options_rows_and_anchors(self):
        p,c = self.fixture()
        p['front_matter']['survey-settings']['all-shuffled'] = True
        plans = option_plan(p)
        self.assertEqual(plans, self.js('optionPlan',[p])['value'])
        q = next(q for page in p['pages'] for q in page['questions'] if q['type']=='mc')
        q['options'].append({'label':'Fixed other','value':'fixed_other'})
        p['front_matter']['survey-settings']['shuffled'] = [{q['id']: '1-2'}]
        plans = option_plan(p)
        compiled = compile_preview(p,c)
        self.assertEqual(compiled, self.js('compileSurvey',[p,c])['value'])
        q = next(x for page in compiled['pages'] for x in page['questions'] if x['id']==q['id'])
        order = option_order(q, lambda n: 0)
        self.assertEqual(order[:2], [q['options'][1]['value'],q['options'][0]['value']])
        self.assertEqual(order[2:], [o['value'] for o in q['options'][2:]])

    def test_invalid_ranges_fail_equally(self):
        p,_ = self.fixture()
        q = next(q for page in p['pages'] for q in page['questions'] if q['type']=='mc')
        for value in ('0-2','2-1',[1,1],[],True,'1-999999999',[-1],['1-2',2]):
            p['front_matter']['survey-settings']['shuffled']=[{q['id']:value}]
            with self.assertRaises(ValueError) as e: option_plan(p)
            self.assertEqual(str(e.exception),self.js('optionPlan',[p])['error'])

    def test_linear_page_order_and_rejections(self):
        p={'front_matter':{},'pages':[{'id':s,'questions':[]} for s in ['open','aa','bb','cc','end']]}
        c={'page_order':['aa','bb','cc']}
        self.assertEqual(page_plan(p,c),self.js('pagePlan',[p,c])['value'])
        m={'pages':p['pages'],'shuffle_pages':page_plan(p,c)}
        for _ in range(100):
            order=page_order(m)
            self.assertEqual(order[0],'open');self.assertEqual(order[-1],'end')
            self.assertEqual(set(order),set(x['id'] for x in p['pages']))
        for selected in (['open','aa'],['aa','cc'],['aa','aa'],['unknown','bb']):
            c['page_order']=selected
            with self.assertRaises(ValueError) as e:page_plan(p,c)
            self.assertEqual(str(e.exception),self.js('pagePlan',[p,c])['error'])

    def test_osf_all_fields_draft_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            result=generate(tmp,{'study':{'id':'draft','title':'A test'},'preregistration':{'adapter':'osf_preregistration','fields':{'research_questions':'Confirmed question'}}})
            data=json.loads(result['json'].read_text())
            self.assertEqual(29,len(FIELDS))
            self.assertFalse(result['ready_for_submission'])
            self.assertEqual(27,len(data['incomplete_fields']))
            for key,_,_ in FIELDS:
                self.assertIn('('+key+')',result['markdown'].read_text())
                self.assertIn('('+key+')',result['korean'].read_text())
            self.assertNotIn('```json',result['markdown'].read_text())
            self.assertFalse(data['registry']['submitted'])

    def test_osf_rejects_unknown_or_nontext(self):
        for fields in ({'invented':'answer'},{'sample_size':50}):
            with tempfile.TemporaryDirectory() as tmp, self.assertRaises(ValueError):
                generate(tmp,{'preregistration':{'fields':fields}})

    def test_redirects_encode_and_reject_missing_unsafe_values(self):
        outcome={'redirect':'https://example.test/return','redirect_params':{'pid':'PID'}}
        plan=redirect_plan(outcome)
        self.assertEqual(plan,self.js('redirectPlan',[outcome])['value'])
        query='?PID=a%26b%3Dc&ignored=secret'
        self.assertEqual(redirect_url(plan,query),self.js('redirectUrl',[plan,query])['value'])
        for query in ('','?PID=','?PID=one&PID=two'):
            with self.assertRaises(ValueError):redirect_url(plan,query)
            self.assertIn('error',self.js('redirectUrl',[plan,query]))
        for outcome in ({'redirect':'javascript:alert(1)'},{'redirect':'https://u:p@example.test/'},{'redirect':'https://example.test/','redirect_params':{'access_token':'token'}},{'redirect':'https://example.test/','redirect_delay':0,'redirect_newtab':True}):
            with self.assertRaises(ValueError) as e:redirect_plan(outcome)
            self.assertEqual(str(e.exception),self.js('redirectPlan',[outcome])['error'])

    def test_upgrade_preserves_original_and_rebuilds_only_new_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)/'original';shutil.copytree(ROOT/'examples/simple-satisfaction-study',source)
            (source/'.env.local').write_text('TEST_SECRET=not-for-copy')
            before=(source/'survey.qmd').read_bytes()
            destination=Path(tmp)/'upgraded'
            result=upgrade(source,destination)
            self.assertEqual('preview_ready_review_required',result['status'])
            self.assertEqual(before,(source/'survey.qmd').read_bytes())
            self.assertFalse((destination/'.env.local').exists())
            self.assertEqual((ROOT/'web/greedyq-core.js').read_bytes(),(destination/'greedyq-core.js').read_bytes())
            self.assertTrue(list((destination/'.greedyq').glob('before-upgrade-*')))
            again=Path(tmp)/'again';upgrade(destination,again)
            self.assertEqual(2,len(list((again/'.greedyq').glob('before-upgrade-*'))))
            with self.assertRaises(ValueError):upgrade(source,destination)
            with self.assertRaises(ValueError):upgrade(source,source/'nested')


if __name__=='__main__':unittest.main()
