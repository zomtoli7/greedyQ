import http.cookiejar
import tempfile
import threading
import unittest
import urllib.parse
import urllib.request
from pathlib import Path

from greedyq.build import build, load_study
from greedyq.runtime import Store, parse_form, structured_answer_problem
from greedyq.server import serve


ROOT = Path(__file__).resolve().parents[1]


class RespondentRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name) / "runtime.sqlite3"
        _, self.model = build(ROOT / "examples/complete-study", write=False)
        _, _, self.config = load_study(ROOT / "examples/complete-study")
        self.store = Store(self.db)

    def tearDown(self): self.temp.cleanup()

    def advance_to_baseline(self, sid, age=30):
        self.store.transition(sid, "welcome", {}, self.model, self.config)
        self.store.transition(sid, "consent", {"consent_choice":"yes"}, self.model, self.config)
        self.store.transition(sid, "eligibility", {"age":age}, self.model, self.config)

    def test_consent_is_recorded_before_research_answers(self):
        sid=self.store.create(self.model,self.config)
        self.store.transition(sid,"welcome",{},self.model,self.config)
        self.store.transition(sid,"consent",{"consent_choice":"yes"},self.model,self.config)
        with self.store.connect() as db:
            self.assertEqual("accepted",db.execute("select decision from consent_events where session_id=?",(sid,)).fetchone()[0])
            self.assertEqual(0,db.execute("select count(*) from answers where session_id=?",(sid,)).fetchone()[0])

    def test_refusal_reaches_terminal_without_research_answers(self):
        sid=self.store.create(self.model,self.config);self.store.transition(sid,"welcome",{},self.model,self.config)
        state=self.store.transition(sid,"consent",{"consent_choice":"no"},self.model,self.config)
        self.assertEqual("consent_refused",state["session"]["lifecycle_state"])
        self.assertEqual({},state["answers"])

    def test_partial_answers_and_current_page_resume(self):
        sid=self.store.create(self.model,self.config);self.advance_to_baseline(sid)
        state=self.store.state(sid)
        self.assertEqual("baseline",state["session"]["current_page"])
        self.assertEqual(30,state["answers"]["age"])

    def test_minor_is_screened_out(self):
        sid=self.store.create(self.model,self.config);self.store.transition(sid,"welcome",{},self.model,self.config);self.store.transition(sid,"consent",{"consent_choice":"yes"},self.model,self.config)
        state=self.store.transition(sid,"eligibility",{"age":17},self.model,self.config)
        self.assertEqual("screened_out",state["session"]["lifecycle_state"])

    def test_assignment_is_persisted_and_balanced(self):
        conditions=[]
        for _ in range(8):
            sid=self.store.create(self.model,self.config);self.advance_to_baseline(sid)
            state=self.store.transition(sid,"baseline",{"support_pre":4,"familiarity":"moderate"},self.model,self.config)
            first=state["condition"];conditions.append(first)
            self.assertEqual(first,self.store.state(sid)["condition"])
        self.assertLessEqual(abs(conditions.count("control")-conditions.count("treatment")),1)

    def test_concurrent_assignment_remains_balanced(self):
        conditions=[];errors=[];guard=threading.Lock()
        def respondent():
            try:
                sid=self.store.create(self.model,self.config);self.advance_to_baseline(sid)
                state=self.store.transition(sid,"baseline",{"support_pre":4,"familiarity":"moderate"},self.model,self.config)
                with guard:conditions.append(state["condition"])
            except Exception as exc:
                with guard:errors.append(exc)
        workers=[threading.Thread(target=respondent) for _ in range(16)]
        for worker in workers:worker.start()
        for worker in workers:worker.join()
        self.assertEqual([],errors);self.assertEqual(16,len(conditions));self.assertLessEqual(abs(conditions.count("control")-conditions.count("treatment")),1)

    def test_required_answer_failure_rolls_back(self):
        sid=self.store.create(self.model,self.config);self.advance_to_baseline(sid)
        with self.assertRaisesRegex(ValueError,"Please answer"):
            self.store.transition(sid,"baseline",{},self.model,self.config)
        self.assertEqual("baseline",self.store.state(sid)["session"]["current_page"])

    def test_complete_experiment_path_reaches_completed_state(self):
        sid=self.store.create(self.model,self.config);self.advance_to_baseline(sid)
        state=self.store.transition(sid,"baseline",{"support_pre":4,"familiarity":"moderate"},self.model,self.config)
        stimulus=state["session"]["current_page"];self.assertIn(stimulus,("stimulus_control","stimulus_treatment"))
        self.store.transition(sid,stimulus,{},self.model,self.config)
        self.store.transition(sid,"post_measure",{"comprehension":"three_libraries","frame_perception":4,"attention_check":5},self.model,self.config)
        self.store.transition(sid,"outcomes",{"support_post":4,"usefulness":{"residents":4,"access":4}},self.model,self.config)
        self.store.transition(sid,"demographics",{},self.model,self.config)
        state=self.store.transition(sid,"participant_control",{"withdraw_now":"submit"},self.model,self.config)
        self.assertEqual("completed",state["session"]["lifecycle_state"])
        self.assertGreaterEqual(len(state["answers"]),8)

    def test_withdrawal_deletion_is_atomic_and_idempotent(self):
        sid=self.store.create(self.model,self.config);self.advance_to_baseline(sid)
        with self.store.connect() as db:
            db.execute("update sessions set current_page='participant_control',lifecycle_state='in_progress' where id=?",(sid,))
            db.execute("insert into answers values(?,?,?,?)",(sid,"comments",'"private answer"',1))
        state=self.store.transition(sid,"participant_control",{"withdraw_now":"withdraw","deletion_request":"yes"},self.model,self.config)
        self.assertEqual("withdrawn",state["session"]["lifecycle_state"]);self.assertEqual({},state["answers"]);self.assertIsNone(state["condition"])
        again=self.store.transition(sid,"participant_control",{},self.model,self.config)
        self.assertEqual("withdrawn",again["session"]["lifecycle_state"])

    def test_http_cookie_resumes_same_session(self):
        server=serve(self.model,self.config,self.store,0);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            jar=http.cookiejar.CookieJar();opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar));base="http://localhost:%d"%server.server_address[1]
            first=opener.open(base+"/study").read().decode();self.assertIn("Digital Service Information Study",first)
            opener.open(urllib.request.Request(base+"/answer",data=b"",method="POST"))
            consent=opener.open(base+"/study").read().decode();self.assertIn("Do you consent",consent)
            opener.open(urllib.request.Request(base+"/answer",data=urllib.parse.urlencode({"consent_choice":"yes"}).encode(),method="POST"))
            eligibility=opener.open(base+"/study").read().decode();self.assertIn("What is your age",eligibility)
            self.assertEqual(1,len(list(jar)))
        finally:server.shutdown();server.server_close();thread.join()

    def test_http_page_contains_live_conditional_question_support(self):
        server=serve(self.model,self.config,self.store,0);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            body=urllib.request.urlopen("http://localhost:%d/study"%server.server_address[1]).read().decode()
            self.assertIn("question-block",body);self.assertIn("document.addEventListener('change',update)",body)
        finally:server.shutdown();server.server_close();thread.join()

    def test_reference_runtime_parses_and_checks_advanced_answers(self):
        page={"questions":[
            {"id":"rank","type":"rank_order","label":"Rank","required":True,"options":[{"value":"a"},{"value":"b"}]},
            {"id":"sum","type":"constant_sum","label":"Allocate","options":[{"value":"a"},{"value":"b"}],"total":100},
            {"id":"group","type":"pick_group_rank","label":"Group","required":True,"options":[{"value":"a"}],"groups":[{"value":"main"}]},
            {"id":"place","type":"drill_down","label":"Place","required":True,"path_separator":" > ","options":[{"label":"Asia > Korea > Seoul","value":"seoul"}]},
            {"id":"time","type":"timing","label":"Time"},
        ]}
        form={"rank:a":["1"],"rank:b":["2"],"sum:a":["40"],"sum:b":["60"],"group:a:group":["main"],"group:a:rank":["1"],"place":["seoul"],"time":["12"]}
        answers=parse_form(page,form)
        self.assertEqual({"a":1,"b":2},answers["rank"])
        self.assertEqual(["Asia","Korea","Seoul"],answers["place"])
        self.assertEqual({"seconds_on_page":12},answers["time"])
        self.assertIsNone(structured_answer_problem(page["questions"][1],answers["sum"]))
        self.assertIn("add up",structured_answer_problem(page["questions"][1],{"a":40,"b":40}))
        self.assertIn("negative",structured_answer_problem(page["questions"][1],{"a":110,"b":-10}))
        self.assertIn("only once",structured_answer_problem(page["questions"][0],{"a":1,"b":1}))
        self.assertIn("every item",structured_answer_problem(page["questions"][0],{"a":1}))
        self.assertIn("invalid rank",structured_answer_problem(page["questions"][0],{"a":1,"b":3}))
        self.assertIn("every level",structured_answer_problem(page["questions"][3],["Asia","Korea"]))


if __name__=="__main__":unittest.main()
