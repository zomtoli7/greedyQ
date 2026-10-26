# greedyQ 로드맵

<!-- GREEDYQ_DESKTOP_POLICY -->
**greedyQ로 설문을 만들거나 수정할 때는 컴퓨터에 설치한 AI 데스크톱 앱이 반드시 필요합니다. AI 웹 앱은 공식 지원하지 않습니다.** ChatGPT 데스크톱 또는 Claude Desktop을 공식 제공처에서 다운로드하세요. Gemini는 데스크톱 앱을 포함해 공식 지원하지 않습니다. 앱에서 파일을 읽고 만들고 작업을 실행하는 에이전트 기능을 사용해야 합니다. 앱 설치나 유료 구독만으로 이 기능이 보장되지는 않습니다. 필요한 도구가 없는 일반 채팅으로는 설문 제작을 진행하지 않습니다. 참여자가 설문에 응답하거나 연구자가 컴퓨터·모바일 미리보기와 결과 화면을 보는 데에는 계속 웹브라우저를 사용합니다. [설문 제작에 사용할 앱](../SUPPORTED-ENVIRONMENTS(kor).md).
<!-- /GREEDYQ_DESKTOP_POLICY -->

[English](./roadmap.md)

**현재 단계:** v0.2 지원 범위 유지·보수, v0.3 CBC 가져오기·서버 수집·보호된 결과와 로컬 검증
**계획 원칙:** 구현 전에 규약을 확정한다

## v0.2에서 완성된 범위

- 저장소에서 시작하고, 결정을 이어서 기록하며, 중요한 판단은 연구자가 승인하는 specification-driven AI-native 연구 workflow.
- `greedyQSimple`, `greedyQExperiment` profile, 모듈형 guide, hash registry, 영문/한글 문서 쌍, 두 개의 golden study와 control gallery.
- 의존성이 적은 Python reference parser·validator·compiler·local runtime·preview server.
- 플랫폼 중립 JavaScript parser·validator·renderer·respondent runtime, desktop/mobile 동시 preview와 연구자용 structure view.
- 문서화된 Surveydown 문항 control 16개와 greedyQ media/advanced control: rank order, side-by-side, NPS, timing, constant sum, pick/group/rank, drill down, 승인된 custom control.
- 동의 이후 수집, session 재접속, 철회 시 삭제, 결정론적 배정, direct/Prolific 출처 표시, test 응답 분리, Supabase RPC 경계, Vercel 정적 배포 bundle.
- real/test 및 direct/Prolific filter, 진행·조건 summary, 분석 가능한 구조화 CSV column, variable guide를 포함한 결과 dashboard.
- preregistration draft와 manifest, Prolific route, native Surveydown project export, 명시적 compatibility report.
- 원자적 ID 연결·중복 방지·만료되는 비공개 반복 시험 권한·철회 답변 삭제·보호된 ID 포함 CSV·서비스 검토 대기 상태를 갖춘 기본 Prolific 시작.
- 문법·route, 저장값 reference, `.greedyq` 지속 상태, manifest hash, migration 안전 계약, secret 위치에 대한 안정적 검사.

## v0.2 안정화 관문

- [x] Python/JavaScript parser 및 normalized model conformance fixture.
- [x] 반응형 matrix와 NPS를 포함한 desktop, mobile, dual-preview rendering.
- [x] advanced control 구조화 수집 및 분석 가능한 CSV export.
- [x] greedyQ 전용 control의 Surveydown `sd_question_custom()` 생성.
- [x] 개발 환경에서 생성된 `app.R`의 R 문법 검사.
- [x] offline deployment preflight 및 결정론적 unit/regression suite.
- [x] 320px, 390px, 768px, 1280px 실제 browser E2E. 조건부 표시, 구조화 control, 재접속, 종료 navigation, dashboard filter, CSV download를 포함합니다.
- [x] 순서가 기록된 Supabase migration manifest, checksum 검증, 변조 탐지 및 복구 안내.
- [x] 연구자 직접 작성·AI-assisted 신규 연구, 수정, fork, custom control, preview 승인, 외부 작업의 정직한 보고를 다루는 AI workflow conformance scenario.
- [x] 공개 Surveydown 1.3.0 API에 대한 생성 project 대조 및 생성된 app·QMD R block의 R 문법 검사.
- [x] 전체 native Surveydown control gallery가 database 계정 없이 Surveydown 1.3.0, R, Quarto, Shiny의 안전한 preview mode에서 rendering 및 기동됩니다.
- [ ] 후속 범위: 실행 중인 Shiny에서 모든 생성 custom control의 동작 대조. 완전한 동등성을 주장하지 않습니다.
- [x] 2026-09-10 연구자와 함께한 새 계정 Vercel/Supabase 연결 시험. 008까지의 migration은 별도 연결 시험 리소스에서도 검증했습니다. 모든 이후 계정·버전을 자동 검증한 것으로 보지 말고 날짜별 근거를 확인합니다.
- [x] 완료·거부·철회·반복 시작의 실제 Prolific 초안 Preview 및 보호된 결과·삭제 확인.
- [x] 실제 유료 제출 1건을 답변·CSV와 대조하고 연구자가 2026-10-26 승인·지급을 확인했습니다. 지급 API를 독립 조회한 것은 아닙니다.
- [x] 전용 종료 안내는 이미 구현되어 있으며 네 참여자 언어·컴퓨터/모바일에서 시작·응답 도중 종료와 일반 통신 오류 구분을 재시험했습니다.
- [x] 연구자가 요청한 즉시 정리를 2026-10-26 완료했습니다. 운영 시험 응답·ID 테이블과 확인한 비공개 사본을 정리하고 수집을 닫았으며 Prolific 지급 내역은 보존했습니다.
- [ ] 후속 연구: 여러 capable host에서 생성·수정·fork 평가.
- [ ] 후속 연구: 보조기술 접근성 점검과 실제 연구자 사용성 연구. 기존 키보드·반응형 회귀는 계속 필요합니다.

## 다음 제품 작업

1. CBC를 v0.3 핵심 기능으로 만듭니다. [명세 초안·골든 예제](../drafts/v0.3/cbc/README(kor).md)부터 시작하고 AI 협업, 빈 CSV·XLSX 직접 작성, 기존 설계표 가져오기를 선택지로 제공합니다. CSV/XLSX 가져오기·로컬 미리보기를 구현했습니다. CBC 전용 서버 저장·동의·철회·결과·보관은 로컬 검증했습니다. 다음은 신규 계정 승인 시험·유료 CBC·QMD 혼합·네이티브 내보내기입니다. v0.2 기능으로 활성화하지 않습니다.
2. 기준 가져오기·검사, 동일한 브라우저 계약, CBC 표시, 지속 배정·순서, 철회에 안전한 저장과 긴 형태 내보내기를 차례로 구현합니다. 적합성 검증 후에만 CBC를 등록합니다.
3. v0.2의 Vercel/Supabase/direct/Prolific 여정을 안정적으로 유지합니다. 008 이후 첫 새 실제 종료 시각과 실제 유료 내부 선별은 해당 환경의 확인 사항이며 완료한 유료 시험을 반복할 이유가 아닙니다.
4. 후속: 운영 관찰, 보관기간 설정, 실제 장애 복구, 층화·적응 배정, 요인 설계와 재현 가능한 설계 생성기. 단순 가중 비율과 지원 문항·선택지·페이지 섞기는 이미 있으므로 미구현으로 나열하지 않습니다.
5. 후속: 추가 참여자 언어, PPTX 가져오기, white paper용 호스트 간 적합성 연구. OSF 초안은 유지하며 registry 로그인·제출은 범위 밖입니다.
6. 홈페이지 게시는 별도 Work가 담당합니다. 소스 생성만으로 게시를 주장하지 않습니다. 유료 시험 운영 자료 정리는 완료했지만 서비스 백업과 연구자 개인 사본은 검사하지 않았습니다.

## 마감 근거와 한계

[v0.2 마감](./v0.2-closeout-2026-10-26(kor).md), [유료 시험 완료](./prolific-paid-test-completion-2026-10-26(kor).md), [CBC 기획](../drafts/v0.3/cbc/README(kor).md)을 참고합니다. 지원 범위 마감이 모든 Surveydown 설정·native custom control 동등성, 서명 Prolific 링크·지급 자동화, 모든 환경, 통계 설계 효율을 보장하지는 않습니다.

## 변하지 않는 요구사항

- 영문 Markdown이 기준이며 모든 파일에는 동기화된 `(kor).md` 사본이 있습니다.
- 주 runtime에서는 survey 작성자가 넣은 임의의 R 또는 JavaScript를 실행하지 않습니다.
- 연구자 기기에는 Python, R, Quarto, Node 없이 필요한 도구가 있는 AI 데스크톱 앱과 웹브라우저로 핵심 workflow를 사용할 수 있어야 합니다.
- 연구자 data ownership, consent-first storage, reproducible assignment, external operation의 정직한 검증을 보존합니다.
- 공개 Surveydown 문서에 근거해 독립 작성한 코드를 사용하고, Surveydown을 명시하며 Surveydown과 greedyQ를 함께 인용하도록 권합니다.
