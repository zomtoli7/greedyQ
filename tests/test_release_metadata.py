import json
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]

class ReleaseMetadataTests(unittest.TestCase):
    def test_current_release_is_consistent_in_public_headers_and_runtimes(self):
        release=json.loads((ROOT/'release.json').read_text())
        identifier=release['release']
        self.assertRegex(identifier,r'^0\.2_\d{4}-\d{2}-\d{2}_[0-9a-f]{7,12}$')
        self.assertTrue(release['source_commit'].startswith(identifier.rsplit('_',1)[-1]))
        for relative in ('README.md','README(kor).md','guides/core/guide.md','guides/core/guide(kor).md'):
            self.assertIn(identifier,(ROOT/relative).read_text()[:3000])
        self.assertIn('__release__ = "'+identifier+'"',(ROOT/'greedyq/__init__.py').read_text())
        self.assertIn('const RELEASE = "'+identifier+'"',(ROOT/'web/greedyq-core.js').read_text())
        for suffix in ('','(kor)'):self.assertTrue((ROOT/f'updates/0.2/{identifier}{suffix}.md').is_file())

    def test_generated_surveys_record_current_provenance_without_rewriting_historical_evidence(self):
        release=json.loads((ROOT/'release.json').read_text())['release']
        for name in ('complete-study','simple-satisfaction-study','control-gallery'):
            root=ROOT/'examples'/name
            self.assertIn('version: "'+release+'"',(root/'survey.qmd').read_text())
            self.assertEqual(release,json.loads((root/'preview-model.json').read_text())['greedyq_version'])
        for path in ('templates/browser/respondent.html','templates/browser/preview.html','templates/supabase/connection-test.html'):
            self.assertIn(release,(ROOT/path).read_text())
        metadata=json.loads((ROOT/'release.json').read_text())
        if metadata['prolific_paid_pilot']=='paused_for_review':self.assertFalse(metadata['payment_verified'])
