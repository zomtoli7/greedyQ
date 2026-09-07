# greedyQualt Product Brief

[한국어](./product-brief(kor).md)

**Status:** Draft

**Product stage:** Pre-implementation specification

**Document role:** Product direction and decision framework

## 1. Product definition

greedyQualt is an open-source, Markdown-first platform for building, deploying, and operating academic surveys and experiments. It accepts surveydown-compatible survey definitions where practical, compiles them into a safe internal schema, renders them as web applications, and stores responses in researcher-owned infrastructure.

The product is not intended to be a pixel-for-pixel Qualtrics clone or another GUI form builder. Its primary abstraction is a version-controlled study specification.

### Core proposition

> Keep the survey-as-code idea. Remove R, RStudio, Quarto, and Shiny from the required toolchain.

### Product promise

> Your survey. Your database. Your data.

## 2. Problem

Academic researchers need powerful survey and experimental capabilities, but existing approaches impose avoidable costs:

- Commercial platforms are expensive and may reduce academic support.
- GUI-authored studies are difficult to review with diffs and reproduce from a precise version.
- Advanced experiments often require platform-specific custom JavaScript.
- Hosted platforms place data storage and operational control with a vendor.
- R/Shiny-based survey-as-code systems require a specialized local and deployment toolchain.

These limitations are especially costly for studies involving random assignment, repeated choice tasks, complex branching, conjoint/CBC, or auditable research workflows.

## 3. Target users

### Primary users

- Academic researchers seeking reproducible survey workflows
- Researchers leaving or supplementing expensive proprietary platforms
- Researchers willing to work with text files and Git, directly or with AI assistance
- Experimental researchers who need randomization, factorial designs, or conjoint/CBC
- Surveydown users who want to retain `survey.qmd` while replacing the R/Shiny runtime

### Not an initial target

Users whose primary requirement is a drag-and-drop visual survey editor are not the initial target audience.

## 4. Product principles

1. **The study specification is the source of truth.** Survey content, logic, and design must be inspectable and version controlled.
2. **Compatibility is user-facing.** Target surveydown's public authoring specification, not its internal implementation.
3. **No arbitrary code execution.** R chunks are parsed only as a restricted set of supported `sd_*()` expressions.
4. **Logic is declarative.** Branching, validation, and randomization use a safe, documented DSL.
5. **Research comes first.** Reproducible randomization, experimental metadata, and analysis-ready data are core concerns.
6. **Researchers own their data.** Responses go to the researcher's Supabase project; greedyQualt does not operate a central respondent-data service.
7. **No GUI dependency.** A GUI survey builder is not required for authoring or deployment.
8. **AI is an authoring interface, not a proprietary dependency.** The specification should enable general-purpose LLMs to generate valid studies.
9. **Deployment should be mundane.** GitHub, Vercel, and Supabase should be sufficient for a production survey.
10. **Research governance must be explicit.** Ethics-review metadata, consent, and respondent-source records should be structured, versioned, and auditable without claiming legal or institutional compliance.

## 5. Compatibility strategy

| Layer | greedyQualt policy |
| --- | --- |
| `survey.qmd` page and question syntax | Compatible wherever practical |
| Surveydown YAML settings | Compatible where documented and feasible |
| `app.R` | Not executed; replaced by declarative configuration |
| Arbitrary R/Shiny reactive code | Unsupported |
| Question types | Implement surveydown's public question API first |
| Conditional logic | Native declarative DSL |
| Randomization | Native first-class feature |
| Database | Researcher-owned Supabase/PostgreSQL |
| Runtime | TypeScript, React, and a web-native server/runtime layer |
| Hosting | Vercel-first |

The intended migration story is:

```text
Existing surveydown project

survey.qmd  ----------------------> retained where compatible
app.R       -- migration tooling -> greedyqualt.yml
                                      |
                                      v
                               greedyQualt runtime
                                      |
                                      v
                              Vercel + Supabase
```

## 6. Proposed technical model

```text
survey.qmd
greedyqualt.yml
design/*.csv
assets/*
      |
      v
QMD parser + restricted sd_* parser
      |
      v
Internal Survey AST / JSON schema
      |
      +-- validator
      +-- logic engine
      +-- randomization engine
      +-- migration diagnostics
      |
      v
React/Next.js survey renderer
      |
      v
Vercel deployment
      |
      v
Researcher's Supabase/PostgreSQL
```

The exact libraries, framework versions, schema layout, and supported function arguments remain specification-stage decisions.

## 7. Proposed project format

```text
my-survey/
├── survey.qmd
├── greedyqualt.yml
├── design/
│   └── choice_sets.csv
├── assets/
└── supabase/
    └── migrations/
```

- `survey.qmd`: Pages, Markdown content, questions, and navigation
- `greedyqualt.yml`: Display rules, branching, validation, and randomization
- `design/*.csv`: Conjoint/CBC and repeated experimental designs
- `assets/`: Images and experimental stimuli
- `supabase/`: Reproducible database migrations

## 8. Declarative logic

`greedyqualt.yml` replaces supported `app.R` use cases with a constrained expression language.

```yaml
logic:
  show:
    - question: q2
      if: q1 == "yes"

  skip:
    - if: age < 18
      to: screenout

  validate:
    - question: zipcode
      if: length(zipcode) != 5
      message: "Zip code must be 5 digits."
```

The expression language must be deterministic, statically validatable, and unable to execute arbitrary JavaScript.

## 9. Randomization as a first-class feature

The engine should ultimately support:

- Simple and weighted random assignment
- Block and stratified randomization
- Factorial designs
- Question, option, page, stimulus, and task-order randomization
- Persistent assignment across refresh and resumed sessions
- Seeded and reproducible assignment
- Stored assignment metadata, including condition, seed, block, and timestamp
- Transaction-safe assignment under concurrent enrollment

Example direction:

```yaml
randomization:
  framing_experiment:
    type: between_subject
    method: block
    seed_by: respondent_id

    factors:
      frame: [gain, loss]
      information: [low, high]

    store:
      - frame
      - information
      - randomization_seed
      - block_id
```

## 10. Persistence and data ownership

The initial data model is expected to cover:

```text
studies
respondents
responses
assignments
choice_tasks
event_log
```

Required behavior includes anonymous sessions, resumable progress, page-level saves, completion state, URL metadata such as Prolific IDs, and analysis-ready export. The specification phase will decide where normalized relational tables or JSONB are appropriate.

## 11. Authoring paths

### 11.1 Direct authoring

Experienced users edit `survey.qmd`, `greedyqualt.yml`, and design files directly. Git history records the exact fielded study.

### 11.2 Follow-up tool 1: PPTX converter

The converter produces a high-quality, editable first draft rather than claiming perfect semantic recovery.

```text
survey.pptx
    |
    v
greedyqualt convert survey.pptx
    |
    +-- survey.qmd
    +-- greedyqualt.yml
    +-- assets/*
    +-- conversion-report.md
```

It should use PPTX structure, layout, tables, speaker notes, and optional metadata to infer pages and questions while reporting ambiguous conversions.

### 11.3 Follow-up tool 2: LLM authoring vignette

A standalone, versioned Markdown vignette teaches GPT, Claude, and other general-purpose LLMs how to generate valid greedyQualt projects from natural-language research requirements.

```text
llm-authoring-vignette.md
             +
natural-language study request
             |
             v
        GPT / Claude
             |
             +-- survey.qmd
             +-- greedyqualt.yml
             +-- design/*.csv
             +-- generation notes
             |
             v
greedyqualt validate --format llm
             |
             v
     LLM-assisted correction
```

The vignette should contain:

- A normative project and output-file contract
- Exact QMD, YAML, logic, randomization, and CSV syntax
- Supported and prohibited constructs
- Complete working examples
- Stable specification-version declarations
- A mandatory generation self-check
- Machine-actionable validation guidance

Planned artifacts:

```text
docs/llm-authoring-vignette.md
docs/llm-authoring-vignette-compact.md
examples/complete-study/
```

The validator should provide stable diagnostic codes and precise locations so a user can return the result to an LLM for correction.

## 12. Initial success criteria

The first end-to-end milestone succeeds when a researcher can:

1. Define a small study in a documented QMD subset.
2. Validate it without installing R.
3. Preview and deploy it as a web application.
4. Enroll a respondent with persistent experimental assignment.
5. Save partial and completed responses to the researcher's Supabase.
6. Export analysis-ready data.
7. Reproduce the fielded study from a Git commit and recorded specification version.

## 13. Research governance and respondent sources

### 13.1 Ethics and IRB metadata

greedyQualt should provide structured metadata and reusable presentation blocks for ethics-review information.

```yaml
study:
  title: Hotel Choice Study

  ethics:
    institution: Example University
    protocol-id: IRB-2026-0123
    approval-date: 2026-08-01
    principal-investigator: Jane Doe
    contact: jane@example.edu
```

The engine may validate required project fields, render the declared information, and preserve it with a fielded study version. It must not claim that a study is IRB-approved, legally compliant, or ethically sufficient. Approval and compliance remain the researcher's and institution's responsibility.

### 13.2 First-class consent

Consent should be a semantic study primitive rather than an ordinary multiple-choice question by convention.

```yaml
consent:
  page: consent
  question: consent_agreement
  accepted-value: yes
  rejected-page: consent_declined
  required: true
  record:
    - consent-version
    - consent-timestamp
    - consent-document-hash
```

The v0.1 specification should define:

- Blocking access to study questions until required consent is accepted
- A deterministic route for declined consent
- Consent document version and content hash
- Server-recorded acceptance timestamp
- Behavior when consent wording changes during fielding
- Withdrawal and response-retention policy hooks
- Optional parental/guardian-consent extensions without assuming jurisdictional rules
- Validator errors for incomplete or inconsistent consent configuration

Electronic signatures and jurisdiction-specific compliance workflows are deferred until their legal and operational requirements are separately specified.

### 13.3 External respondent collectors

greedyQualt should provide a provider-neutral integration contract plus named presets for common respondent platforms.

```yaml
respondent-source:
  provider: prolific

  capture:
    participant-id: PROLIFIC_PID
    study-id: STUDY_ID
    session-id: SESSION_ID

  completion:
    complete: https://app.prolific.com/submissions/complete?cc=ABC123
    screenout: https://app.prolific.com/submissions/complete?cc=SCREEN1
```

The generic contract should support:

- Allowlisted inbound URL parameters
- Required-parameter validation
- Canonical participant, study, and external-session identifiers
- Duplicate-participation policy
- Separate completion routes for complete, screen-out, quota-full, and technical-error outcomes
- Safe parameter interpolation into allowlisted redirect destinations
- Explicit storage and privacy policy for raw external parameters
- Test mode that prevents accidental production completion redirects

A Prolific preset is an initial target. Other providers should use the same generic contract rather than introducing provider-specific runtime logic.

## 14. Open decisions

- Exact v0.1 surveydown compatibility boundary
- Parser implementation and grammar strategy
- Next.js and runtime architecture
- Supabase relational/JSONB schema boundaries
- Safe expression-language grammar
- Transaction model for balanced randomization
- Initial license: MIT or Apache-2.0
- Public naming and trademark review before broad release
- Minimum required ethics metadata and how it varies by study template
- Consent amendment, withdrawal, and response-retention semantics
- Prolific completion-status mapping and duplicate-participation defaults
