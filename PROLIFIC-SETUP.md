# Connect a study to Prolific

[한국어](./PROLIFIC-SETUP(kor).md)

greedyQ collects the survey responses; Prolific recruits participants and handles submissions and payment. Start by creating a **researcher** account, then prepare a draft study. This guide covers standard URL parameters. It does not require a Prolific API token. The agent can prepare everything locally while you create the account.

## What to tell your AI

> Connect my reviewed greedyQ survey to Prolific. Prepare a draft and test it before recruiting anyone. Explain the account steps one at a time. Keep test responses separate from real responses. Do not publish the study or approve payments yet.

## Account and draft setup

1. Sign in to your Prolific researcher account and choose the intended workspace.
2. Create a draft. Confirm the title, description, participant eligibility, devices, estimated duration, sample size and reward with your AI. These are research/budget decisions, not inferred defaults.
3. In **Data collection**, enter the deployed survey URL and choose **URL parameters** for recording participant IDs. Keep the default names `PROLIFIC_PID`, `STUDY_ID`, `SESSION_ID`. Prolific adds their values when participants open the survey. Do not append the same parameters twice.
4. Configure separate **Completion paths** for the outcomes your study uses: completed, screened out, no consent, withdrawal or technical difficulty. Copy the exact URLs/codes to your AI. Never reuse the successful-completion code for a different outcome. Confirm each path's processing action; completion codes can affect payment or return requests.
5. If screening is needed, distinguish validating Prolific's existing prescreeners from custom screening. Custom screening can require a separate screen-out reward. Do not treat refusal of consent as a rejection or invent a screening/payment policy.
6. Give the AI the Prolific study ID and confirm the path mapping. IDs and completion codes are configuration; passwords, login codes and API tokens must not be pasted into chat.

The agent records the expected study ID, builds the survey, applies migrations **001–008** in order and registers the exact reviewed model. Existing installations add missing **006/007** files without rewriting earlier migrations or bulk deleting historical responses. Migration 007 prunes answers removed from future accepted snapshots; the current paid pilot is not upgraded by this local audit. Do not apply migrations to an active shared database without the existing maintenance/review process.

## Test before recruiting

Use Prolific's **Preview** on the draft. It checks URL parameter substitution and the return destination. Confirm:

- A full launch opens; missing, blank, repeated, malformed or wrong-study parameters are refused. Production requires all three 24-character IDs. Standard URL validation is not proof of participant identity or membership in Prolific.
- The protected results link shows the response under **Test responses → Prolific**. A parameter-free test is **Test → Direct** and cannot reveal a Prolific completion code or navigate through a Prolific return path. The production setting is controlled by the reviewed model, never by a URL switch.
- Refresh/reopen in the same browser resumes with the same response and assignment. Another session for the same participant/study is blocked; it does not silently take over the first session. Repeated submissions are not supported by this default. A new browser without the original access capability cannot retrieve private responses merely by knowing IDs.
- Each ending saves before revealing its completion code and enabling return. A failed save leaves both unavailable; refresh/retry after restoring the connection. Completion codes are also shown for manual entry if needed.
- Download CSV includes `PROLIFIC_PID`, `STUDY_ID`, `SESSION_ID` alongside answers, status and the test marker. Direct rows have blank Prolific fields. These identifiers are private participant records; the dashboard remains protected.

Do not claim payment/submission integration was tested by a synthetic browser run or draft Preview. Prolific's separate **Test study as a participant** feature is currently documented as limited beta; it charges the workspace wallet and describes later refunds. Use it only if available and explicitly approved. Actual recruitment/publication is a separate owner action.

## Settings used by the agent

### Moving from tests to a paid pilot

Agree the participant count, honest estimated duration, reward, displayed total and manual/automatic completion review before fielding. One participant is a useful connection pilot; it is not a validation sample for research conclusions. Prepare an actual participant-facing task, consent/data notice and contact route rather than publishing a synthetic path selector. Do not ask a paid participant to deliberately refuse or withdraw. Genuine mistakes in a software check are not automatic rejection grounds.

Confirm retention of both answers and administrative IDs, who will delete them, and how operator downloads will be handled. Withdrawal erasure does not implement the study's later full-retention deadline. Record that deadline when the pilot is verified; do not claim a scheduled deletion exists unless it was actually configured.

Keep the account-free `preview.html` for wording review. The paid pilot uses a separately registered Production model and the ordinary survey URL without `gq_preview`. **Prolific Preview does not override that model: opening a Production URL with valid IDs creates a production response.** Keep URL-parameter recording enabled; never attach a mock `preview.html` as the participant task. Recheck protected results, zero accidental production responses, distinct endings and current study binding before publishing.

After a genuine submission completes, compare all three Prolific identifiers, completion outcome and saved answers against the actual platform submission. A saved database response alone does not verify a Prolific submission or payment. Approve valid work only after this comparison. Publication, recruitment, approval and payment require their own evidence; a deployed URL is not any of those operations.

### If Prolific pauses the study for review

Record the provider status separately from the survey's Test/Production mode and its response lifecycle. A routine-review notice is not proof of a technical fault or a rejection. Follow Prolific's stated instructions. If the notice says no action is needed, preserve the draft/published configuration, URLs, completion paths and approved budget while awaiting review. Do not create a duplicate study, change identifiers, switch collection mode, add funds or repeatedly resume/publish as an automatic workaround. No exact review-completion time is promised.

Check the study status and response count read-only; zero responses while the provider is paused is not evidence of a broken save path. Do not mark the paid pilot verified until submission matching and payment are actually confirmed after the review. Ask for action only when Prolific requests specific information or the researcher reports its decision. A new support message is not sent without authorization.

The agent can run `node tools/prolific_status.cjs MODEL.json PRIVATE_RESULTS_SNAPSHOT.json paused_for_review` to produce a sanitized evidence summary from a protected results snapshot. This offline tool does not contact Prolific, approve work, pay participants or print participant IDs/answers. Its default cannot claim paid verification. Never upload the raw snapshot to the public repository.

```yaml
respondents:
  source: prolific
  mode: test
  duplicate_policy: resume
  prolific:
    study_id: aaaaaaaaaaaaaaaaaaaaaaaa # replace with your real study ID
    completion_paths_reviewed: false # set true only after actual review
    screening_mode: none # none, prescreener_validation, custom
```

Each `outcomes` entry carries the exact Prolific `redirect`. Production refuses missing study binding, unreviewed paths, placeholder codes, shared codes across outcomes, or unreviewed screening. Store administrative panel IDs before consent only as disclosed in the data/consent plan. Research answers remain consent-gated. A saved withdrawal now deletes answers, assignments, consent events and stored browser answers from the active database. Minimal panel identifiers, the session capability and withdrawal status remain for returns and duplicate prevention. Disclose this retention. Anonymization or deletion of those identifiers is a separate reviewed administrative action; duplicate protection cannot be promised afterwards.

## Repeat a Prolific Preview safely

Ordinary links preserve one response per panel participant. Clearing cookies or reopening Prolific Preview does not remove that database restriction. Use a separate **Test-mode** study deployment for repeated testing; never convert an active production study to Test mode just to bypass it.

1. Open your protected **results link** and scroll to **Repeat Prolific preview**. This section appears only for a Prolific study registered in Test mode.
2. Enter the deployed survey URL without query parameters, then choose **Create repeat-test link**. Your AI can perform this through the authenticated results connection instead.
3. Copy the generated URL into the Prolific draft's survey URL field. Keep participant-ID recording through URL parameters enabled. If Prolific asks to append ID parameters, let it append each of the three defaults exactly once. Keep the study as a draft.
4. Start Prolific Preview. A yellow test notice and **Start a new test** appear above the survey. Complete one path and check Prolific's expected completion-code message.
5. Reopen Preview and choose **Start a new test** before testing another path. Earlier test attempts are preserved; the actual three Prolific identifiers are unchanged. Refresh without this button resumes the same attempt.
6. The private link expires after 24 hours. Generate a new one if expired. Do not distribute it to participants. Before real collection, remove the test link and use the reviewed production deployment without `gq_preview`.

The protected server issues a random grant bound to a registered test study; only its hash is stored. A fresh attempt gets an isolated test namespace, not a fabricated Prolific ID. The database rejects missing, expired, wrong-study and production grants. A URL parameter alone cannot turn production into Test mode. The control does not reset or erase earlier attempts. All attempts remain Test responses; duplicate protection for ordinary links is unchanged.

## Withdrawal: deletion and verification

Withdrawal deletes this session's answers, assignments, consent events, questionnaire order and stored browser content atomically. It retains only a minimal withdrawal record and the administrative identifiers needed for return/duplicate prevention. Consumed randomization slots are not reused. The return code/button appears only after the server acknowledges the clean state. Refresh must still show the withdrawal ending with empty answers, and later writes must fail.

This applies to **new withdrawals after migration 006**. Existing historical withdrawals are not silently rewritten. Already downloaded CSV/ZIP files, provider backups, chat attachments and Prolific's own records cannot be erased by this operation; handle them under the researcher's disclosed retention plan. A separate deletion request for administrative identifiers needs researcher review. Native surveydown export reports automatic greedyQ erasure as unsupported; equivalent native storage handling must be verified separately.

Ask your AI: “Test withdrawal with a fictional answer. Confirm that it disappears from the database, results summary, CSV and resumed session; confirm another response is unchanged.” Do not test deletion using a real participant's response.

## Screening and technical endings

greedyQ supports eligibility branching and a distinct screen-out return, but the researcher must choose the policy for each study:

- **Prescreener validation:** use Prolific's exact existing prescreener wording near the start. Configure the appropriate custom path and **Request a return**; do not treat a mismatch alone as a rejection.
- **Custom screening:** choose Prolific's **Screened out** path and confirm its screen-out reward in Prolific. The agent records `screening_mode: custom`; it never invents a reward or enables payment.
- **No screening:** omit unused screen-out routes from a production study rather than configuring a fictional code. Example fixtures can keep unconfigured endings in Test mode.

Technical difficulty needs its own reviewed return/message policy; never send it through successful completion by default. Reaching a return URL is not proof that a submission was returned or paid. Review unresolved submissions in Prolific itself. See [Prolific's screening and consent guidance](https://researcher-help.prolific.com/en/articles/445165-can-i-screen-participants-within-my-study).

The agent may run `python3 tools/prepare_prolific.py STUDY --url https://your-survey.example/ --output NEW_PRIVATE_PATH.json` to produce configuration fields without external writes. `base_survey_url` is for the UI that appends parameters; `api_external_study_url` contains the official placeholders for API-style setup. This command does not create or publish a study.

Signed `prolific_token` launch links require server verification and are explicitly refused by this standard integration. Do not enable that optional Prolific feature for this path or claim the ordinary IDs are verified signatures. Secure-link verification, API recruitment/payment automation and repeated-submission studies are separate capabilities.

## Evidence and sources

Local parsing/compiler parity, real temporary PostgreSQL duplicate/concurrency checks, browser save/return and CSV tests are automated. On 2026-10-25, the owner verified normal completion, no consent and withdrawal through actual Prolific draft Preview; their database states were independently confirmed. Earlier withdrawal evidence predates migration 006 and demonstrated status/return only, not deletion. See the [cloud verification record](./docs/prolific-cloud-test-2026-10-25.md). On 2026-10-26, one real paid submission was matched to its stored response and CSV, and the researcher explicitly confirmed approval and reward payment. The basic paid route is complete. Payment confirmation comes from the researcher, not an independently fetched receipt or payment API. A new real response after timestamp migration 008 and paid in-study screen-out/reward behavior remain unverified. See the [paid-test completion record](./docs/prolific-paid-test-completion-2026-10-26.md) for evidence sources and remaining limits.

Official sources checked 2026-10-25: [IDs and optional secured URLs](https://researcher-help.prolific.com/en/articles/445133-what-are-prolific-ids-and-how-do-i-use-them), [data collection and completion paths](https://researcher-help.prolific.com/en/articles/445127-data-collection), [screening/no consent](https://researcher-help.prolific.com/en/articles/445165-can-i-screen-participants-within-my-study), [draft Preview](https://researcher-help.prolific.com/en/articles/445131-previewing-your-study), [participant test beta](https://researcher-help.prolific.com/en/articles/445134-test-study-as-a-participant), [API URL placeholders](https://docs.prolific.com/api-reference/studies/the-study-object).
