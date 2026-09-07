create extension if not exists pgcrypto;

create table public.gq_sessions (
  id uuid primary key default gen_random_uuid(),
  study_id text not null,
  study_version text not null,
  spec_version text not null,
  current_page text not null default 'welcome',
  is_test boolean not null default false,
  lifecycle_state text not null default 'created' check (
    lifecycle_state in (
      'created', 'consented', 'in_progress', 'completed', 'screened_out',
      'consent_refused', 'withdrawn', 'technical_error'
    )
  ),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  terminal_at timestamptz
);

create table public.gq_external_identifiers (
  session_id uuid not null references public.gq_sessions(id) on delete cascade,
  provider text not null,
  participant_id text not null,
  external_study_id text,
  external_session_id text,
  created_at timestamptz not null default now(),
  primary key (provider, participant_id, external_study_id)
);

create table public.gq_consent_events (
  id bigint generated always as identity primary key,
  session_id uuid not null references public.gq_sessions(id) on delete cascade,
  consent_id text not null,
  consent_version text not null,
  document_sha256 text not null check (document_sha256 ~ '^[0-9a-f]{64}$'),
  decision text not null check (decision in ('accepted', 'refused', 'withdrawn')),
  occurred_at timestamptz not null default now()
);

create table public.gq_answers (
  session_id uuid not null references public.gq_sessions(id) on delete cascade,
  question_id text not null,
  value jsonb,
  answered_at timestamptz not null default now(),
  cleared_at timestamptz,
  primary key (session_id, question_id)
);

create table public.gq_assignments (
  session_id uuid not null references public.gq_sessions(id) on delete cascade,
  randomization_id text not null,
  condition text not null,
  method text not null,
  block_id text,
  draw_id text not null,
  spec_version text not null,
  assigned_at timestamptz not null default now(),
  primary key (session_id, randomization_id)
);

create table public.gq_lifecycle_events (
  id bigint generated always as identity primary key,
  session_id uuid not null references public.gq_sessions(id) on delete cascade,
  from_state text,
  to_state text not null,
  page_id text,
  metadata jsonb not null default '{}'::jsonb,
  occurred_at timestamptz not null default now()
);

create table public.gq_data_requests (
  id bigint generated always as identity primary key,
  session_id uuid not null references public.gq_sessions(id) on delete cascade,
  request_type text not null check (request_type in ('deletion', 'withdrawal')),
  status text not null default 'recorded' check (
    status in ('recorded', 'reviewing', 'completed', 'denied_with_reason')
  ),
  requested_at timestamptz not null default now(),
  resolved_at timestamptz
);

alter table public.gq_sessions enable row level security;
alter table public.gq_external_identifiers enable row level security;
alter table public.gq_consent_events enable row level security;
alter table public.gq_answers enable row level security;
alter table public.gq_assignments enable row level security;
alter table public.gq_lifecycle_events enable row level security;
alter table public.gq_data_requests enable row level security;

-- The reference runtime writes through server-controlled functions or a server role.
-- No direct anonymous SELECT policy is created; respondents cannot enumerate study data.

-- Canonical withdrawal operation. The server role calls this function inside one
-- transaction. Repeated calls are safe and do not recreate deleted research data.
create or replace function public.gq_withdraw_and_delete(p_session_id uuid)
returns void
language plpgsql
security definer
set search_path = public, pg_temp
as $$
declare
  v_state text;
begin
  select lifecycle_state
    into v_state
    from public.gq_sessions
   where id = p_session_id
   for update;

  if not found then
    raise exception 'unknown greedyQ session';
  end if;

  if v_state = 'withdrawn' then
    return;
  end if;

  delete from public.gq_answers where session_id = p_session_id;
  delete from public.gq_assignments where session_id = p_session_id;
  delete from public.gq_external_identifiers where session_id = p_session_id;
  delete from public.gq_consent_events where session_id = p_session_id;
  delete from public.gq_data_requests where session_id = p_session_id;

  update public.gq_sessions
     set lifecycle_state = 'withdrawn',
         current_page = 'withdrawn',
         updated_at = now(),
         terminal_at = coalesce(terminal_at, now())
   where id = p_session_id;

  insert into public.gq_lifecycle_events (
    session_id, from_state, to_state, page_id, metadata
  ) values (
    p_session_id, v_state, 'withdrawn', 'withdrawn',
    jsonb_build_object('research_data_deleted', true)
  );
end;
$$;

revoke all on function public.gq_withdraw_and_delete(uuid) from public;
grant execute on function public.gq_withdraw_and_delete(uuid) to service_role;

-- Canonical analysis boundary. It exposes completed, non-test sessions and their
-- answers as a stable JSON object while deliberately omitting external identifiers.
create or replace view public.gq_analysis_export
with (security_invoker = true)
as
select
  s.id as session_id,
  s.study_id,
  s.study_version,
  s.spec_version,
  s.created_at,
  s.terminal_at as completed_at,
  coalesce(
    jsonb_object_agg(a.question_id, a.value)
      filter (where a.question_id is not null),
    '{}'::jsonb
  ) as answers
from public.gq_sessions s
left join public.gq_answers a on a.session_id = s.id
where s.lifecycle_state = 'completed'
  and not s.is_test
group by s.id;

-- The deployment creates/maps this NOLOGIN role for the authenticated analysis
-- identity. RLS and grants are both required; either one alone is insufficient.
do $$
begin
  if not exists (select 1 from pg_roles where rolname = 'gq_analyst') then
    create role gq_analyst nologin;
  end if;
end
$$;

create policy gq_analyst_sessions_read on public.gq_sessions
  for select to gq_analyst
  using (lifecycle_state = 'completed' and not is_test);

create policy gq_analyst_answers_read on public.gq_answers
  for select to gq_analyst
  using (
    exists (
      select 1 from public.gq_sessions s
       where s.id = gq_answers.session_id
         and s.lifecycle_state = 'completed'
         and not s.is_test
    )
  );

grant usage on schema public to gq_analyst;
grant select on public.gq_sessions, public.gq_answers to gq_analyst;
grant select on public.gq_analysis_export to gq_analyst;
-- Never grant gq_external_identifiers to gq_analyst.
