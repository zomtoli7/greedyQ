# greedyQSimple Golden Reference: User Experience Survey

[한국어](./README(kor).md)

This fictional study is the canonical `greedyQSimple` example. It asks adults who have used greedyQ about satisfaction, usability, problems, and future use without random assignment or experimental conditions.

## What this fixture proves

- A repository-resolved `greedyQSimple` object can produce a complete study package.
- Consent refusal and eligibility screen-out occur before product-feedback questions.
- The survey uses single choice, select, numeric, slider, matrix, and free-text questions.
- Low satisfaction and reported problems trigger relevant follow-up questions.
- Hidden answers are cleared when their triggering response changes.
- Submission, withdrawal, deletion-request, and technical-error outcomes are distinct.
- The research plan is descriptive and does not overclaim representativeness or causality.
- Direct identifiers, credentials, and private research details are not requested.
- Deployment artifacts are present but no live setup or fielding is claimed.

## Files

```text
greedyq.study.json                   greedyQSimple object descriptor
survey.qmd                           participant pages and questions
greedyq.yml                          behavior, privacy, logic, and outcomes
study-plan.md                        short researcher-readable plan
consent.md                           versioned participant information
analysis/README.md                   descriptive analysis plan
analysis/data-dictionary.csv         variable definitions
preview-model.json                   validated preview model
preview.html                         generated self-contained preview
preview-test-report.md              automated coverage and remaining manual gate
.greedyq/guide-lock.json             pinned modular guide resolution
.greedyq/study-state.json            resumable workflow state
.greedyq/decision-log.json           confirmed research decisions
.greedyq/unresolved-decisions.json   blockers for real deployment
.greedyq/validation-report.json      detailed internal checks and manual gates
.greedyq/generation-manifest.json    artifact hashes and external-operation status
supabase/migrations/001_initial.sql  reference persistence schema
vercel.json                          deployment fixture
.env.example                         placeholder environment variables
```

## Status

This is a generated and structurally validated fixture. It has not received institutional review, completed hands-on accessibility review, been deployed, or collected responses. Replace every placeholder and obtain the appropriate approvals before adapting it for real fielding.
