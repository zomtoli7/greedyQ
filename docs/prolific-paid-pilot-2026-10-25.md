# Minimal paid Prolific pilot — preparation

**Historical snapshot.** This report records the scope/evidence at its original source commit. For the final v0.2 documentation reconciliation and the v0.3 CBC boundary, use [the final audit](./v0.2-final-documentation-audit-2026-10-26.md). The later [paid completion record](./prolific-paid-test-completion-2026-10-26.md) supersedes any earlier pending-review/payment status; do not reinterpret earlier test counts as current runs.

[한국어](./prolific-paid-pilot-2026-10-25(kor).md)

The researcher confirmed one participant, two minutes, £0.30 reward and a Prolific-displayed total of £0.42. English wording, manual completion review, existing no-consent/withdrawal paths, and operator deletion of answers plus administrative IDs within 30 days after test verification were confirmed. No automatic scheduled deletion has been claimed; record the deadline when verification is completed and remove retained operator downloads too.

The instrument contains an informed participation page, a simple color-selection check, a number-entry check, optional problem feedback and a voluntary submit/withdraw choice. These inputs are software exercises, not scored attention checks. No participant is instructed to simulate refusal or withdrawal. Contact is through the researcher's Prolific messages. No institution, IRB approval or personal contact address was invented.

The local Test preview passed six browser cases: desktop/mobile × completed, consent refused and withdrawn. Production model `greedyq_paid_pilot_20261025`, version `0.2-paid-pilot-1`, was registered against the researcher's existing draft `6add8ca6d29e6519a7f495d4`. Registration created no production responses. Canonical code was not modified for this instrument.

The stable survey/results aliases were promoted from the earlier synthetic model to this pilot. Existing Test responses are preserved; the current dashboard filters the pilot study. Earlier immutable test deployment URLs remain historical evidence. The participant survey URL is `https://greedyq-prolific-survey.vercel.app/` without `gq_preview`; Prolific must supply its three ordinary ID parameters. Production rejects repeat-preview grants. The results URL is `https://greedyq-prolific-results.vercel.app/` and retains whole-project Authentication. The protected API confirmed zero pilot production responses, rejected production preview-grant issuance, and a parameter-free browser launch made no database writes. Evidence: `paid-pilot-deployment-verification.json` in the private workspace.

A separate mock-only review page is supplied at `https://greedyq-prolific-survey.vercel.app/preview.html`, copied from the canonical build. It renders the Test-mode draft locally in the browser with no external response saving. Do not use that review URL as the Prolific participant survey address.

Before publishing, the researcher must review the participant wording in the separate mock Test preview, replace the draft's repeat-test survey URL with the ordinary survey URL, keep URL-parameter ID recording and the three existing completion paths, select manual review, and verify the final £0.42 cost. Prolific Preview on the production URL would be recorded as a production response; do not use it for another synthetic test. Funding and Publish are separate researcher actions. No funding, recruitment, paid submission or payment has yet occurred.

After one genuine completed submission arrives, compare its Prolific identifiers and completion code with the saved production response, inspect results/CSV and any technical issue, then ask the researcher to approve a valid submission. Do not automatically reject software-check mistakes. Record the verification date and retention deadline. Any larger sample or different budget needs a new researcher decision.

Private operator evidence and sources: `/tmp/greedyq-prolific-live.PYHvob/paid-pilot/`, `paid-pilot-production/`, and `paid-pilot-preparation.json`. These folders are outside the public repository and must not be uploaded wholesale.

## Launch status

The researcher subsequently reported publishing the one-person pilot. This is researcher-reported platform status, not an independent API verification. Initial read-only checks at 06:02 and 06:03 UTC on 2026-10-25 found no pilot sessions yet. No submission approval or participant payment was performed by the agent. Monitor the saved production record and compare it with Prolific's actual submission before advising approval. Private evidence: `paid-pilot-live-status.json`.

The researcher then supplied Prolific's notice that the study was temporarily paused for routine review. It explicitly says this does not necessarily indicate a problem and no action is needed at this time. Preserve the approved settings, budget, ordinary participant URL and completion paths. The pilot is **waiting for platform review**; no genuine paid submission, payment or review completion is verified. Do not automatically create a replacement study, resume/publish, top up or change the collector configuration. Source consolidation and version stamping do not redeploy this frozen pilot. Once review finishes, verify the provider's current decision before continuing.

## Follow-up on 2026-10-26

Matched one Awaiting review submission to the stored production response and published CSV output. Participant ID and required answers agree. Submission approval and payment were not performed or verified. The researcher-authorized database upgrade 007–008 preserved all existing responses. See [terminal timestamp fix and paid response check](./terminal-timestamp-fix-2026-10-26.md). This follow-up updates the historical waiting state above.

## Closure confirmed on 2026-10-26

The researcher subsequently confirmed approval and reward payment for the matched participant. The basic paid connection test is complete. This confirmation updates the historical waiting statements above; no independent transaction receipt was inspected. See the [completed pilot record and remaining boundaries](./prolific-paid-test-completion-2026-10-26.md).
