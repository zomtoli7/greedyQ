# CBC collection verification — 26 October 2026

[한국어](./cbc-collection-verification-2026-10-26(kor).md)

This record describes the earlier local-only run. Subsequent [existing-account cloud verification](./cbc-cloud-verification-2026-10-26.md) supersedes only its pending cloud-deployment item; paid/fresh-account/production boundaries remain.

## Delivered boundary

The dedicated `0.3-collection.1` package and `cbc-1` RPCs connect the independently tested Python/browser importer and shared task renderer to the existing seven response tables, protected results and archive. No registered v0.2 CBC control, mixed QMD authoring, native CBC export or statistical estimator is claimed. No existing cloud survey was redeployed, no real respondent records were read/changed and no recruitment/payment was performed.

## Real local database and browser tests

`tests/test_cbc_collection.py` creates a disposable PostgreSQL 17 cluster, applies unchanged 001–008 plus additive 009, and exercises participant calls as the real `anon` role. Cases include consent before allocation/exposure, refusal, version/text-hash consent events, server-weighted single block, persistent shuffled task/alternative orders, assigned-block-only response, wrong capability/choice/revision, completion timestamp, identical concurrent requests, conflicting stale commands, withdrawal of answers/exposures/orders/consent, immutable registered models, real versus authorized Test scope, Prolific identity and repeat-preview isolation, and generic-route bypass rejection.

`tests/cbc_collection_journey.cjs`, invoked by the Python suite, uses the actual fixed participant renderer, protected Results template/API and actual SQL functions through a local PostgREST-shaped adapter. That adapter supplies transport and synthetic researcher authentication; it does not emulate consent, assignment, storage or withdrawal logic. The database executes those operations. All outbound destinations other than the local server and intercepted synthetic Supabase address are blocked.

The journey covers computer and mobile consent/refusal; no task UI before consent; missing choice and focus; Previous/reload; server rejection before save; a save committed with lost acknowledgement and idempotent retry; completion/reload; authorized Test inside a synthetic production namespace; withdrawal/reload; incomplete response; signed-out Results rejection; Real/Test/Source filters; actual downloaded long CSV; closed collection; and complete archive ZIP. Expected synthetic outcome: 5 sessions, 2 completed, 15 real-scope alternative rows including one unanswered task, 12 Test alternative rows, no withdrawn/refused choice rows. Python and browser long-row converters are compared on the same stored records. No paid or human-participant evidence is inferred.

## Exposure and export semantics

Server `served_at` and browser-acknowledged `presented_at` are separate. A server-prepared task whose response packet was lost stays `available` until acknowledgement or answer; unconfirmed availability is not treated as observed presentation. `answered_at` is server-recorded; chosen null remains blank and differs from explicit none. None rows retain blank feature codes. Completion keeps the original server timestamp on retry. Withdrawal removes all CBC choice/exposure records and respondent-specific ordering while retaining only the existing disclosed administrative boundary.

`tests/cbc_results_api.cjs` verifies complete pagination and ID batching with 103 synthetic sessions/2,003 answers and a simulated 200-row server cap, authenticated-origin test-link creation using the service-only RPC, and failure on an unread later page instead of a truncated success. The Results project still relies on Vercel Authentication for every deployment and `/api/results`; the local adapter is not a substitute for checking the live provider protection.

## Gemini access regression

The screenshot establishes declared URL access failure followed by an improvised interview. On our unauthenticated check, the GitHub page and raw URL returned 200. The original client's retrieval logs are unavailable, so the cause is not diagnosed as a GitHub outage, private repository or Gemini-wide inability. Official Google documentation supplies repository import and file-upload alternatives. We put the stop condition into the copied website/start prompts, explain raw text and complete bundle attachment, and synchronize English/Korean/Chinese guides. `tests/test_guide_access.py` checks these distribution contracts and the separate CBC collection schema. This does not constitute a live Gemini Apps retest.

## Remaining external and product checks

- Apply 009 to a specifically approved Supabase CBC test resource through the migration ledger; verify existing record preservation on that actual resource.
- Deploy separated CBC survey/results folders to an approved Vercel target; verify signed-out protection, exact owner access, browser storage/CSV and current provider behavior.
- Verify fresh-account CBC onboarding and, if required, authorized paid CBC recruitment/returns. Existing v0.2 paid Prolific proof is not CBC proof.
- Complete public CBC profile/QMD integration and truthful native export separately; accessibility/touch/browser-family studies and statistical design validation are not inferred from headless Chrome.

See [CBC collection guide](../CBC-COLLECT.md) and [guide access help](../GUIDE-ACCESS.md). Final regenerated-release test totals are recorded with the source-linked update history.


Subsequent researcher reproduction identified the concrete failed paste: loss of line breaks joined `START-HERE.md` to the following Korean sentence. The [full copy audit](./website-prompt-copy-audit-2026-10-26.md) supersedes a generic access-failure diagnosis for that attempt. The canonical URL still returned 200.


Final regenerated-release verification: **236 Python + 56 Node/browser checks passed (292 total), with zero failures/skips**. See the [machine-readable record](./cbc-collection-verification-2026-10-26.json). The browser collection-plan generator also matches the Python reference; researcher devices do not require Python.
