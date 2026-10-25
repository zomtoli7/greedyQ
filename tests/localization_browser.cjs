const {test}=require('node:test'),assert=require('node:assert/strict'),path=require('node:path');
const {chromium}=require('/Users/dongsookim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
test('Chinese participant UI includes errors, hints, controls, completion and preserves values',async()=>{
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try{for(const language of ['zh-CN','zh-TW'])for(const width of [390,1280]){
  const page=await browser.newPage({viewport:{width,height:750}});const errors=[];page.on('pageerror',e=>errors.push(e.message));await page.setContent('<meta charset="utf-8"><div id="root"></div>');await page.addScriptTag({path:path.resolve(__dirname,'../web/greedyq-core.js')});
  await page.evaluate(language=>{const t=m=>greedyQ.translate(language,m);window.controller=greedyQ.mountRespondent(document.getElementById('root'),{language,study_id:'language',title:'问卷',organization:'研究者',start_page:'start',conditions:['default'],messages:{next:t('Continue'),previous:t('Previous'),required:t('Please answer the required questions before continuing.')},pages:[{id:'start',title:'开始',next:'end',questions:[{id:'answer',type:'text',label:'回答',required:true},{id:'sum',type:'constant_sum',label:'分配',total:100,options:[{label:'甲',value:'a'}]},{id:'many',type:'mc_multiple_buttons',label:'多选',options:[{label:'乙',value:'b'}]},{id:'choose',type:'select',label:'选择',options:[{label:'丙',value:'c'}]},{id:'nps',type:'nps',label:'推荐'}]},{id:'end',title:'结束',questions:[],terminal:'completed'}]});},language);
  assert.equal(await page.locator('#root').getAttribute('lang'),language);
  await page.locator('[data-next]').click();assert.equal(await page.locator('[data-question-error]').count(),2);assert.equal(await page.evaluate(()=>document.activeElement.dataset.q),'answer');
  assert.doesNotMatch(await page.locator('#root').innerText(),/Please|Continue|Select all|allocation|Choose|likely|completed/);
  await page.locator('[data-id="answer"]').fill('测试');await page.locator('[data-constant-item]').fill('100');await page.getByRole('checkbox').check();await page.locator('[data-next]').click();
  assert.equal(await page.evaluate(()=>controller.state.answers.many[0]),'b');assert.equal(await page.locator('.gq-actions strong').textContent(),'作答完成');assert.deepEqual(errors,[]);await page.close();
 }}finally{await browser.close();}
});
