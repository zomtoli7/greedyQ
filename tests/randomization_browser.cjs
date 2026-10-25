/* Real browser conformance; synthetic participants only, no network services. */
const {test}=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const {chromium}=require(process.env.GREEDYQ_PLAYWRIGHT || '/Users/dongsookim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'..'),core=require('../web/greedyq-core.js');
const plan={id:'frame',method:'fixed_block',unit:'respondent',persistence_key:'session_id',conditions:{a:1,b:1},block_size:4};
test('reference vectors and independent simple draws',()=>{
 assert.deepEqual(core.shuffle(['a','b','c','d'],()=>0),['b','c','d','a']);
 const simple={...plan,method:'simple'};delete simple.block_size;
 for(let i=0;i<100;i++)assert.deepEqual(core.drawAssignment(simple,{},()=>0),{condition:'a',block_id:null});
});
test('weighted block totals and persistence use declared method, not least counts',()=>{
 const b=core.createMemoryBackend(),weighted={...plan,conditions:{a:2,b:1},block_size:6};
 for(let block=0;block<200;block++) {
  const values=Array.from({length:6},(_,i)=>b.assign(`${block}-${i}`,['a','b'],weighted));
  assert.equal(values.filter(v=>v==='a').length,4);
 }
 const stored=b.inspect(),again=core.createMemoryBackend(stored);
 assert.equal(again.assign('0-0',['a','b'],weighted),stored.allocations[0].condition);
 assert.throws(()=>again.assign('new',['a','b'],{...weighted,block_size:12}));
 const simple={...plan,method:'simple',conditions:{a:2,b:1}};delete simple.block_size;
 let count=0;for(let i=0;i<12000;i++)count+=core.drawAssignment(simple,{}).condition==='a';
 assert(count>7400&&count<8600);
});
test('connected browser serializes saves, waits for assignment, and rejects an old server contract',async()=>{
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'greedyq-rpc-browser-'));
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try {
  const model={study_id:'rpc_test',study_version:'1',greedyq_version:'test',title:'RPC test',start_page:'baseline',conditions:['a','b'],assignment_page:'baseline',randomization:plan,runtime_policy:{mode:'test'},messages:{previous:'Previous',next:'Next',required:'Required'},pages:[{id:'baseline',title:'Baseline',questions:[],next:'arm'},{id:'arm',title:'Arm',questions:[],next:'done'},{id:'done',title:'Done',questions:[],terminal:'completed'}]};
  const file=path.join(tmp,'index.html');fs.writeFileSync(file,`<div id="root"></div><div id="error"></div><script src="file://${root}/web/greedyq-core.js"></script><script>greedyQ.mountSupabaseRespondent(document.getElementById('root'),${JSON.stringify(model)},{url:'https://test.supabase.co',anonKey:'sb_publishable_test'}).catch(e=>document.getElementById('error').textContent=e.message)</script>`);
  const page=await browser.newPage(),calls=[];let stored={},assigned=null,inflight=0,maxInflight=0,old=false;
  await page.route('https://test.supabase.co/rest/v1/rpc/**',async route=>{
   const name=route.request().url().split('/').at(-1),body=route.request().postDataJSON();calls.push(name);
   let result=null;
   if(name==='greedyq_resume_session')result={state:stored,condition:assigned,...(old?{}:{runtime_contract:'randomization-1',registered_model:model})};
   if(name==='greedyq_save_session') {inflight++;maxInflight=Math.max(maxInflight,inflight);await new Promise(r=>setTimeout(r,30));stored=body.p_state;inflight--;}
   if(name==='greedyq_assign_condition'){assert.equal(stored.page,'baseline');assigned='b';result=assigned;}
   await route.fulfill({status:200,contentType:'application/json',body:JSON.stringify(result)});
  });
  await page.goto('file://'+file);await page.getByRole('heading',{name:'Baseline',exact:true}).waitFor();
  await page.getByRole('button',{name:'Next',exact:true}).click();await page.getByRole('heading',{name:'Arm',exact:true}).waitFor();
  assert.equal(assigned,'b');assert.equal(maxInflight,1);
  await page.reload();await page.getByRole('heading',{name:'Arm',exact:true}).waitFor();
  assert.equal(calls.filter(n=>n==='greedyq_assign_condition').length,1);
  old=true;await page.reload();await page.getByText(/finish the database upgrade/).waitFor();
  assert.equal(await page.locator('[data-next]').count(),0);
 } finally {await browser.close();fs.rmSync(tmp,{recursive:true,force:true});}
});
test('browser question ordering, validation, assignment and resume at two widths',async()=>{
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'greedyq-random-browser-'));
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try {
  const q=id=>({id,type:'mc',label:id,required:true,options:[{label:'Yes',value:'yes'},{label:'No',value:'no'}]});
  const model={study_id:'browser_random',title:'Randomization test',organization:'Test team',start_page:'consent',conditions:['a','b'],messages:{previous:'Previous',next:'Next',required:'Answer required'},assignment_page:'baseline',randomization:plan,runtime_policy:{mode:'test',consent:{question:'consent',accept_value:'yes'}},pages:[{id:'consent',title:'Consent',questions:[q('consent')],next:'baseline',routes:[{when:{field:'consent',equals:'no'},to:'refused'}]},{id:'baseline',title:'Baseline',questions:['q1','q2','q3','anchor'].map(q),shuffle_questions:['q1','q2','q3'],routes:[{when:{field:'condition',equals:'a'},to:'arm_a'},{when:{field:'condition',equals:'b'},to:'arm_b'}]},{id:'arm_a',title:'Arm A',questions:[],next:'complete'},{id:'arm_b',title:'Arm B',questions:[],next:'complete'},{id:'complete',title:'Done',questions:[],terminal:'completed'},{id:'refused',title:'Refused',questions:[],terminal:'consent_refused'}]};
  const html=path.join(tmp,'index.html');
  fs.writeFileSync(html,`<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="file://${root}/web/greedyq-runtime.css"><div id="root"></div><script src="file://${root}/web/greedyq-core.js"></script><script>const model=${JSON.stringify(model)};window.backend=greedyQ.createLocalMockBackend('test-random');window.controller=greedyQ.mountRespondent(document.getElementById('root'),model,{backend,sessionId:new URLSearchParams(location.search).get('id')});</script>`);
  for(const width of [390,1280]) {
   const context=await browser.newContext({viewport:{width,height:850}}),page=await context.newPage(),errors=[];
   page.on('pageerror',e=>errors.push(e.message));
   await page.goto('file://'+html+'?id=person');
   assert.equal(await page.evaluate(()=>backend.inspect().allocations.length),0);
   await page.getByRole('button',{name:'Next',exact:true}).click();
   assert.equal(await page.evaluate(()=>backend.inspect().allocations.length),0);
   await page.getByRole('radio',{name:'Yes',exact:true}).check();await page.getByRole('button',{name:'Next',exact:true}).click();
   await page.getByRole('heading',{name:'Baseline',exact:true}).waitFor();
   const order=await page.locator('[data-q]').evaluateAll(es=>es.map(e=>e.dataset.q));
   assert.equal(order.at(-1),'anchor');assert.deepEqual([...order].sort(),['anchor','q1','q2','q3']);
   await page.getByRole('button',{name:'Next',exact:true}).click();assert.equal(await page.evaluate(()=>backend.inspect().allocations.length),0);
   for(const id of order)await page.locator(`[data-q="${id}"]`).getByRole('radio',{name:'Yes',exact:true}).check();
   await page.getByRole('button',{name:'Next',exact:true}).click();await page.getByRole('heading',{name:/Arm [AB]/}).waitFor();
   const condition=await page.evaluate(()=>controller.state.condition);
   assert.equal(await page.evaluate(()=>backend.inspect().allocations.length),1);
   await page.reload();await page.getByRole('heading',{name:/Arm [AB]/}).waitFor();
   assert.equal(await page.evaluate(()=>controller.state.condition),condition);
   await page.getByRole('button',{name:'Previous',exact:true}).click();
   assert.deepEqual(await page.locator('[data-q]').evaluateAll(es=>es.map(e=>e.dataset.q)),order);
   await page.getByRole('button',{name:'Next',exact:true}).click();await page.getByRole('heading',{name:/Arm [AB]/}).waitFor();
   assert.equal(await page.evaluate(()=>backend.inspect().allocations.length),1);
   await page.getByRole('button',{name:'Next',exact:true}).click();await page.getByRole('heading',{name:'Done',exact:true}).waitFor();
   await page.goto('file://'+html+'?id=declines');await page.getByRole('radio',{name:'No',exact:true}).check();await page.getByRole('button',{name:'Next',exact:true}).click();await page.getByRole('heading',{name:'Refused',exact:true}).waitFor();
   assert.equal(await page.evaluate(()=>backend.inspect().allocations.length),1);
   assert.deepEqual(errors,[]);await context.close();
  }
  const server=require('node:http').createServer((req,res)=>{
   const asset=req.url.split('?')[0];res.setHeader('content-type',asset.endsWith('.js')?'text/javascript':asset.endsWith('.css')?'text/css':'text/html');
   if(asset==='/greedyq-core.js'||asset==='/greedyq-runtime.css')res.end(fs.readFileSync(path.join(root,'web',asset.slice(1))));
   else res.end(fs.readFileSync(html,'utf8').replaceAll(`file://${root}/web/`,'/'));
  });
  await new Promise(resolve=>server.listen(0,'localhost',resolve));
  try {
   const tabsContext=await browser.newContext();
   const tabs=await Promise.all(Array.from({length:8},async(_,i)=>{const p=await tabsContext.newPage();await p.goto(`http://localhost:${server.address().port}/?id=tab-${i}`);return p;}));
   await Promise.all(tabs.map((p,k)=>p.evaluate(async ({k,plan})=>{for(let i=0;i<5;i++)await backend.assign(`parallel-${k}-${i}`,['a','b'],plan);},{k,plan})));
   await tabs[0].evaluate(()=>backend.synchronize());
   const allocations=await tabs[0].evaluate(()=>backend.inspect().allocations);
   assert.equal(allocations.length,40);assert.equal(allocations.filter(a=>a.condition==='a').length,20);
   const retry=await Promise.all(tabs.map(p=>p.evaluate(plan=>backend.assign('parallel-0-0',['a','b'],plan),plan)));
   assert.equal(new Set(retry).size,1);assert.equal(await tabs[0].evaluate(()=>backend.inspect().allocations.length),40);
   await tabsContext.close();
  } finally {await new Promise(resolve=>server.close(resolve));}
 } finally {await browser.close();fs.rmSync(tmp,{recursive:true,force:true});}
});
