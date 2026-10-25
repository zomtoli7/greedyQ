# 외부 연결 준비 상태

[English](./external-connection-readiness.md)

**무작위 배정 업그레이드:** 새 실행 코드는 001–006 migration과 검토한 모든 모델의 등록이 필요합니다. 서버 규약을 확인하여 이전 버전이나 일치하지 않는 설정은 차단합니다. [RANDOMIZATION(kor).md](../RANDOMIZATION(kor).md)를 따릅니다. 과거 계정 연결 시험이 이번 업그레이드의 승인 근거가 되지는 않습니다.

**Release:** `0.2_2026-10-25_0af2387`
**상태:** 로컬·연결 시험 검증 완료. 유료 Prolific 시험은 서비스 내부 검토로 중지됐으며 지급은 미검증입니다.

greedyQ는 Vercel, Supabase, Prolific 계정을 연결하기 전에 설문 애플리케이션을 준비하고 테스트합니다. 이 경계 덕분에 일반적인 설문 검토는 로컬에서 이루어지고, 마지막 외부 단계는 새로운 구현이 아니라 설정 및 검증 작업이 됩니다.

## 로컬에서 구현된 항목

- 동일한 고정 browser JavaScript core가 지원 QMD/YAML subset을 parse, validate, compile, render합니다.
- `index.html`은 현재 device에 따라 desktop 또는 mobile layout을 자동 선택합니다.
- `preview.html`은 서로 독립적인 desktop/mobile participant를 함께 표시하고 network write를 차단하며 synthetic browser storage를 사용합니다.
- 새로고침 재개, 안정적인 mock 배정, 철회/reset, 필수 및 구조화 응답, 숫자 범위, routing, terminal outcome을 자동 테스트합니다. 실제 Chrome E2E suite가 320px, 390px, 768px, 1280px layout, dashboard filter, 다운로드 CSV 구조도 검사합니다.
- JavaScript validator/compiler를 두 golden study와 의도적으로 잘못 만든 입력에서 Python reference implementation과 비교합니다.
- Static Vercel bundle과 offline deployment preflight를 생성합니다.
- 여섯 canonical Supabase migration은 테이블, RLS, 접근 토큰 RPC, 배정, 동의 후 응답 저장, 테스트·실제가 분리된 원자적 Prolific 등록, 철회 답변 삭제, 반복 시험 권한과 연구자 결과 경계를 정의합니다. 순서와 해시가 기록된 manifest가 연결 전에 누락·변경된 파일을 탐지합니다.
- Browser-native `supabase-connection-test.html`은 synthetic `is_test` session으로 연결된 project를 검증하고 끝난 뒤 철회합니다.
- Test code에서 Prolific launch parameter와 HTTPS completion URL을 검증합니다.
- 명시적으로 승인되지 않은 local draft 상태의 preregistration Markdown, JSON, SHA-256 manifest를 생성할 수 있습니다.
- 동작 동등성을 허위로 주장하지 않는 native surveydown project와 compatibility report를 생성할 수 있습니다. 생성된 logic은 문서화된 `sd_show_if()`, `sd_skip_if()`, `sd_stop_if()`를 사용하고 custom control은 QMD의 `sd_output()` placeholder와 server-side `sd_question_custom()`을 사용합니다. 전체 control gallery가 database 계정 없이 Surveydown 1.3.0, R, Quarto, Shiny의 안전한 preview mode에서 rendering 및 기동되는 것을 확인했습니다.

## 외부 계정이 필요한 항목

로컬 테스트는 live Vercel deployment, Supabase migration 적용, Prolific study 설정, production redirect 또는 실제 participant transaction을 수행하지 않습니다. 이런 작업에는 연구자의 계정, 권한, region 및 retention 선택, 명시적 승인이 필요합니다. 연결 후에는 각 서비스를 독립적으로 검증해야 하며, 생성 파일이 존재한다는 사실은 서비스가 작동한다는 증거가 아닙니다.

## 최종 연결 순서

1. 로컬 desktop/mobile preview를 연구자가 직접 검토합니다.
2. 모든 validation error와 중요한 연구 결정을 해결합니다.
3. Preregistration draft를 생성·검토하고 별도의 명시적 승인 후에만 제출합니다.
4. Vercel에 로그인하고 승인된 region의 Supabase Marketplace 리소스를 승인합니다. 연결된 agent가 `003_results_dashboard.sql`을 포함한 모든 migration을 적용하며 수동 SQL은 복구 경로에서만 사용합니다.
5. Vercel이 Supabase 환경변수를 동기화하도록 합니다. 설문에는 공개 설정만 전달하고 보호된 결과 함수의 서버 secret은 브라우저 파일에 넣지 않습니다.
6. `python3 -m greedyq preflight STUDY_DIR` 또는 동등한 agent check를 실행합니다.
7. 공개 설문과 Vercel Authentication으로 별도 보호된 결과 application을 배포합니다.
8. Prolific test parameter와 비production completion route를 설정하고 전체 test submission을 수행합니다.
9. 연결된 test service에서 resume, duplicate handling, consent refusal, 두 experiment condition, completion, withdrawal, analysis export를 검증합니다.
10. Production 전환 및 participant 모집 전 별도의 연구자 결정을 요구합니다.

완료하려면 설문 링크와 결과 링크 두 개가 모두 검증되어야 합니다. 일반 테스트 응답은 테스트/Direct에 나타나야 하고 실제 응답 수는 변하지 않아야 합니다.

## 증거와 한계

Repository unit/contract test는 deterministic behavior와 생성된 연결 artifact에 대한 로컬 증거를 제공합니다. 2026-10-25에 전용 Supabase 시험 데이터베이스와 배포된 Vercel 설문·결과 앱에서 001–006 및 철회·반복 Preview를 실행했습니다. 정확한 근거와 한계는 [클라우드 검증 기록](./prolific-cloud-test-2026-10-25(kor).md)을 참고하세요. 다른 계정·유료 Prolific 제출·모든 브라우저·보조 기술까지 검증한 것은 아니며 해당 환경별 확인이 남습니다.
