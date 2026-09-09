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
- 문법·route, 저장값 reference, `.greedyq` 지속 상태, manifest hash, migration 안전 계약, secret 위치에 대한 안정적 검사.

## v0.2 안정화 관문

- [x] Python/JavaScript parser 및 normalized model conformance fixture.
- [x] 반응형 matrix와 NPS를 포함한 desktop, mobile, dual-preview rendering.
- [x] advanced control 구조화 수집 및 분석 가능한 CSV export.
- [x] greedyQ 전용 control의 Surveydown `sd_question_custom()` 생성.
- [x] 개발 환경에서 생성된 `app.R`의 R 문법 검사.
- [x] offline deployment preflight 및 결정론적 unit/regression suite.
- [ ] 실행 중인 Shiny app에서 생성된 모든 custom control의 native Surveydown 동작 검토.
- [ ] 새 계정 기준 Vercel/Supabase one-click provisioning test. 사용자 승인 OAuth 연결이 필요합니다.
- [ ] GPT, Claude, Gemini 및 다른 capable host에서 생성·수정·fork 평가.
- [ ] assistive technology 접근성 audit와 비기술 연구자 대상 usability study.

## 다음 제품 작업

1. 연구자가 Vercel 로그인 후 설문 URL과 결과 URL만 받도록 external OAuth provisioning 경험을 완성합니다.
2. production observability, migration versioning/rollback 안내, retention control, disaster-recovery exercise를 추가합니다.
3. weighted/stratified assignment, factorial study, reproducible seed, CBC/conjoint, external design table을 추가합니다.
4. 다국어 authoring과 respondent presentation을 추가합니다.
5. 명시적 최종 제출 승인 관문을 유지하면서 live OSF/preregistration adapter를 추가합니다.
6. confidence와 conversion report를 포함한 PPTX import path를 만듭니다.
7. greedyQ white paper를 뒷받침할 portability/conformance 연구를 수행합니다.

## 변하지 않는 요구사항

- 영문 Markdown이 기준이며 모든 파일에는 동기화된 `(kor).md` 사본이 있습니다.
- 주 runtime에서는 survey 작성자가 넣은 임의의 R 또는 JavaScript를 실행하지 않습니다.
- 연구자 기기에는 Python, R, Quarto, Node 없이 capable AI와 modern browser만으로 핵심 workflow를 사용할 수 있어야 합니다.
- 연구자 data ownership, consent-first storage, reproducible assignment, external operation의 정직한 검증을 보존합니다.
- 공개 Surveydown 문서에 근거해 독립 작성한 코드를 사용하고, Surveydown을 명시하며 Surveydown과 greedyQ를 함께 인용하도록 권합니다.
