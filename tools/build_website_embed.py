#!/usr/bin/env python3
"""Build the existing Google Sites embed without changing its renderer or gallery."""
import copy
from html import escape
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MARKER='__GREEDYQ_SITE_CONTENT__'

def build(root=ROOT,write=True):
    site=root/'website'
    data=copy.deepcopy(json.loads((site/'content.json').read_text()))
    overlay=json.loads((site/'prolific-content.json').read_text())
    release=json.loads((root/'release.json').read_text())
    for language,add in overlay.items():
        current=data[language]
        pages=current['guide'];pages[:]=[p for p in pages if p['id']!='prolific']
        index=next(i for i,p in enumerate(pages) if p['id']=='deploy')
        pages.insert(index+1,add['page'])
        for _,ids in current['guideGroups']:
            if 'prolific' in ids:ids.remove('prolific')
            if 'deploy' in ids:ids.insert(ids.index('deploy')+1,'prolific')
        for page_id in ('deploy','results'):
            page=next(p for p in pages if p['id']==page_id)
            page['body']=add[page_id]['body'];page['prompt']=add[page_id]['prompt']
        current['draft']=f"v{release['spec_version']} · {release['release']} · {release['documentation_updated']}"
        current['home']['note']=add['home_note']
        update=next(p for p in current['about'] if p['id']=='updates')
        old=update['body']
        translated={m.group(1):m.group(2) for m in re.finditer(r'<li><code>[^<]* · ([0-9a-f]+)</code><br>(.*?)</li>',old)}
        notes=[p for p in (root/'updates/0.2').glob('*.md') if '(kor)' not in p.name]
        notes.sort(key=lambda p:p.stem,reverse=True)
        notes.sort(key=lambda p:p.stem!=release['release'])
        items=[]
        for note in notes:
            localized=note.with_name(note.stem+'(kor).md') if language=='ko' else note
            if not localized.exists():localized=note
            summary=next((line[2:] for line in localized.read_text().splitlines() if line.startswith('- ')),'')
            if note.stem==release['release']:summary=add['update_summary']
            elif language=='zh':summary=translated.get(note.stem.rsplit('_',1)[-1],summary)
            link='https://github.com/zomtoli7/greedyQ/blob/main/updates/0.2/'+localized.name
            items.append(f'<li><a href="{escape(link,quote=True)}" target="_blank" rel="noopener"><code>{escape(note.stem)}</code></a><br>{escape(summary)}</li>')
        history='<ul class="history">'+''.join(items)+'</ul>'
        update['body']=add['version_intro'].replace('{release}',escape(release['release'])).replace('{date}',release['documentation_updated'])+history+add['history_footer']
    # The public entry routes the host; operational rules live in INITIALIZE.md.
    start_prefix = {
        'en': 'Read and follow the greedyQ start page. If you cannot read it, stop and tell me:\n<https://greedyq.netlify.app/>',
        'ko': '아래 greedyQ 시작 안내를 읽고 따라줘. 읽을 수 없으면 멈추고 알려줘:\n<https://greedyq.netlify.app/>',
        'zh': '请读取并遵循 greedyQ 开始说明。无法读取就停止并告诉我：\n<https://greedyq.netlify.app/>',
    }
    for language in ('en', 'ko', 'zh'):
        current=data[language]; prefix=start_prefix[language]
        if not overlay[language].get('home_note_includes_policy', False):
            current['home']['note']=current['start']['lead']+' '+current['home']['note']
        for page in current['guide']:
            if page.get('prompt') and not page['prompt'].startswith(prefix):
                page['prompt']=prefix+'\n\n'+page['prompt']
    template=(site/'google-sites-template.html').read_text()
    template=template.replace('</style>','.article p button[data-page]{border:0;background:none;padding:0;color:var(--accent);font:inherit;text-decoration:underline;text-underline-offset:3px}</style>',1)
    template=template.replace("readHash();render();});render();", "readHash();render();window.scrollTo(0,0);});render();")
    if template.count(MARKER)!=1:raise ValueError('Exactly one website content marker is required.')
    content=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
    result=template.replace(MARKER,content)
    if write:(site/'google-sites-embed.html').write_text(result)
    return result,data

if __name__=='__main__':
    build();print('Built website/google-sites-embed.html; Google Sites editor save/publication is a separate step.')
