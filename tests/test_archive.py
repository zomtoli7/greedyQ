import copy
import csv
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from greedyq.archive import TABLES, make_archive, verify_archive


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.model = {'study_id': 'sample', 'pages': [{'questions': [
            {'id': 'comment', 'type': 'text'}, {'id': 'missing', 'type': 'numeric'},
            {'id': 'grid', 'type': 'matrix'}, {'id': 'clip', 'type': 'video'}]}]}
        self.snapshot = {'study_id': 'sample', 'collection_closed': True,
                         'created_at': '2026-09-10', 'tables': {t: [] for t in TABLES}}
        for i in range(2):
            self.snapshot['tables']['sessions'].append({'id': str(i), 'study_id': 'sample',
                'created_at': '2026-09-10', 'is_test': bool(i), 'lifecycle_state': 'completed',
                'respondent_source': 'direct', 'access_token_hash': 'SECRET', 'browser_state': {'secret': 'SECRET'}})
        self.snapshot['tables']['answers'] = [
            {'session_id': '0', 'question_id': 'comment', 'value': '=BAD(),\n한국어 "quote"'},
            {'session_id': '0', 'question_id': 'grid', 'value': {'a': ['x', 'y']}},
            {'session_id': '1', 'question_id': 'old_question', 'value': 9}]

    def build(self, tmp):
        path = Path(tmp) / 'archive.zip'
        make_archive(self.snapshot, self.model, path)
        return path

    def test_roundtrip_counts_and_secrets(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.build(tmp)
            self.assertEqual(2, verify_archive(path)['counts']['sessions'])
            with zipfile.ZipFile(path) as z:
                self.assertNotIn(b'SECRET', z.read('data.json'))
                self.assertEqual(self.snapshot['tables']['answers'], json.loads(z.read('data.json'))['answers'])
            self.assertEqual(0o600, path.stat().st_mode & 0o777)

    def test_csv_unicode_formulas_structure_and_unanswered(self):
        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(self.build(tmp)) as z:
                rows = list(csv.DictReader(io.StringIO(z.read('responses.csv').decode('utf-8-sig'))))
                self.assertEqual(1, len(rows))
                self.assertTrue(rows[0]['answer.comment'].startswith("'=BAD"))
                self.assertEqual('', rows[0]['answer.missing'])
                self.assertEqual({'a': ['x', 'y']}, json.loads(rows[0]['answer.grid']))
                tests = list(csv.DictReader(io.StringIO(z.read('test-responses.csv').decode('utf-8-sig'))))
                self.assertEqual('9', tests[0]['answer.old_question'])

    def test_empty_study_keeps_headers(self):
        self.snapshot['tables'] = {t: [] for t in TABLES}
        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(self.build(tmp)) as z:
                self.assertIn(b'answer.missing', z.read('responses.csv'))

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.build(tmp)
            with self.assertRaises(FileExistsError): self.build(tmp)

    def test_invalid_snapshots(self):
        for mutation in ['open', 'mismatch', 'missing', 'orphan', 'duplicate']:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                original = copy.deepcopy(self.snapshot)
                if mutation == 'open': self.snapshot['collection_closed'] = False
                if mutation == 'mismatch': self.snapshot['study_id'] = 'other'
                if mutation == 'missing': del self.snapshot['tables']['assignments']
                if mutation == 'orphan': self.snapshot['tables']['answers'][0]['session_id'] = 'other'
                if mutation == 'duplicate': self.snapshot['tables']['sessions'].append(self.snapshot['tables']['sessions'][0])
                with self.assertRaises(ValueError): self.build(tmp)
                self.snapshot = original

    def test_corruption_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = self.build(tmp)
            target = Path(tmp) / 'bad.zip'
            with zipfile.ZipFile(source) as old, zipfile.ZipFile(target, 'w') as new:
                for name in old.namelist(): new.writestr(name, b'changed' if name == 'responses.csv' else old.read(name))
            with self.assertRaises(ValueError): verify_archive(target)
