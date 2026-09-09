# 외부 연결 준비 상태

[English](./external-connection-readiness.md)

**Release:** `0.2_2026-09-09_3aefdd0`
**상태:** 로컬 검증 완료, 외부 계정 미연결

greedyQ는 Vercel, Supabase, Prolific 계정을 연결하기 전에 설문 애플리케이션을 준비하고 테스트합니다. 이 경계 덕분에 일반적인 설문 검토는 로컬에서 이루어지고, 마지막 외부 단계는 새로운 구현이 아니라 설정 및 검증 작업이 됩니다.

## 로컬에서 구현된 항목

- 동일한 고정 browser JavaScript core가 지원 QMD/YAML subset을 parse, validate, compile, render합니다.
- `index.html`은 현재 device에 따라 desktop 또는 mobile layout을 자동 선택합니다.
- `preview.html`은 서로 독립적인 desktop/mobile participant를 함께 표시하고 network write를 차단하며 synthetic browser storage를 사용합니다.
- 새로고침 재개, 안정적인 mock 배정, 철회/reset, 필수 응답, 숫자 범위, routing, terminal outcome을 자동 테스트합니다.
- JavaScript validator/compiler를 두 golden study와 의도적으로 잘못 만든 입력에서 Python reference implementation과 비교합니다.
- Static Vercel bundle과 offline deployment preflight를 생성합니다.
- Canonical Supabase migration은 table, RLS boundary, capability-token RPC access, lock을 사용하는 균형 배정, consent-gated answer write, 중복 Prolific identifier 거부, transactional withdrawal deletion을 정의합니다.
- Browser-native `supabase-connection-test.html`은 synthetic `is_test` session으로 연결된 project를 검증하고 끝난 뒤 철회합니다.
- Test code에서 Prolific launch parameter와 HTTPS completion URL을 검증합니다.
- 명시적으로 승인되지 않은 local draft 상태의 preregistration Markdown, JSON, SHA-256 manifest를 생성할 수 있습니다.
- 동작 동등성을 허위로 주장하지 않는 native surveydown project와 compatibility report를 생성할 수 있습니다.

## 외부 계정이 필요한 항목

로컬 테스트는 live Vercel deployment, Supabase migration 적용, Prolific study 설정, OSF 제출, production redirect 또는 실제 participant transaction을 수행하지 않습니다. 이런 작업에는 연구자의 계정, 권한, region 및 retention 선택, 명시적 승인이 필요합니다. 연결 후에는 각 서비스를 독립적으로 검증해야 하며, 생성 파일이 존재한다는 사실은 서비스가 작동한다는 증거가 아닙니다.

## 최종 연결 순서

1. 로컬 desktop/mobile preview를 연구자가 직접 검토합니다.
2. 모든 validation error와 중요한 연구 결정을 해결합니다.
3. Preregistration draft를 생성·검토하고 별도의 명시적 승인 후에만 제출합니다.
4. 승인된 region에 Supabase project를 만들고 `001_initial.sql`, `002_browser_rpc.sql` 순서로 적용합니다.
   비기술 연구자용 [Supabase 설정 안내](../SUPABASE-SETUP(kor).md)를 따르며 service-role key나 database password를 제공하지 않습니다.
5. Deployment 설정에는 Supabase project URL과 anonymous key만 넣습니다. Service-role key와 database password는 절대 노출하지 않습니다.
6. `python3 -m greedyq preflight STUDY_DIR` 또는 동등한 agent check를 실행합니다.
7. 이미 테스트한 static bundle을 Vercel에 deploy합니다.
8. Prolific test parameter와 비production completion route를 설정하고 전체 test submission을 수행합니다.
9. 연결된 test service에서 resume, duplicate handling, consent refusal, 두 experiment condition, completion, withdrawal, analysis export를 검증합니다.
10. Production 전환 및 participant 모집 전 별도의 연구자 결정을 요구합니다.

## 증거와 한계

Repository unit/contract test는 deterministic behavior와 생성된 연결 artifact에 대한 로컬 증거를 제공합니다. PostgreSQL SQL은 test로 source review되지만 이 계정 미연결 단계에서는 live Supabase PostgreSQL instance에 실행하지 않았습니다. Browser file은 로컬 제공 및 syntax check를 수행하며, target browser/device에서의 cross-browser 및 assistive-technology acceptance test는 release 단계에 남습니다.
