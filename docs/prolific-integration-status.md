# Prolific integration: implementation and evidence

[한국어](./prolific-integration-status(kor).md)

Checked 2026-10-25. The current source release is recorded in [`release.json`](../release.json). Account-specific state must be checked separately; the first development pilot's pause is not a default status for other researchers.

| Capability | Canonical implementation | Verification and limit |
| --- | --- | --- |
| Three standard launch IDs and bound study | `greedyq/prolific.py`, `web/greedyq-core.js`, respondent template | Python/JS parity; malformed/duplicate/missing/wrong-study IDs rejected; URL IDs are not signed identity proof |
| Atomic session/identity registration | migrations 005–006; `greedyq_start_prolific` | Local PostgreSQL concurrency and actual connected tests; duplicate starts create no orphan session |
| Private response access and resume | capability-protected RPC; canonical browser bridge | Wrong capability rejected; normal reload resumes without exposing another participant's response |
| Source and collection mode | compiled model and server registration | Direct/Prolific and Test/Real independent; client URL cannot switch Production to Test |
| Ending codes and returns | compiled outcomes and save acknowledgements | Actual draft Preview confirmed completion, no consent and withdrawal; synthetic return requests intercepted in automatic tests |
| Repeat draft Preview | migration 006, protected results POST, canonical new-test control | Actual researcher Preview and six-width/language website checks; expired/wrong-study/production grants fail; ordinary duplicates remain blocked |
| Withdrawal answer erasure | migration 006; Python reference; browser/mock state | Atomic deletion, concurrent-write safety, clean reload, results/CSV absence and another response preserved; disclosed minimal administrative IDs remain |
| Protected results and CSV | fixed results template/API | Vercel Authentication enabled; all three IDs joined to correct rows; no server secret in respondent files |
| Screening and technical endings | reviewed outcome routes and `screening_mode` | Local/synthetic routing tested; each researcher must supply its actual codes and compensation policy; configured paid screening is not verified |
| Provider review pause | guide/checkpoints and `tools/prolific_status.cjs` | Evidence summary cannot turn stored answers into paid-verification claims; no automatic resumption, duplicate study, payment or support message |
| Paid transition | separately registered model; ordinary launch; reviewed budget and retention | One-person pilot published by researcher, then paused for routine Prolific review; genuine submission matching, approval and payment remain pending |
| Signed links and repeated production submissions | explicit refusal/unsupported diagnostics | Not implemented; do not enable or advertise them as verified |
| Native surveydown export | compatibility report | Display/logic exports do not imply equivalent atomic erasure or panel identity handling; material gaps are reported |

## Operational sequence

1. Finish the questionnaire, governance and account-free desktop/mobile review.
2. Connect Vercel/Supabase, apply 001–006 and register the exact model; verify public survey and protected results separately.
3. Create an unpublished Prolific draft, confirm study binding, all endings, eligibility, costs and processing actions.
4. Use a private expiring grant for repeated connected Test previews. Check storage, return, erasure, filtered results and CSV.
5. Confirm a real participant-facing paid task, count/duration/reward/total, retention operator/deadline and the publication decision. Use an ordinary Production URL; keep synthetic review separate.
6. If Prolific pauses for routine review, preserve settings and record the waiting status. Follow its notice; no review ETA is promised.
7. After a genuine submission, compare actual platform identifiers/outcome with the saved record before asking the researcher to approve valid work. Record payment separately.
8. After verification, record the approved retention deadline. Remove administrative IDs and operator copies by that deadline; withdrawal erasure is not that later cleanup job.

## Evidence

- Automated regression: 172 Python tests and 36 JavaScript/browser tests passed before release stamping; repeat the release checks after stamping.
- [Connected and researcher-assisted Preview evidence](./prolific-cloud-test-2026-10-25.md).
- [Paid pilot and routine-review state](./prolific-paid-pilot-2026-10-25.md).
- [Researcher procedure](../PROLIFIC-SETUP.md), [results](../RESULTS-DASHBOARD.md), [website source and edit boundary](../website/README.md).

Private credentials, raw response snapshots and participant identifiers remain outside public source. Existing deployed studies retain their recorded runtime/provenance until a separately reviewed upgrade; release stamping does not redeploy or alter the paused pilot.
