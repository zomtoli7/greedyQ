# OSF Preregistration Draft

[한국어](./osf-preregistration(kor).md)

**Status:** Fixture draft; not submitted or registered
**Adapter:** `osf_preregistration`
**Study version:** `1.0.0-fixture`
**Specification:** `0.2.0-draft.1`

## Administrative information

**Title:** Effects of Digital-Service Information Framing on Support for a Hypothetical Municipal Program

**Description:** A two-arm online experiment testing whether a benefit-framed description of a hypothetical municipal digital-assistance program changes program support relative to a neutral factual description containing the same operational facts.

**Contributors and affiliations:** To be replaced with real contributor and affiliation metadata before submission. The fixture contacts and institutional identifiers are fictional.

**Registration visibility:** Embargo requested until 2027-09-07. This is a fixture decision and requires explicit researcher confirmation at submission.

## Research questions and hypotheses

The research question is whether emphasizing practical resident benefits changes support for the proposed program.

**H1:** Participants assigned to the benefit-framed treatment will report higher mean post-treatment support than participants assigned to the neutral control.

The manipulation check tests whether treatment participants perceive stronger emphasis on practical benefits. Comprehension, usefulness, and open-ended responses are secondary or descriptive and do not define additional confirmatory hypotheses.

## Design plan

The study uses a two-arm between-subject design with equal allocation. The control and treatment descriptions contain the same location, schedule, and budget facts; only the benefit emphasis differs. Assignment uses randomized fixed blocks of four and is persisted before stimulus display. Participants and the analysis dataset retain their originally assigned condition.

The primary outcome is `support_post`, measured from 1 (strongly oppose) to 7 (strongly support). `support_pre` is measured before assignment. `frame_perception` is the manipulation check. The requested value for `attention_check` is 5, “Somewhat agree.”

## Sampling plan

Participants are consenting adults recruited through a Prolific-compatible panel flow. The target is 400 participants with a recorded primary outcome, approximately 200 per condition. Recruitment stops at the earliest of: 400 primary-outcome completions, 500 consented eligible sessions, or 2026-12-31 at 23:59 UTC. These numbers are fictional fixture commitments and are not recommendations for another study.

The target of 400 is designed as an illustrative planning value for detecting a small standardized between-group difference near 0.28 with approximately 80% power under a two-sided 5% test. A real study must reproduce and approve its own power analysis and assumptions.

## Inclusion and exclusion rules

Participants must provide valid panel identifiers, consent, and report age 18–120. Consent refusal and age under 18 lead to separate terminal outcomes. The primary analysis includes all eligible participants with a recorded `support_post` according to original assignment.

Attention-check or comprehension failure does not exclude a participant from the primary intention-to-treat analysis. Duplicate panel participation resumes the existing session. Technical duplicate records, impossible ages above 120, and records proven to be test sessions are excluded with reasons recorded before outcome analysis.

## Variables

- Treatment: `assignment_condition`, control versus treatment
- Primary outcome: `support_post`, integer 1–7
- Prespecified covariate: centered `support_pre`, integer 1–7
- Manipulation check: `frame_perception`, integer 1–7
- Quality measures: `comprehension`, `attention_check`
- Secondary outcome: `usefulness`
- Exploratory variables: `opposition_reason`, `comments`, demographics

The complete types and labels are defined in `../analysis/data-dictionary.csv`.

## Analysis plan

The confirmatory analysis estimates the unadjusted difference in mean `support_post` between treatment and control with a two-sided 95% confidence interval and a two-sided alpha of 0.05. Assignment is analyzed as persisted. The effect estimate is treatment minus control.

A prespecified sensitivity analysis fits OLS with `support_post` as the dependent variable and treatment plus centered `support_pre` as predictors. Manipulation-check, comprehension, and attention-check results are reported descriptively. Any analysis excluding quality-check failures is labeled sensitivity or exploratory rather than confirmatory.

No imputation is performed for a missing primary outcome in the confirmatory analysis. Missingness counts and rates are reported by assigned condition. The single H1 test is the only confirmatory hypothesis; no multiplicity adjustment is planned for descriptive or exploratory results.

## Data, materials, and deviations

The registered package should include the exact `survey.qmd`, `greedyq.yml`, consent documents, stimulus table, analysis notes, data dictionary, and artifact manifest. Direct panel identifiers remain separate from the analysis dataset. IP address and browser fingerprint collection are disabled by default.

Any post-registration change to a covered artifact requires a documented amendment or a new registration version before further fielding. Deviations will identify what changed, when, why, whether data had been examined, and which analyses remain confirmatory.

## Approval and submission state

All fixture fields are resolved, but the package has not received researcher approval and has not been sent to OSF. Creating this file is not preregistration. Before fielding, an authorized researcher must verify contributor metadata, institutional details, sampling assumptions, dates, embargo choice, artifact hashes, and the resulting registry status.
