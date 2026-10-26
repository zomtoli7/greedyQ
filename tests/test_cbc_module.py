"""Module insertion, ordinary-question sequencing and safe saved-study handoff."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import zipfile
from greedyq import cbc_authoring as A
from greedyq.cbc import build_collection,collection_model,CBCError
from greedyq.cbc_flow import import_questions,normalize_flow
ROOT=Path(__file__).resolve().parents[1]
GOLD=ROOT/'drafts/v0.3/cbc/module-reference'

class CBCModuleTests(unittest.TestCase):
    def test_module_uses_ordinary_qmd_and_normalizes_python_browser_equally(self):
        flow=import_questions(GOLD/'survey.qmd');self.assertEqual(['background','preferences'],[p['id'] for p in flow['before']]);self.assertEqual(['impressions'],[p['id'] for p in flow['after']]);self.assertTrue(flow['before'][0]['questions'][0]['required'])
        s=json.loads((GOLD/'collection.json').read_text());s['flow']=flow;m=collection_model(GOLD,s)
        js="const fs=require('fs'),C=require('./web/greedyq-cbc.js');const x=JSON.parse(fs.readFileSync(0));C.collectionModel(x.cbc,x.settings,x.release).then(m=>process.stdout.write(JSON.stringify(m)))"
        r=subprocess.run(['node','-e',js],input=json.dumps({'cbc':m['cbc'],'settings':s,'release':m['greedyq_version']}),cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(0,r.returncode,r.stderr);self.assertEqual(m,json.loads(r.stdout));self.assertEqual('cbc-module-1',m['module_contract'])
        with self.assertRaises(CBCError):normalize_flow({'before':[{'id':'bad','title':'X','body':'','questions':[],'next':'skip'}],'after':[]})

    def test_add_module_keeps_original_questions_and_rejects_second_sequence(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'study';A.initialize(p,'authoring_test');original=(p/'survey.qmd').read_text();A.insert(p,'complete');result=(p/'survey.qmd').read_text();self.assertIn('--- welcome',result);self.assertIn('--- complete',result);self.assertIn('sd_cbc(',result);self.assertEqual('cbc_route',A.inspect(p)['phase'])
            with self.assertRaises(ValueError):A.insert(p,'complete','another')
            with self.assertRaises(FileExistsError):A.initialize(p,'other_study')
            self.assertEqual(original.split('--- complete')[0],result.split('--- choice_tasks')[0])

    def test_all_routes_and_blank_table_return_preserve_state(self):
        with tempfile.TemporaryDirectory() as d:
            for route in sorted(A.ROUTES):
                p=Path(d)/route;A.initialize(p,'route_'+route);A.set_route(p,route);self.assertEqual(route,A.inspect(p)['route'])
            p=Path(d)/'blank_table';A.blank_tables(p,['price','support']);self.assertEqual('awaiting_design_table',A.inspect(p)['phase']);self.assertIn('alternative_id,price,support',(p/'design/design.csv').read_text())
            z=A.pack(p,Path(d)/'handoff.zip');report=A.resume(z,Path(d)/'returned');self.assertEqual('awaiting_design_table',report['phase']);self.assertFalse(report['missing_files'])
            with self.assertRaises(FileExistsError):A.blank_tables(p,['new'])

    def test_source_handoff_omits_credentials_responses_and_generated_files(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'s';A.initialize(p,'handoff_study');(p/'.env').write_text('SECRET=private');(p/'responses').mkdir();(p/'responses/answers.csv').write_text('private');(p/'index.html').write_text('generated')
            z=A.pack(p,Path(d)/'s.zip')
            with zipfile.ZipFile(z) as f:self.assertEqual({'survey.qmd','authoring.json','authoring-package.json','.greedyq/guide-lock.json'},set(f.namelist()))
            bad=Path(d)/'bad.zip'
            with zipfile.ZipFile(bad,'w') as f:f.writestr('../outside.txt','bad');f.writestr('authoring.json','{}');f.writestr('authoring-package.json','{}')
            with self.assertRaises(ValueError):A.resume(bad,Path(d)/'bad')
            self.assertFalse((Path(d)/'outside.txt').exists())

    def test_fork_changes_identity_resets_approvals_and_does_not_touch_original(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'s';A.initialize(p,'original_study','ai');c=json.loads((GOLD/'study.design.json').read_text());c['study_id']='original_study';A.write(p/'study.design.json',c);A.write(p/'collection.json',json.loads((GOLD/'collection.json').read_text()));before=(p/'authoring.json').read_bytes()
            target=A.fork(p,Path(d)/'fork','new_study');self.assertEqual(before,(p/'authoring.json').read_bytes());self.assertEqual('new_study',json.loads((target/'study.design.json').read_text())['study_id']);self.assertEqual('test',json.loads((target/'collection.json').read_text())['mode']);self.assertFalse(any(json.loads((target/'collection.json').read_text())['approvals'].values()))
            state=json.loads((target/'authoring.json').read_text());state['greedyq_version']='old-release';A.write(target/'authoring.json',state)
            self.assertTrue(A.resume(target)['upgrade_available'])
            with self.assertRaises(ValueError):A.upgrade(target)
            upgraded=A.upgrade(target,True,Path(d)/'upgraded');self.assertTrue(A.resume(target)['upgrade_available']);self.assertFalse(upgraded['upgrade_available'])
            self.assertIn('version: "'+A.release()+'"',(Path(d)/'upgraded/survey.qmd').read_text())

    def test_complete_mixed_package_has_current_protocol_and_offline_dual_preview(self):
        with tempfile.TemporaryDirectory() as d:
            p,m=build_collection(GOLD,GOLD/'collection.json',Path(d)/'package');self.assertEqual('cbc-module-1',m['module_contract']);html=(p/'preview.html').read_text();self.assertIn('id="desktop"',html);self.assertIn('id="mobile"',html);self.assertIn('No responses are sent',html);self.assertNotIn('__MODEL__',html)
            self.assertEqual(10,len(json.loads((p/'supabase/migrations/manifest.json').read_text())['migrations']))

    def test_offline_dual_preview_keeps_computer_and_mobile_modules_independent(self):
        import os
        with tempfile.TemporaryDirectory() as d:
            package,m=build_collection(GOLD,GOLD/'collection.json',Path(d)/'package')
            node=Path('/Users/dongsookim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node');mods=node.parent.parent/'node_modules'
            r=subprocess.run([str(node),str(ROOT/'tests/cbc_module_preview.cjs'),str(package)],cwd=ROOT,env={**os.environ,'NODE_PATH':str(mods)},capture_output=True,text=True,timeout=120)
            self.assertEqual(0,r.returncode,r.stdout+'\n'+r.stderr)

    def test_human_pilot_preflight_does_not_invent_recruitment_approval(self):
        report=A.preflight(GOLD);self.assertEqual('passed',report['status']);self.assertFalse(report['fielding_ready']);self.assertIn('real_researcher_contact',report['blocking_approvals']);self.assertEqual('failed',A.preflight(GOLD,'fielding')['status'])

    def test_preflight_rejects_two_competing_question_sources(self):
        import shutil
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'study';shutil.copytree(GOLD,p)
            settings=json.loads((p/'collection.json').read_text());settings['flow']=import_questions(p/'survey.qmd');A.write(p/'collection.json',settings)
            with self.assertRaisesRegex(ValueError,'not both'):A.preflight(p)
