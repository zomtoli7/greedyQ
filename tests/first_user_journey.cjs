/* Disposable browser → canonical RPCs → PostgreSQL → results → archive journey.
   The only provider is a local fake; no cloud credentials or network are used. */
const assert = require('node:assert/strict');
const fs = require('node:fs'), path = require('node:path'), http = require('node:http');
const {spawnSync} = require('node:child_process');
const {pathToFileURL} = require('node:url');
const {chromium} = require('playwright');
const {Client} = require(process.env.GREEDYQ_PG_MODULE || 'pg');
const ops = require('../tools/cloud_lifecycle.cjs');
const results = require('../templates/vercel/api/results.js');
const repo = path.resolve(__dirname, '..'), study = process.argv[2];
const model = JSON.parse(fs.readFileSync(path.join(study, 'preview-model.json')));
const connection = {host:process.env.PGHOST, port:Number(process.env.PGPORT), database:'postgres'};
const client = new Client(connection);
// Keep participant RLS calls on their own connection; SET ROLE must never
// leak into administrative assertions when an autosave is still in flight.
const respondentClient = new Client(connection);
const quote = value => "'" + String(value).replaceAll("'", "''") + "'";
let browser, server;
let rpcQueue=Promise.resolve();
async function rpc(name, body) {
  assert.match(name, /^greedyq_[a-z_]+$/);
  const signature = (await client.query(`SELECT proargnames, ARRAY(SELECT format_type(t,NULL) FROM unnest(proargtypes) t) types FROM pg_proc WHERE pronamespace='public'::regnamespace AND proname=$1`, [name])).rows;
  assert.equal(signature.length,1);
  const {proargnames, types} = signature[0];
  const args = Object.entries(body).map(([key,value]) => {
    const i=proargnames.indexOf(key); assert(i>=0);
    const encoded = value==null ? 'NULL' : quote(typeof value==='object' ? JSON.stringify(value) : value);
    return `${key} => ${encoded}::${types[i]}`;
  });
  return (await respondentClient.query(`SELECT to_json(public.${name}(${args.join(',')})) value`)).rows[0].value;
}
// Exercise the real results handler through a local PostgREST-shaped adapter.
async function databaseFetch(input) {
  const url=new URL(input); assert.equal(url.hostname,'journey.supabase.test');
  const table=url.pathname.split('/').at(-1);
  assert(['gq_sessions','gq_answers','gq_assignments','gq_external_identifiers'].includes(table));
  const columns=url.searchParams.get('select').split(',');columns.forEach(c=>assert.match(c,/^[a-z_]+$/));
  const values=[], where=[];
  for(const [key,value] of url.searchParams) {
    if(['select','order','limit','offset'].includes(key))continue;
    assert(['study_id','is_test','respondent_source','session_id'].includes(key));
    if(value.startsWith('eq.')) { values.push(value.slice(3)); where.push(`${key}=$${values.length}`); }
    else { assert(value.startsWith('in.(')&&value.endsWith(')'));const ids=value.slice(4,-1).split(',');where.push('session_id IN ('+ids.map(id=>{values.push(id);return '$'+values.length;}).join(',')+')'); }
  }
  const rows=(await client.query(`SELECT ${columns.join(',')} FROM public.${table}${where.length?' WHERE '+where.join(' AND '):''}`,values)).rows;
  return {ok:true,json:async()=>rows.slice(Number(url.searchParams.get('offset')||0),Number(url.searchParams.get('offset')||0)+Number(url.searchParams.get('limit')||1000))};
}
async function main() {
  await client.connect();
  await respondentClient.connect();
  await respondentClient.query('SET ROLE anon');
  await ops.registerStudy(client,model);
  const bundles=path.join(study,'bundles');
  ops.prepareDeployments({repo,model,directory:bundles,url:'https://journey.supabase.test',publishableKey:'sb_publishable_imaginary'});
  global.fetch=databaseFetch;
  process.env.SUPABASE_URL='https://journey.supabase.test';process.env.SUPABASE_SECRET_KEY='synthetic_server_key';
  server=http.createServer(async(req,res)=>{
    try {
      const url=new URL(req.url,'http://localhost');
      if(url.pathname==='/api/results') {req.query=Object.fromEntries(url.searchParams);return await results(req,res);}
      const dashboard=url.pathname.startsWith('/results');
      const name=url.pathname==='/'||url.pathname==='/results' ? 'index.html' : url.pathname.slice(1);
      if(!/^[a-zA-Z0-9_.-]+$/.test(name)){res.writeHead(404);return res.end();}
      const directory=['preview.html','studio.html'].includes(name)?study:path.join(bundles,dashboard?'results':'survey');
      const file=path.join(directory,name);
      if(!fs.existsSync(file)){res.writeHead(404);return res.end();}
      res.setHeader('content-type',name.endsWith('.js')?'text/javascript':name.endsWith('.css')?'text/css':'text/html; charset=utf-8');
      res.end(fs.readFileSync(file));
    }catch(error){res.writeHead(500);res.end(error.message);}
  });
  await new Promise(r=>server.listen(0,'localhost',r));
  const base=`http://localhost:${server.address().port}`;
  browser=await chromium.launch({executablePath:process.env.GREEDYQ_CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:true});
  // Follow the downloaded-folder instructions with file:// and no local server.
  for(const width of [320,390,1280]){
    const page=await browser.newPage({viewport:{width,height:850}});
    await page.goto(pathToFileURL(path.join(study,'preview.html')).href);
    await page.locator('#desktop').getByRole('heading',{name:'Welcome',exact:true}).waitFor();
    await page.locator('#mobile').getByRole('heading',{name:'Welcome',exact:true}).waitFor();
    await page.goto(pathToFileURL(path.join(study,'studio.html')).href);
    await page.locator('#build').click();assert((await page.locator('#status').textContent()).includes('Choose survey.qmd'));
    await page.locator('#qmd').setInputFiles(path.join(study,'survey.qmd'));await page.locator('#yml').setInputFiles(path.join(study,'greedyq.yml'));
    await page.locator('#build').click();await page.locator('#desktop').getByRole('heading',{name:'Welcome',exact:true}).waitFor();
    assert((await page.locator('#status').textContent()).includes('Your preview is ready'));
    const dimensions=await page.evaluate(()=>({desktop:document.querySelector('#desktop').getBoundingClientRect().width,mobile:document.querySelector('#mobile').getBoundingClientRect().width,page:document.documentElement.scrollWidth,view:document.documentElement.clientWidth}));
    assert(dimensions.desktop>=900);assert(dimensions.mobile<=390);assert(dimensions.page<=dimensions.view+1,JSON.stringify(dimensions));
    await page.locator('#qmd').setInputFiles({name:'survey.qmd',mimeType:'text/plain',buffer:Buffer.from('invalid survey')});await page.locator('#build').click();assert.equal(await page.locator('#preview').isVisible(),false);
    await page.close();
  }
  const blocked=[],errors=[];
  async function participant(width=1280) {
    const context=await browser.newContext({viewport:{width,height:850}});
    await context.route('**/*',async route=>{
      const request=route.request(),u=new URL(request.url());
      if(u.hostname==='localhost')return route.continue();
      if(u.hostname!=='journey.supabase.test') {blocked.push(u.href);return route.abort();}
      try { const pending=rpcQueue.then(()=>rpc(u.pathname.split('/').at(-1),request.postDataJSON()));rpcQueue=pending.catch(()=>{});const data=await pending;await route.fulfill({status:200,contentType:'application/json',body:JSON.stringify(data)}); }
      catch(error){await route.fulfill({status:400,contentType:'application/json',body:JSON.stringify({message:error.message})});}
    });
    const page=await context.newPage();page.on('pageerror',e=>errors.push(e.message));await page.goto(base);
    await page.getByRole('heading',{name:'Welcome',exact:true}).waitFor();
    return {page,context};
  }
  const next=page=>page.locator('#survey [data-next]').click();
  async function consent(page,answer='yes') {
    await page.getByRole('button',{name:'Start',exact:true}).click();
    await page.locator(`[name=consent_choice][value=${answer}]`).check();await next(page);
  }
  async function feedback(page,comment='Synthetic feedback') {
    await consent(page);await page.locator('label').filter({has:page.locator('[name=used_service][value=yes]')}).click();await next(page);
    await page.locator('[name=rating][value="4"]').check();
    await page.locator('[name=had_problem][value=yes]').check();
    await page.locator('[data-id=problem_detail]').fill('Imaginary problem');
    await page.locator('[name=had_problem][value=no]').check();
    assert.equal(await page.locator('[data-q=problem_detail]').count(),0);
    await page.locator('[data-id=comment]').fill(comment);await next(page);
    await page.getByRole('heading',{name:'Finish your participation',exact:true}).waitFor();
  }
  const a=await participant();await consent(a.page,'no');await a.page.getByRole('heading',{name:'Participation declined',exact:true}).waitFor();assert.equal(await a.page.locator('[data-back]').count(),0);await a.context.close();
  const b=await participant(390);await consent(b.page);await b.page.locator('label').filter({has:b.page.locator('[name=used_service][value=no]')}).click();await next(b.page);await b.page.getByRole('heading',{name:'Not eligible',exact:true}).waitFor();assert.equal(await b.page.locator('[data-back]').count(),0);await b.context.close();
  for(const width of [390,1280]) {
    const c=await participant(width);await feedback(c.page,'=1+1, "Unicode 한글 中文"\nsecond line');
    await c.page.reload();await c.page.getByRole('heading',{name:'Finish your participation',exact:true}).waitFor();
    await c.page.locator('[name=withdraw_now][value=submit]').check();await next(c.page);await c.page.getByRole('heading',{name:'Thank you',exact:true}).waitFor();await c.context.close();
  }
  const w=await participant();await feedback(w.page,'Must be erased');await w.page.locator('[name=withdraw_now][value=withdraw]').check();await next(w.page);await w.page.getByRole('heading',{name:'Participation withdrawn',exact:true}).waitFor();await w.context.close();
  const incomplete=await participant(390);await feedback(incomplete.page,'Incomplete imaginary response');
  const sessions=(await client.query('SELECT * FROM gq_sessions WHERE study_id=$1',[model.study_id])).rows;
  assert.equal(sessions.length,6);assert(sessions.every(s=>s.is_test&&s.respondent_source==='direct'));
  const withdrawn=sessions.find(s=>s.lifecycle_state==='withdrawn');assert(withdrawn);
  assert.equal((await client.query('SELECT * FROM gq_answers WHERE session_id=$1',[withdrawn.id])).rows.length,0);
  assert.equal((await client.query("SELECT * FROM gq_answers WHERE question_id='problem_detail'")).rows.length,0);
  const dashboard=await browser.newPage();dashboard.on('pageerror',e=>errors.push(e.message));await dashboard.goto(base+'/results');
  await dashboard.waitForFunction(()=>document.getElementById('status').textContent.startsWith('Updated'));
  assert.equal(await dashboard.locator('#started').textContent(),'0');
  await dashboard.locator('#scope').selectOption('test');await dashboard.waitForFunction(()=>document.getElementById('started').textContent==='6');
  await dashboard.locator('#source').selectOption('prolific');await dashboard.waitForFunction(()=>document.getElementById('started').textContent==='0');
  await dashboard.locator('#source').selectOption('direct');await dashboard.waitForFunction(()=>document.getElementById('started').textContent==='6');
  const [download]=await Promise.all([dashboard.waitForEvent('download'),dashboard.locator('#download').click()]);
  const csv=fs.readFileSync(await download.path(),'utf8');fs.writeFileSync(path.join(study,'dashboard.csv'),csv);
  assert(csv.includes('problem_detail'));assert(!csv.includes('Must be erased'));
  assert(csv.includes("'=1+1"),'Dashboard CSV must preserve text without treating it as a spreadsheet formula');
  assert(!csv.includes('[object Object]'));
  // Close the exact study, create and verify the actual archive, then exercise only a fake provider.
  const snapshot=await ops.closeAndSnapshot(client,model.study_id,model.study_id);
  snapshot.targets={team:'local-team',survey:'local-survey',results:'local-results',supabase:'local-db'};
  const snapshotFile=path.join(study,'snapshot.json'),archive=path.join(study,'study-archive.zip');fs.writeFileSync(snapshotFile,JSON.stringify(snapshot));
  const built=spawnSync(process.env.GREEDYQ_PYTHON||'python3',['-m','greedyq.archive',snapshotFile,path.join(study,'preview-model.json'),archive],{cwd:repo,encoding:'utf8'});assert.equal(built.status,0,built.stderr);
  const verified=spawnSync(process.env.GREEDYQ_PYTHON||'python3',['-c','import sys,json;from greedyq.archive import verify_archive;print(json.dumps(verify_archive(sys.argv[1])))',archive],{cwd:repo,encoding:'utf8'});assert.equal(verified.status,0,verified.stderr);
  const manifest=JSON.parse(verified.stdout);assert.equal(manifest.counts.sessions,6);
  const contents=spawnSync(process.env.GREEDYQ_PYTHON||'python3',['-c',`
import csv,io,json,sys,zipfile
from pathlib import Path
with zipfile.ZipFile(sys.argv[1]) as z:
 real=list(csv.DictReader(io.StringIO(z.read('responses.csv').decode('utf-8-sig'))))
 tests=list(csv.DictReader(io.StringIO(z.read('test-responses.csv').decode('utf-8-sig'))))
 data=json.loads(z.read('data.json'))
 assert len(real)==0 and len(tests)==6
 assert all(not r['PROLIFIC_PID'] and not r['STUDY_ID'] and not r['SESSION_ID'] for r in tests)
 assert all(not r['answer.problem_detail'] for r in tests)
 assert any(r['answer.comment']=='Incomplete imaginary response' for r in tests)
 assert not any(a['value']=='Must be erased' for a in data['answers'])
 assert any(a['value']=='=1+1, "Unicode 한글 中文"\\nsecond line' for a in data['answers'])
rows=list(csv.DictReader(io.StringIO(Path(sys.argv[2]).read_text(encoding='utf-8-sig'))))
assert len(rows)==6 and any(r['comment'].startswith("'=1+1") for r in rows)
assert all(not r['problem_detail'] for r in rows)
`,archive,path.join(study,'dashboard.csv')],{cwd:repo,encoding:'utf8'});
  assert.equal(contents.status,0,contents.stderr);
  await incomplete.page.locator('[name=withdraw_now][value=submit]').check();
  await incomplete.page.getByRole('heading',{name:'Survey closed',exact:true}).waitFor();
  assert.equal(await incomplete.page.locator('[data-next]').count(),0);await incomplete.context.close();
  const closed=await browser.newPage();
  await closed.route('https://journey.supabase.test/**',async route=>route.fulfill({status:400,json:{message:'This study is closed for archiving'}}));
  await closed.goto(base);await closed.getByRole('heading',{name:'Survey closed',exact:true}).waitFor();await closed.close();
  const probe=sessions.find(s=>s.lifecycle_state==='consent_refused');
  await assert.rejects(client.query('UPDATE gq_sessions SET current_page=current_page WHERE id=$1',[probe.id]),/closed for archiving/);
  const calls=[],paused=new Set();const provider={preflight:async()=>calls.push('preflight'),isPaused:async(k,id)=>paused.has(id),pause:async(k,id)=>{calls.push(id);paused.add(id);}};
  const args={archivePath:archive,expectedHash:ops.hash(fs.readFileSync(archive)),downloadConfirmed:false,exclusiveResources:true,targets:snapshot.targets,provider,record:async()=>{},verifyArchive:async()=>manifest,approvedStudyId:model.study_id};
  await assert.rejects(ops.pauseServices(args));assert.equal(calls.length,0);
  assert.equal((await ops.pauseServices({...args,downloadConfirmed:true})).status,'archived');assert.deepEqual(calls,['preflight','local-survey','local-results','local-db']);
  await assert.rejects(ops.reopenCollection(client,model.study_id,'wrong-study'));await ops.reopenCollection(client,model.study_id,model.study_id);
  await client.query('UPDATE gq_sessions SET current_page=current_page WHERE id=$1',[probe.id]);
  assert.deepEqual(blocked,[]);assert.deepEqual(errors,[]);
  console.log(JSON.stringify({sessions:6,completed:2,incomplete:1,withdrawn_answers:0,archive_sessions:manifest.counts.sessions,cloud_calls:0,provider:'local fake only',browser_errors:errors.length}));
}
main().catch(error=>{console.error(error);process.exitCode=1;}).finally(async()=>{if(browser)await browser.close();if(server)await new Promise(r=>server.close(r));await respondentClient.end();await client.end();});
