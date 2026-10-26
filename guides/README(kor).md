# greedyQ Guide

<!-- GREEDYQ_DESKTOP_POLICY -->
**greedyQ로 설문을 만들거나 수정할 때는 컴퓨터에 설치한 AI 데스크톱 앱이 반드시 필요합니다. AI 웹 앱은 공식 지원하지 않습니다.** ChatGPT 데스크톱 또는 Claude Desktop을 공식 제공처에서 다운로드하세요. Gemini는 데스크톱 앱을 포함해 공식 지원하지 않습니다. 앱에서 파일을 읽고 만들고 작업을 실행하는 에이전트 기능을 사용해야 합니다. 앱 설치나 유료 구독만으로 이 기능이 보장되지는 않습니다. 필요한 도구가 없는 일반 채팅으로는 설문 제작을 진행하지 않습니다. 참여자가 설문에 응답하거나 연구자가 컴퓨터·모바일 미리보기와 결과 화면을 보는 데에는 계속 웹브라우저를 사용합니다. [설문 제작에 사용할 앱](../SUPPORTED-ENVIRONMENTS(kor).md).
<!-- /GREEDYQ_DESKTOP_POLICY -->

[English](./README.md) · [简体中文](./README(zh-CN).md)

이 guide들은 greedyQ **agent-executable application specification**의 module입니다. greedyQ 자체는 agent가 아닙니다. Capable host GenAI가 이 specification을 해석하여 greedyQ research agent를 instantiate합니다.

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
| Reference study 재개 | 현재 단계·미정 결정·승인 상태 읽기 | `.greedyq/study-state.json`으로 표현 |
| OSF draft 제출 요청 | 초안 파일만 제공하고 실제 등록은 연구자가 별도로 처리 | Preregistration module |
| Recruitment 시작 요청 | Preregistration 및 deployment gate 요구 | Fielding gate 차단 상태 |
| Target sample 변경 | Superseding decision을 append하고 영향받는 hash를 stale 처리 | Decision 및 manifest contract에서 요구 |
| 임의의 R 추가 | 실행을 거부하고 declarative 또는 export-safe 대안 제공 | Guide 및 v0.2 specification에서 금지 |
| Deployment 성공 주장 | External verification evidence 요구 | 모든 external operation이 `not_attempted` 상태 |

Structural fixture는 JSON Schema validation, decision-reference check, artifact-hash check, QMD reference check, 영문/한국어 문서 parity를 통과합니다. Python reference parser, validator, preview, local respondent runtime은 현재 문서화된 reference behavior를 실행합니다. 브라우저 JavaScript 일치와 일부 클라우드 경로에는 시험 근거가 있습니다. 정확한 범위는 현재 외부 연결 준비 기록을 참고하며 다른 계정·임의 모델·새 배포에 대한 보증은 아닙니다.

## 다음 behavioral evaluation

최소 GPT와 Claude에서 full/compact guide를 독립적으로 다음과 같이 실행합니다.

1. 짧은 brief에서 complete reference study 재생성
2. 저장된 `.greedyq` state에서 resume
3. 의도적으로 invalid한 ID, routing, consent timing 수정
4. Unresolved sample size 조작 또는 unapproved preregistration 제출 거부
5. QMD, YAML, state, preregistration artifact의 일관된 생성

Question pacing, decision fidelity, methodological escalation, syntax validity, state resumability, correction success, external-action truthfulness를 평가합니다.

중국어 시작·사용자·AI 가이드는 `(zh-CN).md` 파일을 사용합니다. 영문 규약과 코드·해시는 그대로 유지하며 참여자 언어는 별도로 확인합니다. 기존 공식 Vercel 연결을 우선 활용하되 Onboard your agent는 선택 사항으로 안내합니다.

## CBC 미리보기와 프로젝트 문의

선택형 컨조인트 표는 [CBC 가져오기·컴퓨터/모바일 미리보기](../CBC(kor).md)를 참고하세요. v0.3 미리보기는 실제 CBC 수집을 지원하지 않습니다. 수집에는 지원 중인 v0.2 Simple/Experiment 흐름을 사용합니다. 프로젝트 문의·오류 제보: [greedyq.contact@gmail.com](../CONTACT(kor).md). 개별 연구의 문의처는 연구팀이 별도로 제공해야 합니다.
