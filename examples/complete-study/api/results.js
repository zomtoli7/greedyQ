/* Server-only greedyQ results API. Deploy behind Vercel Authentication. */
const send = (res, status, body, type = "application/json; charset=utf-8") => {
  res.statusCode = status;
  res.setHeader("content-type", type);
  res.setHeader("cache-control", "no-store");
  res.end(type.startsWith("application/json") ? JSON.stringify(body) : body);
};

const allowed = (value, values, fallback) => values.includes(value) ? value : fallback;
// Read every page or fail explicitly; never silently cap a CBC export at 1,000 rows.
const query = async (path, secret) => {
  const all=[];
  for(let offset=0;offset<1000000;){
    const response = await fetch(`${process.env.SUPABASE_URL}/rest/v1/${path}&limit=1000&offset=${offset}`, {
      headers: { apikey: secret, authorization: `Bearer ${secret}`, Prefer: "count=exact" },
    });
    if (!response.ok) throw new Error(`Database request failed (${response.status}).`);
    const rows=await response.json();if(!Array.isArray(rows))throw Error('Invalid results response.');all.push(...rows);
    const range=response.headers?.get?.('content-range'),total=range&&/\/(\d+)$/.exec(range);
    if(total){if(all.length>=Number(total[1]))return all;if(!rows.length)throw Error('Incomplete results page.');}
    else if(rows.length<1000)return all;
    offset+=rows.length;
  }
  throw Error('This export is too large for the results page. Use the complete archive.');
};
const related = async (table,columns,ids,secret) => {
  const all=[];
  for(let i=0;i<ids.length;i+=100){const subset=ids.slice(i,i+100);all.push(...await query(`${table}?select=${columns}&session_id=in.(${subset.join(',')})&order=session_id.asc${table==='gq_answers'?',question_id.asc':table==='gq_assignments'?',randomization_id.asc':',provider.asc'}`,secret));}
  return all;
};

module.exports = async (req, res) => {
  if (!["GET","POST"].includes(req.method)) return send(res, 405, { error: "Method not allowed" });
  const secret = process.env.SUPABASE_SECRET_KEY || process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!process.env.SUPABASE_URL || !secret)
    return send(res, 503, { error: "The results connection has not been provisioned." });
  if(req.method==='POST'){
    // The entire results project, including this API, requires Vercel Authentication.
    if(req.headers.origin!==`https://${req.headers.host}` || !String(req.headers['content-type'] || '').startsWith('application/json'))return send(res,403,{error:'Open the protected results page to create a test link.'});
    try{
      const body=typeof req.body==='string'?JSON.parse(req.body):req.body;
      if(body?.action!=='preview' || !/^[A-Za-z0-9_-]{1,120}$/.test(body.study || ''))return send(res,400,{error:'Choose a registered test study.'});
      const response=await fetch(`${process.env.SUPABASE_URL}/rest/v1/rpc/${body.kind==='cbc'?'greedyq_issue_cbc_preview':'greedyq_issue_preview'}`,{method:'POST',headers:{apikey:secret,authorization:`Bearer ${secret}`,'content-type':'application/json'},body:JSON.stringify({p_study_id:body.study})});
      if(!response.ok)return send(res,400,{error:'A test link requires the matching upgraded database and a registered study.'});
      return send(res,200,{preview_token:await response.json(),expires_in_hours:24});
    }catch{return send(res,400,{error:'Could not create the test link.'});}
  }
  const scope = allowed(req.query?.scope, ["production", "test", "all"], "production");
  const source = allowed(req.query?.source, ["direct", "prolific", "all"], "all");
  const study = String(req.query?.study || "").slice(0, 120);
  const filters = [];
  if (scope !== "all") filters.push(`is_test=eq.${scope === "test"}`);
  if (source !== "all") filters.push(`respondent_source=eq.${source}`);
  if (study) filters.push(`study_id=eq.${encodeURIComponent(study)}`);
  try {
    const suffix = filters.length ? `&${filters.join("&")}` : "";
    const sessions = await query(`gq_sessions?select=id,study_id,study_version,current_page,is_test,respondent_source,lifecycle_state,created_at,updated_at,terminal_at,question_orders,option_orders,page_order&order=created_at.desc,id.asc${suffix}`, secret);
    const ids = sessions.map(x => x.id);
    const [answers, assignments, external_identifiers] = await Promise.all([
      related('gq_answers','session_id,question_id,value,answered_at',ids,secret),
      related('gq_assignments','session_id,randomization_id,condition,method,block_id,draw_id,assigned_at',ids,secret),
      related('gq_external_identifiers','session_id,provider,participant_id,external_study_id,external_session_id',ids,secret),
    ]);
    return send(res, 200, { generated_at: new Date().toISOString(), scope, source, sessions, answers, assignments, external_identifiers });
  } catch (error) {
    return send(res, 502, { error: error.message });
  }
};
