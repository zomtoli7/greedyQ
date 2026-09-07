# 완전한 기준 연구

[English](./README.md)

**Fixture 상태:** Pre-implementation golden reference
**스펙:** `0.1.0-draft.1`
**연구 ID:** `digital_service_info_001`

## 목적

이 가상의 최소 위험 연구는 가상 지방정부 디지털 지원 프로그램의 실용적 혜택을 제시하는 방식이 중립적인 사실 설명과 비교해 지지도를 변화시키는지 검증합니다. 실제 정책 증거를 만들기 위한 것이 아니라 greedyQ specification, AI guide, parser, validator, runtime, persistence model, native surveydown export를 검증하기 위한 예제입니다.

## 설계

- 모집단: Prolific-compatible flow로 모집한 동의한 성인
- 설계: Two-arm between-subject experiment
- Control: 중립적인 프로그램 설명
- Treatment: 동일한 핵심 사실을 포함하는 혜택 중심 프로그램 설명
- Primary outcome: 처치 후 프로그램 지지도, 1–7
- Secondary outcome: 인지된 유용성, 이해도, 자유응답 이유
- 배정: 4명 고정 block, 1:1 allocation, stimulus 표시 전 저장
- 분석 의도: 처치 후 평균 지지도 차이 및 사전 지정된 baseline-adjusted sensitivity analysis

## Coverage

이 fixture는 governance metadata, versioned consent, Prolific parameter, duplicate resume, screening, pre-treatment measurement, persistent randomization, conditional stimulus, manipulation check, attention check, conditional follow-up, privacy를 존중하는 demographic, partial save, withdrawal/deletion-request 기록, 구분된 terminal outcome, Supabase schema, Vercel configuration, native surveydown export expectation을 다룹니다.

## 파일

```text
survey.qmd                         study pages and questions
greedyq.yml                        behavior and integration contract
consent.md                         versioned participant information
design/stimuli.csv                 condition content and analysis labels
analysis/                          analysis intent and data dictionary
preregistration/                   OSF-oriented draft, structured data, and hash manifest
.greedyq/                          resumable state, decision history, and generation provenance
supabase/migrations/001_initial.sql  reference persistence schema
vercel.json                        deployment fixture
export/surveydown/                 expected native export fixture
```

## 안전 및 상태

모든 기관, 연락처, protocol ID, URL, completion code, 정책 내용은 가상의 placeholder입니다. 실제 모집 전에 반드시 교체하고 검토해야 합니다. 이 fixture는 실행·배포·IRB 승인되지 않았으며 작동하는 greedyQ 구현으로 검증되지 않았습니다.
