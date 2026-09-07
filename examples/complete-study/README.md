# Complete Reference Study

[한국어](./README(kor).md)

**Fixture status:** Pre-implementation golden reference
**Specification:** `0.2.0-draft.1`
**Study ID:** `digital_service_info_001`

## Purpose

This fictional, minimal-risk study tests whether presenting the practical benefits of a hypothetical municipal digital-assistance program changes support compared with a neutral factual description. It exists to exercise the greedyQ specification, AI guide, parser, validator, runtime, persistence model, and native surveydown export—not to produce real policy evidence.

## Design

- Population: consenting adults recruited through a Prolific-compatible flow
- Design: two-arm between-subject experiment
- Control: neutral program description
- Treatment: benefit-framed program description containing the same core facts
- Primary outcome: post-treatment program support, 1–7
- Secondary outcomes: perceived usefulness, comprehension, and open-ended reasoning
- Assignment: fixed blocks of four, 1:1 allocation, persisted before stimulus display
- Analysis intent: difference in mean post-treatment support with a prespecified baseline-adjusted sensitivity analysis

## Coverage

The fixture covers governance metadata, versioned consent, Prolific parameters, duplicate resume, screening, pre-treatment measurement, persistent randomization, conditional stimuli, a manipulation check, an attention check, conditional follow-up, privacy-respecting demographics, partial save, distinct terminal outcomes, schema-valid AI state, atomic deletion-on-withdrawal, paired RLS policies and grants, an identifier-free analysis export, Vercel configuration, and native surveydown export expectations.

Its QMD demonstrates the normative named-vector direction: `"Displayed label" = "stored_value"`. The Supabase migration is the canonical generation base for v0.2; generated studies extend it rather than improvising deletion or access-control code.

## Files

```text
survey.qmd                         study pages and questions
greedyq.study.json                 greedyQExperiment object descriptor
greedyq.yml                        behavior and integration contract
study-plan.md                      short nontechnical researcher record
consent.md                         versioned participant information
design/stimuli.csv                 condition content and analysis labels
analysis/                          analysis intent and data dictionary
preregistration/                   OSF-oriented draft, structured data, and hash manifest
.greedyq/                          guide lock, resumable state, decisions, validation, and provenance
supabase/migrations/001_initial.sql  reference persistence schema
vercel.json                        deployment fixture
preview-model.json                 validated preview-only study model
preview.html                       generated self-contained interactive preview
preview-test-report.md             automated coverage, fixes, and remaining manual gate
export/surveydown/                 expected native export fixture
```

## Safety and status

All institutions, contacts, protocol IDs, URLs, completion codes, and policy content are fictional placeholders. They MUST be replaced and reviewed before any real recruitment. This fixture has not been executed, deployed, IRB-approved, or validated by a working greedyQ implementation.
