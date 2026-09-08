# Golden Reference Preview Test Report

Korean copy: [preview-test-report(kor).md](preview-test-report(kor).md)

## Scope

This report covers the golden reference study preview model, the self-contained preview runtime, its generated HTML, and the AI-generation contracts that protect them. The preview is a researcher review artifact; it is not a production data-collection runtime.

## Automated result

- 87 repository tests, including 11 QMD-to-browser pipeline scenarios and 11 durable respondent-runtime scenarios, passed on 2026-09-08.
- The preview model and HTML were regenerated directly from `survey.qmd` and `greedyq.yml`; no separately hand-authored model was used.
- The canonical runtime JavaScript passed `node --check`.
- The preview model passed its JSON Schema.
- Every QMD page and question is represented in the preview model.
- Display labels and stored values match the QMD source exactly.
- Both experimental conditions and all five terminal outcomes have resolved paths.
- Consent refusal, minor screen-out, withdrawal, conditional deletion request, hidden-answer clearing, validation, and condition switching are covered.
- The generated preview embeds the canonical model byte-for-byte and its manifest hashes match.
- English/Korean Markdown pairing and repository whitespace checks passed.

## Defects found and corrected

1. Several support-scale labels in the preview model did not exactly match the QMD source. They now preserve the complete respondent-facing labels and stored values.
2. A conditional deletion-request field was omitted from the required-field parity assertion. It is now represented as conditionally required and tested against `greedyq.yml`.
3. Forced condition changes could retain answers collected after assignment. The runtime now clears those answers and records their IDs in a `condition_forced` audit event.
4. The former preview was too sparse for meaningful researcher review. It now includes respondent-grade controls, validation, progress, mobile behavior, a separate researcher panel, routing/state inspection, terminal outcomes, and a safe no-network execution boundary.

## Scenario coverage

The model tests exercise both control and treatment happy paths, refusal and screen-out routes, withdrawal with and without a deletion request, every terminal outcome, both states of conditional questions, required-field failures, numeric bounds, route resolution, progress paths, duplicate identifiers, and exact option mapping. Failure simulations cover malformed QMD calls, missing question IDs, missing route targets, reversed display/store mappings, unsafe raw HTML, and every supported preview input type.

The normative visual and interaction acceptance criteria are in [`docs/preview-ui-spec.md`](../../docs/preview-ui-spec.md). They include desktop, tablet, phone, keyboard, focus, validation, matrix overflow, 200% zoom, and researcher-control review cases.

## Remaining manual gate

The local in-app browser integration could not start because its Node runtime bridge returned an operating-system “No such file or directory” error. Therefore no claim is made that real-browser viewport, keyboard, or screen-reader review passed. `interactive_preview_reviewed` must remain incomplete until a human opens `preview.html`, runs the required scenario suite, and records evidence. Automated model, security, syntax, and contract checks passed independently of that limitation.
