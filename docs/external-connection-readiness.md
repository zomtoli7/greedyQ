# External Connection Readiness

[한국어](./external-connection-readiness(kor).md)

**Release:** `0.2_2026-09-09_236d2a3`
**Status:** locally verified; external accounts not connected

greedyQ prepares and tests the survey application before any Vercel, Supabase, or Prolific account is connected. This boundary keeps ordinary questionnaire review local and makes the final external step a configuration and verification task rather than a new implementation task.

## What is implemented locally

- The same fixed browser JavaScript core parses, validates, compiles, and renders the supported QMD/YAML subset.
- `index.html` automatically selects a desktop or mobile layout from the current device.
- `preview.html` displays independent desktop and mobile participants together, blocks network writes, and uses synthetic browser storage.
- Refresh resume, stable mock assignment, withdrawal/reset, required answers, numeric bounds, routing, and terminal outcomes are covered by automated tests.
- The JavaScript validator and compiler are compared with the Python reference implementation on both golden studies and on deliberately invalid inputs.
- A static Vercel bundle and offline deployment preflight are generated.
- Canonical Supabase migrations define tables, RLS boundaries, capability-token RPC access, locked balanced assignment, consent-gated answer writes, duplicate Prolific identifier rejection, and transactional withdrawal deletion.
- A browser-native `supabase-connection-test.html` verifies the connected project with synthetic `is_test` sessions and withdraws them afterward.
- Prolific launch parameters and HTTPS completion URLs are validated in test code.
- Preregistration Markdown, JSON, and a SHA-256 manifest can be generated as an explicitly unapproved local draft.
- A native surveydown project and an honest compatibility report can be generated without claiming behavioral equivalence.

## What still requires an external account

No live Vercel deployment, Supabase migration, Prolific study configuration, OSF submission, production redirect, or real participant transaction is performed by local tests. Those operations require the researcher's account, authorization, region and retention choices, and explicit approval. After connection, each service must be verified independently; the presence of generated files is not evidence that a service works.

## Final connection sequence

1. Complete researcher review of the local desktop and mobile preview.
2. Resolve every validation error and material research decision.
3. Generate and review the preregistration draft; submit only after separate explicit approval.
4. Sign in to Vercel and approve a Supabase Marketplace resource in the approved region. The connected agent applies all migrations, including `003_results_dashboard.sql`; manual SQL is a recovery path only.
5. Let Vercel synchronize the Supabase environment variables. The survey receives only public configuration; the protected results function receives its server secret without placing it in browser files.
6. Run `python3 -m greedyq preflight STUDY_DIR` or the equivalent agent check.
7. Deploy the public survey and a separately Vercel-authenticated results application.
8. Configure Prolific test parameters and non-production completion routes, then run a full test submission.
9. Verify resume, duplicate handling, consent refusal, both experiment conditions, completion, withdrawal, and analysis export against the connected test services.
10. Require a separate researcher decision before switching to production and recruiting participants.

Completion requires two verified URLs: the survey link and the results link. A direct test response must appear under Test/Direct while the Real responses count remains unchanged.

## Evidence and limits

The repository's unit and contract tests provide local evidence for deterministic behavior and generated connection artifacts. PostgreSQL SQL is source-reviewed by tests but has not been executed against a live Supabase PostgreSQL instance in this account-free phase. Browser files are served and syntax-checked locally; cross-browser and assistive-technology acceptance testing remains a release activity on the target browsers and devices.
