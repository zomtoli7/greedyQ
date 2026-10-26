const {test}=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const {chromium}=require('/Users/dongsookim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
test('results identify the study, explain empty filters, protect CSV text and reject stale requests',async()=>{
 const model={study_id:'usability',title:'Service feedback',organization:'Example team',greedyq_version:'test',pages:[{id:'feedback',title:'Your experience',questions:[{id:'comment',type:'textarea',label:'Your suggestions'},{id:'age',type:'numeric',label:'A signed number'},{id:'custom_budget',type:'custom',base_type:'constant_sum',label:'Allocation',options:[{value:'a',label:'First'},{value:'b',label:'Second'}]},{id:'unanswered',type:'text',label:'Unanswered'},{id:'source',type:'text',label:'How did you hear about us?'}]}]};
 const html=fs.readFileSync(path.resolve(__dirname,'../templates/browser/results.html'),'utf8').replace('<script id="greedyq-model" type="application/json">{}</script>',`<script id="greedyq-model" type="application/json">${JSON.stringify(model)}</script>`);
 const server=http.createServer((req,res)=>{res.setHeader('content-type','text/html');res.end(html)});await new Promise(r=>server.listen(0,'localhost',r));
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try{
  const page=await browser.newPage();let fail=false,delay=false,release,started;
  const oldStarted=new Promise(r=>started=r);
  function payload(scope,source,count){return{generated_at:new Date().toISOString(),scope,source,sessions:Array.from({length:count},(_,i)=>({id:'s'+i,current_page:'feedback',created_at:'2026-10-25',terminal_at:'2026-10-25T09:08:25.169Z',lifecycle_state:'completed',respondent_source:'direct',is_test:true})),answers:count?[{session_id:'s0',question_id:'comment',value:'=1+1, "한글 中文"\nsecond line'},{session_id:'s0',question_id:'source',value:'A colleague'},{session_id:'s0',question_id:'age',value:-5},{session_id:'s0',question_id:'custom_budget',value:{a:40,b:60}}]:[],assignments:[],external_identifiers:[]}}
  await page.route('**/api/results?*',async route=>{
   const u=new URL(route.request().url()),scope=u.searchParams.get('scope'),source=u.searchParams.get('source');
   if(fail)return route.fulfill({status:502,json:{error:'Could not load results'}});
   if(delay&&source==='all'){started();await new Promise(r=>release=r);return route.fulfill({json:payload(scope,source,9)})}
   return route.fulfill({json:payload(scope,source,scope==='test'?2:0)});
  });
  await page.goto(`http://localhost:${server.address().port}/results`);
  await page.waitForFunction(()=>document.querySelector('#started').textContent==='0');
  assert.equal(await page.locator('h1').textContent(),'Service feedback');assert((await page.locator('#view-note').textContent()).includes('Test responses'));
  delay=true;await page.locator('#scope').selectOption('test');await oldStarted;
  assert(await page.locator('#download').isDisabled());
  await page.locator('#source').selectOption('direct');await page.waitForFunction(()=>document.querySelector('#started').textContent==='2');
  const oldResponse=page.waitForResponse(r=>r.url().includes('source=all')&&r.url().includes('scope=test'));release();await oldResponse;await page.waitForLoadState('networkidle');
  assert.equal(await page.locator('#started').textContent(),'2');assert((await page.locator('#answers').textContent()).includes('Your suggestions'));assert((await page.locator('#rows').textContent()).includes('Your experience'));
  const [download]=await Promise.all([page.waitForEvent('download'),page.locator('#download').click()]);
  const csv=fs.readFileSync(await download.path(),'utf8');assert(csv.startsWith('\ufeff'));assert(csv.includes('\"completed_at\"'));assert(csv.includes('2026-10-25T09:08:25.169Z'));assert(csv.includes("'=1+1"));assert(csv.includes('"-5"'));assert(csv.includes('custom_budget.a'));assert(csv.includes('"40"'));assert(csv.includes('unanswered'));assert(csv.includes('answer.source'));assert(csv.includes('A colleague'));assert.equal(csv.split('\r\n')[0].split(',').filter(c=>c==='"source"').length,1);assert(download.suggestedFilename().includes('test-direct'));
  fail=true;await page.locator('#refresh').click();await page.waitForFunction(()=>document.querySelector('#status').textContent==='Could not load results');assert(await page.locator('#download').isDisabled());assert((await page.locator('#view-note').textContent()).includes('Previous figures may be out of date'));
  fail=false;delay=false;await page.locator('#refresh').click();await page.waitForFunction(()=>!document.querySelector('#download').disabled);
 }finally{await browser.close();await new Promise(r=>server.close(r));}
});
