"""Real local PostgreSQL integration; no Supabase credentials or cloud writes."""
import concurrent.futures
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import uuid

ROOT=Path(__file__).resolve().parents[1]
BIN=Path(os.environ.get("GREEDYQ_PG_BIN", "/opt/homebrew/opt/postgresql@17/bin"))


@unittest.skipUnless((BIN/"initdb").is_file(), "Set GREEDYQ_PG_BIN to local PostgreSQL tools")
class PostgresRandomizationTests(unittest.TestCase):
    def test_first_researcher_browser_results_and_archive_journey(self):
        """Synthetic local study only; never contact Vercel, Supabase or Prolific."""
        from greedyq.build import build
        node = Path('/Users/dongsookim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node')
        modules = node.parent.parent / 'node_modules'
        pg = Path(os.environ.get('GREEDYQ_PG_MODULE', '/Users/dongsookim/.npm/_npx/ff3a78d6668cab0a/node_modules/pg'))
        if not node.is_file() or not pg.is_dir() or not (modules/'playwright').is_dir():
            self.skipTest('Local Node, Playwright and pg are required for this browser journey')
        with tempfile.TemporaryDirectory(prefix='greedyq-first-user-') as tmp:
            study=Path(tmp)/'study'
            shutil.copytree(ROOT/'tests/fixtures/first-user-study', study)
            report,_=build(study)
            self.assertEqual('passed',report['status'],report)
            result=subprocess.run([str(node),str(ROOT/'tests/first_user_journey.cjs'),str(study)],cwd=ROOT,
                env={**os.environ,'NODE_PATH':str(modules),'GREEDYQ_PG_MODULE':str(pg),
                     'PGHOST':str(self.root),'PGPORT':'55439'},text=True,capture_output=True,timeout=180)
            self.assertEqual(0,result.returncode,result.stderr)
            evidence=json.loads(result.stdout.strip().splitlines()[-1])
            self.assertEqual(6,evidence['archive_sessions'])
            self.assertEqual(0,evidence['cloud_calls'])

    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory(prefix="greedyq-random-pg-")
        cls.root=Path(cls.tmp.name); cls.data=cls.root/"data"
        subprocess.run([str(BIN/"initdb"),"-D",str(cls.data),"-A","trust","--no-locale","-E","UTF8"],check=True,capture_output=True)
        subprocess.run([str(BIN/"pg_ctl"),"-D",str(cls.data),"-l",str(cls.root/"server.log"),"-o",f"-h '' -k {cls.root} -p 55439","-w","start"],check=True,capture_output=True)
        cls.addClassCleanup(cls.cleanup_server)
        cls.sql("create role anon; create role authenticated; create role service_role; create schema extensions; create extension pgcrypto with schema extensions;")
        for source in [ROOT/"examples/complete-study/supabase/migrations/001_initial.sql",*[ROOT/"templates/supabase"/name for name in ("002_browser_rpc.sql","003_results_dashboard.sql","004_randomization.sql","005_prolific.sql","006_withdrawal_preview.sql","007_answer_snapshot.sql")]]:
            cls.sql(source.read_text())

    def test_accepted_answer_snapshot_prunes_only_removed_session_answers(self):
        sid=self.participant(); other=self.participant()
        def save(state,token='abcdefghijklmnopqrstuvwx'):
            self.sql(f"set role anon; select greedyq_save_session('{sid}','{token}','{json.dumps(state)}','consent');")
        original={'page':'baseline','answers':{'consent':'yes','q1':'keep','q2':'hidden later'}}
        save(original)
        reduced={'page':'baseline','answers':{'consent':'yes','q1':'keep'}}
        with self.assertRaisesRegex(RuntimeError,'invalid session capability'):save(reduced,'wrong')
        self.assertEqual('3',self.sql(f"select count(*) from gq_answers where session_id='{sid}'"))
        save(reduced)
        self.assertEqual('2',self.sql(f"select count(*) from gq_answers where session_id='{sid}'"))
        self.assertEqual('0',self.sql(f"select count(*) from gq_answers where session_id='{sid}' and question_id='q2'"))
        self.assertEqual('1',self.sql(f"select count(*) from gq_answers where session_id='{other}'"))

    @classmethod
    def cleanup_server(cls):
        subprocess.run([str(BIN/"pg_ctl"),"-D",str(cls.data),"-m","fast","-w","stop"],check=True,capture_output=True)
        cls.tmp.cleanup()

    @classmethod
    def sql(cls, text):
        proc=subprocess.run([str(BIN/"psql"),"-h",str(cls.root),"-p","55439","-d","postgres","-XqAt","-v","ON_ERROR_STOP=1"],input=text,text=True,capture_output=True)
        if proc.returncode: raise RuntimeError(proc.stderr)
        return proc.stdout.strip()

    def setUp(self):
        self.sql("truncate public.gq_sessions,public.gq_study_plans cascade;")
        self.model={"study_id":"trial","study_version":"1","assignment_page":"baseline","randomization":{"id":"frame","method":"fixed_block","unit":"respondent","persistence_key":"session_id","conditions":{"a":1,"b":1},"block_size":4},"pages":[{"id":"baseline","questions":[{"id":"q1"},{"id":"q2"},{"id":"q3"}],"shuffle_questions":["q1","q2"]}],"runtime_policy":{"consent":{"question":"consent","accept_value":"yes"}}}
        self.register()

    def register(self):
        model=json.dumps(self.model).replace("'","''")
        self.sql(f"insert into public.gq_study_plans values('trial','{model}',now()) on conflict(study_id) do update set model=excluded.model;")

    def participant(self, test=True, page="baseline", consent="yes"):
        sid=str(uuid.uuid4()); state=json.dumps({"page":page,"answers":{"consent":consent},"consent_accepted":consent=="yes"})
        self.sql(f"set role anon; select public.greedyq_create_session('{sid}','abcdefghijklmnopqrstuvwx','trial','1','0.2','release',{str(test).lower()}); select public.greedyq_save_session('{sid}','abcdefghijklmnopqrstuvwx','{state}','forged_consent_field');")
        return sid

    def assign(self,sid,test=True):
        return self.sql(f"set role anon; select public.greedyq_assign_condition('{sid}','abcdefghijklmnopqrstuvwx','trial','1','0.2','release',array['forged'],{str(test).lower()});")

    def test_saved_option_and_page_orders_cannot_change(self):
        self.model['pages'][0]['questions'][0].update(type='mc',options=[{'value':'a'},{'value':'b'},{'value':'other'}],shuffle_items=['a','b'])
        self.model['pages'] += [{'id':p,'questions':[]} for p in ('first','second','ending')]
        self.model['shuffle_pages']=['first','second'];self.register()
        sid=self.participant()
        state={'page':'baseline','answers':{'consent':'yes'},'option_orders':{'q1':['b','a','other']},'page_order':['baseline','second','first','ending']}
        def save(value):self.sql(f"set role anon; select greedyq_save_session('{sid}','abcdefghijklmnopqrstuvwx','{json.dumps(value)}','consent');")
        save(state);save(state)
        self.assertEqual('["b", "a", "other"]',self.sql(f"select option_orders->'q1' from gq_sessions where id='{sid}';"))
        state['option_orders']['q1']=['a','b','other']
        with self.assertRaisesRegex(RuntimeError,'option order changed'):save(state)
        state['option_orders']['q1']=['b','a','other'];state['page_order']=['baseline','first','second','ending']
        with self.assertRaisesRegex(RuntimeError,'page order changed'):save(state)

    def prolific_start(self,sid,pid='a'*24,external_session='c'*24,test=True,token='abcdefghijklmnopqrstuvwx'):
        return self.sql(f"set role anon; select greedyq_start_prolific('{sid}','{token}','trial','1','0.2','release',{str(test).lower()},'{pid}','{'b'*24}','{external_session}');")

    def prolific_plan(self,test=True):
        self.model['runtime_policy'].update(mode='test' if test else 'production',respondent_source='prolific',prolific={'study_id':'b'*24})
        self.register()

    def test_prolific_atomic_start_resume_and_immutable_identity(self):
        self.prolific_plan();sid=str(uuid.uuid4());self.prolific_start(sid);self.prolific_start(sid)
        self.assertEqual('1',self.sql("select count(*) from gq_external_identifiers"))
        self.assertEqual('prolific',self.sql(f"select respondent_source from gq_sessions where id='{sid}'"))
        with self.assertRaisesRegex(RuntimeError,'immutable'):self.prolific_start(sid,pid='d'*24)
        with self.assertRaisesRegex(RuntimeError,'capability'):self.prolific_start(sid,token='another-strong-token-xxxxxxxx')
        fresh=str(uuid.uuid4())
        with self.assertRaisesRegex(RuntimeError,'duplicate'):self.prolific_start(fresh)
        self.assertEqual('0',self.sql(f"select count(*) from gq_sessions where id='{fresh}'"))
        with self.assertRaisesRegex(RuntimeError,'duplicate'):self.prolific_start(str(uuid.uuid4()),pid='d'*24)

    def test_withdrawal_erases_answers_state_and_preserves_duplicate_guard(self):
        self.prolific_plan();sid=str(uuid.uuid4());self.prolific_start(sid)
        state=json.dumps({'page':'baseline','lifecycle':'in_progress','answers':{'consent':'yes','q1':'private answer'}})
        self.sql(f"select greedyq_save_session('{sid}','abcdefghijklmnopqrstuvwx','{state}','consent');")
        self.assertEqual('2',self.sql(f"select count(*) from gq_answers where session_id='{sid}'"))
        with self.assertRaisesRegex(RuntimeError,'invalid session capability'):
            self.sql(f"select greedyq_withdraw_session('{sid}','wrong-token');")
        self.assertEqual('2',self.sql(f"select count(*) from gq_answers where session_id='{sid}'"))
        state=json.dumps({'page':'anything','lifecycle':'withdrawn','answers':{'q1':'private answer'}})
        self.sql(f"select greedyq_save_session('{sid}','abcdefghijklmnopqrstuvwx','{state}','consent');")
        self.assertEqual('0',self.sql(f"select count(*) from gq_answers where session_id='{sid}'"))
        self.assertEqual('{}',self.sql(f"select browser_state->'answers' from gq_sessions where id='{sid}'"))
        self.assertEqual('1',self.sql(f"select count(*) from gq_external_identifiers where session_id='{sid}'"))
        self.sql(f"select greedyq_withdraw_session('{sid}','abcdefghijklmnopqrstuvwx');")
        self.assertEqual('1',self.sql(f"select count(*) from gq_lifecycle_events where session_id='{sid}'"))
        with self.assertRaisesRegex(RuntimeError,'session ended'):
            self.sql(f"select greedyq_save_session('{sid}','abcdefghijklmnopqrstuvwx','{{\"answers\":{{\"q1\":\"resurrect\"}}}}','consent');")
        with self.assertRaisesRegex(RuntimeError,'duplicate'):self.prolific_start(str(uuid.uuid4()))

    def test_concurrent_save_and_withdrawal_cannot_resurrect_answers(self):
        sid=self.participant();state=json.dumps({'page':'baseline','answers':{'consent':'yes','q1':'secret'}})
        def operation(i):
            try:
                if i%2:self.sql(f"select greedyq_withdraw_session('{sid}','abcdefghijklmnopqrstuvwx');")
                else:self.sql(f"select greedyq_save_session('{sid}','abcdefghijklmnopqrstuvwx','{state}','consent');")
            except RuntimeError as error:self.assertIn('session ended',str(error))
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:list(pool.map(operation,range(8)))
        self.assertEqual('0',self.sql(f"select count(*) from gq_answers where session_id='{sid}'"))
        self.assertEqual('withdrawn',self.sql(f"select lifecycle_state from gq_sessions where id='{sid}'"))

    def test_preview_grants_repeat_same_identifiers_without_weakening_production(self):
        self.prolific_plan();grant=self.sql("select greedyq_issue_preview('trial')")
        def start(sid,token=grant,test=True):
            return self.sql(f"set role anon; select greedyq_start_prolific_preview('{sid}','abcdefghijklmnopqrstuvwx','trial','1','0.2','release',{str(test).lower()},'{'a'*24}','{'b'*24}','{'c'*24}','{token}');")
        ids=[str(uuid.uuid4()) for _ in range(3)]
        for sid in ids:start(sid);start(sid)
        self.assertEqual('3',self.sql("select count(*) from gq_sessions where preview_run_id<>'' and is_test"))
        self.assertEqual('3',self.sql("select count(*) from gq_external_identifiers where preview_run_id<>''"))
        self.sql("insert into gq_study_plans(study_id,model) select 'other',jsonb_set(model,'{study_id}','\"other\"') from gq_study_plans where study_id='trial';")
        foreign=str(uuid.uuid4())
        with self.assertRaisesRegex(RuntimeError,'invalid or expired'):
            self.sql(f"set role anon; select greedyq_start_prolific_preview('{foreign}','abcdefghijklmnopqrstuvwx','other','1','0.2','release',true,'{'a'*24}','{'b'*24}','{'c'*24}','{grant}');")
        self.assertEqual('0',self.sql(f"select count(*) from gq_sessions where id='{foreign}'"))
        with self.assertRaisesRegex(RuntimeError,'permission denied'):self.sql("set role anon; select greedyq_issue_preview('trial');")
        with self.assertRaisesRegex(RuntimeError,'invalid or expired'):start(str(uuid.uuid4()),'f'*64)
        self.sql("update gq_preview_grants set expires_at=now()-interval '1 second'")
        with self.assertRaisesRegex(RuntimeError,'invalid or expired'):start(str(uuid.uuid4()))
        self.prolific_plan(False)
        with self.assertRaisesRegex(RuntimeError,'preview forbidden'):start(str(uuid.uuid4()),test=False)
        with self.assertRaisesRegex(RuntimeError,'registered Prolific test'):self.sql("select greedyq_issue_preview('trial')")

    def test_prolific_concurrent_duplicates_and_test_real_isolation(self):
        self.prolific_plan();ids=[str(uuid.uuid4()) for _ in range(8)]
        def attempt(sid):
            try:self.prolific_start(sid);return True
            except RuntimeError:return False
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(attempt,ids))
        self.assertEqual(1,sum(results));self.assertEqual('1',self.sql('select count(*) from gq_sessions'))
        self.prolific_plan(False);self.prolific_start(str(uuid.uuid4()),test=False)
        self.assertEqual('2',self.sql('select count(*) from gq_external_identifiers'))

    def test_prolific_production_cannot_save_without_registration(self):
        self.prolific_plan(False);sid=str(uuid.uuid4())
        self.sql(f"set role anon; select greedyq_create_session('{sid}','abcdefghijklmnopqrstuvwx','trial','1','0.2','release',false)")
        with self.assertRaisesRegex(RuntimeError,'registration required'):
            self.sql(f"set role anon; select greedyq_save_session('{sid}','abcdefghijklmnopqrstuvwx','{{\"page\":\"baseline\",\"answers\":{{\"consent\":\"yes\"}}}}','consent')")
        with self.assertRaisesRegex(RuntimeError,'invalid production'):
            self.prolific_start(str(uuid.uuid4()),pid='short',test=False)
        self.prolific_start(sid,test=False)
        self.sql(f"set role anon; select greedyq_withdraw_session('{sid}','abcdefghijklmnopqrstuvwx')")
        self.assertEqual('withdrawn',self.sql(f"select lifecycle_state from gq_sessions where id='{sid}'"))

    def test_concurrent_blocks_resume_and_permissions(self):
        ids=[self.participant() for _ in range(40)]
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            assigned=list(pool.map(self.assign,ids))
        self.assertEqual(20,assigned.count("a"))
        self.assertEqual("10",self.sql("select count(*) from (select block_id from gq_assignments group by block_id having count(*)=4 and count(*) filter(where condition='a')=2)t;"))
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            repeated=list(pool.map(self.assign,[ids[0]]*16))
        self.assertEqual({assigned[0]},set(repeated))
        self.assertEqual("40",self.sql("select count(*) from gq_assignments;"))
        with self.assertRaisesRegex(RuntimeError,"permission denied"):
            self.sql("set role anon; select * from gq_allocation_sequences;")

    def test_consent_boundary_and_test_isolation(self):
        for sid in (self.participant(page="welcome"),self.participant(consent="no")):
            with self.assertRaises(RuntimeError): self.assign(sid)
        test=[self.participant() for _ in range(4)]; real=[self.participant(False) for _ in range(4)]
        for t,r in zip(test,real): self.assign(t);self.assign(r,False)
        self.assertEqual("2",self.sql("select count(*) from gq_allocation_sequences where cardinality(remaining)=0 and block_number=1;"))
        with self.assertRaisesRegex(RuntimeError,"mismatch"): self.assign(test[0],False)

    def test_withdrawal_does_not_reuse_slot(self):
        sid=self.participant();self.assign(sid)
        self.sql(f"set role anon; select public.greedyq_withdraw_session('{sid}','abcdefghijklmnopqrstuvwx');")
        self.assertEqual("3",self.sql("select cardinality(remaining) from gq_allocation_sequences;"))
        with self.assertRaisesRegex(RuntimeError,"ended"): self.assign(sid)
        for _ in range(3): self.assign(self.participant())
        self.assertEqual("1|0",self.sql("select block_number,cardinality(remaining) from gq_allocation_sequences;"))

    def test_weighted_block_and_simple(self):
        self.model["randomization"].update(conditions={"a":2,"b":1},block_size=6);self.register()
        values=[self.assign(self.participant()) for _ in range(12)]
        self.assertEqual(8,values.count("a"))
        self.sql("truncate gq_sessions cascade; truncate gq_allocation_sequences;")
        self.model["randomization"]["method"]="simple";self.model["randomization"].pop("block_size");self.register()
        values=[self.assign(self.participant()) for _ in range(70)]
        self.assertTrue(25<values.count("a")<66)
        self.assertEqual("0",self.sql("select count(*) from gq_assignments where block_id is not null;"))
        self.assertTrue(any(values[i]==values[i+1]==values[i+2] for i in range(68)))

    def test_saved_order_stable_and_anchors(self):
        sid=self.participant()
        def save(order):
            state=json.dumps({"page":"baseline","answers":{"consent":"yes"},"question_orders":{"baseline":order}})
            return self.sql(f"set role anon; select public.greedyq_save_session('{sid}','abcdefghijklmnopqrstuvwx','{state}',null);")
        with self.assertRaisesRegex(RuntimeError,"fixed question"): save(["q3","q1","q2"])
        save(["q2","q1","q3"]);save(["q2","q1","q3"])
        with self.assertRaisesRegex(RuntimeError,"order changed"): save(["q1","q2","q3"])
        self.assertEqual('["q2", "q1", "q3"]',self.sql("select question_orders->'baseline' from gq_sessions;"))
        self.sql(f"set role anon; select greedyq_withdraw_session('{sid}','abcdefghijklmnopqrstuvwx');")
        self.assertEqual('{}',self.sql('select question_orders from gq_sessions;'))

    def test_failed_write_rolls_back_draw_and_resume_has_contract(self):
        sid=self.participant()
        self.sql("create function gq_test_fail() returns trigger language plpgsql as $$ begin raise exception 'injected failure'; end; $$; create trigger gq_test_fail before insert on gq_assignments for each row execute function gq_test_fail();")
        try:
            with self.assertRaisesRegex(RuntimeError,'injected failure'):self.assign(sid)
            self.assertEqual('0',self.sql('select count(*) from gq_allocation_sequences;'))
            self.assertEqual('0',self.sql('select count(*) from gq_assignments;'))
        finally:self.sql('drop trigger gq_test_fail on gq_assignments; drop function gq_test_fail();')
        condition=self.assign(sid)
        response=json.loads(self.sql(f"set role anon; select greedyq_resume_session('{sid}','abcdefghijklmnopqrstuvwx');"))
        self.assertEqual(condition,response['condition']);self.assertEqual('randomization-1',response['runtime_contract'])
        self.assertEqual(self.model,response['registered_model'])
