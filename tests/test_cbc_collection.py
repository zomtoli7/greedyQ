"""CBC collection reference/model checks and real disposable PostgreSQL RPC tests."""
import concurrent.futures
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
import uuid
from greedyq.cbc import collection_model,build_collection,CBCError,stored_rows
ROOT=Path(__file__).resolve().parents[1]
GOLD=ROOT/'drafts/v0.3/cbc/golden-reference'
BIN=Path('/opt/homebrew/opt/postgresql@17/bin')
TOKEN='test-capability-only-000000000000000000000000'

def settings(mode='test',source='direct'):
    text='Synthetic software test. Participation is voluntary. You may decline or withdraw; withdrawal deletes choices and presentation records. No real recruitment is approved. Contact the fictional test team at researcher@example.invalid.'
    return {'schema_version':'0.3-collection.1','study_version':'synthetic-1','title':'Synthetic course choice study','organization':'Fictional test team','mode':mode,'source':source,'consent':{'id':'cbc_consent','version':'test-1','text':text,'document_sha256':hashlib.sha256(text.encode()).hexdigest(),'researcher_contact':'researcher@example.invalid'},'approvals':dict.fromkeys(['instrument','consent','data_plan','deployment','fielding'],False)}

def literal(value):return "'"+str(value).replace("'","''")+"'"

class CBCCollectionTests(unittest.TestCase):
    def test_collection_settings_do_not_turn_preview_into_unapproved_fielding(self):
        m=collection_model(GOLD,settings());self.assertFalse(m['fielding_approved']);self.assertEqual('cbc_study',m['kind'])
        for mutate in [lambda x:x.update(mode='production'),lambda x:x['consent'].update(document_sha256='0'*64),lambda x:x.pop('organization'),lambda x:x['approvals'].update(fielding='yes')]:
            s=settings();mutate(s)
            with self.assertRaises(CBCError):collection_model(GOLD,s)

    def test_collection_package_separates_private_plan_from_participant_html(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);f=p/'collection.json';f.write_text(json.dumps(settings()));dest,m=build_collection(GOLD,f,p/'package')
            html=(dest/'index.html').read_text();self.assertNotIn('block_a',html);self.assertNotIn('monthly_price',html);self.assertIn('"mode":"unconnected"',html)
            self.assertEqual(10,len(json.loads((dest/'supabase/migrations/manifest.json').read_text())['migrations']))
            self.assertEqual(m,json.loads((dest/'registered-model.json').read_text()))
            from test_cbc_import import workbook
            xlsx=p/'input.xlsx';xlsx.write_bytes(workbook((GOLD/'design/attributes.csv').read_text(),(GOLD/'design/design.csv').read_text()))
            _,from_workbook=build_collection(GOLD,f,p/'xlsx-package',xlsx)
            self.assertEqual(m,from_workbook)
            self.assertEqual('*', (dest/'.vercelignore').read_text().strip())
            manifest=json.loads((dest/'cbc-package.manifest.json').read_text());self.assertTrue(manifest['publish_only_separated_directories'])
            for name,digest in manifest['files'].items():self.assertEqual(digest,hashlib.sha256((dest/name).read_bytes()).hexdigest())
            with self.assertRaises(CBCError):build_collection(GOLD,f,dest)

@unittest.skipUnless((BIN/'initdb').is_file(),'Local PostgreSQL required')
class CBCPostgresTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory(prefix='greedyq-cbc-pg-');cls.root=Path(cls.tmp.name);data=cls.root/'data'
        subprocess.run([str(BIN/'initdb'),'-D',str(data),'-A','trust','--no-locale','-E','UTF8'],check=True,capture_output=True)
        subprocess.run([str(BIN/'pg_ctl'),'-D',str(data),'-l',str(cls.root/'server.log'),'-o',f"-h '' -k {cls.root} -p 55440",'-w','start'],check=True,capture_output=True)
        cls.addClassCleanup(cls.cleanup)
        cls.sql('create role anon;create role authenticated;create role service_role;create schema extensions;create extension pgcrypto with schema extensions;')
        for p in sorted((ROOT/'templates/supabase').glob('[0-9][0-9][0-9]_*.sql')):cls.sql(p.read_text())
        cls.sql('create table gq_migration_history(name text primary key,sha256 text not null)')
        for p in sorted((ROOT/'templates/supabase').glob('[0-9][0-9][0-9]_*.sql')):cls.sql("insert into gq_migration_history values ("+literal(p.name)+","+literal(hashlib.sha256(p.read_bytes()).hexdigest())+")")

    @classmethod
    def cleanup(cls):
        subprocess.run([str(BIN/'pg_ctl'),'-D',str(cls.root/'data'),'-m','immediate','stop'],capture_output=True);cls.tmp.cleanup()

    @classmethod
    def sql(cls,text):
        p=subprocess.run([str(BIN/'psql'),'-h',str(cls.root),'-p','55440','-d','postgres','-At','-v','ON_ERROR_STOP=1','-c',text],text=True,capture_output=True)
        if p.returncode:raise RuntimeError(p.stderr)
        return p.stdout.strip()

    def plan(self,mode='test',source='direct',flow=None):
        s=settings(mode,source)
        if flow is not None:s['flow']=flow
        if mode=='production':s['approvals']=dict.fromkeys(s['approvals'],True);s['consent']['researcher_contact']='synthetic-team@greedyq.org'
        if source=='prolific':s['prolific']={'study_id':'b'*24,'returns':{k:'https://app.prolific.com/submissions/complete?cc=SYNTHETIC' for k in ['completed','consent_refused','withdrawn']}}
        m=collection_model(GOLD,s);m['study_id']=m['cbc']['study_id']='cbc_'+uuid.uuid4().hex
        self.sql(f"insert into gq_study_plans values({literal(m['study_id'])},{literal(json.dumps(m))}::jsonb,now())")
        return m

    def rpc(self,name,*values):
        args=','.join('NULL' if x is None else literal(json.dumps(x) if isinstance(x,dict) else x) for x in values)
        text=self.sql(f'set role anon;select {name}({args})');value=text.splitlines()[-1]
        return json.loads(value) if value and value not in ['SET',''] else None

    def start(self,m,preview=None,external=None):
        sid=str(uuid.uuid4());r=self.rpc('greedyq_cbc_start',sid,TOKEN,m['study_id'],m['cbc']['design_sha256'],preview,external);return sid,r

    def consent(self,sid,decision='accepted'):return self.rpc('greedyq_cbc_consent',sid,TOKEN,decision)

    def step(self,sid,r,choice='none',direction='next',request=None):
        s=r['state'];return self.rpc('greedyq_cbc_step',sid,TOKEN,s['task_order'][s['index']],choice,direction,s['revision'],request or str(uuid.uuid4()))


    def test_module_ordinary_controls_and_visibility_reject_invalid_answers(self):
        gallery=json.loads((ROOT/'examples/control-gallery/preview-model.json').read_text());questions={q['type']:q for p in gallery['pages'] for q in p['questions']}
        cases=[('constant_sum',{'design':101},False),('rank_order',{'speed':1,'trust':1},False),('matrix',{'injected':1},False),('nps',11,False),('daterange',['2026-12-01','2026-01-01'],False),('drill_down',['Asia','Korea','Seoul'],True),('numeric',20,True)]
        # Use the actual declared option codes for allocation/rank checks.
        q=questions['constant_sum'];good={o['value']:0 for o in q['options']};good[q['options'][0]['value']]=q.get('total',100)
        cases.append(('constant_sum',good,True))
        for kind,value,ok in cases:
            q=questions[kind]
            call='select gq_cbc_check_answer('+literal(json.dumps(q))+'::jsonb,'+literal(json.dumps(value))+'::jsonb,true)'
            if ok:self.sql(call)
            else:
                with self.assertRaises(RuntimeError,msg=kind):self.sql(call)
        for rule,answers,expected in [({'field':'a','not_equals':'x'},{},False),({'field':'a','answered':False},{},True),({'field':'a','length':{'gte':2}},{'a':'中文'},True)]:
            result=self.sql('select gq_cbc_question_visible('+literal(json.dumps(rule))+'::jsonb,'+literal(json.dumps(answers))+'::jsonb)')
            self.assertEqual('t' if expected else 'f',result)

    def test_module_pages_gate_exposure_completion_and_erase_withdrawal(self):
        s=settings();s['flow']={'before':[{'id':'background','title':'Background','body':'','questions':[{'id':'experience','type':'numeric','label':'Experience','min':0,'max':10,'required':True}]}],'after':[{'id':'feedback','title':'Feedback','body':'','questions':[{'id':'rating','type':'nps','label':'Rating','required':True}]}]}
        m=collection_model(GOLD,s);m['study_id']=m['cbc']['study_id']='module_'+uuid.uuid4().hex
        self.sql(f"insert into gq_study_plans values({literal(m['study_id'])},{literal(json.dumps(m))}::jsonb,now())")
        sid,_=self.start(m);r=self.consent(sid);self.assertEqual('before',r['state']['phase']);self.assertIsNone(r['model']);self.assertEqual('0',self.sql(f"select count(*) from gq_answers where session_id='{sid}'"))
        def form(r,page,answers,direction='next',request=None):return self.rpc('greedyq_cbc_form_step',sid,TOKEN,page,answers,direction,r['state']['revision'],request or str(uuid.uuid4()))
        with self.assertRaisesRegex(RuntimeError,'required question'):form(r,'background',{})
        with self.assertRaisesRegex(RuntimeError,'numeric bound'):form(r,'background',{'experience':11})
        with self.assertRaisesRegex(RuntimeError,'unknown question'):form(r,'background',{'experience':2,'injected':'bad'})
        rid=str(uuid.uuid4());r=form(r,'background',{'experience':2},request=rid);self.assertEqual('tasks',r['state']['phase']);self.assertEqual(r,self.rpc('greedyq_cbc_form_step',sid,TOKEN,'background',{'experience':2},'next',1,rid))
        r=self.step(sid,r,None,'previous');self.assertEqual('before',r['state']['phase']);r=form(r,'background',{'experience':3})
        while r['state']['phase']=='tasks':r=self.step(sid,r)
        self.assertEqual('after',r['state']['phase']);self.assertIsNone(r['terminal_at']);self.assertEqual('in_progress',self.sql(f"select lifecycle_state from gq_sessions where id='{sid}'"))
        with self.assertRaisesRegex(RuntimeError,'required question'):form(r,'feedback',{})
        r=form(r,'feedback',{'rating':8});self.assertEqual('completed',r['state']['phase']);self.assertTrue(r['terminal_at'])
        self.assertEqual('3',self.sql(f"select value from gq_answers where session_id='{sid}' and question_id='experience'"))
        self.rpc('greedyq_cbc_withdraw',sid,TOKEN);self.assertEqual('0',self.sql(f"select count(*) from gq_answers where session_id='{sid}'"))

    def test_consent_gates_assignment_and_exposure_and_refusal_is_terminal(self):
        m=self.plan();sid,r=self.start(m);self.assertIsNone(r['model']);self.assertEqual('consent',r['state']['phase'])
        self.assertEqual('0',self.sql(f"select count(*) from gq_answers where session_id='{sid}'"))
        self.assertEqual('0',self.sql(f"select count(*) from gq_assignments where session_id='{sid}'"))
        with self.assertRaisesRegex(RuntimeError,'session ended'):self.rpc('greedyq_cbc_step',sid,TOKEN,'task_1','none','next',0,str(uuid.uuid4()))
        r=self.consent(sid,'refused');self.assertIsNone(r['model']);self.assertEqual('consent_refused',r['state']['phase']);self.assertTrue(r['terminal_at'])
        self.assertEqual(r,self.consent(sid,'refused'))
        with self.assertRaisesRegex(RuntimeError,'session ended'):self.consent(sid)

    def test_server_presentation_and_orders_are_stable_only_assigned_block_is_returned(self):
        m=self.plan();sid,_=self.start(m);r=self.consent(sid);self.assertEqual(1,len(r['model']['blocks']));self.assertEqual(r['state']['block_id'],r['model']['blocks'][0]['id'])
        self.assertEqual(r,self.consent(sid));self.assertEqual(r,self.rpc('greedyq_cbc_resume',sid,TOKEN))
        self.assertEqual('1',self.sql(f"select count(*) from gq_consent_events where session_id='{sid}'"))
        self.assertEqual('1',self.sql(f"select count(*) from gq_answers where session_id='{sid}'"))
        generic=self.rpc('greedyq_resume_session',sid,TOKEN);self.assertNotIn('registered_model',generic)

    def test_server_availability_is_not_fabricated_display_and_acknowledgement_is_idempotent(self):
        m=self.plan();sid,_=self.start(m);r=self.consent(sid);tid=r['state']['task_order'][0]
        value=json.loads(self.sql(f"select value from gq_answers where session_id='{sid}'"));self.assertIsNone(value['presented_at']);self.assertTrue(value['served_at'])
        self.rpc('greedyq_cbc_ack',sid,TOKEN,tid)
        first=json.loads(self.sql(f"select value from gq_answers where session_id='{sid}'"));self.assertTrue(first['presented_at']);self.assertIsNone(first['answered_at'])
        self.rpc('greedyq_cbc_ack',sid,TOKEN,tid);self.assertEqual(first,json.loads(self.sql(f"select value from gq_answers where session_id='{sid}'")))
        with self.assertRaisesRegex(RuntimeError,'not served'):self.rpc('greedyq_cbc_ack',sid,TOKEN,'unknown')

    def test_invalid_choice_missing_choice_capability_and_stale_revision_fail_closed(self):
        m=self.plan();sid,_=self.start(m);r=self.consent(sid)
        with self.assertRaisesRegex(RuntimeError,'choice required'):self.step(sid,r,None)
        with self.assertRaisesRegex(RuntimeError,'unknown alternative'):self.step(sid,r,'invented')
        with self.assertRaisesRegex(RuntimeError,'invalid session capability'):self.rpc('greedyq_cbc_resume',sid,'wrong')
        r2=self.step(sid,r)
        with self.assertRaisesRegex(RuntimeError,'revision conflict'):self.step(sid,r,'a')
        self.assertEqual(r2,self.rpc('greedyq_cbc_resume',sid,TOKEN))

    def test_completion_retry_and_previous_preserve_exposures_and_server_end_time(self):
        m=self.plan();sid,_=self.start(m);r=self.consent(sid);first=r['state']['task_order'][0]
        r=self.step(sid,r,'a');r=self.step(sid,r,None,'previous');self.assertEqual('a',r['state']['answers'][first])
        r=self.step(sid,r,'none')
        while r['state']['phase']=='tasks':
            before=r;request=str(uuid.uuid4());r=self.step(sid,r,'none',request=request)
        self.assertEqual('completed',r['state']['phase']);self.assertTrue(r['terminal_at']);self.assertEqual(r,self.step(sid,before,'none',request=request))
        vals=json.loads(self.sql(f"select json_agg(value) from gq_answers where session_id='{sid}'"));self.assertEqual(4,len(vals));self.assertTrue(all(v['presented_at'] and v['answered_at'] for v in vals))
        self.assertTrue(all(v['choice']=='none' for v in vals));self.assertEqual(4,sum(1 for v in vals if len(v['alternatives'])==3))

    def test_withdrawal_erases_choices_orders_consent_but_retains_minimal_receipt(self):
        m=self.plan();sid,_=self.start(m);r=self.step(sid,self.consent(sid));r=self.rpc('greedyq_cbc_withdraw',sid,TOKEN)
        self.assertIsNone(r['model']);self.assertEqual('withdrawn',r['state']['lifecycle'])
        for table in ['answers','assignments','consent_events']:
            self.assertEqual('0',self.sql(f"select count(*) from gq_{table} where session_id='{sid}'"))
        self.assertNotIn('alternative_orders',r['state']);self.assertEqual(r,self.rpc('greedyq_cbc_withdraw',sid,TOKEN))
        with self.assertRaisesRegex(RuntimeError,'session ended'):self.consent(sid)

    def test_mixed_prolific_real_and_preview_keep_identity_and_scope(self):
        flow={'before':[{'id':'intro_question','title':'Intro','body':'','questions':[{'id':'ready','type':'mc','label':'Ready?','options':[{'label':'Yes','value':'yes'}],'required':True}]}],'after':[]}
        m=self.plan('production','prolific',flow);ids={'PROLIFIC_PID':'d'*24,'STUDY_ID':'b'*24,'SESSION_ID':'e'*24}
        sid,r=self.start(m,external=ids);self.assertFalse(r['is_test']);r=self.consent(sid);self.assertEqual('before',r['state']['phase'])
        r=self.rpc('greedyq_cbc_form_step',sid,TOKEN,'intro_question',{'ready':'yes'},'next',r['state']['revision'],str(uuid.uuid4()));self.assertEqual('tasks',r['state']['phase'])
        grant=self.sql(f"set role service_role;select greedyq_issue_cbc_preview({literal(m['study_id'])})").splitlines()[-1]
        sid2,r2=self.start(m,grant,ids);self.assertTrue(r2['is_test']);self.assertEqual('before',self.consent(sid2)['state']['phase']);self.assertNotEqual(sid,sid2)

    def test_real_and_authorized_test_share_study_but_cannot_spoof_scope(self):
        m=self.plan('production');sid,real=self.start(m);self.assertFalse(real['is_test']);self.assertEqual('direct',real['source'])
        grant=self.sql(f"set role service_role;select greedyq_issue_cbc_preview({literal(m['study_id'])})").splitlines()[-1]
        _,trial=self.start(m,grant);self.assertTrue(trial['is_test'])
        with self.assertRaisesRegex(RuntimeError,'invalid or expired'):self.start(m,'0'*64)
        with self.assertRaisesRegex(RuntimeError,'permission denied'):self.rpc('greedyq_issue_cbc_preview',m['study_id'])
        with self.assertRaisesRegex(RuntimeError,'use CBC protocol'):self.rpc('greedyq_create_session',str(uuid.uuid4()),TOKEN,m['study_id'],'v','0.2','v',True)
        with self.assertRaisesRegex(RuntimeError,'use CBC protocol'):self.rpc('greedyq_save_session',sid,TOKEN,{'answers':{'bypass':'bad'}},None)

    def test_prolific_identity_and_repeat_test_namespace(self):
        m=self.plan('production','prolific');ids={'PROLIFIC_PID':'a'*24,'STUDY_ID':'b'*24,'SESSION_ID':'c'*24}
        sid,r=self.start(m,external=ids);self.assertEqual('prolific',r['source']);self.assertFalse(r['is_test']);self.consent(sid)
        grant=self.sql(f"set role service_role;select greedyq_issue_cbc_preview({literal(m['study_id'])})").splitlines()[-1]
        sid2,r2=self.start(m,grant,ids);sid3,r3=self.start(m,grant,ids);self.assertNotEqual(sid2,sid3);self.assertTrue(r2['is_test'] and r3['is_test'])
        self.rpc('greedyq_cbc_withdraw',sid,TOKEN);self.assertEqual('1',self.sql(f"select count(*) from gq_external_identifiers where session_id='{sid}'"))

    def test_concurrent_duplicate_is_idempotent_and_different_command_conflicts(self):
        m=self.plan();sid,_=self.start(m);r=self.consent(sid);request=str(uuid.uuid4())
        with concurrent.futures.ThreadPoolExecutor(2) as pool:results=list(pool.map(lambda _:self.step(sid,r,request=request),range(2)))
        self.assertEqual(results[0],results[1]);self.assertEqual(2,results[0]['state']['revision'])
        with self.assertRaisesRegex(RuntimeError,'revision conflict'):self.step(sid,r,request=str(uuid.uuid4()))

    def test_browser_results_and_archive_journey(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);f=root/'collection.json';cfg=settings('production');cfg['approvals']=dict.fromkeys(cfg['approvals'],True);cfg['consent']['researcher_contact']='software-fixture@greedyq.org';f.write_text(json.dumps(cfg));package,m=build_collection(GOLD,f,root/'package')
            node=Path('/Users/dongsookim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node');mods=node.parent.parent/'node_modules'
            result=subprocess.run([str(node),str(ROOT/'tests/cbc_collection_journey.cjs'),str(package)],cwd=ROOT,env={**os.environ,'NODE_PATH':str(mods),'GREEDYQ_PG_MODULE':'/Users/dongsookim/.npm/_npx/ff3a78d6668cab0a/node_modules/pg','PGHOST':str(self.root),'PGPORT':'55440'},capture_output=True,text=True,timeout=180)
            self.assertEqual(0,result.returncode,result.stderr);e=json.loads(result.stdout.strip().splitlines()[-1]);self.assertEqual(0,e['external_cloud_calls']);self.assertGreaterEqual(e['completed'],2)

    def test_mixed_module_browser_saves_every_stage_and_withdraws_together(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=ROOT/'drafts/v0.3/cbc/module-reference';package,m=build_collection(source,source/'collection.json',Path(tmp)/'package')
            node=Path('/Users/dongsookim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node');mods=node.parent.parent/'node_modules'
            result=subprocess.run([str(node),str(ROOT/'tests/cbc_module_journey.cjs'),str(package)],cwd=ROOT,env={**os.environ,'NODE_PATH':str(mods),'GREEDYQ_PG_MODULE':'/Users/dongsookim/.npm/_npx/ff3a78d6668cab0a/node_modules/pg','PGHOST':str(self.root),'PGPORT':'55440'},capture_output=True,text=True,timeout=180)
            self.assertEqual(0,result.returncode,result.stdout+'\n'+result.stderr)
