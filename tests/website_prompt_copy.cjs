/* Exhaustive prompt-copy audit: three languages, all pages, all copy paths. */
const{test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const{chromium}=require('/Users/dongsookim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root=path.resolve(__dirname,'..'),entry='https://greedyq.netlify.app/';
async function setup(){const server=http.createServer((req,res)=>{res.setHeader('content-type','text/html; charset=utf-8');res.end(fs.readFileSync(path.join(root,'website/google-sites-embed.html')));});await new Promise(r=>server.listen(0,'localhost',r));const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});return{server,browser,base:'http://localhost:'+server.address().port};}
const urls=text=>[...text.matchAll(/https?:\/\/[^\s<>"{}]+/g)].map(m=>m[0]);
function check(text,kind,route="start"){assert(text.length);assert.equal(text.includes('\r'),false);if(kind==='code')return;for(const line of text.split('\n').slice(1,-1))assert(line.startsWith(' ')&&line.endsWith(' '),'Each line needs explicit ASCII separation');const flattened=text.replace(/[\n\u2028\u2029]/g,'');for(const url of urls(text))assert(flattened.includes('<'+url+'>'),'URL must remain delimited when line breaks disappear');assert(!flattened.includes('START-HERE.md새'));if(!route.startsWith('about/'))assert(urls(text).includes(entry),'Every researcher request must use the public start URL: '+text.slice(0,180));assert(!urls(text).some(u=>u.includes('github.com/')&&u.endsWith('/START-HERE.md')));}
test('all website example blocks copy exact plain text without joining URLs, at phone and computer widths',async()=>{
 const{server,browser,base}=await setup(),source=JSON.parse(fs.readFileSync(path.join(root,'website/content.json')));let count=0,code=0;
 try{for(const width of [320,1280])for(const language of ['en','ko','zh']){
  const page=await browser.newPage({viewport:{width,height:900}});await page.route('**/*',r=>new URL(r.request().url()).hostname==='localhost'?r.continue():r.abort());await page.addInitScript(()=>{window.syntheticClipboard='';Object.defineProperty(navigator,'clipboard',{value:{writeText:async text=>{window.syntheticClipboard=text;}}});document.execCommand=()=>{throw Error('Modern clipboard must be preferred');};});
  const data=source[language],routes=['home','start',...data.guide.map(p=>'guide/'+p.id),'guide/prolific',...data.about.map(p=>'about/'+p.id),'examples'];
  for(const route of [...new Set(routes)]){await page.goto(base+'#'+language+'/'+route);await page.locator('main').waitFor();const blocks=page.locator('.prompt');for(let i=0;i<await blocks.count();i++){
   const block=blocks.nth(i),text=await block.locator('pre').textContent(),kind=await block.getAttribute('data-copy-kind');check(text,kind,route);await block.locator('.copy').click();await page.waitForFunction(value=>window.syntheticClipboard===value,text);assert.equal(await page.evaluate(()=>window.syntheticClipboard),text);if(kind==='code'){code++;assert(text.includes('@article{hu2025surveydown'));assert(text.includes('url = {https://github.com/zomtoli7/greedyQ}'));}count++;
  }}await page.close();
 }assert(count>=100,'Audit must cover all generated control and guide prompt blocks');assert.equal(code,6);
 console.log(JSON.stringify({prompt_blocks_checked:count,code_blocks_preserved:code,languages:3,widths:[320,1280],newline_loss_urls_preserved:true}));
 }finally{await browser.close();await new Promise(r=>server.close(r));}
});
test('legacy fallback and manual selection emit text/plain only, retaining line boundaries and literal URL delimiters',async()=>{
 const{server,browser,base}=await setup();try{for(const method of ['legacy','manual'])for(const language of ['en','ko','zh']){
  const page=await browser.newPage();await page.addInitScript(method=>{window.syntheticCopy=null;Object.defineProperty(navigator,'clipboard',{value:{writeText:async()=>{throw Error('Restricted embed');}}});document.execCommand=()=>{if(method==='manual')return false;const data=new DataTransfer();document.dispatchEvent(new ClipboardEvent('copy',{clipboardData:data,cancelable:true}));window.syntheticCopy={plain:data.getData('text/plain'),html:data.getData('text/html')};return true;};},method);
  await page.goto(base+'#'+language+'/start');const text=await page.locator('.prompt pre').textContent();await page.locator('.copy').click();if(method==='manual'){
   await page.waitForFunction(()=>getSelection().toString().includes('https://greedyq.netlify.app/'));await page.locator('.prompt pre').evaluate(()=>{const data=new DataTransfer();document.dispatchEvent(new ClipboardEvent('copy',{clipboardData:data,cancelable:true}));window.syntheticCopy={plain:data.getData('text/plain'),html:data.getData('text/html')};});
  }await page.waitForFunction(()=>window.syntheticCopy!==null);const captured=await page.evaluate(()=>window.syntheticCopy);assert.equal(captured.plain,text);assert.equal(captured.html,'');check(captured.plain,'prompt');await page.close();
 }}finally{await browser.close();await new Promise(r=>server.close(r));}
});
