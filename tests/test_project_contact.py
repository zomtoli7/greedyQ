"""Project support must stay distinct from an individual study's contact."""
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
EMAIL='greedyq.contact@gmail.com'

class ProjectContactTests(unittest.TestCase):
    def test_three_language_entry_guides_link_verified_contact(self):
        for suffix in ['', '(kor)', '(zh-CN)']:
            for stem in ['README','START-HERE','USER-GUIDE','CONTACT','guides/core/guide','guides/greedyq-guide-compact']:
                self.assertIn(EMAIL,(ROOT/(stem+suffix+'.md')).read_text())
        contact=(ROOT/'CONTACT.md').read_text()
        self.assertIn('not automatically the contact for an individual research study',contact)
        self.assertIn('must not send a message',contact)

    def test_website_contact_and_release_metadata_agree(self):
        site=json.loads((ROOT/'website/content.json').read_text())
        for language in ['en','ko','zh']:
            contact=next(p for p in site[language]['about'] if p['id']=='contact')
            self.assertIn('mailto:'+EMAIL,contact['body'])
        metadata=json.loads((ROOT/'release.json').read_text())
        self.assertEqual(EMAIL,metadata['project_contact']['email'])
        self.assertFalse(metadata['project_contact']['individual_study_contact'])

    def test_cbc_preview_does_not_claim_live_fielding(self):
        release=json.loads((ROOT/'release.json').read_text())
        self.assertFalse(release['next_line']['live_collection'])
        self.assertEqual('0.3-preview.1',release['next_line']['preview_schema'])
        for name in ['CBC.md','CBC(kor).md','CBC(zh-CN).md']:
            self.assertIn('0.3-preview.1',(ROOT/name).read_text())
