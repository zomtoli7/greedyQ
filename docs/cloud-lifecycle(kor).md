# 클라우드 설정 및 보관 운영 규약

<!-- GREEDYQ_DESKTOP_POLICY -->
**greedyQ로 설문을 만들거나 수정할 때는 컴퓨터에 설치한 AI 데스크톱 앱이 반드시 필요합니다. AI 웹 앱은 공식 지원하지 않습니다.** ChatGPT 데스크톱 또는 Claude Desktop을 공식 제공처에서 다운로드하세요. Gemini는 데스크톱 앱을 포함해 공식 지원하지 않습니다. 앱에서 파일을 읽고 만들고 작업을 실행하는 에이전트 기능을 사용해야 합니다. 앱 설치나 유료 구독만으로 이 기능이 보장되지는 않습니다. 필요한 도구가 없는 일반 채팅으로는 설문 제작을 진행하지 않습니다. 참여자가 설문에 응답하거나 연구자가 컴퓨터·모바일 미리보기와 결과 화면을 보는 데에는 계속 웹브라우저를 사용합니다. [설문 제작에 사용할 앱](../SUPPORTED-ENVIRONMENTS(kor).md).
<!-- /GREEDYQ_DESKTOP_POLICY -->

[English](./cloud-lifecycle.md)

에이전트 환경에서 기준 `tools/cloud_lifecycle.cjs`를 그대로 사용합니다. 연구자는 결정을 승인하며 명령어를 직접 실행하지 않습니다. 비공개 작업 폴더·`.env`·보관 파일·관리 도구를 Vercel에 올리지 않습니다.

## 재사용 코드에 반영한 연결 경험

`onboardingCommands({team,name,region})`는 셸 문자열이 아닌 Vercel CLI 인자 배열을 반환합니다. `whoami`와 팀을 확인하고 중복 방지를 위해 기존 연동·리소스를 조회하며, 승인된 지역과 무료 요금제를 사용합니다. 약관 승인이 필요하다는 응답은 사용자 확인 단계이지 생성 성공이 아닙니다. 생성 결과가 불확실하면 다시 조회한 뒤 재시도합니다. 사용 가능 상태와 연결 정보 동기화를 기다립니다. 최초 연결 직후에는 아직 인증 정보가 내려오지 않을 수 있습니다.

Supabase 리소스는 서버 비밀키를 받는 결과 프로젝트에만 연결합니다. 인증 정보는 비공개로 내려받습니다. `databaseClient(pg.Client, POSTGRES_URL)`는 공식 CA를 다운로드하고 충돌하는 URL의 SSL 옵션을 제거한 뒤 TLS 인증서를 검증합니다. `migrate(client,migrationDirectory)`는 파일 해시를 확인하고 적용 이력을 트랜잭션에 기록하여 안전하게 재시도합니다. 이력이 없는 기존 데이터베이스는 별도 대조가 필요합니다. 처음의 CREATE TABLE을 무작정 재실행하거나 최신 상태라고 간주하지 않습니다.

`prepareDeployments({repo,model,directory,url,publishableKey})`는 기준 템플릿에서 허용된 파일만 골라 설문·결과 폴더를 분리 생성합니다. 공개 publishable key만 받습니다. 반환된 결과 보호 설정(`ssoProtection.deploymentType=all`)은 **배포 전에** 적용합니다. 운영 별칭을 포함한 모든 결과 URL·API의 비로그인 접근 차단을 확인합니다. 프리뷰 URL만 보호해서는 안 됩니다. 보호를 끌 수 있는 것은 설문 프로젝트뿐입니다. 전달 전 Test/Direct 저장, 실제 응답 수 유지, 재접속과 접근 경계를 검증합니다. 연구 모델이나 테스트·운영 모드를 몰래 바꾸지 않습니다.

## 보관 실행

새 실행 코드를 사용하기 전에 001–008를 적용하고 검토한 연구마다 `registerStudy(client, model)`을 호출합니다. 실험이 아닌 설문도 등록해야 합니다. [배정 및 업그레이드 요구사항](../RANDOMIZATION(kor).md)을 참고합니다. 운영 중인 공유 데이터베이스에는 다른 연구도 등록하고 점검 시간을 조정하지 않은 채 004를 적용하면 안 됩니다. 새 저장 단계는 미등록 연구를 차단합니다. 과거 검증 기록은 당시 버전에 대한 결과이며 이번 업그레이드를 자동으로 검증하지는 않습니다.

에이전트 환경에 Node, `pg` 패키지, 보관 파일 생성용 Python이 필요합니다. 연구자 컴퓨터에는 추가 설치가 필요하지 않습니다. 외부 계정 없이 데이터베이스·서비스 어댑터를 주입해 테스트할 수 있습니다.

비공개 프로세스 환경에 `POSTGRES_URL`, `SUPABASE_URL`을 두고 `node tools/archive_study.cjs snapshot PRIVATE_CONFIG.json`을 실행합니다. 설정:

```json
{
  "studyId": "study-id",
  "approvedStudyId": "study-id",
  "model": "/private/study/preview-model.json",
  "output": "/private/archives/new-unique-directory",
  "targets": {
    "team": "team_exact",
    "survey": "prj_survey",
    "results": "prj_results",
    "supabase": "exactprojectref"
  }
}
```

모델이 배포된 연구에 속하는지, 정확한 리소스 ID와 데이터베이스 인증 정보가 같은 프로젝트를 가리키는지, 다른 연결 앱이나 아직 응답이 없는 연구까지 조사했는지 확인합니다. `closeAndSnapshot`은 연구별 쓰기 차단을 설치하고 테이블 잠금으로 진행 중 쓰기를 정리한 뒤 연구를 닫고 일곱 데이터 테이블을 한 트랜잭션에서 읽습니다. 페이지 수 제한이 있는 대시보드 API를 사용하지 않습니다. 트랜잭션 실패 시 롤백합니다. 이후 로컬 파일 생성이 실패해도 수집은 닫힌 상태로 유지합니다. 내보내기를 재시도하며 몰래 수집을 재개하지 않습니다. 비공개 스냅샷으로 ZIP 생성도 오프라인 재시도할 수 있습니다. 차단에는 온라인 철회를 포함한 추가·수정·삭제가 모두 포함되므로 연구팀 연락 경로와 추후 요청을 위한 별도 승인 관리 절차를 마련합니다.

`greedyq.archive.make_archive`는 ZIP을 생성 후 다시 열어 해시를 확인하고, 실제·테스트 CSV를 분리하며, 미완료 응답과 과거 문항 ID를 보존하고, 복잡한 값은 JSON 셀로 저장합니다. 운영 CLI는 별도 다운로드 가능한 CSV도 만듭니다. 비공개 파일 다운로드가 타사 AI나 공개 호스트로의 전송 승인을 뜻하지는 않습니다. 원래 연구 파일·미디어는 별도 보관하세요. 전체 SQL·Storage 복원본이 아닙니다.

연구자가 파일 저장을 확인하고 정확한 프로젝트들의 중지를 승인한 뒤 `node tools/archive_study.cjs pause PRIVATE_CONFIG.json`을 실행합니다. 두 번째 설정:

```json
{
  "archivePath": "/private/archives/new-unique-directory/study-archive.zip",
  "expectedHash": "sha256-returned-by-snapshot",
  "approvedStudyId": "study-id",
  "downloadConfirmed": true,
  "exclusiveResources": true,
  "resourceOwnershipReviewed": true,
  "freePlanReviewed": true,
  "linkedProjectsReviewed": true,
  "targets": {
    "team": "team_exact",
    "survey": "prj_survey",
    "results": "prj_results",
    "supabase": "exactprojectref"
  }
}
```

참·거짓 값들은 실제 승인·검토 기록이며 자동으로 채울 기본값이 아닙니다. `VERCEL_TOKEN`, `SUPABASE_ACCESS_TOKEN`은 승인된 관리용 인증 정보여야 합니다. 공개 키나 service-role 데이터베이스 키는 Supabase 관리 토큰이 아닙니다. Marketplace만 연결한 계정에서는 추가 서비스 승인이 필요할 수 있습니다. 채팅으로 비밀번호·비밀키를 요청하지 않습니다. 허용된 관리 경로가 없으면 다운로드 준비 상태에서 멈추고 사람에게 Pause 메뉴를 안내합니다. 삭제·연동 제거로 대체하지 않습니다.

마지막 단계는 변경 전 ZIP 내용·SHA-256·연구와 리소스의 일치·공유 여부·소유권을 재확인합니다. 설문, 결과, Supabase 순서로 중지하며 비공개 `pause-events.jsonl`에 요청·확인 상태를 기록합니다. 시간 초과나 비동기 중지 대기는 성공이 아닙니다. 나중에 다시 상태를 확인하며 이미 중지된 리소스는 건너뜁니다. 일부 실패는 삭제나 자동 재개 없이 일부 완료 상태로 남깁니다. 관련 별칭 주소와 데이터베이스 직접 쓰기로 응답이 수집되지 않는지 확인하고, 무료 프로젝트 자리는 별도로 서비스에서 확인합니다. HTTP 성공만으로 자리가 확보됐다고 추론하지 않습니다.

## 검증 범위

`python3 -m unittest tests.test_archive`, `node --test tests/cloud_lifecycle.cjs`와 전체 Python 테스트를 실행합니다. 실제 수집 종료·재개와 연구자가 참여한 Supabase 중지·재개를 검증했습니다. 정확한 범위와 현재 리소스 상태는 [반복 사용자 인수 검사](./repeat-user-acceptance(kor).md)를 참고하세요. 유료 계정 동작, 대규모 동시 접근 부하, 무인 Supabase 관리 권한은 검증하지 않았습니다. ZIP 복원은 필수 범위가 아닙니다. 서비스 재개는 **Resume project**, 수집 재개는 별도 승인한 `reopen` CLI 작업을 사용합니다.

출처: [Vercel 중지](https://vercel.com/docs/projects/managing-projects), [Supabase 중지 API와 권한](https://supabase.com/docs/reference/api/v1-pause-a-project), [Supabase TLS](https://supabase.com/docs/guides/platform/ssl-enforcement).

기존 CLI 기반 운영 경로는 계속 지원합니다. 승인된 공식 Vercel 연결이 있으면 계정·팀을 확인한 뒤 지원 작업에 우선 사용하고, 기능이 없으면 같은 검수·승인 경계를 유지하며 기존 경로를 사용합니다. Onboard your agent는 필수가 아닙니다. CLI와 MCP의 인증은 별도로 확인하고 팀 접근 거절은 해당 팀 승인으로 해결하며 몰래 다른 인증으로 우회하지 않습니다. [연결 선택 규약](../guides/modules/deployment-vercel-supabase/guide(kor).md)을 따르세요.
