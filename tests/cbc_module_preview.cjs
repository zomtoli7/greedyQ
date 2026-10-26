/* Account-free ordinary survey + one CBC module in both independent preview panes. */
'use strict';
const fs=require('fs'),http=require('http'),path=require('path'),assert=require('assert/strict');
const{chromium}=require('playwright');let browser,server;
(async()=>{const file=path.join(process.argv[2],'preview.html');server=http.createServer((_,res)=>{res.setHeader('content-type','text/html; charset=utf-8');res.end(fs.readFileSync(file))});await new Promise(r=>server.listen(0,'localhost',r));browser=await chromium.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});const page=await browser.newPage({viewport:{width:390,height:850}}),errors=[],blocked=[];page.on('pageerror',e=>errors.push(e.message));await page.route('**/*',r=>new URL(r.request().url()).hostname==='localhost'?r.continue():(blocked.push(r.request().url()),r.abort()));await page.goto('http://localhost:'+server.address().port);await page.locator('#desktop [data-consent="accepted"]').waitFor();
 for(const id of ['desktop','mobile']){
  const root=page.locator('#'+id);await root.locator('[data-consent="accepted"]').click();await root.locator('input[type=number]').waitFor();await root.locator('[data-next]').click();await root.locator('[data-question-error]').waitFor();await root.locator('input[type=number]').fill('3');await root.locator('input[type=number]').dispatchEvent('change');
  async function next(){const revision=await page.evaluate(id=>controllers[id].state.state.revision,id);await root.locator('[data-next]').click();await page.waitForFunction(({id,revision})=>controllers[id].state.state.revision>revision,{id,revision});}
  await next();await root.getByRole('heading',{name:'Your usual preference'}).waitFor();await root.locator('input[type=radio]').first().check();await next();await root.locator('fieldset').waitFor();
  assert.equal(await root.locator('[data-cbc-orientation]').getAttribute('data-cbc-orientation'),id==='desktop'?'horizontal':'vertical');
  for(let i=0;i<4;i++){await root.locator('input[value="none"]').check();await next();}
  await root.getByRole('heading',{name:'After the choices'}).waitFor();await root.locator('[data-next]').click();await root.locator('[data-question-error]').waitFor();await root.locator('input[type=radio][value="8"]').check();await next();await root.getByRole('heading',{name:'Thank you. Your answers have been saved.',exact:true}).waitFor();
 }
 await page.locator('#structure').click();assert(await page.locator('#structure-dialog').isVisible());assert((await page.locator('#structure-list').textContent()).includes('CBC module'));assert.deepEqual(errors,[]);assert.equal(blocked.length,0);console.log('PASS integrated offline dual preview, module layout at phone viewport, validation, independent sessions and structure');
})().catch(e=>{console.error(e);process.exitCode=1}).finally(async()=>{await browser?.close();await new Promise(r=>server?server.close(r):r())});
