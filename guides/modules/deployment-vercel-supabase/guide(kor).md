# Vercel 및 Supabase Deployment Module

[English](./guide.md)

Application configuration과 database policy에는 registry에 등록된 canonical template을 사용합니다. Secret은 provider environment setting에 두고, browser access에는 최소 권한을 사용하며, privileged operation은 server-side에 유지하고 service-role credential을 노출하지 않습니다.

파일 준비, 서비스 설정, 배포, live URL 검증, 모집 시작은 서로 다른 상태입니다. 외부 변경은 승인과 사용 가능한 연결 도구가 있을 때만 수행합니다. 실제로 관찰한 결과만 보고합니다. 조사 시작 전 배포된 version에서 consent, resume, assignment persistence, 모든 terminal outcome, duplicate handling, withdrawal, data deletion request, analysis export를 시험합니다.

Account access를 요청하기 전에 study를 build하고 `supabase-connection-test.html`, `001_initial.sql`, `002_browser_rpc.sql`을 제공합니다. 연결된 browser runtime은 첫 save 전에 capability-protected session을 만들고 정확한 `greedyq_version`을 저장하며, Prolific external `SESSION_ID`를 internal UUID와 분리하고 검증된 Prolific identifier를 `greedyq_register_external`로 등록해야 합니다. 연구자 handoff에는 [SUPABASE-SETUP(kor).md](../../../SUPABASE-SETUP(kor).md)를 사용합니다.
