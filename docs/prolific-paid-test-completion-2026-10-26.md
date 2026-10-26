# Prolific paid connection test — completed

[한국어](./prolific-paid-test-completion-2026-10-26(kor).md)

> Subsequent authorized cleanup: on 2026-10-26 the researcher chose immediate deletion. Active trial records and known private operator copies were removed and collection closed. The earlier November 25 pending-cleanup statement below records the original plan; see the [closeout record](./v0.2-closeout-2026-10-26.md).

## Result and evidence sources

On 2026-10-26, the researcher confirmed that the participant submission was approved and the reward paid. The basic one-person paid connection test is complete: Prolific launch, saved answers, completed response, results/CSV matching, and researcher-confirmed approval and payment. This is a connection/workflow check, not validation of research design or every Prolific feature.

| Step | Result | Evidence source |
| --- | --- | --- |
| Actual participant response | One completed non-test Prolific response, four required answers present | Agent inspection of the authenticated results API and database |
| Submission matches the response | Participant ID and displayed start minute match | Researcher-provided Prolific Awaiting review screenshot compared by the agent with the stored record |
| Results and CSV | Correct answers, study/participant identifiers, Prolific source and non-test flag | Published dashboard HTML exercised against a private read-only snapshot in an isolated browser; external requests blocked |
| Submission approval | Confirmed | Researcher's explicit confirmation in this conversation on 2026-10-26 |
| Reward payment | Confirmed | Same researcher confirmation; no independent payment API response or transaction receipt was inspected |
| Completion timestamp fix | Applied and tested; historical response unchanged | Local PostgreSQL tests and connected savepoint tests, before/after full-row comparisons, migrations 007–008 |

The approved trial settings were one participant, two minutes, £0.30 reward, and £0.42 displayed total. No separate financial reconciliation or receipt amount was fetched. Do not describe payment as agent-executed, API-verified, or independently audited. Do not approve or pay again.

## Checked separately from the paid completion

Actual draft Preview covered normal completion, refusal, withdrawal and starting a fresh test without weakening production duplicate checks. Withdrawal erasure, concurrent save protection, independent test/real filtering, resume and CSV behavior have local/connected evidence. Those checks do not mean a paid participant was asked to refuse or withdraw.

## Remaining boundaries

- **First paid response after migration 008:** future first end times are recorded and stable in local and connected synthetic tests. The only matched paid response predates this fix and its empty timestamp is intentionally unchanged. A subsequent real response has not yet verified the new timestamp; this can be checked with the first response of the next approved study.
- **Paid in-study screening:** routing exists and has local/synthetic checks, but the actual Screened out path and its reward have not been exercised in a paid study. Verify per study if that policy is used.
- **Additional environments and scale:** this pilot does not verify every new account, study, institution, sample size or custom allocation. Run the relevant checks for the actual design.
- **Receipt inspection:** payment is confirmed by the researcher; an independent receipt/transaction check was not performed.
- **Unsupported features:** signed-link verification, recruitment/payment API automation and repeated production submissions are not established capabilities of the standard URL integration. They are not pending requirements for the completed basic test.
- **Cleanup:** delete retained test answers, administrative IDs and private operator CSV/snapshot copies by 2026-11-25 under the approved 30-day retention rule. This remains an operator task; no automatic deletion job or completed deletion is claimed.
- **Unfinished record:** the pilot has one additional unfinished production record of unestablished origin. It was not treated as another verified paid participant and was not deleted or reclassified.

No further paid test is required merely to re-confirm the already completed basic route. Do not enlarge the sample, change reward settings, recruit, approve or pay without the researcher's separate decision.

## Release validation

After release stamping, all 194 Python tests and 41 JavaScript/browser tests passed without skips. The generated homepage matches its release, byte length and SHA-256 in `website/publication-manifest.json`. English, Korean and Chinese navigation, history and restricted mobile prompt copying passed browser checks. This records local/source validation, not Google Sites publication or another external payment check.

## Related records

- [Timestamp fix and matched CSV evidence](./terminal-timestamp-fix-2026-10-26.md)
- [Dated pilot preparation and review history](./prolific-paid-pilot-2026-10-25.md)
- [Current integration evidence and limits](./prolific-integration-status.md)
- [Researcher setup guide](../PROLIFIC-SETUP.md)

Raw identifiers, participant answers, database credentials and operator downloads remain outside the public repository. Website HTML generation and GitHub publication are separate from Google Sites publication; the website-update Work must verify the published page after applying the generated file.
