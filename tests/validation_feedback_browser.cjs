const {test}=require('node:test'),assert=require('node:assert/strict'),path=require('node:path');
const {chromium}=require('/Users/dongsookim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'..');
test('question feedback, focus, sum signaling, hints and preview-only timing at both widths',async()=>{
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try{for(const width of [390,1280]){
  const page=await browser.newPage({viewport:{width,height:650}});await page.setContent('<div id="root"></div>');await page.addStyleTag({path:path.join(root,'web/greedyq-runtime.css')});await page.addScriptTag({path:path.join(root,'web/greedyq-core.js')});
  await page.evaluate(()=>{window.model={study_id:'feedback',title:'Feedback',start_page:'start',conditions:['default'],messages:{next:'Next',required:'Please answer this question.',previous:'Previous'},pages:[{id:'start',title:'Start',next:'end',questions:[{id:'name',type:'text',label:'Name',required:true},{id:'budget',type:'constant_sum',label:'Budget',total:100,options:[{label:'A',value:'a'},{label:'B',value:'b'}]},{id:'many',type:'mc_multiple_buttons',label:'Services',options:[{label:'Mail',value:'mail'}]},{id:'hidden_hint',type:'mc_multiple',label:'No hint',selection_hint:false,options:[{label:'Other',value:'other'}]},{id:'clock',type:'timing',label:'Timing'}]},{id:'end',title:'Done',terminal:'completed',questions:[]}]};window.controller=greedyQ.mountRespondent(document.getElementById('root'),model,{preview:true});});
  assert.equal(await page.locator('.gq-selection-hint').count(),1);
  assert.equal(await page.locator('.gq-total-warning').count(),1);
  const start=await page.locator('[data-timing-preview]').textContent();await page.waitForFunction(old=>document.querySelector('[data-timing-preview]').textContent!==old,start);
  await page.getByRole('button',{name:'Next',exact:true}).click();assert.equal(await page.locator('[data-question-error]').count(),2);
  assert.equal(await page.evaluate(()=>document.activeElement.dataset.q),'name');
  assert.equal(await page.locator('[data-q="name"]').evaluate(e=>e.previousElementSibling.hasAttribute('data-question-error')),true);
  await page.locator('[data-id="name"]').fill('Synthetic');assert.equal(await page.locator('[data-question-error]').count(),1);
  await page.locator('[data-constant-item="a"]').fill('101');assert.equal(await page.locator('.gq-total-warning').count(),1);
  await page.locator('[data-constant-item="a"]').fill('100');assert.equal(await page.locator('.gq-total-warning').count(),0);assert.equal(await page.locator('[data-question-error]').count(),0);
  await page.getByRole('button',{name:'Next',exact:true}).click();await page.getByRole('heading',{name:'Done',exact:true}).waitFor();
  await page.evaluate(()=>{controller=greedyQ.mountRespondent(document.getElementById('root'),model,{preview:false});});assert.equal(await page.locator('[data-timing-preview]').count(),0);assert.equal(await page.locator('[data-q="clock"]').isVisible(),false);
  await page.close();
 }}finally{await browser.close();}
});
