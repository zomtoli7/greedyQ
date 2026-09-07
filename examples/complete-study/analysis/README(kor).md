# 분석 노트

[English](./README.md)

**상태:** 사전 지정된 fixture 의도이며 실행된 분석이 아님

## 주요 estimand

주요 estimand는 `treatment`와 `control`에 배정된 참여자의 평균 `support_post`에 대한 intention-to-treat difference입니다.

## 주요 분석

양측 95% confidence interval과 함께 보정하지 않은 평균 차이를 추정합니다. Manipulation-check 또는 attention-check 응답과 관계없이 저장된 assignment에 따라 참여자를 분석합니다. 주요 분석에서 post-treatment measure를 근거로 참여자를 제외하지 않습니다.

## Sensitivity analysis

Treatment indicator와 centered `support_pre`에 대한 `support_post` OLS model을 추정합니다. Attention-check와 comprehension 성과는 기술적으로 보고하고, 사전에 지정한 quality exclusion을 사용하는 결과는 명확히 sensitivity로 표시합니다.

## Missingness 및 multiplicity

Assigned condition별 outcome missingness를 보고합니다. 기준 연구는 하나의 primary outcome을 정의하며 secondary outcome은 exploratory로 표시해야 합니다.

## Export 형식

분석 export는 동의한 session당 한 row와 `data-dictionary.csv`의 variable을 포함해야 합니다. Array 및 matrix response는 machine-readable 형태를 유지하거나 문서화된 column name으로 펼쳐야 합니다. Direct identifier는 analysis table과 분리해야 합니다.
