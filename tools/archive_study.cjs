#!/usr/bin/env node
/* Operator CLI; Node + pg and Python are agent tools, not researcher requirements. */
const fs=require('node:fs'),path=require('node:path'),{spawnSync}=require('node:child_process');
const ops=require('./cloud_lifecycle.cjs');
const repo=path.resolve(__dirname,'..');
function python(code,args){
 const r=spawnSync(process.env.GREEDYQ_PYTHON||'python3',['-c',code,...args],{cwd:repo,encoding:'utf8',env:{...process.env,PYTHONPATH:repo}});
 if(r.status!==0)throw new Error('Archive creation/verification failed; no service was paused');
 return r.stdout;
}
async function main(){
 const [command,configFile]=process.argv.slice(2);
 if(!['snapshot','pause','reopen'].includes(command)||!configFile)throw new Error('Usage: node tools/archive_study.cjs snapshot|pause|reopen PRIVATE_CONFIG.json');
 const config=JSON.parse(fs.readFileSync(configFile));
 if(command==='snapshot'||command==='reopen'){
  if(config.approvedStudyId!==config.studyId)throw new Error('Researcher closure approval required');
  if(!config.targets?.supabase || !process.env.SUPABASE_URL || new URL(process.env.SUPABASE_URL).hostname!==config.targets.supabase+'.supabase.co')throw new Error('Database project binding mismatch');
  const databaseURL=new URL(process.env.POSTGRES_URL);
  if(databaseURL.hostname!==`db.${config.targets.supabase}.supabase.co` && decodeURIComponent(databaseURL.username)!==`postgres.${config.targets.supabase}`)throw new Error('Database credential target mismatch');
  const model=JSON.parse(fs.readFileSync(config.model));
  if(model.study_id!==config.studyId)throw new Error('Study model mismatch');
  if(command==='reopen'){
   if(config.approveReopen!==true)throw new Error('Separate collection reopening approval required');
   const {Client}=require('pg');
   const client=await ops.databaseClient(Client,process.env.POSTGRES_URL);
   try{console.log(JSON.stringify(await ops.reopenCollection(client,config.studyId,config.approvedStudyId)));}finally{await client.end();}
   return;
  }
  // Never overwrite an existing archive or silently use another study directory.
  fs.mkdirSync(config.output,{recursive:false,mode:0o700});
  const {Client}=require('pg');
  const client=await ops.databaseClient(Client,process.env.POSTGRES_URL);
  let snapshot;
  try{snapshot=await ops.closeAndSnapshot(client,config.studyId,config.approvedStudyId);}finally{await client.end();}
  snapshot.targets=config.targets;
  const source=path.join(config.output,'snapshot.json'),zip=path.join(config.output,'study-archive.zip');
  fs.writeFileSync(source,JSON.stringify(snapshot),{mode:0o600,flag:'wx'});
  python('import sys,json; from pathlib import Path; from greedyq.archive import make_archive; make_archive(json.loads(Path(sys.argv[1]).read_text()),json.loads(Path(sys.argv[2]).read_text()),sys.argv[3])',[source,config.model,zip]);
  python('import sys,zipfile; from pathlib import Path; z=zipfile.ZipFile(sys.argv[1]);\nfor name in ("responses.csv","test-responses.csv"):\n p=Path(sys.argv[2])/name\n with p.open("xb") as f: f.write(z.read(name))\n p.chmod(0o600)',[zip,config.output]);
  console.log(JSON.stringify({status:'awaiting_download_confirmation',archive:zip,sha256:ops.hash(fs.readFileSync(zip)),csv:path.join(config.output,'responses.csv')}));
 }else{
  const verifyArchive=async file=>JSON.parse(python('import sys,json; from greedyq.archive import verify_archive; print(json.dumps(verify_archive(sys.argv[1])))',[file]));
  const provider=ops.managementProvider({vercelToken:process.env.VERCEL_TOKEN,supabaseToken:process.env.SUPABASE_ACCESS_TOKEN,
    review:async()=>config.resourceOwnershipReviewed===true && config.freePlanReviewed===true && config.linkedProjectsReviewed===true});
  const journal=path.join(path.dirname(config.archivePath),'pause-events.jsonl');
  const result=await ops.pauseServices({...config,provider,verifyArchive,record:async event=>fs.appendFileSync(journal,JSON.stringify({...event,at:new Date().toISOString()})+'\n',{mode:0o600})});
  console.log(JSON.stringify(result));
 }
}
main().catch(()=>{console.error('Archive operation stopped. Inspect private operation state and configuration; do not assume services are paused.');process.exitCode=1;});
