/* Agent-side operations. Never ship this module or its environment to respondents. */
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const hash = data => crypto.createHash('sha256').update(data).digest('hex');
const tables = ['sessions','answers','assignments','external_identifiers','consent_events','lifecycle_events','data_requests'];
const caURL = 'https://supabase-downloads.s3-ap-southeast-1.amazonaws.com/prod/ssl/prod-ca-2021.crt';

async function databaseClient(Client, connectionString, fetcher = fetch) {
  const response = await fetcher(caURL);
  if (!response.ok) throw new Error('Official database CA download failed');
  const ca = await response.text();
  if (!ca.includes('BEGIN CERTIFICATE')) throw new Error('Invalid database CA');
  const url = new URL(connectionString);
  for (const key of ['sslmode','sslrootcert','sslcert','sslkey']) url.searchParams.delete(key);
  const client = new Client({connectionString:url.toString(),ssl:{ca,rejectUnauthorized:true},connectionTimeoutMillis:15000});
  await client.connect();
  return client;
}

async function migrate(client, directory) {
  const manifest = JSON.parse(fs.readFileSync(path.join(directory,'manifest.json')));
  const expected=['001_initial.sql','002_browser_rpc.sql','003_results_dashboard.sql','004_randomization.sql','005_prolific.sql','006_withdrawal_preview.sql','007_answer_snapshot.sql','008_terminal_timestamp.sql'];
  const names=manifest.migrations.map(e=>e.name);
  if (![JSON.stringify(expected),JSON.stringify([...expected,'009_cbc.sql'])].includes(JSON.stringify(names))) throw new Error('Complete ordered migration set required');
  for (const entry of manifest.migrations) {
    if (!/^\d{3}_[a-z_]+\.sql$/.test(entry.name)) throw new Error('Invalid migration name');
    if (hash(fs.readFileSync(path.join(directory,entry.name))) !== entry.sha256) throw new Error('Migration checksum mismatch');
  }
  await client.query('BEGIN');
  try {
    await client.query("SELECT pg_advisory_xact_lock(hashtext('greedyq_migrations'))");
    await client.query('CREATE TABLE IF NOT EXISTS public.gq_migration_history (name text primary key, sha256 text not null)');
    await client.query('REVOKE ALL ON public.gq_migration_history FROM public, anon, authenticated');
    for (const entry of manifest.migrations) {
      const old = await client.query('SELECT sha256 FROM public.gq_migration_history WHERE name=$1',[entry.name]);
      if (old.rows.length) {
        if (old.rows[0].sha256 !== entry.sha256) throw new Error('Previously applied migration changed');
        continue;
      }
      await client.query(fs.readFileSync(path.join(directory,entry.name),'utf8'));
      await client.query('INSERT INTO public.gq_migration_history VALUES ($1,$2)',[entry.name,entry.sha256]);
    }
    await client.query('COMMIT');
  } catch (error) { await client.query('ROLLBACK'); throw error; }
}

async function closeAndSnapshot(client, studyId, approvedStudyId) {
  if (!studyId || approvedStudyId !== studyId) throw new Error('Exact study closure approval required');
  await client.query('BEGIN');
  try {
    // Locks drain in-flight writes and prevent a gap between closure and the snapshot.
    await client.query('LOCK TABLE '+tables.map(t=>'public.gq_'+t).join(',')+' IN SHARE ROW EXCLUSIVE MODE');
    await client.query('CREATE TABLE IF NOT EXISTS public.gq_closed_studies (study_id text primary key, closed_at timestamptz not null default now())');
    await client.query('REVOKE ALL ON public.gq_closed_studies FROM public, anon, authenticated');
    await client.query(`CREATE OR REPLACE FUNCTION public.gq_guard_closed_study() RETURNS trigger
      LANGUAGE plpgsql SECURITY DEFINER SET search_path=public,pg_temp AS $$
      DECLARE sid text; previous_sid text;
      BEGIN
        IF TG_TABLE_NAME='gq_sessions' THEN
          IF TG_OP<>'DELETE' THEN sid:=NEW.study_id; END IF;
          IF TG_OP<>'INSERT' THEN previous_sid:=OLD.study_id; END IF;
        ELSE
          IF TG_OP<>'DELETE' THEN SELECT study_id INTO sid FROM public.gq_sessions WHERE id=NEW.session_id; END IF;
          IF TG_OP<>'INSERT' THEN SELECT study_id INTO previous_sid FROM public.gq_sessions WHERE id=OLD.session_id; END IF;
        END IF;
        IF EXISTS(SELECT 1 FROM public.gq_closed_studies WHERE study_id IN (sid,previous_sid)) THEN
          RAISE EXCEPTION 'This study is closed for archiving';
        END IF;
        IF TG_OP='DELETE' THEN RETURN OLD; ELSE RETURN NEW; END IF;
      END $$`);
    for (const table of tables) {
      await client.query(`DROP TRIGGER IF EXISTS gq_archive_guard ON public.gq_${table}`);
      await client.query(`CREATE TRIGGER gq_archive_guard BEFORE INSERT OR UPDATE OR DELETE ON public.gq_${table} FOR EACH ROW EXECUTE FUNCTION public.gq_guard_closed_study()`);
    }
    await client.query('INSERT INTO public.gq_closed_studies(study_id) VALUES ($1) ON CONFLICT DO NOTHING',[studyId]);
    const data = {};
    data.sessions=(await client.query('SELECT * FROM public.gq_sessions WHERE study_id=$1 ORDER BY id',[studyId])).rows;
    for (const table of tables.slice(1)) data[table]=(await client.query(`SELECT t.* FROM public.gq_${table} t JOIN public.gq_sessions s ON s.id=t.session_id WHERE s.study_id=$1`,[studyId])).rows;
    for (const s of data.sessions) { delete s.access_token_hash; delete s.browser_state; }
    const otherStudies=(await client.query('SELECT DISTINCT study_id FROM public.gq_sessions WHERE study_id<>$1',[studyId])).rows.map(r=>r.study_id);
    await client.query('COMMIT');
    return {study_id:studyId,collection_closed:true,created_at:new Date().toISOString(),tables:data,other_studies:otherStudies};
  } catch(error) {await client.query('ROLLBACK');throw error;}
}

async function pauseServices({archivePath,expectedHash,downloadConfirmed,exclusiveResources,targets,provider,record,verifyArchive,approvedStudyId}) {
  if (!downloadConfirmed || !exclusiveResources) throw new Error('Download confirmation and exclusive resource review required');
  if (!expectedHash || hash(fs.readFileSync(archivePath)) !== expectedHash) throw new Error('Archive changed or missing');
  if (typeof verifyArchive!=='function') throw new Error('Archive content verifier required');
  const manifest=await verifyArchive(archivePath);
  if (!approvedStudyId || manifest.study_id!==approvedStudyId || manifest.collection_closed!==true) throw new Error('Archive study approval mismatch');
  if (!targets?.supabase || !targets?.survey || !targets?.results || !targets?.team || targets.survey===targets.results) throw new Error('Exact distinct resource targets required');
  if (manifest.other_studies?.length) throw new Error('Shared database cannot be paused for one study');
  if (manifest.unresolved_data_requests) throw new Error('Resolve pending data requests before pausing');
  if (!manifest.targets || Object.keys(targets).some(k=>targets[k]!==manifest.targets[k])) throw new Error('Archive resource binding mismatch');
  // Provider preflight must verify ownership, all linked projects, plan and permission before mutations.
  await provider.preflight(targets);
  for (const [kind,id] of [['vercel',targets.survey],['vercel',targets.results],['supabase',targets.supabase]]) {
    if (await provider.isPaused(kind,id)) {await record({kind,id,status:'paused'});continue;}
    await record({kind,id,status:'pause_requested'});
    try { await provider.pause(kind,id); }
    catch(error) { await record({kind,id,status:'pause_failed_or_uncertain'}); throw error; }
    if (!await provider.isPaused(kind,id)) {
      await record({kind,id,status:'pending_verification'});
      return {status:'pending_verification',kind,id};
    }
    await record({kind,id,status:'paused'});
  }
  return {status:'archived'};
}

function managementProvider({vercelToken,supabaseToken,review,fetcher=fetch}) {
  let binding;
  const request=async(kind,endpoint,method='GET')=>{
    const token=kind==='vercel'?vercelToken:supabaseToken;
    if(!token)throw new Error('Provider management authorization required; database keys are insufficient');
    const host=kind==='vercel'?'https://api.vercel.com':'https://api.supabase.com';
    const response=await fetcher(host+endpoint,{method,headers:{Authorization:'Bearer '+token},signal:AbortSignal.timeout(20000)});
    if(!response.ok)throw new Error(`${kind} management request failed (${response.status})`);
    return response.status===204?{}:response.json();
  };
  return {
    async preflight(targets){
      for(const value of Object.values(targets))if(!/^[a-zA-Z0-9_-]+$/.test(value))throw new Error('Invalid target ID');
      if(!review || !await review(targets))throw new Error('Resource ownership, free plan and sharing review required');
      binding=targets;
      for(const id of [targets.survey,targets.results]) {
        const p=await request('vercel',`/v9/projects/${id}?teamId=${targets.team}`);
        if(p.id!==id || p.accountId!==targets.team)throw new Error('Vercel target ownership mismatch');
      }
      const p=await request('supabase',`/v1/projects/${targets.supabase}`);
      if(p.id!==targets.supabase)throw new Error('Supabase project mismatch');
    },
    async isPaused(kind,id){
      const p=await request(kind,kind==='vercel'?`/v9/projects/${id}?teamId=${binding.team}`:`/v1/projects/${id}`);
      return kind==='vercel'?p.paused===true:p.status==='INACTIVE';
    },
    pause(kind,id){return request(kind,kind==='vercel'?`/v1/projects/${id}/pause?teamId=${binding.team}`:`/v1/projects/${id}/pause`,'POST');}
  };
}
async function reopenCollection(client, studyId, approvedStudyId) {
  if (!studyId || approvedStudyId!==studyId) throw new Error('Exact collection reopening approval required');
  await client.query('BEGIN');
  try {
    await client.query('LOCK TABLE '+tables.map(t=>'public.gq_'+t).join(',')+' IN SHARE ROW EXCLUSIVE MODE');
    const pending=await client.query("SELECT count(*)::int n FROM public.gq_data_requests r JOIN public.gq_sessions s ON s.id=r.session_id WHERE s.study_id=$1 AND r.status IN ('recorded','reviewing')",[studyId]);
    if(pending.rows[0].n)throw new Error('Resolve data requests before reopening');
    await client.query('DELETE FROM public.gq_closed_studies WHERE study_id=$1',[studyId]);
    await client.query('COMMIT');
    return {study_id:studyId,collection_closed:false};
  }catch(error){await client.query('ROLLBACK');throw error;}
}

function onboardingCommands({team,name,region}) {
  if (![team,name,region].every(v=>typeof v==='string' && /^[a-z0-9-]+$/.test(v))) throw new Error('Explicit safe team, resource name and region required');
  return [
    ['whoami'], ['teams','ls'], ['integration','installations','--scope',team],
    ['integration','add','supabase','--scope',team,'--name',name,'--plan','free','--metadata',`region=${region}`,'--no-connect','--no-env-pull','--non-interactive']
  ];
}

async function registerStudy(client, model) {
  const core=require('../web/greedyq-core.js');
  if (!model.study_id || !model.pages?.length) throw new Error('Reviewed study model required');
  if (model.randomization) {const problem=core.planProblem(model.randomization);if(problem)throw new Error(problem);}
  await client.query('BEGIN');
  try {
    await client.query('LOCK TABLE public.gq_study_plans IN SHARE ROW EXCLUSIVE MODE');
    const old=await client.query('SELECT model FROM public.gq_study_plans WHERE study_id=$1',[model.study_id]);
    if (old.rows.length) {
      const same=await client.query('SELECT model=$2::jsonb AS same FROM public.gq_study_plans WHERE study_id=$1',[model.study_id,JSON.stringify(model)]);
      if (!same.rows[0]?.same) throw new Error('Registered study changed; use a new study ID.');
    } else {
      const previous=await client.query('SELECT 1 FROM public.gq_assignments a JOIN public.gq_sessions s ON s.id=a.session_id WHERE s.study_id=$1 LIMIT 1',[model.study_id]);
      if (previous.rows.length && model.randomization) throw new Error('Legacy assignments exist; use a new study ID.');
      await client.query('INSERT INTO public.gq_study_plans(study_id,model) VALUES($1,$2::jsonb)',[model.study_id,JSON.stringify(model)]);
    }
    await client.query('COMMIT');
  } catch(error) {await client.query('ROLLBACK');throw error;}
}
function prepareDeployments({repo,model,directory,url,publishableKey}) {
  if (new URL(url).protocol!=='https:' || !publishableKey || !model.study_id) throw new Error('Public deployment configuration required');
  if (!publishableKey.startsWith('sb_publishable_')) throw new Error('Use a public publishable key, never a server secret');
  // Separate directories prevent accidentally publishing results APIs or private study records.
  fs.mkdirSync(directory,{recursive:false,mode:0o700});
  const embed=(html,id,value)=>html.replace(new RegExp('(<script id="'+id+'"[^>]*>)[\\s\\S]*?(</script>)'),(_,a,b)=>a+JSON.stringify(value).replace(/</g,'\\u003c')+b);
  for(const type of ['survey','results']) {
    const dest=path.join(directory,type);fs.mkdirSync(dest);
    for(const asset of ['greedyq-core.js','greedyq-runtime.css','greedyq-cbc.js']) fs.copyFileSync(path.join(repo,'web',asset),path.join(dest,asset));
    const template=type==='survey'?'respondent.html':'results.html';
    let html=embed(fs.readFileSync(path.join(repo,'templates/browser',template),'utf8'),'greedyq-model',model);
    if(type==='survey') html=embed(html,'greedyq-deployment',{mode:'supabase',supabase_url:url,supabase_anon_key:publishableKey});
    fs.writeFileSync(path.join(dest,'index.html'),html);
    fs.writeFileSync(path.join(dest,'vercel.json'),JSON.stringify({cleanUrls:false}));
    if(type==='results'){fs.mkdirSync(path.join(dest,'api'));fs.copyFileSync(path.join(repo,'templates/vercel/api/results.js'),path.join(dest,'api/results.js'));}
  }
  return {resultsProtection:{ssoProtection:{deploymentType:'all'}},surveyProtection:{ssoProtection:null}};
}
module.exports={hash,databaseClient,migrate,registerStudy,closeAndSnapshot,reopenCollection,pauseServices,managementProvider,onboardingCommands,prepareDeployments};
