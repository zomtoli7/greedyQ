# Prolific cloud preparation and verification — 2026-10-25

[한국어](./prolific-cloud-test-2026-10-25(kor).md)

## Deployed test environment

- Vercel account: `zomtoli7`, team `greedy-q`.
- Public synthetic survey: https://greedyq-prolific-survey.vercel.app
- Protected results: https://greedyq-prolific-results.vercel.app
- New Supabase Free resource: `greedyq-prolific-test`, Seoul pooler region `ap-northeast-2`, project `motspwocmwyjffmwvnqx`.
- Canonical migrations 001–005 and the exact test model were registered. Reapplying through the checksum ledger passed.
- Initial survey model: `greedyq_prolific_smoke_20261025`, mode `test`; the later draft-bound revision is recorded below. Vercel's “production deployment” label does not change this response classification.

The previous resource `supabase-copper-flower` was resumed by the owner. Its two test sessions, 15 answers and one assignment were checked before and after this work and preserved. Its schema and old deployment were not upgraded. The new resource is connected only to the new results project, which receives server credentials. Survey files contain public configuration only.

## Actual cloud evidence

Chrome at 390px and 1280px completed all five synthetic ending paths: completed, screened out, consent refused, withdrawn and technical error. Ten parameter-based synthetic panel records plus one parameter-free Direct record were saved under Test. Refresh restored answers, and a second browser using the same synthetic panel identity was blocked without creating an orphan session.

The authenticated results page showed zero real responses, ten synthetic Prolific-source records and one Direct test record. Actual CSV download contained ten panel records with `PROLIFIC_PID`, `STUDY_ID`, `SESSION_ID` joined to their answers. A separate internal return fixture was excluded by the results page's study filter.

The latest deployment recheck showed three Direct test records after additional page opens. These are still test-only starts; the count can increase when the public test survey is opened. The panel CSV remained at ten synthetic records and the real count remained zero.

Ten further canonical-runtime checks against the live database exercised ending codes, reload and return navigation. Their example return requests were intercepted locally: no requests with example codes were transmitted to Prolific. These are synthetic records, not Prolific submissions.

Results HTML/API requests without authentication returned 302 to Vercel login on the stable alias and deployment URL. The authorized dashboard/CSV check used a private automation capability. The deployed survey runtime hash matched the canonical repository core. No credential or raw response file belongs in the public repository or survey deployment.

## Fixes promoted to canonical code

- A withdrawn session rejects further writes. The browser now reuses the acknowledged save for an unchanged withdrawal ending, including after reload, so the completion code can still be displayed. Response edits remain rejected by the server. A browser regression reproduces the old failure and covers the fix.
- Results requests include the current study ID, avoiding mixed records when multiple reviewed test models share a database.

Regression verification: 163 Python tests and 30 JavaScript/browser tests passed; whitespace checks passed. This is a working-tree deployment, not a newly stamped Git release.

## Remaining account step

The owner subsequently created the unpublished draft **greedyQ Connection Test** and supplied its study ID and normal-completion URL. New immutable model `greedyq_prolific_smoke_20261025_r2` was registered and deployed to both stable aliases in Test mode. Previous models and records were retained. The results page now filters this revision.

Only normal completion has an actual supplied code. Other endings remain unconfigured; never reuse the completed code for them. The code is shown after successful saving for panel launches; Direct testing does not display it or enable return. At 390px and 1280px, two synthetic launches verified saving, resume, code display and the exact return URL. Wrong-study launches were rejected. Return requests were intercepted, not transmitted to Prolific. Evidence: `prolific-r2-verification.json` in the private workspace.

The owner completed Prolific's actual draft Preview and reported: “This completion URL is working correctly. The participant will complete with the code C1HEJQ9F.” An independent database check found one additional completed Test/Prolific response, excluding the two known automated synthetic participants, with three saved answers and the bound external study ID. Evidence: `owner-preview-verification.json` in the private workspace. Normal-completion Preview round trip and storage are now verified with researcher assistance.

The owner then supplied the `No consent` code `CCS9RKLM` and `Withdrawn consent` code `CMD6M77M`. A new immutable Test model, `greedyq_prolific_smoke_20261025_r3`, was registered and deployed to the same survey and protected results aliases. Normal completion retains `C1HEJQ9F`. Earlier revisions and responses are preserved; the dashboard displays the current revision.

Six browser checks (390px and 1280px × normal completion, consent refusal and withdrawal) passed saving, terminal state, code display, reload and exact return URL checks. The database independently confirmed the six corresponding Test/Prolific states and external study binding. Direct refusal and withdrawal did not expose panel codes or enable return. Synthetic return requests were intercepted, with zero actual Prolific requests. Evidence: `prolific-r3-verification.json` in the private workspace. The two newly supplied paths still require researcher-assisted Prolific draft Preview; supplying URLs does not verify their submission-processing settings.

The protected dashboard and actual CSV download were rechecked against this revision: six Test/Prolific records, four Direct test starts, zero real responses, six panel CSV rows with all three external identifiers, and the correct study filter. Evidence: `results-r3-verification.json` in the private workspace.

The owner confirmed the actual draft Preview return for refusal (`CCS9RKLM`). A read-only database check excluding the six automated participants found one additional Test/Prolific `consent_refused` session. Reopening Preview then encountered the existing participant uniqueness guard. A fresh, immutable Test-only revision `greedyq_prolific_smoke_20261025_r4` was deployed to the same aliases for the next withdrawal check, preserving all prior sessions and the duplicate guard. This is an operator test-workspace workaround, not a general repeatable-Preview feature. Do not reset production records or fabricate real participant IDs to repeat a test. Private evidence: `owner-refusal-verification.json`.

The owner then confirmed the actual withdrawal Preview return with code `CMD6M77M`. An independent read-only check excluded automated R4 participants and found one additional Test/Prolific session with lifecycle `withdrawn`. Evidence: `owner-withdrawal-verification.json` in the private workspace. Its three test answers remain stored; this check confirms the terminal state and return, not response erasure. Normal completion, refusal and withdrawal now each have researcher-assisted Prolific draft Preview confirmation and database-state evidence. Actual platform return processing was not exercised through a paid participant submission.

Screen-out and technical-error returns remain unconfigured. Actual participant recruitment, paid platform submissions/approvals, payments and signed URL validation remain unverified. Follow [Prolific setup](../PROLIFIC-SETUP.md).

## Withdrawal erasure and repeat-preview upgrade

Migration 006 was applied to the dedicated test database and retried through the checksum ledger. Before/after counts were identical: 53 sessions, 85 answers and 37 external identifier records. Historical models, including earlier withdrawals, were preserved. Evidence: `withdrawal-preview-upgrade.json` in the private workspace.

The canonical runtime now acknowledges server-side answer erasure for new withdrawals before enabling return. The PostgreSQL boundary removes answers, assignment, consent events, prior lifecycle payloads, data requests and stored browser content, while retaining the minimal withdrawal record and administrative panel identifiers. Used allocation slots remain consumed. A browser regression found queued pre-erasure snapshots after acknowledgement; these are now discarded instead of retried. Native surveydown export explicitly reports the missing storage-deletion implementation.

The protected dashboard now issues 24-hour test grants. Two real cloud/browser runs each exercised ten cases: 390px and 1280px × completed, consent refused, withdrawn, screened out and technical error. Each width reused the same actual-format synthetic panel identifiers across five distinct attempt namespaces. Ordinary refresh resumed the same attempt. New-test controls preserved previous attempts. Withdrawal had zero answer rows, clean resumed browser state, no corresponding results answers and no unique fictional text in the downloaded CSV; a prior completed response remained intact. Code returns were locally intercepted. Screen-out and technical-error had no invented return code. Anonymous issuance was blocked by Vercel Authentication. The first run's final assertion expected 302 but Vercel correctly returned 401 for unauthenticated POST; the assertion was corrected and the complete run repeated successfully. Evidence: `repeat-withdrawal-verification.json`. No actual Prolific requests, recruitment or payment occurred.

Final regression: 167 Python tests and 32 JavaScript/browser tests passed with no skips. A further targeted 13-test PostgreSQL run covered wrong-study preview grants and concurrent withdrawal/save. The standalone responsive-controls/browser harness ran through the Python suite. Whitespace checks passed. The deployed core SHA-256 matched the canonical source (`f0c99b80fa797df42d60658e2298f6c43121a290efd091e1348ab8e0238fe3c0`), and results-project Authentication remained enabled for all deployments. Generated examples, consent hashes, native export mismatch reports, guide registry, locks, embedded fallback guides and artifact manifests were refreshed. No new release commit or release identifier was fabricated.

The researcher subsequently confirmed actual Prolific draft Preview through the new repeat-test link: both no-consent and withdrawal returns worked, and **Start a new test** did not encounter duplicate blocking. A read-only query after the automated-run cutoff found one Test/Prolific refusal with one consent answer, one fresh start with zero answers, and one withdrawal with zero answers. Evidence: `owner-repeat-preview-verification.json` in the private workspace. Researcher-assisted repeat-preview and withdrawal-erasure verification is complete for this test deployment.

This verifies the deployed survey, protected dashboard, API and database workflow with synthetic and researcher-assisted draft-preview responses. It does not verify paid platform submissions, actual return processing or payment. The earlier three actual draft Preview confirmations remain valid for their tested revisions. Signed Prolific links are still rejected explicitly; enabling that optional feature or approving paid recruitment is outside this verified path.

Private operator workspace and evidence: `/tmp/greedyq-prolific-live.PYHvob`. It includes private environment files; do not publish or upload it as a deployment bundle. If it is unavailable later, re-pull credentials through the authorized Vercel connection rather than requesting secrets in chat.
