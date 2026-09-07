# Analysis Notes

[한국어](./README(kor).md)

**Status:** Prespecified fixture intent; not an executed analysis

## Primary estimand

The primary estimand is the intention-to-treat difference in mean `support_post` between participants assigned to `treatment` and `control`.

## Primary analysis

Estimate an unadjusted difference in means with a two-sided 95% confidence interval. Analyze participants according to persisted assignment, regardless of manipulation-check or attention-check responses. Do not exclude participants based on a post-treatment measure in the primary analysis.

## Sensitivity analysis

Estimate an OLS model of `support_post` on the treatment indicator and centered `support_pre`. Report attention-check and comprehension performance descriptively, then provide clearly labeled sensitivity results using any prespecified quality exclusion.

## Missingness and multiplicity

Report outcome missingness by assigned condition. The reference study defines one primary outcome; secondary outcomes are exploratory and should be labeled accordingly.

## Export shape

The analysis export should contain one row per consented session and the variables in `data-dictionary.csv`. Array and matrix responses must remain machine-readable or be expanded with documented column names. Direct identifiers must be separated from the analysis table.
