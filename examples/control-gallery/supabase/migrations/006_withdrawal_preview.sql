-- Additive upgrade: future withdrawals erase answers atomically; no historical rewrite.
alter function public.greedyq_save_session(uuid,text,jsonb,text) rename to gq_save_session_validated;
revoke all on function public.gq_save_session_validated(uuid,text,jsonb,text) from public,anon,authenticated;

create or replace function public.greedyq_withdraw_session(p_session_id uuid,p_access_token text)
returns void language plpgsql security definer set search_path=public,pg_temp as $$
declare s public.gq_sessions; model jsonb; ending text;
begin
  select * into s from public.gq_sessions where id=p_session_id for update;
  if not found or not public.greedyq_token_ok(p_session_id,p_access_token) then raise exception 'invalid session capability'; end if;
  if s.lifecycle_state='withdrawn' then return; end if;
  select p.model into model from public.gq_study_plans p where p.study_id=s.study_id;
  select p->>'id' into ending from jsonb_array_elements(model->'pages') p where p->>'terminal'='withdrawn' limit 1;
  ending:=coalesce(ending,'withdrawn');
  delete from public.gq_answers where session_id=s.id;
  delete from public.gq_assignments where session_id=s.id;
  delete from public.gq_consent_events where session_id=s.id;
  delete from public.gq_data_requests where session_id=s.id;
  -- Minimal external identifiers remain for platform return and duplicate prevention.
  -- Allocation sequences remain consumed. Never recycle a withdrawn allocation.
  delete from public.gq_lifecycle_events where session_id=s.id;
  update public.gq_sessions set lifecycle_state='withdrawn',current_page=ending,
    browser_state=jsonb_build_object('page',ending,'lifecycle','withdrawn','answers','{}'::jsonb,'history','[]'::jsonb,'visited',jsonb_build_array(ending),'condition',null,'consent_accepted',false),
    updated_at=now(),terminal_at=coalesce(terminal_at,now()) where id=s.id;
  insert into public.gq_lifecycle_events(session_id,from_state,to_state,page_id,metadata)
    values(s.id,s.lifecycle_state,'withdrawn',ending,'{"research_data_deleted":true}'::jsonb);
end;$$;

create function public.greedyq_save_session(p_session_id uuid,p_access_token text,p_state jsonb,p_consent_question text)
returns void language plpgsql security definer set search_path=public,pg_temp as $$
begin
  if p_state->>'lifecycle'='withdrawn' then
    perform public.greedyq_withdraw_session(p_session_id,p_access_token);
  else
    perform public.gq_save_session_validated(p_session_id,p_access_token,p_state,p_consent_question);
  end if;
end;$$;
revoke all on function public.greedyq_save_session(uuid,text,jsonb,text) from public;
grant execute on function public.greedyq_save_session(uuid,text,jsonb,text) to anon,authenticated;

-- Only an authenticated researcher dashboard/agent can issue a 24-hour test grant.
create table public.gq_preview_grants (
  token_hash text primary key,
  study_id text not null references public.gq_study_plans(study_id),
  expires_at timestamptz not null
);
alter table public.gq_preview_grants enable row level security;
revoke all on public.gq_preview_grants from public,anon,authenticated;
alter table public.gq_sessions add column preview_run_id text not null default '';
alter table public.gq_external_identifiers add column preview_run_id text not null default '';
alter table public.gq_external_identifiers drop constraint gq_external_identifiers_pkey;
alter table public.gq_external_identifiers add primary key(provider,participant_id,external_study_id,greedyq_study_id,is_test,preview_run_id);
drop index public.gq_external_submission_unique;
create unique index gq_external_submission_unique on public.gq_external_identifiers(provider,external_session_id,greedyq_study_id,is_test,preview_run_id);

create function public.gq_set_preview_namespace() returns trigger language plpgsql security definer set search_path=public,pg_temp as $$
begin
  select preview_run_id into new.preview_run_id from public.gq_sessions where id=new.session_id;
  return new;
end;$$;
revoke all on function public.gq_set_preview_namespace() from public,anon,authenticated;
create trigger gq_preview_namespace before insert on public.gq_external_identifiers for each row execute function public.gq_set_preview_namespace();

create function public.greedyq_issue_preview(p_study_id text) returns text language plpgsql security definer set search_path=public,pg_temp as $$
declare token text;
begin
  if not exists(select 1 from public.gq_study_plans where study_id=p_study_id and model->'runtime_policy'->>'mode'='test' and model->'runtime_policy'->>'respondent_source'='prolific') then raise exception 'preview requires a registered Prolific test study'; end if;
  token:=encode(extensions.gen_random_bytes(32),'hex');
  insert into public.gq_preview_grants values(encode(extensions.digest(token,'sha256'),'hex'),p_study_id,now()+interval '24 hours');
  return token;
end;$$;
revoke all on function public.greedyq_issue_preview(text) from public,anon,authenticated;
grant execute on function public.greedyq_issue_preview(text) to service_role;

create function public.greedyq_start_prolific_preview(p_session_id uuid,p_access_token text,p_study_id text,p_study_version text,p_spec_version text,p_greedyq_version text,p_is_test boolean,p_participant_id text,p_external_study_id text,p_external_session_id text,p_preview_token text)
returns void language plpgsql security definer set search_path=public,pg_temp as $$
declare s public.gq_sessions;
begin
  if p_is_test is distinct from true or not exists(select 1 from public.gq_study_plans where study_id=p_study_id and model->'runtime_policy'->>'mode'='test') then raise exception 'preview forbidden in production'; end if;
  if not exists(select 1 from public.gq_preview_grants where token_hash=encode(extensions.digest(p_preview_token,'sha256'),'hex') and study_id=p_study_id and expires_at>now()) then raise exception 'invalid or expired preview grant'; end if;
  perform public.greedyq_create_session(p_session_id,p_access_token,p_study_id,p_study_version,p_spec_version,p_greedyq_version,true);
  select * into s from public.gq_sessions where id=p_session_id for update;
  if s.study_id<>p_study_id or s.study_version<>p_study_version or not s.is_test then raise exception 'session study mismatch'; end if;
  if s.preview_run_id='' and exists(select 1 from public.gq_external_identifiers where session_id=s.id) then raise exception 'cannot convert an existing panel response to preview'; end if;
  update public.gq_sessions set preview_run_id=p_session_id::text where id=s.id;
  perform public.greedyq_start_prolific(p_session_id,p_access_token,p_study_id,p_study_version,p_spec_version,p_greedyq_version,true,p_participant_id,p_external_study_id,p_external_session_id);
end;$$;
revoke all on function public.greedyq_start_prolific_preview(uuid,text,text,text,text,text,boolean,text,text,text,text) from public;
grant execute on function public.greedyq_start_prolific_preview(uuid,text,text,text,text,text,boolean,text,text,text,text) to anon,authenticated;
