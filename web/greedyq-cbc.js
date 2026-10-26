/* Fixed browser-native CBC import/validation and local preview helpers. */
(function(scope){
  'use strict';
  const MAX_FILE=16*1024*1024,MAX_XML=8*1024*1024,MAX_ROWS=50000;
  class CBCError extends Error{constructor(code,message){super(message);this.name='CBCError';this.code=code;}}
  const fail=(code,message)=>{throw new CBCError(code,message);};
  const object=v=>v!==null&&typeof v==='object'&&!Array.isArray(v);
  const canonical=v=>JSON.stringify(sort(v));
  function sort(v){return Array.isArray(v)?v.map(sort):object(v)?Object.fromEntries(Object.keys(v).sort().map(k=>[k,sort(v[k])])):v;}
  const digest=async text=>[...new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(text)))].map(x=>x.toString(16).padStart(2,'0')).join('');
  function cleanTable(rows){
    rows=rows.filter(row=>row.some(v=>v!==''));
    if(!rows.length)fail('CBC002','The table is empty. Fill the blank template first.');
    const header=rows[0];
    if(header.length>64||header.some(x=>!x)||new Set(header).size!==header.length)fail('CBC002','Table headings must be nonempty and unique.');
    if(rows.length>MAX_ROWS+1)fail('CBC002','The table has too many rows.');
    const data=rows.slice(1).map((row,index)=>{if(row.length!==header.length||row.some(x=>x===''))fail('CBC003',`Row ${index+2} is incomplete or has extra cells.`);return Object.fromEntries(header.map((key,i)=>[key,row[i]]));});
    if(!data.length)fail('CBC002','The table is empty. Fill the blank template first.');
    return[header,data];
  }
  function parseCSV(text){
    if(typeof text!=='string'||new TextEncoder().encode(text).length>MAX_FILE||text.includes('\0'))fail('CBC001','The CSV is too large or contains invalid text.');
    text=text.replace(/^\uFEFF/,'').replaceAll('\r\n','\n').replaceAll('\r','\n');
    const rows=[];let row=[],field='',quoted=false,closed=false;
    for(let i=0;i<text.length;i++){
      const char=text[i];
      if(quoted){if(char==='"'){if(text[i+1]==='"'){field+='"';i++;}else{quoted=false;closed=true;}}else field+=char;}
      else if(char===','||char==='\n'){row.push(field);field='';closed=false;if(char==='\n'){rows.push(row);row=[];}}
      else if(char==='"'){if(field||closed)fail('CBC001','The CSV has an invalid quoted field.');quoted=true;}
      else{if(closed)fail('CBC001','The CSV has text after a closing quote.');field+=char;}
    }
    if(quoted)fail('CBC001','The CSV has an unclosed quoted field.');
    if(field||row.length||closed)rows.push([...row,field]);
    return cleanTable(rows);
  }
  const identifier=value=>{if(typeof value!=='string'||!/^[A-Za-z0-9][A-Za-z0-9_.-]{0,119}$/.test(value)||['constructor','prototype','__proto__'].includes(value))fail('CBC004','Use stable text IDs with letters, digits, dots, hyphens or underscores.');return value;};
  const positive=(value,max)=>Number.isInteger(value)&&value>=1&&value<=max;
  const equal=(a,b)=>canonical(a)===canonical(b);
  const exactKeys=(v,keys)=>object(v)&&equal(Object.keys(v).sort(),[...keys].sort());
  async function normalize(at,dt,config){
    const allowed=['schema_version','status','object','study_id','research_question','attributes_source','design_source','alternatives_per_task','tasks_per_block','block_assignment','task_order','alternative_order','none','design_origin','statistical_efficiency','fielding_approval','proposed_estimator','attribute_ids','prohibitions','language'];
    if(!object(config)||Object.keys(config).some(k=>!allowed.includes(k))||allowed.filter(k=>!['language','prohibitions'].includes(k)).some(k=>!Object.hasOwn(config,k)))fail('CBC005','The CBC settings contain unsupported fields.');
    if(config.schema_version!=='0.3-draft.1'||config.object!=='greedyQCBC'||config.status!=='design_only'||config.fielding_approval!==false)fail('CBC005','Use the CBC preview settings; this importer does not authorize fielding.');
    const studyId=identifier(config.study_id),language=config.language??'en';
    if(!['en','ko','zh-CN','zh-TW'].includes(language))fail('CBC005','Choose en, ko, zh-CN or zh-TW for preview messages.');
    if(typeof config.research_question!=='string'||[...config.research_question].length<1||[...config.research_question].length>2000)fail('CBC005','The research question must be a short text label.');
    const count=config.alternatives_per_task,size=config.tasks_per_block;
    if(!positive(count,10)||count<2||!positive(size,100))fail('CBC005','Set 2–10 alternatives and 1–100 tasks per block.');
    const[ah,ar]=at,[dh,dr]=dt;
    if(!equal(ah,['attribute_id','attribute_label','level_id','level_label']))fail('CBC002','Attribute headings must be attribute_id, attribute_label, level_id, level_label.');
    const attributes=[],byAttribute=new Map();
    for(const row of ar){
      const aid=identifier(row.attribute_id),lid=identifier(row.level_id);
      if(["respondent_id", "block_id", "task_id", "task_position", "alternative_id", "display_position", "is_none", "chosen", "design_version", "design_sha256", "presentation_state"].includes(aid))fail('CBC004','An attribute ID is reserved for exported response metadata.');
      if([...row.attribute_label].length>500||[...row.level_label].length>2000)fail('CBC004','An attribute or level label is too long.');
      if(!byAttribute.has(aid)){const a={id:aid,label:row.attribute_label,levels:[]};byAttribute.set(aid,a);attributes.push(a);}
      const a=byAttribute.get(aid);
      if(a.label!==row.attribute_label)fail('CBC004','One attribute has conflicting labels.');
      if(a.levels.some(x=>x.id===lid))fail('CBC004','One attribute has a duplicate level ID.');
      a.levels.push({id:lid,label:row.level_label});
    }
    const aids=attributes.map(a=>a.id);
    if(aids.length<2||aids.length>50||attributes.some(a=>a.levels.length<2))fail('CBC004','Use 2–50 attributes, each with at least two levels.');
    if(!equal(config.attribute_ids,aids)||!equal(dh,['block_id','task_id','alternative_id',...aids]))fail('CBC002','Confirm the attribute IDs and matching Design columns; do not keep placeholder headings.');
    const none=config.none;
    if(!exactKeys(none,['enabled','id','label','position'])||typeof none.enabled!=='boolean'||none.id!=='none'||none.position!=='last'||typeof none.label!=='string'||[...none.label].length<1||[...none.label].length>500)fail('CBC005','Configure none separately with an enabled flag, label, reserved ID and last position.');
    if(!['source_order','randomized_once_per_respondent'].includes(config.task_order)||!['source_order','randomized_once_per_task'].includes(config.alternative_order))fail('CBC005','Choose the supported task and alternative order rules.');
    const prohibitions=config.prohibitions??[],levelSets=new Map(attributes.map(a=>[a.id,new Set(a.levels.map(x=>x.id))]));
    if(!Array.isArray(prohibitions))fail('CBC005','Prohibitions must be a list of attribute-level combinations.');
    for(const rule of prohibitions)if(!object(rule)||!Object.keys(rule).length||Object.entries(rule).some(([k,v])=>!levelSets.has(k)||!levelSets.get(k).has(v)))fail('CBC005','A prohibited combination uses an unknown attribute or level.');
    const blocks=[],byBlock=new Map(),keys=new Set();
    for(const row of dr){
      const bid=identifier(row.block_id),tid=identifier(row.task_id),aid=identifier(row.alternative_id),key=JSON.stringify([bid,tid,aid]);
      if(keys.has(key))fail('CBC006','A block/task/alternative key is duplicated.');keys.add(key);
      if(aid==='none')fail('CBC006','Do not add none as an ordinary design row.');
      const levels=Object.fromEntries(aids.map(k=>[k,row[k]]));
      if(Object.entries(levels).some(([k,v])=>!levelSets.get(k).has(v)))fail('CBC006','A design cell contains an unknown level code.');
      if(prohibitions.some(rule=>Object.entries(rule).every(([k,v])=>levels[k]===v)))fail('CBC006','A design row contains a prohibited combination.');
      if(!byBlock.has(bid)){const b={id:bid,tasks:[]};byBlock.set(bid,b);blocks.push(b);}
      const block=byBlock.get(bid);let task=block.tasks.find(t=>t.id===tid);
      if(!task){task={id:tid,alternatives:[]};block.tasks.push(task);}
      if(task.alternatives.some(a=>equal(a.levels,levels)))fail('CBC006','A task contains identical ordinary profiles.');
      task.alternatives.push({id:aid,levels});
    }
    const assignment=config.block_assignment;
    if(!exactKeys(assignment,['method','unit','weights'])||assignment.method!=='simple'||assignment.unit!=='respondent'||!object(assignment.weights)||!equal(Object.keys(assignment.weights).sort(),[...byBlock.keys()].sort())||Object.values(assignment.weights).some(w=>!positive(w,1000000))||Object.values(assignment.weights).reduce((a,b)=>a+b,0)>1000000)fail('CBC005','Confirm one positive integer weight for each block and simple respondent allocation.');
    for(const b of blocks){b.weight=assignment.weights[b.id];if(b.tasks.length!==size||b.tasks.some(t=>t.alternatives.length!==count))fail('CBC006','Every block/task must match the declared task/alternative counts.');}
    const model={schema_version:'0.3-preview.1',kind:'cbc_preview',study_id:studyId,language,research_question:config.research_question??'',attributes,blocks,alternatives_per_task:count,tasks_per_block:size,task_order:config.task_order,alternative_order:config.alternative_order,none,prohibitions};
    model.design_sha256=await digest(canonical(model));model.warnings=['Preview only: no live response storage or fielding approval.','File validation does not establish statistical design efficiency.'];return model;
  }

  const decoder=new TextDecoder('utf-8',{fatal:true});
  const crcTable=Uint32Array.from({length:256},(_,n)=>{for(let k=0;k<8;k++)n=n&1?0xedb88320^(n>>>1):n>>>1;return n>>>0;});
  function crc32(bytes){let n=0xffffffff;for(const b of bytes)n=crcTable[(n^b)&255]^(n>>>8);return(n^0xffffffff)>>>0;}
  async function zipEntries(input){
    const bytes=input instanceof Uint8Array?input:new Uint8Array(input);
    if(bytes.length>MAX_FILE||bytes.length<22)fail('CBC010','The workbook is too large or not a readable XLSX file.');
    const d=new DataView(bytes.buffer,bytes.byteOffset,bytes.byteLength),u16=i=>d.getUint16(i,true),u32=i=>d.getUint32(i,true);let end=-1;
    for(let i=bytes.length-22;i>=Math.max(0,bytes.length-65557);i--)if(u32(i)===0x06054b50&&i+22+u16(i+20)===bytes.length){end=i;break;}
    if(end<0||u16(end+4)||u16(end+6)||u16(end+8)!==u16(end+10)||u16(end+10)>256)fail('CBC010','The workbook archive exceeds its safety limits.');
    let pos=u32(end+16),total=0;const entries=new Map();
    for(let index=0;index<u16(end+10);index++){
      if(pos+46>end||u32(pos)!==0x02014b50)fail('CBC010','The workbook archive directory is invalid.');
      const flags=u16(pos+8),method=u16(pos+10),crc=u32(pos+16),compressed=u32(pos+20),size=u32(pos+24),len=u16(pos+28),extra=u16(pos+30),comment=u16(pos+32),offset=u32(pos+42);
      if(pos+46+len+extra+comment>end)fail('CBC010','The workbook archive directory is invalid.');
      let name;try{name=decoder.decode(bytes.slice(pos+46,pos+46+len));}catch{fail('CBC010','The workbook archive contains an unsafe entry.');}
      total+=size;
      if(entries.has(name)||flags&1||![0,8].includes(method)||size>MAX_XML||total>32*1024*1024||name.startsWith('/')||name.split('/').includes('..'))fail('CBC010','The workbook archive contains an unsafe entry.');
      if(/vbaproject|externallinks\//i.test(name))fail('CBC011','Use a values-only workbook without macros or external links.');
      if(offset+30>bytes.length||u32(offset)!==0x04034b50)fail('CBC010','The workbook archive data is invalid.');
      const start=offset+30+u16(offset+26)+u16(offset+28);if(start+compressed>pos)fail('CBC010','The workbook archive data is invalid.');
      let content=bytes.slice(start,start+compressed);
      if(method===8){
        try{
          const stream=new Blob([content]).stream().pipeThrough(new DecompressionStream('deflate-raw')).getReader(),chunks=[];let count=0;
          while(true){const item=await stream.read();if(item.done)break;count+=item.value.length;if(count>size||count>MAX_XML){await stream.cancel();fail('CBC010','The workbook archive exceeds its safety limits.');}chunks.push(item.value);}
          content=new Uint8Array(count);let at=0;for(const c of chunks){content.set(c,at);at+=c.length;}
        }catch(error){if(error instanceof CBCError)throw error;fail('CBC010','This browser could not decompress the workbook. Use the CSV files instead.');}
      }
      if(content.length!==size||crc32(content)!==crc)fail('CBC010','The workbook archive checksum is invalid.');
      entries.set(name,content);pos+=46+len+extra+comment;
    }
    return entries;
  }
  const children=(node,name)=>Array.from(node?.children??[]).filter(x=>x.localName===name);
  const descendants=(node,name)=>Array.from(node?.getElementsByTagName('*')??[]).filter(x=>x.localName===name);
  async function readXLSX(input){
    const entries=await zipEntries(input),docs=new Map();
    for(const[name,bytes]of entries)if(/\.(xml|rels)$/.test(name)){
      let text;try{text=decoder.decode(bytes);}catch{fail('CBC010','The workbook contains invalid XML.');}
      if(/<!DOCTYPE|<!ENTITY/i.test(text))fail('CBC010','The workbook contains oversized or unsafe XML.');
      const doc=new DOMParser().parseFromString(text,'application/xml');if(doc.querySelector('parsererror'))fail('CBC010','The workbook contains invalid XML.');
      if(descendants(doc,'f').length||descendants(doc,'Relationship').some(x=>x.getAttribute('TargetMode')==='External'))fail('CBC011','Use a values-only workbook without formulas or external links.');
      if(name==='[Content_Types].xml'&&descendants(doc,'Override').some(x=>/macroenabled/i.test(x.getAttribute('ContentType')??'')))fail('CBC011','Use a values-only workbook without macros or external links.');
      docs.set(name,doc);
    }
    const book=docs.get('xl/workbook.xml'),rels=docs.get('xl/_rels/workbook.xml.rels');
    if(!book||!rels)fail('CBC010','The workbook is missing its sheet directory.');
    const sheets=descendants(book,'sheet');if(!equal(sheets.map(x=>x.getAttribute('name')),['Attributes','Design']))fail('CBC012','The workbook must contain Attributes and Design sheets in that order.');
    const targets=new Map(descendants(rels,'Relationship').map(x=>[x.getAttribute('Id'),x.getAttribute('Target')])),shared=descendants(docs.get('xl/sharedStrings.xml'),'si').map(x=>x.textContent),result=[];
    for(const sheet of sheets){
      let target=targets.get(sheet.getAttributeNS('http://schemas.openxmlformats.org/officeDocument/2006/relationships','id'))??'';
      target=target.startsWith('/xl/')?target.slice(1):'xl/'+target;
      if(target.split('/').includes('..')||!target.startsWith('xl/worksheets/')||!docs.has(target))fail('CBC010','The workbook has an invalid worksheet path.');
      const doc=docs.get(target);if(descendants(doc,'mergeCells').length)fail('CBC012','Do not merge cells in the input sheets.');
      const rows=[];
      for(const row of descendants(doc,'row')){
        const cells=new Map();for(const cell of children(row,'c')){
          const match=/^([A-Z]+)[1-9][0-9]*$/.exec(cell.getAttribute('r')??'');if(!match)fail('CBC010','The workbook has an invalid cell address.');
          let col=0;for(const char of match[1])col=col*26+char.charCodeAt(0)-64;
          if(col>64||cells.has(col))fail('CBC010','The workbook has duplicate or too many columns.');
          let raw=children(cell,'v')[0]?.textContent??'';const kind=cell.getAttribute('t')??'n';
          if(kind==='s'){if(!/^\d+$/.test(raw)||Number(raw)>=shared.length)fail('CBC010','The workbook has an invalid text reference.');raw=shared[Number(raw)];}
          else if(kind==='inlineStr')raw=children(cell,'is')[0]?.textContent??'';
          else if(kind==='b')raw=raw==='1'?'TRUE':'FALSE';
          else if(kind==='e')fail('CBC011','The workbook contains a spreadsheet error.');
          else if(!['n','str','d'].includes(kind))fail('CBC010','The workbook has an unsupported cell type.');
          cells.set(col,raw.replaceAll('\r\n','\n').replaceAll('\r','\n'));
        }
        const nonempty=[...cells].filter(([,v])=>v!=='').map(([k])=>k);if(nonempty.length)rows.push(Array.from({length:Math.max(...nonempty)},(_,i)=>cells.get(i+1)??''));
        if(rows.length>MAX_ROWS+1)fail('CBC002','The table has too many rows.');
      }result.push(cleanTable(rows));
    }return result;
  }
  async function importDesign({config,attributesText,designText,workbook}){
    if(workbook!==undefined&&workbook!==null){if(attributesText!==undefined||designText!==undefined)fail('CBC001','Choose either a workbook or the two CSV files.');const[a,d]=await readXLSX(workbook);return normalize(a,d,config);}
    return normalize(parseCSV(attributesText),parseCSV(designText),config);
  }
  function randomInt(n){if(!Number.isInteger(n)||n<1||n>0x100000000)throw Error('Invalid random bound');const cap=Math.floor(0x100000000/n)*n;let x;do{x=crypto.getRandomValues(new Uint32Array(1))[0];}while(x>=cap);return x%n;}
  function shuffle(items){const a=[...items];for(let i=a.length-1;i>0;i--){const j=randomInt(i+1);[a[i],a[j]]=[a[j],a[i]];}return a;}
  function freshSession(model,forcedBlock){
    let block=model.blocks.find(b=>b.id===forcedBlock);
    if(forcedBlock&&!block)throw Error('Unknown preview block');
    if(!block){let draw=randomInt(model.blocks.reduce((n,b)=>n+b.weight,0));block=model.blocks.find(b=>(draw-=b.weight)<0);}
    return{design_sha256:model.design_sha256,block_id:block.id,task_order:(model.task_order==='source_order'?block.tasks:shuffle(block.tasks)).map(t=>t.id),alternative_orders:Object.fromEntries(block.tasks.map(t=>[t.id,(model.alternative_order==='source_order'?t.alternatives:shuffle(t.alternatives)).map(a=>a.id)])),answers:{},visited:[],index:0,completed:false,withdrawn:false};
  }
  function validateSession(model,state){
    if(!object(state)||state.design_sha256!==model.design_sha256)return false;
    if(state.withdrawn===true)return exactKeys(state,['design_sha256','withdrawn']);
    const block=model.blocks.find(b=>b.id===state.block_id);if(!block||!Array.isArray(state.task_order)||!equal([...state.task_order].sort(),block.tasks.map(t=>t.id).sort())||!Number.isInteger(state.index)||state.index<0||state.index>=block.tasks.length||!object(state.answers)||!object(state.alternative_orders)||!Array.isArray(state.visited)||state.visited.some(id=>!state.task_order.includes(id))||new Set(state.visited).size!==state.visited.length||!equal(Object.keys(state.alternative_orders).sort(),block.tasks.map(t=>t.id).sort()))return false;
    for(const t of block.tasks){if(!Array.isArray(state.alternative_orders[t.id])||!equal([...state.alternative_orders[t.id]].sort(),t.alternatives.map(a=>a.id).sort()))return false;if(Object.hasOwn(state.answers,t.id)&&!t.alternatives.some(a=>a.id===state.answers[t.id])&&!(model.none.enabled&&state.answers[t.id]==='none'))return false;}
    return Object.keys(state.answers).every(k=>state.task_order.includes(k))&&typeof state.completed==='boolean'&&typeof state.withdrawn==='boolean'&&(!state.completed||state.task_order.every(k=>Object.hasOwn(state.answers,k)));
  }
  function longRows(model,state,respondent='virtual'){
    if(!validateSession(model,state))throw Error('Invalid preview session');if(state.withdrawn)return[];
    const block=model.blocks.find(b=>b.id===state.block_id),rows=[];
    for(const tid of state.task_order){if(!state.visited.includes(tid))continue;const task=block.tasks.find(t=>t.id===tid),order=[...state.alternative_orders[tid],...(model.none.enabled?['none']:[])];
      order.forEach((aid,i)=>{const a=task.alternatives.find(a=>a.id===aid);rows.push({respondent_id:respondent,block_id:block.id,task_id:tid,task_position:state.task_order.indexOf(tid)+1,alternative_id:aid,display_position:i+1,is_none:aid==='none',chosen:Object.hasOwn(state.answers,tid)?Number(state.answers[tid]===aid):null,...Object.fromEntries(model.attributes.map(x=>[x.id,a?.levels[x.id]??''])),design_version:model.schema_version,design_sha256:model.design_sha256,presentation_state:Object.hasOwn(state.answers,tid)?'answered':'presented'});});
    }return rows;
  }
  function inspectDesign(model){
    const tasks=model.blocks.flatMap(b=>b.tasks),profiles=tasks.flatMap(t=>t.alternatives);
    return{blocks:model.blocks.length,tasks:tasks.length,profiles:profiles.length,
      level_frequencies:Object.fromEntries(model.attributes.map(a=>[a.id,Object.fromEntries(a.levels.map(l=>[l.id,profiles.filter(p=>p.levels[a.id]===l.id).length]))])),
      within_task_overlap:Object.fromEntries(model.attributes.map(a=>[a.id,tasks.filter(t=>new Set(t.alternatives.map(p=>p.levels[a.id])).size<t.alternatives.length).length])),
      unused_levels:model.attributes.flatMap(a=>a.levels.filter(l=>!profiles.some(p=>p.levels[a.id]===l.id)).map(l=>({attribute_id:a.id,level_id:l.id}))),statistical_efficiency_established:false};
  }
  function csv(rows){if(!rows.length)return'';const fields=Object.keys(rows[0]);const q=v=>{let s=String(v??'');if(typeof v==='string'&&/^[\t\r\n]|^\s*[=+\-@]/.test(s))s="'"+s;return'"'+s.replaceAll('"','""')+'"';};return'\ufeff'+[fields,...rows.map(r=>fields.map(k=>r[k]))].map(row=>row.map(q).join(',')).join('\r\n');}
  const api={CBCError,canonical,digest,parseCSV,readXLSX,normalize,importDesign,freshSession,validateSession,longRows,inspectDesign,csv};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;scope.greedyQCBC=api;
})(typeof globalThis!=='undefined'?globalThis:this);
