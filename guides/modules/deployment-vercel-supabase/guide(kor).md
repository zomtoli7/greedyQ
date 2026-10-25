# Vercel 및 Supabase Deployment Module

[English](./guide.md) · [简体中文](./guide(zh-CN).md)

001–007 migration 전체를 적용한 후 `tools/cloud_lifecycle.cjs`의 `registerStudy(client, model)`로 검토한 모델을 각각 등록합니다. [RANDOMIZATION(kor).md](../../../RANDOMIZATION(kor).md)의 기존 데이터베이스 제한을 따릅니다. 계속 사용할 모든 연구의 등록을 계획하지 않은 채 운영 중인 공유 데이터베이스를 변경하면 안 됩니다. 과거 연결 검증은 새 실행 코드나 migration을 검증하지 않습니다.

Application configuration과 database policy에는 registry에 등록된 canonical template을 사용합니다. Secret은 provider environment setting에 두고, browser access에는 최소 권한을 사용하며, privileged operation은 server-side에 유지하고 service-role credential을 노출하지 않습니다.

파일 준비, 서비스 설정, 배포, live URL 검증, 모집 시작은 서로 다른 상태입니다. 외부 변경은 승인과 사용 가능한 연결 도구가 있을 때만 수행합니다. 실제로 관찰한 결과만 보고합니다. 조사 시작 전 배포된 version에서 consent, resume, assignment persistence, 모든 terminal outcome, duplicate handling, withdrawal, data deletion request, analysis export를 시험합니다.

기본 연구자 여정에서는 Vercel 로그인과 Vercel-native Supabase 리소스의 필요한 승인을 요청합니다. Agent는 모든 migration과 환경 연결, 공개 설문 배포, Vercel Authentication으로 보호되는 별도 결과 배포를 구성합니다. Survey와 Results 링크를 명확히 제공하고 일반 연구자에게 Supabase 조작을 요구하지 않습니다.

Account access를 요청하기 전에 study를 build하고 `supabase-connection-test.html`과 `003_results_dashboard.sql`을 포함한 모든 등록 migration을 제공합니다. 연결된 browser runtime은 첫 save 전에 capability-protected session을 만들고 정확한 `greedyq_version`을 저장하며, Prolific external `SESSION_ID`를 internal UUID와 분리하고 세션·ID를 원자적 `greedyq_start_prolific`으로 등록해야 합니다. 일반 시작을 생성·등록 두 요청으로 나눠 구현하지 않습니다. `greedyq_start_prolific_preview`는 서버에서 검증된 Test 권한이 있을 때만 사용합니다. `is_test`와 `respondent_source`를 독립적으로 저장합니다. Fielding 전에 일반 테스트 응답을 만들고 결과 대시보드의 Test/Direct에서 보이는 동시에 Real responses가 변하지 않는지 확인합니다. 연구자 workflow에는 [RESULTS-DASHBOARD(kor).md](../../../RESULTS-DASHBOARD(kor).md)를 사용하며 [SUPABASE-SETUP(kor).md](../../../SUPABASE-SETUP(kor).md)는 복구 안내서로 취급합니다.

007 migration은 앞으로 저장되는 전체 답변 상태에서 빠진 답변을 같은 세션의 데이터베이스에서도 제거합니다. 조건부 문항이 숨겨져 답을 지운 경우 결과·CSV에도 남지 않아야 합니다. 다른 세션이나 과거 응답을 일괄 변경하지 않습니다. 기존 설치에는 누락된 007을 검토 후 적용하며, 검토 중인 유료 시험은 이번 로컬 점검으로 변경하지 않습니다.

초기 대화에서 미리보기는 계정 없이 가능하지만 실제 게시에는 연구자의 Vercel 로그인·연결 승인이 필요하다고 알려주세요. 선택적 [Vercel 에이전트 연결 준비](../../../docs/vercel-agent-onboarding(kor).md)는 로그인·Supabase 설정·응답 저장 검증을 대신하지 않습니다. 새 폴더에는 `init`으로 시작·종료 페이지와 전체 기록·배포 파일을 만듭니다. 로컬 파일 준비는 `preflight PATH_TO_STUDY`, 실제 배포 전 확인은 `preflight PATH_TO_STUDY --stage deployment`로 구분합니다. 후자는 mock 모드·미승인 결정을 차단하며, 통과 후에도 별도로 실제 연결을 확인해야 합니다.

연결 정보가 삽입된 후보가 별도 폴더에 있으면 `preflight PATH_TO_STUDY --stage deployment --deployment-index PREPARED_SURVEY/index.html`로 검사합니다. 원본 미리보기는 mock 상태로 유지하며 후보의 연구 내용이 현재 검증 결과와 같은지도 확인합니다.

## 연결 방식 선택 규약

기본 연구자 여정은 설문 검토 → Vercel 로그인 → 필요한 Vercel/Supabase 접근 승인 → 검증한 설문·결과 링크 전달입니다. **Onboard your agent는 선택 사항이며 필수 선행 조건이 아닙니다.** 일반적인 첫 사용 절차에 도구 설치·플러그인 설정·앱 재시작을 추가하지 않습니다.

1. 설치나 설정 전에 호스트의 기존 연결을 확인합니다. 이미 사용 가능한 공식 Vercel 연결이 있으면 읽기 전용 조회로 인증 계정과 대상 팀을 확인한 뒤 지원하는 작업에 우선 사용합니다. 팀 목록이 비었다고 팀이나 프로젝트가 없다고 단정하지 않습니다.
2. 공식 연결이 없거나 필요한 작업을 지원하지 않으면 계정·팀 범위를 별도로 검증한 기존 CLI/통합 경로를 사용합니다. 계정을 바꾸거나 개인 계정을 기본값으로 사용하거나 프로젝트를 중복 생성하지 마세요. CLI 로그인 성공을 MCP 승인으로 간주하지 않습니다. 두 경로에 같은 기본 파일·연구자 승인·개인정보 경계·실제 운영 검수를 적용합니다.
3. 팀 접근이 거절되면 제공자의 `authorize_team_access` 복구 절차를 해당 팀에 사용하고 반환된 승인 링크를 연구자에게 보여줍니다. 직접 승인할 때까지 대기한 뒤 같은 연결에서 같은 요청을 다시 확인합니다. SSO가 없는 팀도 별도 팀 승인이 필요할 수 있습니다. 계정 전체를 재연결하거나 인증 정보를 지우거나 다른 인증으로 거절된 권한을 몰래 우회하지 않습니다. 임시 승인 URL은 공개 문서나 참가자 파일에 넣지 않습니다.
4. Onboard your agent는 요청받았거나 연구자가 반복 사용을 위해 지원 호스트를 준비하려는 경우에만 선택적으로 제안합니다. 기존 도구를 재사용하고 해당 호스트에 가이드를 한 번 설치하며, 새 도구가 나타나지 않을 때만 갱신·재시작합니다. 다른 설정을 보존합니다. 전역 연결 준비 중에는 프로젝트 생성·연결, Supabase 설정, 배포, 수집을 수행하지 않습니다.
5. 설정 후 문서 검색·팀 목록·대상 팀 접근을 실제 도구 호출로 확인합니다. 설치·인증·도구 발견·팀 접근·배포·실제 응답 저장 검증은 별도 상태입니다. 온보딩 시험만 성공했다고 연구 전체를 준비 완료로 표시하지 않습니다. 어느 경로도 사용할 수 없으면 완성된 연구를 보존하고 가능한 인계 방법을 설명합니다.

계정·프로젝트 변경에는 확인을 유지하고, 필요한 로그인·승인만 쉬운 말로 요청합니다. 연구자에게 인증 정보를 붙여 넣거나 내부 도구 이름을 배우도록 요구하지 않습니다.
