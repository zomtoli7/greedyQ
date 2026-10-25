const {test}=require('node:test'),assert=require('node:assert/strict');
const handler=require('../templates/vercel/api/results.js');
test('preview issuance requires exact protected-page origin and JSON; database rejects production',async()=>{
 const originalFetch=global.fetch,oldUrl=process.env.SUPABASE_URL,oldSecret=process.env.SUPABASE_SECRET_KEY;let calls=0,production=false;
 process.env.SUPABASE_URL='https://unit.supabase.co';process.env.SUPABASE_SECRET_KEY='test_server_secret';
 global.fetch=async(url,options)=>{calls++;assert(url.endsWith('/rpc/greedyq_issue_preview'));assert.equal(options.headers.apikey,'test_server_secret');assert.deepEqual(JSON.parse(options.body),{p_study_id:'trial'});return{ok:!production,json:async()=> 'a'.repeat(64)};};
 const request=async(headers,body={action:'preview',study:'trial'})=>{let status,result;await handler({method:'POST',headers,body},{set statusCode(v){status=v},setHeader(){},end(v){result=JSON.parse(v)}});return{status,result};};
 try{
  assert.equal((await request({host:'results.test',origin:'https://attacker.test','content-type':'application/json'})).status,403);
  assert.equal((await request({host:'results.test',origin:'https://results.test','content-type':'text/plain'})).status,403);assert.equal(calls,0);
  const headers={host:'results.test',origin:'https://results.test','content-type':'application/json'};
  const good=await request(headers);assert.equal(good.status,200);assert.equal(good.result.expires_in_hours,24);
  production=true;assert.equal((await request(headers)).status,400);
 }finally{global.fetch=originalFetch;if(oldUrl===undefined)delete process.env.SUPABASE_URL;else process.env.SUPABASE_URL=oldUrl;if(oldSecret===undefined)delete process.env.SUPABASE_SECRET_KEY;else process.env.SUPABASE_SECRET_KEY=oldSecret;}
});
