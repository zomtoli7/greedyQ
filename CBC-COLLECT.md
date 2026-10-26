# Collect CBC responses and review results

**Development line: v0.3.** CBC is not part of the supported v0.2 release. The existing shared-source release identifier records provenance, not CBC feature availability. Local synthetic verification is distinct from cloud/paid acceptance.

<!-- GREEDYQ_DESKTOP_POLICY -->
**greedyQ requires an installed desktop AI app for creating or modifying studies. AI web apps are officially unsupported.** Download ChatGPT desktop or Claude Desktop from the official provider. Gemini is not officially supported, including its desktop app. Use an agent-enabled mode that can read the complete guide, create real files and run the canonical preview; installing an app or paying for a model alone does not establish these capabilities. Ordinary desktop chat without these tools is not a supported authoring route. Participant surveys, computer/mobile previews and the researcher results page still run in a web browser. [Supported authoring environment](SUPPORTED-ENVIRONMENTS.md).
<!-- /GREEDYQ_DESKTOP_POLICY -->

[한국어](./CBC-COLLECT(kor).md) · [简体中文](./CBC-COLLECT(zh-CN).md)

The dedicated CBC collection path now has server storage, consent, withdrawal, protected results and CSV export. It reuses the existing greedyQ response tables and deployment journey. It has been tested with synthetic respondents in real local PostgreSQL and desktop/mobile browsers. This does not mean a CBC study has been deployed to your accounts or approved for recruitment.

## What the researcher does

1. Prepare and review the design with your AI using [CBC table import and preview](./CBC.md). You may collaborate with the AI, fill a blank Excel/CSV table, or bring an existing design. Confirm attributes, levels, opt-out, blocks and ordering yourself.
2. Provide the research-team name, study title, actual participation information, contact, consent version and data plan. The AI must show the full consent text on the actual participant page. The project support email is not inserted as your study's contact automatically.
3. Tell the AI when the instrument, consent, data plan, deployment and fielding are approved. A template, working preview or a passing parser does not supply these approvals. The AI records them separately; production packaging is blocked until all five are explicitly true and a real researcher contact is supplied.
4. Sign in to Vercel and approve any missing Supabase integration access when requested. An existing authorized connection is preferred; “Onboard your agent” remains optional. The AI prepares two separate sites: the public “Survey link”, where participants answer, and the protected “Results link”, where only the researcher reviews data.
5. Open an authorized Test link from the Results page and try agreeing, declining, selecting “neither”, returning to a previous task, refreshing and withdrawing on computer and phone. Ask the AI to compare stored records and downloaded CSV. Test data must remain marked Test even when the actual study accepts real responses.
6. Start recruitment only after approving it. Existing Direct and Prolific rules still apply; Prolific study setup, completion paths, compensation and paid CBC acceptance remain distinct checks. No payment or recruitment is automated by this feature.

## What the participant sees

The opening shows the approved participant information and consent choice. Before consent, no block assignment, task order or CBC exposure is stored or returned. Refusing ends the session and does not show CBC tasks. Agreeing records the consent version and exact text hash, then the server assigns one block and fixes task/alternative orders. Only that block is returned. Refresh or Previous does not draw a new block or order.

The computer and phone use the same fixed renderer as preview. A missing choice gives a message above the task and moves focus there. Next waits for confirmed server storage. When storage fails, the last confirmed state remains; retry uses the same request ID, preventing duplicate advances if the server saved but the acknowledgement was lost. Reload restores confirmed progress. Do not repeatedly change answers or navigate elsewhere during an unresolved connection failure.

“Withdraw participation” first asks for a confirming click. Only a successful server deletion displays the withdrawal receipt. It erases CBC choices, exposures, orders, assignments and participant consent records; the disclosed minimum session/platform administration record can remain. Already downloaded copies are not remotely erased. After archiving/pausing, contact the research team to handle withdrawal requests under its data plan. Completion records the first server end time and preserves it on retries.

## Results and download choices

The Results page starts on **Real responses**. “Test responses” shows trials; “All” deliberately combines them. Source separately selects Direct, Prolific or both. A caller cannot turn a real response into Test with `?test=true` or a participant-supplied flag. On a production study, the protected Results page issues a private 24-hour test grant; valid grants start Test sessions. “Start another test” uses a new virtual identity so repeated checks do not block each other. Do not distribute test links for recruitment.

- **Response overview CSV**: one row per session, including incomplete, declined and withdrawn session metadata in the selected view. Structured task values are preserved as JSON. This is useful for administration, not the main conjoint analysis table.
- **CBC choice CSV**: one row per alternative in each server-served task, with its display-confirmation state. It includes ordinary alternatives and opt-out, selected value, block, actual positions, design version/hash, server presentation/answer times, source, test flag and session completion time. Use this table for analysis preparation. Unanswered is blank, never “neither”; opt-out feature columns are blank. Unvisited tasks do not create fabricated observations. Rows from withdrawn/refused sessions do not contain choices or exposures.
- **Archive ZIP**: after closure and download confirmation, the existing archive contains raw structured records and separate real/test CBC long CSVs, with checksums. Keep the approved design and media too. CSV downloads are private research data and may include platform identifiers in the response overview.

Descriptive task/none counts are shown. They are not utility estimates, WTP, model fit, statistical efficiency or sample-size advice. Filters apply to both figures and downloads. On a failed/stale refresh, downloads are disabled until the selected view loads; empty CSVs retain their headings.


Server preparation and display are distinct: `served_at` records the server making a task available; `presented_at` is recorded after browser render acknowledgement (or an explicit answer). `presentation_state=available` means display is unconfirmed, `presented` means acknowledged but unanswered, and `answered` means a recorded choice. A lost next-page response is never evidence that the participant saw that next task. Long CSV retains available rows for auditing; exclude them when analysing confirmed exposures. Even a render acknowledgement does not prove human attention.

## Fixed implementation for agents

Use `greedyq/cbc.py`, `web/greedyq-cbc.js`, `web/greedyq-cbc-collection.js`, the fixed browser templates and `tools/cbc_cloud.cjs`; do not author a replacement runtime. `study.design.json` remains an unapproved import contract. Store collection decisions separately in `collection.json` using `0.3-collection.1`. See the explicitly synthetic [test settings](./drafts/v0.3/cbc/golden-reference/collection.test.example.json). Its fictional contact and approvals are not suitable for a real study.

```sh
python3 -m greedyq cbc-package path/to/study --collection path/to/collection.json --output path/to/new-package
```

This is a **preparation package**, not a folder to upload wholesale. It includes the private `registered-model.json` and migrations. The participant HTML contains only the public study descriptor, not the full choice design. Register the reviewed immutable model with `registerCBCStudy`, then use `prepareCBCDeployments` to make separate allowlisted `survey/` and `results/` folders. Only the results site receives a server Supabase key, in its server environment; the participant site receives the publishable key. Enforce Vercel Authentication on **all deployments/routes of the results project**, including `/api/results`. Check signed-out rejection after deployment.

Apply unchanged migrations 001–008 followed by additive **009_cbc.sql** through the migration ledger. Existing v0.2 installations do not need 009 unless enabling CBC. Never rewrite applied migrations or alter an existing approved study model. Use a new study ID for a materially different registered design, consent or collection mode. `migrate` accepts exactly the original ordered set or that set followed by 009. `gq_study_plans` stores the immutable reviewed CBC plan; session, consent, assignment, lifecycle and structured exposure/choice records stay in the existing seven-table archive boundary. No extra participant-data table is omitted by archival.

The canonical CBC RPC protocol is `cbc-1`: start/resume, consent, server allocation/presentation, revision-checked idempotent steps and withdrawal. General v0.2 writer/creator/resumer routes cannot bypass the CBC checks or reveal all blocks. Stable server rows use question IDs `cbc:<task_id>` with a structured `kind=cbc` value. Code IDs remain strings. Design changes invalidate the hash and require review. Production approvals are researcher attestations, not evidence of ethics-board approval or guaranteed scientific validity.


Agents with browser/JavaScript tools can call `greedyQCBC.importDesign` and `greedyQCBC.collectionModel(cbc, settings, release)` directly; the latter is checked against the Python reference. Pass that reviewed model as `model` to `prepareCBCDeployments`, or use a Python preparation package. This does not require installing Python on the researcher’s Windows or Mac device. For an Excel-backed package the CLI also accepts `--workbook path/to/design.xlsx`. The preparation root contains `.vercelignore` excluding all files and a checksummed package manifest; only the explicitly separated publication directories are deployable outputs.

## Current boundaries

This is the dedicated CBC package workflow, not yet a registered v0.2 `sd_cbc` control or an arbitrary QMD mixed-question CBC authoring path. Native surveydown CBC export, automatic design optimization/inference, fresh-account CBC cloud acceptance and paid CBC recruitment remain unverified or unimplemented as recorded in the [collection verification record](./docs/cbc-collection-verification-2026-10-26.md). Do not silently substitute multiple-choice questions and claim equivalent export. Existing v0.2 survey/Prolific verification does not automatically validate CBC fielding.

## CBC presentation styles

Ask the researcher to choose the appearance before fielding. The fixed greedyQ renderer supports **button profiles** (click the whole alternative) and **comparison tables**. Each supports horizontal, vertical, or computer-horizontal/mobile-vertical presentation. Request, for example, “Use button profiles side by side on computers and stacked vertically on phones.” This is an appearance decision; block assignment, task order, alternative codes, none handling and saved choices keep their existing meanings.

The agent writes an optional field in `study.design.json`:

```json
"presentation": {"type": "buttons", "orientation": "responsive"}
```

`type` accepts `buttons` or `table`; `orientation` accepts `horizontal`, `vertical`, or `responsive`. The preview offers the same choices above its two panes. Changing presentation produces a different checked-design hash and separate virtual sessions, so review the resulting participant experience again and rebuild/register the reviewed collection plan before deploying it. Previously registered plans cannot be silently changed. Absent this field, the existing layout and hash are preserved. Explicit horizontal presentation on a small screen can scroll within the comparison area; vertical and responsive mobile layouts fit without sideways page scrolling. Preview choices do not update an already deployed survey.

The public [surveydown buttons](https://surveydown.org/templates/conjoint_buttons) and [tables](https://surveydown.org/templates/conjoint_tables) examples inform the two presentation categories; implementation is independently authored, without copying surveydown source. These are greedyQ CBC presentation settings, not a claim of interchangeable native surveydown conjoint code.
