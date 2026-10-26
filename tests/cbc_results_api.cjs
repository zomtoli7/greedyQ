/* Synthetic results API boundaries and complete pagination; no external requests. */
const{test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
function handler(fetcher,env={SUPABASE_URL:'https://synthetic.test',SUPABASE_SECRET_KEY:'synthetic_server_only'}){const ctx={module:{exports:{}},process:{env},fetch:fetcher,URL,Error,JSON,Array,Date};vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../templates/vercel/api/results.js'),'utf8'),ctx);return ctx.module.exports;}
async function call(h,req={}){let body;const res={setHeader(){},end(s){body=JSON.parse(s);}};await h({method:'GET',query:{study:'cbc',scope:'production',source:'direct'},headers:{},...req},res);return{status:res.statusCode,body};}
test('CBC results paginate every session and answer, batch long ID lists and honor server page caps',async()=>{
 const sessions=Array.from({length:103},(_,i)=>({id:'session_'+i})),answers=Array.from({length:2003},(_,i)=>({session_id:'session_'+(i%103),question_id:'cbc:task_'+i,value:{kind:'cbc'}})),calls=[];
 const h=handler(async(input,opts)=>{const u=new URL(input);calls.push(u);assert.equal(opts.headers.Prefer,'count=exact');let rows=u.pathname.endsWith('gq_sessions')?sessions:u.pathname.endsWith('gq_answers')?answers:[];if(u.searchParams.has('session_id')){const ids=u.searchParams.get('session_id').slice(4,-1).split(',');assert(ids.length<=100);rows=rows.filter(x=>ids.includes(x.session_id));}const offset=Number(u.searchParams.get('offset')),slice=rows.slice(offset,offset+200);return{ok:true,headers:{get:()=>`${offset}-${offset+slice.length-1}/${rows.length}`},json:async()=>slice};});
 const r=await call(h);assert.equal(r.status,200);assert.equal(r.body.sessions.length,103);assert.equal(r.body.answers.length,2003);assert.equal(new Set(r.body.answers.map(a=>a.question_id)).size,2003);assert(calls.some(u=>u.searchParams.get('offset')==='200'));assert(calls.filter(u=>u.pathname.endsWith('gq_sessions')).every(u=>u.searchParams.get('is_test')==='eq.false'&&u.searchParams.get('respondent_source')==='eq.direct'));
});
test('CBC test grants use the service-only RPC and reject unprotected-origin creation',async()=>{
 const calls=[],h=handler(async(u,opts)=>{calls.push({u,opts});return{ok:true,json:async()=>'a'.repeat(64)}});
 let r=await call(h,{method:'POST',headers:{host:'research.test',origin:'https://evil.test','content-type':'application/json'},body:{action:'preview',kind:'cbc',study:'cbc'}});assert.equal(r.status,403);assert.equal(calls.length,0);
 r=await call(h,{method:'POST',headers:{host:'research.test',origin:'https://research.test','content-type':'application/json'},body:{action:'preview',kind:'cbc',study:'cbc'}});assert.equal(r.status,200);assert(calls[0].u.endsWith('/greedyq_issue_cbc_preview'));assert.equal(JSON.parse(calls[0].opts.body).p_study_id,'cbc');assert.equal(r.body.expires_in_hours,24);
});
test('failed later page returns an error instead of a truncated success',async()=>{
 const h=handler(async u=>{const p=new URL(u);if(p.searchParams.get('offset')!=='0')return{ok:false,status:503};return{ok:true,headers:{get:()=> '0-999/1001'},json:async()=>Array.from({length:1000},(_,i)=>({id:String(i)}))};});const r=await call(h);assert.equal(r.status,502);assert(!r.body.sessions);assert(r.body.error.includes('503'));
});
