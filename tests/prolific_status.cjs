const {test}=require('node:test'),assert=require('node:assert/strict'),{assessStatus}=require('../tools/prolific_status.cjs');
const model={study_id:'pilot',runtime_policy:{mode:'production',respondent_source:'prolific',prolific:{study_id:'b'.repeat(24)}}};
function data(){return{sessions:[{id:'one',study_id:'pilot',is_test:false,respondent_source:'prolific',lifecycle_state:'completed'}],answers:[{session_id:'one',question_id:'choice',value:'yes'}],external_identifiers:[{session_id:'one',provider:'prolific',participant_id:'a'.repeat(24),external_study_id:'b'.repeat(24),external_session_id:'c'.repeat(24)}]};}
test('routine review waits without treating a deployment or empty database as paid verification',()=>{
 const r=assessStatus(model,{sessions:[]},{providerStatus:'paused_for_review'});assert.equal(r.phase,'waiting_for_platform_review');assert.equal(r.evidence.end_to_end_paid_verified,false);assert(r.next_action.includes('preserve'));
 assert.equal(assessStatus(model,data(),{providerStatus:'paused_for_review',submissionConfirmed:true,paymentConfirmed:true}).phase,'needs_review');
});
test('saved answers do not verify a platform submission or payment; matched explicit evidence is required',()=>{
 const r=assessStatus(model,data(),{providerStatus:'active'});assert.equal(r.phase,'awaiting_submission_match');assert.equal(r.evidence.end_to_end_paid_verified,false);
 assert.equal(assessStatus(model,data(),{providerStatus:'completed',submissionConfirmed:true,paymentConfirmed:true}).evidence.end_to_end_paid_verified,true);
 const bad=data();bad.external_identifiers[0].external_study_id='d'.repeat(24);assert.equal(assessStatus(model,bad,{providerStatus:'completed',submissionConfirmed:true,paymentConfirmed:true}).phase,'needs_review');
 assert(!JSON.stringify(r).includes('a'.repeat(24)));
});
test('other studies, Direct and Test records cannot prove production completion; legacy withdrawn answers are flagged',()=>{
 const snapshot=data();snapshot.sessions[0].is_test=true;assert.equal(assessStatus(model,snapshot).counts.sessions,0);
 snapshot.sessions[0].is_test=false;snapshot.sessions[0].lifecycle_state='withdrawn';const r=assessStatus(model,snapshot);assert.equal(r.phase,'needs_review');assert.equal(r.counts.withdrawn_without_answers,0);
 snapshot.answers=[];assert.equal(assessStatus(model,snapshot).counts.withdrawn_without_answers,1);
});
