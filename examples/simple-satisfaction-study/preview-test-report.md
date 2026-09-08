# greedyQSimple Satisfaction Survey Test Report

[한국어](./preview-test-report(kor).md)

## Automated result

The study passed its dedicated survey tests as part of an 87-test repository suite, including 11 QMD-to-browser pipeline scenarios and 11 durable respondent-runtime scenarios, on 2026-09-08.

The preview is now regenerated directly from `survey.qmd` and `greedyq.yml`; `preview-model.json` is no longer a separately maintained source.

The automated checks cover:

- the `greedyQSimple` object and pinned modular guide resolution;
- all internal state schemas and artifact hashes;
- exact page and question parity between QMD and preview;
- exact displayed-label and stored-value mapping;
- the absence of randomization and experimental-condition routes;
- eligible completion, consent refusal, minor and nonuser screen-out, withdrawal, and technical-error outcomes;
- low-satisfaction, other-purpose, problem, and deletion-request follow-ups in both visible and hidden states;
- age and recommendation-score bounds;
- consent timing before product-feedback questions;
- the absence of participant redirects and direct-identifier questions;
- reproducible generation of the self-contained preview;
- descriptive, noncausal analysis language.

## Research-design choices

The survey accepts unsuccessful and incomplete greedyQ experiences rather than screening for successful users. It treats overall satisfaction as the primary descriptive result, measures concrete parts of the experience separately, and collects a conventional recommendation score without treating it as the only product outcome. Open-text prompts warn against entering credentials or private research information. No attention check is included because it would add burden to a short voluntary feedback survey without serving the reference study’s main purpose.

## Remaining manual gate

Automated checks do not replace hands-on review. Before any real use, a researcher must open `preview.html`, try every early exit and conditional path, review phone and desktop layouts, test keyboard use, and replace the fictional contacts. The study has not been institutionally reviewed, deployed, or opened for responses.
