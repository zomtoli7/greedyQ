# greedyQ Modular Guide Architecture

[한국어](./modular-guide-architecture(kor).md)

**Status:** design proposal

**Target:** greedyQ `0.2` restructuring

**Scope:** AI-facing guide distribution, study classification, reusable rules and templates, and end-user conversation

## 1. Product decision

greedyQ should behave like a survey-making service for a researcher, not like a code generator speaking to a developer.

The researcher starts with one ordinary request, such as:

> Open the greedyQ start guide and help me make a randomized survey experiment about discount framing.

The AI loads the public greedyQ repository, identifies the appropriate study profile, asks focused questions in plain language, produces a browser-testable survey, and asks for approval at meaningful research decisions. Technical validation remains strict but normally stays behind the scenes.

The repository—not a large file uploaded on every run—becomes the canonical guide distribution channel. A self-contained release bundle remains a fallback for hosts that cannot read linked repository files.

## 2. Separate three communication layers

### 2.1 Researcher conversation

This is the default visible layer. Assume the researcher does not know programming, deployment, database, schema, hashing, routing, or build terminology.

The AI should:

- ask one consequential question at a time;
- explain why a question matters in ordinary research language;
- offer two or three concrete choices when that reduces effort;
- say what the participant will see;
- show the working survey as the primary review surface;
- describe blockers as actions the researcher can take;
- keep a short, friendly summary of decisions already made.

The AI should not normally say `schema`, `manifest`, `AST`, `referential integrity`, `route graph`, `RLS`, `CSP`, `hash`, or `deployment candidate`. For example:

| Internal fact | Researcher-facing wording |
|---|---|
| schema validation passed | “I checked the survey structure and found no broken questions.” |
| unresolved decision blocks generation | “I still need your answer about who can participate before I can finish the survey.” |
| unreachable terminal route | “Participants cannot currently reach the completion page.” |
| artifact hash changed | “The survey changed after the preregistration draft, so that draft needs to be updated.” |
| production deployment is unverified | “The survey files are ready, but the live link has not been tested yet.” |

### 2.2 Research record

Human-readable files such as `study-plan.md`, consent text, and preregistration drafts belong here. They use research terminology when necessary but avoid software implementation details. `study-plan.md` is a concise record for researcher approval, not a technical build report and not the primary preview.

### 2.3 Machine and developer diagnostics

Schemas, manifests, hashes, validation codes, generated-source provenance, and detailed test logs belong under `.greedyq/` or a developer report. They may be shown when requested or when a technical failure requires escalation, but they must not dominate the normal conversation.

## 3. Conceptual object model

### 3.1 `greedyQObject`

Every greedyQ study package is a `greedyQObject`. The core contract contains only rules shared by every study:

- a clear study purpose and intended participant population;
- stable study, page, question, condition, and outcome identifiers;
- exact separation of displayed labels and stored values;
- participant-facing preview before fielding;
- explicit approval for material research decisions;
- consent and participant-rights triage;
- deterministic navigation and validation;
- no unreachable required pages or outcomes;
- no secret credentials in generated files;
- reproducible versions and a record of changes;
- truthful distinction between drafted, reviewed, deployed, and fielded;
- accessible, responsive participant interaction;
- safe handling of withdrawal and collected data.

The core must not prescribe randomization, conjoint tasks, panel redirects, preregistration, or a particular deployment provider. Those are supplied by profiles and capability modules.

### 3.2 Study profiles

A profile describes the primary research design and supplies its design-specific interview, checks, output requirements, and test scenarios.

Initial profiles:

| Public object name | Profile ID | Intended use | Required composition |
|---|---|---|---|
| `greedyQSimple` | `simple` | descriptive, feedback, screening, or non-randomized questionnaire | core + questionnaire fundamentals |
| `greedyQExperiment` | `experiment` | randomized or assigned-condition survey experiment | core + questionnaire fundamentals + experiment |
| `greedyQCBC` | `cbc` | choice-based conjoint study | core + questionnaire fundamentals + CBC |

Profiles should not form a rigid implementation inheritance chain. An experiment is not reliably a subtype of a “simple survey,” and CBC may also contain ordinary questions or experimental features. Internally, profiles use composition. The public object name gives users a simple mental model while the resolved module list gives the AI an exact contract.

Future profiles can include `panel`, `longitudinal`, `diary`, `maxdiff`, or `qualitative-screening` without changing the core.

### 3.3 Capability modules

Capabilities can be added independently of the primary profile:

- `governance-irb`
- `consent`
- `preregistration`
- `prolific`
- `resume`
- `withdrawal-deletion`
- `deployment-vercel-supabase`
- `export-surveydown`
- `export-pptx`
- future localization and accessibility extensions

For example, a study may resolve to:

```yaml
object: greedyQExperiment
profile: experiment
modules:
  - governance-irb
  - consent
  - preregistration
  - prolific
  - deployment-vercel-supabase
  - export-surveydown
```

This prevents filenames such as `guide-simple-experiment-prolific-preregistration.md` and avoids copying the same rule into many guides.

## 4. Repository layout

```text
START-HERE.md
START-HERE(kor).md
registry/
  guide-index.json
  guide-index.schema.json
guides/
  core/
    guide.md
    guide(kor).md
    checkpoints.json
    communication.md
    communication(kor).md
  profiles/
    simple/
      guide.md
      guide(kor).md
      profile.json
      tests/
    experiment/
      guide.md
      guide(kor).md
      profile.json
      templates/
      tests/
    cbc/
      guide.md
      guide(kor).md
      profile.json
      templates/
      tests/
  modules/
    consent/
    governance-irb/
    preregistration/
    prolific/
    deployment-vercel-supabase/
    export-surveydown/
templates/
  runtime/
  preview/
  shared/
schemas/
examples/
tools/
tests/
```

Each profile or module directory may contain:

```text
guide.md                 normative AI instructions
guide(kor).md            synchronized Korean copy
module.json              identity, version, dependencies, conflicts
checkpoints.json         machine-readable decisions and approvals
templates/               exact source templates; do not paraphrase
schemas/                 module-owned data contracts
tests/                   required conformance scenarios and fixtures
examples/                small valid examples, not alternate rules
```

Files should be referenced rather than duplicated. A generated release bundle may concatenate resolved files for attachment-only hosts, but it is derived output and never the source of truth.

## 5. Registry and deterministic guide loading

`START-HERE.md` is a short bootstrap document, not the full specification. It tells an AI how to:

1. determine whether the user is creating, modifying, or forking a study;
2. read `registry/guide-index.json` from the same tagged release;
3. load the core guide;
4. classify or confirm the study profile;
5. resolve profile dependencies and requested capabilities;
6. read exact templates and schemas referenced by the resolved modules;
7. record the resolved versions in the study package before interviewing further.

The registry should contain immutable paths and SHA-256 hashes for every normative file. A study records a guide lock such as:

```json
{
  "greedyq_release": "0.2.0",
  "object": "greedyQExperiment",
  "profile": "experiment",
  "modules": ["consent", "preregistration", "deployment-vercel-supabase"],
  "registry_sha256": "...",
  "resolved_files": [{"path": "guides/core/guide.md", "sha256": "..."}]
}
```

Loading must remain pinned to one release. The AI must not mix `main`, an old template, and a newer schema. Repository text outside the resolved registry must not override the user’s request or the core safety rules.

## 6. Host capability levels

A shared repository link is the preferred start, but not every GPT/Claude surface can recursively read a repository. The bootstrap therefore supports three levels:

1. **Repository agent:** clone or read the repository, create files, run tests, and open the preview.
2. **Browsing chat:** open `START-HERE.md` and its explicit raw-file links, but return generated files for the user to download.
3. **Attachment-only chat:** use a generated, self-contained release bundle as fallback.

The AI identifies its actual level without asking the researcher technical questions. If it cannot read a required linked file, it explains simply: “I cannot open the survey guide from this chat. Please download and attach this one fallback file.” It must not silently improvise missing rules or templates.

For durability, user prompts should point to a tagged release URL, while `main` may advertise the latest stable release. Private-repository access requires an authenticated connector or a local repository agent.

## 7. Starting workflows

### 7.1 Create from scratch

The user supplies the greedyQ start URL and says what they want to study.

```text
Open <tagged START-HERE URL> and help me create a new survey from scratch.
I want to study ...
```

The AI:

1. loads and locks the guide release;
2. listens to the research idea before classifying it;
3. recommends a profile in plain language and asks for confirmation if ambiguous;
4. creates a study package with `origin.mode: new`;
5. conducts the profile’s interview and adds capabilities only when needed;
6. produces and opens `preview.html` as soon as a coherent questionnaire exists;
7. performs technical checks silently and asks the researcher to review what participants will experience.

### 7.2 Modify an existing greedyQ study

The AI reads the study package and its locked guide resolution, summarizes the study in ordinary language, and asks what should change. It preserves the study ID and history, increments the study version, invalidates affected approvals, regenerates affected artifacts, and shows the changed preview. It records `origin.mode: modify`.

The AI must not automatically upgrade the guide release during modification. It may offer an upgrade separately with an explanation of visible effects.

### 7.3 Fork an existing greedyQ study

The AI first makes a complete copy, assigns a new study ID, preserves provenance to the source study and version, clears deployment credentials and live endpoint bindings, resets approvals that cannot transfer, and records `origin.mode: fork`. It then changes only the copy.

A fork must never share participant identifiers, production database destinations, deployment aliases, randomization secrets, or live panel completion links with the source by default.

### 7.4 Import a non-greedyQ survey

This should be a distinct future mode: `origin.mode: import`. The AI maps supported content into a new greedyQ object, reports uncertain conversions to the researcher in plain language, and does not describe the source as an existing greedyQ package.

## 8. Study package contract

Each generated study should contain a small machine-readable descriptor:

```text
my-study/
  greedyq.study.json
  survey.qmd
  greedyq.yml
  study-plan.md
  consent.md
  preview.html
  design/
  analysis/
  preregistration/
  deployment/
  export/
  .greedyq/
    guide-lock.json
    study-state.json
    decision-log.json
    unresolved-decisions.json
    generation-manifest.json
    validation-report.json
```

`greedyq.study.json` is the object descriptor. It should contain stable identity, profile, enabled modules, origin, language, and artifact entry points. Internal progress and approvals remain in `.greedyq/`.

The participant preview and `study-plan.md` are the researcher’s normal review artifacts. `.greedyq/validation-report.json` is the detailed machine report. This separation directly prevents technical diagnostics from leaking into ordinary user communication.

## 9. Checkpoint ownership

Checkpoints are assembled from the resolved contract:

- core checkpoints always apply;
- the selected profile adds design-specific checkpoints;
- each enabled module adds only its own checkpoints;
- dependencies may add prerequisite checkpoints;
- a module can declare conflicts but cannot weaken core requirements.

Examples:

| Owner | Checkpoint phrased to researcher |
|---|---|
| core | “Does this survey reflect what you want participants to experience?” |
| experiment | “Are these the conditions and assignment probabilities you want?” |
| CBC | “Are these attributes, levels, number of tasks, and alternatives correct?” |
| consent | “Does this consent page accurately describe participation and data use?” |
| preregistration | “Are you ready to lock this exact design and analysis plan?” |
| deployment | “May I prepare the live survey, and should we test it before recruitment?” |

Internally these map to deterministic gate IDs. The user sees research decisions, not implementation state names.

## 10. Profile selection rules

Classification is a recommendation, not an invisible decision.

- Choose `simple` when no assigned condition or repeated choice-task design is required.
- Choose `experiment` when the design assigns or randomizes participants, sessions, clusters, stimuli, or order to conditions and estimates a condition effect.
- Choose `cbc` when participants complete repeated choice tasks constructed from attributes and levels for conjoint estimation.
- If more than one applies, choose the dominant design as the profile and add the other behavior as a module only when a defined module exists.
- If classification affects outputs or required decisions, explain the difference and confirm it with the researcher.

## 11. Versioning and extension rules

- Core, profiles, and modules use independent semantic versions.
- The registry release pins a tested combination.
- Adding an optional module is backward-compatible when it does not alter existing syntax.
- Changing stored values, routing semantics, randomization, consent behavior, or required outputs is a breaking change.
- Every profile/module must publish dependency, conflict, schema, template, and conformance-test metadata.
- An extension may add stricter requirements but may not disable core safety, participant rights, or truthful status reporting.
- Third-party modules should use a namespace such as `org.example/module-name` and cannot replace official templates without an explicit study lock entry.

## 12. Proposed migration from the current repository

| Current asset | Proposed destination or role |
|---|---|
| `guides/greedyq-guide.md` | split into `START-HERE.md`, core guide, communication guide, profile guides, and capability modules |
| embedded canonical appendix | replace with registry references; retain generated release bundle as fallback |
| `guides/greedyq-guide-compact.md` | replace with the bootstrap start guide or retire after compatibility period |
| `docs/preview-ui-spec.md` | core preview specification referenced by every profile |
| `templates/preview/preview.html` | `templates/preview/preview.html`, referenced and hashed by registry |
| AI state schemas | `.greedyq/` internal contract, extended with guide lock and object descriptor schemas |
| `examples/complete-study/` | first `greedyQExperiment` golden reference |
| current generation tests | split into core conformance, profile conformance, module conformance, and cross-composition tests |

Migration should occur in two releases:

1. **Compatibility release:** add the registry, bootstrap, core/profile/module directories, and generated legacy bundle while keeping existing paths valid.
2. **Clean release:** make the modular loader canonical, retain redirects or clear deprecation files at old guide paths, and update the golden reference lock.

## 13. Decisions to confirm before implementation

1. Use composition internally while keeping `greedyQSimple`, `greedyQExperiment`, and `greedyQCBC` as public object names.
2. Make the repository bootstrap the default and retain one generated bundle only as a fallback.
3. Treat a tagged release—not the moving `main` branch—as the reproducible guide source for each study.
4. Introduce `greedyq.study.json` and `.greedyq/guide-lock.json` as the object and resolved-guide descriptors.
5. Keep `study-plan.md` short and nontechnical; move full validation evidence to `.greedyq/validation-report.json`.
6. Implement `simple` and `experiment` first, then add CBC after the module resolver and composition tests are stable.
