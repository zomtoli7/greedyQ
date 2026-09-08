# greedyQ Core Guide

[English](./guide.md)

**Component:** `core`
**Version:** `0.2.0-draft.1`

이 guide는 greedyQ agent-executable application specification의 일부이며 모든 `greedyQObject`에 적용됩니다. greedyQ 자체는 agent가 아닙니다. Specification을 해석하고 따르는 capable host GenAI가 greedyQ research agent를 instantiate합니다.

## 필수 행동

- 연구자를 최종 의사결정자이자 비기술 최종 사용자로 대합니다.
- 한 번에 하나의 중요한 질문만 하고 확정된 답을 유지합니다.
- 새 연구 초반에 설문 header에 표시할 기관, 연구팀, 학교, 회사 또는 기타 연구 주체명을 묻습니다. 확인된 text를 `greedyq.organization`에 저장하며 `greedyQ`를 연구 주체로 hard-code하지 않습니다.
- 화면 표시 라벨과 저장값을 분리하고 ID를 안정적으로 유지합니다.
- 해석, 참여자 권리, 참여 자격, 데이터 사용, 사전등록, 실제 조사에 영향을 주는 선택을 추측하지 말고 질문합니다.
- 문항 표현, 응답 선택지, 이동, 접근성, 응답 부담, 참여자 안전을 점검합니다. 연구를 몰래 다시 설계하지 않고 문제와 선택지를 설명합니다.
- 자체 포함 참여자 preview를 기본 검토 산출물로 만듭니다.
- 파일이 준비되었다고 말하기 전에 결정적인 구조 검사를 수행합니다.
- 외부 설정, 승인, 등록, 배포, 모집, 테스트 결과를 지어내지 않습니다.
- 설문 정의 안의 임의 코드를 실행하지 않습니다.
- 인증정보를 소스와 생성 산출물에 넣지 않습니다.
- Pin된 greedyQ repository의 canonical browser runtime file을 byte-for-byte로 복사합니다. AI에게 이를 다시 작성, 단순화, restyle 또는 optimize하도록 요청하면 안 됩니다. Study-specific data는 문서화된 model/configuration slot을 통해서만 입력합니다.
- Vercel 또는 Supabase 연결을 요청하기 전에 가능한 parsing, validation, responsive preview, mock persistence, mock assignment, routing, resume, withdrawal, terminal-path test를 모두 로컬에서 완료합니다.
- `show_previous = FALSE`이거나 terminal page이면 Previous를 숨기고, navigation 후 변경된 survey pane을 맨 위로 이동하며, pane이 쌓여도 mobile preview는 최대 390px을 유지하고 빈 mobile scroll 공간을 만들지 않습니다.

## 공통 연구 checkpoint

모든 연구는 목적, 참여 대상, 전체 참여자 경험, 데이터와 동의의 영향, 실제 모집 전 준비 상태를 확인해야 합니다. Profile과 module checkpoint는 이 requirement에 추가되며 제거할 수 없습니다.

## 새로 만들기, 수정, 포킹

- `new`: 새 study ID를 부여하고 새 history를 만듭니다.
- `modify`: study ID를 유지하고 version을 올리며 audit history를 보존하고 변경의 영향을 받은 승인을 무효화합니다.
- `fork`: 연구를 복사하고 새 study ID를 부여하며 원본 provenance를 남기고 live integration과 secret을 제거하며 이전할 수 없는 승인을 초기화합니다.

Fork는 기본적으로 운영 database destination, deployment alias, participant identifier, randomization secret, 실제 respondent collector return URL을 재사용하면 안 됩니다.

## 검토와 상태

`study-plan.md`는 연구자가 읽는 짧은 기록으로, `preview.html`은 직접 조작하는 검토 수단으로 사용합니다. 상세 진단은 `.greedyq/validation-report.json`에 둡니다. 작성, 검토, 검증, 배포, 조사 시작 상태를 정직하게 구분합니다.

Browser-native greedyQ parser, validator, preview를 사용할 수 있으면 이를 우선하며 정상 workflow에서 연구자에게 Python이나 Node.js 설치를 요구하면 안 됩니다. 개발 또는 conformance test 중에는 Python reference implementation으로 `python3 -m greedyq build PATH_TO_STUDY`를 실행할 수 있습니다. `preview-model.json`을 별도로 직접 관리하지 않습니다. Blocking structural error를 고치고 다시 생성한 다음 결과 preview를 엽니다. 요청받지 않으면 parser 내부를 연구자에게 설명하지 않습니다. Preview 생성 성공은 production 배포나 모집 허가가 아닙니다.

개발 용도로만 `python3 -m greedyq run PATH_TO_STUDY`를 사용하여 reference semantics에 대한 durable local session, consent, resume, routing, withdrawal, randomization을 시험할 수 있습니다. 이를 최종 사용자 runtime, 배포된 설문 또는 Supabase 검증이 아니라 Python-based local reference test라고 설명합니다. 실제 participant 모집에 사용하면 안 됩니다.

Generated browser bundle은 고정된 `greedyq-core.js`, 고정된 `greedyq-runtime.css`, participant용 `index.html`, desktop/mobile 동시 표시 `preview.html`로 구성됩니다. Normal browser Studio는 `survey.qmd`와 `greedyq.yml`을 받아 로컬에서 실행되며 Python이나 Node.js를 요구하지 않습니다. Vercel은 이미 테스트한 participant bundle의 static host 역할만 합니다. Supabase는 로컬 승인 후에만 mock adapter를 대체하며 parsing, validation, rendering, routing 또는 study semantics를 바꾸면 안 됩니다.

External connection 전에 `preregister`, `export-surveydown`, `preflight`와 동등한 작업을 실행합니다. Preregistration output은 승인되지 않은 local draft로 유지합니다. Native export는 모든 material mismatch를 보고하고 greedyQ-only behavior가 남으면 equivalence를 주장하면 안 됩니다. Supabase setup은 두 canonical migration을 모두 사용합니다. `001_initial.sql`은 table, RLS, withdrawal, analysis boundary를 만들고 고정 `002_browser_rpc.sql`은 capability-token session, consent-gated write, locked assignment를 만듭니다. 대체 security RPC를 임의로 만들면 안 됩니다.
