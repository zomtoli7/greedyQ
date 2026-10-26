# Netlify에 공개 시작 안내 게시하기

[English](./NETLIFY-START.md)

이는 프로젝트 관리자가 한 번 설정하는 작업이며 연구자에게 Netlify 계정을 요구하지 않습니다. JavaScript 없는 공개 시작 페이지는 `START-HERE.md`와 한국어·중국어 원문에서 생성합니다. 전체 운영 절차는 `INITIALIZE.md`와 필수 모듈에 있습니다. Markdown과 HTML은 같은 원문을 사용하며 안내를 따로 작성하지 않습니다.

## 저장소 한 번 연결하기

로그인한 Netlify 팀에서 **Add new project → Import an existing project → GitHub**를 선택하고 `zomtoli7/greedyQ` 접근을 승인한 뒤 그 저장소를 고릅니다.

| 항목 | 입력값 |
| --- | --- |
| Project name | 가능하면 `greedyq-start`, 없으면 배정된 이름도 가능 |
| Production branch | `main` |
| Framework preset | Other / 프레임워크 없음 |
| Base directory | 빈칸, 저장소 최상위 |
| Build command | `python3 tools/build_bootstrap.py --output dist/bootstrap` |
| Publish directory | `dist/bootstrap` |
| 비밀 환경 변수 | 없음 |

저장소의 `netlify.toml`이 빌드·게시 설정을 제공합니다. 파일이 푸시된 뒤 게시합니다. 일부 팀은 기본 비공개이므로 로그인·비밀번호 없이 읽을 수 있도록 공개 상태를 확인합니다. 별도 도메인은 필요 없습니다. 배포 뒤 실제 배정된 공개 `https://…netlify.app/START-HERE.html` 주소를 복사하고 주소를 추측하지 않습니다. 설문을 배포하거나 데이터베이스에 접근하거나 기존 Vercel 프로젝트를 바꾸는 작업이 아닙니다.

## 홈페이지 프롬프트를 바꾸기 전에 검증하기

로그인하지 않고 실제 주소를 여세요. 본문에 `greedyq-start-bootstrap-1`, 데스크톱 지원 조건, `INITIALIZE.md`, 기존 연구 이어가기 안내가 있어야 합니다. 영어·한국어·중국어, 언어 링크, 휴대폰 화면, JavaScript를 끈 상태의 읽기를 확인합니다. `bootstrap-manifest.json`과 실제 파일 해시도 대조합니다. 초기화 링크는 움직이는 main이 아니라 Netlify가 배포한 정확한 Git `COMMIT_REF`를 가리킵니다.

Gemini에게 연구를 만들지 말고 읽기 확인 문구와 지원 앱만 알려달라고 요청합니다. 성공해도 그 세션에서 이 페이지가 읽힌 것만 입증하며 제공업체 전체 도메인 정책이나 Gemini 지원을 입증하지 않습니다. 읽기 실패를 설정 성공으로 보고하지 않습니다.

실제 URL과 게시가 확인된 뒤에만 홈페이지 복사 요청을 짧게 줄여 이 공개 입구로 연결합니다. 가이드를 못 읽으면 멈추고 알려달라는 한 줄은 유지합니다. 추측한 Netlify 주소를 게시하지 않습니다.

## 저장한 연구

공개 입구는 연구자를 안내하며 저장된 연구의 잠금·이력을 대체하지 않습니다. 작성용 폴더·ZIP은 잠근 가이드·실행 파일 버전을 유지하고 해시를 확인합니다. 버전 기록이 소스 커밋보다 나중에 생길 수 있어 소스 커밋만으로 잠근 모든 파일을 복원할 수는 없습니다. 완전히 일치하는 사본을 확보하거나 멈추고 승인할 업그레이드 사본을 논의합니다. 진행 중인 설문은 자동 업그레이드하지 않습니다. 종료된 연구의 데이터 아카이브는 분석·보관용이며 온라인 서비스 복원용이 아닙니다.

## 관리자 로컬 확인

소스를 커밋한 뒤 `python3 tools/build_bootstrap.py`를 실행합니다. 공개 출력은 전용 `dist/bootstrap` 폴더뿐입니다. 생성기는 관계없는 파일이 있는 출력 폴더나 체크아웃과 다른 `COMMIT_REF`를 거부합니다. 설문 응답·비공개 연구 기록·인증 정보·저장소 전체를 복사하지 않습니다. `robots.txt`가 수집을 허용해도 특정 AI가 읽는다고 보장할 수는 없습니다.

참고: [Netlify 저장소 배포](https://docs.netlify.com/start/quickstarts/deploy-from-repository/), [빌드·게시 설정](https://docs.netlify.com/build/configure-builds/overview/).


로컬 준비 검증: Python 241개가 통과했습니다. 홈페이지 이동·복사 검사 4개와 JavaScript를 끈 3개 언어·320/1280px 읽기, 언어 링크, 페이지 가로 넘침 없음을 확인했습니다. 원문 문서의 언어 짝 검사는 추적 중인 Markdown으로 범위를 명확히 하고, 생성된 공개 Markdown·HTML은 별도 직접 일치·링크 검사로 확인합니다. 실제 Netlify 설정·배정 주소·Gemini 읽기·홈페이지 프롬프트 교체는 아직 대기입니다.
