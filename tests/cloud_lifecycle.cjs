const {test}=require('node:test'),assert=require('node:assert/strict');
const fs=require('node:fs'),os=require('node:os'),path=require('node:path');
const ops=require('../tools/cloud_lifecycle.cjs');
const root=path.resolve(__dirname,'..');
test('onboarding pins free plan and explicit region; rejects shell fragments',()=>{
 assert(ops.onboardingCommands({team:'team-a',name:'study-a',region:'icn1'}).at(-1).includes('free'));
 assert.throws(()=>ops.onboardingCommands({team:'a;rm',name:'a',region:'icn1'}));
});
test('separate deployment bundles copy runtime exactly and never include private files',()=>{
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'gq-deploy-test-'));
 const dest=path.join(tmp,'bundles');
 const model=JSON.parse(fs.readFileSync(path.join(root,'examples/complete-study/preview-model.json')));
 const settings=ops.prepareDeployments({repo:root,model,directory:dest,url:'https://example.supabase.co',publishableKey:'sb_publishable_fake'});
 assert.equal(settings.resultsProtection.ssoProtection.deploymentType,'all');
 assert(!fs.existsSync(path.join(dest,'survey/api')));
 assert(fs.existsSync(path.join(dest,'results/api/results.js')));
 assert.equal(ops.hash(fs.readFileSync(path.join(dest,'survey/greedyq-core.js'))),ops.hash(fs.readFileSync(path.join(root,'web/greedyq-core.js'))));
 assert.throws(()=>ops.prepareDeployments({repo:root,model,directory:dest,url:'https://example.supabase.co',publishableKey:'sb_secret_fake'}));
 fs.rmSync(tmp,{recursive:true});
});
test('TLS remains verified and strips weaker URL SSL overrides',async()=>{
 let config;class Client{constructor(c){config=c}async connect(){}}
 await ops.databaseClient(Client,'postgres://u:p@host/db?sslmode=require',async()=>({ok:true,text:async()=> '-----BEGIN CERTIFICATE-----\nfake'}));
 assert.equal(config.ssl.rejectUnauthorized,true);assert(!config.connectionString.includes('sslmode'));
 await assert.rejects(ops.databaseClient(Client,'postgres://host/db',async()=>({ok:false})));
});
test('snapshot drains writes, installs gates and filters every table',async()=>{
 const queries=[];const client={query:async(sql,args)=>{queries.push([sql,args]);return {rows:[]}}};
 await assert.rejects(ops.closeAndSnapshot(client,'a','b'));assert.equal(queries.length,0);
 const snap=await ops.closeAndSnapshot(client,'a','a');
 assert(snap.collection_closed);assert.equal(Object.keys(snap.tables).length,7);
 assert(queries.some(([q])=>q.startsWith('LOCK TABLE')));
 assert.equal(queries.filter(([q])=>q.startsWith('CREATE TRIGGER')).length,7);
 assert.equal(queries.at(-1)[0],'COMMIT');
});
test('snapshot failure rolls back',async()=>{
 const queries=[];const client={query:async sql=>{queries.push(sql);if(sql.startsWith('LOCK'))throw Error('busy');return {rows:[]}}};
 await assert.rejects(ops.closeAndSnapshot(client,'a','a'));assert.equal(queries.at(-1),'ROLLBACK');
});
for(const scenario of ['success','not-downloaded','shared','changed','pending','failure','already-paused','wrong-study','pending-data-request','shared-database','wrong-target'])test('pause workflow '+scenario,async()=>{
 const tmp=fs.mkdtempSync(path.join(os.tmpdir(),'gq-pause-test-')),file=path.join(tmp,'archive.zip');fs.writeFileSync(file,'test archive');
 const calls=[],states=new Set(),records=[];
 const provider={preflight:async()=>calls.push('preflight'),isPaused:async(k,id)=>scenario==='already-paused'||states.has(id),pause:async(k,id)=>{calls.push(id);if(scenario==='failure')throw Error('denied');if(scenario!=='pending')states.add(id)}};
 const args={archivePath:file,expectedHash:scenario==='changed'?'wrong':ops.hash(fs.readFileSync(file)),downloadConfirmed:scenario!=='not-downloaded',exclusiveResources:scenario!=='shared',targets:{team:'t',survey:'s',results:'r',supabase:'db'},provider,record:async r=>records.push(r),approvedStudyId:'a',verifyArchive:async()=>({study_id:scenario==='wrong-study'?'b':'a',collection_closed:true,targets:{team:'t',survey:'s',results:'r',supabase:'db'}})};
 const originalVerifier=args.verifyArchive;
 args.verifyArchive=async()=>({...await originalVerifier(),unresolved_data_requests:scenario==='pending-data-request'?1:0,other_studies:scenario==='shared-database'?['other']:[],...(scenario==='wrong-target'?{targets:{}}:{})});
 if(['not-downloaded','shared','changed','failure','wrong-study','pending-data-request','shared-database','wrong-target'].includes(scenario))await assert.rejects(ops.pauseServices(args));
 else assert.equal((await ops.pauseServices(args)).status,scenario==='pending'?'pending_verification':'archived');
 if(['not-downloaded','shared','changed','wrong-study'].includes(scenario))assert.equal(calls.length,0);
 if(scenario==='success')assert.deepEqual(calls,['preflight','s','r','db']);
 if(scenario==='pending')assert.deepEqual(calls,['preflight','s']);
 fs.rmSync(tmp,{recursive:true});
});
test('migrations check before writes and retry via ledger',async()=>{
 const dir=path.join(root,'examples/complete-study/supabase/migrations');
 const ledger=new Map(),calls=[];
 const client={query:async(sql,args)=>{calls.push(sql);if(sql.startsWith('SELECT sha256'))return {rows:ledger.has(args[0])?[{sha256:ledger.get(args[0])}]:[]};if(sql.startsWith('INSERT INTO public.gq_migration_history'))ledger.set(args[0],args[1]);return {rows:[]}}};
 await ops.migrate(client,dir);assert.equal(ledger.size,6);
 const firstCount=calls.filter(q=>q.startsWith('create extension')).length;
 await ops.migrate(client,dir);assert.equal(calls.filter(q=>q.startsWith('create extension')).length,firstCount);
 ledger.set('001_initial.sql','bad');await assert.rejects(ops.migrate(client,dir));assert.equal(calls.at(-1),'ROLLBACK');
});
test('collection reopen requires approval and blocks unresolved requests',async()=>{
 const calls=[];let pending=0;
 const client={query:async(sql,args)=>{calls.push([sql,args]);return {rows:[{n:pending}]}}};
 await assert.rejects(ops.reopenCollection(client,'a','b'));assert.equal(calls.length,0);
 await ops.reopenCollection(client,'a','a');assert.equal(calls.at(-1)[0],'COMMIT');
 assert(calls.some(([sql,args])=>sql.startsWith('DELETE FROM public.gq_closed_studies')&&args[0]==='a'));
 pending=1;await assert.rejects(ops.reopenCollection(client,'a','a'));assert.equal(calls.at(-1)[0],'ROLLBACK');
});
test('reviewed model registration is idempotent and refuses changed or legacy assignments',async()=>{
 const model={study_id:'test',pages:[{id:'welcome'}]},calls=[];
 let registered=false,same=true,legacy=false;
 const client={query:async(sql,args)=>{calls.push(sql);if(sql.startsWith('SELECT model FROM'))return {rows:registered?[{model}]:[]};if(sql.startsWith('SELECT model='))return {rows:[{same}]};if(sql.startsWith('SELECT 1 FROM public.gq_assignments'))return {rows:legacy?[{}]:[]};return {rows:[]}}};
 await ops.registerStudy(client,model);assert(calls.some(s=>s.startsWith('INSERT INTO public.gq_study_plans')));
 registered=true;await ops.registerStudy(client,model);
 same=false;await assert.rejects(ops.registerStudy(client,model),/new study ID/);
 registered=false;legacy=true;
 await assert.rejects(ops.registerStudy(client,{...model,randomization:{id:'arm',unit:'respondent',persistence_key:'session_id',method:'simple',conditions:{a:1,b:1}}}),/Legacy/);
 assert.equal(calls.at(-1),'ROLLBACK');
});
