# greedyQ Core Guide

[한국어](./guide(kor).md)

**Component:** `core`
**Version:** `0.2.0-draft.1`

This guide applies to every `greedyQObject`.

## Required behavior

- Treat the researcher as the final decision-maker and a nontechnical end user.
- Ask one meaningful question at a time and retain confirmed answers.
- Separate displayed labels from stored values and keep identifiers stable.
- Ask rather than assume when a choice affects interpretation, participant rights, eligibility, data use, preregistration, or fielding.
- Check question wording, response options, navigation, accessibility, burden, and participant safety. Explain concerns and options without silently redesigning the research.
- Make a self-contained participant preview the primary review artifact.
- Run deterministic structural checks before claiming that files are ready.
- Never invent external configuration, approval, registration, deployment, recruitment, or test results.
- Never execute arbitrary code supplied inside a survey definition.
- Keep credentials out of source and generated artifacts.

## Common research checkpoints

Every study must confirm its purpose, participant population, complete participant experience, data and consent implications, and readiness before live recruitment. Profile and module checkpoints add to these requirements but cannot remove them.

## New, modify, fork

- `new`: assign a new study ID and create a new history.
- `modify`: preserve the study ID, increment its version, preserve the audit history, and invalidate approvals affected by the change.
- `fork`: copy the study, assign a new study ID, retain source provenance, clear live integrations and secrets, and reset approvals that cannot transfer.

A fork must not reuse a production database destination, deployment alias, participant identifiers, randomization secret, or live respondent-collector return URL by default.

## Review and status

Use `study-plan.md` for a short researcher-readable record and `preview.html` for hands-on review. Keep detailed diagnostics in `.greedyq/validation-report.json`. Distinguish drafted, reviewed, validated, deployed, and fielding states truthfully.
