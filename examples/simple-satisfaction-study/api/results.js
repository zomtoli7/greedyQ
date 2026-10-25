/* Server-only greedyQ results API. Deploy behind Vercel Authentication. */
const send = (res, status, body, type = "application/json; charset=utf-8") => {
  res.statusCode = status;
  res.setHeader("content-type", type);
  res.setHeader("cache-control", "no-store");
  res.end(type.startsWith("application/json") ? JSON.stringify(body) : body);
};

const allowed = (value, values, fallback) => values.includes(value) ? value : fallback;
const query = async (path, secret) => {
  const response = await fetch(`${process.env.SUPABASE_URL}/rest/v1/${path}`, {
    headers: { apikey: secret, authorization: `Bearer ${secret}` },
  });
  if (!response.ok) throw new Error(`Database request failed (${response.status}).`);
  return response.json();
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
      const response=await fetch(`${process.env.SUPABASE_URL}/rest/v1/rpc/greedyq_issue_preview`,{method:'POST',headers:{apikey:secret,authorization:`Bearer ${secret}`,'content-type':'application/json'},body:JSON.stringify({p_study_id:body.study})});
      if(!response.ok)return send(res,400,{error:'A preview link requires an upgraded database and a registered Prolific study in Test mode.'});
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
    const sessions = await query(`gq_sessions?select=id,study_id,study_version,current_page,is_test,respondent_source,lifecycle_state,created_at,updated_at,terminal_at,question_orders,option_orders,page_order&order=created_at.desc${suffix}`, secret);
    const ids = sessions.map(x => x.id);
    const idFilter = ids.length ? `in.(${ids.join(",")})` : "eq.00000000-0000-0000-0000-000000000000";
    const [answers, assignments, external_identifiers] = await Promise.all([
      query(`gq_answers?select=session_id,question_id,value,answered_at&session_id=${idFilter}&order=answered_at.asc`, secret),
      query(`gq_assignments?select=session_id,randomization_id,condition,method,block_id,draw_id,assigned_at&session_id=${idFilter}`, secret),
      query(`gq_external_identifiers?select=session_id,provider,participant_id,external_study_id,external_session_id&session_id=${idFilter}`,secret),
    ]);
    return send(res, 200, { generated_at: new Date().toISOString(), scope, source, sessions, answers, assignments, external_identifiers });
  } catch (error) {
    return send(res, 502, { error: error.message });
  }
};
