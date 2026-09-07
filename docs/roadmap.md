# greedyQualt Roadmap

[한국어](./roadmap(kor).md)

**Status:** Draft

**Planning principle:** Specification before implementation

## Phase 0: Project foundation

- [x] Establish the initial product direction.
- [x] Define English as the documentation source of truth.
- [x] Require a synchronized `(kor).md` copy for every Markdown document.
- [x] Create the initial README, product brief, and roadmap.
- [ ] Select an open-source license.
- [ ] Initialize the local Git repository.
- [ ] Create and connect the GitHub repository.

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
- [ ] Collect representative official examples as conformance fixtures.

Deliverables:

```text
docs/surveydown-compatibility.md
docs/surveydown-compatibility(kor).md
```

## Phase 2: greedyQualt v0.1 specification

- [ ] Define the supported QMD grammar.
- [ ] Define the restricted `sd_*()` expression grammar.
- [ ] Define the Survey AST / JSON schema.
- [ ] Define `greedyqualt.yml` and its expression language.
- [ ] Define navigation, validation, and lifecycle semantics.
- [ ] Define randomization semantics and stored metadata.
- [ ] Define persistence and session behavior.
- [ ] Define the Supabase schema.
- [ ] Define ethics/IRB metadata without making compliance claims.
- [ ] Define versioned consent, refusal, amendment, and withdrawal semantics.
- [ ] Define the generic external-respondent contract and Prolific preset.
- [ ] Define stable validator diagnostic codes.
- [ ] Mark every surveydown feature as supported, partial, unsupported, or deferred.

Deliverables:

```text
docs/greedyqualt-v0.1-spec.md
docs/greedyqualt-v0.1-spec(kor).md
```

## Phase 3: Architecture and deployment skeleton

- [ ] Select parser libraries and finalize the grammar implementation approach.
- [ ] Create the TypeScript parser and normalized AST packages.
- [ ] Create the validator and diagnostic format.
- [ ] Create the React/Next.js renderer skeleton.
- [ ] Create Supabase migrations and access policies.
- [ ] Create a Vercel deployment template.
- [ ] Implement local validation and preview commands.
- [ ] Add automated tests for documented conformance fixtures.

## Phase 4: End-to-end MVP

Implement the smallest complete survey path.

- [ ] Render Markdown pages and basic navigation.
- [ ] Implement text, textarea, numeric, single-choice, and multiple-choice questions.
- [ ] Implement required fields and basic validation.
- [ ] Create anonymous respondent sessions.
- [ ] Persist partial progress and completed responses.
- [ ] Implement simple and block random assignment.
- [ ] Persist assignment metadata across resumed sessions.
- [ ] Export analysis-ready data.
- [ ] Deploy a complete example study to Vercel and Supabase.

## Phase 5: Compatibility expansion

- [ ] Implement select, slider, date, Likert, and matrix questions.
- [ ] Implement supported surveydown settings.
- [ ] Implement declarative show, skip, stop, and validation rules.
- [ ] Implement option, item, page, and task-order shuffling.
- [ ] Improve migration diagnostics for unsupported `app.R` code.
- [ ] Add regression tests for the compatibility matrix.

## Phase 6: Research-specific capabilities

- [ ] Weighted and stratified randomization
- [ ] Factorial experiment definitions
- [ ] Reproducible seeded assignment
- [ ] Attention checks
- [ ] Timers and page dwell time
- [ ] Response revision history
- [ ] Prolific participant and completion-code support
- [ ] Structured ethics/IRB metadata and reusable information blocks
- [ ] First-class consent with document version, hash, and timestamp
- [ ] Generic respondent-collector integration contract
- [ ] Prolific preset with completion and screen-out routes
- [ ] Duplicate-participation and external-ID validation policies
- [ ] Conjoint/CBC rendering and data capture
- [ ] External CSV experimental designs
- [ ] Multilingual surveys

## Phase 7: LLM authoring vignette

Design the specification and validation surface so general-purpose language models can reliably author studies.

- [ ] Publish a full versioned authoring vignette.
- [ ] Publish a token-efficient compact vignette.
- [ ] Provide a complete reference study.
- [ ] Define the LLM output-file contract and generation notes.
- [ ] Add a mandatory pre-output self-check.
- [ ] Implement `greedyqualt validate --format llm`.
- [ ] Test generation and correction workflows with GPT and Claude.
- [ ] Add conformance tests for common natural-language study requests.

Deliverables:

```text
docs/llm-authoring-vignette.md
docs/llm-authoring-vignette(kor).md
docs/llm-authoring-vignette-compact.md
docs/llm-authoring-vignette-compact(kor).md
examples/complete-study/
```

## Phase 8: PPTX converter

- [ ] Extract text, tables, images, and speaker notes from PPTX.
- [ ] Infer pages and common question structures from slide layout.
- [ ] Support optional authoring metadata for deterministic conversion.
- [ ] Generate `survey.qmd`, `greedyqualt.yml`, and assets.
- [ ] Produce a conversion report with confidence and warnings.
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

## Immediate next actions

1. Collect executable conformance fixtures for the v0.1 compatibility targets.
2. Turn the research findings into the normative greedyQualt v0.1 specification.
3. Define the restricted QMD/R-expression grammar and normalized Survey AST.
4. Define persistence, randomization, privacy, and validation semantics.
