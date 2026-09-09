# 로컬 운영 및 복구 안내

[English](./operations-runbook.md)

이 문서는 외부 계정을 연결하기 전에 greedyQ가 수행할 수 있는 모든 검사를 설명합니다. 일반적으로 연구자가 직접 실행할 필요는 없으며, 연결된 AI agent가 수행하고 필요한 결과만 쉽게 설명해야 합니다.

## 외부 연결 전

1. 연구를 validate·build하고 전체 regression 및 실제 browser E2E test를 실행합니다.
2. desktop, 390px mobile, 320px narrow-mobile, 조건부 표시, 종료, 재접속, 철회, 구조화 응답 경로를 확인합니다.
3. preregistration draft와 native Surveydown export를 생성합니다. R을 사용할 수 있으면 생성된 `app.R`을 parse합니다.
4. deployment preflight를 실행합니다. 필수 browser file, server-only secret, RLS/withdrawal contract, migration 번호 순서와 `supabase/migrations/manifest.json`에 기록된 모든 checksum을 검사합니다.
5. 연구는 test mode로 유지합니다. Production 전환은 중요한 fielding action이므로 정확한 설문 검토, consent/privacy 결정, 필요한 preregistration gate, live persistence test 성공, 연구자의 명시적 승인이 필요합니다.

## Migration 복구

- 이미 적용한 migration을 수정하지 않습니다. 다음 번호의 migration을 추가합니다.
- Migration을 변경하면 다시 build하여 `manifest.json`에 순서와 SHA-256 값을 기록합니다.
- Checksum이 다르면 준비 후 deployment bundle이 바뀐 것입니다. 중단하고 다시 build합니다.
- 숫자 순서대로 migration을 적용하고 배포된 release identifier를 기록합니다. Canonical migration 재실행은 복구에 쓰기 전에 disposable project에서 검사해야 합니다.

## Data 복구와 보존

- `is_test`로 test와 production 응답을 분리하고 test를 연구 데이터로 바꾸지 않습니다.
- Backup, retention 기간, deletion 일정은 연구자 결정입니다. Fielding 전에 기록합니다.
- 철회·삭제 test에서는 비식별 lifecycle event만 남기고 answer, assignment, external identifier가 하나의 작업으로 삭제되는지 확인합니다.
- CSV는 특정 시점의 snapshot입니다. 분석 파일과 함께 study release, filter, export time, data dictionary를 기록합니다.
- 실제 database 상태와 researcher dashboard를 확인하지 않고 복구나 삭제 성공을 주장하지 않습니다.

## 연결 준비 증거

자동 test 통과, 생성 artifact와 manifest 일치, 두 golden study preflight 통과, browser artifact의 secret 부재를 확인하고, 남은 항목이 live Vercel, Supabase, Prolific, OSF 또는 native Surveydown 실행을 실제로 요구할 때만 외부 연결을 요청할 준비가 된 것입니다.
