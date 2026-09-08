-- greedyQ v0.2 browser RPC boundary. Apply after 001_initial.sql.
alter table public.gq_sessions add column if not exists access_token_hash text;
alter table public.gq_sessions add column if not exists browser_state jsonb not null default '{}'::jsonb;

create or replace function public.greedyq_token_ok(p_session_id uuid, p_access_token text)
returns boolean language sql stable security definer set search_path=public,pg_temp as $$
  select exists(select 1 from public.gq_sessions where id=p_session_id and access_token_hash=encode(digest(p_access_token,'sha256'),'hex'));
$$;

create or replace function public.greedyq_resume_session(p_session_id uuid, p_access_token text)
returns jsonb language sql stable security definer set search_path=public,pg_temp as $$
  select case when public.greedyq_token_ok(p_session_id,p_access_token)
    then jsonb_build_object('state',browser_state,'condition',(select condition from public.gq_assignments where session_id=p_session_id order by assigned_at limit 1))
    else null end from public.gq_sessions where id=p_session_id;
$$;

create or replace function public.greedyq_assign_condition(p_session_id uuid,p_access_token text,p_study_id text,p_study_version text,p_spec_version text,p_conditions text[],p_is_test boolean)
returns text language plpgsql security definer set search_path=public,pg_temp as $$
declare v_condition text; v_min bigint;
begin
  if coalesce(array_length(p_conditions,1),0)<1 then raise exception 'conditions required'; end if;
  perform pg_advisory_xact_lock(hashtext(p_study_id));
  insert into public.gq_sessions(id,study_id,study_version,spec_version,is_test,access_token_hash)
  values(p_session_id,p_study_id,p_study_version,p_spec_version,p_is_test,encode(digest(p_access_token,'sha256'),'hex')) on conflict(id) do nothing;
  if not public.greedyq_token_ok(p_session_id,p_access_token) then raise exception 'invalid session capability'; end if;
  select condition into v_condition from public.gq_assignments where session_id=p_session_id order by assigned_at limit 1;
  if v_condition is not null then return v_condition; end if;
  select min(n) into v_min from (select c,count(a.condition) filter(where s.id is not null) n from unnest(p_conditions)c left join public.gq_assignments a on a.condition=c left join public.gq_sessions s on s.id=a.session_id and s.study_id=p_study_id group by c)q;
  select c into v_condition from unnest(p_conditions)c left join public.gq_assignments a on a.condition=c left join public.gq_sessions s on s.id=a.session_id and s.study_id=p_study_id group by c having count(a.condition) filter(where s.id is not null)=v_min order by c limit 1;
  insert into public.gq_assignments(session_id,randomization_id,condition,method,draw_id,spec_version) values(p_session_id,'primary',v_condition,'least_count_locked',gen_random_uuid()::text,p_spec_version);
  return v_condition;
end;$$;

create or replace function public.greedyq_save_session(p_session_id uuid,p_access_token text,p_state jsonb,p_consent_question text)
returns void language plpgsql security definer set search_path=public,pg_temp as $$
declare v_answers jsonb:=coalesce(p_state->'answers','{}'::jsonb); v_key text; v_value jsonb;
begin
  if not public.greedyq_token_ok(p_session_id,p_access_token) then raise exception 'invalid session capability'; end if;
  if coalesce((p_state->>'consent_accepted')::boolean,false)=false and (select count(*) from jsonb_object_keys(v_answers) k where k<>p_consent_question)>0 then raise exception 'research data cannot be saved before consent'; end if;
  update public.gq_sessions set browser_state=p_state,current_page=coalesce(p_state->>'page',current_page),lifecycle_state=coalesce(p_state->>'lifecycle',lifecycle_state),updated_at=now() where id=p_session_id;
  for v_key,v_value in select * from jsonb_each(v_answers) loop
    if v_key=p_consent_question or coalesce((p_state->>'consent_accepted')::boolean,false) then insert into public.gq_answers(session_id,question_id,value) values(p_session_id,v_key,v_value) on conflict(session_id,question_id) do update set value=excluded.value,answered_at=now(); end if;
  end loop;
end;$$;

create or replace function public.greedyq_register_external(p_session_id uuid,p_access_token text,p_provider text,p_participant_id text,p_external_study_id text,p_external_session_id text)
returns void language plpgsql security definer set search_path=public,pg_temp as $$
begin
  if not public.greedyq_token_ok(p_session_id,p_access_token) then raise exception 'invalid session capability'; end if;
  if p_provider<>'prolific' or coalesce(length(p_participant_id),0)<1 or length(p_participant_id)>200 then raise exception 'invalid external participant identifier'; end if;
  insert into public.gq_external_identifiers(session_id,provider,participant_id,external_study_id,external_session_id)
  values(p_session_id,p_provider,p_participant_id,p_external_study_id,p_external_session_id)
  on conflict(provider,participant_id,external_study_id) do update set external_session_id=excluded.external_session_id
  where public.gq_external_identifiers.session_id=excluded.session_id;
  if not found then raise exception 'duplicate participant'; end if;
end;$$;

create or replace function public.greedyq_withdraw_session(p_session_id uuid,p_access_token text)
returns void language plpgsql security definer set search_path=public,pg_temp as $$
declare v_state text;
begin
  if not public.greedyq_token_ok(p_session_id,p_access_token) then raise exception 'invalid session capability'; end if;
  select lifecycle_state into v_state from public.gq_sessions where id=p_session_id for update;
  if v_state='withdrawn' then return; end if;
  delete from public.gq_answers where session_id=p_session_id; delete from public.gq_assignments where session_id=p_session_id; delete from public.gq_external_identifiers where session_id=p_session_id; delete from public.gq_consent_events where session_id=p_session_id;
  update public.gq_sessions set lifecycle_state='withdrawn',current_page='withdrawn',browser_state='{"lifecycle":"withdrawn"}'::jsonb,updated_at=now(),terminal_at=coalesce(terminal_at,now()) where id=p_session_id;
  insert into public.gq_lifecycle_events(session_id,from_state,to_state,page_id,metadata) values(p_session_id,v_state,'withdrawn','withdrawn',jsonb_build_object('research_data_deleted',true));
end;$$;

revoke all on function public.greedyq_token_ok(uuid,text),public.greedyq_resume_session(uuid,text),public.greedyq_assign_condition(uuid,text,text,text,text,text[],boolean),public.greedyq_save_session(uuid,text,jsonb,text),public.greedyq_register_external(uuid,text,text,text,text,text),public.greedyq_withdraw_session(uuid,text) from public;
grant execute on function public.greedyq_resume_session(uuid,text),public.greedyq_assign_condition(uuid,text,text,text,text,text[],boolean),public.greedyq_save_session(uuid,text,jsonb,text),public.greedyq_register_external(uuid,text,text,text,text,text),public.greedyq_withdraw_session(uuid,text) to anon,authenticated;
