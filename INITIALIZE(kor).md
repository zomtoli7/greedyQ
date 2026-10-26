# greedyQ 시작하기

<!-- GREEDYQ_HOST_FILTER_START -->

규약의 작성 언어와 관계없이 사용자와의 모든 대화는 사용자 언어로 합니다. 설문 참여자에게 보여줄 언어는 별도로 확인합니다.
## 첫 동작: 사용하는 AI 앱을 확인하고 미지원 환경에서는 멈추기

다른 가이드 읽기, 연구 질문, 파일 첨부 요청, 연구 파일 생성보다 먼저 이 확인을 수행합니다. 새 연구·수정·사본 만들기·재개 모두에 적용하는 첫 실행 지침입니다.

- 필요한 도구가 있는 설치된 ChatGPT 데스크톱 앱(Work/Codex) 또는 에이전트 도구가 있는 Claude Desktop에서만 진행합니다.
- AI 웹사이트, Gemini(데스크톱 포함), 모바일 AI 앱, 다른 제공업체, 브라우저에서 설치한 웹사이트 바로가기/PWA라면 **“ChatGPT, Claude 데스크톱 앱만 현재 지원됩니다.”**라고 안내하고 설문 제작을 멈춥니다. 그대로 진행하자고 제안하거나 ZIP·전체 가이드 첨부를 요청하거나 연구 인터뷰·문항 생성을 시작하지 않습니다. 가이드를 읽을 수 있어도 예외가 아닙니다.
- 실제 사용 앱을 모르면 어떤 앱을 쓰는지, 컴퓨터에 설치한 데스크톱 앱인지만 먼저 묻습니다. 답을 기다린 뒤 연구를 시작합니다. 모델 이름, 유료 구독, 스크린샷, 주소 읽기 성공만으로 데스크톱 앱이라고 추정하지 않습니다. 신뢰할 수 있는 앱 환경 정보가 있으면 활용하되 자동 감지를 했다고 지어내지 않습니다.
- 지원되는 데스크톱 앱임을 확인한 뒤 SUPPORTED-ENVIRONMENTS.md에 따라 실제 파일·미리보기 도구를 확인합니다. 앱 설치만으로 충분하지 않습니다. 도구가 없으면 제작을 멈추고 필요한 기능이 있는 데스크톱 에이전트로 안내합니다.

이 제작 환경 확인은 참여자의 웹브라우저 응답이나 연구자의 미리보기·결과 확인을 제한하지 않습니다.
<!-- GREEDYQ_HOST_FILTER_END -->


Gemini는 데스크톱도 공식 지원하지 않습니다. 가이드·파일 확인 전에 앱 종류를 확인하고 ChatGPT 데스크톱 Work/Codex 또는 Claude Desktop으로 안내합니다. Gemini 저장소 가져오기나 첨부는 예외가 아닙니다.

<!-- GREEDYQ_DESKTOP_POLICY -->
**greedyQ로 설문을 만들거나 수정할 때는 컴퓨터에 설치한 AI 데스크톱 앱이 반드시 필요합니다. AI 웹 앱은 공식 지원하지 않습니다.** ChatGPT 데스크톱 또는 Claude Desktop을 공식 제공처에서 다운로드하세요. Gemini는 데스크톱 앱을 포함해 공식 지원하지 않습니다. 앱에서 파일을 읽고 만들고 작업을 실행하는 에이전트 기능을 사용해야 합니다. 앱 설치나 유료 구독만으로 이 기능이 보장되지는 않습니다. 필요한 도구가 없는 일반 채팅으로는 설문 제작을 진행하지 않습니다. 참여자가 설문에 응답하거나 연구자가 컴퓨터·모바일 미리보기와 결과 화면을 보는 데에는 계속 웹브라우저를 사용합니다. [설문 제작에 사용할 앱](SUPPORTED-ENVIRONMENTS(kor).md).
<!-- /GREEDYQ_DESKTOP_POLICY -->

[English](./INITIALIZE.md) · [简体中文](./INITIALIZE(zh-CN).md)

greedyQ는 online academic research를 위한 agent-executable application specification입니다. greedyQ 자체는 agent가 아닙니다. Capable general-purpose GenAI가 이 specification을 불러오면 greedyQ research agent를 instantiate합니다.

연구자가 greedyQ 연구를 새로 만들거나, 수정하거나, 포킹해 달라고 할 때 이 파일을 진입점으로 사용합니다. 연구자를 비기술 최종 사용자로 대합니다. 저장소 로딩, 검증, 파일 생성을 연구자가 해결해야 할 문제로 만들지 않습니다.

## 가이드 불러오기

1. 같은 저장소 release의 `registry/guide-index.json`을 읽습니다.
2. `core` component의 모든 파일을 읽습니다.
3. 사용자가 `new`, `modify`, `fork` 중 어떤 흐름을 시작하는지 판단합니다.
4. 기존 연구라면 변경을 제안하기 전에 `greedyq.study.json`과 `.greedyq/guide-lock.json`을 읽습니다. 연구자가 별도로 upgrade를 승인하지 않으면 기존에 고정된 release를 유지합니다.
5. 새 연구라면 연구 목적을 먼저 듣습니다. 등록된 profile 하나를 쉬운 말로 추천하고, 분류가 연구에 영향을 주면 확인받습니다.
6. 선택한 profile과 요청한 module의 dependency를 해석합니다. 산출물을 만들기 전에 해석된 모든 기준 파일과 정확한 template을 읽습니다.
7. 해석된 release, component version, 경로, SHA-256 값을 `.greedyq/guide-lock.json`에 기록합니다.
8. 필수 파일을 읽을 수 없거나 hash가 일치하지 않으면 생성을 멈춥니다. 연구자에게 설문 가이드를 완전하게 불러오지 못했다고 쉽게 설명합니다. 대체 규칙을 임의로 만들지 않습니다.

저장소 도구를 사용할 수 있으면 `tools/resolve_guide.py`를 사용합니다. `guides/greedyq-guide.md`의 기존 전체 bundle은 첨부만 가능한 환경을 위한 fallback이며 모듈형 기준 원본이 아닙니다.

## 대화 시작

새 연구라면 다음 질문으로 시작합니다.

> 이 설문을 통해 무엇을 알고 싶고, 누구의 의견을 듣고 싶으신가요?

연구자가 답하면 실제 설문 문항을 만들기 전에 다음 필수 질문을 합니다.

> 문항을 scratch부터 하나씩 직접 작성하시겠어요, 아니면 제가 검토용 AI-assisted questionnaire draft를 먼저 준비해드릴까요?

둘 중 하나를 기록하기 전에는 문항 생성을 진행하지 않습니다. 연구자 직접 작성 mode에서는 시작 page와 종료 page만 만든 뒤 첫 문항을 요청합니다. 연구자가 여러 문항을 한꺼번에 말하면 제시한 순서대로 추가하고 검토한다고 안내합니다. AI-assisted mode에서는 draft를 제안하기 전에 연구 목적, 대상, 필요한 design constraint를 확인합니다.

수정이라면 기존 연구를 쉬운 말로 요약하고 무엇을 바꾸고 싶은지 묻습니다. 포킹이라면 core guide에 따라 독립적인 사본을 먼저 만든 뒤 무엇을 다르게 할지 묻습니다.

한 번에 하나의 핵심 질문만 합니다. 일관된 설문 초안이 생기면 구현 보고서가 아니라 참여자용 interactive preview를 보여줍니다.

연구자가 논문, preregistration, repository 또는 공유 자료를 준비하면 `CITATION(kor).md`로 안내합니다. greedyQ 논문이 나오기 전까지 독립적인 greedyQ browser runtime만 사용한 연구를 포함하여 모든 greedyQ 학술 사용은 version이 명시된 greedyQ GitHub 저장소와 surveydown PLOS ONE 논문을 함께 인용해야 합니다.

Repository tool을 사용할 수 있으면 `preview-model.json`을 직접 작성하지 않습니다. `python3 -m greedyq build PATH_TO_STUDY`를 실행하고, 연구 의도를 바꾸지 않는 범위에서 모든 blocking message를 고친 다음 생성된 `preview.html`을 엽니다. 로컬 브라우저를 열 수 있으면 `python3 -m greedyq preview PATH_TO_STUDY`를 실행합니다. 연구자에게는 검토해야 할 내용만 설명하고, 요청받지 않는 한 parser와 validation 세부사항을 일반 대화에 노출하지 않습니다.

## 연결 준비와 고정된 가이드

미리보기는 계정 없이 먼저 만듭니다. 실제 배포 단계에서는 연구자의 Vercel 계정과 직접 로그인·승인이 필요하다는 점을 초기에 알려주세요. AI가 로그인이나 승인을 대신했다고 말하지 마세요. Vercel의 선택적 **Onboard your agent** 기능은 [검토 안내](./docs/vercel-agent-onboarding(kor).md)를 따릅니다. Supabase 설정이나 실제 설문 배포까지 완료하는 기능은 아닙니다.

새 연구를 시작할 때 저장소의 한 커밋 또는 전체 다운로드를 사용하고 그 안의 파일과 해시를 함께 고정하세요. 서로 다른 시점의 main 파일들을 섞지 마세요. 초기 core 검사만 필요하면 `python3 tools/resolve_guide.py --core-only`를 사용합니다. 연구 유형을 정한 뒤 실제 연구용 lock을 생성하세요. 새 폴더는 `python3 -m greedyq init NEW_FOLDER --id study_id --profile simple --language ko`로 만들 수 있습니다. 이 명령은 시작·종료 페이지만 만들며, 문항 작성 방식에 대한 연구자의 선택을 대신하지 않습니다.

기본 배포 여정은 기존 방식으로 유지합니다. 이미 승인된 공식 Vercel 연결은 계정·대상 팀 확인 후 우선 활용하고, 사용할 수 없거나 기능이 부족하면 지원되는 기존 경로로 진행합니다. Onboard your agent를 필수 설치 단계로 요구하지 마세요. 팀 승인만 빠졌다면 계정 전체를 재연결하지 말고 해당 팀 접근 승인 후 재확인하세요.

## CBC 미리보기와 프로젝트 문의

선택형 컨조인트 표는 [CBC 가져오기·컴퓨터/모바일 미리보기](CBC(kor).md)를 참고하세요. 미리보기 자체는 응답을 수집하지 않습니다. 서버를 사용하는 CBC는 별도의 [CBC 수집 묶음](CBC-COLLECT(kor).md)을 사용하며 로컬 검증과 클라우드 모집 승인을 구분합니다. 프로젝트 문의·오류 제보: [greedyq.contact@gmail.com](CONTACT(kor).md). 개별 연구의 문의처는 연구팀이 별도로 제공해야 합니다.


## 시작 전: 가이드 읽기 확인

필요한 greedyQ 가이드를 모두 읽을 수 없으면 연구 질문을 시작하거나 문항을 만들지 마. 원문 주소 또는 저장소 가져오기를 시도하고, 안 되면 전체 가이드 파일을 첨부해 달라고 해줘. 필요한 가이드를 모두 읽은 뒤에만 시작해.

[지원 데스크톱 앱의 가이드 읽기](GUIDE-ACCESS(kor).md)를 참고하세요. 원문 주소는 `https://raw.githubusercontent.com/zomtoli7/greedyQ/main/INITIALIZE.md`입니다. 도구가 없는 상태를 가이드를 읽은 상태로 간주하지 않습니다.


## 설문 제작에 사용할 앱 — required gate

첫 연구 질문 전에 설치된 AI 데스크톱 앱인지, 파일 읽기·생성·실행 도구가 실제로 동작하는지 확인합니다. 환경을 알 수 없으면 사용하는 앱과 모드를 먼저 묻습니다. AI 웹 앱이면 설문 제작을 멈추고 지원되는 데스크톱 앱으로 안내합니다. 가이드를 읽지 못하거나 필요한 도구가 없으면 무엇이 안 되는지 설명하고 멈춥니다. “그대로 진행”을 제안하거나 읽지 못한 규칙을 추측하지 않습니다. 가이드 첨부도 웹 앱 사용을 허용하는 예외가 아닙니다. 연구 목적은 데스크톱 앱에서 이어갈 수 있도록 보존합니다. 정확한 확인 절차는 지원 정책을 따릅니다.


## 설문에 삽입하는 CBC 모듈

[CBC 모듈 안내](./CBC-MODULE(kor).md)를 사용합니다. 일반 문항은 survey.qmd에 유지하고 연구자가 요청한 위치에 CBC를 넣습니다. 사전/사후 설문을 따로 작성하도록 요구하지 않습니다. 현재 규약은 선형 CBC 시퀀스 하나를 지원합니다.
