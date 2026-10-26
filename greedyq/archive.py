"""Private, lossless study-data archive. No cloud mutations or credentials."""
import csv
import hashlib
import io
import json
from pathlib import Path
import zipfile

TABLES = ('sessions', 'answers', 'assignments', 'external_identifiers',
          'consent_events', 'lifecycle_events', 'data_requests')


def encode(value):
    return json.dumps(value, ensure_ascii=False, indent=2).encode('utf-8')


def make_archive(snapshot, model, destination):
    """Snapshot must come from one DB transaction, not the paginated dashboard API."""
    if set(snapshot['tables']) != set(TABLES):
        raise ValueError('All seven data tables are required')
    if not snapshot.get('collection_closed') or snapshot['study_id'] != model['study_id']:
        raise ValueError('A closed, matching study is required')
    tables = json.loads(json.dumps(snapshot['tables']))
    sessions = tables['sessions']
    if any(type(s.get('is_test')) is not bool for s in sessions):
        raise ValueError('Explicit boolean test classification required')
    ids = {s['id'] for s in sessions}
    if len(ids) != len(sessions) or any(s['study_id'] != model['study_id'] for s in sessions):
        raise ValueError('Duplicate or mixed-study sessions')
    if any(row['session_id'] not in ids for t in TABLES[1:] for row in tables[t]):
        raise ValueError('Orphan or cross-study record')
    for session in sessions:
        for field in ('access_token_hash', 'browser_state'):
            session.pop(field, None)
    questions = [q for page in model['pages'] for q in page.get('questions', [])]
    question_ids = [q['id'] for q in questions if q['type'] not in ('audio', 'video')]
    # Preserve historical/unknown answer IDs as well as all currently unanswered questions.
    question_ids = list(dict.fromkeys(question_ids + [a['question_id'] for a in tables['answers']]))
    answers = {(a['session_id'], a['question_id']): a['value'] for a in tables['answers']}
    metadata = ['session_id', 'study_id', 'study_version', 'greedyq_version', 'started_at',
                'completed_at', 'status', 'source', 'is_test', 'current_page', 'assignments', 'question_orders', 'option_orders', 'page_order']
    assignments = {}
    for item in tables['assignments']:
        assignments.setdefault(item['session_id'], {})[item['randomization_id']] = item['condition']
    # Prefix question columns to prevent collisions with session metadata.
    header = ['PROLIFIC_PID','STUDY_ID','SESSION_ID'] + metadata + ['answer.' + q for q in question_ids]
    external={item['session_id']:item for item in tables['external_identifiers'] if item.get('provider')=='prolific'}
    def cell(value):
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False, separators=(',', ':'))
        value = '' if value is None else str(value)
        # Neutralize spreadsheet formula execution; raw JSON retains the exact value.
        return "'" + value if value.lstrip().startswith(('=', '+', '-', '@', '\t', '\r')) else value
    def csv_file(test):
        stream = io.StringIO(newline='')
        writer = csv.writer(stream)
        writer.writerow(header)
        for s in sessions:
            if s['is_test'] is not test:
                continue
            p=external.get(s['id'],{})
            writer.writerow([cell(v) for v in [p.get('participant_id'),p.get('external_study_id'),p.get('external_session_id'),s['id'], s['study_id'], s.get('study_version'),
                s.get('greedyq_version'), s['created_at'], s.get('terminal_at'), s['lifecycle_state'],
                s['respondent_source'], s['is_test'], s.get('current_page'), assignments.get(s['id'], {}),
                s.get('question_orders', {}), s.get('option_orders', {}), s.get('page_order', []),
                *[answers.get((s['id'], q)) for q in question_ids]]])
        return ('\ufeff' + stream.getvalue()).encode('utf-8')
    files = {'responses.csv': csv_file(False), 'test-responses.csv': csv_file(True),
             'study-model.json': encode(model), 'data.json': encode(tables),
             'variables.json': encode({'columns': header, 'questions': questions,
                 'structured_answers': 'Lossless JSON in CSV cells; exact values in data.json',
                 'spreadsheet_safety': 'Potential formulas are prefixed with an apostrophe in CSV only'})}
    if model.get('kind')=='cbc_study':
        from .cbc import stored_rows
        cbc_rows=stored_rows(tables)
        attributes=['attribute.'+a['id'] for a in model['cbc']['attributes']]
        columns=['session_id','study_id','study_version','started_at','completed_at','status','source','is_test','block_id','task_id','task_position','alternative_id','display_position','is_none','chosen',*attributes,'design_version','design_sha256','presentation_state','served_at','presented_at','answered_at']
        for test,name in [(False,'cbc-choices.csv'),(True,'cbc-test-choices.csv')]:
            stream=io.StringIO(newline='');writer=csv.writer(stream);writer.writerow(columns)
            for row in cbc_rows:
                if row['is_test'] is test:writer.writerow([cell(str(row[k]).lower() if isinstance(row.get(k),bool) else row.get(k)) for k in columns])
            files[name]=('\ufeff'+stream.getvalue()).encode('utf-8')
    manifest = {'format': 'greedyq-data-archive/1', 'study_id': model['study_id'],
                'collection_closed': True, 'created_at': snapshot['created_at'],
                'other_studies': snapshot.get('other_studies', []),
                'targets': snapshot.get('targets'),
                'unresolved_data_requests': sum(r.get('status') in ('recorded', 'reviewing') for r in tables['data_requests']),
                'counts': {t: len(tables[t]) for t in TABLES},
                'files': {name: hashlib.sha256(data).hexdigest() for name, data in files.items()},
                'limitations': ['Not a database restore image', 'No credentials or browser capabilities',
                                'No uploaded media or Storage objects', 'Contains private participant records']}
    files['manifest.json'] = encode(manifest)
    destination = Path(destination)
    import os
    with os.fdopen(os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600), 'wb') as output:
        with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
            for name, data in files.items():
                archive.writestr(name, data)
    destination.chmod(0o600)
    verify_archive(destination)
    return manifest


def verify_archive(path):
    with zipfile.ZipFile(path) as archive:
        if archive.testzip() is not None:
            raise ValueError('Corrupt archive')
        manifest = json.loads(archive.read('manifest.json'))
        if len(set(archive.namelist())) != len(archive.namelist()):
            raise ValueError('Duplicate archive entries')
        if set(archive.namelist()) != set(manifest['files']) | {'manifest.json'}:
            raise ValueError('Unexpected archive entries')
        for name, digest in manifest['files'].items():
            if hashlib.sha256(archive.read(name)).hexdigest() != digest:
                raise ValueError('Archive checksum mismatch')
        return manifest


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('snapshot')
    parser.add_argument('model')
    parser.add_argument('destination')
    args = parser.parse_args()
    make_archive(json.loads(Path(args.snapshot).read_text()),
                 json.loads(Path(args.model).read_text()), args.destination)
    print('Archive created and verified; cloud resources remain unchanged.')
