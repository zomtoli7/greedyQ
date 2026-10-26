/* Agent-only CBC provisioning. No account sign-in or upload is performed here. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
async function registerCBCStudy(client,model){
 const C=require('../web/greedyq-cbc.js');
 if(model.kind!=='cbc_study'||!model.pages?.length||!model.cbc||!model.consent?.text)throw Error('Reviewed CBC collection model required');
 const c=model.cbc,base=Object.fromEntries(Object.entries(c).filter(([k])=>!['design_sha256','warnings'].includes(k)));
 if(await C.digest(C.canonical(base))!==c.design_sha256)throw Error('CBC design hash mismatch');
 if(crypto.createHash('sha256').update(model.consent.text).digest('hex')!==model.consent.document_sha256)throw Error('Consent hash mismatch');
 if(!['direct','prolific'].includes(model.runtime_policy?.respondent_source)||!['test','production'].includes(model.runtime_policy?.mode))throw Error('Collection mode and source required');
 if(model.runtime_policy.mode==='production'&&(!model.fielding_approved||!['instrument','consent','data_plan','deployment','fielding'].every(k=>model.approvals?.[k]===true)))throw Error('CBC fielding approval required');
 // Reconstruct the canonical input to validate every code/count/order rule, not only the hash.
 const csv=rows=>rows.map(r=>r.map(x=>'"'+String(x).replaceAll('"','""')+'"').join(',')).join('\n');
 const aids=c.attributes.map(a=>a.id),attrs=[['attribute_id','attribute_label','level_id','level_label'],...c.attributes.flatMap(a=>a.levels.map(l=>[a.id,a.label,l.id,l.label]))];
 const rows=[['block_id','task_id','alternative_id',...aids],...c.blocks.flatMap(b=>b.tasks.flatMap(t=>t.alternatives.map(a=>[b.id,t.id,a.id,...aids.map(k=>a.levels[k])]))) ];
 const config={schema_version:'0.3-draft.1',status:'design_only',object:'greedyQCBC',study_id:c.study_id,research_question:c.research_question,attributes_source:'design/attributes.csv',design_source:'design/design.csv',alternatives_per_task:c.alternatives_per_task,tasks_per_block:c.tasks_per_block,block_assignment:{method:'simple',unit:'respondent',weights:Object.fromEntries(c.blocks.map(b=>[b.id,b.weight]))},task_order:c.task_order,alternative_order:c.alternative_order,none:c.none,design_origin:'reviewed_import',statistical_efficiency:'not_established',fielding_approval:false,proposed_estimator:'not_committed',attribute_ids:aids,prohibitions:c.prohibitions,language:c.language};
 if(c.presentation)config.presentation=c.presentation;
 const checked=await C.importDesign({config,attributesText:csv(attrs),designText:csv(rows)});if(checked.design_sha256!==c.design_sha256||model.study_id!==c.study_id)throw Error('CBC design contract mismatch');
 const settings={schema_version:'0.3-collection.1',study_version:model.study_version,title:model.title,organization:model.organization,mode:model.runtime_policy.mode,source:model.runtime_policy.respondent_source,consent:model.consent,approvals:model.approvals};
 if(settings.source==='prolific')settings.prolific=model.runtime_policy.prolific;
 const verified=await C.collectionModel(c,settings,model.greedyq_version);if(C.canonical(verified)!==C.canonical(model))throw Error('CBC collection contract mismatch');
 return require('./cloud_lifecycle.cjs').registerStudy(client,model);
}
function prepareCBCDeployments({repo,packageDirectory,model:providedModel,directory,url,publishableKey}){
 if(new URL(url).protocol!=='https:'||!publishableKey?.startsWith('sb_publishable_'))throw Error('Public Supabase URL and publishable key required');
 const model=providedModel||JSON.parse(fs.readFileSync(path.join(packageDirectory,'registered-model.json')));if(model.kind!=='cbc_study')throw Error('CBC package required');
 fs.mkdirSync(directory,{recursive:false,mode:0o700});
 const embed=(html,id,value)=>html.replace(new RegExp('(<script id="'+id+'"[^>]*>)[\\s\\S]*?(</script>)'),(_,a,b)=>a+JSON.stringify(value).replace(/</g,'\\u003c').replace(/\u2028/g,'\\u2028').replace(/\u2029/g,'\\u2029')+b);
 for(const kind of ['survey','results']){
  const dest=path.join(directory,kind);fs.mkdirSync(dest);
  for(const asset of ['greedyq-core.js','greedyq-runtime.css','greedyq-cbc.js','greedyq-cbc.css','greedyq-cbc-collection.js'])fs.copyFileSync(path.join(repo,'web',asset),path.join(dest,asset));
  const descriptor=Object.fromEntries(['study_id','study_version','greedyq_version','title','organization','language','runtime_policy'].map(k=>[k,model[k]]));descriptor.design_sha256=model.cbc.design_sha256;
  const resultsModel=Object.fromEntries(Object.entries(model).filter(([k])=>!['cbc','consent','approvals'].includes(k)));resultsModel.cbc_attributes=model.cbc.attributes;
  let html=embed(fs.readFileSync(path.join(repo,'templates/browser',kind==='survey'?'cbc-respondent.html':'results.html'),'utf8'),'greedyq-model',kind==='survey'?descriptor:resultsModel);
  if(kind==='survey')html=embed(html,'greedyq-deployment',{mode:'supabase',supabase_url:url,supabase_anon_key:publishableKey});
  fs.writeFileSync(path.join(dest,'index.html'),html);fs.writeFileSync(path.join(dest,'vercel.json'),JSON.stringify({cleanUrls:false}));
  if(kind==='results'){fs.mkdirSync(path.join(dest,'api'));fs.copyFileSync(path.join(repo,'templates/vercel/api/results.js'),path.join(dest,'api/results.js'));}
 }

 return {resultsProtection:{ssoProtection:{deploymentType:'all'}},surveyProtection:{ssoProtection:null}};
}
module.exports={registerCBCStudy,prepareCBCDeployments};
