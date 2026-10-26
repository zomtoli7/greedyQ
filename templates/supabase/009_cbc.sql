-- Additive CBC protocol. Existing 001–008 bytes and existing records stay unchanged.
-- Reviewed immutable CBC plans share the protected study registry and seven data tables.
create function public.gq_cbc_context(p_session_id uuid,p_access_token text) returns jsonb
language plpgsql security definer set search_path=public,pg_temp as $$
declare s public.gq_sessions; m jsonb;
begin
 select * into s from public.gq_sessions where id=p_session_id for update;
 if not found or not public.greedyq_token_ok(s.id,p_access_token) then raise exception 'invalid session capability'; end if;
 select model into m from public.gq_study_plans where study_id=s.study_id;
 if m->>'kind' is distinct from 'cbc_study' then raise exception 'CBC study required'; end if;
 return m;
end;$$;
revoke all on function public.gq_cbc_context(uuid,text) from public,anon,authenticated;

-- Return only the assigned block, never the other blocks or the full private plan.
create function public.greedyq_cbc_resume(p_session_id uuid,p_access_token text) returns jsonb
language plpgsql security definer set search_path=public,pg_temp as $$
declare m jsonb; s public.gq_sessions; c jsonb; b jsonb;
begin
 m:=public.gq_cbc_context(p_session_id,p_access_token);
 select * into s from public.gq_sessions where id=p_session_id;
 c:=m->'cbc';
 if s.browser_state->>'block_id' is not null and s.lifecycle_state<>'withdrawn' then
  select value into b from jsonb_array_elements(c->'blocks') where value->>'id'=s.browser_state->>'block_id';
 end if;
 return jsonb_build_object('runtime_contract','cbc-1','study_id',s.study_id,'design_sha256',c->>'design_sha256',
  'state',s.browser_state,'is_test',s.is_test,'source',s.respondent_source,'consent',m->'consent',
  'title',m->>'title','organization',m->>'organization','language',m->>'language',
  'model',case when b is null then null else jsonb_set(c,'{blocks}',jsonb_build_array(b)) end,
  'terminal_at',s.terminal_at);
end;$$;
revoke all on function public.greedyq_cbc_resume(uuid,text) from public;
grant execute on function public.greedyq_cbc_resume(uuid,text) to anon,authenticated;

create function public.greedyq_cbc_start(p_session_id uuid,p_access_token text,p_study_id text,p_design_sha256 text,p_preview_token text default null,p_external jsonb default null) returns jsonb
language plpgsql security definer set search_path=public,pg_temp as $$
declare m jsonb; s public.gq_sessions; test boolean; expected text;
begin
 select model into m from public.gq_study_plans where study_id=p_study_id;
 if m->>'kind' is distinct from 'cbc_study' or m->'cbc'->>'design_sha256' is distinct from p_design_sha256 then raise exception 'CBC design mismatch'; end if;
 if length(coalesce(p_access_token,''))<32 or length(p_access_token)>256 then raise exception 'invalid session capability'; end if;
 if m->'runtime_policy'->>'mode' not in ('test','production') then raise exception 'CBC mode required'; end if;
 test:=m->'runtime_policy'->>'mode'='test';
 if p_preview_token is not null then
  if not exists(select 1 from public.gq_preview_grants where token_hash=encode(extensions.digest(p_preview_token,'sha256'),'hex') and study_id=p_study_id and expires_at>now()) then raise exception 'invalid or expired preview grant'; end if;
  test:=true;
 end if;
 if not test and (m->>'fielding_approved') is distinct from 'true' then raise exception 'CBC fielding approval required'; end if;
 if m->'runtime_policy'->>'respondent_source'='direct' and p_external is not null then raise exception 'unexpected panel identifiers'; end if;
 insert into public.gq_sessions(id,study_id,study_version,spec_version,greedyq_version,is_test,access_token_hash,browser_state,current_page)
 values(p_session_id,p_study_id,m->>'study_version','0.3',m->>'greedyq_version',test,encode(extensions.digest(p_access_token,'sha256'),'hex'),jsonb_build_object('phase','consent','revision',0,'lifecycle','created','design_sha256',p_design_sha256),'consent') on conflict(id) do nothing;
 perform public.gq_cbc_context(p_session_id,p_access_token);
 select * into s from public.gq_sessions where id=p_session_id;
 if s.study_id<>p_study_id or s.is_test<>test or s.study_version is distinct from m->>'study_version' then raise exception 'session study mismatch'; end if;
 if s.lifecycle_state='withdrawn' then return public.greedyq_cbc_resume(s.id,p_access_token); end if;
 if m->'runtime_policy'->>'respondent_source'='prolific' then
  if p_external is null then raise exception 'Prolific identifiers required'; end if;
  if test and p_preview_token is not null then
   if s.preview_run_id='' and exists(select 1 from public.gq_external_identifiers where session_id=s.id) then raise exception 'existing panel response'; end if;
   update public.gq_sessions set preview_run_id=s.id::text where id=s.id;
  end if;
  perform public.greedyq_register_external(s.id,p_access_token,'prolific',p_external->>'PROLIFIC_PID',p_external->>'STUDY_ID',p_external->>'SESSION_ID');
 end if;
 return public.greedyq_cbc_resume(s.id,p_access_token);
end;$$;
revoke all on function public.greedyq_cbc_start(uuid,text,text,text,text,jsonb) from public;
grant execute on function public.greedyq_cbc_start(uuid,text,text,text,text,jsonb) to anon,authenticated;

create function public.gq_cbc_permute(items text[],enabled boolean) returns text[] language plpgsql volatile set search_path=public,pg_temp as $$
declare i integer; j integer; t text;
begin
 if enabled then for i in reverse cardinality(items)..2 loop j:=public.gq_random_below(i)+1;t:=items[i];items[i]:=items[j];items[j]:=t;end loop;end if;
 return items;
end;$$;
revoke all on function public.gq_cbc_permute(text[],boolean) from public,anon,authenticated;

-- Exposure/choice values contain all actual positions and feature codes for lossless archives.
create function public.gq_cbc_present(p_session_id uuid,m jsonb,state jsonb) returns void
language plpgsql security definer set search_path=public,pg_temp as $$
declare b jsonb; task jsonb; tid text; alternatives jsonb:='[]'; aid text; a jsonb; pos integer:=0; v jsonb;
begin
 tid:=state->'task_order'->>((state->>'index')::integer);
 select value into b from jsonb_array_elements(m->'cbc'->'blocks') where value->>'id'=state->>'block_id';
 select value into task from jsonb_array_elements(b->'tasks') where value->>'id'=tid;
 for aid in select jsonb_array_elements_text(state->'alternative_orders'->tid) loop
  pos:=pos+1; select value into a from jsonb_array_elements(task->'alternatives') where value->>'id'=aid;
  alternatives:=alternatives||jsonb_build_array(jsonb_build_object('id',aid,'display_position',pos,'is_none',false,'levels',a->'levels'));
 end loop;
 if (m->'cbc'->'none'->>'enabled')::boolean then alternatives:=alternatives||jsonb_build_array(jsonb_build_object('id','none','display_position',pos+1,'is_none',true,'levels','{}'::jsonb));end if;
 v:=jsonb_build_object('kind','cbc','design_version',m->'cbc'->>'schema_version','design_sha256',m->'cbc'->>'design_sha256','block_id',b->>'id','task_id',tid,'task_position',(state->>'index')::integer+1,'alternatives',alternatives,'choice',null,'served_at',clock_timestamp(),'presented_at',null,'answered_at',null);
 insert into public.gq_answers(session_id,question_id,value) values(p_session_id,'cbc:'||tid,v) on conflict(session_id,question_id) do nothing;
end;$$;
revoke all on function public.gq_cbc_present(uuid,jsonb,jsonb) from public,anon,authenticated;

create function public.greedyq_cbc_consent(p_session_id uuid,p_access_token text,p_decision text) returns jsonb
language plpgsql security definer set search_path=public,pg_temp as $$
declare m jsonb; s public.gq_sessions; state jsonb; chosen jsonb; item jsonb; task jsonb; orders jsonb:='{}'; tids text[]; aids text[]; total integer; draw integer;
begin
 m:=public.gq_cbc_context(p_session_id,p_access_token);select * into s from public.gq_sessions where id=p_session_id;
 if p_decision not in ('accepted','refused') or p_decision is null then raise exception 'invalid consent decision';end if;
 if s.lifecycle_state<>'created' then
  if (s.lifecycle_state='consent_refused' and p_decision='refused') or (s.lifecycle_state in ('in_progress','completed') and p_decision='accepted') then return public.greedyq_cbc_resume(s.id,p_access_token);end if;
  raise exception 'session ended';
 end if;
 insert into public.gq_consent_events(session_id,consent_id,consent_version,document_sha256,decision) values(s.id,m->'consent'->>'id',m->'consent'->>'version',m->'consent'->>'document_sha256',p_decision);
 if p_decision='refused' then
  update public.gq_sessions set lifecycle_state='consent_refused',current_page='consent_refused',browser_state=jsonb_build_object('phase','consent_refused','lifecycle','consent_refused','revision',1,'design_sha256',m->'cbc'->>'design_sha256'),updated_at=now() where id=s.id;
 else
  select sum((value->>'weight')::integer) into total from jsonb_array_elements(m->'cbc'->'blocks');draw:=public.gq_random_below(total);
  for item in select value from jsonb_array_elements(m->'cbc'->'blocks') loop draw:=draw-(item->>'weight')::integer;if draw<0 then chosen:=item;exit;end if;end loop;
  select array_agg(value->>'id' order by ordinal) into tids from jsonb_array_elements(chosen->'tasks') with ordinality t(value,ordinal);
  tids:=public.gq_cbc_permute(tids,m->'cbc'->>'task_order'='randomized_once_per_respondent');
  for task in select value from jsonb_array_elements(chosen->'tasks') loop
   select array_agg(value->>'id' order by ordinal) into aids from jsonb_array_elements(task->'alternatives') with ordinality a(value,ordinal);
   aids:=public.gq_cbc_permute(aids,m->'cbc'->>'alternative_order'='randomized_once_per_task');orders:=orders||jsonb_build_object(task->>'id',to_jsonb(aids));
  end loop;
  state:=jsonb_build_object('phase','tasks','lifecycle','in_progress','design_sha256',m->'cbc'->>'design_sha256','block_id',chosen->>'id','task_order',to_jsonb(tids),'alternative_orders',orders,'index',0,'answers','{}'::jsonb,'visited',jsonb_build_array(tids[1]),'completed',false,'withdrawn',false,'revision',1);
  insert into public.gq_assignments(session_id,randomization_id,condition,method,block_id,draw_id,spec_version) values(s.id,'cbc',chosen->>'id','simple',chosen->>'id',gen_random_uuid()::text,'0.3');
  update public.gq_sessions set browser_state=state,current_page='cbc:'||tids[1],lifecycle_state='in_progress',page_order=to_jsonb(tids),option_orders=orders,updated_at=now() where id=s.id;
  perform public.gq_cbc_present(s.id,m,state);
 end if;
 return public.greedyq_cbc_resume(s.id,p_access_token);
end;$$;
revoke all on function public.greedyq_cbc_consent(uuid,text,text) from public;
grant execute on function public.greedyq_cbc_consent(uuid,text,text) to anon,authenticated;

-- Browser-render acknowledgement is distinct from a server-prepared next task.
-- An answer also acknowledges its own task; a lost next-page response never invents a viewed task.
create function public.greedyq_cbc_ack(p_session_id uuid,p_access_token text,p_task_id text) returns void
language plpgsql security definer set search_path=public,pg_temp as $$
declare m jsonb;s public.gq_sessions;v jsonb;
begin
 m:=public.gq_cbc_context(p_session_id,p_access_token);select * into s from public.gq_sessions where id=p_session_id;
 if s.lifecycle_state in ('withdrawn','consent_refused','created') or not coalesce(s.browser_state->'visited' ? p_task_id,false) then raise exception 'task was not served';end if;
 select value into v from public.gq_answers where session_id=s.id and question_id='cbc:'||p_task_id;
 if v is null then raise exception 'task was not served';end if;
 if v->>'presented_at' is null then
  update public.gq_answers set value=v||jsonb_build_object('presented_at',clock_timestamp()) where session_id=s.id and question_id='cbc:'||p_task_id;
 end if;
end;$$;
revoke all on function public.greedyq_cbc_ack(uuid,text,text) from public;
grant execute on function public.greedyq_cbc_ack(uuid,text,text) to anon,authenticated;

create function public.greedyq_cbc_step(p_session_id uuid,p_access_token text,p_task_id text,p_choice text,p_direction text,p_revision integer,p_request_id uuid) returns jsonb
language plpgsql security definer set search_path=public,pg_temp as $$
declare m jsonb; s public.gq_sessions; st jsonb; v jsonb; idx integer; tid text; next_tid text; selected boolean;
begin
 m:=public.gq_cbc_context(p_session_id,p_access_token);select * into s from public.gq_sessions where id=p_session_id;st:=s.browser_state;
 if st->>'last_request_id'=p_request_id::text then return public.greedyq_cbc_resume(s.id,p_access_token);end if;
 if s.lifecycle_state<>'in_progress' then raise exception 'session ended';end if;
 if p_request_id is null or p_revision is distinct from (st->>'revision')::integer then raise exception 'CBC revision conflict';end if;
 idx:=(st->>'index')::integer;tid:=st->'task_order'->>idx;
 if p_task_id is distinct from tid or p_direction not in ('next','previous') or p_direction is null then raise exception 'invalid CBC step';end if;
 select value into v from public.gq_answers where session_id=s.id and question_id='cbc:'||tid;
 if v is null then raise exception 'task was not presented';end if;
 if p_choice is not null then
  if not exists(select 1 from jsonb_array_elements(v->'alternatives') a where a->>'id'=p_choice) then raise exception 'unknown alternative';end if;
  v:=v||jsonb_build_object('choice',p_choice,'presented_at',coalesce((v->>'presented_at')::timestamptz,clock_timestamp()),'answered_at',clock_timestamp());
  update public.gq_answers set value=v,answered_at=clock_timestamp() where session_id=s.id and question_id='cbc:'||tid;
  st:=jsonb_set(st,array['answers',tid],to_jsonb(p_choice));
 end if;
 if p_direction='next' and v->>'choice' is null then raise exception 'choice required';end if;
 if p_direction='previous' then if idx=0 then raise exception 'first task';end if;idx:=idx-1;
 elsif idx+1=jsonb_array_length(st->'task_order') then
  if exists(select 1 from jsonb_array_elements_text(st->'task_order') t where not exists(select 1 from public.gq_answers a where a.session_id=s.id and a.question_id='cbc:'||t and a.value->>'choice' is not null)) then raise exception 'unanswered task';end if;
  st:=st||'{"completed":true,"phase":"completed","lifecycle":"completed"}'::jsonb;
 else idx:=idx+1;end if;
 st:=st||jsonb_build_object('index',idx,'revision',p_revision+1,'last_request_id',p_request_id);
 if st->>'phase'='tasks' then
  next_tid:=st->'task_order'->>idx;
  if not st->'visited' ? next_tid then st:=jsonb_set(st,'{visited}',st->'visited'||jsonb_build_array(next_tid));end if;
  perform public.gq_cbc_present(s.id,m,st);
 end if;
 update public.gq_sessions set browser_state=st,current_page=case when st->>'phase'='completed' then 'completed' else 'cbc:'||next_tid end,lifecycle_state=st->>'lifecycle',updated_at=now() where id=s.id;
 return public.greedyq_cbc_resume(s.id,p_access_token);
end;$$;
revoke all on function public.greedyq_cbc_step(uuid,text,text,text,text,integer,uuid) from public;
grant execute on function public.greedyq_cbc_step(uuid,text,text,text,text,integer,uuid) to anon,authenticated;

create function public.greedyq_cbc_withdraw(p_session_id uuid,p_access_token text) returns jsonb
language plpgsql security definer set search_path=public,pg_temp as $$
begin
 perform public.gq_cbc_context(p_session_id,p_access_token);
 perform public.greedyq_withdraw_session(p_session_id,p_access_token);
 return public.greedyq_cbc_resume(p_session_id,p_access_token);
end;$$;
revoke all on function public.greedyq_cbc_withdraw(uuid,text) from public;
grant execute on function public.greedyq_cbc_withdraw(uuid,text) to anon,authenticated;

create function public.greedyq_issue_cbc_preview(p_study_id text) returns text
language plpgsql security definer set search_path=public,pg_temp as $$
declare token text;
begin
 if not exists(select 1 from public.gq_study_plans where study_id=p_study_id and model->>'kind'='cbc_study') then raise exception 'CBC study required';end if;
 token:=encode(extensions.gen_random_bytes(32),'hex');
 insert into public.gq_preview_grants values(encode(extensions.digest(token,'sha256'),'hex'),p_study_id,now()+interval '24 hours');return token;
end;$$;
revoke all on function public.greedyq_issue_cbc_preview(text) from public,anon,authenticated;
grant execute on function public.greedyq_issue_cbc_preview(text) to service_role;

-- The older general writer/creator/resumer must not bypass the CBC boundary.
alter function public.greedyq_create_session(uuid,text,text,text,text,text,boolean) rename to gq_create_session_before_cbc;
revoke all on function public.gq_create_session_before_cbc(uuid,text,text,text,text,text,boolean) from public,anon,authenticated;
create function public.greedyq_create_session(p_session_id uuid,p_access_token text,p_study_id text,p_study_version text,p_spec_version text,p_greedyq_version text,p_is_test boolean) returns void
language plpgsql security definer set search_path=public,pg_temp as $$
begin
 if exists(select 1 from public.gq_study_plans where study_id=p_study_id and model->>'kind'='cbc_study') then raise exception 'use CBC protocol';end if;
 perform public.gq_create_session_before_cbc(p_session_id,p_access_token,p_study_id,p_study_version,p_spec_version,p_greedyq_version,p_is_test);
end;$$;
revoke all on function public.greedyq_create_session(uuid,text,text,text,text,text,boolean) from public;
grant execute on function public.greedyq_create_session(uuid,text,text,text,text,text,boolean) to anon,authenticated;
alter function public.greedyq_save_session(uuid,text,jsonb,text) rename to gq_save_session_before_cbc;
revoke all on function public.gq_save_session_before_cbc(uuid,text,jsonb,text) from public,anon,authenticated;
create function public.greedyq_save_session(p_session_id uuid,p_access_token text,p_state jsonb,p_consent_question text) returns void
language plpgsql security definer set search_path=public,pg_temp as $$
begin
 if exists(select 1 from public.gq_sessions s join public.gq_study_plans p on s.study_id=p.study_id where s.id=p_session_id and p.model->>'kind'='cbc_study') then raise exception 'use CBC protocol';end if;
 perform public.gq_save_session_before_cbc(p_session_id,p_access_token,p_state,p_consent_question);
end;$$;
revoke all on function public.greedyq_save_session(uuid,text,jsonb,text) from public;
grant execute on function public.greedyq_save_session(uuid,text,jsonb,text) to anon,authenticated;
alter function public.greedyq_resume_session(uuid,text) rename to gq_resume_session_before_cbc;
revoke all on function public.gq_resume_session_before_cbc(uuid,text) from public,anon,authenticated;
create function public.greedyq_resume_session(p_session_id uuid,p_access_token text) returns jsonb
language plpgsql security definer set search_path=public,pg_temp as $$
begin
 if exists(select 1 from public.gq_sessions s join public.gq_study_plans p on s.study_id=p.study_id where s.id=p_session_id and p.model->>'kind'='cbc_study') then return public.greedyq_cbc_resume(p_session_id,p_access_token);end if;
 return public.gq_resume_session_before_cbc(p_session_id,p_access_token);
end;$$;
revoke all on function public.greedyq_resume_session(uuid,text) from public;
grant execute on function public.greedyq_resume_session(uuid,text) to anon,authenticated;
