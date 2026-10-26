"""Public bootstrap generation without JavaScript, provider access or private data."""
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from tools.build_bootstrap import build, build_managed, render

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
    def fake_checkout(self, folder):
        root = Path(folder)
        names = ['release.json', 'INITIALIZE.md', 'schemas/authoring-support-policy.json']
        names += ['START-HERE' + suffix + '.md' for suffix in ['', '(kor)', '(zh-CN)']]
        for name in names:
            target = root / name; target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        (root / '.gitignore').write_text('dist/\n')
        for command in [['git', 'init', '-q'], ['git', 'add', '.'],
                        ['git', '-c', 'user.name=Bootstrap Test', '-c', 'user.email=bootstrap@example.invalid',
                         'commit', '-qm', 'Synthetic bootstrap fixture']]:
            subprocess.run(command, cwd=root, check=True, capture_output=True)
        return root

    def test_managed_rebuild_handles_stale_extra_and_partial_cache_without_publishing_it(self):
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ, {}, clear=False):
            os.environ.pop('COMMIT_REF', None)
            root = self.fake_checkout(d); output = root / 'dist/bootstrap'
            output.mkdir(parents=True); (output / 'cached-extra.txt').write_text('preserve')
            (output / 'bootstrap-manifest.json').write_text('{"files":{"missing.html":"old"}}')
            manifest = build_managed(root)
            self.assertEqual(set(manifest['files']) | {'bootstrap-manifest.json'}, {p.name for p in output.iterdir()})
            backups = list((root / 'dist').glob('.bootstrap-previous-*'))
            self.assertEqual('preserve', (backups[0] / 'cached-extra.txt').read_text())
            (output / 'START-HERE.html').unlink()  # Partial cache, not unrelated source.
            build_managed(root)
            self.assertTrue((output / 'START-HERE.html').is_file())
            before = (output / 'index.html').read_bytes()
            with patch.dict(os.environ, {'COMMIT_REF': '0' * 40}):
                with self.assertRaises(ValueError): build_managed(root)
            self.assertEqual(before, (output / 'index.html').read_bytes())
            real_replace = os.replace
            def fail_new_publish(source, destination):
                if Path(source).name.startswith('.bootstrap-build-') and Path(destination).resolve() == output.resolve():
                    raise OSError('Synthetic publish swap failure')
                return real_replace(source, destination)
            with patch('tools.build_bootstrap.os.replace', side_effect=fail_new_publish):
                with self.assertRaises(OSError): build_managed(root)
            self.assertEqual(before, (output / 'index.html').read_bytes())

    def test_managed_build_refuses_tracked_files_and_symlink_destinations(self):
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as elsewhere:
            root = self.fake_checkout(d); outside = Path(elsewhere)
            (outside / 'keep.txt').write_text('keep')
            (root / 'dist').symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError): build_managed(root)
            self.assertEqual('keep', (outside / 'keep.txt').read_text())
            (root / 'dist').unlink(); target = root / 'dist/bootstrap/source.md'
            target.parent.mkdir(parents=True); target.write_text('tracked source')
            subprocess.run(['git', 'add', '-f', 'dist/bootstrap/source.md'], cwd=root, check=True)
            with self.assertRaises(ValueError): build_managed(root)
            self.assertEqual('tracked source', target.read_text())

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
        self.assertEqual(sorted(front.index('## ' + str(i) + '.') for i in range(4)), [front.index('## ' + str(i) + '.') for i in range(4)])
        self.assertIn("user's language", front)
        self.assertIn('GUIDE-ACCESS.md', front)
        self.assertIn('**STOP**', front)
        self.assertIn('locked version', front)
        self.assertIn('not a resumable', front)
        self.assertEqual('INITIALIZE.md', json.loads((ROOT / 'registry/guide-index.source.json').read_text())['bootstrap'])
