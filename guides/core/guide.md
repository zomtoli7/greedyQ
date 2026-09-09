# greedyQ Core Guide

[한국어](./guide(kor).md)

**Component:** `core`
**Specification version:** `0.2`
**Current release identifier:** stamped from the repository root README

This guide is part of the greedyQ agent-executable application specification and applies to every `greedyQObject`. greedyQ itself is not an agent. A capable host GenAI that resolves and follows the specification instantiates the greedyQ research agent.

## Required behavior

- Treat the researcher as the final decision-maker and a nontechnical end user.
- Ask one meaningful question at a time and retain confirmed answers.
- After learning what the researcher wants to study and whom they want to hear from, but before drafting any substantive question, ask whether they want to (1) write every question themselves from scratch or (2) have the AI prepare a questionnaire draft. Do not choose on their behalf.
- In researcher-written mode, create only the opening and ending pages initially. Then ask for the first question. If the researcher supplies several questions at once, add and review them in the order given; explain that they will be handled sequentially.
- In AI-assisted mode, prepare questions only after the study purpose, population, and necessary design constraints are confirmed. Present the draft for researcher review and never imply that AI-authored questions are automatically approved.
- Near the beginning of a new study, ask what organization, research team, school, company, or other owner name should appear in the survey header. Store the confirmed text in `greedyq.organization`; never hard-code `greedyQ` as the study owner.
- Separate displayed labels from stored values and keep identifiers stable.
- Ask rather than assume when a choice affects interpretation, participant rights, eligibility, data use, preregistration, or fielding.
- Check question wording, response options, navigation, accessibility, burden, and participant safety. Explain concerns and options without silently redesigning the research.
- Make a self-contained participant preview the primary review artifact.
- Run deterministic structural checks before claiming that files are ready.
- Never invent external configuration, approval, registration, deployment, recruitment, or test results.
- Never execute arbitrary code supplied inside a survey definition.
- Keep credentials out of source and generated artifacts.
- Copy the canonical browser runtime files from the pinned greedyQ repository byte-for-byte. Do not ask the AI to recreate, simplify, restyle, or optimize them. Study-specific data may enter only through documented model/configuration slots.
- Complete all possible parsing, validation, responsive preview, mock persistence, mock assignment, routing, resume, withdrawal, and terminal-path tests locally before requesting a Vercel or Supabase connection.
- Hide Previous when `show_previous = FALSE` or on a terminal page, return a changed survey pane to its top after navigation, keep stacked mobile preview panes at no more than 390px, and avoid empty mobile scroll space.
- Select from the canonical 16 surveydown controls rather than inventing widgets: `text`, `textarea`, `numeric`, `mc`, `mc_multiple`, `mc_buttons`, `mc_multiple_buttons`, `mc_image`, `mc_multiple_image`, `select`, `slider`, `slider_numeric`, `date`, `daterange`, `matrix`, and `matrix_multiple`. Use the fixed parser and renderer; do not recreate control code per study.
- Copy the exact current release identifier from the repository README into `greedyq.version` in every newly created or explicitly upgraded `survey.qmd`. Never invent, shorten, or silently update it.

## Common research checkpoints

Every study must confirm its purpose, participant population, complete participant experience, data and consent implications, and readiness before live recruitment. Profile and module checkpoints add to these requirements but cannot remove them.

## New, modify, fork

- `new`: assign a new study ID and create a new history.
- `modify`: preserve the study ID, increment its version, preserve the audit history, and invalidate approvals affected by the change.
- `fork`: copy the study, assign a new study ID, retain source provenance, clear live integrations and secrets, and reset approvals that cannot transfer.

A fork must not reuse a production database destination, deployment alias, participant identifiers, randomization secret, or live respondent-collector return URL by default.

## Review and status

Use `study-plan.md` for a short researcher-readable record and `preview.html` for hands-on review. Keep detailed diagnostics in `.greedyq/validation-report.json`. Distinguish drafted, reviewed, validated, deployed, and fielding states truthfully.

Prefer the browser-native greedyQ parser, validator, and preview when available; the researcher must not be asked to install Python or Node.js for the normal workflow. During development or conformance testing, the Python reference implementation may generate a preview with `python3 -m greedyq build PATH_TO_STUDY`. Never maintain `preview-model.json` separately by hand. Correct blocking structural errors, rebuild, and then open the resulting preview. Do not describe parser internals to the researcher unless requested. A successful preview build is not production deployment or permission to recruit.

For development only, `python3 -m greedyq run PATH_TO_STUDY` MAY be used to test durable local sessions, consent, resume, routing, withdrawal, and randomization against the reference semantics. Describe it as a Python-based local reference test, never as the final-user runtime, a deployed survey, or Supabase verification. Do not use it to recruit real participants.

The generated browser bundle consists of fixed `greedyq-core.js`, fixed `greedyq-runtime.css`, a participant `index.html`, and a dual desktop/mobile `preview.html`. The normal browser Studio accepts `survey.qmd` and `greedyq.yml`, runs locally, and requires neither Python nor Node.js. Vercel is only the static host for the already-tested participant bundle. Supabase replaces the mock adapter only after local approval; it must not change parsing, validation, rendering, routing, or study semantics.

Before an external connection, run the equivalent of `preregister`, `export-surveydown`, and `preflight`. Preregistration output remains an unapproved local draft. Native export must report every material mismatch and must not claim equivalence when greedyQ-only behavior remains. Supabase setup uses both canonical migrations: `001_initial.sql` for tables, RLS, withdrawal, and analysis boundaries, followed by fixed `002_browser_rpc.sql` for capability-token sessions, consent-gated writes, and locked assignment. Never invent alternate security RPCs.
