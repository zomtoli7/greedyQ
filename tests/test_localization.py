import copy
import json
import subprocess
import unittest
from pathlib import Path
from greedyq.build import load_study
from greedyq.compiler import compile_preview
from greedyq.localization import LANGUAGES, MESSAGES, translate
from greedyq.validator import validate

ROOT=Path(__file__).resolve().parents[1]
NODE='/Users/dongsookim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node'

class LocalizationTests(unittest.TestCase):
    def test_catalog_and_compiler_parity(self):
        for language in LANGUAGES:
            payload={'language':language,'messages':list(MESSAGES)}
            script="const g=require('./web/greedyq-core.js'),p=JSON.parse(process.argv[1]);console.log(JSON.stringify(p.messages.map(m=>g.translate(p.language,m))))"
            result=json.loads(subprocess.check_output([NODE,'-e',script,json.dumps(payload)],cwd=ROOT))
            self.assertEqual(result,[translate(language,m) for m in MESSAGES])
            _,parsed,config=load_study(ROOT/'examples/simple-satisfaction-study')
            parsed['front_matter']['greedyq']['language']=language
            parsed['front_matter'].pop('system-messages',None)
            expected=compile_preview(parsed,config)
            script="const g=require('./web/greedyq-core.js'),p=JSON.parse(process.argv[1]);console.log(JSON.stringify(g.compileSurvey(p[0],p[1])))"
            actual=json.loads(subprocess.check_output([NODE,'-e',script,json.dumps([parsed,config])],cwd=ROOT))
            self.assertEqual(expected,actual)
            self.assertEqual(expected['messages']['next'],translate(language,'Continue'))

    def test_unsupported_language_fails_and_content_is_preserved(self):
        _,parsed,config=load_study(ROOT/'examples/simple-satisfaction-study')
        original=copy.deepcopy(parsed['pages'])
        parsed['front_matter']['greedyq']['language']='zh-TW'
        compile_preview(parsed,config)
        self.assertEqual(parsed['pages'],original)
        parsed['front_matter']['greedyq']['language']='xx'
        self.assertTrue(any('greedyq.language' in i['message'] for i in validate(parsed,config)['issues']))
        with self.assertRaises(ValueError):compile_preview(parsed,config)
