const {test}=require('node:test'),assert=require('node:assert/strict'),path=require('node:path'),http=require('node:http');
const {chromium}=require('/Users/dongsookim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'..');
test('repeat-preview button starts a fresh capability while refresh resumes and normal links remain unchanged',async()=>{
 const fs=require('node:fs'),g=require('../web/greedyq-core.js'),model=JSON.parse(fs.readFileSync(path.join(root,'examples/complete-study/preview-model.json')));
 model.runtime_policy.mode='test';model.runtime_policy.respondent_source='prolific';model.runtime_policy.prolific.study_id='b'.repeat(24);
 const embed=(html,id,value)=>html.replace(new RegExp('(<script id="'+id+'"[^>]*>)[\\s\\S]*?(</script>)'),(_,a,b)=>a+JSON.stringify(value)+b);
 let html=embed(fs.readFileSync(path.join(root,'templates/browser/respondent.html'),'utf8'),'greedyq-model',model);html=embed(html,'greedyq-deployment',{mode:'supabase',supabase_url:'https://unit.supabase.co',supabase_anon_key:'public'});
 const server=http.createServer((req,res)=>{res.setHeader('content-type',req.url.startsWith('/greedyq-core.js')?'text/javascript':'text/html');res.end(req.url.startsWith('/greedyq-core.js')?fs.readFileSync(path.join(root,'web/greedyq-core.js')):req.url.startsWith('/greedyq-runtime.css')?'':html);});await new Promise(r=>server.listen(0,'localhost',r));
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true}),states=new Map(),starts=[];
 try{
  const page=await browser.newPage();await page.route('https://unit.supabase.co/rest/v1/rpc/**',async route=>{
   const name=route.request().url().split('/').at(-1),body=route.request().postDataJSON();
   if(name==='greedyq_start_prolific_preview'){assert.equal(body.p_preview_token,'a'.repeat(64));assert.equal(body.p_is_test,true);starts.push(body.p_session_id);}
   if(name==='greedyq_save_session')states.set(body.p_session_id,body.p_state);
   return route.fulfill({json:name==='greedyq_resume_session'?{state:states.get(body.p_session_id)||null,registered_model:model,runtime_contract:'randomization-1'}:null});
  });
  const base=`http://localhost:${server.address().port}/`,ids='PROLIFIC_PID='+ 'a'.repeat(24)+'&STUDY_ID='+ 'b'.repeat(24)+'&SESSION_ID='+ 'c'.repeat(24);
  await page.goto(base+'?'+ids+'&gq_preview='+'a'.repeat(64));await page.locator('[data-next]').waitFor();assert(await page.locator('#preview-tools').isVisible());
  const first=starts.at(-1);await page.reload();await page.locator('[data-next]').waitFor();assert.equal(starts.at(-1),first);
  await page.locator('#preview-restart').click();await page.locator('[data-next]').waitFor();assert.notEqual(starts.at(-1),first);assert(states.has(first));assert.equal(new Set(starts).size,2);
  await page.goto(base+'?'+ids);await page.locator('[data-next]').waitFor();assert(await page.locator('#preview-tools').isHidden());
  assert.equal(g.parseProlificLaunch('?'+ids+'&gq_preview='+'a'.repeat(64),'production').status,'failed');
 }finally{await browser.close();await new Promise(r=>server.close(r));}
});
test('connected Prolific outcomes save before code/return, resume and isolate direct tests',async()=>{
 const server=http.createServer((req,res)=>{res.setHeader('content-type','text/html; charset=utf-8');res.end('<meta charset="utf-8"><div id="root"></div>');});await new Promise(resolve=>server.listen(0,'localhost',resolve));
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try{for(const width of [390,1280])for(const outcome of ['completed','screened_out','consent_refused','withdrawn']){
  const page=await browser.newPage({viewport:{width,height:800}}),states=new Map(),requests=[];page.setDefaultTimeout(5000);let model,failTerminal=true;
  const code='C'+String(['completed','screened_out','consent_refused','withdrawn'].indexOf(outcome)+1).padStart(7,'0');
  await page.route('https://unit.supabase.co/rest/v1/rpc/**',async route=>{
   const name=route.request().url().split('/').at(-1),body=route.request().postDataJSON();requests.push([name,body]);
   if(name==='greedyq_resume_session')return route.fulfill({json:{state:states.get(body.p_session_id)||null,runtime_contract:'randomization-1',registered_model:model}});
   if(name==='greedyq_save_session'){
    if(states.get(body.p_session_id)?.lifecycle==='withdrawn')return route.fulfill({status:400,json:{message:'session ended'}});
    if(failTerminal && body.p_state.lifecycle===outcome)return route.fulfill({status:503,json:{message:'synthetic failed save'}});
    states.set(body.p_session_id,outcome==='withdrawn' && body.p_state.lifecycle==='withdrawn'?{...body.p_state,answers:{},history:[],condition:null,consent_accepted:false}:body.p_state);
   }
   return route.fulfill({json:null});
  });
  await page.goto(`http://localhost:${server.address().port}/`);await page.addScriptTag({path:path.join(root,'web/greedyq-core.js')});
  model={study_id:'panel',study_version:'1',greedyq_version:'0.2_fixture',title:'Panel',start_page:'start',conditions:['default'],messages:{next:'Next',previous:'Previous',required:'Required'},runtime_policy:{mode:'test',respondent_source:'prolific',consent:null,duplicate_policy:'resume',prolific:{study_id:'b'.repeat(24),identity_verification:'url_parameters_only',paths:{[outcome]:{page:'end',status:outcome,url:'https://app.prolific.com/submissions/complete?cc='+code,code}}}},pages:[{id:'start',title:'Start',questions:[{id:'answer',type:'text',label:'Synthetic answer',required:true}],next:'end'},{id:'end',title:'End',questions:[],terminal:outcome,redirect:{url:'https://app.prolific.com/submissions/complete?cc='+code,params:{},delay:null,newtab:false,label:'Return'}}]};
  const mount=async external=>page.evaluate(async({model,external})=>{
   window.model=model;window.controller=await greedyQ.mountSupabaseRespondent(document.getElementById('root'),model,{url:'https://unit.supabase.co',anonKey:'sb_publishable_synthetic',externalIdentifiers:external?{PROLIFIC_PID:'a'.repeat(24),STUDY_ID:'b'.repeat(24),SESSION_ID:'c'.repeat(24)}:null});
  },{model,external});
  await mount(true);assert(requests.some(([name])=>name==='greedyq_start_prolific'));assert(!requests.some(([name])=>name==='greedyq_register_external'));
  await page.locator('[data-id="answer"]').fill('synthetic');await page.locator('[data-next]').click();await page.getByText('Response not saved. Please retry before leaving.',{exact:true}).waitFor();
  assert.equal(await page.locator('[data-completion-code]').count(),0);assert(await page.locator('[data-redirect]').isDisabled());
  failTerminal=false;await page.evaluate(()=>controller.render());await page.locator('[data-completion-code]').waitFor();assert((await page.locator('[data-completion-code]').textContent()).includes(code));
  assert.equal([...states.values()][0].lifecycle,outcome);
  if(outcome==='withdrawn'){assert.deepEqual([...states.values()][0].answers,{});assert.deepEqual(await page.evaluate(()=>controller.state.answers),{});}
  const originalId=await page.evaluate(()=>controller.sessionId);
  await mount(true);assert.equal(await page.evaluate(()=>controller.sessionId),originalId);await page.locator('[data-completion-code]').waitFor();
  await page.route('https://app.prolific.com/**',r=>r.fulfill({body:'Synthetic return; no Prolific account accessed'}));
  await page.locator('[data-redirect]').click();assert(page.url().includes('cc='+code));
  await page.goto(`http://localhost:${server.address().port}/direct`);await page.addScriptTag({path:path.join(root,'web/greedyq-core.js')});
  await page.evaluate(({model,outcome})=>{model.start_page='end';greedyQ.mountRespondent(document.getElementById('root'),model,{allowExternalRedirects:true});},{model,outcome});
  assert(await page.locator('[data-redirect]').isDisabled());assert.equal(await page.locator('[data-completion-code]').count(),0);await page.close();
 }}finally{await browser.close();await new Promise(resolve=>server.close(resolve));}
});

test('results CSV joins Prolific identifiers to the matching response only',async()=>{
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try{
  const page=await browser.newPage(),requests=[];page.on('request',r=>{if(r.url().includes('/api/results'))requests.push(r.url())});await page.route('https://results.example.test/',r=>r.fulfill({path:path.join(root,'examples/complete-study/results.html')}));
  await page.route('https://results.example.test/api/results**',r=>r.fulfill({json:{generated_at:new Date().toISOString(),sessions:[{id:'one',created_at:new Date().toISOString(),respondent_source:'prolific',lifecycle_state:'completed',is_test:true},{id:'two',created_at:new Date().toISOString(),respondent_source:'direct',lifecycle_state:'completed',is_test:true}],answers:[],assignments:[],external_identifiers:[{session_id:'one',provider:'prolific',participant_id:'a'.repeat(24),external_study_id:'b'.repeat(24),external_session_id:'c'.repeat(24)}]}}));
  await page.goto('https://results.example.test/');await page.getByText('a'.repeat(24),{exact:true}).waitFor();
  const pending=page.waitForEvent('download');await page.getByRole('button',{name:'Download CSV',exact:true}).click();const download=await pending,stream=await download.createReadStream(),chunks=[];for await(const chunk of stream)chunks.push(chunk);const csv=Buffer.concat(chunks).toString();
  assert(csv.startsWith('\ufeff'));assert(csv.slice(1).startsWith('"PROLIFIC_PID","STUDY_ID","SESSION_ID"'));assert(csv.split('\n')[1].includes('a'.repeat(24)));assert(csv.split('\n')[2].startsWith('"","",""'));
  assert.equal(new URL(requests[0]).searchParams.get('study'),'digital_service_info_001');
 }finally{await browser.close();}
});
