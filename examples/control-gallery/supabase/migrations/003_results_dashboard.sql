-- greedyQ v0.2 results metadata migration. Apply after 002_browser_rpc.sql.
alter table public.gq_sessions add column if not exists respondent_source text not null default 'direct';

update public.gq_sessions s
set respondent_source = 'prolific'
where exists (
  select 1 from public.gq_external_identifiers e
  where e.session_id = s.id and e.provider = 'prolific'
);

do $$ begin
  if not exists (
    select 1 from pg_constraint where conname = 'gq_sessions_respondent_source_check'
  ) then
    alter table public.gq_sessions add constraint gq_sessions_respondent_source_check
      check (respondent_source in ('direct','prolific'));
  end if;
end $$;
