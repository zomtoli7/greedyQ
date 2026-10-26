"""Check the v0.3 draft fixture only; not a production CBC importer/runtime."""
import csv
import hashlib
import io
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = ROOT / 'drafts/v0.3/cbc/golden-reference'


def table(text):
    reader = csv.reader(io.StringIO(text.lstrip('\ufeff')))
    rows = list(reader)
    if not rows or not rows[0] or len(set(rows[0])) != len(rows[0]):
        raise ValueError('Missing or duplicate headers')
    header = rows[0]
    data = []
    for values in rows[1:]:
        if not any(values):
            continue
        if len(values) != len(header) or any(value == '' for value in values):
            raise ValueError('Partial or malformed row')
        data.append(dict(zip(header, values)))
    return header, data


def validate_design(attributes_text, design_text, alternatives=2, tasks_per_block=4):
    header, attributes = table(attributes_text)
    if header != ['attribute_id', 'attribute_label', 'level_id', 'level_label']:
        raise ValueError('Attribute headers differ from draft contract')
    design_header, rows = table(design_text)
    if not attributes or not rows:
        raise ValueError('Blank template: awaiting input, not a runnable design')
    levels, labels = {}, {}
    for row in attributes:
        aid = row['attribute_id']
        if aid in labels and labels[aid] != row['attribute_label']:
            raise ValueError('Conflicting attribute labels')
        labels[aid] = row['attribute_label']
        level_set = levels.setdefault(aid, set())
        if row['level_id'] in level_set:
            raise ValueError('Duplicate level ID')
        level_set.add(row['level_id'])
    if len(levels) < 2 or any(len(values) < 2 for values in levels.values()):
        raise ValueError('At least two attributes with two levels are required for this fixture')
    if design_header != ['block_id', 'task_id', 'alternative_id', *levels]:
        raise ValueError('Design attribute columns need confirmed mapping')
    tasks, blocks, keys = {}, {}, set()
    for row in rows:
        key = tuple(row[k] for k in ('block_id', 'task_id', 'alternative_id'))
        if key in keys:
            raise ValueError('Duplicate alternative key')
        if row['alternative_id'] == 'none':
            raise ValueError('None is configured separately, not a design profile')
        keys.add(key)
        for aid, allowed in levels.items():
            if row[aid] not in allowed:
                raise ValueError('Unknown level code for ' + aid)
        tasks.setdefault(key[:2], []).append(row)
        blocks.setdefault(key[0], set()).add(key[1])
    for profiles in tasks.values():
        if len(profiles) != alternatives:
            raise ValueError('Wrong number of alternatives')
        if len({tuple(row[aid] for aid in levels) for row in profiles}) != len(profiles):
            raise ValueError('Identical profiles in one task')
    if any(len(ids) != tasks_per_block for ids in blocks.values()):
        raise ValueError('Wrong task count in a block')
    return {'attributes': len(levels), 'blocks': len(blocks), 'tasks': len(tasks), 'profiles': len(rows)}


def check_reference(directory=REFERENCE):
    config = json.loads((directory / 'study.design.json').read_text())
    assert config['status'] == 'design_only' and not config['fielding_approval']
    result = validate_design((directory / config['attributes_source']).read_text(),
                             (directory / config['design_source']).read_text(),
                             config['alternatives_per_task'], config['tasks_per_block'])
    manifest = json.loads((directory / 'design.manifest.json').read_text())
    for entry in manifest['files']:
        assert hashlib.sha256((directory / entry['path']).read_bytes()).hexdigest() == entry['sha256']
    attributes = list(csv.DictReader(io.StringIO((directory / config['attributes_source']).read_text())))
    profiles = list(csv.DictReader(io.StringIO((directory / config['design_source']).read_text())))
    normalized = json.dumps({'attributes': attributes, 'profiles': profiles}, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    assert hashlib.sha256(normalized.encode()).hexdigest() == manifest['normalized_design_sha256']
    with (directory / 'expected/choice-data-long.csv').open(newline='') as file:
        exported = list(csv.DictReader(file))
    with (directory / config['design_source']).open(newline='') as file:
        design = {(row['block_id'], row['task_id'], row['alternative_id']): row for row in csv.DictReader(file)}
    groups = {}
    for row in exported:
        assert row['design_sha256'] == manifest['normalized_design_sha256']
        assert row['design_version'] == config['schema_version'] and row['presentation_state'] == 'answered'
        groups.setdefault((row['respondent_id'], row['block_id'], row['task_id']), []).append(row)
        if row['is_none'] == 'true':
            assert row['alternative_id'] == 'none' and all(not row[aid] for aid in config['attribute_ids'])
        else:
            source = design[(row['block_id'], row['task_id'], row['alternative_id'])]
            assert all(row[aid] == source[aid] for aid in config['attribute_ids'])
    for rows in groups.values():
        assert len(rows) == config['alternatives_per_task'] + 1
        assert sum(int(row['chosen']) for row in rows) == 1
        assert sorted(int(row['display_position']) for row in rows) == [1, 2, 3]
    return {**result, 'synthetic_export_rows': len(exported), 'status': 'draft_fixture_passed',
            'cbc_cloud_verified': False, 'cbc_collection_implemented': True, 'local_preview_available': True, 'statistical_efficiency_established': False}


if __name__ == '__main__':
    print(json.dumps(check_reference(Path(sys.argv[1]) if len(sys.argv) > 1 else REFERENCE), indent=2))
