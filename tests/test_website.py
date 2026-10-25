import json
from pathlib import Path
import re
import unittest
from tools.build_website_embed import build

ROOT=Path(__file__).resolve().parents[1]

class WebsiteTests(unittest.TestCase):
    def test_collect_navigation_and_adjacent_pages_are_consistent_in_every_language(self):
        _,data=build(write=False)
        for language,content in data.items():
            pages={page['id']:page for page in content['guide']}
            group=next(ids for _,ids in content['guideGroups'] if 'deploy' in ids)
            self.assertEqual(['deploy','prolific','results'],group[group.index('deploy'):group.index('deploy')+3])
            for page in ('deploy','results'):self.assertIn('data-topic="prolific"',pages[page]['body'])
            self.assertIn('gq_preview',pages['prolific']['body']);self.assertIn('24',pages['prolific']['body'])
            self.assertEqual(len(pages),len(content['guide']))
    def test_generated_file_matches_sources_and_every_history_note_is_present(self):
        html,data=build(write=False)
        self.assertEqual(html,(ROOT/'website/google-sites-embed.html').read_text())
        release=json.loads((ROOT/'release.json').read_text())
        for content in data.values():
            self.assertIn(release['release'],content['draft'])
            history=next(page['body'] for page in content['about'] if page['id']=='updates')
            for note in (ROOT/'updates/0.2').glob('*.md'):
                if '(kor)' not in note.name:self.assertIn(note.stem,history)
        self.assertNotIn('__GREEDYQ_SITE_CONTENT__',html)
    def test_embed_has_no_operator_deployments_or_private_capabilities(self):
        html,_=build(write=False)
        for forbidden in ('greedyq-prolific-survey.vercel.app','greedyq-prolific-results.vercel.app','sb_secret_','service_role_key','gzhgtfbdgbuuehgsadmi','C1HEJQ9F','CCS9RKLM','CMD6M77M'):
            self.assertNotIn(forbidden,html)
        self.assertEqual(len(re.findall(r'<script(?:\s[^>]*)?>',html)),len(re.findall(r'</script>',html)))
