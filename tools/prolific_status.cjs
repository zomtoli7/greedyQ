/* Offline operator evidence summary. No credentials, network calls or payment actions. */
'use strict';
const providerStates=['unknown','draft','active','paused','paused_for_review','awaiting_review','completed'];
function assessStatus(model,snapshot,{providerStatus='unknown',submissionConfirmed=false,paymentConfirmed=false}={}){
 if(!providerStates.includes(providerStatus))throw new Error('Unknown Prolific provider status.');
 if(typeof submissionConfirmed!=='boolean' || typeof paymentConfirmed!=='boolean')throw new Error('Evidence confirmations must be boolean.');
 if(!model?.study_id || model.runtime_policy?.respondent_source!=='prolific')throw new Error('Choose a compiled Prolific study model.');
 const mode=model.runtime_policy.mode,ids=new Set(),sessions=(snapshot.sessions || []).filter(s=>s.study_id===model.study_id && s.is_test===(mode!=='production') && s.respondent_source==='prolific');
 const external=(snapshot.external_identifiers || []).filter(e=>e.provider==='prolific'),answers=snapshot.answers || [],issues=[];
 let completed=0,withdrawn=0,erased=0,validCompleted=0;
 for(const session of sessions){
  if(ids.has(session.id)){issues.push('Duplicate internal session rows in the snapshot.');continue;}ids.add(session.id);
  const links=external.filter(e=>e.session_id===session.id),link=links[0];
  const valid=links.length===1 && link.external_study_id===model.runtime_policy.prolific?.study_id && ['participant_id','external_study_id','external_session_id'].every(k=>typeof link[k]==='string' && /^[a-fA-F0-9]{24}$/.test(link[k]));
  if(!valid)issues.push('A response has missing, malformed or mismatched Prolific identifiers.');
  if(session.lifecycle_state==='completed'){
   completed++;if(valid && answers.some(a=>a.session_id===session.id))validCompleted++;
   else issues.push('A completed response lacks matched identifiers or saved answers.');
  }
  if(session.lifecycle_state==='withdrawn'){
   withdrawn++;if(!answers.some(a=>a.session_id===session.id))erased++;
   else issues.push('A withdrawn response still has answers; inspect its migration/version before claiming erasure.');
  }
 }
 const waiting=['paused_for_review','paused','draft'].includes(providerStatus);
 if((submissionConfirmed || paymentConfirmed) && waiting)issues.push('Platform evidence conflicts with the reported pre-fielding or paused state.');
 if(paymentConfirmed && !submissionConfirmed)issues.push('Payment confirmation needs an independently matched platform submission.');
 const verified=mode==='production' && !waiting && !issues.length && validCompleted>0 && submissionConfirmed && paymentConfirmed;
 let phase=verified?'verified':providerStatus==='paused_for_review'?'waiting_for_platform_review':waiting?'waiting_for_platform':!sessions.length?'waiting_for_participants':!submissionConfirmed?'awaiting_submission_match':'awaiting_payment_confirmation';
 if(issues.length)phase='needs_review';else if(mode!=='production')phase='test_only';
 return{schema_version:'0.2',study_id:model.study_id,mode,provider_status:providerStatus,phase,
  counts:{sessions:ids.size,completed,withdrawn,withdrawn_without_answers:erased},
  evidence:{snapshot_checked:true,platform_submission_confirmed:submissionConfirmed,payment_confirmed:paymentConfirmed,end_to_end_paid_verified:verified},issues,
  next_action:providerStatus==='paused_for_review'?'Wait for Prolific review; preserve study settings, budget and completion paths.':verified?'Record verification date and the approved retention deadline.':'Compare the protected response with the actual Prolific submission before any payment approval.'};
}
if(require.main===module){
 const fs=require('node:fs'),[modelPath,snapshotPath,providerStatus='unknown']=process.argv.slice(2);
 try{if(!modelPath || !snapshotPath)throw new Error('Usage: node tools/prolific_status.cjs MODEL.json PRIVATE_RESULTS_SNAPSHOT.json [provider_status]');
  process.stdout.write(JSON.stringify(assessStatus(JSON.parse(fs.readFileSync(modelPath)),JSON.parse(fs.readFileSync(snapshotPath)),{providerStatus}),null,2)+'\n');
 }catch(error){process.stderr.write(error.message+'\n');process.exitCode=1;}
}
module.exports={assessStatus};
