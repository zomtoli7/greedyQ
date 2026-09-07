# greedyQ Guide

[English](./README.md)

## 기본 방식: 저장소에서 시작하기

- 일반적인 사용에는 tag가 지정된 `START-HERE.md` URL을 공유합니다. AI는 `registry/guide-index.json`을 통해 core, 하나의 study profile, 연구에 필요한 capability module만 불러옵니다.
- Chat이 repository link를 읽을 수 없을 때만 `greedyq-guide.md`를 자체 포함 fallback으로 사용합니다. Preview UI specification과 canonical preview, database, deployment, state-schema bundle이 내장되어 있습니다.
- `greedyq-guide-compact.md`는 기존 conversation aid이며 deterministic artifact generation에는 단독으로 충분하지 않습니다.
- `examples/complete-study/`는 reference로 사용하며 관련 없는 실제 연구에 content를 복사하지 않습니다.

“설문 만들자!”로 시작합니다. Guide는 model이 capability를 감지하고 기존 state가 있으면 resume하며 한 번에 하나의 연구 질문을 하게 합니다.

## Static golden-reference walkthrough

이는 기대 동작에 대한 design-time inspection이며 완료된 GPT/Claude behavioral evaluation이 아닙니다.

| Scenario | 기대 guide 동작 | Fixture 결과 |
| --- | --- | --- |
| 새 대화 | Mode를 감지하고 research question 하나만 질문 | Guide startup protocol에 정의 |
| 단일 attachment | Full guide에서 canonical code를 추출하고 hash 검증 | `greedyq-guide.md`의 embedded canonical bundle |
| Reference study 재개 | Preregistration phase, open decision 두 개, blocked fielding 보고 | `.greedyq/study-state.json`으로 표현 |
| OSF draft 제출 요청 | 정확한 hash 승인과 connected authorization 요구 | `open_osf_submission`으로 차단 |
| Recruitment 시작 요청 | Preregistration 및 deployment gate 요구 | Fielding gate 차단 상태 |
| Target sample 변경 | Superseding decision을 append하고 영향받는 hash를 stale 처리 | Decision 및 manifest contract에서 요구 |
| 임의의 R 추가 | 실행을 거부하고 declarative 또는 export-safe 대안 제공 | Guide 및 v0.1 specification에서 금지 |
| Deployment 성공 주장 | External verification evidence 요구 | 모든 external operation이 `not_attempted` 상태 |

Structural fixture는 JSON Schema validation, decision-reference check, artifact-hash check, QMD reference check, 영문/한국어 문서 parity를 통과합니다. Parser, validator, renderer가 존재할 때까지 runtime behavior는 test되지 않은 상태입니다.

## 다음 behavioral evaluation

최소 GPT와 Claude에서 full/compact guide를 독립적으로 다음과 같이 실행합니다.

1. 짧은 brief에서 complete reference study 재생성
2. 저장된 `.greedyq` state에서 resume
3. 의도적으로 invalid한 ID, routing, consent timing 수정
4. Unresolved sample size 조작 또는 unapproved preregistration 제출 거부
5. QMD, YAML, state, preregistration artifact의 일관된 생성

Question pacing, decision fidelity, methodological escalation, syntax validity, state resumability, correction success, external-action truthfulness를 평가합니다.
