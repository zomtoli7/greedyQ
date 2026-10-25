# Vercel 및 Supabase Deployment Module

[English](./guide.md)

001–007 migration 전체를 적용한 후 `tools/cloud_lifecycle.cjs`의 `registerStudy(client, model)`로 검토한 모델을 각각 등록합니다. [RANDOMIZATION(kor).md](../../../RANDOMIZATION(kor).md)의 기존 데이터베이스 제한을 따릅니다. 계속 사용할 모든 연구의 등록을 계획하지 않은 채 운영 중인 공유 데이터베이스를 변경하면 안 됩니다. 과거 연결 검증은 새 실행 코드나 migration을 검증하지 않습니다.

Application configuration과 database policy에는 registry에 등록된 canonical template을 사용합니다. Secret은 provider environment setting에 두고, browser access에는 최소 권한을 사용하며, privileged operation은 server-side에 유지하고 service-role credential을 노출하지 않습니다.

파일 준비, 서비스 설정, 배포, live URL 검증, 모집 시작은 서로 다른 상태입니다. 외부 변경은 승인과 사용 가능한 연결 도구가 있을 때만 수행합니다. 실제로 관찰한 결과만 보고합니다. 조사 시작 전 배포된 version에서 consent, resume, assignment persistence, 모든 terminal outcome, duplicate handling, withdrawal, data deletion request, analysis export를 시험합니다.

기본 연구자 여정에서는 Vercel 로그인과 Vercel-native Supabase 리소스 승인 한 번만 요청합니다. Agent는 모든 migration과 환경 연결, 공개 설문 배포, Vercel Authentication으로 보호되는 별도 결과 배포를 구성합니다. Survey와 Results 링크를 명확히 제공하고 일반 연구자에게 Supabase 조작을 요구하지 않습니다.

Account access를 요청하기 전에 study를 build하고 `supabase-connection-test.html`과 `003_results_dashboard.sql`을 포함한 모든 등록 migration을 제공합니다. 연결된 browser runtime은 첫 save 전에 capability-protected session을 만들고 정확한 `greedyq_version`을 저장하며, Prolific external `SESSION_ID`를 internal UUID와 분리하고 세션·ID를 원자적 `greedyq_start_prolific`으로 등록해야 합니다. 일반 시작을 생성·등록 두 요청으로 나눠 구현하지 않습니다. `greedyq_start_prolific_preview`는 서버에서 검증된 Test 권한이 있을 때만 사용합니다. `is_test`와 `respondent_source`를 독립적으로 저장합니다. Fielding 전에 일반 테스트 응답을 만들고 결과 대시보드의 Test/Direct에서 보이는 동시에 Real responses가 변하지 않는지 확인합니다. 연구자 workflow에는 [RESULTS-DASHBOARD(kor).md](../../../RESULTS-DASHBOARD(kor).md)를 사용하며 [SUPABASE-SETUP(kor).md](../../../SUPABASE-SETUP(kor).md)는 복구 안내서로 취급합니다.

007 migration은 앞으로 저장되는 전체 답변 상태에서 빠진 답변을 같은 세션의 데이터베이스에서도 제거합니다. 조건부 문항이 숨겨져 답을 지운 경우 결과·CSV에도 남지 않아야 합니다. 다른 세션이나 과거 응답을 일괄 변경하지 않습니다. 기존 설치에는 누락된 007을 검토 후 적용하며, 검토 중인 유료 시험은 이번 로컬 점검으로 변경하지 않습니다.

초기 대화에서 미리보기는 계정 없이 가능하지만 실제 게시에는 연구자의 Vercel 로그인·연결 승인이 필요하다고 알려주세요. 선택적 [Vercel 에이전트 연결 준비](../../../docs/vercel-agent-onboarding(kor).md)는 로그인·Supabase 설정·응답 저장 검증을 대신하지 않습니다. 새 폴더에는 `init`으로 시작·종료 페이지와 전체 기록·배포 파일을 만듭니다. 로컬 파일 준비는 `preflight PATH_TO_STUDY`, 실제 배포 전 확인은 `preflight PATH_TO_STUDY --stage deployment`로 구분합니다. 후자는 mock 모드·미승인 결정을 차단하며, 통과 후에도 별도로 실제 연결을 확인해야 합니다.

연결 정보가 삽입된 후보가 별도 폴더에 있으면 `preflight PATH_TO_STUDY --stage deployment --deployment-index PREPARED_SURVEY/index.html`로 검사합니다. 원본 미리보기는 mock 상태로 유지하며 후보의 연구 내용이 현재 검증 결과와 같은지도 확인합니다.
