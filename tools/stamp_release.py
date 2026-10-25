#!/usr/bin/env python3
"""Stamp a substantive source commit; a later metadata commit avoids self-reference."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]

def command(*args):
    subprocess.run([sys.executable,*args],cwd=ROOT,check=True)

def stamp(source_commit,date):
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',date):raise ValueError('Use the approved release date YYYY-MM-DD.')
    commit=subprocess.check_output(['git','rev-parse','--verify',source_commit+'^{commit}'],cwd=ROOT,text=True).strip()
    metadata=json.loads((ROOT/'release.json').read_text());old=metadata['release'];short=commit[:7]
    release='0.2_'+date+'_'+short
    metadata.update(release=release,source_commit=commit,release_date=date,documentation_updated=date)
    (ROOT/'release.json').write_text(json.dumps(metadata,indent=2)+'\n')
    for relative in ('README.md','README(kor).md','guides/core/guide.md','guides/core/guide(kor).md','docs/external-connection-readiness.md','docs/external-connection-readiness(kor).md'):
        path=ROOT/relative;text=path.read_text().replace(old,release)
        if relative.startswith('README'):
            text=re.sub(r'\[`[0-9a-f]{7,40}`\]\(https://github.com/zomtoli7/greedyQ/commit/[0-9a-f]+\)',f'[`{short}`](https://github.com/zomtoli7/greedyQ/commit/{commit})',text)
        path.write_text(text)
    for relative in ('guides/greedyq-guide.md','guides/greedyq-guide(kor).md'):
        path=ROOT/relative;text=path.read_text()
        text=re.sub(r'(?m)^\*\*Guide version:\*\* `[^`]+`',f'**Guide version:** `{release}`',text)
        text=re.sub(r'(?m)^\*\*Compatible specification:\*\* `[^`]+`','**Compatible specification:** `greedyQ 0.2`',text)
        path.write_text(text)
    for base in ('templates','tests','examples'):
        for path in (ROOT/base).rglob('*'):
            if path.is_file() and path.suffix in ('.qmd','.html','.py'):
                text=path.read_text();new=text.replace(old,release)
                if new!=text:path.write_text(new)
    init=ROOT/'greedyq/__init__.py';text=init.read_text()
    text=re.sub(r'(?m)^__release__ = .*\n?','',text).rstrip()+f'\n__release__ = "{release}"\n';init.write_text(text)
    core=ROOT/'web/greedyq-core.js';text=core.read_text();text=re.sub(r'(?m)^  const RELEASE = .*\n','',text)
    text=text.replace('  const VERSION = "0.2.0-draft.1";',f'  const VERSION = "0.2.0-draft.1";\n  const RELEASE = "{release}";')
    if 'VERSION, RELEASE,' not in text:text=text.replace('VERSION, inlineMarkdown','VERSION, RELEASE, inlineMarkdown')
    core.write_text(text)
    source=ROOT/'registry/guide-index.source.json';data=json.loads(source.read_text());data['release']=release;source.write_text(json.dumps(data,indent=2)+'\n')
    notes={
        'en':['Complete standard Prolific ID capture, isolated repeat Preview, atomic withdrawal erasure, protected results/CSV and routine-review evidence handling.','Document verified draft Preview paths and the paid pilot awaiting Prolific review; payment remains unverified.','Add the standalone Collect → Connect to Prolific page, adjacent-page guidance and synchronized website version/history.','Consolidate earlier runtime, randomization, archive, localization and preregistration work into the v0.2 source.'],
        'ko':['기본 Prolific ID 기록·분리된 반복 Preview·원자적 철회 답변 삭제·보호된 결과/CSV·내부 검토 상태 처리를 정리했습니다.','검증된 초안 Preview와 Prolific 검토 대기 중인 유료 시험을 기록했으며 지급은 아직 미검증입니다.','Collect → Prolific 연결하기 독립 페이지·앞뒤 안내·웹사이트 버전/이력을 동기화했습니다.','기존 runtime·무작위화·아카이빙·다국어·사전등록 작업을 v0.2 소스에 함께 정리했습니다.']}
    for language,suffix,other in (('en','','(kor)'),('ko','(kor)','')):
        path=ROOT/f'updates/0.2/{release}{suffix}.md'
        opposite='한국어' if language=='en' else 'English'
        path.write_text(f'# {release}\n\n[{opposite}](./{release}{other}.md)\n\n'+'\n'.join('- '+line for line in notes[language])+'\n')
        index=ROOT/('updates/README.md' if language=='en' else 'updates/README(kor).md');text=index.read_text()
        link=f'- [`{release}`](./0.2/{release}{suffix}.md) — '+notes[language][0]+'\n'
        if f'[`{release}`]' not in text:text=text.replace('## 0.2\n','## 0.2\n\n'+link,1)
        previous='0.2_2026-09-10_c4a8405'
        if previous!=release and f'[`{previous}`]' not in text:
            oldlink=f'- [`{previous}`](./0.2/{previous}{suffix}.md) — '+('Responsive browser checks and native export stabilization.' if language=='en' else '반응형 브라우저 검사·native export 안정화.')+'\n'
            text=text.replace(link,link+oldlink,1)
        index.write_text(text)
    for study in ('complete-study','simple-satisfaction-study','control-gallery'):
        command('-m','greedyq','build','examples/'+study)
        command('-m','greedyq','export-surveydown','examples/'+study)
    command('tools/build_guide_registry.py')
    for study in ('complete-study','simple-satisfaction-study'):
        directory=ROOT/'examples'/study;descriptor=json.loads((directory/'greedyq.study.json').read_text())
        args=['tools/resolve_guide.py','--profile',descriptor['profile']]
        for module in descriptor['modules']:args+=['--module',module]
        command(*args,'--output',str(directory/'.greedyq/guide-lock.json'))
        manifest=directory/'.greedyq/generation-manifest.json';data=json.loads(manifest.read_text());data['guide_version']=release;data['source_commit']=commit
        for entry in data['artifacts']:
            file=directory/entry['path']
            if file.is_file():entry['sha256']=hashlib.sha256(file.read_bytes()).hexdigest()
        manifest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
        state=directory/'.greedyq/study-state.json';data=json.loads(state.read_text());data['guide_version']=release;state.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
        data=json.loads(manifest.read_text())
        for entry in data['artifacts']:
            file=directory/entry['path']
            if file.is_file():entry['sha256']=hashlib.sha256(file.read_bytes()).hexdigest()
        manifest.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    command('tools/sync_guide_bundle.py');command('tools/build_website_embed.py')
    print('Stamped '+release+' from '+commit)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--source-commit',required=True);parser.add_argument('--date',required=True);args=parser.parse_args();stamp(args.source_commit,args.date)
