-- Additive upgrade. Keep 001-003 unchanged so existing migration ledgers remain valid.
-- Register the reviewed model using the agent-side registerStudy() operation before fielding.
alter table public.gq_sessions add column question_orders jsonb not null default '{}'::jsonb;
alter table public.gq_sessions add column option_orders jsonb not null default '{}'::jsonb;
alter table public.gq_sessions add column page_order jsonb not null default '[]'::jsonb;
create function public.gq_clear_question_orders() returns trigger language plpgsql set search_path=public,pg_temp as $$
begin
  if new.lifecycle_state='withdrawn' then new.question_orders:='{}'::jsonb; new.option_orders:='{}'::jsonb; new.page_order:='[]'::jsonb; end if;
  return new;
end;$$;
revoke all on function public.gq_clear_question_orders() from public,anon,authenticated;
create trigger gq_clear_question_orders before update on public.gq_sessions for each row execute function public.gq_clear_question_orders();
create table public.gq_study_plans (
  study_id text primary key,
  model jsonb not null,
  registered_at timestamptz not null default now()
);
create table public.gq_allocation_sequences (
  study_id text not null references public.gq_study_plans(study_id),
  randomization_id text not null,
  is_test boolean not null,
  remaining text[] not null default '{}',
  block_number bigint not null default 0,
  primary key(study_id,randomization_id,is_test)
);
alter table public.gq_study_plans enable row level security;
alter table public.gq_allocation_sequences enable row level security;
revoke all on public.gq_study_plans,public.gq_allocation_sequences from public,anon,authenticated;

-- Reserved synthetic diagnostic fixture, used only by connection-test.html.
insert into public.gq_study_plans(study_id,model) values('greedyq_connection_test',
  '{"study_id":"greedyq_connection_test","assignment_page":"consent","randomization":{"id":"connection_test","unit":"respondent","persistence_key":"session_id","method":"simple","conditions":{"control":1,"treatment":1}},"runtime_policy":{"consent":{"question":"consent_choice","accept_value":"yes"}},"pages":[{"id":"consent","questions":[{"id":"consent_choice"}]},{"id":"questions","questions":[{"id":"connection_test_answer"}]}]}'::jsonb);

create function public.gq_random_below(n integer) returns integer
language plpgsql volatile set search_path=public,pg_temp as $$
declare b bytea; x bigint; ceiling bigint;
begin
  if n is null or n<1 then raise exception 'invalid random bound'; end if;
  ceiling:=4294967296-(4294967296 % n);
  loop
    b:=extensions.gen_random_bytes(4);
    x:=get_byte(b,0)::bigint*16777216+get_byte(b,1)::bigint*65536+get_byte(b,2)::bigint*256+get_byte(b,3);
    exit when x<ceiling;
  end loop;
  return (x % n)::integer;
end;$$;
revoke all on function public.gq_random_below(integer) from public,anon,authenticated;

create or replace function public.greedyq_resume_session(p_session_id uuid,p_access_token text)
returns jsonb language sql stable security definer set search_path=public,pg_temp as $$
  select case when public.greedyq_token_ok(p_session_id,p_access_token) then jsonb_build_object(
    'runtime_contract','randomization-1',
    'registered_model',(select model from public.gq_study_plans p where p.study_id=s.study_id),
    'state',s.browser_state,
    'condition',(select condition from public.gq_assignments where session_id=s.id order by assigned_at limit 1))
    else null end from public.gq_sessions s where id=p_session_id;
$$;

create or replace function public.greedyq_assign_condition(p_session_id uuid,p_access_token text,p_study_id text,p_study_version text,p_spec_version text,p_greedyq_version text,p_conditions text[],p_is_test boolean)
returns text language plpgsql security definer set search_path=public,pg_temp as $$
declare s public.gq_sessions; model jsonb; plan jsonb; seq public.gq_allocation_sequences;
  chosen text; block text; total integer; n integer; i integer; j integer; size integer;
  item record; pool text[]; tmp text; consent jsonb;
begin
  -- Lock ordering matches the save boundary: session first, then per-study allocation state.
  select * into s from public.gq_sessions where id=p_session_id for update;
  if not found or not public.greedyq_token_ok(p_session_id,p_access_token) then raise exception 'invalid session capability'; end if;
  if s.study_id<>p_study_id or s.study_version<>p_study_version or s.is_test<>p_is_test then raise exception 'session study mismatch'; end if;
  if s.lifecycle_state in ('withdrawn','completed','screened_out','consent_refused','technical_error') then raise exception 'session ended'; end if;
  select p.model into model from public.gq_study_plans p where p.study_id=s.study_id;
  if model is null then raise exception 'reviewed study plan not registered'; end if;
  plan:=model->'randomization';
  if plan is null then return 'default'; end if;
  select condition into chosen from public.gq_assignments where session_id=s.id and randomization_id=plan->>'id';
  if chosen is not null then return chosen; end if;
  if s.current_page is distinct from model->>'assignment_page' then raise exception 'not at assignment point'; end if;
  consent:=model->'runtime_policy'->'consent';
  if consent is not null and consent<>'null'::jsonb and s.browser_state->'answers'->(consent->>'question') is distinct from consent->'accept_value' then raise exception 'consent required before assignment'; end if;
  if plan->>'method' not in ('simple','fixed_block') then raise exception 'unsupported randomization method'; end if;
  select sum(value::integer) into total from jsonb_each_text(plan->'conditions');
  if total is null or total<2 or total>1000 or exists(select 1 from jsonb_each_text(plan->'conditions') where value::integer<1) then raise exception 'invalid weights'; end if;
  perform pg_advisory_xact_lock(hashtext(s.study_id || ':' || (plan->>'id') || ':' || s.is_test::text));
  if plan->>'method'='simple' then
    n:=public.gq_random_below(total);
    for item in select key,value::integer w from jsonb_each_text(plan->'conditions') order by key loop
      n:=n-item.w;
      if n<0 then chosen:=item.key; exit; end if;
    end loop;
  else
    size:=(plan->>'block_size')::integer;
    if size is null or size<2 or size>1000 or size % total<>0 then raise exception 'invalid block size'; end if;
    insert into public.gq_allocation_sequences(study_id,randomization_id,is_test) values(s.study_id,plan->>'id',s.is_test) on conflict do nothing;
    select * into seq from public.gq_allocation_sequences where study_id=s.study_id and randomization_id=plan->>'id' and is_test=s.is_test for update;
    pool:=seq.remaining;
    if cardinality(pool)=0 then
      for item in select key,value::integer w from jsonb_each_text(plan->'conditions') order by key loop
        for i in 1..(item.w*size/total) loop pool:=array_append(pool,item.key); end loop;
      end loop;
      for i in reverse cardinality(pool)..2 loop
        j:=public.gq_random_below(i)+1; tmp:=pool[i]; pool[i]:=pool[j]; pool[j]:=tmp;
      end loop;
      seq.block_number:=seq.block_number+1;
    end if;
    chosen:=pool[1]; block:=seq.block_number::text;
    update public.gq_allocation_sequences set remaining=pool[2:cardinality(pool)],block_number=seq.block_number where study_id=s.study_id and randomization_id=plan->>'id' and is_test=s.is_test;
  end if;
  insert into public.gq_assignments(session_id,randomization_id,condition,method,block_id,draw_id,spec_version)
    values(s.id,plan->>'id',chosen,plan->>'method',block,gen_random_uuid()::text,s.spec_version);
  return chosen;
end;$$;

-- Preserve the audited answer writer, adding a trusted plan and stable-order boundary.
alter function public.greedyq_save_session(uuid,text,jsonb,text) rename to gq_save_session_legacy;
revoke all on function public.gq_save_session_legacy(uuid,text,jsonb,text) from public,anon,authenticated;
create function public.greedyq_save_session(p_session_id uuid,p_access_token text,p_state jsonb,p_consent_question text)
returns void language plpgsql security definer set search_path=public,pg_temp as $$
declare s public.gq_sessions; model jsonb; consent jsonb; state jsonb:=p_state; assigned text; pair record;
  page jsonb; expected text[]; actual text[]; k integer; selected jsonb; question jsonb;
begin
  select * into s from public.gq_sessions where id=p_session_id for update;
  if not found or not public.greedyq_token_ok(p_session_id,p_access_token) then raise exception 'invalid session capability'; end if;
  if s.lifecycle_state='withdrawn' then raise exception 'session ended'; end if;
  select p.model into model from public.gq_study_plans p where p.study_id=s.study_id;
  if model is null then raise exception 'reviewed study plan not registered'; end if;
  consent:=model->'runtime_policy'->'consent';
  state:=jsonb_set(state,'{consent_accepted}',to_jsonb(consent is null or consent='null'::jsonb or coalesce(state->'answers'->(consent->>'question')=consent->'accept_value',false)));
  select condition into assigned from public.gq_assignments where session_id=s.id order by assigned_at limit 1;
  if model->'randomization' is not null then
    if state->>'condition' is not null and state->>'condition' is distinct from assigned then raise exception 'assignment mismatch'; end if;
    state:=jsonb_set(state,'{condition}',coalesce(to_jsonb(assigned),'null'::jsonb));
  end if;
  for pair in select * from jsonb_each(coalesce(s.browser_state->'question_orders','{}'::jsonb)) loop
    if state->'question_orders'->pair.key is distinct from pair.value then raise exception 'question order changed'; end if;
  end loop;
  for pair in select * from jsonb_each(coalesce(state->'question_orders','{}'::jsonb)) loop
    select p into page from jsonb_array_elements(model->'pages') p where p->>'id'=pair.key;
    if page is null or jsonb_typeof(pair.value)<>'array' then raise exception 'invalid question order'; end if;
    select coalesce(array_agg(q->>'id'),'{}') into expected from jsonb_array_elements(page->'questions') q;
    select coalesce(array_agg(q),'{}') into actual from jsonb_array_elements_text(pair.value) q;
    if cardinality(expected)<>cardinality(actual) or not (expected @> actual and actual @> expected) then raise exception 'question order is not a permutation'; end if;
    selected:=coalesce(page->'shuffle_questions','[]'::jsonb);
    for k in 1..cardinality(expected) loop
      if not selected ? expected[k] and actual[k]<>expected[k] then raise exception 'fixed question moved'; end if;
    end loop;
  end loop;
  for pair in select * from jsonb_each(coalesce(s.browser_state->'option_orders','{}'::jsonb)) loop
    if state->'option_orders'->pair.key is distinct from pair.value then raise exception 'option order changed'; end if;
  end loop;
  for pair in select * from jsonb_each(coalesce(state->'option_orders','{}'::jsonb)) loop
    select q into question from jsonb_array_elements(model->'pages') p cross join lateral jsonb_array_elements(p->'questions') q where q->>'id'=pair.key;
    if question is null or question->'shuffle_items' is null or jsonb_typeof(pair.value)<>'array' then raise exception 'invalid option order'; end if;
    select array_agg(o->>'value') into expected from jsonb_array_elements(question->(case when question->>'type'='matrix' then 'rows' else 'options' end)) o;
    select array_agg(v) into actual from jsonb_array_elements_text(pair.value) v;
    if cardinality(expected)<>cardinality(actual) or not (expected @> actual and actual @> expected) then raise exception 'option order is not a permutation'; end if;
    for k in 1..cardinality(expected) loop
      if not exists(select 1 from jsonb_array_elements_text(question->'shuffle_items') x where x=expected[k]) and actual[k]<>expected[k] then raise exception 'fixed option moved'; end if;
    end loop;
  end loop;
  if s.browser_state->'page_order' is not null and state->'page_order' is distinct from s.browser_state->'page_order' then raise exception 'page order changed'; end if;
  if state->'page_order' is not null then
    if model->'shuffle_pages' is null or jsonb_typeof(state->'page_order')<>'array' then raise exception 'invalid page order'; end if;
    select array_agg(p->>'id') into expected from jsonb_array_elements(model->'pages') p;
    select array_agg(v) into actual from jsonb_array_elements_text(state->'page_order') v;
    if cardinality(expected)<>cardinality(actual) or not (expected @> actual and actual @> expected) then raise exception 'page order is not a permutation'; end if;
    for k in 1..cardinality(expected) loop
      if not model->'shuffle_pages' ? expected[k] and actual[k]<>expected[k] then raise exception 'fixed page moved'; end if;
    end loop;
  end if;
  perform public.gq_save_session_legacy(s.id,p_access_token,state,consent->>'question');
  update public.gq_sessions set question_orders=coalesce(state->'question_orders','{}'::jsonb),option_orders=coalesce(state->'option_orders','{}'::jsonb),page_order=coalesce(state->'page_order','[]'::jsonb) where id=s.id;
end;$$;
revoke all on function public.greedyq_save_session(uuid,text,jsonb,text) from public;
grant execute on function public.greedyq_save_session(uuid,text,jsonb,text) to anon,authenticated;
