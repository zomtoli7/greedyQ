/* Synthetic browser checks. No external response submission. */
const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),os=require('node:os');
const {chromium}=require('/Users/dongsookim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'..');
test('desktop/mobile option and page orders survive answers, back and reload',async()=>{
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'gq-order-')),browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try {
  const q=id=>({id,type:'mc',label:id,required:true,options:[{label:'A',value:'a'},{label:'B',value:'b'},{label:'Other',value:'other'}],shuffle_items:['a','b']});
  const model={study_id:'ordering',study_version:'draft',title:'Ordering',start_page:'opening',conditions:['default'],messages:{next:'Next',previous:'Previous',required:'Required'},shuffle_pages:['first','second'],pages:[{id:'opening',title:'Opening',questions:[],next:'first'},{id:'first',title:'First',questions:[q('first_answer')],next:'second'},{id:'second',title:'Second',questions:[q('second_answer')],next:'ending'},{id:'ending',title:'Ending',questions:[],terminal:'completed',redirect:{url:'https://example.test/return',params:{},newtab:false,delay:0,label:'Return'}}]};
  const html=path.join(tmp,'index.html');
  fs.writeFileSync(html,`<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><div id="root"></div><script src="file://${root}/web/greedyq-core.js"></script><script>const model=${JSON.stringify(model)};const backend=greedyQ.createLocalMockBackend('ordering');window.controller=greedyQ.mountRespondent(document.getElementById('root'),model,{backend,sessionId:'one'});</script>`);
  for(const width of [390,1280]) {
   const context=await browser.newContext({viewport:{width,height:800}}),page=await context.newPage(),errors=[];
   page.on('pageerror',e=>errors.push(e.message));await page.goto('file://'+html);
   assert.deepEqual(errors,[]);
   const expected=await page.evaluate(()=>controller.state.page_order);
   await page.getByRole('button',{name:'Next',exact:true}).click();await page.locator('[data-q]').waitFor();
   const first=await page.locator('[data-q]').getAttribute('data-q'),order=await page.locator('input[type=radio]').evaluateAll(es=>es.map(e=>e.value));
   assert.equal(order.at(-1),'other');assert.deepEqual([...order].sort(),['a','b','other']);
   await page.getByRole('radio',{name:'B',exact:true}).check();await page.reload();
   assert.deepEqual(await page.locator('input[type=radio]').evaluateAll(es=>es.map(e=>e.value)),order);
   assert.equal(await page.getByRole('radio',{name:'B',exact:true}).isChecked(),true);
   assert.deepEqual(await page.evaluate(()=>controller.state.page_order),expected);
   await page.getByRole('button',{name:'Next',exact:true}).click();await page.locator(`[data-q]:not([data-q="${first}"])`).waitFor();
   await page.getByRole('button',{name:'Previous',exact:true}).click();assert.equal(await page.locator('[data-q]').getAttribute('data-q'),first);
   await page.getByRole('button',{name:'Next',exact:true}).click();await page.getByRole('radio',{name:'A',exact:true}).check();await page.getByRole('button',{name:'Next',exact:true}).click();
   await page.getByRole('heading',{name:'Ending',exact:true}).waitFor();assert.equal(await page.locator('[data-redirect]').isDisabled(),true);
   assert.ok(page.url().startsWith('file:'));assert.deepEqual(errors,[]);await context.close();
  }
 } finally {await browser.close();fs.rmSync(tmp,{recursive:true,force:true});}
});

test('conditional page bypass, stop checks and compound same-page visibility',async()=>{
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try {
  const page=await browser.newPage();await page.setContent('<div id="root"></div>');await page.addScriptTag({path:path.join(root,'web/greedyq-core.js')});
  await page.evaluate(()=>{
   const model={study_id:'rules',title:'Rules',start_page:'start',conditions:['default'],messages:{next:'Next',previous:'Previous',required:'Required'},pages:[
    {id:'start',title:'Start',next:'conditional',questions:[{id:'amount',type:'numeric',label:'Amount',required:true},{id:'follow',type:'text',label:'Follow-up',show_if:{all:[{field:'amount',answered:true},{field:'amount',gt:0}]}}],checks:[{when:{field:'amount',gt:10},message:'Use at most ten'}]},
    {id:'conditional',title:'Should be skipped',questions:[],show_if:{field:'amount',gt:10},next:'end'},
    {id:'end',title:'Finished',questions:[],terminal:'completed'}]};
   window.controller=greedyQ.mountRespondent(document.getElementById('root'),model);
  });
  assert.equal(await page.getByText('Follow-up',{exact:true}).count(),0);
  await page.locator('[data-id="amount"]').fill('12');await page.locator('[data-id="amount"]').press('Tab');
  await page.getByText('Follow-up',{exact:true}).waitFor();await page.getByRole('button',{name:'Next',exact:true}).click();
  await page.getByText('Use at most ten',{exact:true}).waitFor();assert.equal(await page.evaluate(()=>controller.state.page),'start');
  await page.locator('[data-id="amount"]').fill('2');await page.locator('[data-id="amount"]').press('Tab');await page.getByRole('button',{name:'Next',exact:true}).click();
  await page.getByRole('heading',{name:'Finished',exact:true}).waitFor();assert.deepEqual(await page.evaluate(()=>controller.state.visited),['start','end']);
 }finally{await browser.close();}
});

test('return links stay disabled on failed save and navigate only after successful save',async()=>{
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try{
  const page=await browser.newPage();await page.setContent('<div id="root"></div>');await page.addScriptTag({path:path.join(root,'web/greedyq-core.js')});
  await page.evaluate(()=>{
   window.model={study_id:'return',title:'Return',start_page:'end',conditions:['default'],messages:{},pages:[{id:'end',title:'Done',questions:[],terminal:'completed',redirect:{url:'https://example.test/return',params:{},newtab:false,delay:null,label:'Return'}}]};
   const backend=greedyQ.createMemoryBackend();backend.save=()=>Promise.reject(new Error('synthetic failed save'));
   greedyQ.mountRespondent(document.getElementById('root'),model,{backend,allowExternalRedirects:true});
  });
  await page.getByText('Response not saved. Please retry before leaving.',{exact:true}).waitFor();assert.equal(await page.locator('[data-redirect]').isDisabled(),true);
  await page.route('https://example.test/**',route=>route.fulfill({status:200,body:'Synthetic return destination'}));
  await page.evaluate(()=>greedyQ.mountRespondent(document.getElementById('root'),model,{allowExternalRedirects:true}));
  await page.getByRole('button',{name:'Return',exact:true}).click();await page.waitForURL('https://example.test/return');
 }finally{await browser.close();}
});
