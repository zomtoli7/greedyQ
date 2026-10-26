"""Deterministic CBC CSV/XLSX import and account-free preview reference.

No survey-authored code, workbook formulas, macros or external links are run.
This module does not register live CBC storage or estimate a choice model.
"""
import hashlib
import io
import json
import math
from pathlib import Path, PurePosixPath
import re
import xml.etree.ElementTree as ET
import zipfile
import zlib

MAX_FILE = 16 * 1024 * 1024
MAX_XML = 8 * 1024 * 1024
MAX_ROWS = 50000
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
ATTRIBUTE_HEADERS = ['attribute_id', 'attribute_label', 'level_id', 'level_label']
CONFIG_KEYS = {'schema_version','status','object','study_id','research_question','attributes_source','design_source',
               'alternatives_per_task','tasks_per_block','block_assignment','task_order','alternative_order','none',
               'design_origin','statistical_efficiency','fielding_approval','proposed_estimator','attribute_ids','prohibitions','language'}


class CBCError(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)


def fail(code, message):
    raise CBCError(code, message)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def parse_csv(text):
    if not isinstance(text,str) or len(text.encode('utf-8')) > MAX_FILE or '\x00' in text:
        fail('CBC001','The CSV is too large or contains invalid text.')
    text=text.removeprefix('\ufeff').replace('\r\n','\n').replace('\r','\n')
    rows=[]; row=[]; field=''; quoted=False; closed=False; i=0
    while i<len(text):
        char=text[i]
        if quoted:
            if char=='"':
                if i+1<len(text) and text[i+1]=='"':field+='"';i+=1
                else:quoted=False;closed=True
            else:field+=char
        elif char in ',\n':
            row.append(field);field='';closed=False
            if char=='\n':rows.append(row);row=[]
        elif char=='"':
            if field or closed:fail('CBC001','The CSV has an invalid quoted field.')
            quoted=True
        else:
            if closed:fail('CBC001','The CSV has text after a closing quote.')
            field+=char
        i+=1
    if quoted:fail('CBC001','The CSV has an unclosed quoted field.')
    if field or row or closed:rows.append([*row,field])
    return clean_table(rows)


def clean_table(rows):
    rows=[row for row in rows if any(cell!='' for cell in row)]
    if not rows:fail('CBC002','The table is empty. Fill the blank template first.')
    header=rows[0]
    if len(header)>64 or any(not x for x in header) or len(set(header))!=len(header):
        fail('CBC002','Table headings must be nonempty and unique.')
    if len(rows)>MAX_ROWS+1:fail('CBC002','The table has too many rows.')
    data=[]
    for index,row in enumerate(rows[1:],2):
        if len(row)!=len(header) or any(cell=='' for cell in row):
            fail('CBC003',f'Row {index} is incomplete or has extra cells.')
        data.append(dict(zip(header,row)))
    if not data:fail('CBC002','The table is empty. Fill the blank template first.')
    return header,data


def xml_document(data):
    try:text=data.decode('utf-8')
    except UnicodeError:fail('CBC010','The workbook contains invalid XML.')
    if len(data)>MAX_XML or '<!DOCTYPE' in text.upper() or '<!ENTITY' in text.upper():
        fail('CBC010','The workbook contains oversized or unsafe XML.')
    try:return ET.fromstring(text)
    except ET.ParseError:fail('CBC010','The workbook contains invalid XML.')


def read_xlsx(data):
    if len(data)>MAX_FILE:fail('CBC010','The workbook is too large.')
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            infos=archive.infolist();names=[x.filename for x in infos]
            if len(names)>256 or len(set(names))!=len(names) or sum(x.file_size for x in infos)>32*1024*1024:
                fail('CBC010','The workbook archive exceeds its safety limits.')
            for info in infos:
                parts=PurePosixPath(info.filename).parts
                if info.flag_bits&1 or info.compress_type not in (0,8) or info.file_size>MAX_XML or '..' in parts or info.filename.startswith('/'):
                    fail('CBC010','The workbook archive contains an unsafe entry.')
                if 'vbaproject' in info.filename.lower() or 'externallinks/' in info.filename.lower():
                    fail('CBC011','Use a values-only workbook without macros or external links.')
            documents={}
            for name in names:
                if name.endswith(('.xml','.rels')):
                    document=xml_document(archive.read(name));documents[name]=document
                    if any(node.tag.rsplit('}',1)[-1]=='f' for node in document.iter()) or any(node.attrib.get('TargetMode')=='External' for node in document.iter()):
                        fail('CBC011','Use a values-only workbook without formulas or external links.')
                    if name=='[Content_Types].xml' and any('macroenabled' in str(node.attrib).lower() for node in document.iter()):
                        fail('CBC011','Use a values-only workbook without macros or external links.')
            book=documents.get('xl/workbook.xml');rels=documents.get('xl/_rels/workbook.xml.rels')
            if book is None or rels is None:fail('CBC010','The workbook is missing its sheet directory.')
            sheets=book.findall('s:sheets/s:sheet',NS)
            if [s.attrib.get('name') for s in sheets]!=['Attributes','Design']:
                fail('CBC012','The workbook must contain Attributes and Design sheets in that order.')
            targets={r.attrib.get('Id'):r.attrib.get('Target','') for r in rels}
            shared=[''.join(node.itertext()) for node in documents.get('xl/sharedStrings.xml',ET.Element('empty')).findall('s:si',NS)]
            result={}
            for sheet in sheets:
                target=targets.get(sheet.attrib.get('{'+NS['r']+'}id'),'')
                target=target.lstrip('/') if target.startswith('/xl/') else 'xl/'+target
                if '..' in PurePosixPath(target).parts or not target.startswith('xl/worksheets/') or target not in documents:
                    fail('CBC010','The workbook has an invalid worksheet path.')
                document=documents[target]
                if document.find('s:mergeCells',NS) is not None:fail('CBC012','Do not merge cells in the input sheets.')
                rows=[]
                for row in document.findall('s:sheetData/s:row',NS):
                    cells={}
                    for cell in row.findall('s:c',NS):
                        match=re.fullmatch(r'([A-Z]+)[1-9][0-9]*',cell.attrib.get('r',''))
                        if not match:fail('CBC010','The workbook has an invalid cell address.')
                        col=0
                        for char in match[1]:col=col*26+ord(char)-64
                        if col>64 or col in cells:fail('CBC010','The workbook has duplicate or too many columns.')
                        value=cell.find('s:v',NS);raw=value.text or '' if value is not None else ''
                        kind=cell.attrib.get('t','n')
                        if kind=='s':
                            if not raw.isdigit() or int(raw)>=len(shared):fail('CBC010','The workbook has an invalid text reference.')
                            raw=shared[int(raw)]
                        elif kind=='inlineStr':raw=''.join(cell.find('s:is',NS).itertext()) if cell.find('s:is',NS) is not None else ''
                        elif kind=='b':raw='TRUE' if raw=='1' else 'FALSE'
                        elif kind=='e':fail('CBC011','The workbook contains a spreadsheet error.')
                        elif kind not in ('n','str','d'):fail('CBC010','The workbook has an unsupported cell type.')
                        cells[col]=raw.replace('\r\n','\n').replace('\r','\n')
                    nonempty=[col for col,value in cells.items() if value!='']
                    if nonempty:rows.append([cells.get(col,'') for col in range(1,max(nonempty)+1)])
                    if len(rows)>MAX_ROWS+1:fail('CBC002','The table has too many rows.')
                result[sheet.attrib['name']]=clean_table(rows)
            return result['Attributes'],result['Design']
    except CBCError:raise
    except (zipfile.BadZipFile,KeyError,UnicodeError,RuntimeError,EOFError,ValueError,zlib.error):
        fail('CBC010','The workbook is not a readable XLSX file.')


def identifier(value):
    if not isinstance(value,str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,119}',value) or value in ('constructor','prototype','__proto__'):
        fail('CBC004','Use stable text IDs with letters, digits, dots, hyphens or underscores.')
    return value


def positive(value,maximum):
    return isinstance(value,(int,float)) and not isinstance(value,bool) and math.isfinite(value) and value==int(value) and 1<=value<=maximum


def normalize(attributes_table,design_table,config):
    if not isinstance(config,dict) or set(config)-CONFIG_KEYS or CONFIG_KEYS-{'language','prohibitions'}-set(config):fail('CBC005','The CBC settings contain unsupported fields.')
    if config.get('schema_version')!='0.3-draft.1' or config.get('object')!='greedyQCBC' or config.get('status')!='design_only' or config.get('fielding_approval') is not False:
        fail('CBC005','Use the CBC preview settings; this importer does not authorize fielding.')
    study_id=identifier(config.get('study_id'))
    language=config.get('language','en')
    if language not in ('en','ko','zh-CN','zh-TW'):fail('CBC005','Choose en, ko, zh-CN or zh-TW for preview messages.')
    if not isinstance(config.get('research_question'),str) or not 1<=len(config['research_question'])<=2000:
        fail('CBC005','The research question must be a short text label.')
    count=config.get('alternatives_per_task');size=config.get('tasks_per_block')
    if not positive(count,10) or count<2 or not positive(size,100):fail('CBC005','Set 2–10 alternatives and 1–100 tasks per block.')
    count=int(count);size=int(size)
    ah,ar=attributes_table;dh,dr=design_table
    if ah!=ATTRIBUTE_HEADERS:fail('CBC002','Attribute headings must be attribute_id, attribute_label, level_id, level_label.')
    attributes=[];by_attribute={}
    for row in ar:
        aid=identifier(row['attribute_id']);lid=identifier(row['level_id'])
        if aid in ['respondent_id', 'block_id', 'task_id', 'task_position', 'alternative_id', 'display_position', 'is_none', 'chosen', 'design_version', 'design_sha256', 'presentation_state']:fail('CBC004','An attribute ID is reserved for exported response metadata.')
        if len(row['attribute_label'])>500 or len(row['level_label'])>2000:fail('CBC004','An attribute or level label is too long.')
        if aid not in by_attribute:
            attribute={'id':aid,'label':row['attribute_label'],'levels':[]};by_attribute[aid]=attribute;attributes.append(attribute)
        attribute=by_attribute[aid]
        if attribute['label']!=row['attribute_label']:fail('CBC004','One attribute has conflicting labels.')
        if any(level['id']==lid for level in attribute['levels']):fail('CBC004','One attribute has a duplicate level ID.')
        attribute['levels'].append({'id':lid,'label':row['level_label']})
    aids=[a['id'] for a in attributes]
    if not 2<=len(aids)<=50 or any(len(a['levels'])<2 for a in attributes):fail('CBC004','Use 2–50 attributes, each with at least two levels.')
    if config.get('attribute_ids')!=aids or dh!=['block_id','task_id','alternative_id',*aids]:
        fail('CBC002','Confirm the attribute IDs and matching Design columns; do not keep placeholder headings.')
    none=config.get('none')
    if not isinstance(none,dict) or set(none)!={'enabled','id','label','position'} or not isinstance(none['enabled'],bool) or none['id']!='none' or none['position']!='last' or not isinstance(none['label'],str) or not 1<=len(none['label'])<=500:
        fail('CBC005','Configure none separately with an enabled flag, label, reserved ID and last position.')
    if config.get('task_order') not in ('source_order','randomized_once_per_respondent') or config.get('alternative_order') not in ('source_order','randomized_once_per_task'):
        fail('CBC005','Choose the supported task and alternative order rules.')
    prohibitions=config.get('prohibitions',[])
    if not isinstance(prohibitions,list):fail('CBC005','Prohibitions must be a list of attribute-level combinations.')
    level_sets={a['id']:{x['id'] for x in a['levels']} for a in attributes}
    for rule in prohibitions:
        if not isinstance(rule,dict) or not rule or any(k not in level_sets or not isinstance(v,str) or v not in level_sets[k] for k,v in rule.items()):fail('CBC005','A prohibited combination uses an unknown attribute or level.')
    blocks=[];by_block={};keys=set()
    for row in dr:
        bid=identifier(row['block_id']);tid=identifier(row['task_id']);aid=identifier(row['alternative_id']);key=(bid,tid,aid)
        if key in keys:fail('CBC006','A block/task/alternative key is duplicated.')
        keys.add(key)
        if aid=='none':fail('CBC006','Do not add none as an ordinary design row.')
        levels={key:row[key] for key in aids}
        if any(value not in level_sets[key] for key,value in levels.items()):fail('CBC006','A design cell contains an unknown level code.')
        if any(all(levels[k]==v for k,v in rule.items()) for rule in prohibitions):fail('CBC006','A design row contains a prohibited combination.')
        if bid not in by_block:by_block[bid]={'id':bid,'tasks':[]};blocks.append(by_block[bid])
        block=by_block[bid];task=next((t for t in block['tasks'] if t['id']==tid),None)
        if task is None:task={'id':tid,'alternatives':[]};block['tasks'].append(task)
        if any(a['levels']==levels for a in task['alternatives']):fail('CBC006','A task contains identical ordinary profiles.')
        task['alternatives'].append({'id':aid,'levels':levels})
    assignment=config.get('block_assignment')
    if not isinstance(assignment,dict) or set(assignment)!={'method','unit','weights'} or assignment['method']!='simple' or assignment['unit']!='respondent' or not isinstance(assignment['weights'],dict) or set(assignment['weights'])!=set(by_block) or any(not positive(w,1000000) for w in assignment['weights'].values()) or sum(assignment['weights'].values())>1000000:
        fail('CBC005','Confirm one positive integer weight for each block and simple respondent allocation.')
    for block in blocks:
        block['weight']=int(assignment['weights'][block['id']])
        if len(block['tasks'])!=size or any(len(t['alternatives'])!=count for t in block['tasks']):fail('CBC006','Every block/task must match the declared task/alternative counts.')
    model={'schema_version':'0.3-preview.1','kind':'cbc_preview','study_id':study_id,'language':language,
           'research_question':config.get('research_question',''),'attributes':attributes,'blocks':blocks,
           'alternatives_per_task':count,'tasks_per_block':size,'task_order':config['task_order'],
           'alternative_order':config['alternative_order'],'none':none,'prohibitions':prohibitions}
    model['design_sha256']=digest(canonical(model))
    model['warnings']=['Preview only: no live response storage or fielding approval.','File validation does not establish statistical design efficiency.']
    return model


def import_design(config,attributes_text=None,design_text=None,workbook=None):
    if workbook is not None:
        if attributes_text is not None or design_text is not None:fail('CBC001','Choose either a workbook or the two CSV files.')
        at,dt=read_xlsx(workbook)
    else:at,dt=parse_csv(attributes_text),parse_csv(design_text)
    return normalize(at,dt,config)


def inspect_design(model):
    """Descriptive counts only; never an efficiency or identifiability test."""
    tasks=[t for b in model['blocks'] for t in b['tasks']]
    profiles=[a for t in tasks for a in t['alternatives']]
    return {'blocks':len(model['blocks']),'tasks':len(tasks),'profiles':len(profiles),
            'level_frequencies':{a['id']:{l['id']:sum(p['levels'][a['id']]==l['id'] for p in profiles) for l in a['levels']} for a in model['attributes']},
            'within_task_overlap':{a['id']:sum(len({p['levels'][a['id']] for p in t['alternatives']})<len(t['alternatives']) for t in tasks) for a in model['attributes']},
            'unused_levels':[{ 'attribute_id':a['id'],'level_id':l['id']} for a in model['attributes'] for l in a['levels'] if not any(p['levels'][a['id']]==l['id'] for p in profiles)],
            'statistical_efficiency_established':False}


def load_design(directory):
    root=Path(directory).resolve()
    config=json.loads((root/'study.design.json').read_text())
    def source(name):
        value=config.get(name,'');p=(root/value).resolve()
        if not p.is_relative_to(root) or not p.is_file():fail('CBC001','A design source must be a file within the study folder.')
        if p.stat().st_size>MAX_FILE:fail('CBC001','A design source is too large.')
        return p.read_bytes().decode('utf-8-sig')
    return import_design(config,source('attributes_source'),source('design_source'))


def build_preview(directory,output=None,workbook=None):
    root=Path(directory).resolve()
    config=json.loads((root/'study.design.json').read_text())
    if workbook is not None:
        source=Path(workbook)
        if source.stat().st_size>MAX_FILE:fail('CBC010','The workbook is too large.')
        model=import_design(config,workbook=source.read_bytes())
    else:model=load_design(root)
    repo=Path(__file__).resolve().parents[1]
    template=(repo/'templates/browser/cbc-preview.html').read_text()
    def payload(value):return json.dumps(value,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c').replace('\u2028','\\u2028').replace('\u2029','\\u2029')
    for key,value in [('__CBC_LIBRARY__',(repo/'web/greedyq-cbc.js').read_text()),('__CBC_MODEL__',payload(model)),('__CBC_CONFIG__',payload(config))]:
        if template.count(key)!=1:raise ValueError('The fixed CBC preview template has an invalid marker.')
        template=template.replace(key,value)
    target=Path(output).resolve() if output else root/'cbc-preview.html'
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(template)
    return target,model
