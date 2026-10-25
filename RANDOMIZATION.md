# Random assignment and question order

[한국어](./RANDOMIZATION(kor).md)

## Researcher choices

greedyQ supports one between-participant assignment per study. Your AI must explain the choices and ask you to approve the method, conditions, ratio, assignment point, and (when applicable) block size. It must not choose these research decisions silently.

- **Simple random assignment:** each participant receives an independent draw. A 1:1 ratio means a 50% chance of each condition, not equal final sample sizes.
- **Fixed-block random assignment:** each block contains the approved numbers of each condition in a randomly shuffled order. With a block size of 4 and ratio 1:1, every completed block contains two participants per condition. An incomplete last block and participant dropout can leave the analyzed groups unequal. Known fixed block sizes can make later assignments predictable; consider this when deciding whether the method suits the study.
- **Question shuffling:** independently shuffle selected questions on the same page for each participant. Unselected questions stay in their original positions. Returning to the page or resuming the session preserves that participant's order. Answer-option shuffling and shuffling entire pages are not included in this feature.

Examples of requests:

> Assign participants independently to A or B with equal probability. Explain what I should expect if I recruit 100 people.

> Use blocks of six, with twice as many participants in A as B. Ask me to confirm before applying this.

> Shuffle the three satisfaction questions on this page, but keep the overall rating first and the free-text suggestion last.

> Show me both conditions and verify that refreshing does not change a participant's assignment or question order.

No setting is silently changed in an existing study. Use a new study ID for an altered registered plan. Reuse of a session is stable; direct visitors who start a different session are not automatically identified as the same person.

## Canonical configuration

These settings belong in `greedyq.yml`, not in executable R or agent-written JavaScript. Condition weights are positive integers with total at most 1000. For `fixed_block`, `block_size` must be a multiple of that total, from 2 to 1000. For `simple`, omit `block_size`.

```yaml
randomization:
  - id: information_frame
    unit: respondent
    method: fixed_block
    block_size: 4
    conditions:
      control: 1
      treatment: 1
    assignment_point:
      after_page: baseline
      before_condition_pages: [stimulus_control, stimulus_treatment]
    persistence_key: session_id
    store:
      condition_as: assignment_condition

question_order:
  - page: satisfaction
    questions: [ease_of_use, design_help, output_quality]
```

All referenced pages/questions must exist. Only one shuffle group per page is supported. Keep the consent page fixed, and keep same-page dependent questions and their trigger questions outside shuffle groups. The validator rejects unsupported units, methods, multiple assignment stages, invalid weights/block sizes, invalid shuffle references, and assignment before the consent page. Check every actual branch in preview; source order alone cannot prove all research logic is appropriate.

## Fixed implementation and records

The reference algorithms are in `greedyq/randomization.py`; the browser implementation is in `web/greedyq-core.js`; the database implementation is the additive `templates/supabase/004_randomization.sql`. Reuse these files unchanged. Python uses `secrets.randbelow`, browsers use Web Crypto with rejection sampling, and PostgreSQL uses pgcrypto with rejection sampling. Fisher–Yates shuffles block schedules and question groups. The same rules and distributions apply across runtimes; independent participants and platforms do not receive identical random sequences.

Assignments happen after valid answers at the declared boundary, and after consent when consent is configured. The live database uses the server-registered model, not client-supplied conditions or ratios. It commits an assignment before the stimulus is displayed. Concurrent requests serialize allocation; a retry returns the original assignment. Test and production use separate block schedules. Withdrawal does not rewind or refill consumed block slots. Balance refers to allocated participants, not only completed/nonwithdrawn responses.

The database stores randomization ID, condition, method, block ID when relevant, unique draw ID, specification version, and timestamp. A draw ID is an audit identifier, not a replay seed. Future block entries are private; the browser never receives the live schedule. The web-hosted local preview uses private-to-that-browser simulated schedules and IndexedDB transactions to coordinate tabs, not a production database. Fixed templates await `backend.ready` before mounting. `backend.synchronize()` refreshes the diagnostic snapshot from other tabs.

For a double-clicked `file:` preview, each tab has its own session-storage simulation because browsers do not provide consistent shared-file-origin storage behavior. Refreshing the same tab resumes it; closing it ends that simulation. Desktop/mobile panes in that tab still share the simulated allocation pool with independent participant IDs. An upgrade resets old mock storage; it never resets live participant data.

Question orders are stored as ordered question IDs in `question_orders`, retained on resume, and included in the results CSV and archive CSV/JSON. The result CSV also includes `randomization_method`, `block_id`, `draw_id`, and `assignment_at`. These describe presentation, not response values. Preview's Structure view shows source order and marks shuffled questions; the actual panes show participant-specific order. Forced-condition preview controls are for inspection, not evidence of the allocation distribution.

`question_orders` records the full page order before conditional visibility filtering. Hidden questions can therefore appear in this list; it is not proof that every listed question was displayed or read. Withdrawal with deletion clears this ordering record too.

## Deployment and upgrade

The agent applies migrations **001–006** in order, then calls `registerStudy(client, model)` from `tools/cloud_lifecycle.cjs` with the reviewed compiled model. This is a privileged setup step; no server credential belongs in the survey. Run the existing checksum/ledger checks. Registering exactly the same model is safe to retry; a different registered model requires a new study ID. Register studies without random assignment too: the save boundary uses their consent and question definitions.

Do not modify already-applied 001–003. Existing databases without an applied-migration ledger need explicit reconciliation. Existing experimental studies with legacy assignments require a **new study ID**; never relabel old least-count assignments as random. Applying 004 changes the save boundary for the database: register all studies that must remain usable in that database and deploy the matching runtime during an approved maintenance window. Otherwise saves fail closed. Test the migration on a separate test database first.

This implementation update does not itself migrate or redeploy an existing Vercel/Supabase project. Live acceptance after approval must verify a direct test completion, resume, both conditions, test/real isolation, and the CSV records. Local tests are not proof that a previously deployed URL is updated.

## Compatibility and limits

Native Surveydown export reports its random-draw translation as unverified; it does not claim fixed-block or persistence equivalence. Question shuffling is reported as unsupported in native export and retains source order. Do not field that export as an equivalent randomized study without implementing and validating the reported differences.

Stratification, variable block sizes, cluster assignment, multiple independent stages and external allocation services remain outside this implemented contract. The AI must state these limits instead of inventing runtime code or silently substituting another design. Choice and page ordering use the separate contracts below.

## Choice and page ordering

In the `survey.qmd` header, `survey-settings.shuffled` accepts a question ID or a single-question mapping to one-based positions. For example, `shuffled: [{satisfaction: "1-4"}]` shuffles only the first four positions; all other positions remain fixed. Lists such as `[1, 3, 5]` and combined ranges such as `["1-3", "5-7"]` are supported. `all-shuffled: true` applies to supported types. This means choice options for mc/mc_buttons/mc_multiple/mc_multiple_buttons and rows for matrix, not matrix columns. Save values and labels remain paired. Unknown types, duplicate positions and invalid ranges fail validation.

For independent pages, use `page_order: [topics, preferences, experience]` in `greedyq.yml`. They must be one contiguous middle group in source order, without explicit next-page links or show/skip rules. Opening, consent, assignment, treatment and ending pages stay fixed. The validator rejects unsupported combinations instead of guessing what a branch should do. This is a greedyQ extension, not a documented Surveydown page-shuffle setting.

The browser saves `option_orders` and `page_order` per session, including across refresh. Raw/CSV exports retain them. Native export preserves official choice-shuffle settings but reports question/page shuffling as unsupported. See the [compatibility audit](./docs/surveydown-compatibility-audit.md).
