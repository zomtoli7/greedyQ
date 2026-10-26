/* Local-only module preview transport. Never used by the Supabase respondent page. */
(function(scope){
'use strict';
function transport(model,storage,key){
 const C=scope.greedyQCBC;let data;try{data=JSON.parse(storage.getItem(key));}catch{}
 if(!data||data.hash!==model.cbc.design_sha256)data={hash:model.cbc.design_sha256,state:{phase:'consent',revision:0,lifecycle:'created'}};
 const persist=()=>storage.setItem(key,JSON.stringify(data));
 function envelope(){const st=data.state,b=model.cbc.blocks.find(b=>b.id===st.block_id);return{runtime_contract:'cbc-1',module_contract:model.module_contract,study_id:model.study_id,design_sha256:model.cbc.design_sha256,state:JSON.parse(JSON.stringify(st)),is_test:true,source:'direct',consent:model.consent,title:model.title,organization:model.organization,language:model.language,has_before:!!model.flow?.before.length,model:st.phase==='tasks'&&b?{...model.cbc,blocks:[b]}:null,form_page:model.flow?.[st.phase]?.[st.form_index],form_answers:st.survey_answers||{},terminal_at:data.terminal_at||null};}
 return async(_,options)=>{try{const name=_.split('/').pop(),p=JSON.parse(options.body),s=data.state;let changed=true;
  if(name==='greedyq_cbc_start'||name==='greedyq_cbc_resume'||name==='greedyq_cbc_ack')changed=false;
  else if(name==='greedyq_cbc_withdraw'){data.state={phase:'withdrawn',lifecycle:'withdrawn',revision:s.revision+1,withdrawn:true};data.terminal_at||=new Date().toISOString();}
  else if(name==='greedyq_cbc_consent'){
   if(s.phase!=='consent')throw Error('Consent already decided');
   if(p.p_decision==='refused'){s.phase='consent_refused';s.lifecycle='consent_refused';}
   else{data.state={...C.freshSession(model.cbc),revision:1,lifecycle:'in_progress',phase:model.flow?.before.length?'before':'tasks',form_index:0,survey_answers:{}};if(data.state.phase==='tasks')data.state.visited=[data.state.task_order[0]];}
  }else{
   if(s.last_request_id===p.p_request_id)return {ok:true,status:200,json:async()=>envelope()};
   if(p.p_revision!==s.revision)throw Error('Revision conflict');
   if(name==='greedyq_cbc_form_step'){
    const page=model.flow?.[s.phase]?.[s.form_index];if(!page||page.id!==p.p_page_id)throw Error('Wrong question page');Object.assign(s.survey_answers,p.p_answers);
    if(p.p_direction==='previous'){if(s.form_index)s.form_index--;else if(s.phase==='after'){s.phase='tasks';s.index=s.task_order.length-1;}else throw Error('First page');}
    else if(s.form_index+1<model.flow[s.phase].length)s.form_index++;
    else if(s.phase==='before'){s.phase='tasks';s.index=0;if(!s.visited.includes(s.task_order[0]))s.visited.push(s.task_order[0]);}else{s.phase='completed';s.completed=true;s.lifecycle='completed';}
   }else if(name==='greedyq_cbc_step'){
    if(s.phase!=='tasks'||p.p_task_id!==s.task_order[s.index])throw Error('Wrong CBC task');if(p.p_choice!==null)s.answers[p.p_task_id]=p.p_choice;
    if(p.p_direction==='previous'){if(s.index)s.index--;else if(model.flow?.before.length){s.phase='before';s.form_index=model.flow.before.length-1;}else throw Error('First task');}
    else{if(!s.answers[p.p_task_id])throw Error('Choose an alternative');if(s.index+1<s.task_order.length)s.index++;else if(model.flow?.after.length){s.phase='after';s.form_index=0;}else{s.phase='completed';s.completed=true;s.lifecycle='completed';}}
    if(s.phase==='tasks'&&!s.visited.includes(s.task_order[s.index]))s.visited.push(s.task_order[s.index]);
   }else throw Error('Unknown preview operation');s.revision++;s.last_request_id=p.p_request_id;
  }
  if(['completed','consent_refused','withdrawn'].includes(data.state.phase))data.terminal_at||=new Date().toISOString();if(changed)persist();return{ok:true,status:200,json:async()=>envelope()};
 }catch(error){return{ok:false,status:400,json:async()=>({message:error.message})};}};
}
scope.greedyQCBCPreview={transport};
})(globalThis);
