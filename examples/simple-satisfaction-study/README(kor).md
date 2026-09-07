# greedyQSimple 골든 레퍼런스: 사용자 경험 설문

[English](./README.md)

이 가상 연구는 기준 `greedyQSimple` 예제입니다. 무작위 배정이나 실험 조건 없이 greedyQ를 사용한 성인에게 만족도, 사용성, 문제, 향후 사용 의향을 묻습니다.

## 이 fixture가 검증하는 것

- Repository에서 해석된 `greedyQSimple` object가 완전한 연구 package를 생성합니다.
- Consent 거부와 eligibility screen-out이 제품 feedback 문항보다 먼저 이루어집니다.
- Single choice, select, numeric, slider, matrix, free-text 문항을 사용합니다.
- 낮은 만족도와 문제 경험에 따라 관련 후속 문항을 표시합니다.
- Triggering response가 바뀌면 숨겨진 응답을 삭제합니다.
- 제출, 철회, 삭제 요청, 기술 오류 결과를 구분합니다.
- 분석 계획은 기술적 분석이며 대표성이나 인과관계를 과장하지 않습니다.
- 직접 identifier, credential, 비공개 연구 내용을 요구하지 않습니다.
- Deployment artifact는 있지만 실제 설정이나 fielding을 했다고 주장하지 않습니다.

## 파일

```text
greedyq.study.json                   greedyQSimple object descriptor
survey.qmd                           participant pages and questions
greedyq.yml                          behavior, privacy, logic, and outcomes
study-plan(kor).md                   짧고 연구자가 읽기 쉬운 계획
consent(kor).md                      versioned participant information
analysis/README(kor).md              descriptive analysis plan
analysis/data-dictionary.csv         variable definitions
preview-model.json                   validated preview model
preview.html                         generated self-contained preview
preview-test-report(kor).md          자동 검사 범위와 남은 수동 승인 단계
.greedyq/guide-lock.json             pinned modular guide resolution
.greedyq/study-state.json            resumable workflow state
.greedyq/decision-log.json           confirmed research decisions
.greedyq/unresolved-decisions.json   실제 배포를 막는 미결정 사항
.greedyq/validation-report.json      상세 내부 검사 및 manual gate
.greedyq/generation-manifest.json    artifact hash와 external-operation 상태
supabase/migrations/001_initial.sql  reference persistence schema
vercel.json                          deployment fixture
.env.example                         placeholder environment variables
```

## 상태

생성 및 구조 검증을 마친 fixture입니다. 실제 기관 검토, 직접 조작하는 접근성 검토, 배포, 응답 수집은 수행하지 않았습니다. 실제 조사에 맞게 바꾸기 전에 모든 placeholder를 교체하고 필요한 승인을 받아야 합니다.
