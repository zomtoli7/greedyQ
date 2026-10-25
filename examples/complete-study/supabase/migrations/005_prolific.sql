-- Standard Prolific URL integration. Add after 004; never rewrite applied migrations.
alter table public.gq_external_identifiers add column greedyq_study_id text;
alter table public.gq_external_identifiers add column is_test boolean;
update public.gq_external_identifiers e set greedyq_study_id=s.study_id,is_test=s.is_test from public.gq_sessions s where s.id=e.session_id;
alter table public.gq_external_identifiers alter column greedyq_study_id set not null;
alter table public.gq_external_identifiers alter column is_test set not null;
alter table public.gq_external_identifiers drop constraint gq_external_identifiers_pkey;
alter table public.gq_external_identifiers add primary key(provider,participant_id,external_study_id,greedyq_study_id,is_test);
create unique index gq_external_submission_unique on public.gq_external_identifiers(provider,external_session_id,greedyq_study_id,is_test);
create unique index gq_external_session_unique on public.gq_external_identifiers(session_id,provider);

create or replace function public.greedyq_register_external(p_session_id uuid,p_access_token text,p_provider text,p_participant_id text,p_external_study_id text,p_external_session_id text)
returns void language plpgsql security definer set search_path=public,pg_temp as $$
declare s public.gq_sessions; model jsonb; old public.gq_external_identifiers;
begin
  select * into s from public.gq_sessions where id=p_session_id for update;
  if not found or not public.greedyq_token_ok(p_session_id,p_access_token) then raise exception 'invalid session capability'; end if;
  select p.model into model from public.gq_study_plans p where p.study_id=s.study_id;
  if model is null or model->'runtime_policy'->>'respondent_source' is distinct from 'prolific' then raise exception 'Prolific study plan not registered'; end if;
  if p_provider is distinct from 'prolific' or p_participant_id is null or p_external_study_id is null or p_external_session_id is null
     or p_participant_id !~ '^[A-Za-z0-9_-]{1,200}$' or p_external_study_id !~ '^[A-Za-z0-9_-]{1,200}$' or p_external_session_id !~ '^[A-Za-z0-9_-]{1,200}$'
     then raise exception 'invalid Prolific identifiers'; end if;
  if not s.is_test and (p_participant_id !~ '^[a-fA-F0-9]{24}$' or p_external_study_id !~ '^[a-fA-F0-9]{24}$' or p_external_session_id !~ '^[a-fA-F0-9]{24}$') then raise exception 'invalid production Prolific identifiers'; end if;
  if not s.is_test and (model->'runtime_policy'->'prolific'->>'study_id' is null or model->'runtime_policy'->'prolific'->>'study_id' is distinct from p_external_study_id) then raise exception 'Prolific study mismatch'; end if;
  if model->'runtime_policy'->'prolific'->>'study_id' is not null and model->'runtime_policy'->'prolific'->>'study_id' is distinct from p_external_study_id then raise exception 'Prolific study mismatch'; end if;
  select * into old from public.gq_external_identifiers where session_id=s.id and provider='prolific';
  if found then
    if old.participant_id is distinct from p_participant_id or old.external_study_id is distinct from p_external_study_id or old.external_session_id is distinct from p_external_session_id then raise exception 'Prolific identifiers are immutable'; end if;
    return;
  end if;
  insert into public.gq_external_identifiers(session_id,provider,participant_id,external_study_id,external_session_id,greedyq_study_id,is_test)
  values(s.id,p_provider,p_participant_id,p_external_study_id,p_external_session_id,s.study_id,s.is_test);
  update public.gq_sessions set respondent_source='prolific',updated_at=now() where id=s.id;
exception when unique_violation then raise exception 'duplicate Prolific participant or submission';
end;$$;

create function public.greedyq_start_prolific(p_session_id uuid,p_access_token text,p_study_id text,p_study_version text,p_spec_version text,p_greedyq_version text,p_is_test boolean,p_participant_id text,p_external_study_id text,p_external_session_id text)
returns void language plpgsql security definer set search_path=public,pg_temp as $$
declare model jsonb; s public.gq_sessions;
begin
  select p.model into model from public.gq_study_plans p where p.study_id=p_study_id;
  if model is null or model->>'study_version' is distinct from p_study_version or (model->'runtime_policy'->>'mode'='production') is distinct from (not p_is_test) then raise exception 'session study mismatch'; end if;
  perform public.greedyq_create_session(p_session_id,p_access_token,p_study_id,p_study_version,p_spec_version,p_greedyq_version,p_is_test);
  select * into s from public.gq_sessions where id=p_session_id for update;
  if s.study_id<>p_study_id or s.study_version<>p_study_version or s.is_test<>p_is_test then raise exception 'session study mismatch'; end if;
  perform public.greedyq_register_external(p_session_id,p_access_token,'prolific',p_participant_id,p_external_study_id,p_external_session_id);
end;$$;
revoke all on function public.greedyq_start_prolific(uuid,text,text,text,text,text,boolean,text,text,text) from public;
grant execute on function public.greedyq_start_prolific(uuid,text,text,text,text,text,boolean,text,text,text) to anon,authenticated;

create function public.gq_prolific_guard() returns trigger language plpgsql security definer set search_path=public,pg_temp as $$
declare s public.gq_sessions; model jsonb;
begin
  if TG_TABLE_NAME='gq_sessions' then s:=new;
  else select * into s from public.gq_sessions where id=new.session_id; end if;
  if s.lifecycle_state='withdrawn' then return new; end if;
  if not s.is_test then
    select p.model into model from public.gq_study_plans p where p.study_id=s.study_id;
    if model->'runtime_policy'->>'respondent_source'='prolific' and not exists(select 1 from public.gq_external_identifiers where session_id=s.id and provider='prolific') then
      raise exception 'Prolific registration required before responses or assignment';
    end if;
  end if;
  return new;
end;$$;
revoke all on function public.gq_prolific_guard() from public,anon,authenticated;
create trigger gq_prolific_guard before update on public.gq_sessions for each row execute function public.gq_prolific_guard();
create trigger gq_prolific_guard before insert or update on public.gq_answers for each row execute function public.gq_prolific_guard();
create trigger gq_prolific_guard before insert or update on public.gq_assignments for each row execute function public.gq_prolific_guard();
