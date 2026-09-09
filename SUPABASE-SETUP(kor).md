# Supabase 프로젝트 연결하기

[English](./SUPABASE-SETUP.md)

**greedyQ release:** `0.2_2026-09-09_3aefdd0`
**현재 상태:** 계정 생성 직전까지 준비 완료, 외부 프로젝트 미연결

이 문서는 로컬 설문 검토가 끝난 지점에서 시작합니다. Database 지식은 필요하지 않습니다. AI는 한 번에 한 단계씩 진행하고 연결 테스트가 모두 통과할 때까지 test mode를 유지해야 합니다.

## 미리 준비된 것

- 순서대로 적용할 `001_initial.sql`, `002_browser_rpc.sql`
- 안전한 session 생성, 저장, 재접속, 고정 배정, Prolific 중복 감지, 철회 삭제 browser code
- 가상 데이터만 사용하는 browser-native connection tester
- Project URL과 publishable/anon key만 필요한 static deployment bundle
- 빠진 RPC, browser에 노출된 privileged credential, 불완전한 deployment file 자동 검사

## 프로젝트를 만든 뒤 할 일

1. 테스트용 Supabase project를 새로 만듭니다.
2. 승인된 데이터 위치 정책에 따라 region을 선택합니다. IRB 또는 기관 정책에서 정하지 않았다면 추측하지 않습니다.
3. SQL editor에서 [`001_initial.sql`](./examples/complete-study/supabase/migrations/001_initial.sql)을 한 번 실행합니다.
4. 이어서 [`002_browser_rpc.sql`](./examples/complete-study/supabase/migrations/002_browser_rpc.sql)을 실행합니다.
5. Project URL과 **publishable key** 또는 legacy `anon` key를 복사합니다. Service-role key나 database password는 복사하지 않습니다.
6. 이 두 public browser value를 AI에 전달하고 test survey의 `index.html` 안 `greedyq-deployment` block에 넣는 작업을 승인합니다.
7. `supabase-connection-test.html`을 열어 두 값을 입력하고 **Run all connection tests**를 누릅니다.
8. 모든 항목이 통과하기 전에는 Vercel deployment로 넘어가지 않습니다.

## 통과해야 하는 결과

가상 session 생성, 잘못된 capability token 차단, 고정 assignment, consent 이후 저장과 재접속, 가상 Prolific participant 중복 차단, anonymous response 목록 조회 차단, 철회 삭제, test-session 정리가 모두 통과해야 합니다. Tester는 `is_test = true`를 사용하므로 분석에서 제외됩니다. 실제 participant identifier는 사용하지 않습니다.

## Browser에 넣어도 되는 값

Project URL과 publishable/legacy anon key만 respondent-facing file에 넣을 수 있습니다. `service_role` key, database password, Supabase account access token, private API key, signing secret은 repository, survey folder, browser, chat 첨부, Vercel client 설정 또는 screenshot에 넣으면 안 됩니다.

## 즉시 멈출 조건

Migration 또는 connection test 실패, region 미승인, privileged key 노출, consent rule 미결정 또는 무관한 production data가 있는 경우 local mock mode를 유지합니다. 테스트 통과는 deployment나 participant 모집 승인이 아닙니다.

## 돌아온 뒤 사용할 메시지

```text
Supabase 테스트 프로젝트를 만들었어. SUPABASE-SETUP.md에 따라 연결을 도와줘. test mode를 유지하고 가상 participant data만 사용하며, project URL이나 publishable key를 전송하기 전에 확인받아. Vercel 배포나 participant 모집은 하지 마.
```
