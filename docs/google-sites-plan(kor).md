# greedyq.org: Google Sites 구성안

[English](./google-sites-plan.md)

소유자는 이미 공개된 Google Site를 사용합니다. 이 문서는 사이트 구성이며 새 편집의 저장·게시를 증명하는 기록은 아닙니다. 기존 임베드의 렌더러·갤러리·영어/한국어/중국어 내용은 `website/`에 보존했으며 `tools/build_website_embed.py`로 교체 파일을 생성합니다. Google Sites 호스팅을 유지합니다. Surveydown의 작업 중심 구성을 참고하되 문구·시각 자료를 복제하지 않습니다.

## 메뉴와 원본 연결

| 공개 섹션 | 내용 | 저장소 원본 |
| --- | --- | --- |
| 홈 | greedyQ 소개, 3단계 흐름, 시작·예제 버튼 | README.md, docs/product-brief.md |
| 시작하기 | 새 연구, 재개, 수정, 포크와 복사할 첫 프롬프트 | START-HERE.md, USER-GUIDE.md |
| 첫 설문 만들기 | 직접 문항 작성·AI 초안 선택, 연구팀명, 윤리 안내 시점 | USER-GUIDE.md, guides/core/communication.md |
| 문항 갤러리 | 실제 조작·모바일 보기·AI 요청 예시 | examples/control-gallery, USER-GUIDE.md |
| 설문 흐름 | 필수 응답, 조건부 문항, 이동, 구조 보기 | USER-GUIDE.md, preview 명세 |
| 실험 | 배정과 순서의 차이, 고정 선택지, 제한·예시 | RANDOMIZATION.md, 호환성 점검 |
| 테스트·검토 | 컴퓨터·모바일, 가상 데이터, 수정 요청 | USER-GUIDE.md, examples/simple-satisfaction-study |
| 배포·수집 | 계정 승인, 설문·보호된 결과 링크, 테스트·실제 구분 | SUPABASE-SETUP.md, RESULTS-DASHBOARD.md |
| Prolific 연결하기 | Guide → Collect에서 배포와 수집 다음, 응답 확인 전의 독립 페이지. 설정·반복 Preview·유료 전환·검토 중지 | PROLIFIC-SETUP.md, website/prolific-content.json |
| 종료·다시 사용 | 보관·다운로드, 수집 종료, 중지·재개, 새 연구, 초안 업그레이드 | ARCHIVING.md, UPGRADING.md |
| 사전등록 | 초안 파일, 미정 결정, 별도 제출 | PREREGISTRATION.md |
| 고급·호환성 | Native Surveydown export, 지원 범위, 커스텀 컨트롤 | 호환성 점검, export 가이드 |
| 소개·인용·업데이트 | 정체성, 두 프로젝트 인용, MIT, 릴리스·이력 | CITATION.md, NOTICE.md, updates/ |

모든 페이지에 영문·한국어 전환 링크를 둡니다. 상위 메뉴는 시작, 사용법, 예제, 소개로 묶고 고급 정보를 첫 사용 경로에서 분리합니다. 안내 페이지마다 한 문장 목적, 복사할 프롬프트, 번호별 행동, 기대 화면·결과, 문제 해결, 다음 단계를 둡니다. 하단에 확인한 릴리스·날짜를 표시합니다.

## 홈 초안

헤드라인: **Be greedy with your time. Just ask your AI to make your questionnaire.**

소개: “greedyQ는 AI가 연구 아이디어부터 작동하는 설문과 보호된 결과 페이지까지 안내하도록 돕습니다. 연구는 여러분이 결정하고, 파일과 설정은 AI가 담당합니다.”

주 버튼: 내 설문 만들기. 보조 버튼: 예제 설문 체험하기.

아래에는 연구 설명 → 실제 미리보기 검토 → 배포 승인 순서를 보여줍니다. 미리보기에는 외부 서비스 연결이 필요하지 않지만 배포에는 계정·연동 승인이 필요할 수 있음을 설명합니다. 무제한 무료, 승인 불필요, 모든 Surveydown 기능 지원을 약속하지 않습니다.

## 인터랙티브 갤러리

Google Sites는 설명서이며 참가자 런타임이나 비공개 대시보드가 아닙니다. 공개된 버전별 정적 갤러리를 링크·임베드하고 새 탭 열기를 함께 제공합니다. GitHub의 HTML 파일 화면은 작동하는 웹페이지가 아닙니다. 실제 공개 갤러리 주소를 확인한 뒤 연결합니다. 응답 기록, 인증정보, 보호된 결과, 운영 연구를 임베드하지 않습니다. 가상 예제만 사용합니다. 편집 미리보기뿐 아니라 공개 화면에서 임베드·키보드·좁은 화면을 검사합니다. [Google 임베드 안내](https://support.google.com/sites/answer/90569?hl=en).

## 사용자가 알려주실 것

1. Google Sites **편집 주소**, 또는 로그인한 Google 계정에 빈 사이트를 만들어도 된다는 승인.
2. 개인 계정인지 학교·직장 Google Workspace인지. 관리 계정은 관리자 권한이 필요할 수 있습니다.
3. 편집 권한이 있는 현재 브라우저 로그인 상태. 비밀번호·인증코드를 보내거나 존재하지 않는 AI 이메일에 소유권을 넘길 필요는 없습니다.
4. greedyq.org 등록·DNS 업체명과 필요한 정확한 DNS 값을 입력·승인할 준비. 메일·다른 서비스 기록은 건드리지 않습니다.
5. 메뉴 구성, 공개 연락처, 로고, 우선 언어, 공개 갤러리 주소에 대한 확인.
6. 최종 공개 및 도메인 연결 승인. 초안 편집, 공개 공유, DNS 변경은 별도 작업입니다.

Google 안내상 하위 도메인이 필요하므로 Sites는 **www.greedyq.org**, **greedyq.org**는 등록 업체의 지원 기능으로 www 주소에 연결하는 구성을 계획합니다. 도메인 연결은 사이트 소유자만 가능합니다. 소유권 검증과 DNS 변경이 필요할 수 있고 반영에 최대 48시간 걸릴 수 있습니다. 학교·직장 계정은 관리자 작업이 필요할 수 있습니다. [공식 도메인 안내](https://support.google.com/sites/answer/9068867?hl=en).

초안 편집 권한은 제한하고 공개 방문자에게 편집 권한을 주지 않습니다. 공개 후 로그아웃 상태에서 확인합니다. [공개·공유](https://support.google.com/sites/answer/6372880?hl=en), [편집 권한](https://support.google.com/sites/answer/97934?hl=en).

## 공개 전 점검

- 처음 온 연구자가 GitHub 코드를 읽지 않고 시작할 수 있음.
- 프롬프트 복사, 영문·한국어 전환, 다음 단계 링크 정상.
- 갤러리는 릴리스 런타임을 사용하며 외부 응답을 쓰지 않음.
- 미리보기·실제 설문·비공개 결과의 차이가 분명함.
- 컴퓨터·모바일 메뉴, 이미지, 대비, 임베드 확인.
- 릴리스, 제한, 인용, 다운로드 주소가 저장소와 일치.
- 소유자가 공개 내용, 도메인, 게시를 각각 승인.
- 연결된 브라우저로 편집할 수 없으면 페이지별 붙여넣기 자료를 제공하며 Sites 편집 완료를 주장하지 않음.
