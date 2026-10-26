"""Linear ordinary-question pages around one CBC sequence; no executable survey code."""
import copy
import re
from pathlib import Path

TYPES = {'text','textarea','numeric','mc','mc_buttons','mc_image','mc_multiple','mc_multiple_buttons','mc_multiple_image','select','slider','slider_numeric','date','daterange','matrix','matrix_multiple','audio','video','timing','nps','rank_order','constant_sum','side_by_side','pick_group_rank','drill_down','custom'}

def normalize_flow(flow):
    from .cbc import fail
    if not isinstance(flow,dict) or set(flow)!={'before','after'}: fail('CBC030','Provide before/after question-page lists.')
    ids=set();questions=set();result=copy.deepcopy(flow)
    for phase,pages in result.items():
        if not isinstance(pages,list) or len(pages)>50:fail('CBC030','Use at most 50 ordinary pages per stage.')
        for p in pages:
            if not isinstance(p,dict) or set(p)-{'id','title','body','questions','show_previous','previous_mode','next_mode','next_delay_seconds','next_label','checks','messages'}:fail('CBC030','Mixed CBC pages are linear; branching, checks and page shuffling require separate support.')
            if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]{0,79}',str(p.get('id',''))) or p['id'] in ids or p['id'] in {'consent','completed','withdrawn','consent_refused','cbc_tasks'}:fail('CBC030','Use distinct ordinary page IDs.')
            ids.add(p['id'])
            if not isinstance(p.get('title',''),str) or not isinstance(p.get('body',''),str) or not isinstance(p.get('questions'),list):fail('CBC030','Provide page title, body and questions.')
            for q in p['questions']:
                if not isinstance(q,dict) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,79}',str(q.get('id',''))) or q['id'] in questions or q.get('type') not in TYPES or not isinstance(q.get('label'),str):fail('CBC030','Use supported, distinct ordinary questions; CBC tasks stay separate.')
                questions.add(q['id'])
                if q.get('shuffle_items'):fail('CBC030','Ordinary option shuffling requires durable module presentation support; do not silently reshuffle it on resume.')
                if q['type']=='custom' and q.get('base_type') not in TYPES-{'custom'}:fail('CBC030','Custom questions must use a supported base control.')
                if type(q.get('required',False)) is not bool:fail('CBC030','Required must be true or false.')
    return result

def import_questions(path):
    """Use the fixed QMD parser/compiler; cbc_tasks is a single sequence marker."""
    from .parser import parse_qmd
    from .compiler import compile_preview
    from .cbc import fail
    parsed=parse_qmd(Path(path))
    from .yaml_min import loads
    config_path=Path(path).parent/'greedyq.yml'
    config=loads(config_path.read_text()) if config_path.is_file() else {'study':{'id':'cbc_flow','title':'CBC questions'},'respondents':{'source':'direct_link','mode':'test'}}
    if config.get('randomization') or config.get('logic',{}).get('skip') or parsed['front_matter'].get('survey-settings',{}).get('shuffle-pages'):fail('CBC030','The first CBC module contract is linear; do not discard page branches or a separate experimental assignment.')
    compiled=compile_preview(parsed,config);pages=compiled['pages']
    for p in pages:p['messages']=compiled['messages']
    for index,p in enumerate(parsed['pages']):
        next_page=p.get('nav',{}).get('next_page') or p.get('nav',{}).get('next')
        if next_page and next_page!=(parsed['pages'][index+1]['id'] if index+1<len(parsed['pages']) else None):fail('CBC030','Keep ordinary pages linear around this CBC module.')
    for p in parsed['pages']:
        if any(q.get('unsupported_arguments') for q in p['questions']):fail('CBC030','Remove unsupported ordinary-question arguments before adding CBC.')
    markers=[i for i,p in enumerate(parsed['pages']) if p.get('cbc_module') or p['id']=='cbc_tasks']
    if len(markers)!=1 or pages[markers[0]]['questions']:fail('CBC030','Add exactly one empty --- cbc_tasks marker page.')
    marker=parsed['pages'][markers[0]]
    if marker.get('cbc_module'):
        design=Path(path).parent/marker['cbc_module']['design']
        if design.resolve()!= (Path(path).parent/'study.design.json').resolve():fail('CBC030','The CBC module must reference this study design: study.design.json.')
    def clean(p):return {k:v for k,v in p.items() if k not in {'next','terminal'}}
    i=markers[0]
    return normalize_flow({'before':[clean(p) for p in pages[:i]],'after':[clean(p) for p in pages[i+1:] if not p.get('terminal')]})


def build_module_preview(model,destination):
    import json
    root=Path(__file__).resolve().parents[1]
    html=(root/'templates/browser/cbc-module-preview.html').read_text()
    libraries='\n'.join((root/'web'/n).read_text() for n in ['greedyq-core.js','greedyq-cbc.js','greedyq-cbc-collection.js','greedyq-cbc-preview-session.js'])
    styles='\n'.join((root/'web'/n).read_text() for n in ['greedyq-runtime.css','greedyq-cbc.css'])
    html=html.replace('__STYLES__',styles).replace('__LIBRARIES__',libraries.replace('</script','<\\/script')).replace('__MODEL__',json.dumps(model,ensure_ascii=False).replace('<','\\u003c'))
    Path(destination).write_text(html)
    return Path(destination)


def build_module_study(folder,write=True):
    """Normal survey build dispatches the module without replacing ordinary source pages."""
    import json
    import tempfile
    import shutil
    from .cbc import build_collection
    root=Path(folder)
    settings=root/'collection.json'
    if (root/'authoring.json').is_file():
        from .cbc_authoring import inspect
        if inspect(root)['upgrade_available']:raise ValueError('This authoring package is pinned to another greedyQ version. Keep that snapshot or approve an upgrade into a separate copy.')
    if not settings.is_file():
        return {'status':'failed','summary':'The CBC module needs its reviewed design and collection.json before a complete preview can be built.','issues':[]},None
    with tempfile.TemporaryDirectory(prefix='greedyq-module-build-') as tmp:
        package,model=build_collection(root,settings,Path(tmp)/'package')
        if write:
            for name in ['preview.html','index.html','results.html','greedyq-core.js','greedyq-runtime.css','greedyq-cbc.js','greedyq-cbc.css','greedyq-cbc-collection.js']:
                (root/name).write_bytes((package/name).read_bytes())
            # This source folder is not a participant publication folder.
            runtime=root/'cbc-package'
            if runtime.exists():
                backup=root/'.greedyq'/'previous-builds';backup.mkdir(parents=True,exist_ok=True)
                runtime.rename(backup/('cbc-package-'+__import__('uuid').uuid4().hex))
            shutil.copytree(package,runtime)
            internal=root/'.greedyq';internal.mkdir(exist_ok=True)
            (internal/'normalized-survey.json').write_text(json.dumps(model,ensure_ascii=False,indent=2)+'\n')
    return {'status':'passed','summary':'Ordinary pages and the CBC module passed validation; open preview.html.','issues':[]},model
