import collections
import unittest
import copy
import json
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from greedyq.runtime import Store
from pathlib import Path
from greedyq.build import load_study
from greedyq.validator import validate
from greedyq.compiler import compile_preview
from greedyq.randomization import draw, shuffle, plan_problem, question_order


def plan(method="fixed_block", weights=None):
    result={"id":"trial","unit":"respondent","persistence_key":"session_id","method":method,"conditions":weights or {"a":1,"b":1}}
    if method=="fixed_block": result["block_size"]=sum(result["conditions"].values())*2
    return result


class RandomizationTests(unittest.TestCase):
    def test_sqlite_concurrent_and_restart(self):
        model={"study_id":"sqlite_trial","start_page":"baseline","pages":[{"id":"baseline","questions":[{"id":"q1","type":"text"},{"id":"q2","type":"text"}],"shuffle_questions":["q1","q2"],"next":"done"},{"id":"done","questions":[],"terminal":"completed"}]}
        config={"study":{"version":"1"},"randomization":[{**plan(),"assignment_point":{"after_page":"baseline"}}]}
        with tempfile.TemporaryDirectory() as tmp:
            stores=[Store(Path(tmp)/'db.sqlite') for _ in range(4)]
            ids=[stores[0].create(model,config) for _ in range(24)]
            with ThreadPoolExecutor(max_workers=4) as pool:
                states=list(pool.map(lambda pair:stores[pair[0]%4].transition(pair[1],'baseline',{},model,config),enumerate(ids)))
            self.assertEqual(12,sum(s['condition']=='a' for s in states))
            resumed=Store(Path(tmp)/'db.sqlite')
            self.assertEqual(states[0]['question_orders'],resumed.state(ids[0])['question_orders'])
            self.assertEqual(states[0]['condition'],resumed.state(ids[0])['condition'])
            with resumed.connect() as db:
                self.assertEqual(6,db.execute('select count(distinct block_id) from assignments').fetchone()[0])

    def test_invalid_configuration_parity(self):
        root=Path(__file__).resolve().parents[1]
        node=Path('/Users/dongsookim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node')
        if not node.exists(): self.skipTest('Node unavailable')
        _,parsed,base=load_study(root/'examples/complete-study')
        cases=[]
        for patch in ({"method":"bad"},{"block_size":3},{"conditions":{"a":0,"b":1}},{"unit":"cluster"},{"strata":["age"]},{"conditions":None},{"assignment_point":False},{"store":[]}):
            config=copy.deepcopy(base);config['randomization'][0].update(patch);cases.append(config)
        config=copy.deepcopy(base);config['randomization']*=2;cases.append(config)
        config=copy.deepcopy(base);config['randomization']={};cases.append(config)
        for order in ([{"page":"missing","questions":["a","b"]}], [{"page":"consent","questions":["consent_choice","consent_choice"]}], False):
            config=copy.deepcopy(base);config['question_order']=order;cases.append(config)
        for config in cases:
            expected=validate(parsed,config)
            proc=subprocess.run([str(node),'-e','const g=require("./web/greedyq-core.js"),x=JSON.parse(require("fs").readFileSync(0,"utf8"));console.log(JSON.stringify(g.validateSurvey(x.p,x.c)))'],cwd=root,input=json.dumps({'p':parsed,'c':config}),capture_output=True,text=True,check=True)
            actual=json.loads(proc.stdout)
            self.assertEqual([(i['code'],i['message']) for i in expected['issues']],[(i['code'],i['message']) for i in actual['issues']])

    def test_valid_shuffling_and_custom_condition_field_parity(self):
        root=Path(__file__).resolve().parents[1];node=Path('/Users/dongsookim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node')
        if not node.exists():self.skipTest('Node unavailable')
        _,parsed,config=load_study(root/'examples/complete-study')
        config['randomization'][0]['store']['condition_as']='my_arm'
        for rule in config['logic']['skip']: rule['if']=rule['if'].replace('assignment_condition','my_arm')
        page=next(p for p in parsed['pages'] if len(p['questions'])>=2 and p['id']!='consent')
        config['question_order']=[{'page':page['id'],'questions':[q['id'] for q in page['questions']]}]
        proc=subprocess.run([str(node),'-e','const g=require("./web/greedyq-core.js"),x=JSON.parse(require("fs").readFileSync(0,"utf8"));console.log(JSON.stringify(g.compileSurvey(x.p,x.c)))'],cwd=root,input=json.dumps({'p':parsed,'c':config}),capture_output=True,text=True,check=True)
        self.assertEqual(compile_preview(parsed,config),json.loads(proc.stdout))

    def test_simple_is_independent_not_balanced(self):
        self.assertEqual([("a",None)]*20,[draw(plan("simple"),{},lambda n:0) for _ in range(20)])

    def test_blocks_and_weights(self):
        for weights in ({"a":1,"b":1},{"a":2,"b":1},{"a":1,"b":1,"c":1}):
            p=plan(weights=weights); state={}
            for block in range(1,101):
                draws=[draw(p,state) for _ in range(p["block_size"])]
                self.assertEqual({k:w*2 for k,w in weights.items()},dict(collections.Counter(c for c,b in draws)))
                self.assertEqual({str(block)},{b for c,b in draws})

    def test_reference_vector_and_anchors(self):
        self.assertEqual(["b","c","d","a"],shuffle(list("abcd"),lambda n:0))
        page={"questions":[{"id":q} for q in ["intro","a","b","c","end"]],"shuffle_questions":["a","b","c"]}
        self.assertEqual(["intro","b","c","a","end"],question_order(page,lambda n:0))

    def test_invalid_plans(self):
        for patch in ({"method":"least_count"},{"conditions":{"a":0,"b":1}},{"conditions":{"a":True,"b":1}},{"block_size":3},{"unit":"cluster"},{"persistence_key":"email"}):
            self.assertIsNotNone(plan_problem({**plan(),**patch}))

    def test_simple_distribution(self):
        counts=collections.Counter(draw(plan("simple",{"a":2,"b":1}),{})[0] for _ in range(12000))
        self.assertTrue(7400<counts["a"]<8600,counts)

if __name__=="__main__": unittest.main()
