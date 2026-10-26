"""Public bootstrap generation without JavaScript, provider access or private data."""
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

from tools.build_bootstrap import build, render

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.links = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        self.links.extend(v for k, v in attrs if tag == 'a' and k == 'href')

    def handle_data(self, text):
        self.text.append(text)


class BootstrapTests(unittest.TestCase):
    def test_formats_share_one_source_and_allowlist_only_public_files(self):
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, {}, clear=False):
            os.environ.pop('COMMIT_REF', None)
            out = Path(d) / 'site'
            m = build(out)
            self.assertEqual(11, len(list(out.iterdir())))
            self.assertEqual((out / 'START-HERE.html').read_bytes(), (out / 'index.html').read_bytes())
            for name, digest in m['files'].items():
                self.assertEqual(hashlib.sha256((out / name).read_bytes()).hexdigest(), digest)
            for suffix, language in [('', 'en'), ('(kor)', 'ko'), ('(zh-CN)', 'zh-CN')]:
                markdown = (out / ('START-HERE' + suffix + '.md')).read_text()
                page = (out / ('START-HERE' + suffix + '.html')).read_text()
                self.assertEqual(page, render(markdown, language))
                p = Page(); p.feed(page)
                self.assertNotIn('script', p.tags)
                self.assertNotIn('iframe', p.tags)
                self.assertNotIn('form', p.tags)
                self.assertIn('greedyq-start-bootstrap-1', ''.join(p.text))
                self.assertIn('INITIALIZE', ''.join(p.text))
                if not suffix:
                    self.assertFalse(re.search(r'[\uac00-\ud7a3\u4e00-\u9fff]', ''.join(p.text)))
                self.assertIn(m['repository_snapshot'] + '/INITIALIZE', ''.join(p.text))
                self.assertTrue(any(m['repository_snapshot'] + '/INITIALIZE' in x for x in p.links))
                self.assertIn('./START-HERE', markdown)
                self.assertNotIn('/blob/main/', markdown)
            self.assertFalse(m['live_deployment_verified'])
            self.assertFalse(m['requires_browser_javascript'])
            self.assertEqual(['experiment', 'simple'], sorted(k for k, x in json.loads((ROOT / 'registry/guide-index.json').read_text())['components'].items() if x['kind'] == 'profile'))

    def test_mismatched_checkout_and_unrelated_output_are_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / 'site'; out.mkdir(); keep = out / 'private.txt'; keep.write_text('keep')
            with patch.dict(os.environ, {'COMMIT_REF': '0' * 40}):
                with self.assertRaises(ValueError): build(out)
            with patch.dict(os.environ, {}, clear=False):
                os.environ.pop('COMMIT_REF', None)
                with self.assertRaises(ValueError): build(out)
            self.assertEqual('keep', keep.read_text())

    def test_resume_rules_and_interview_live_in_initialize_not_the_public_front_door(self):
        front = (ROOT / 'START-HERE.md').read_text()
        initialize = (ROOT / 'INITIALIZE.md').read_text()
        self.assertNotIn('What would you like to learn', front)
        self.assertIn('What would you like to learn', initialize)
        self.assertIn('guide-lock.json', initialize)
        self.assertIn('locked version', front)
        self.assertIn('not a resumable', front)
        self.assertEqual('INITIALIZE.md', json.loads((ROOT / 'registry/guide-index.source.json').read_text())['bootstrap'])
