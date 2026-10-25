-- Accepted browser answers are a complete snapshot, not a partial patch.
-- Preserve migrations 001–006; change only future authenticated session saves.
create or replace function public.greedyq_save_session(
  p_session_id uuid,p_access_token text,p_state jsonb,p_consent_question text
) returns void language plpgsql security definer set search_path=public,pg_temp as $$
begin
  if p_state->>'lifecycle'='withdrawn' then
    perform public.greedyq_withdraw_session(p_session_id,p_access_token);
  else
    -- This validates capability, consent, identity, ordering and assignment and
    -- locks the session until this entire transaction (including pruning) ends.
    perform public.gq_save_session_validated(p_session_id,p_access_token,p_state,p_consent_question);
    if jsonb_typeof(p_state->'answers')='object' then
      delete from public.gq_answers
        where session_id=p_session_id and not (p_state->'answers' ? question_id);
    end if;
  end if;
end;$$;
revoke all on function public.greedyq_save_session(uuid,text,jsonb,text) from public;
grant execute on function public.greedyq_save_session(uuid,text,jsonb,text) to anon,authenticated;
