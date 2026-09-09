# greedyQ v0.2 Specification

[한국어](./greedyq-v0.2-spec(kor).md)

**Status:** Draft normative specification
**Specification version:** `0.2.0-draft.1`
**Primary conformance fixtures:** `examples/complete-study/` and `examples/simple-satisfaction-study/`

## 1. Purpose and conformance language

This specification defines the smallest complete greedyQ study format, web-native runtime behavior, validation contract, and native surveydown export boundary. The words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY are normative.

greedyQ is a specification-driven, AI-native application for online academic research. The modular greedyQ bundle is an agent-executable application specification: combined with a capable general-purpose GenAI, it instantiates a greedyQ research agent that applies this normative format and produces research artifacts plus executable survey software. greedyQ itself is not an agent and MUST NOT be represented as one. Differences in host AI or interface MUST NOT weaken the conformance requirements in this document.

greedyQ is an independent implementation. It MUST NOT incorporate or execute surveydown source code. Compatibility targets publicly documented surveydown-style `survey.qmd` authoring conventions. The primary runtime is greedyQ on Vercel and Supabase; generated native surveydown files are a first-class parallel output.

An implementation conforms to v0.2 only when it can parse, validate, and deterministically normalize the complete reference study. Deployment and native export conformance are separate capabilities and MUST be reported separately.

## 2. Project contract

A study root MUST contain:

```text
survey.qmd
greedyq.yml
```

It MAY also contain:

```text
design/*.csv
assets/*
supabase/migrations/*.sql
vercel.json
preview.html
export/surveydown/*
```

`survey.qmd` is the source of truth for ordered pages, displayed content, questions, and navigation. `greedyq.yml` is the source of truth for study identity, governance metadata, consent, logic, randomization, persistence, respondent sources, outcomes, and export policy.

All normative artifacts MUST declare `spec_version: "0.2"`. Unknown keys MUST produce a warning by default and MAY be promoted to an error in strict mode.

## 3. Identifiers and references

IDs MUST match `^[a-z][a-z0-9_]{1,63}$`, be unique within their namespace, and remain stable after data collection begins. Page and question IDs share one namespace. Outcome, rule, randomization, and consent IDs use separate namespaces.

The following IDs are reserved for compatibility and MUST NOT be used as page or question IDs:

```text
session_id time_start time_end exit_survey_rating current_page browser ip_address
```

Every reference MUST resolve statically. Duplicate IDs, missing references, and references to a later unavailable value MUST be errors.

## 4. `survey.qmd` grammar

### 4.1 Front matter

The file MUST begin with YAML front matter containing `greedyq.spec_version` and `greedyq.version`. `greedyq.version` MUST equal the repository's current release identifier in `0.2_YYYY-MM-DD_<short-commit>` form. New studies SHOULD include `greedyq.organization`, the participant-visible study owner or research-team label, containing 1–120 characters. Legacy files without it render the neutral fallback “Research team.” v0.2 accepts the documented `theme-settings`, `survey-settings`, and `system-messages` namespaces. Unsupported Quarto execution options MUST be rejected.

```yaml
---
greedyq:
  spec_version: "0.2"
  version: "0.2_2026-09-09_40c5053"
  organization: "Example University Research Team"
survey-settings:
  show-previous: true
  required: [support_post]
---
```

Hyphens and underscores in recognized setting keys are equivalent after normalization. Boolean values normalize to true or false.

### 4.2 Pages

A page begins with `--- page_id` on its own line and ends at the next page marker or end of file. Content before the first page marker is invalid. Page order is source order unless an explicit forward target applies.

### 4.3 Markdown

v0.2 supports headings, paragraphs, emphasis, strong text, links, ordered and unordered lists, block quotes, thematic breaks, inline code, fenced non-executable code, and images with relative or HTTPS sources. Raw HTML and executable Quarto extensions are unsupported. Rendered output MUST be sanitized.

### 4.4 Questions

Questions are declared in non-executed R-style fenced chunks containing one allowlisted `sd_question()` call. The parser MUST parse the restricted expression and MUST NOT invoke R.

Required arguments are `id`, `type`, and `label`. v0.2 implements all 16 question controls documented by surveydown: `text`, `textarea`, `numeric`, `mc`, `mc_multiple`, `mc_buttons`, `mc_multiple_buttons`, `mc_image`, `mc_multiple_image`, `select`, `slider`, `slider_numeric`, `date`, `daterange`, `matrix`, and `matrix_multiple`.

Button controls support `direction`, `selected`, and `justified`. Image controls require one safe relative or HTTPS `image` source per option. `daterange` stores an ordered two-date array. `matrix_multiple` stores an array of selected values for each row. Native greedyQ persistence uses arrays and row objects; surveydown export converts these to its pipe-separated and wide-column representation where required.

`slider` uses a named option vector as an ordered labeled scale and stores the selected option value. `slider_numeric` uses numeric `min`, `max`, and optional positive `step` arguments. Both render as draggable, keyboard-operable native range controls. `orientation` may be `horizontal` (the portable default) or `vertical`; vertical orientation is a greedyQ extension and MUST be identified in native surveydown export diagnostics.

Allowed value forms are strings, numbers, booleans, null, `c(...)`, and named `c(label = value, ...)`. Arbitrary function calls, variable lookup, assignment, interpolation, and side effects are errors.

In every named option vector, the left-hand name is the respondent-facing display label and the right-hand value is the stored value. Generators MUST use the following direction and MUST NOT reverse it:

```r
option = c(
  "I agree to participate" = "agree",
  "I do not agree" = "decline"
)
```

The same rule applies to `option`, `options`, and matrix `row` vectors. Stored values are the only values used by logic, consent contracts, scoring, derivations, data dictionaries, and analysis plans. A validator MUST build a display-label/stored-value symbol table and MUST issue a blocking error when a referenced or documented stored value is absent. This cross-artifact check includes at least consent accept/refusal/withdrawal values, show/skip/validate expressions, attention-check answers, manipulation-check scoring, derived variables, and declared data-dictionary values.

### 4.5 Navigation

Pages receive an automatic Next action unless an `sd_nav()` call or terminal outcome is declared. v0.2 supports `show_previous`, `show_next`, `page_next`, `label_previous`, and `label_next`. Back navigation MUST preserve valid answers and MUST NOT change a persisted random assignment.

## 5. `greedyq.yml`

The root keys are:

```text
spec_version study governance consent respondents runtime persistence
logic randomization preregistration outcomes export
```

Unknown root keys are errors in strict mode. Secrets MUST NOT appear in this file.

Generators MUST use the canonical key names and shapes in `examples/complete-study/greedyq.yml`; they MUST NOT invent aliases or alternative object shapes. A declared alias is accepted only where this specification explicitly defines its normalization.

## 6. Expression language

Expressions are strings parsed by greedyQ. v0.2 permits literals, answer and stored-value identifiers, parentheses, `==`, `!=`, `<`, `<=`, `>`, `>=`, `and`, `or`, `not`, `in`, and the pure functions `answered(id)`, `length(value)`, and `contains(collection, value)`.

Evaluation MUST be deterministic and side-effect free. Missing values evaluate as null. Comparisons with null are false except `value == null`. Type-invalid expressions MUST fail validation rather than coerce silently.

## 7. Logic and lifecycle

`logic.show` controls visibility, `logic.skip` changes the forward destination, and `logic.validate` blocks leaving a page. Rules MUST have stable IDs and are evaluated in declaration order. Conflicting skip rules that can be true together are errors unless explicit priority is provided.

Hidden unanswered questions remain null. When a prior answer hides an answered question, the default policy is `clear_on_hide`; the clearing event MUST be recorded. Unreachable pages, cycles without an explicit bounded loop, and terminal pages with outgoing navigation are errors.

Lifecycle states are `created`, `consented`, `in_progress`, `completed`, `screened_out`, `consent_refused`, `withdrawn`, and `technical_error`. Only defined transitions are permitted and every terminal transition MUST be timestamped.

## 8. Governance and consent

Governance metadata records institutional context without claiming approval or compliance. It supports protocol title, institution, review status, protocol identifier, investigator contact, data contact, and jurisdiction notes.

The AI workflow MUST record `governance_timing` as `now` or `after_instrument_draft` after the initial topic, objective, and broad design are understood. Detailed governance collection MAY be deferred, but a minimal early triage MUST identify vulnerable populations, sensitive or directly identifying data, deception or incomplete disclosure, elevated-risk procedures, regulated interventions, and known institutional restrictions. A design-changing concern MUST be resolved or explicitly left blocking before instrument work continues.

Consent MUST be versioned and include an ID, version, effective date, document path, confirmation question, and refusal outcome. Consent acceptance MUST record the document version, a content hash, timestamp, and session ID before research responses are collected. Refusal MUST not create research-response rows beyond the minimum operational event record.

Consent amendments MUST require renewed confirmation. Withdrawal policy MUST state whether already collected responses are retained, anonymized, or deleted, subject to researcher configuration and applicable obligations; greedyQ MUST NOT claim that a configured policy is legally sufficient.

When detailed work is deferred, a draft preview MAY contain conspicuous placeholder governance and consent content. It MUST NOT present that content as reviewed or approved. Detailed governance, privacy, withdrawal, retention, and participant-facing consent MUST be confirmed after the coherent instrument draft and before interactive preview approval. Production deployment MUST remain blocked until that confirmation is recorded.

When deletion-on-withdrawal is selected, the runtime MUST perform the operation atomically and idempotently. It MUST lock the session, delete research answers, assignments, and external identifiers as configured, retain only the explicitly declared minimum operational record, append the terminal lifecycle event, and roll back the whole operation on failure. Generated Supabase projects MUST start from the reviewed canonical implementation in `examples/complete-study/supabase/migrations/001_initial.sql`; an agent MUST NOT replace it with an unreviewed approximation. Any study-specific deviation MUST be documented and researcher-approved.

## 9. Respondent sources and Prolific

The generic respondent contract defines allowlisted inbound parameters, validation, canonical identifiers, duplicate policy, and outcome redirects. Raw query parameters MUST NOT be stored unless explicitly allowlisted.

The Prolific preset recognizes `PROLIFIC_PID`, `STUDY_ID`, and `SESSION_ID`. A valid participant ID is required before consent for panel runs. Duplicate behavior MUST be one of `resume`, `reject`, or `allow`; v0.2 defaults to `resume`. Completion, screen-out, consent-refusal, and technical-error routes MUST be distinct and test mode MUST suppress production redirects.

## 10. Randomization

v0.2 supports simple and fixed-block between-subject assignment. A randomization declares an ID, unit, method, conditions, allocation, assignment point, persistence key, and stored metadata.

Assignment MUST occur only after consent and immediately before the first condition-dependent page. It MUST be atomic, persisted before stimulus display, invariant across refresh/resume, and never recomputed for the same persistence key. Stored metadata MUST include condition, method, seed or draw identifier, block identifier when applicable, assignment timestamp, and specification version.

## 11. Persistence and privacy

Supabase/PostgreSQL is the v0.2 live persistence target. The native schema separates sessions, consent events, answers, assignments, lifecycle events, and external identifiers. Server credentials MUST remain in deployment environment variables. Browser and IP collection are off by default.

Partial answers MUST be saved at successful page transitions. Resume MUST restore the latest committed page, valid answers, consent version, lifecycle state, and random assignment. Multiple-choice responses are stored as arrays, not pipe-delimited strings. Analysis export MAY produce a documented wide representation.

Row Level Security MUST prevent respondents from reading other respondents' data. Administrative analysis access MUST use a separate authenticated role.

RLS enablement, grants, and policies MUST be validated together: a grant without a matching policy is not usable access. The canonical migration MUST provide a restricted analyst policy or security-definer export boundary, exclude external identifiers, and expose completed non-test sessions and their answers in a documented export shape. Generated migrations MUST use the canonical migration as their base and may only extend it through documented, validated changes.

## 12. Validation and diagnostics

Diagnostics MUST include `code`, `severity`, `message`, `file`, `location`, and optional `related_ids` and `suggested_fix`. Stable v0.2 codes include:

| Code | Severity | Meaning |
| --- | --- | --- |
| `GQ001` | error | Invalid or duplicate identifier |
| `GQ002` | error | Unresolved reference |
| `GQ003` | error | Unsupported executable expression |
| `GQ004` | error | Unreachable page or invalid cycle |
| `GQ005` | error | Ambiguous navigation or skip logic |
| `GQ006` | error | Missing or invalid consent contract |
| `GQ007` | error | Randomization is not persistently defined |
| `GQ008` | error | Respondent-source contract is incomplete |
| `GQ009` | error | Secret or unsafe redirect detected |
| `GQ010` | error | Preregistration contains unresolved or inconsistent commitments |
| `GQ011` | error | Display-label/stored-value contract is inconsistent |
| `GQ012` | error | AI state artifact fails its published JSON Schema |
| `GQ013` | error | Generated persistence, withdrawal, RLS, or analysis-export contract is incomplete |
| `GQ110` | warning | Methodological concern awaits researcher review |
| `GQ101` | warning | Feature is greedyQ-only in native export |
| `GQ102` | warning | Native export changes storage representation |

Validation MUST be deterministic: identical bytes and validator version produce identical diagnostics and normalized AST.

Unknown front-matter keys in `greedyq`, `theme-settings`, `survey-settings`, and `system-messages` MUST produce an error in strict or generation mode. Implementations MUST publish the accepted-key allowlist, types, enum values, and canonical spelling. Similar-looking invented keys MUST NOT be silently normalized.

All `.greedyq/*.json` artifacts MUST validate against the exact published schemas in `schemas/ai/` before they are written to the generation manifest. Generators MUST read those schemas, MUST use canonical templates derived from them, MUST NOT invent fields or enum values, and MUST NOT report the `validated` checkpoint when any state artifact fails schema validation. When schema validation is unavailable, the artifact and checkpoint MUST be marked unvalidated rather than represented as successful.

Methodological concerns such as treatment confounding, contamination, construct validity, or questionable exclusions do not become hard syntax errors merely because the LLM detects them. The LLM MUST explain the concern and concrete options, record it as an unresolved decision, and obtain an explicit researcher decision at the applicable checkpoint. A validator MAY emit `GQ110`, but MUST NOT silently alter the design.

## 13. Preregistration output and fielding gate

Preregistration is a first-class generated output. `greedyq.yml` MUST identify a template adapter, output directory, registration status, and fielding gate. v0.2 supports `osf_preregistration` and `generic_markdown`; additional registry templates are adapters rather than changes to the study model.

The package MUST include a human-readable Markdown draft, a machine-readable JSON representation, and a SHA-256 artifact manifest covering the exact study, consent, stimuli, and analysis-plan versions being registered. It SHOULD include hypotheses, design, sampling plan, stopping rule, exclusions, conditions, randomization, variables, primary and secondary outcomes, analysis models, missing-data handling, and known deviations or unresolved decisions.

The LLM MUST ask the researcher about missing material commitments and MUST NOT invent them. Every unresolved item MUST remain visibly marked and MUST block `ready_for_submission`. Generation of a draft is not submission. Creating an external draft, submitting it, choosing public release or embargo, and starting sample collection are distinct actions. Each external mutation requires appropriate authorization, and submission plus public/embargo choice requires explicit researcher approval and verification of the resulting registry state.

Once the researcher approves a preregistration package, greedyQ MUST record an immutable local snapshot and block fielding when covered artifact hashes change. A change requires a documented amendment or a new preregistration version; greedyQ MUST NOT silently regenerate the approved record. Registry-specific behavior can change, so adapters MUST declare the external template/version they target and MUST not claim successful registration without verification.

## 14. Web-native runtime

The primary renderer is a browser-native JavaScript application deployable as static assets on Vercel. It consumes only validated AST data, renders sanitized content, provides client feedback plus authoritative Supabase/PostgreSQL validation and transactions, and does not require a local Python, Node.js, or framework runtime.

Instrument review MUST be preview-first rather than prose-first. A generator MUST produce a browser-testable preview after a coherent instrument exists and SHOULD open it directly when the host supports interactive artifacts or browser control. Otherwise it MUST provide a self-contained `preview.html`; `study.md` MAY accompany it but MUST NOT substitute for respondent-flow review.

The normative layout, question-state, validation, responsive, accessibility, researcher-control, safety, scenario-suite, and review-evidence requirements are defined in `docs/preview-ui-spec.md`. That document and the canonical runtime are embedded in the full AI guide and therefore apply when the guide is the only attachment.

The preview MUST use a fixed trusted runtime over the validated AST, MUST NOT execute survey-authored JavaScript, and MUST disable external writes and production redirects. It MUST exercise navigation, required checks, show/skip logic, stored values, assignment, back navigation, resume, and terminal outcomes. It SHOULD expose a researcher-only debug panel and deterministic condition/path selectors. Generation or automated opening alone does not constitute review: `interactive_preview_reviewed` requires explicit researcher confirmation after hands-on testing and is a gate for `deployment_candidate` unless preview inability is explicitly accepted and recorded.

Preview mode MUST use non-production outcome handling and visibly identify itself. Production deployment MUST fail closed when required environment variables, migrations, or redirect configuration are missing. A tool or AI MUST NOT report successful deployment without verifying the live endpoint and persistence health.

### Researcher results application

Every connected study produces a public respondent application and a separately protected researcher results application. Sessions store test status independently from respondent source. The results application defaults to production records, can deliberately switch to test records, summarizes drop-off, assignments, and answers, and exports only the current filter. Its database secret is server-only and the results deployment requires Vercel Authentication. See [RESULTS-DASHBOARD.md](../RESULTS-DASHBOARD.md).

## 15. Native surveydown export

The exporter consumes the same validated AST and produces a self-contained export directory containing at least `survey.qmd`, `app.R`, required question/design files, assets, and `compatibility-report.json`.

Every feature is classified as:

- `directly_portable`: emitted as compatible QMD without semantic change
- `generated`: translated into deterministic `app.R` or supporting files
- `greedyq_only`: omitted or approximated only with an explicit warning
- `unsupported`: export fails

Generated `app.R` MAY depend on the surveydown R package but MUST be authored from greedyQ templates and AST transforms, not copied from surveydown source. Export MUST never claim behavioral equivalence when the compatibility report contains a material mismatch.

## 16. Reference-study acceptance criteria

The complete reference study MUST demonstrate:

1. governance metadata and versioned consent;
2. Prolific parameter validation and duplicate resume;
3. pre-treatment measures;
4. persisted treatment/control assignment;
5. condition-specific stimulus display;
6. manipulation, attention, Likert, choice, numeric, and free-text questions;
7. conditional display and skip logic;
8. privacy-respecting demographics;
9. partial save, resume, withdrawal, and deletion-request recording;
10. distinct completion, screen-out, refusal, and error outcomes;
11. human-readable and machine-readable preregistration artifacts plus an artifact-hash manifest;
12. Supabase migration and Vercel configuration; and
13. native surveydown export expectations.

The Python reference implementation MAY establish expected grammar and runtime semantics during development, but it MUST NOT be presented as a final-user prerequisite. The production parser, validator, compiler, preview, and respondent renderer MUST execute in a modern browser without requiring a locally installed Python or Node.js runtime. Its platform-neutral core MUST accept text/data inputs and MUST NOT depend on filesystem or Node-specific APIs.

The browser implementation MUST be tested against the same independently authored conformance fixtures as the Python reference. Equivalent input MUST yield semantically equivalent normalized ASTs, stable diagnostics, routes, conditions, stored values, and participant-visible behavior. Implementation-language-specific metadata and serialization ordering MAY differ when they have no semantic effect. Production readiness MUST NOT be claimed until this cross-runtime conformance suite passes.

## 17. Deferred from v0.2

Deferred capabilities include arbitrary R/Shiny or JavaScript, raw HTML, custom Quarto extensions, image questions, date ranges, multiple-response matrices, arbitrary widgets, weighted or stratified allocation, factorial and conjoint execution, electronic signatures, and jurisdiction-specific compliance automation.

## 18. Versioning

Breaking grammar or semantic changes require a new specification version. A fielded study MUST pin the greedyQ specification, validator, runtime, schema migration, consent document, preregistration package, guide, and export-generator versions. Generated artifacts MUST include provenance sufficient to reproduce their source commit and configuration.
