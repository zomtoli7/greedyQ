"""Regression for an unread URL followed by an improvised survey interview."""
import json
from pathlib import Path
import unittest
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]

class GuideAccessTests(unittest.TestCase):
    def test_copyable_website_prompts_contain_the_stop_condition_before_the_url(self):
        data=json.loads((ROOT/'website/content.json').read_text())
        for lang,stop in [('en','do not start'),('ko','문항을 만들지 마'),('zh','不要开始')]:
            prompt=data[lang]['start']['prompt'];self.assertIn(stop,prompt);self.assertLess(prompt.index(stop),prompt.index('https://github.com/'))
        self.assertIn('Import Code',data['en']['start']['after'])

    def test_all_entry_languages_offer_raw_import_and_full_attachment_without_fake_success(self):
        for suffix in ['','(kor)','(zh-CN)']:
            access=(ROOT/f'GUIDE-ACCESS{suffix}.md').read_text()
            self.assertIn('https://raw.githubusercontent.com/zomtoli7/greedyQ/main/START-HERE.md',access)
            self.assertIn('Import Code',access);self.assertIn('.txt',access)
            self.assertIn('GUIDE-ACCESS',(ROOT/f'START-HERE{suffix}.md').read_text())
        self.assertIn('was not retested',(ROOT/'GUIDE-ACCESS.md').read_text())

    def test_cbc_collection_schema_and_synthetic_example_do_not_authorize_production(self):
        schema=json.loads((ROOT/'schemas/cbc-collection.schema.json').read_text());Draft202012Validator.check_schema(schema)
        value=json.loads((ROOT/'drafts/v0.3/cbc/golden-reference/collection.test.example.json').read_text());v=Draft202012Validator(schema)
        self.assertEqual([],list(v.iter_errors(value)));value['mode']='production';self.assertTrue(list(v.iter_errors(value)))
        self.assertTrue(all(x is False for x in value['approvals'].values()))
