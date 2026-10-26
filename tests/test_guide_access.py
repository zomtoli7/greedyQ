"""Regression for an unread URL followed by an improvised survey interview."""
import json
from pathlib import Path
import unittest
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]

class GuideAccessTests(unittest.TestCase):
    def test_entry_host_filter_is_first_and_does_not_offer_attachments_to_unsupported_hosts(self):
        for suffix in ['', '(kor)', '(zh-CN)']:
            entry=(ROOT/f'INITIALIZE{suffix}.md').read_text()
            self.assertTrue(entry.splitlines()[2].startswith('<!-- GREEDYQ_HOST_FILTER_START -->'))
            self.assertLess(entry.index('GREEDYQ_HOST_FILTER_START'),entry.index('GREEDYQ_DESKTOP_POLICY'))
            self.assertIn('GREEDYQ_HOST_FILTER_END',entry)
        policy=json.loads((ROOT/'schemas/authoring-support-policy.json').read_text())['researcher_authoring']
        self.assertEqual(policy['gate_order'],'before_guide_loading_and_study_interview')
        self.assertEqual(policy['unsupported_host_action'],'show_support_message_then_stop_without_attachment_request')
        self.assertEqual(policy['unknown_host_action'],'ask_app_and_desktop_status_then_wait')


    def test_desktop_support_is_required_even_when_a_web_host_can_read_the_guide(self):
        policy=json.loads((ROOT/'schemas/authoring-support-policy.json').read_text())
        authoring=policy['researcher_authoring']
        self.assertTrue(authoring['desktop_app_required'])
        self.assertEqual(authoring['official_host_families'], ['chatgpt_desktop','claude_desktop'])
        self.assertIn('gemini',authoring['unsupported_host_families'])
        self.assertFalse(authoring['ai_web_app_supported'])
        self.assertFalse(authoring['attachment_waives_host_requirement'])
        self.assertEqual(authoring['on_failure'],'stop_authoring_and_offer_desktop_handoff')
        self.assertIn('participant_survey',policy['browser_supported_for'])
        for suffix in ['', '(kor)', '(zh-CN)']:
            for stem in ['README','START-HERE','USER-GUIDE','GUIDE-ACCESS']:
                self.assertIn('GREEDYQ_DESKTOP_POLICY',(ROOT/f'{stem}{suffix}.md').read_text())
            policy_doc=(ROOT/f'SUPPORTED-ENVIRONMENTS{suffix}.md').read_text()
            for official in ['https://learn.chatgpt.com/docs/app','https://claude.com/download']:
                self.assertIn(official,policy_doc)
            self.assertNotIn('[Gemini for desktop]',policy_doc)
        # The unread-guide guard alone cannot authorize a web app via attachments.
        self.assertNotIn('Conduct the full interview',(ROOT/'guides/greedyq-guide.md').read_text().split('<!-- GREEDYQ_BUNDLE_START -->')[0])

    def test_copyable_website_prompts_contain_the_stop_condition_before_the_url(self):
        data=json.loads((ROOT/'website/content.json').read_text())
        for lang,stop in [('en','stop and tell me'),('ko','멈추고 알려줘'),('zh','停止并告诉我')]:
            prompt=data[lang]['start']['prompt'];self.assertIn(stop,prompt);self.assertLess(prompt.index(stop),prompt.index('https://greedyq.netlify.app/'))
        self.assertIn('installed desktop',data['en']['start']['after'])

    def test_all_entry_languages_offer_raw_import_and_full_attachment_without_fake_success(self):
        for suffix in ['','(kor)','(zh-CN)']:
            access=(ROOT/f'GUIDE-ACCESS{suffix}.md').read_text()
            self.assertIn('https://greedyq.netlify.app/',access)
            self.assertIn('https://raw.githubusercontent.com/zomtoli7/greedyQ/main/INITIALIZE.md',access)
            self.assertIn('SUPPORTED-ENVIRONMENTS',access);self.assertIn('.txt',access)
            self.assertIn('GUIDE-ACCESS',(ROOT/f'START-HERE{suffix}.md').read_text())
        self.assertIn('was not retested',(ROOT/'GUIDE-ACCESS.md').read_text())

    def test_cbc_collection_schema_and_synthetic_example_do_not_authorize_production(self):
        schema=json.loads((ROOT/'schemas/cbc-collection.schema.json').read_text());Draft202012Validator.check_schema(schema)
        value=json.loads((ROOT/'drafts/v0.3/cbc/golden-reference/collection.test.example.json').read_text());v=Draft202012Validator(schema)
        self.assertEqual([],list(v.iter_errors(value)));value['mode']='production';self.assertTrue(list(v.iter_errors(value)))
        self.assertTrue(all(x is False for x in value['approvals'].values()))
