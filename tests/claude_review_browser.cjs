const {test}=require('node:test'),assert=require('node:assert/strict'),path=require('node:path');
const {chromium}=require('/Users/dongsookim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'..');
for(const width of [390,1280])test(`required and optional sliders, explicit defaults and same-page Other at ${width}px`,async()=>{
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try{
  const page=await browser.newPage({viewport:{width,height:720}});await page.setContent('<div id="root"></div>');await page.addStyleTag({path:path.join(root,'web/greedyq-runtime.css')});await page.addScriptTag({path:path.join(root,'web/greedyq-core.js')});
  await page.evaluate(()=>{window.model={study_id:'slider_review',language:'ko',title:'Review',messages:{next:'계속하기',previous:'이전',required:'필수 문항입니다.'},start_page:'start',conditions:['default'],pages:[{id:'start',title:'Start',next:'end',questions:[{id:'score',type:'slider_numeric',label:'Required slider',required:true,min:0,max:10,step:1},{id:'optional',type:'slider_numeric',label:'Optional slider',min:0,max:10,step:1},{id:'preset',type:'slider_numeric',label:'Explicit default',min:0,max:10,step:1,default:3},{id:'tools',type:'mc_multiple',label:'Tools',options:[{label:'Other',value:'other'},{label:'GPT',value:'gpt'}]},{id:'other',type:'text',label:'Describe other',show_if:{field:'tools',contains:'other'}}]},{id:'end',title:'Done',terminal:'completed',questions:[]}]};window.controller=greedyQ.mountRespondent(document.getElementById('root'),model,{preview:true});});
  await page.getByRole('button',{name:'계속하기',exact:true}).click();assert.equal(await page.locator('[data-question-error]').count(),1);assert.equal(await page.evaluate(()=>Object.hasOwn(controller.state.answers,'score')),false);assert.equal(await page.evaluate(()=>Object.hasOwn(controller.state.answers,'optional')),false);
  assert.equal(await page.locator('[data-q="other"]').isVisible(),false);
  await page.getByLabel('Other',{exact:true}).check();await page.locator('[data-q="other"]').waitFor({state:'visible'});
  await page.getByLabel('Other',{exact:true}).uncheck();assert.equal(await page.locator('[data-q="other"]').isVisible(),false);
  const range=page.locator('input[type=range][data-id="score"]');await range.focus();await range.press('ArrowRight');
  await page.getByRole('button',{name:'계속하기',exact:true}).click();await page.getByRole('heading',{name:'Done',exact:true}).waitFor();
  const answers=await page.evaluate(()=>controller.state.answers);assert.equal(typeof answers.score,'number');assert.equal(answers.preset,3);assert.equal(Object.hasOwn(answers,'optional'),false);
 }finally{await browser.close();}
});
test('new Korean draft preserves title/language, exposes mock warning and localizes preview tools',async()=>{
 const fs=require('node:fs'),os=require('node:os'),cp=require('node:child_process'),base=fs.mkdtempSync(path.join(os.tmpdir(),'greedyq-review-')),study=path.join(base,'study');
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try{
  cp.execFileSync('python3',['-m','greedyq','init',study,'--id','review_screen','--profile','simple','--language','ko','--title','Korean study title'],{cwd:root});
  const page=await browser.newPage({viewport:{width:390,height:720}});await page.goto('file://'+path.join(study,'index.html'));await page.locator('#survey .gq-card').waitFor();assert.equal(await page.title(),'Korean study title');assert.equal(await page.locator('html').getAttribute('lang'),'ko');assert.equal(await page.locator('#local-preview-banner').isVisible(),true);assert.match(await page.locator('#local-preview-banner').textContent(),/연구자에게 전달되지/);
  await page.goto('file://'+path.join(study,'preview.html'));await page.getByRole('button',{name:'구조 보기',exact:true}).click();assert.equal(await page.getByRole('heading',{name:'설문 구조',exact:true}).isVisible(),true);assert.equal(await page.getByLabel('컴퓨터 페이지',{exact:true}).count(),1);
  const layout=await page.locator('#mobile').evaluate(el=>({width:el.getBoundingClientRect().width,lang:el.lang}));assert(layout.width<=390);assert.equal(layout.lang,'ko');
 }finally{await browser.close();fs.rmSync(base,{recursive:true,force:true});}
});
