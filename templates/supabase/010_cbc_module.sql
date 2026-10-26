-- CBC as one module in a normal linear survey. Preserve every applied migration.
-- The dedicated before/after arrays are generated from ordinary QMD pages;
-- researchers insert sd_cbc, rather than authoring a second survey.
alter function public.greedyq_cbc_resume(uuid,text) rename to gq_cbc_resume_v1;
revoke all on function public.gq_cbc_resume_v1(uuid,text) from public,anon,authenticated;
create function public.greedyq_cbc_resume(p_session_id uuid,p_access_token text) returns jsonb
language plpgsql security definer set search_path=public,pg_temp as $$
declare r jsonb;m jsonb;st jsonb;pages jsonb;phase text;
begin
 r:=public.gq_cbc_resume_v1(p_session_id,p_access_token);m:=public.gq_cbc_context(p_session_id,p_access_token);if m ? 'flow' then r:=r||jsonb_build_object('module_contract','cbc-module-1');end if;st:=r->'state';phase:=st->>'phase';r:=r||jsonb_build_object('has_before',jsonb_array_length(coalesce(m->'flow'->'before','[]'))>0);
 if phase in ('before','after') then
  pages:=m->'flow'->phase;
  r:=r||jsonb_build_object('model',null,'form_page',pages->((st->>'form_index')::int),'form_answers',coalesce(st->'survey_answers','{}'::jsonb));
 end if;
 return r;
end;$$;
revoke all on function public.greedyq_cbc_resume(uuid,text) from public;
grant execute on function public.greedyq_cbc_resume(uuid,text) to anon,authenticated;

alter function public.greedyq_cbc_consent(uuid,text,text) rename to gq_cbc_consent_v1;
revoke all on function public.gq_cbc_consent_v1(uuid,text,text) from public,anon,authenticated;
create function public.greedyq_cbc_consent(p_session_id uuid,p_access_token text,p_decision text) returns jsonb
language plpgsql security definer set search_path=public,pg_temp as $$
declare m jsonb;first_accept boolean;st jsonb;
begin
 m:=public.gq_cbc_context(p_session_id,p_access_token);
 select lifecycle_state='created' into first_accept from public.gq_sessions where id=p_session_id;
 perform public.gq_cbc_consent_v1(p_session_id,p_access_token,p_decision);
 if first_accept and p_decision='accepted' and jsonb_array_length(coalesce(m->'flow'->'before','[]'))>0 then
  select browser_state into st from public.gq_sessions where id=p_session_id;
  -- No unvisited stimulus exposure is committed before the ordinary pages.
  delete from public.gq_answers where session_id=p_session_id and question_id like 'cbc:%';
  st:=st||jsonb_build_object('phase','before','form_index',0,'survey_answers','{}'::jsonb,'visited','[]'::jsonb);
  update public.gq_sessions set browser_state=st,current_page=m->'flow'->'before'->0->>'id' where id=p_session_id;
 end if;
 return public.greedyq_cbc_resume(p_session_id,p_access_token);
end;$$;
revoke all on function public.greedyq_cbc_consent(uuid,text,text) from public;
grant execute on function public.greedyq_cbc_consent(uuid,text,text) to anon,authenticated;

create function public.gq_cbc_question_visible(rule jsonb,answers jsonb) returns boolean
language plpgsql immutable set search_path=public,pg_temp as $$
declare item jsonb;v jsonb;
begin
 if rule is null or rule='null'::jsonb then return true;end if;
 if rule ? 'all' then for item in select value from jsonb_array_elements(rule->'all') loop if not public.gq_cbc_question_visible(item,answers) then return false;end if;end loop;return true;end if;
 if rule ? 'any' then for item in select value from jsonb_array_elements(rule->'any') loop if public.gq_cbc_question_visible(item,answers) then return true;end if;end loop;return false;end if;
 if rule ? 'not' then return not public.gq_cbc_question_visible(rule->'not',answers);end if;
 v:=answers->(rule->>'field');
 if rule ? 'answered' then return (v is not null and v not in ('null'::jsonb,'""'::jsonb,'[]'::jsonb,'{}'::jsonb))=(rule->>'answered')::boolean;end if;
 if rule ? 'length' then
  if jsonb_typeof(v) not in ('string','array') then return false;end if;
  return public.gq_cbc_question_visible((rule->'length')||jsonb_build_object('field','length_value'),jsonb_build_object('length_value',case when jsonb_typeof(v)='array' then jsonb_array_length(v) else length(v#>>'{}') end));
 end if;
 if rule ? 'equals' then return case when jsonb_typeof(v) in ('array','object') then false else coalesce(v,'null'::jsonb)=rule->'equals' end;end if;
 if rule ? 'not_equals' then return v is not null and v<>'null'::jsonb and rule->'not_equals'<>'null'::jsonb and v is distinct from rule->'not_equals';end if;
 if rule ? 'in' then return coalesce(rule->'in' @> jsonb_build_array(v),false);end if;
 if rule ? 'contains' then return coalesce(v @> jsonb_build_array(rule->'contains'),false);end if;
 if jsonb_typeof(v)='number' then
  if rule ? 'gte' then return v::numeric >= (rule->>'gte')::numeric;end if;
  if rule ? 'lte' then return v::numeric <= (rule->>'lte')::numeric;end if;
  if rule ? 'gt' then return v::numeric > (rule->>'gt')::numeric;end if;
  if rule ? 'lt' then return v::numeric < (rule->>'lt')::numeric;end if;
 end if;
 return false;
end;$$;
revoke all on function public.gq_cbc_question_visible(jsonb,jsonb) from public,anon,authenticated;

-- Validate ordinary controls without executing survey-authored code.
create function public.gq_cbc_check_answer(q jsonb,v jsonb,enforce_required boolean) returns void
language plpgsql set search_path=public,pg_temp as $$
declare t text:=case when q->>'type'='custom' then q->>'base_type' else q->>'type' end;missing boolean;item jsonb;r jsonb;pair record;n numeric;total numeric:=0;
begin
 missing:=v is null or v='null'::jsonb or v='""'::jsonb or v='[]'::jsonb or v='{}'::jsonb;
 if t in ('audio','video') then return;end if;
 if missing then if enforce_required and coalesce((q->>'required')::boolean,false) then raise exception 'required question: %',q->>'id';end if;return;end if;
 if pg_column_size(v)>65536 then raise exception 'answer too large';end if;
 if t in ('text','textarea','date') and jsonb_typeof(v)<>'string' then raise exception 'text answer required';end if;
 if t='slider_numeric' and jsonb_typeof(v)='array' then
  if jsonb_array_length(v)<>2 then raise exception 'two slider endpoints required';end if;
  for item in select value from jsonb_array_elements(v) loop perform public.gq_cbc_check_answer(q||jsonb_build_object('type','numeric'),item,enforce_required);end loop;
  if (v->>0)::numeric>(v->>1)::numeric then raise exception 'ordered slider range required';end if;return;
 end if;
 if t in ('numeric','nps','slider_numeric','timing') then
  if jsonb_typeof(v)<>'number' then raise exception 'numeric answer required';end if;n:=v::numeric;
  if (q ? 'min' and n<(q->>'min')::numeric) or (q ? 'max' and n>(q->>'max')::numeric) or (t='nps' and (n<0 or n>10 or trunc(n)<>n)) or (t='timing' and n<0) then raise exception 'numeric bound violation';end if;
 end if;
 if t in ('mc','mc_buttons','mc_image','select','slider') and not exists(select 1 from jsonb_array_elements(q->'options') a where a->'value'=v) then raise exception 'unknown option';end if;
 if t in ('mc_multiple','mc_multiple_buttons','mc_multiple_image') then
  if jsonb_typeof(v)<>'array' or jsonb_array_length(v)<>(select count(distinct value) from jsonb_array_elements(v)) then raise exception 'multiple choice array required';end if;
  for item in select value from jsonb_array_elements(v) loop if not exists(select 1 from jsonb_array_elements(q->'options') a where a->'value'=item) then raise exception 'unknown option';end if;end loop;
 end if;
 if t in ('matrix','matrix_multiple') then
  if jsonb_typeof(v)<>'object' then raise exception 'matrix object required';end if;
  for pair in select * from jsonb_each(v) loop
   if not exists(select 1 from jsonb_array_elements(q->'rows') a where a->>'value'=pair.key) then raise exception 'unknown matrix row';end if;
   perform public.gq_cbc_check_answer(jsonb_build_object('id',q->>'id','type',case when t='matrix' then 'mc' else 'mc_multiple' end,'options',q->'options','required',true),pair.value,true);
  end loop;
  if enforce_required and coalesce((q->>'required')::boolean,false) and exists(select 1 from jsonb_array_elements(q->'rows') a where not v ? (a->>'value')) then raise exception 'matrix row required';end if;
 end if;
 if t in ('constant_sum','rank_order','side_by_side','pick_group_rank') then
  if jsonb_typeof(v)<>'object' then raise exception 'structured answer required';end if;
  if t in ('constant_sum','rank_order') then
   for pair in select * from jsonb_each(v) loop
    if not exists(select 1 from jsonb_array_elements(q->'options') a where a->>'value'=pair.key) or jsonb_typeof(pair.value)<>'number' or pair.value::numeric<0 then raise exception 'invalid item allocation';end if;
    total:=total+pair.value::numeric;
   end loop;
   if t='constant_sum' and enforce_required and total<>coalesce((q->>'total')::numeric,100) then raise exception 'constant sum mismatch';end if;
   if t='rank_order' and enforce_required and coalesce((q->>'required')::boolean,false) and (select count(*) from jsonb_each(v))<>jsonb_array_length(q->'options') then raise exception 'rank every item';end if;
   if t='rank_order' and ((select count(distinct value) from jsonb_each(v))<>(select count(*) from jsonb_each(v)) or exists(select 1 from jsonb_each(v) where value::numeric<1 or trunc(value::numeric)<>value::numeric or value::numeric>jsonb_array_length(q->'options'))) then raise exception 'invalid ranking';end if;
  end if;
 end if;
 if t in ('daterange','drill_down') and jsonb_typeof(v)<>'array' then raise exception 'ordered answer required';end if;

 if t='side_by_side' then
  for pair in select * from jsonb_each(v) loop
   if not exists(select 1 from jsonb_array_elements(q->'columns') a where a->>'value'=pair.key) then raise exception 'unknown rating column';end if;
   perform public.gq_cbc_check_answer(jsonb_build_object('id',q->>'id','type','matrix','options',q->'options','rows',q->'rows','required',q->'required'),pair.value,enforce_required);
  end loop;
  if enforce_required and coalesce((q->>'required')::boolean,false) and (select count(*) from jsonb_each(v))<>jsonb_array_length(q->'columns') then raise exception 'complete all rating columns';end if;
 end if;
 if t='pick_group_rank' then
  for pair in select * from jsonb_each(v) loop
   if not exists(select 1 from jsonb_array_elements(q->'options') a where a->>'value'=pair.key) or not exists(select 1 from jsonb_array_elements(q->'groups') a where a->'value'=pair.value->'group') then raise exception 'unknown group item';end if;
   if pair.value->>'rank' is not null and (jsonb_typeof(pair.value->'rank')<>'number' or (pair.value->>'rank')::numeric<1 or trunc((pair.value->>'rank')::numeric)<>(pair.value->>'rank')::numeric) then raise exception 'invalid group rank';end if;
  end loop;
  if enforce_required and coalesce((q->>'required')::boolean,false) and (select count(*) from jsonb_each(v))<>jsonb_array_length(q->'options') then raise exception 'place every group item';end if;
  if exists(select 1 from jsonb_each(v) where value->>'rank' is not null group by value->'group',value->'rank' having count(*)>1) then raise exception 'duplicate group rank';end if;
 end if;
 if t='drill_down' then
  if not exists(select 1 from jsonb_array_elements(q->'options') a where (string_to_array(a->>'label',coalesce(q->>'path_separator',' > ')))[1:jsonb_array_length(v)]=array(select jsonb_array_elements_text(v))) then raise exception 'invalid drill down path';end if;
  if enforce_required and coalesce((q->>'required')::boolean,false) and not exists(select 1 from jsonb_array_elements(q->'options') a where to_jsonb(string_to_array(a->>'label',coalesce(q->>'path_separator',' > ')))=v) then raise exception 'complete drill down path';end if;
 end if;
 if t='date' then perform (v#>>'{}')::date;end if;
 if t='date' and (v#>>'{}') !~ '^\d{4}-\d{2}-\d{2}$' then raise exception 'ISO date required';end if;
 if t='daterange' then
  perform (v->>0)::date;perform (v->>1)::date;
  if jsonb_array_length(v)<>2 or (v->>0) !~ '^\d{4}-\d{2}-\d{2}$' or (v->>1) !~ '^\d{4}-\d{2}-\d{2}$' or (v->>0)>(v->>1) then raise exception 'ordered ISO date range required';end if;
 end if;

end;$$;
revoke all on function public.gq_cbc_check_answer(jsonb,jsonb,boolean) from public,anon,authenticated;

create function public.greedyq_cbc_form_step(p_session_id uuid,p_access_token text,p_page_id text,p_answers jsonb,p_direction text,p_revision integer,p_request_id uuid) returns jsonb
language plpgsql security definer set search_path=public,pg_temp as $$
declare m jsonb;s public.gq_sessions;st jsonb;phase text;idx integer;pages jsonb;page jsonb;q jsonb;answers jsonb;pair record;tid text;
begin
 m:=public.gq_cbc_context(p_session_id,p_access_token);select * into s from public.gq_sessions where id=p_session_id;st:=s.browser_state;phase:=st->>'phase';
 if st->>'last_request_id'=p_request_id::text then return public.greedyq_cbc_resume(s.id,p_access_token);end if;
 if s.lifecycle_state<>'in_progress' or phase not in ('before','after') or p_revision is distinct from (st->>'revision')::integer or p_request_id is null or p_direction not in ('next','previous') or p_direction is null then raise exception 'invalid form step';end if;
 pages:=m->'flow'->phase;idx:=(st->>'form_index')::integer;page:=pages->idx;
 if p_page_id is distinct from page->>'id' or jsonb_typeof(p_answers)<>'object' or p_answers is null then raise exception 'form page mismatch';end if;
 for pair in select * from jsonb_each(p_answers) loop
  if not exists(select 1 from jsonb_array_elements(page->'questions') element where element.value->>'id'=pair.key) then raise exception 'unknown question';end if;
 end loop;
 answers:=coalesce(st->'survey_answers','{}'::jsonb)||p_answers;
 for q in select value from jsonb_array_elements(page->'questions') loop
  if public.gq_cbc_question_visible(q->'show_if',answers) then
   perform public.gq_cbc_check_answer(q,p_answers->(q->>'id'),p_direction='next');
   if p_answers ? (q->>'id') then
    insert into public.gq_answers(session_id,question_id,value) values(s.id,q->>'id',p_answers->(q->>'id')) on conflict(session_id,question_id) do update set value=excluded.value,answered_at=now();
   else answers:=answers-(q->>'id');delete from public.gq_answers where session_id=s.id and question_id=q->>'id';end if;
  else answers:=answers-(q->>'id');delete from public.gq_answers where session_id=s.id and question_id=q->>'id';end if;
 end loop;
 if p_direction='next' then
  for q in select value from jsonb_array_elements(coalesce(page->'checks','[]'::jsonb)) loop
   if public.gq_cbc_question_visible(q->'when',answers) then raise exception '%',q->>'message';end if;
  end loop;
 end if;
 st:=st||jsonb_build_object('survey_answers',answers,'revision',p_revision+1,'last_request_id',p_request_id);
 if p_direction='previous' then
  if idx>0 then idx:=idx-1;
  elsif phase='after' then phase:='tasks';st:=st||jsonb_build_object('index',jsonb_array_length(st->'task_order')-1);
  else raise exception 'first survey page';end if;
 elsif idx+1<jsonb_array_length(pages) then idx:=idx+1;
 elsif phase='before' then
  phase:='tasks';tid:=st->'task_order'->>0;st:=st||jsonb_build_object('index',0);if not st->'visited' ? tid then st:=jsonb_set(st,'{visited}',st->'visited'||jsonb_build_array(tid));end if;perform public.gq_cbc_present(s.id,m,st);
 else phase:='completed';st:=st||jsonb_build_object('completed',true,'lifecycle','completed');end if;
 st:=st||jsonb_build_object('phase',phase,'form_index',idx);
 update public.gq_sessions set browser_state=st,current_page=case when phase='tasks' then 'cbc:'||(st->'task_order'->>((st->>'index')::int)) when phase='completed' then 'completed' else m->'flow'->phase->idx->>'id' end,lifecycle_state=st->>'lifecycle',updated_at=now() where id=s.id;
 return public.greedyq_cbc_resume(s.id,p_access_token);
end;$$;
revoke all on function public.greedyq_cbc_form_step(uuid,text,text,jsonb,text,integer,uuid) from public;
grant execute on function public.greedyq_cbc_form_step(uuid,text,text,jsonb,text,integer,uuid) to anon,authenticated;

create or replace function public.greedyq_cbc_step(p_session_id uuid,p_access_token text,p_task_id text,p_choice text,p_direction text,p_revision integer,p_request_id uuid) returns jsonb
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
 if p_direction='previous' then if idx=0 then
   if jsonb_array_length(coalesce(m->'flow'->'before','[]'))=0 then raise exception 'first task';end if;
   st:=st||jsonb_build_object('phase','before','form_index',jsonb_array_length(m->'flow'->'before')-1);
  else idx:=idx-1;end if;
 elsif idx+1=jsonb_array_length(st->'task_order') then
  if exists(select 1 from jsonb_array_elements_text(st->'task_order') t where not exists(select 1 from public.gq_answers a where a.session_id=s.id and a.question_id='cbc:'||t and a.value->>'choice' is not null)) then raise exception 'unanswered task';end if;
  if jsonb_array_length(coalesce(m->'flow'->'after','[]'))>0 then st:=st||jsonb_build_object('phase','after','form_index',0);
  else st:=st||'{"completed":true,"phase":"completed","lifecycle":"completed"}'::jsonb;end if;
 else idx:=idx+1;end if;
 st:=st||jsonb_build_object('index',idx,'revision',p_revision+1,'last_request_id',p_request_id);
 if st->>'phase'='tasks' then
  next_tid:=st->'task_order'->>idx;
  if not st->'visited' ? next_tid then st:=jsonb_set(st,'{visited}',st->'visited'||jsonb_build_array(next_tid));end if;
  perform public.gq_cbc_present(s.id,m,st);
 end if;
 update public.gq_sessions set browser_state=st,current_page=case when st->>'phase'='completed' then 'completed' when st->>'phase' in ('before','after') then m->'flow'->(st->>'phase')->((st->>'form_index')::int)->>'id' else 'cbc:'||next_tid end,lifecycle_state=st->>'lifecycle',updated_at=now() where id=s.id;
 return public.greedyq_cbc_resume(s.id,p_access_token);
end;$$;
