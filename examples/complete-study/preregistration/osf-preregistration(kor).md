# OSF Preregistration 초안

[English](./osf-preregistration.md)

**상태:** Fixture draft이며 제출 또는 등록되지 않음
**Adapter:** `osf_preregistration`
**연구 버전:** `1.0.0-fixture`
**스펙:** `0.2.0-draft.1`

## 관리 정보

**제목:** 가상 지방정부 프로그램 지지도에 대한 디지털 서비스 정보 framing의 효과

**설명:** 동일한 운영 사실을 포함하는 중립적 설명과 비교하여 가상 지방정부 디지털 지원 프로그램의 혜택 중심 설명이 프로그램 지지도를 변화시키는지 검증하는 two-arm online experiment입니다.

**Contributor 및 소속:** 제출 전에 실제 contributor 및 affiliation metadata로 교체해야 합니다. Fixture의 연락처와 기관 identifier는 가상입니다.

**Registration 공개 설정:** 2027-09-07까지 embargo를 요청합니다. 이는 fixture 결정이며 제출할 때 연구자의 명시적 확인이 필요합니다.

## 연구 질문 및 hypothesis

연구 질문은 주민의 실용적 혜택을 강조하는 것이 제안 프로그램 지지도를 변화시키는지 여부입니다.

**H1:** 혜택 중심 treatment에 배정된 참여자는 중립 control에 배정된 참여자보다 평균 post-treatment support가 높을 것입니다.

Manipulation check는 treatment 참여자가 실용적 혜택을 더 강하게 강조했다고 인식하는지 검증합니다. Comprehension, usefulness, 자유응답은 secondary 또는 descriptive이며 추가 confirmatory hypothesis를 정의하지 않습니다.

## 설계 계획

연구는 동일 allocation의 two-arm between-subject design을 사용합니다. Control과 treatment 설명은 동일한 장소, 일정, 예산 사실을 포함하고 혜택 강조만 다릅니다. Assignment는 4명 randomized fixed block을 사용하며 stimulus 표시 전에 저장합니다. 참여자와 analysis dataset은 최초 assigned condition을 유지합니다.

Primary outcome은 1(strongly oppose)부터 7(strongly support)까지 측정하는 `support_post`입니다. `support_pre`는 assignment 전에 측정합니다. `frame_perception`은 manipulation check입니다. `attention_check`의 요청값은 5인 “Somewhat agree”입니다.

## 표본 계획

Prolific-compatible panel flow를 통해 동의한 성인을 모집합니다. 목표는 primary outcome이 기록된 400명이며 condition당 약 200명입니다. 400 primary-outcome completion, 500 consented eligible session, 또는 2026-12-31 23:59 UTC 중 가장 먼저 발생하는 시점에 모집을 중단합니다. 이 숫자는 가상의 fixture commitment이며 다른 연구를 위한 권고가 아닙니다.

400명 목표는 양측 5% test에서 약 0.28의 작은 표준화 집단 간 차이를 약 80% power로 검출하는 illustrative planning value입니다. 실제 연구는 자체 power analysis와 assumption을 재현하고 승인해야 합니다.

## 포함 및 제외 규칙

참여자는 유효한 panel identifier를 제공하고 동의하며 18–120세라고 응답해야 합니다. Consent refusal과 18세 미만은 별도 terminal outcome으로 이동합니다. Primary analysis에는 원래 assignment에 따라 `support_post`가 기록된 모든 eligible participant를 포함합니다.

Attention-check 또는 comprehension 실패로 primary intention-to-treat analysis에서 참여자를 제외하지 않습니다. Duplicate panel participation은 기존 session을 resume합니다. 기술적으로 중복된 record, 120세를 초과하는 불가능한 age, test session으로 입증된 record는 outcome analysis 전에 이유를 기록하고 제외합니다.

## Variable

- Treatment: `assignment_condition`, control versus treatment
- Primary outcome: `support_post`, integer 1–7
- Prespecified covariate: centered `support_pre`, integer 1–7
- Manipulation check: `frame_perception`, integer 1–7
- Quality measure: `comprehension`, `attention_check`
- Secondary outcome: `usefulness`
- Exploratory variable: `opposition_reason`, `comments`, demographic

전체 type과 label은 `../analysis/data-dictionary.csv`에 정의합니다.

## 분석 계획

Confirmatory analysis는 양측 95% confidence interval 및 양측 alpha 0.05와 함께 treatment와 control 간 평균 `support_post`의 보정하지 않은 차이를 추정합니다. 저장된 assignment에 따라 분석하며 effect estimate는 treatment minus control입니다.

사전 지정된 sensitivity analysis는 `support_post`를 dependent variable로, treatment와 centered `support_pre`를 predictor로 사용하는 OLS를 적합합니다. Manipulation-check, comprehension, attention-check 결과는 descriptive하게 보고합니다. Quality-check 실패를 제외하는 분석은 confirmatory가 아니라 sensitivity 또는 exploratory로 표시합니다.

Confirmatory analysis에서는 missing primary outcome을 impute하지 않습니다. Assigned condition별 missingness count와 rate를 보고합니다. 단일 H1 test만 confirmatory hypothesis이며 descriptive 또는 exploratory result에 대한 multiplicity adjustment는 계획하지 않습니다.

## 데이터, material, deviation

등록 package에는 정확한 `survey.qmd`, `greedyq.yml`, consent document, stimulus table, analysis note, data dictionary, artifact manifest가 포함되어야 합니다. Direct panel identifier는 analysis dataset과 분리합니다. IP address 및 browser fingerprint 수집은 기본적으로 비활성화합니다.

등록 후 대상 artifact를 변경하려면 추가 fielding 전에 문서화된 amendment 또는 새 registration version이 필요합니다. Deviation에는 변경 내용, 시점, 이유, data 확인 여부, confirmatory로 유지되는 analysis를 기록합니다.

## 승인 및 제출 상태

모든 fixture field는 해결됐지만 package는 연구자 승인을 받지 않았고 OSF로 전송되지 않았습니다. 이 파일 생성은 preregistration이 아닙니다. Fielding 전에 권한 있는 연구자가 contributor metadata, 기관 정보, sampling assumption, 날짜, embargo 선택, artifact hash, resulting registry status를 검증해야 합니다.
