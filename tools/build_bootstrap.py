#!/usr/bin/env python3
"""Render canonical START-HERE Markdown as a public script-free static site."""
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://github.com/zomtoli7/greedyQ/blob/'
LANGUAGES = (('', 'en'), ('(kor)', 'ko'), ('(zh-CN)', 'zh-CN'))


def inline(text):
    text = html.escape(text)
    text = re.sub(r'\[([^\]]+)\]\(([^\s]*?\.(?:md|html)|https?://[^\s]+?|mailto:[^\s]+?)\)',
                  lambda m: '<a href="' + m[2] + '">' + m[1] + '</a>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    return re.sub(r'`([^`]+)`', r'<code>\1</code>', text)


def render(markdown, language):
    markdown = re.sub(r'<!--.*?-->', '', markdown, flags=re.S)
    blocks = []
    for block in re.split(r'\n\s*\n', markdown.strip()):
        heading = re.fullmatch(r'(#{1,3}) (.+)', block)
        if heading:
            tag = 'h' + str(len(heading[1]))
            blocks.append('<' + tag + '>' + inline(heading[2]) + '</' + tag + '>')
        else:
            blocks.append('<p>' + inline(block.replace('\n', ' ')) + '</p>')
    return ('<!doctype html><html lang="' + language + '"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>greedyQ - Start here</title><style>body{max-width:760px;margin:32px auto;padding:0 20px;'
            'font:18px/1.65 system-ui,sans-serif;color:#172033;background:#fff}a{color:#14577a}'
            'p,code{overflow-wrap:anywhere}h1,h2{line-height:1.3}h2{margin-top:32px}</style>'
            '</head><body><main>' + '\n'.join(blocks) + '</main></body></html>\n')


def build(output, root=ROOT):
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    commit = os.environ.get('COMMIT_REF') or head
    if not re.fullmatch(r'[0-9a-f]{40}', commit) or commit != head:
        raise ValueError('COMMIT_REF must match the exact checked-out Git commit.')
    for name in ('INITIALIZE.md', 'START-HERE.md'):
        subprocess.run(['git', 'cat-file', '-e', commit + ':' + name], cwd=root,
                       check=True, capture_output=True)
    release = json.loads((root / 'release.json').read_text())
    policy = json.loads((root / 'schemas/authoring-support-policy.json').read_text())
    if policy['researcher_authoring']['official_host_families'] != ['chatgpt_desktop', 'claude_desktop']:
        raise ValueError('Review the public start page before changing supported hosts.')
    output = Path(output)
    if output.resolve() in (root.resolve(), (root / '.greedyq').resolve()):
        raise ValueError('Use a separate publish folder.')
    if output.exists() and any(output.iterdir()):
        old = output / 'bootstrap-manifest.json'
        if not old.is_file():
            raise ValueError('Refuse a nonempty folder without a bootstrap manifest.')
        previous = json.loads(old.read_text())
        if {p.name for p in output.iterdir()} != set(previous['files']) | {'bootstrap-manifest.json'}:
            raise ValueError('Refuse an output folder containing unrelated files.')
    files = {}
    for suffix, language in LANGUAGES:
        name = 'START-HERE' + suffix
        markdown = (root / (name + '.md')).read_text(encoding='utf-8')
        markdown = re.sub(r'\]\(\./([^\n]*?\.md)\)',
                          lambda m: '](' + ('./' + m[1].replace('.md', '.html') if m[1].startswith('START-HERE') else BASE + commit + '/' + m[1]) + ')', markdown)
        files[name + '.md'] = markdown
        files[name + '.html'] = render(markdown, language)
    files['index.html'] = files['START-HERE.html']
    files['START-HERE.txt'] = files['START-HERE.md']
    files['robots.txt'] = 'User-agent: *\nAllow: /\n'
    files['authoring-support-policy.json'] = json.dumps(policy, ensure_ascii=False, indent=2) + '\n'
    output.mkdir(parents=True, exist_ok=True)
    for name, value in files.items():
        (output / name).write_text(value, encoding='utf-8')
    manifest = {'format': 'greedyq-bootstrap-1', 'release': release['release'],
                'repository_snapshot': commit, 'initialization_url': BASE + commit + '/INITIALIZE.md',
                'files': {name: hashlib.sha256(value.encode()).hexdigest() for name, value in files.items()},
                'requires_browser_javascript': False, 'live_deployment_verified': False}
    (output / 'bootstrap-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'dist/bootstrap')
    args = parser.parse_args()
    result = build(args.output)
    print('Prepared static start page for ' + result['release'] + '; deployment not verified.')
