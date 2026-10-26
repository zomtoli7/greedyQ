"""Researcher-owned CBC module authoring, handoff and explicit version migration."""
import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import stat
import zipfile

ROUTES={'ai','blank_table','existing_design'}
SOURCE_NAMES={'survey.qmd','greedyq.yml','study.design.json','collection.json','authoring.json','study-plan.md','study-plan(kor).md','consent.md','consent(kor).md','greedyq.study.json'}
PRIVATE_NAMES={'guide-lock.json','study-state.json','decision-log.json','unresolved-decisions.json','generation-manifest.json','validation-report.json'}

def release():
    from . import __release__
    p=Path(__file__).resolve().parents[1]/'release.json'
    return json.loads(p.read_text()).get('next_line',{}).get('release',__release__)

def write(path,data):Path(path).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def stamp_version(path):
    """Update only the greedyQ provenance of an explicitly created/upgraded source."""
    path=Path(path);text=path.read_text();parts=text.split('---',2)
    if len(parts)!=3 or parts[0].strip():raise ValueError('QMD front matter is required for version provenance.')
    header=parts[1]
    block=re.search(r'(?m)^greedyq:\s*\n(?:[ \t]+[^\n]*\n|\n)*',header)
    if block:
        value=block[0]
        line='  version: "'+release()+'"\n'
        value=re.sub(r'(?m)^  version:.*\n',lambda _:line,value) if re.search(r'(?m)^  version:',value) else value.replace('greedyq:\n','greedyq:\n'+line,1)
        header=header[:block.start()]+value+header[block.end():]
    else:header+='greedyq:\n  version: "'+release()+'"\n'
    path.write_text('---'+header+'---'+parts[2])

def record_lock(root):
    from tools.resolve_guide import resolve
    root=Path(root);descriptor=root/'greedyq.study.json'
    d=json.loads(descriptor.read_text()) if descriptor.is_file() else {'profile':'simple','modules':[]}
    lock=resolve(d.get('profile','simple'),list(set(d.get('modules',[]))|{'cbc'}))
    private=root/'.greedyq';private.mkdir(exist_ok=True);write(private/'guide-lock.json',lock)
    if descriptor.is_file():d['modules']=lock['modules'];write(descriptor,d)
    return lock

def inspect(folder):
    root=Path(folder);s=json.loads((root/'authoring.json').read_text())
    required=['survey.qmd','authoring.json']
    missing=[n for n in required if not (root/n).is_file()]
    return {'study_id':s['study_id'],'route':s.get('route'),'phase':s['phase'],'pinned_version':s['greedyq_version'],'current_version':release(),'upgrade_available':s['greedyq_version']!=release(),'missing_files':missing,'next_question':s['next_question'],'approval_required_for_upgrade':True}

def initialize(folder,study_id,route=None,language='en'):
    if route is not None and route not in ROUTES:raise ValueError('Choose AI collaboration, blank table or existing design.')
    if not re.fullmatch(r'[a-z][a-z0-9_]{1,63}',study_id):raise ValueError('Use a distinct study ID.')
    root=Path(folder)
    if root.exists():raise FileExistsError('Choose a new folder.')
    root.mkdir(parents=True)
    text='What would you like to ask first? You can ask to insert a CBC module at any point.'
    (root/'survey.qmd').write_text('---\ntitle: "Research draft"\ngreedyq:\n  language: '+language+'\n---\n\n--- welcome\n# Welcome\n\n--- complete\n# Thank you\n')
    stamp_version(root/'survey.qmd')
    write(root/'authoring.json',{'format':'greedyq-module-authoring/1','study_id':study_id,'greedyq_version':release(),'route':route,'phase':'questions' if route else 'cbc_route','decisions':[],'approvals':{},'next_question':text if route else 'Would you like AI help with the CBC design, a blank design table, or to import your existing design?','expected_files':[]})
    record_lock(root)
    return root

def set_route(folder,route):
    if route not in ROUTES:raise ValueError('Unknown design route.')
    root=Path(folder);s=json.loads((root/'authoring.json').read_text());s.update(route=route,phase='attributes',next_question='Which attributes and levels do you want to compare?');s['decisions'].append({'topic':'cbc_design_route','confirmed_value':route});write(root/'authoring.json',s)

def insert(folder,before_page,module_id='choice_tasks'):
    from .parser import parse_qmd
    root=Path(folder);path=root/'survey.qmd';parsed=parse_qmd(path)
    if any(p.get('cbc_module') for p in parsed['pages']):raise ValueError('One CBC module sequence is supported per study; preserve existing module.')
    if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]{0,79}',module_id) or any(p['id']==module_id for p in parsed['pages']):raise ValueError('Use a new module page ID.')
    if before_page not in [p['id'] for p in parsed['pages']]:raise ValueError('Select an existing insertion page.')
    body='--- '+module_id+'\n# Choice tasks\n\n```{r}\nsd_cbc(name = "'+module_id+'", design = "study.design.json")\n```\n\n'
    text=path.read_text();text=re.sub(r'^--- '+re.escape(before_page)+r'\s*$',lambda m:body+m[0],text,count=1,flags=re.M);path.write_text(text)
    state=root/'authoring.json'
    if state.is_file():s=json.loads(state.read_text())
    else:
        from .yaml_min import loads
        descriptor=root/'greedyq.study.json';config=root/'greedyq.yml'
        sid=json.loads(descriptor.read_text())['study_id'] if descriptor.is_file() else loads(config.read_text())['study']['id']
        s={'format':'greedyq-module-authoring/1','study_id':sid,'greedyq_version':release(),'route':None,'decisions':[],'approvals':{}}
    s.update(phase='attributes' if s.get('route') else 'cbc_route',module_id=module_id,next_question='Which CBC attributes and levels have you confirmed?' if s.get('route') else 'Would you like AI design help, a blank CSV/XLSX table, or to import an existing design?');s['approvals']={};write(state,s)
    record_lock(root)

def blank_tables(folder,attributes):
    root=Path(folder);dest=root/'design'
    if (dest/'attributes.csv').exists() or (dest/'design.csv').exists():raise FileExistsError('Keep existing design tables; choose a new draft before replacing them.')
    if not isinstance(attributes,list) or not attributes or len(attributes)>20 or any(not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,79}',a) for a in attributes) or len(set(attributes))!=len(attributes):raise ValueError('Provide distinct confirmed attribute IDs.')
    dest.mkdir(exist_ok=True)
    for name,header in [('attributes.csv',['attribute_id','attribute_label','level_id','level_label']),('design.csv',['block_id','task_id','alternative_id',*attributes])]:
        with (dest/name).open('w',newline='') as f:csv.writer(f).writerow(header)
    # A dependency-free, editable workbook with the same confirmed headings.
    from xml.sax.saxutils import escape
    headers=[['attribute_id','attribute_label','level_id','level_label'],['block_id','task_id','alternative_id',*attributes]]
    with zipfile.ZipFile(dest/'design-template.xlsx','w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'+''.join('<Override PartName="/xl/worksheets/sheet'+str(i)+'.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in [1,2])+'</Types>')
        z.writestr('_rels/.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        z.writestr('xl/workbook.xml','<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Attributes" sheetId="1" r:id="rId1"/><sheet name="Design" sheetId="2" r:id="rId2"/></sheets></workbook>')
        z.writestr('xl/_rels/workbook.xml.rels','<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+''.join('<Relationship Id="rId'+str(i)+'" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet'+str(i)+'.xml"/>' for i in [1,2])+'</Relationships>')
        for i,header in enumerate(headers,1):
            cells=''.join('<c r="'+chr(65+j)+'1" t="inlineStr"><is><t>'+escape(value)+'</t></is></c>' for j,value in enumerate(header))
            z.writestr('xl/worksheets/sheet'+str(i)+'.xml','<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData><row r="1">'+cells+'</row></sheetData></worksheet>')
    s=json.loads((root/'authoring.json').read_text());s.update(phase='awaiting_design_table',expected_files=['design/attributes.csv','design/design.csv'],next_question='Please return the filled design tables when ready.');write(root/'authoring.json',s)
    return dest

def source_files(root):
    for p in root.rglob('*'):
        if not p.is_file() or p.is_symlink():continue
        rel=p.relative_to(root);name=rel.as_posix()
        if any(x in {'.vercel','node_modules','runtime','export','responses','archive'} for x in rel.parts) or p.name.startswith('.env'):continue
        if name in SOURCE_NAMES or (len(rel.parts)==2 and rel.parts[0]=='.greedyq' and p.name in PRIVATE_NAMES) or (rel.parts[0] in {'design','assets','media'} and p.suffix.lower() in {'.csv','.xlsx','.png','.jpg','.jpeg','.svg','.webp','.mp3','.mp4','.wav','.ogg','.webm'}):yield p

def pack(folder,destination):
    root=Path(folder).resolve();target=Path(destination).resolve()
    if target.exists():raise FileExistsError('Keep the previous handoff package.')
    if not (root/'authoring.json').is_file():raise ValueError('An authoring folder is required; an analysis archive is not a resumable study.')
    files=list(source_files(root));manifest={'kind':'greedyq-authoring-package','files':{p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files}}
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,p.relative_to(root).as_posix())
        z.writestr('authoring-package.json',json.dumps(manifest,indent=2))
    return target

def resume(source,destination=None):
    source=Path(source)
    if source.is_dir():return inspect(source)
    if destination is None:raise ValueError('Choose a new folder for the authoring ZIP.')
    target=Path(destination)
    if target.exists():raise FileExistsError('Never overwrite an existing study.')
    with zipfile.ZipFile(source) as z:
        entries=z.infolist()
        if len(entries)>1000 or sum(i.file_size for i in entries)>64*1024*1024:raise ValueError('Authoring package is too large.')
        names=[i.filename for i in entries]
        if len(set(names))!=len(names) or 'authoring-package.json' not in names or 'authoring.json' not in names:raise ValueError('A complete authoring package is required; data archives are not restored.')
        for i in entries:
            p=Path(i.filename)
            if p.is_absolute() or '..' in p.parts or '\\' in i.filename or stat.S_ISLNK(i.external_attr>>16):raise ValueError('Unsafe ZIP member.')
        manifest=json.loads(z.read('authoring-package.json'))
        if manifest.get('kind')!='greedyq-authoring-package' or set(names)!=set(manifest['files'])|{'authoring-package.json'}:raise ValueError('Authoring manifest mismatch.')
        for name,digest in manifest['files'].items():
            if hashlib.sha256(z.read(name)).hexdigest()!=digest:raise ValueError('Authoring source changed in transit.')
        target.mkdir(parents=True)
        for name in manifest['files']:
            p=target/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(name))
    return inspect(target)

def fork(folder,destination,new_id):
    if not re.fullmatch(r'[a-z][a-z0-9_]{1,63}',new_id):raise ValueError('Use a distinct new study ID.')
    root=Path(folder);target=Path(destination)
    if target.exists():raise FileExistsError('Never overwrite the original study.')
    state=json.loads((root/'authoring.json').read_text())
    if new_id==state['study_id']:raise ValueError('A fork needs its own study ID.')
    target.mkdir(parents=True)
    for p in source_files(root):
        rel=p.relative_to(root);q=target/rel;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
    state.update(study_id=new_id,origin={'mode':'fork','study_id':state['study_id']},phase='review',approvals={},next_question='What would you like to change in this independent copy?');write(target/'authoring.json',state)
    design=target/'study.design.json'
    if design.is_file():
        c=json.loads(design.read_text());c['study_id']=new_id;c['fielding_approval']=False;write(design,c)
    settings=target/'collection.json'
    if settings.is_file():
        c=json.loads(settings.read_text());c['mode']='test';c['study_version']='draft-1';c['approvals']={k:False for k in c['approvals']};write(settings,c)
    descriptor=target/'greedyq.study.json'
    if descriptor.is_file():
        c=json.loads(descriptor.read_text());c.update(study_id=new_id,study_version='draft-1',origin={'mode':'fork','study_id':state['origin']['study_id']});write(descriptor,c)
    config=target/'greedyq.yml'
    if config.is_file():
        text=config.read_text();text=re.sub(r'(?m)^(  id:)\s*.*$',r'\1 '+new_id,text,count=1);text=re.sub(r'(?m)^(  version:)\s*.*$',r'\1 draft-1',text,count=1);config.write_text(text)
    for name in PRIVATE_NAMES:
        p=target/'.greedyq'/name
        if not p.is_file():continue
        try:c=json.loads(p.read_text())
        except ValueError:continue
        if 'study_id' in c:c['study_id']=new_id
        if 'study_version' in c:c['study_version']='draft-1'
        for gate in c.get('gates',{}):c['gates'][gate]={'status':'pending'}
        write(p,c)
    manifest=target/'.greedyq/generation-manifest.json'
    if manifest.is_file():
        c=json.loads(manifest.read_text());c['artifacts']=[entry for entry in c.get('artifacts',[]) if (target/entry['path']).is_file()]
        for entry in c['artifacts']:
            entry['sha256']=hashlib.sha256((target/entry['path']).read_bytes()).hexdigest();entry['status']='generated'
        write(manifest,c)
    return target

def upgrade(folder,approved=False,destination=None):
    if not approved:raise ValueError('Researcher approval is required; the pinned version remains unchanged.')
    original=Path(folder);root=Path(destination) if destination else original.with_name(original.name+'-upgraded-'+release())
    if root.exists():raise FileExistsError('Choose a new upgrade folder; preserve the original.')
    root.mkdir(parents=True)
    for p in source_files(original):
        target=root/p.relative_to(original);target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
    s=json.loads((root/'authoring.json').read_text());s['previous_version']=s['greedyq_version'];s['greedyq_version']=release();s['approvals']={};s['phase']='review';write(root/'authoring.json',s)
    stamp_version(root/'survey.qmd')
    settings=root/'collection.json'
    if settings.is_file():
        c=json.loads(settings.read_text());c['mode']='test';c['approvals']={k:False for k in c['approvals']};write(settings,c)
    record_lock(root)
    result=inspect(root);result['output_path']=str(root);return result


def preflight(folder,stage='package'):
    from .cbc import collection_model
    from .cbc_flow import import_questions
    root=Path(folder);settings=json.loads((root/'collection.json').read_text())
    original=copy.deepcopy(settings);settings['mode']='test'
    if (root/'survey.qmd').is_file():
        if 'flow' in settings:raise ValueError('Use ordinary survey.qmd or an explicit flow, not both.')
        settings['flow']=import_questions(root/'survey.qmd')
    model=collection_model(root,settings)
    gates=original.get('approvals',{});blockers=[k for k in ['instrument','consent','data_plan','deployment','fielding'] if gates.get(k) is not True]
    if original.get('mode')!='production':blockers.append('production_mode')
    if model['consent']['researcher_contact'].lower().endswith(('.invalid','@example.com','@example.org','@example.net')):blockers.append('real_researcher_contact')
    if stage=='fielding' and not blockers:
        # Re-run the production guard without changing any source file.
        production=copy.deepcopy(original)
        if 'flow' in settings:production['flow']=settings['flow']
        collection_model(root,production)
    return {'status':'failed' if stage=='fielding' and blockers else 'passed','stage':stage,'study_id':model['study_id'],'module_contract':model.get('module_contract'),'technical_package_valid':True,'fielding_ready':not blockers,'blocking_approvals':blockers,'live_deployment_verified_by_this_check':False,'paid_participant_test_verified':False,'summary':'Package checks passed. Review unresolved approvals before real collection.' if blockers else 'Local fielding approvals recorded. Verify this exact deployed instrument before recruitment.'}
