import copy,json,subprocess,tempfile,unittest
from pathlib import Path
from greedyq.build import load_study
from greedyq.prolific import parse_launch,resolve_launch,integration_plan
from greedyq.compiler import compile_preview
from tools.prepare_prolific import prepare
ROOT=Path(__file__).resolve().parents[1]
NODE='/Users/dongsookim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'

class ProlificTests(unittest.TestCase):
    def js(self,name,args):
        code='const g=require("./web/greedyq-core.js"),a=JSON.parse(process.argv[2]);try{console.log(JSON.stringify(g[process.argv[1]](...a)))}catch(e){console.log(JSON.stringify({error:e.message}))}'
        return json.loads(subprocess.check_output([NODE,'-e',code,name,json.dumps(args)],cwd=ROOT))
    def test_launch_parity_and_invalid_identifiers(self):
        for mode in ('test','production'):
            for query in ('','?PROLIFIC_PID=','?PROLIFIC_PID=one&PROLIFIC_PID=two&STUDY_ID=s&SESSION_ID=x','?PROLIFIC_PID={{%PROLIFIC_PID%}}&STUDY_ID=s&SESSION_ID=x','?PROLIFIC_PID=p&STUDY_ID=s&SESSION_ID=x','?prolific_token=secret','?PROLIFIC_PID='+'a'*24+'&STUDY_ID='+'b'*24+'&SESSION_ID='+'c'*24):
                for name,fn in (('parseProlificLaunch',parse_launch),('resolveProlificLaunch',resolve_launch)):
                    self.assertEqual(fn(query,mode),self.js(name,[query,mode]))
        self.assertEqual('failed',parse_launch('?PROLIFIC_PID='+'a'*24+'&STUDY_ID='+'b'*24+'&SESSION_ID='+'c'*24,'production','d'*24)['status'])
    def test_plan_compiler_and_offline_setup(self):
        _,parsed,config=load_study(ROOT/'examples/complete-study')
        self.assertEqual(integration_plan(config),self.js('prolificPlan',[config]))
        self.assertEqual(compile_preview(parsed,config),self.js('compileSurvey',[parsed,config]))
        fields=prepare(ROOT/'examples/complete-study','https://survey.example.test/')
        self.assertIn('{{%PROLIFIC_PID%}}',fields['api_external_study_url']);self.assertEqual('draft_not_published',fields['status'])
        for url in ('http://survey.test','https://survey.test/?token=secret','https://user:password@survey.test'):
            with self.assertRaises(ValueError):prepare(ROOT/'examples/complete-study',url)
    def test_repeat_preview_launch_parity_and_no_production_mode_switch(self):
        identifiers='PROLIFIC_PID='+'a'*24+'&STUDY_ID='+'b'*24+'&SESSION_ID='+'c'*24
        for mode in ('test','production'):
            for suffix in ('gq_preview=','gq_preview=invalid','gq_preview='+'d'*64,'gq_preview='+'d'*64+'&gq_preview='+'e'*64):
                query='?'+identifiers+'&'+suffix
                self.assertEqual(parse_launch(query,mode),self.js('parseProlificLaunch',[query,mode]))
        self.assertEqual('failed',resolve_launch('?gq_preview='+'d'*64)['status'])
        self.assertEqual('failed',parse_launch('?'+identifiers+'&gq_preview='+'d'*64,'production')['status'])
    def test_production_requires_reviewed_bound_distinct_paths(self):
        _,_,original=load_study(ROOT/'examples/complete-study')
        production=copy.deepcopy(original);production['respondents']['mode']='production'
        for stage in range(4):
            if stage==1:production['respondents']['prolific']={'study_id':'b'*24}
            if stage==2:production['respondents']['prolific']['completion_paths_reviewed']=True
            if stage==3:
                for i,outcome in enumerate(production['outcomes'].values()):outcome['redirect']='https://app.prolific.com/submissions/complete?cc=C123456'+str(i)
            with self.assertRaises(ValueError) as error:integration_plan(production)
            self.assertEqual({'error':str(error.exception)},self.js('prolificPlan',[production]))
        production['respondents']['prolific']['screening_mode']='custom'
        self.assertEqual(integration_plan(production),self.js('prolificPlan',[production]))
        outcomes=list(production['outcomes'].values());outcomes[1]['redirect']=outcomes[0]['redirect']
        with self.assertRaises(ValueError):integration_plan(production)
