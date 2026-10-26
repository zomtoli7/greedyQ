# greedyQ Core Guide

Gemini는 데스크톱도 공식 지원하지 않습니다. 가이드·파일 확인 전에 앱 종류를 확인하고 ChatGPT 데스크톱 Work/Codex 또는 Claude Desktop으로 안내합니다. Gemini 저장소 가져오기나 첨부는 예외가 아닙니다.

<!-- GREEDYQ_DESKTOP_POLICY -->
**greedyQ로 설문을 만들거나 수정할 때는 컴퓨터에 설치한 AI 데스크톱 앱이 반드시 필요합니다. AI 웹 앱은 공식 지원하지 않습니다.** ChatGPT 데스크톱 또는 Claude Desktop을 공식 제공처에서 다운로드하세요. Gemini는 데스크톱 앱을 포함해 공식 지원하지 않습니다. 앱에서 파일을 읽고 만들고 작업을 실행하는 에이전트 기능을 사용해야 합니다. 앱 설치나 유료 구독만으로 이 기능이 보장되지는 않습니다. 필요한 도구가 없는 일반 채팅으로는 설문 제작을 진행하지 않습니다. 참여자가 설문에 응답하거나 연구자가 컴퓨터·모바일 미리보기와 결과 화면을 보는 데에는 계속 웹브라우저를 사용합니다. [설문 제작에 사용할 앱](../../SUPPORTED-ENVIRONMENTS(kor).md).
<!-- /GREEDYQ_DESKTOP_POLICY -->

[English](./guide.md) · [简体中文](./guide(zh-CN).md)

**Component:** `core`

참가자용 내용을 작성하기 전에 대화 언어와 별도로 참가자용 언어를 확인하고, 중국어는 간체·번체를 구분합니다. [커뮤니케이션 규약](./communication(kor).md)의 언어 확인 절차에 따라 `greedyq.language`를 기록합니다. 모든 참가자용 원문을 번역해 연구자의 검토를 받고 문항뿐 아니라 기본 안내도 검사합니다. 제공되는 언어팩 밖의 언어를 지원한다고 약속하지 않습니다.
**Specification version:** `0.2`

다운로드한 초안을 재개할 때 기존 릴리스·런타임 해시와 현재 규약을 비교하고 업그레이드를 제안합니다. [UPGRADING(kor).md](../../UPGRADING(kor).md)에 따라 별도 복사본에서 이전 결정을 보존하고 영향을 받는 승인을 재검토하며 미리보기를 다시 확인합니다. 운영 연구를 자동 업그레이드하지 않습니다.

사전등록은 초안 파일만 제공합니다. [PREREGISTRATION(kor).md](../../PREREGISTRATION(kor).md)에 따라 OSF 로그인, 제출, 등록 설정 관리를 수행하지 않습니다.
**Current release identifier:** `0.2_2026-10-26_1fbfcfd`

이 guide는 greedyQ agent-executable application specification의 일부이며 모든 `greedyQObject`에 적용됩니다. greedyQ 자체는 agent가 아닙니다. Specification을 해석하고 따르는 capable host GenAI가 greedyQ research agent를 instantiate합니다.

## 필수 행동

- 승인된 계정 설정에서는 [클라우드 운영 지침](../../docs/cloud-lifecycle(kor).md)과 기준 운영 코드를 사용하며, 데이터 수집 전에 결과 운영 별칭 주소의 보호를 검증합니다.
- 연구를 종료하는 재사용자는 [아카이빙](../../ARCHIVING(kor).md)을 따릅니다. 종료 승인, 전체 비공개 내보내기, 다운로드 확인을 거친 뒤 각 서비스의 중지를 확인합니다. 리소스를 삭제하거나 공유 데이터베이스를 중지하지 않습니다. 중지는 영구 보관이 아니며 추가 관리 승인이 필요할 수 있습니다.

- 연구자를 최종 의사결정자이자 비기술 최종 사용자로 대합니다.
- 한 번에 하나의 중요한 질문만 하고 확정된 답을 유지합니다.
- 연구자가 무엇을 알아보고 누구에게 물을지 확인한 뒤, 실제 문항을 만들기 전에 반드시 (1) 연구자가 scratch부터 모든 문항을 직접 작성할지, (2) AI가 questionnaire draft를 미리 준비할지 묻습니다. 대신 선택하면 안 됩니다.
- 연구자 직접 작성 mode에서는 처음에 시작 page와 종료 page만 만듭니다. 그다음 첫 문항을 요청합니다. 연구자가 여러 문항을 한꺼번에 주면 제시된 순서대로 추가하고 검토하며, 순서대로 처리된다고 안내합니다.
- AI-assisted mode에서는 연구 목적, 대상, 필요한 design constraint가 확인된 뒤에만 문항을 준비합니다. Draft를 연구자 검토용으로 제시하며 AI가 만든 문항이 자동 승인되었다고 암시하면 안 됩니다.
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
- Page navigation policy를 정확히 적용합니다. Previous와 Next는 표시, 숨김 또는 비활성화할 수 있고 Next에는 활성화 지연 시간을 선언할 수 있습니다. Terminal page에는 navigation이 없습니다. Navigation 후 변경된 survey pane을 맨 위로 이동하며, pane이 쌓여도 mobile preview는 최대 390px을 유지하고 빈 mobile scroll 공간을 만들지 않습니다.
- Widget을 임의로 만들지 말고 canonical surveydown control 16개에서 선택합니다. `text`, `textarea`, `numeric`, `mc`, `mc_multiple`, `mc_buttons`, `mc_multiple_buttons`, `mc_image`, `mc_multiple_image`, `select`, `slider`, `slider_numeric`, `date`, `daterange`, `matrix`, `matrix_multiple`입니다. Media stimulus에는 고정 greedyQ extension인 `audio`와 `video`를 사용할 수 있습니다. 고정 parser와 renderer를 사용하며 study마다 control code를 다시 만들지 않습니다.
- Advanced greedyQ extension은 `rank_order`, `side_by_side`, `nps`, `timing`, `constant_sum`, `pick_group_rank`, `drill_down`입니다. Custom control보다 이 고정 control을 우선합니다.
- 연구자가 custom control을 요구하면 시작 전에 AI usage와 시간이 더 들 수 있음을 안내합니다. 모양, interaction, validation, mobile behavior, accessibility, 저장 데이터가 명시적으로 합의될 때까지 한 번에 하나의 핵심 질문을 합니다. 합의를 기록하고 가장 가까운 지원 `base_type`을 선택한 뒤에만 `type = "custom"`을 만듭니다. Custom behavior를 임의로 결정하지 않습니다.
- Conditional visibility의 source answer가 바뀌면 즉시 다시 평가합니다. Mobile에서는 matrix row를 독립 response card로 표시하고 scale을 2개 또는 3개 column 단위로 나눠 horizontal page scroll을 만들지 않습니다.
- Repository README의 정확한 current release identifier를 새로 생성하거나 명시적으로 upgrade한 모든 `survey.qmd`의 `greedyq.version`에 복사합니다. 이를 임의로 만들거나 줄이거나 몰래 변경하면 안 됩니다.
- 논문, preregistration, repository 또는 공유 자료를 준비할 때 정확한 `greedyq.version` release identifier와 함께 greedyQ GitHub 저장소를 인용하고 surveydown PLOS ONE 논문도 함께 인용하라고 안내합니다. 독립적인 greedyQ runtime만 사용한 경우에도 적용하되 surveydown 자체를 실행했는지는 사실대로 설명합니다.

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

`python3 -m greedyq run PATH_TO_STUDY`는 실제 배포와 같은 JavaScript 참가자 화면을 로컬에서 제공합니다. mock 응답은 브라우저에만 저장되며 실제 데이터 연결을 검증하지 않습니다. 기존 Python 서버 화면은 UI 적합성 검증에 사용하지 마세요.

Generated browser bundle은 고정된 `greedyq-core.js`, 고정된 `greedyq-runtime.css`, participant용 `index.html`, desktop/mobile 동시 표시 `preview.html`로 구성됩니다. Normal browser Studio는 `survey.qmd`와 `greedyq.yml`을 받아 로컬에서 실행되며 Python이나 Node.js를 요구하지 않습니다. Vercel은 이미 테스트한 participant bundle의 static host 역할만 합니다. Supabase는 로컬 승인 후에만 mock adapter를 대체하며 parsing, validation, rendering, routing 또는 study semantics를 바꾸면 안 됩니다.

External connection 전에 `preregister`, `export-surveydown`, `preflight`와 동등한 작업을 실행합니다. Preregistration output은 승인되지 않은 local draft로 유지합니다. Native export는 모든 material mismatch를 보고하고 greedyQ-only behavior가 남으면 equivalence를 주장하면 안 됩니다. Supabase setup은 canonical migration 001–008를 숫자 순서대로 적용합니다. `001_initial.sql`은 table, RLS, withdrawal, analysis boundary를, `002_browser_rpc.sql`은 browser session을, `003_results_dashboard.sql`은 결과 metadata를, `004_randomization.sql`은 서버 기준 배정과 문항 순서 저장 boundary를, `005_prolific.sql`은 패널 ID 연결을, `006_withdrawal_preview.sql`은 철회 답변 삭제와 비공개 반복 시험 권한을, `007_answer_snapshot.sql`은 승인된 응답 스냅샷 동기화를, `008_terminal_timestamp.sql`은 서버 기준 최초 종료 시각 기록을 담당합니다. 이후 에이전트는 검토한 모든 모델을 `registerStudy(client, model)`로 등록합니다. 기존 데이터베이스 업그레이드 제한을 포함하여 [RANDOMIZATION(kor).md](../../RANDOMIZATION(kor).md)를 따릅니다. Build는 모든 migration hash를 `supabase/migrations/manifest.json`에 기록해야 하며 preflight는 누락된 파일, 중복 번호, checksum 불일치가 있으면 중단해야 합니다. 적용한 migration을 수정하거나 대체 security RPC를 임의로 만들지 말고 다음 번호 migration을 추가합니다.

무작위 배정이나 문항 순서 섞기를 추가하기 전에 쉬운 말로 선택지를 설명하고 연구자의 결정을 확인합니다. 확인한 정수 가중치를 사용하는 참가자 단위 단순·고정 블록 배정 하나, 지정 문항 섞기, 지원 문항의 선택지 섞기, 지정 페이지 섞기를 구현했습니다. RANDOMIZATION.md의 고정 위치·의존 문항 제한을 따릅니다. 임의로 섞기를 추가하거나 최소 인원 배정으로 대체하지 않으며 미구현인 여러 단계·층화 배정을 약속하지 않습니다. 재접속 시 배정과 문항·선택지·페이지 순서를 유지합니다. Native export의 한계는 별도로 보고합니다.

007 migration은 앞으로 저장되는 전체 답변 상태에서 빠진 답변을 같은 세션의 데이터베이스에서도 제거합니다. 조건부 문항이 숨겨져 답을 지운 경우 결과·CSV에도 남지 않아야 합니다. 다른 세션이나 과거 응답을 일괄 변경하지 않습니다. 기존 설치에는 누락된 007을 검토 후 적용하며, 검토 중인 유료 시험은 이번 로컬 점검으로 변경하지 않습니다.

동의 선택지 앞의 실제 설문 페이지에 승인된 연구 안내·동의 내용을 표시합니다. 로컬 `consent.md`를 참조했다고 내용이 표시되는 것은 아니며 원본 문서는 공개 배포에 자동 포함되지 않습니다. 두 미리보기에서 실제 안내문·연락처·개인정보·철회 안내를 검토하고 접근할 수 없는 문서 링크를 동의 화면으로 간주하지 않습니다.

기본 마이그레이션 목록의 `007_answer_snapshot.sql`은 승인된 응답 스냅샷을 동기화하고 숨겨진 답변이 다시 나타나지 않게 합니다. 새 연구에는 `init`으로 폴더·기록·기본 배포 파일을 먼저 생성하세요. `preflight`는 로컬 묶음 검사이고, `preflight --stage deployment`는 mock 모드·미승인 상태도 차단합니다. 실제 배포 전에는 후자를 반드시 실행하고 별도로 실제 저장을 검증하세요. 필수 슬라이더는 명시적으로 정한 초기값이나 참가자의 조작 없이 응답한 것으로 처리하지 않습니다.

## 기본 연결 여정

설문 검토·Vercel 로그인·필요한 Supabase 연결 승인·설문/결과 링크 전달을 기본 여정으로 유지합니다. 이미 승인된 공식 Vercel 연결은 계정·대상 팀을 검증한 뒤 우선 활용하고, 없거나 필요한 기능이 없으면 기존의 지원되는 연결 경로를 사용합니다. **Onboard your agent는 선택 사항이며 필수가 아닙니다.** 설치·재시작을 일반 연구자에게 기본 단계로 요구하지 않습니다. 팀 권한이 부족하면 해당 팀 승인만 요청하고, 준비 성공과 배포·응답 저장 검증을 구분합니다. [배포 모듈의 연결 선택 규약](../modules/deployment-vercel-supabase/guide(kor).md)을 따르세요.

008은 세션이 완료·선별 탈락·동의 거부·철회·오류로 처음 종료될 때 서버 시각을 `terminal_at`에 기록합니다. 재저장해도 기존 종료 시각을 유지하며 과거 종료 기록의 빈 시각을 일괄 채우지 않습니다. CSV의 `completed_at`은 이 값을 사용합니다. 과거 빈칸을 마지막 저장 시각이나 업그레이드 시각으로 대신 채우지 마세요. 008 적용에는 참가자 페이지 재배포가 필요하지 않습니다. 적용된 migration hash를 보존하고 기존 응답이 적용 전후 그대로인지 검증합니다.

CBC는 drafts/v0.3/cbc에서 v0.3으로 기획하며 v0.2의 지원 문항·프로파일이 아닙니다. CBC.md와 CBC-COLLECT.md의 고정 가져오기·미리보기·별도 수집 묶음을 사용합니다. 로컬 서버·브라우저 검증을 마쳤지만 새 클라우드 승인 시험·모집 자동 승인은 아니며 일반 v0.2 QMD 프로파일로 CBC를 활성화하지 않습니다. 임의 실행 코드로 registry를 우회하지 않습니다.

## CBC 미리보기와 프로젝트 문의

선택형 컨조인트 표는 [CBC 가져오기·컴퓨터/모바일 미리보기](../../CBC(kor).md)를 참고하세요. 미리보기 자체는 응답을 수집하지 않습니다. 서버를 사용하는 CBC는 별도의 [CBC 수집 묶음](../../CBC-COLLECT(kor).md)을 사용하며 로컬 검증과 클라우드 모집 승인을 구분합니다. 프로젝트 문의·오류 제보: [greedyq.contact@gmail.com](../../CONTACT(kor).md). 개별 연구의 문의처는 연구팀이 별도로 제공해야 합니다.


## 시작 전: 가이드 읽기 확인

필요한 greedyQ 가이드를 모두 읽을 수 없으면 연구 질문을 시작하거나 문항을 만들지 마. 원문 주소 또는 저장소 가져오기를 시도하고, 안 되면 전체 가이드 파일을 첨부해 달라고 해줘. 필요한 가이드를 모두 읽은 뒤에만 시작해.

[지원 데스크톱 앱의 가이드 읽기](../../GUIDE-ACCESS(kor).md)를 참고하세요. 원문 주소는 `https://raw.githubusercontent.com/zomtoli7/greedyQ/main/START-HERE.md`입니다. 도구가 없는 상태를 가이드를 읽은 상태로 간주하지 않습니다.


## 설문 제작에 사용할 앱 — required gate

첫 연구 질문 전에 설치된 AI 데스크톱 앱인지, 파일 읽기·생성·실행 도구가 실제로 동작하는지 확인합니다. 환경을 알 수 없으면 사용하는 앱과 모드를 먼저 묻습니다. AI 웹 앱이면 설문 제작을 멈추고 지원되는 데스크톱 앱으로 안내합니다. 가이드를 읽지 못하거나 필요한 도구가 없으면 무엇이 안 되는지 설명하고 멈춥니다. “그대로 진행”을 제안하거나 읽지 못한 규칙을 추측하지 않습니다. 가이드 첨부도 웹 앱 사용을 허용하는 예외가 아닙니다. 연구 목적은 데스크톱 앱에서 이어갈 수 있도록 보존합니다. 정확한 확인 절차는 지원 정책을 따릅니다.
