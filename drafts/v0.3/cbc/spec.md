# greedyQ v0.3 CBC specification draft

[한국어](./spec(kor).md)

**Draft contract `0.3-draft.1`; import and local preview model `0.3-preview.1` are implemented separately from the v0.2 survey runtime.** MUST/SHOULD below still include future server, fielding and export requirements. Current scope and commands: [CBC preview](../../../CBC.md).

## Object and scope

`greedyQCBC` is a proposed direct child of `greedyQObject`, parallel to Simple and Experiment. Reuse the core interview, governance, approval, versioning, preview, deployment and results contracts. A choice task is a structured control, not an agent-generated HTML widget. Do not activate the CBC profile in the public registry until parser, validator, runtime, storage and export conformance pass.

First scope: full-profile, unlabeled, single-choice tasks; a fixed number of ordinary alternatives; optional “none”; imported finite task tables; one assigned block per respondent; optional once-per-session task and alternative shuffling; analysis-ready long export. Ordinary questions may appear before and after the task sequence.

Adaptive CBC, alternative-specific/partial profiles, dual-response none, best–worst, conjoint ratings, automatic utility estimation, WTP, population predictions and efficient-design optimization are deferred. Do not emulate deferred features with arbitrary agent-authored scripts.

## Required interview and approval

1. Confirm research question and population, then ask whether to collaborate with the AI, fill a blank CSV/XLSX, or bring an existing design. Persist the choice.
2. Confirm attributes, level wording/units, alternatives per task, tasks per respondent, opt-out meaning, blocked design and order rules. Ask one central question at a time; never pick methodological decisions without confirmation.
3. For the blank-table route, allow a generic template before the attribute inventory is final. Once confirmed, generate matching attribute columns. Save `awaiting_design_table`, record expected files and unresolved decisions, and permit download/return/resume across hosts.
4. Read returned data as data. Show the interpreted attributes, levels, blocks, example tasks and errors in ordinary language. Researcher approval is required for remapping, recoding, deleting rows, resolving unknown levels or changing the design.
5. Keep ethics/consent scheduling consistent with core guidance. Before collection, resolve consent/privacy and approval gates; AI-suggested tasks are drafts.
6. Freeze the approved normalized design and hashes. Any material design change requires a new design version and renewed approval; never change a registered live study underneath existing respondents.

## File contracts

CSV is UTF-8, optionally with BOM, using a header row. IDs are strings; never convert `001` to `1`, translate IDs, silently trim/merge codes or infer a missing level. Fully empty rows are ignored; partial rows are errors. Reject duplicate/unknown headers and data outside the declared table. Text labels are escaped at rendering and protected in spreadsheet exports.

`attributes.csv` has `attribute_id,attribute_label,level_id,level_label`, one row per level. Each attribute has a unique stable ID, one consistent label and at least two distinct level IDs. Labels may be authored in any approved participant language. Units belong in the confirmed labels/dictionary. Numeric interpretation is a separate confirmed coding decision, not inferred from a text label.

`design.csv` has `block_id,task_id,alternative_id,<attribute_id>...`, exactly one level-code column per declared attribute. One row is one ordinary alternative of one task in one block. `(block_id,task_id,alternative_id)` is unique. Task IDs can repeat in different blocks; alternative IDs can repeat in different tasks. The ordinary alternative count is constant. Every cell references a level of its own attribute. A task must contain distinct ordinary profiles unless an explicitly modeled later extension authorizes otherwise.

The generic blank Design sheet has four placeholder attribute columns. The future agent replaces their headings with confirmed attribute IDs before interpreting it as a study design; fewer/more attributes require a matching table, not hidden unused columns. An empty template is `awaiting_input`, never a valid runnable design.

XLSX uses exact sheets `Attributes` and `Design`, with the same headers in row 1. Ignore formatting-only empty cells. Do not evaluate formulas, cached formula results, macros or external links; reject them for import and ask for a values-only file. No secrets or participant records belong in these files. Browser-native XLSX reading is implemented by the fixed preview importer. The supplied template remains a blank input artifact; it is not an approved design.

## Design inspection and provenance

Validate shape, codes, missing cells, duplicate keys/profiles, task sizes, block sizes, available levels and confirmed combination restrictions. Report level frequencies and overlaps as diagnostics; do not call a design balanced, identifiable, orthogonal or D-efficient solely because it parses or an LLM proposed it. Statistical adequacy must be justified for the confirmed analysis and design strategy.

Keep the original files, their SHA-256, declared source (manual, external tool, AI-assisted), tool/version/settings where known, mapping decisions and approved normalized data. Hash normalized JSON using sorted object keys, UTF-8, no extra whitespace, original ordered arrays and unmodified string IDs. Store original-file hashes separately; do not overwrite source files when normalizing. Generator seeds are recorded only when a real deterministic generator supports them. Do not invent a seed or import provenance.

External design tools may use different layouts or reserved codes. Import requires explicit mapping; direct Sawtooth/Qualtrics/Ngene compatibility is not claimed by this schema.

## Assignment and presentation

Block assignment, task ordering and alternative ordering are different operations. Confirm each independently. Assign a block once after consent, server-side for live collection; retries/resume preserve it. Each respondent receives only the tasks in that block. v0.2 experimental condition allocation is not automatically a CBC block API.

Persist task/alternative display orders before presenting stimuli. Choice values refer to stable alternative IDs, not the left/right position. Do not reshuffle on input, back navigation, reload or re-opening a host conversation. “None” has reserved ID `none`, a confirmed label, and fixed last position in the first slice; it is configured separately, not a fake profile with invented levels.

Desktop: aligned attribute rows and alternative columns, readable wrapping and clear single-choice controls. Mobile: keep alternatives comparable in a compact aligned grid or approved stacked layout, repeat attribute labels as needed, and avoid horizontal page scrolling. Opt-out remains separate and visible. Provide keyboard/radio semantics, a named task group and an understandable task-progress indicator. Reuse core validation: focus the first invalid task and put its message immediately above it. Do not reveal another block's stimuli through a participant shortcut; researcher preview may inspect all blocks with mock data only.

## Saved data and export

Separate design rows, assigned presentation and chosen values. Proposed exposure keys include study/design version and hash, respondent/session, block, task, task position, alternative display positions, presented/answered times and selected ID. Commit assignment/presentation through the server before treating a screen as presented; network failure must not fabricate exposure or completion. “Planned”, “presented” and “answered” are different states.

Long export has one row per alternative of each actually presented task, including a none row if offered. Include stable keys, observed display positions, level codes/labels or a versioned dictionary, design hash and `chosen`. One answered task has exactly one `chosen=1`; other alternatives are `0`. An unanswered task has missing choice values, never an inferred none choice. Do not output unshown tasks as observed responses. Include separate export metadata for consent/refusal/withdrawal and preserve test/real/source filtering.

Withdrawals must erase CBC choices and respondent-specific presentation/order records under the core policy, while retaining only disclosed administrative identifiers. Proposed server tables/RPCs require a new additive migration and conformance tests; no CBC table is installed by v0.2 closure. An imported table cannot authorize collection or satisfy unresolved ethics/sample/analysis choices.

## Golden fixture and release gates

The [course-plan reference](./golden-reference/README.md) supplies independently authored tables, a declared block plan, synthetic long data and acceptance scenarios. Its sizes are software examples, not sample-size advice or statistically optimized design.

Before declaring CBC usable, test malformed imports, blank/partial returns, non-ASCII labels, typed string IDs, forbidden combinations, both blocks, order persistence, none versus missing answers, back/reload/offline failure, simultaneous saves, withdrawal erasure, protected results, long CSV joins, modification/fork and v0.2 regression. Python/browser normalized output must match. Native Surveydown export must report CBC as unsupported until a generated custom-control implementation has its own verified semantics; never flatten it into an ordinary multiple-choice question and claim equivalence.

## Method references

The [ISPOR experimental-design report](https://www.ispor.org/docs/default-source/resources/outcomes-research-guidelines-index/piis1098301512041629.pdf?sfvrsn=d9c2e90c_0) motivates separating a study's design justification from software validation. [Sawtooth's public import/export description](https://sawtoothsoftware.com/help/lighthouse-studio/manual/importing-exporting-cbc-designs.html) illustrates an external version/task/alternative/level table. greedyQ's fixture and format are independently authored; no external code or example rows were copied.
