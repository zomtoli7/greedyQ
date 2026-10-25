const {test}=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const {chromium}=require('/Users/dongsookim/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
test('website Collect order, previous/next, three languages, mobile menu and full history',async()=>{
 const root=path.resolve(__dirname,'../website');
 const server=http.createServer((req,res)=>{const name=req.url.split('?')[0].split('#')[0].split('/').at(-1);if(!['google-sites-embed.html','copy-embed.html'].includes(name)){res.statusCode=404;return res.end();}res.setHeader('content-type','text/html; charset=utf-8');res.end(fs.readFileSync(path.join(root,name)));});await new Promise(r=>server.listen(0,'localhost',r));
 const browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
 try{for(const width of [390,1280])for(const language of ['en','ko','zh']){
  const page=await browser.newPage({viewport:{width,height:900}}),base=`http://localhost:${server.address().port}/google-sites-embed.html`;
  await page.goto(base+'#'+language+'/guide/prolific');await page.locator('h1').waitFor();assert.equal(await page.locator('.side-link.active').getAttribute('data-topic'),'prolific');
  const pager=page.locator('.pager button');assert.equal(await pager.nth(0).getAttribute('data-topic'),'deploy');assert.equal(await pager.nth(1).getAttribute('data-topic'),'results');
  await pager.nth(0).click();assert(page.url().endsWith('/guide/deploy'));await page.locator('.pager button[data-topic=prolific]').click();await page.locator('.pager button[data-topic=results]').click();assert(page.url().endsWith('/guide/results'));
  await page.locator('#language').selectOption(language==='en'?'ko':'en');assert(page.url().endsWith('/guide/results'));
  if(width===390){await page.locator('.toc-toggle').click();assert((await page.locator('.sidebar').getAttribute('class')).includes('open'));}
  await page.goto(base+'#'+language+'/about/updates');assert(await page.locator('.history li').count()>=11);assert((await page.locator('.footer').textContent()).includes('0.2_'));
  await page.close();
 }
 const helper=await browser.newPage();await helper.goto(`http://localhost:${server.address().port}/copy-embed.html`);await helper.waitForFunction(()=>!document.getElementById('copy').disabled);assert.equal(await helper.locator('#source').inputValue(),fs.readFileSync(path.join(root,'google-sites-embed.html'),'utf8'));
 }finally{await browser.close();await new Promise(r=>server.close(r));}
});
