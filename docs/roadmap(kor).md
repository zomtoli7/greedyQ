# greedyQ 로드맵

[English](./roadmap.md)

**현재 단계:** v0.2 안정화
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
- [ ] 실행 중인 Shiny app에서 생성된 모든 custom control의 native Surveydown 동작 검토.
- [x] 2026-09-10 연구자와 함께한 새 계정 Vercel/Supabase 연결 시험. 최신 006은 별도 연결 시험 리소스에서도 검증했습니다. 모든 이후 계정·버전을 자동 검증한 것으로 보지 말고 날짜별 근거를 확인합니다.
- [x] 완료·거부·철회·반복 시작의 실제 Prolific 초안 Preview 및 보호된 결과·삭제 확인.
- [ ] 진짜 유료 Prolific 제출 대조·승인·지급: 최초 1명 시험은 일반 내부 검토로 중지됐습니다.
- [ ] GPT, Claude, Gemini 및 다른 capable host에서 생성·수정·fork 평가.
- [ ] assistive technology 접근성 audit와 비기술 연구자 대상 usability study.

## 다음 제품 작업

1. 승인된 Vercel/Supabase 설문·결과 여정을 유지하고 서비스 검토 후 유료 Prolific 시험을 마칩니다. 검토 대기 중에는 설정을 보존합니다.
2. production observability, 연구자가 설정하는 retention control, live disaster-recovery exercise를 추가합니다. offline migration versioning, 무결성 검사, 복구 안내는 완료되었습니다.
3. weighted/stratified assignment, factorial study, reproducible seed, CBC/conjoint, external design table을 추가합니다.
4. 구현된 영어·한국어·중국어 간체/번체 외의 참여자 언어 팩을 확장하고 연구자가 작성 문구의 번역을 검토하도록 유지합니다.
5. 공식 OSF 항목 목록과 다운로드할 사전등록 초안을 유지합니다. OSF 로그인·제출·등록 관리는 범위 밖이며 연구자가 별도로 등록합니다.
6. confidence와 conversion report를 포함한 PPTX import path를 만듭니다.
7. greedyQ white paper를 뒷받침할 portability/conformance 연구를 수행합니다.

## 변하지 않는 요구사항

- 영문 Markdown이 기준이며 모든 파일에는 동기화된 `(kor).md` 사본이 있습니다.
- 주 runtime에서는 survey 작성자가 넣은 임의의 R 또는 JavaScript를 실행하지 않습니다.
- 연구자 기기에는 Python, R, Quarto, Node 없이 capable AI와 modern browser만으로 핵심 workflow를 사용할 수 있어야 합니다.
- 연구자 data ownership, consent-first storage, reproducible assignment, external operation의 정직한 검증을 보존합니다.
- 공개 Surveydown 문서에 근거해 독립 작성한 코드를 사용하고, Surveydown을 명시하며 Surveydown과 greedyQ를 함께 인용하도록 권합니다.
