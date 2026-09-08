# greedyQ Product Brief

[한국어](./product-brief(kor).md)

**Status:** Draft

**Product stage:** Pre-implementation specification

**Document role:** Product direction and decision framework

## 1. Product definition

greedyQ is a specification-driven, AI-native application for online academic research. Rather than implementing the application itself in conventional source code, greedyQ specifies how a general-purpose generative AI agent should instantiate and operate the application. Its Markdown guides, schemas, checkpoints, and exact templates form a portable **agent-executable application specification**.

greedyQ itself is not an agent. The greedyQ specification combined with a capable host GenAI instantiates a greedyQ research agent. That research agent collaborates with the researcher and produces research-design artifacts plus executable respondent-facing survey software.

The product is not intended to be a pixel-for-pixel Qualtrics clone, another GUI form builder, or a proprietary AI service. Its primary user interface is a guided conversation, while its durable abstraction is a version-controlled study specification. Direct QMD authoring remains an expert path.

greedyQ is an independent MIT-licensed implementation. Its primary product is its own Vercel/Supabase web runtime; it adopts a documented subset of surveydown-style `survey.qmd` conventions for authoring compatibility and generates native surveydown projects for advanced R, Shiny, and Quarto customization. It incorporates no surveydown source code and claims no affiliation or endorsement.

### Core proposition

> Package a reproducible research methodology and workflow as an agent-executable specification that turns a capable general-purpose GenAI into a domain-specific research application.

### Architectural identity

1. **Architecture:** a specification-driven AI-native application whose normative behavior is distributed as a human-readable, agent-executable specification.
2. **Domain:** online academic research, including research design, consent, measurement, experiments, respondent collection, data planning, preregistration, deployment, and fielding.
3. **Implementation:** greedyQ, a concrete and testable implementation of that architecture.

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
- Researchers who want to create a rigorous survey through conversation without learning a survey DSL
- Expert users who prefer to inspect or edit text files and Git directly
- Experimental researchers who need randomization, factorial designs, or conjoint/CBC
- Surveydown users who want a web-native runtime while retaining a path to native R/Shiny customization

### Not an initial target

Users whose primary requirement is a drag-and-drop visual survey editor are not the initial target audience.

## 4. Product principles

1. **The study specification is the source of truth.** Survey content, logic, and design must be inspectable and version controlled.
2. **Compatibility is user-facing and independently implemented.** Target surveydown's publicly documented authoring conventions without incorporating surveydown source code.
3. **No arbitrary code execution.** R chunks are parsed only as a restricted set of supported `sd_*()` expressions.
4. **Logic is declarative.** Branching, validation, and randomization use a safe, documented DSL.
5. **Research comes first.** Reproducible randomization, experimental metadata, and analysis-ready data are core concerns.
6. **Researchers own their data.** Responses go to the researcher's Supabase project; greedyQ does not operate a central respondent-data service.
7. **No GUI dependency.** A GUI survey builder is not required for authoring or deployment.
8. **The agent-executable specification is the application core.** A capable general-purpose GenAI instantiates it as a greedyQ research agent that interviews the researcher, maintains study state, and produces valid artifacts.
9. **Deployment should be mundane.** GitHub, Vercel, and Supabase should be sufficient for a production survey.
10. **Research governance must be explicit.** Ethics-review metadata, consent, and respondent-source records should be structured, versioned, and auditable without claiming legal or institutional compliance.
11. **The LLM provides research intelligence.** greedyQ should not duplicate a model's evolving methodological knowledge; it should define when review occurs, which decisions require confirmation, and how decisions are recorded.
12. **Researcher authority is preserved.** The AI explains concerns and proposes alternatives but never silently changes a material research decision.
13. **Capabilities must be honest.** Chat mode creates artifacts and handoff instructions; agent mode may configure and verify external services only when the required tools and authorization exist.
14. **The web-native runtime comes first.** Vercel and Supabase are the primary execution path; native surveydown export is a first-class parallel output, not the greedyQ runtime.
15. **Advanced customization has an escape hatch.** Generate `app.R` and related native project files so researchers can continue directly in surveydown when unrestricted R, Shiny, or Quarto is required.
16. **Preregistration is a first-class output.** Generate a reviewable, versioned preregistration package from confirmed study and analysis decisions, and require explicit researcher approval before any registry submission or sample collection.

## 5. Compatibility strategy

| Layer | greedyQ policy |
| --- | --- |
| `survey.qmd` page and question syntax | Compatible wherever practical |
| Surveydown YAML settings | Compatible where documented and feasible |
| Existing `app.R` input | Never executed; recognized patterns may be migrated with diagnostics |
| Generated `app.R` output | First-class native surveydown export generated from the validated AST |
| Arbitrary R/Shiny reactive code | Unsupported |
| Question types | Implement surveydown's public question API first |
| Conditional logic | Native declarative DSL |
| Randomization | Native first-class feature |
| Database | Researcher-owned Supabase/PostgreSQL |
| Parser core | Platform-neutral TypeScript/JavaScript with no Node-specific dependency |
| Final-user runtime | Browser-native JavaScript; no local Python or Node.js requirement |
| Reference implementation | Dependency-light Python for semantic development and conformance |
| Secure persistence | Supabase/PostgreSQL RPC, transactions, and row-level security |
| Hosting | Vercel-first |

Every feature must be classified across both output paths:

- **Directly portable:** represented in compatible QMD and preserved in native surveydown output
- **Generated:** implemented natively by greedyQ and translated into generated `app.R` or supporting files
- **greedyQ-only:** available in the web-native runtime but exported with an explicit limitation or alternative
- **Unsupported:** rejected with a stable diagnostic rather than silently changed

The intended execution and export pipeline is:

```text
survey.qmd + greedyq.yml + design/*.csv + assets
                         |
                         v
              parser -> validated AST
                    /             \
                   v               v
       greedyQ web runtime    export generator
                   |               |
                   v               v
         Vercel + Supabase   survey.qmd + app.R
                                     |
                                     v
                           native surveydown project
```

## 6. Proposed technical model

```text
Versioned guide + natural-language study request
      |
      v
Guided interview + researcher approval checkpoints
      |
      v
survey.qmd
greedyq.yml
design/*.csv
assets/*
      |
      v
Browser-neutral JS parser + restricted sd_* parser
      |
      v
Internal Survey AST / JSON schema
      |
      +-- validator
      +-- logic engine
      +-- randomization engine
      +-- migration diagnostics
      +-- native surveydown export generator
      |
      v
Browser-native survey renderer
      |
      v
Vercel deployment
      |
      v
Researcher's Supabase/PostgreSQL
```

Development proceeds reference-first. The Python implementation is used to make grammar and semantic decisions explicit and testable. The final-user JavaScript implementation then reproduces those decisions in a platform-neutral core exposing string-to-data operations such as `parseSurvey(qmdText)`, `validateSurvey(ast)`, and `renderSurvey(ast)`. The core MUST NOT depend on a filesystem, Node.js APIs, or a build step. Browser and optional Node adapters may wrap it without changing its semantics.

Both implementations run the same conformance corpus. A JavaScript build is not conforming merely because it renders successfully: normalized ASTs, stable diagnostic codes, routing, stored values, conditional logic, and participant-visible behavior must match the reference contract.

The exact libraries, framework versions, schema layout, and supported function arguments remain specification-stage decisions.

## 7. Proposed project format

```text
my-survey/
├── survey.qmd
├── greedyq.yml
├── design/
│   └── choice_sets.csv
├── assets/
├── export/
│   └── surveydown/
│       ├── survey.qmd
│       ├── app.R
│       └── compatibility-report.json
└── supabase/
    └── migrations/
```

- `survey.qmd`: Pages, Markdown content, questions, and navigation
- `greedyq.yml`: Display rules, branching, validation, and randomization
- `design/*.csv`: Conjoint/CBC and repeated experimental designs
- `assets/`: Images and experimental stimuli
- `export/surveydown/`: Generated native surveydown project and compatibility report
- `supabase/`: Reproducible database migrations

## 8. Declarative logic

`greedyq.yml` expresses supported runtime behavior in a constrained language. The greedyQ runtime evaluates it directly; the native export generator translates supported behavior into `app.R` without executing arbitrary R during parsing, validation, preview, or deployment.

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

## 11. Primary experience and alternative authoring paths

### 11.1 Main feature: instantiating the greedyQ research agent

A versioned greedyQ repository supplies an agent-executable application specification. A capable general-purpose GenAI loads that specification and instantiates the greedyQ research agent. Different hosts may use different interfaces and native capabilities, but the resulting agent remains accountable to the same normative checkpoints, artifact contracts, and conformance tests.

```text
START-HERE.md + registry + resolved specification
                   |
                   v
         capable general-purpose GenAI
                   |
                   v
          greedyQ research agent
                   |
     +-------------+--------------+
     | research design            |
     | eligibility and consent    |
     | questions and measurement  |
     | logic and randomization    |
     | respondent source          |
     | data, privacy, deployment  |
     +-------------+--------------+
                   |
                   v
       researcher approval checkpoints
                   |
                   v
     survey.qmd + greedyq.yml + design/*.csv
                   |
                   v
 validate -> preregister -> preview -> approve -> deploy
```

The interview asks one focused question at a time, keeps a structured record of confirmed decisions, and updates artifacts at stable checkpoints. Before fielding, it generates a preregistration package covering hypotheses, design, sampling, exclusions, variables, and analysis. The LLM may detect methodological risks, explain them, and suggest alternatives using its own research knowledge, but it must not invent unresolved preregistration commitments. The guide does not attempt to maintain an encyclopedia of survey methodology. It defines the review workflow and requires researcher confirmation before material decisions change.

### 11.2 Chat mode and agent mode

The guide begins by detecting available capabilities.

- **Chat mode:** Conduct the interview, create all project artifacts, run guide-based self-checks, and provide precise validation/deployment handoff instructions.
- **Agent mode:** Additionally edit the repository, execute the validator, provision or connect Supabase and Vercel, configure environment variables, deploy, and verify the live survey when tools and authorization permit.

The workflow must never claim that a repository, database, deployment, or external panel was configured unless the operation was performed and verified.

### 11.3 Division of responsibility

| Actor | Responsibility |
| --- | --- |
| LLM | Research reasoning, question critique, design concerns, alternatives, natural-language collaboration |
| greedyQ guide | Interview sequence, required review moments, approval checkpoints, artifact and deployment workflow |
| greedyQ validator | IDs, references, reachability, cycles, configuration completeness, deterministic constraints |
| Researcher | Substantive research decisions and final approval |

### 11.4 Guide artifacts

```text
guides/greedyq-guide.md
guides/greedyq-guide-compact.md
examples/complete-study/
```

The full guide should define:

- Role, scope, and prohibited behavior
- Capability detection and mode selection
- Phased interview protocol
- One-question-at-a-time interaction
- Research-review and researcher-confirmation checkpoints
- Study-state and decision-log format
- QMD, YAML, logic, randomization, and CSV contracts
- IRB/ethics, consent, and respondent-source workflow
- Preregistration interview, template selection, artifact hashes, and pre-fielding approval gate
- Artifact creation and update rules
- Validation and LLM correction loop
- Preview and pre-deployment approval
- GitHub, Vercel, Supabase, and Prolific procedures
- Deployment verification and study handoff

### 11.5 Expert path: direct authoring

Experienced users may edit `survey.qmd`, `greedyq.yml`, and design files directly. Their artifacts enter the same validation, preview, approval, and deployment pipeline.

### 11.6 Import path: PPTX converter

The converter produces a high-quality, editable first draft rather than claiming perfect semantic recovery.

```text
survey.pptx
    |
    v
greedyq convert survey.pptx
    |
    +-- survey.qmd
    +-- greedyq.yml
    +-- assets/*
    +-- conversion-report.md
    |
    v
guided AI review -> validate -> preview -> deploy
```

It should use PPTX structure, layout, tables, speaker notes, and optional metadata to infer pages and questions while reporting ambiguous conversions.

## 12. Initial success criteria

The first end-to-end milestone succeeds when a researcher can:

1. Attach the guide, request a new survey, and complete a one-question-at-a-time interview.
2. Review and approve the recorded material research decisions.
3. Receive valid QMD, configuration, design, consent, and deployment artifacts.
4. Validate the study without installing R.
5. Review and approve a generated preregistration package before sample collection.
6. Preview and deploy the study through chat-mode handoff or agent-mode execution.
6. Enroll a respondent with persistent experimental assignment.
7. Save partial and completed responses to the researcher's Supabase.
8. Export analysis-ready data.
9. Reproduce the interview decisions and fielded study from a Git commit and recorded specification version.

## 13. Research governance and respondent sources

### 13.1 Ethics and IRB metadata

greedyQ should provide structured metadata and reusable presentation blocks for ethics-review information.

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

The v0.2 specification should define:

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

greedyQ should provide a provider-neutral integration contract plus named presets for common respondent platforms.

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

- Exact v0.2 surveydown compatibility boundary
- Parser implementation and grammar strategy
- Next.js and runtime architecture
- Supabase relational/JSONB schema boundaries
- Safe expression-language grammar
- Transaction model for balanced randomization
- Public naming and trademark review before broad release
- Minimum required ethics metadata and how it varies by study template
- Consent amendment, withdrawal, and response-retention semantics
- Prolific completion-status mapping and duplicate-participation defaults
