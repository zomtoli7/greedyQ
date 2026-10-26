# Terminal timestamp fix and paid response check

[한국어](./terminal-timestamp-fix-2026-10-26(kor).md)

> Later update on 2026-10-26: the researcher confirmed approval and reward payment. The statements below describe the earlier timestamp/response inspection; see the [paid-test completion record](./prolific-paid-test-completion-2026-10-26.md) for current status and evidence sources.

## Cause and correction

The browser save path updated session status and `updated_at` but did not set `terminal_at` on completion. CSV exported that null as an empty `completed_at`. This was a server persistence omission, not a missing answer or a Prolific redirect failure.

Additive migration `008_terminal_timestamp.sql` records server statement time on the first transition from an active state to completed, screened out, consent refused, withdrawn or technical error. The existing end time is immutable across retries and later saves. Client timestamps are not used. The timestamp and answer save share the same transaction; failed writes roll back both. Historical ended sessions with a missing time are not backfilled, even on a repeated save. Migrations 001–007 are unchanged.

Build, deployment checks, migration ledger validation, the canonical registry, all three full AI guides and the reference study bundles include migration 008. Existing installations apply missing canonical migrations in order. CSV continues to use `terminal_at` without substituting the last save or upgrade time.

## Verification

- 194 Python tests and 41 JavaScript/browser tests passed without skips. The PostgreSQL suite includes all terminal states, active sessions, wrong capabilities, failed answer writes, Prolific completion, concurrent retries, preserved first times, forged client times, upgrade preservation and legacy nulls. Browser CSV coverage verifies the exported timestamp field.
- The live deployment had migrations 001–006. Applied the missing snapshot migration 007 and timestamp migration 008, after checking the hashes of all previously applied files. No participant or results bundle redeployment was necessary.
- Connected tests exercised five end states and a Prolific completion in an isolated database savepoint, then rolled back all synthetic fixtures. Retrying the upgrade applied nothing.
- Before/after full-row comparisons matched for all eight data/model tables: 94 sessions, 153 answers, 72 external identity rows, seven lifecycle events and nine study plans; assignment, consent-event and data-request tables remained empty. Existing timestamps and answers were preserved, including the old completed response's null end time. Private evidence: `terminal-timestamp-upgrade.json` in the existing operator workspace.

## Paid response and CSV comparison

The researcher-supplied Prolific screenshot shows one submission awaiting review. Its participant ID matches the stored completed production response, as does the displayed start minute. All four required answers are present; optional feedback is empty. There is also one unfinished production record, whose origin is not established. Earlier test responses are separated by study and `is_test`.

Fetched the protected deployed results HTML and replayed it against the read-only database snapshot in an isolated local browser with external requests blocked. Its downloaded CSV has two production rows, one completed row, the matched participant/study IDs, correct answers, `source=prolific`, `is_test=false`, and the intentionally unchanged legacy empty `completed_at`. This verifies the published CSV implementation, not automation of the researcher's signed-in browser. Raw snapshots, CSV and identifiers remain private.

Prolific reports 2 minutes 3 seconds; the database creation-to-last-save interval is about 1 minute 50 seconds. Those intervals use different boundaries and do not establish a lost answer. The screenshot displays a completion label, not the literal return code. No payment approval, payment confirmation, survey restart or participant-data backfill was performed.

The approved retention rule is deletion within 30 days after verification. With this response verification dated 2026-10-26, the operator deadline is 2026-11-25, including private CSV/snapshot copies and administrative identifiers. No automatic deletion job has been scheduled.
