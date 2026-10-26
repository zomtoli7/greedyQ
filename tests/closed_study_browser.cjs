/* Canonical participant page: explicit closure is not a network/save error. */
const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const {chromium}=require('/Users/dongsookim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'..');
test('closed study screen for new and active respondents in four languages on desktop/mobile; network errors stay distinct',async()=>{
 const template=fs.readFileSync(path.join(root,'templates/browser/respondent.html'),'utf8');
 const model={study_id:'closed_fixture',study_version:'test',greedyq_version:'fixture',title:'Closure test',start_page:'welcome',conditions:['default'],messages:{next:'Next',previous:'Previous'},runtime_policy:{mode:'test'},pages:[{id:'welcome',title:'Welcome',next:'end',questions:[]},{id:'end',title:'End',questions:[],terminal:'completed'}]};
 let language='en',stage='create',network=false;
 const server=http.createServer((req,res)=>{
  const name=req.url.split('?')[0].slice(1);
  if(['greedyq-core.js','greedyq-runtime.css'].includes(name)){res.setHeader('content-type',name.endsWith('.js')?'text/javascript':'text/css');return res.end(fs.readFileSync(path.join(root,'web',name)));}
  const html=template.replace(/(<script id="greedyq-model"[^>]*>)[\s\S]*?(<\/script>)/,(_,a,b)=>a+JSON.stringify({...model,language})+b).replace(/(<script id="greedyq-deployment"[^>]*>)[\s\S]*?(<\/script>)/,(_,a,b)=>a+JSON.stringify({mode:'supabase',supabase_url:'https://closed.supabase.test',supabase_anon_key:'synthetic_public_key'})+b);
  res.setHeader('content-type','text/html; charset=utf-8');res.end(html);
 });await new Promise(r=>server.listen(0,'localhost',r));
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 try{
  for(language of ['en','ko','zh-CN','zh-TW'])for(const width of [390,1280])for(stage of ['create','save']){
   const context=await browser.newContext({viewport:{width,height:800}});const page=await context.newPage();let called=0;
   await page.route('https://closed.supabase.test/**',route=>{
    const name=route.request().url().split('/').at(-1);called++;
    if((stage==='create'&&name==='greedyq_create_session')||(stage==='save'&&name==='greedyq_save_session'))return route.fulfill({status:400,json:{message:'This study is closed for archiving'}});
    if(name==='greedyq_resume_session')return route.fulfill({json:{runtime_contract:'randomization-1',registered_model:{...model,language},state:null}});
    return route.fulfill({status:200,json:null});
   });
   await page.goto('http://localhost:'+server.address().port+'/');
   const heading={'en':'Survey closed','ko':'설문이 종료되었습니다','zh-CN':'问卷已关闭','zh-TW':'問卷已關閉'}[language];
   await page.getByRole('heading',{name:heading,exact:true}).waitFor();
   assert.equal(await page.locator('[data-next],[data-back],[data-save-error]').count(),0);assert(called>0);
   assert.doesNotMatch(await page.locator('#survey').innerText(),/could not be saved|secure data connection|연결을 확인/);await context.close();
  }
  language='en';stage='create';network=true;
  const p=await browser.newPage();await p.route('https://closed.supabase.test/**',r=>r.fulfill({status:503,json:{message:'Temporary database issue'}}));await p.goto('http://localhost:'+server.address().port+'/');await p.getByRole('heading',{name:'Survey unavailable',exact:true}).waitFor();assert.equal(await p.getByRole('heading',{name:'Survey closed',exact:true}).count(),0);
 }finally{await browser.close();await new Promise(r=>server.close(r));}
});
