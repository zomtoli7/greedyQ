# greedyQ Roadmap

[한국어](./roadmap(kor).md)

**Status:** Draft

**Planning principle:** Specification before implementation

## Phase 0: Project foundation

- [x] Establish the initial product direction.
- [x] Define English as the documentation source of truth.
- [x] Require a synchronized `(kor).md` copy for every Markdown document.
- [x] Create the initial README, product brief, and roadmap.
- [x] Select the MIT License for greedyQ.
- [x] Initialize the local Git repository.
- [x] Create and connect the GitHub repository.

## Phase 1: Surveydown specification research

Research the current public, user-facing surveydown behavior from primary sources and executable examples.

- [x] Inventory project and file structure.
- [x] Document QMD front matter and page grammar.
- [x] Inventory all public question types and arguments.
- [x] Document navigation and survey lifecycle behavior.
- [x] Document theme and survey settings.
- [x] Analyze required, validation, shuffle, and metadata behavior.
- [x] Analyze `app.R` logic: show, skip, stop, and reactive behavior.
- [x] Analyze randomization and stored-value behavior.
- [x] Analyze session persistence and PostgreSQL/Supabase behavior.
- [ ] Create independently authored conformance fixtures from documented public behavior.
- [x] Establish a no-source-code-reuse policy for the independent implementation.

Deliverables:

```text
docs/surveydown-compatibility.md
docs/surveydown-compatibility(kor).md
```

## Phase 2: greedyQ v0.1 specification

- [ ] Define the supported QMD grammar.
- [ ] Define the restricted `sd_*()` expression grammar.
- [ ] Define the Survey AST / JSON schema.
- [ ] Define `greedyq.yml` and its expression language.
- [ ] Define navigation, validation, and lifecycle semantics.
- [ ] Define randomization semantics and stored metadata.
- [ ] Define persistence and session behavior.
- [ ] Define the Supabase schema.
- [ ] Define ethics/IRB metadata without making compliance claims.
- [ ] Define versioned consent, refusal, amendment, and withdrawal semantics.
- [ ] Define the generic external-respondent contract and Prolific preset.
- [ ] Define the structured preregistration contract, template adapters, and artifact manifest.
- [ ] Define stable validator diagnostic codes.
- [x] Define the display-label/stored-value direction and mandatory cross-artifact checks.
- [x] Require published-schema validation for every AI state artifact.
- [x] Define canonical atomic withdrawal, RLS, and analysis-export SQL behavior.
- [x] Separate methodological review warnings from deterministic conformance errors.
- [ ] Classify every feature as directly portable, generated to native surveydown, greedyQ-only, or unsupported.
- [ ] Define the native surveydown export contract for `survey.qmd`, generated `app.R`, supporting files, and compatibility reports.

Deliverables:

```text
docs/greedyq-v0.1-spec.md
docs/greedyq-v0.1-spec(kor).md
```

## Phase 3: AI-guided workflow specification

Specify the primary product experience before building the runtime.

- [x] Define capability detection and Chat/Agent mode selection.
- [x] Define the phased, one-question-at-a-time interview protocol.
- [x] Define study-state, assumption, unresolved-decision, and decision-log formats.
- [x] Define when the LLM performs research review and when researcher confirmation is mandatory.
- [x] Define artifact update checkpoints and resumable conversation handoff.
- [x] Define IRB/ethics, consent, respondent-source, privacy, and deployment interview stages.
- [x] Define the LLM output-file contract and generation notes.
- [x] Define the validation/correction loop and stable LLM-facing diagnostics.
- [x] Define pre-preview and pre-deployment approval gates.
- [x] Define the preregistration review, explicit submission approval, and pre-fielding lock gates.
- [x] Define truthful completion and verification requirements for external operations.
- [x] Define capability-adaptive structured interview controls and numbered fallback.
- [x] Make hands-on interactive preview review a pre-deployment checkpoint.
- [x] Publish full and compact versioned guides with a complete reference study.
- [ ] Test guided creation and correction workflows with multiple capable LLMs.

Deliverables:

```text
guides/greedyq-guide.md
guides/greedyq-guide(kor).md
guides/greedyq-guide-compact.md
guides/greedyq-guide-compact(kor).md
examples/complete-study/
```

## Phase 4: Architecture and deployment skeleton

- [ ] Select parser libraries and finalize the grammar implementation approach.
- [ ] Create the TypeScript parser and normalized AST packages.
- [ ] Create the validator and LLM-friendly diagnostic format.
- [ ] Implement `GQ011` stored-value symbol-table and cross-artifact validation.
- [ ] Implement `GQ012` validation of all generated `.greedyq/*.json` files.
- [ ] Implement `GQ013` migration-contract validation for withdrawal, RLS, and export.
- [ ] Reject unknown QMD front-matter keys in generation/strict mode.
- [ ] Create the native surveydown exporter and deterministic `app.R` generator.
- [ ] Create the React/Next.js renderer skeleton.
- [ ] Create the safe self-contained preview runtime and researcher debug panel.
- [ ] Create Supabase migrations and access policies.
- [ ] Create a Vercel deployment template.
- [ ] Implement local validation and preview commands.
- [ ] Add automated tests for independently authored conformance fixtures and native export snapshots.

## Phase 5: AI-guided end-to-end MVP

Implement the smallest complete conversational study path.

- [ ] Start from the versioned guide and a natural-language study request.
- [ ] Conduct a resumable one-question-at-a-time interview.
- [ ] Record and obtain approval for material research decisions.
- [ ] Generate valid study, consent, respondent-source, and deployment artifacts.
- [ ] Generate human-readable and machine-readable preregistration artifacts from confirmed decisions.
- [ ] Generate a native surveydown project and explicit compatibility report from the same validated study.
- [ ] Render Markdown pages and basic navigation.
- [ ] Implement text, textarea, numeric, single-choice, and multiple-choice questions.
- [ ] Implement required fields and basic validation.
- [ ] Create anonymous respondent sessions.
- [ ] Persist partial progress and completed responses.
- [ ] Implement simple and block random assignment.
- [ ] Persist assignment metadata across resumed sessions.
- [ ] Support Chat-mode deployment handoff and Agent-mode verified deployment.
- [ ] Export analysis-ready data.
- [ ] Deploy and verify a complete example study on Vercel and Supabase.

## Phase 6: Compatibility expansion

- [ ] Implement select, slider, date, Likert, and matrix questions.
- [ ] Implement supported surveydown settings.
- [ ] Implement declarative show, skip, stop, and validation rules.
- [ ] Implement option, item, page, and task-order shuffling.
- [ ] Improve migration diagnostics for unsupported `app.R` code.
- [ ] Add regression tests for the compatibility matrix.

## Phase 7: Research-specific capabilities

- [ ] Weighted and stratified randomization
- [ ] Factorial experiment definitions
- [ ] Reproducible seeded assignment
- [ ] Attention checks
- [ ] Timers and page dwell time
- [ ] Response revision history
- [ ] Prolific participant and completion-code support
- [ ] Structured ethics/IRB metadata and reusable information blocks
- [ ] Additional registry and discipline-specific preregistration template adapters
- [ ] First-class consent with document version, hash, and timestamp
- [ ] Generic respondent-collector integration contract
- [ ] Prolific preset with completion and screen-out routes
- [ ] Duplicate-participation and external-ID validation policies
- [ ] Conjoint/CBC rendering and data capture
- [ ] External CSV experimental designs
- [ ] Multilingual surveys

## Phase 8: PPTX import path

- [ ] Extract text, tables, images, and speaker notes from PPTX.
- [ ] Infer pages and common question structures from slide layout.
- [ ] Support optional authoring metadata for deterministic conversion.
- [ ] Generate `survey.qmd`, `greedyq.yml`, and assets.
- [ ] Produce a conversion report with confidence and warnings.
- [ ] Feed generated artifacts into the guided AI review workflow.
- [ ] Validate generated projects automatically.

## Cross-cutting requirements

These requirements apply to every phase:

- Preserve English/Korean documentation parity.
- Version all normative formats and generated artifacts.
- Prefer deterministic, testable behavior.
- Never execute arbitrary R or JavaScript from a survey definition.
- Preserve researcher ownership of respondent data.
- Record enough metadata to reproduce fielded experiments.
- Keep the core workflow usable without R, RStudio, Quarto, or Shiny.
- Keep the Vercel/Supabase web-native runtime as the primary execution path.
- Generate native surveydown projects as a first-class path for unrestricted R, Shiny, and Quarto customization.
- Implement compatibility from public documentation without incorporating surveydown source code.
- Preserve attribution without implying affiliation, endorsement, or shared maintainership.
- Keep the primary experience model-agnostic and usable with multiple capable LLMs.
- Preserve researcher authority through explicit approval of material decisions.
- Never invent unresolved hypotheses, sample sizes, exclusions, outcomes, or analysis commitments in a preregistration.
- Never submit, publish, or embargo a registration without explicit researcher approval and verified external results.
- Never claim external setup or deployment succeeded without performing and verifying it.

## Immediate next actions

1. Review and freeze the v0.1 grammar and state contracts against the golden reference.
2. Run the full and compact guides with multiple GPT and Claude configurations.
3. Turn behavioral failures into guide revisions and repeatable evaluation cases.
4. Implement the QMD parser, normalized AST, and validator against independent fixtures.
5. Implement the native surveydown exporter and web-runtime skeleton from the same AST.
