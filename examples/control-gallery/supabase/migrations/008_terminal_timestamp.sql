-- Record the server time of the first new terminal transition.
-- This additive migration does not backfill or rewrite historical responses.
create function public.gq_record_terminal_timestamp() returns trigger
language plpgsql set search_path=public,pg_temp as $$
begin
  if old.terminal_at is not null then
    -- Retries, subsequent saves and attempted reopening cannot change it.
    new.terminal_at := old.terminal_at;
  elsif old.lifecycle_state not in ('completed','screened_out','consent_refused','withdrawn','technical_error')
    and new.lifecycle_state in ('completed','screened_out','consent_refused','withdrawn','technical_error') then
    new.terminal_at := statement_timestamp();
  else
    -- In particular, do not invent a completion time for legacy ended sessions.
    new.terminal_at := old.terminal_at;
  end if;
  return new;
end;$$;
revoke all on function public.gq_record_terminal_timestamp() from public,anon,authenticated;
create trigger gq_terminal_timestamp before update on public.gq_sessions
for each row execute function public.gq_record_terminal_timestamp();
