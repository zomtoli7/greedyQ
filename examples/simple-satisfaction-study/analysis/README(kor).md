# 분석 안내

[English](./README.md)

**Status:** 기준 분석 계획; 실행되지 않음

## 주요 요약

참여 자격이 있고 제출을 완료한 응답 수, `overall_satisfaction`의 전체 분포, 평균과 양측 95% confidence interval을 보고합니다. 모집 과정이 그 주장을 뒷받침하지 않으면 표본이 모든 연구자를 대표한다고 표현하지 않습니다.

## 추가 요약

- `experience_ratings`의 각 문항을 별도로 보고하며 추가 검증 없이 하나의 척도로 합치지 않습니다.
- `confidence`, `time_saved`, `completion_status`, `recommend_score`, `use_again`의 분포를 보고합니다.
- 기술적인 제품 추적을 위해 `recommend_score`에서 일반적인 Net Promoter Score 범주를 계산합니다. Detractor는 0–6, passive는 7–8, promoter는 9–10입니다. 점수와 각 범주의 수를 함께 보고합니다.
- `had_problem`과 `problem_area`를 요약합니다. 서술 응답은 실수로 포함된 식별정보나 기밀 내용을 제거한 뒤 검토합니다.
- 사용 횟수, 주 사용 목적, AI product, 완료 정도, guide 제공 방식에 따른 비교는 탐색적인 기술 결과로만 제시합니다. 집단 크기를 함께 보여주고 인과 표현을 사용하지 않습니다.

## 결측 응답과 제외

문항별 결측을 설명합니다. 주요 요약에는 참여 자격과 동의를 충족하고 완료 결과에 도달한 session을 포함합니다. 동의 거부, 선별 탈락, 철회, preview, test session은 제품 feedback 응답이 아닙니다. 부정적인 응답이라는 이유로 완료 응답을 제외하지 않습니다.
