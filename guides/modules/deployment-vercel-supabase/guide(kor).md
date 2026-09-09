# Vercel 및 Supabase Deployment Module

[English](./guide.md)

Application configuration과 database policy에는 registry에 등록된 canonical template을 사용합니다. Secret은 provider environment setting에 두고, browser access에는 최소 권한을 사용하며, privileged operation은 server-side에 유지하고 service-role credential을 노출하지 않습니다.

파일 준비, 서비스 설정, 배포, live URL 검증, 모집 시작은 서로 다른 상태입니다. 외부 변경은 승인과 사용 가능한 연결 도구가 있을 때만 수행합니다. 실제로 관찰한 결과만 보고합니다. 조사 시작 전 배포된 version에서 consent, resume, assignment persistence, 모든 terminal outcome, duplicate handling, withdrawal, data deletion request, analysis export를 시험합니다.

기본 연구자 여정에서는 Vercel 로그인과 Vercel-native Supabase 리소스 승인 한 번만 요청합니다. Agent는 모든 migration과 환경 연결, 공개 설문 배포, Vercel Authentication으로 보호되는 별도 결과 배포를 구성합니다. Survey와 Results 링크를 명확히 제공하고 일반 연구자에게 Supabase 조작을 요구하지 않습니다.

Account access를 요청하기 전에 study를 build하고 `supabase-connection-test.html`과 `003_results_dashboard.sql`을 포함한 모든 등록 migration을 제공합니다. 연결된 browser runtime은 첫 save 전에 capability-protected session을 만들고 정확한 `greedyq_version`을 저장하며, Prolific external `SESSION_ID`를 internal UUID와 분리하고 검증된 Prolific identifier를 `greedyq_register_external`로 등록해야 합니다. `is_test`와 `respondent_source`를 독립적으로 저장합니다. Fielding 전에 일반 테스트 응답을 만들고 결과 대시보드의 Test/Direct에서 보이는 동시에 Real responses가 변하지 않는지 확인합니다. 연구자 workflow에는 [RESULTS-DASHBOARD(kor).md](../../../RESULTS-DASHBOARD(kor).md)를 사용하며 [SUPABASE-SETUP(kor).md](../../../SUPABASE-SETUP(kor).md)는 복구 안내서로 취급합니다.
