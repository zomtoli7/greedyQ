# greedyQ 사용자 설명서

[English](./USER-GUIDE.md)

> **Be greedy with your time. Just ask your AI to make your questionnaire.**

이 설명서는 비기술 연구자가 아이디어에서 시작해 컴퓨터와 모바일에서 직접 시험할 수 있는 설문을 만드는 과정까지 안내합니다. 실제 계정을 연결하거나 실제 참여자를 모집하기 전에 끝납니다.

## 필요한 것

- 공개 GitHub repository를 읽을 수 있는 GPT, Claude 또는 다른 capable AI
- 무엇을 알고 싶은지, 누구의 의견을 듣고 싶은지에 대한 짧은 설명
- 질문에 답하고 결과를 직접 시험할 시간

프로그래밍, Markdown, database 또는 deployment tool을 알 필요가 없습니다.

## 1. AI에게 greedyQ 알려주기

[greedyQ 시작 페이지](./START-HERE(kor).md)를 열거나 AI에게 다음 URL을 줍니다.

```text
https://github.com/zomtoli7/greedyQ/blob/main/START-HERE.md
```

AI는 이 파일과 같은 repository에 연결된 파일들을 읽어야 합니다. Guide와 template을 하나씩 모두 첨부할 필요는 없습니다.

## 2. 시작 방식 선택하기

### 새 설문 만들기

다음 메시지를 복사합니다.

```text
다음 주소의 현재 greedyQ 지침을 읽고 따라줘:
https://github.com/zomtoli7/greedyQ/blob/main/START-HERE.md

새로운 greedyQ 연구를 만들어줘. 나를 비기술 연구자로 대하고 한 번에 하나의 핵심 질문만 하면서 실제로 작동하는 컴퓨터·모바일 preview까지 안내해줘.

알고 싶은 것: [연구 질문]
의견을 듣고 싶은 사람: [대상 참여자]
```

### 기존 설문 수정하기

AI가 기존 greedyQ study folder에 접근할 수 있게 한 다음 복사합니다.

```text
다음 주소의 현재 greedyQ 지침을 읽고 따라줘:
https://github.com/zomtoli7/greedyQ/blob/main/START-HERE.md

이것은 기존 greedyQ 연구야. 쉬운 말로 요약하고 수정을 도와줘. 내가 upgrade를 승인하지 않으면 기존 기록과 현재 greedyQ version을 유지해줘. 한 번에 하나의 핵심 질문만 해줘.

바꾸고 싶은 것: [변경 내용]
```

수정은 원본 연구를 변경합니다. 결과를 받아들이기 전에 쉬운 말로 된 변경 요약을 요청하십시오.

### 기존 설문 포크하기

AI가 기존 study folder에 접근할 수 있게 한 다음 복사합니다.

```text
다음 주소의 현재 greedyQ 지침을 읽고 따라줘:
https://github.com/zomtoli7/greedyQ/blob/main/START-HERE.md

이 greedyQ 연구를 포크해줘. 원본은 보존하고 새로운 study identity를 가진 독립적인 사본을 만든 다음 사본만 수정하도록 도와줘. 한 번에 하나의 핵심 질문만 해줘.

새 버전에서 바꾸고 싶은 것: [변경 내용]
```

AI가 별도 사본을 만들었고 원본을 덮어쓰지 않았는지 확인합니다.

## 3. 안내 대화 진행하기

AI는 software engineer가 아니라 research assistant처럼 대화해야 합니다. 연구 목적, 대상 참여자, 설계, 주요 결과, 모집, 문항, 설문 흐름, consent와 privacy, 분석 및 preregistration을 차례로 질문합니다.

무엇을 알아보고 누구에게 물을지 설명하면 AI는 곧바로 문항 작성 방식을 반드시 물어야 합니다.

- **Scratch부터 직접 작성:** AI는 처음에 시작 page와 종료 page만 만들고 첫 문항을 요청합니다. 한 문항 또는 여러 문항을 한꺼번에 줄 수 있으며, 여러 문항은 말한 순서대로 추가하고 검토합니다.
- **AI에게 draft 준비 요청:** AI가 목적, 대상, 필수 design choice를 확인한 뒤 전체 초안을 제안합니다. 중요한 연구 결정의 최종 승인은 여전히 연구자가 합니다.

AI가 문항을 만들 수 있다는 이유만으로 두 번째 방식을 몰래 선택하면 안 됩니다.

대화 초반에는 설문 위쪽에 참여자에게 보일 이름도 묻습니다. 회사, 학교, 연구실 또는 연구팀 이름 등을 사용할 수 있습니다. 이 값은 `greedyq.organization`에 저장되며 나중에 바꿀 수 있습니다.

“아직 결정하지 않았다”고 답해도 됩니다. AI는 답을 지어내지 않고 미결정 사항으로 기록해야 합니다.

연구 목적과 전체 설계가 분명해지면 상세 IRB 및 consent 작업을 지금 할지 첫 설문 초안 이후에 할지 선택합니다. 세부 작업은 미룰 수 있지만 deployment 전에는 생략할 수 없습니다.

AI가 문항이나 연구설계의 문제를 발견할 수 있습니다. 문제와 선택지를 설명해야 하지만 중요한 연구 결정을 바꾸기 전에는 연구자에게 물어야 합니다.

## 4. Interactive preview 받기

일관된 설문이 만들어지면 AI가 survey를 생성하고 참여자용 preview를 보여줘야 합니다. `study.md`나 기술 보고서만 준다면 다음 메시지를 복사합니다.

```text
greedyQ preview checkpoint를 따라줘. 컴퓨터와 모바일 화면이 모두 있는 실제 interactive respondent-facing preview를 보여줘. 구현 보고서를 주된 검토 화면으로 사용하지 마.
```

Study folder에는 최소한 다음 파일이 있어야 합니다.

```text
survey.qmd
greedyq.yml
index.html
preview.html
studio.html
greedyq-core.js
greedyq-runtime.css
```

AI가 preview를 열거나 interactive artifact를 보여주거나 다운로드할 folder를 제공할 수 있습니다. Folder를 받았다면 파일을 함께 유지하고 modern browser에서 `preview.html`을 엽니다.

Preview mode는 컴퓨터와 모바일 화면을 보여주며 가상 참여자를 사용하고 test response를 local에만 보관합니다. 외부 service로 응답을 보내면 안 됩니다.

지원되는 모든 컨트롤을 한곳에서 확인하려면 [온라인 컨트롤 갤러리](https://zomtoli7.github.io/greedyQ/examples/control-gallery/preview.html)를 여세요. Surveydown-compatible 문항 16종, 숫자 슬라이더 두 형식, responsive matrix, navigation policy, advanced 및 custom-base 예제를 포함한 모든 고정 greedyQ extension을 담고 있습니다. 웹 게시가 아직 끝나지 않았다면 저장소의 [`examples/control-gallery/`](./examples/control-gallery/) 사본을 사용할 수 있습니다.

프리뷰 상단의 **스트럭처 보기(View structure)**를 누르면 설문을 처음부터 클릭하지 않고도 전체 구성을 확인할 수 있습니다. 읽기 전용 개요에서 응답자가 보게 될 페이지 순서, `T`로 표시된 안내문, `Q`로 표시된 문항, 문항 ID와 컨트롤 종류를 보여줍니다. 이 화면은 설문을 변경하거나 응답을 저장하지 않습니다.

## 5. 참여자처럼 테스트하기

모든 설문에서 다음을 확인합니다.

- 필수 문항에 답하지 않고 진행해 봅니다.
- Previous와 Continue를 사용하고 새로고침 후 진행 상태가 이어지는지 봅니다.
- 응답 거부, 기타 및 자유응답 선택지를 시험합니다.
- 숨겨진 문항이 의도한 때에만 나타나는지 확인합니다.
- 핸드폰에서 matrix가 row card와 2개 또는 3개 column group을 사용하며 horizontal page scroll을 만들지 않는지 확인합니다.
- 모든 audio 또는 video stimulus를 재생하고 caption과 transcript를 확인합니다.
- 선언된 숨김, 비활성화 또는 지연 navigation action을 모두 확인합니다.
- 해당되는 완료, consent 거부, 선별 탈락 및 철회 경로를 시험합니다.
- 컴퓨터와 모바일 화면을 읽고 누르기 쉬운지 확인합니다.
- Test-state에 저장된 값이 선택한 답과 일치하는지 확인합니다.

실험 연구에서는 모든 condition을 시험합니다. 의도한 condition에서만 treatment가 나타나는지, 의도한 시점에 배정되는지, 뒤로 가거나 새로고침해도 배정 condition이 바뀌지 않는지 확인합니다.

“모바일에서 선택지를 읽기 어렵다” 또는 “consent에서 No를 선택하면 거부 종료 화면으로 가야 한다”처럼 평범한 말로 문제를 설명하면 됩니다.

## 6. 수정하고 승인하기

Feedback을 준 다음 복사합니다.

```text
다른 연구 결정은 바꾸지 말고 이 변경을 반영해줘. 설문을 다시 build하고 validate한 다음 업데이트된 컴퓨터·모바일 preview와 무엇이 바뀌었는지에 대한 짧고 쉬운 요약을 보여줘.
```

설문을 직접 끝까지 사용해 보고 만족할 때까지 반복합니다. Validation 통과만으로는 연구자의 승인이 아닙니다.

준비되면 다음과 같이 말합니다.

```text
내가 컴퓨터와 모바일 preview를 직접 테스트했고 이 questionnaire version을 승인한다. 승인을 기록하되 아직 외부 계정을 연결하거나 preregistration을 제출하거나 deploy하거나 participant를 모집하지 마.
```

## 그다음 단계

Preview 승인 후 greedyQ는 preregistration draft, Vercel-ready survey, Supabase setup file, Prolific setting, native surveydown export를 준비할 수 있습니다. Account 연결, 제출, deployment 및 모집에는 각각 별도 승인과 외부 검증이 필요합니다. [외부 연결 준비 상태](./docs/external-connection-readiness(kor).md)에서 계속하십시오.

## 연구에 사용한 software 인용하기

연구가 논문, preprint, 학위논문 또는 보고서로 공개된다면 설문이 greedyQ의 독립 browser runtime에서만 실행되었더라도 greedyQ와 surveydown을 모두 인용하십시오. `survey.qmd`의 `greedyq.version`에 저장된 정확한 release identifier를 사용해야 합니다. 복사해서 사용할 수 있는 reference와 정확한 연구방법 문구는 [CITATION(kor).md](./CITATION(kor).md)를 참고하십시오.

첫 test database를 만들 준비가 되면 [Supabase 프로젝트 연결하기](./SUPABASE-SETUP(kor).md)를 따르세요. 이 단계는 Vercel deployment와 실제 participant 모집 전에 멈춥니다.

## 7. 한 번 연결하고 두 개의 링크 받기

정상 배포 흐름에서는 연구자가 Supabase를 직접 다루지 않습니다. Vercel에 로그인하고 Vercel 안에서 제시되는 Supabase 리소스를 승인한 뒤, 연결된 AI agent가 설정을 끝내도록 합니다. AI는 데이터베이스 migration 설치, 환경변수 연결, 공개 설문 배포, Vercel 로그인으로 보호되는 결과 화면 배포, 두 링크 검증을 수행해야 합니다.

완료 메시지에는 참가자에게 공유할 **설문 링크**와 Vercel 팀에서 승인된 연구자가 사용할 **결과 링크**가 있어야 합니다. 데이터베이스 키 복사, SQL 붙여넣기, Supabase 테이블 찾기, 환경변수 수동 연결은 정상 사용자 절차가 아니라 복구 절차입니다.

## 8. 대시보드에서 테스트 응답 확인하기

결과 링크는 모든 테스트 제출을 제외하는 **실제 응답**으로 열립니다. **테스트 응답**을 선택하고 **유입 경로**를 **Direct**로 둔 뒤 일반 테스트 설문을 한 번 제출합니다. **새로 고침**을 눌러 건수, 현재 페이지 분포, 응답 요약, 응답 표가 바뀌었는지 확인합니다.

Prolific 테스트에서는 **테스트 응답**을 유지하고 **유입 경로**를 **Prolific**으로 바꿉니다. 유효한 패널 식별자가 있어도 테스트가 분석 응답으로 바뀌면 안 됩니다.

| 모드 | 유입 경로 | 용도 |
| --- | --- | --- |
| 테스트 | Direct | 연결된 DB를 사용하는 일반 테스트 |
| 테스트 | Prolific | 패널 링크와 식별자 테스트 |
| 실제 | Direct | 패널 없이 공개 모집 |
| 실제 | Prolific | 실제 Prolific 모집 |

**CSV 다운로드**에는 화면의 필터가 그대로 적용됩니다. 현재 응답자가 답하지 않은 문항도 모든 설문 변수의 열은 유지되고 미응답 값만 빈 칸으로 남습니다. Matrix 행과 advanced structured control은 안정적인 분석 열로 펼쳐지고 **변수 안내**에서 열 이름의 의미를 확인할 수 있습니다. 자세한 내용은 [결과 대시보드 설명서](./RESULTS-DASHBOARD(kor).md)를 보십시오.

## 자주 생기는 문제

- **AI가 GitHub를 읽지 못함:** [전체 fallback guide](./guides/greedyq-guide.md)를 다운로드해 파일 하나만 첨부하고 시작 메시지를 반복합니다.
- **AI가 너무 기술적으로 말함:** “greedyQ communication rule을 따라줘. 나를 비기술 연구자로 대하고 한 번에 하나의 핵심 질문만 해줘”라고 말합니다.
- **AI가 결정을 지어냄:** “그 결정을 미결정으로 표시하고 마지막으로 확인한 design을 복구한 다음 결정하기 전에 내게 물어봐”라고 말합니다.
- **Preview가 열리지 않음:** `preview.html`, `greedyq-core.js`, `greedyq-runtime.css`를 함께 두고 AI에게 browser bundle을 다시 만들고 local에서 검증하도록 요청합니다.
- **AI가 참여자 모집을 시작해도 된다고 함:** 작동하는 preview는 deployment나 fielding 승인이 아닙니다. 남은 consent, preregistration, connection, security 및 production test checkpoint를 요청합니다.

## 최종 체크리스트

- [ ] 새로 만들기, 수정하기 또는 포크하기 중 하나를 선택했다.
- [ ] AI가 현재 greedyQ repository 지침을 불러왔다.
- [ ] 중요한 연구 결정을 직접 확인했고 미결정 사항이 보이게 남아 있다.
- [ ] Consent 및 privacy 결정을 검토했다.
- [ ] 컴퓨터, 모바일 및 중요한 모든 경로와 condition을 직접 시험했다.
- [ ] 정확한 questionnaire version을 승인했다.
- [ ] 별도 승인 없이 외부 계정을 연결하거나 participant를 모집하지 않았다.

## 문항 컨트롤 안내

코드 이름을 외울 필요는 없습니다. 연구자가 평소 쓰는 말로 필요한 응답 방식을 설명하면 됩니다.

| 필요한 응답 | greedyQ 컨트롤 | 적합한 용도 |
| --- | --- | --- |
| 짧은 주관식 | `text` | 코드, 짧은 명칭, 한 줄 응답 |
| 긴 주관식 | `textarea` | 의견과 설명 |
| 숫자 | `numeric` | 나이, 수량, 비율, 금액 |
| 하나만 선택 | `mc` | 서로 겹치지 않는 범주 |
| 여러 개 선택 | `mc_multiple` | 복수 응답 문항 |
| 하나의 버튼 선택 | `mc_buttons` | 짧고 행동 중심인 선택지 |
| 여러 버튼 선택 | `mc_multiple_buttons` | 간결한 복수 선택지 |
| 이미지 하나 선택 | `mc_image` | 시각 자극 또는 이미지 범주 |
| 이미지 여러 개 선택 | `mc_multiple_image` | 복수의 시각 항목 선택 |
| 드롭다운 | `select` | 선택지가 긴 범주 목록 |
| 이름이 붙은 슬라이더 | `slider` | 순서가 있는 명목 척도 |
| 숫자 슬라이더 또는 범위 | `slider_numeric` | 하나의 값 또는 상·하한 범위 |
| 날짜 하나 | `date` | 특정 날짜 |
| 날짜 범위 | `daterange` | 시작일과 종료일 |
| 각 행에서 하나씩 선택 | `matrix` | 일반적인 평정 행렬 |
| 각 행에서 여러 개 선택 | `matrix_multiple` | 행×열 복수 선택 행렬 |
| 오디오 자극 재생 | `audio` | Caption과 transcript를 넣을 수 있는 소리 자극 |
| 비디오 자극 재생 | `video` | Poster, caption, transcript를 넣을 수 있는 영상 자극 |
| 선호 순서 정하기 | `rank_order` | 항목 전체의 순위 |
| 여러 버전을 나란히 평가 | `side_by_side` | 같은 항목과 척도를 공유하는 여러 표 |
| 추천 의향 질문 | `nps` | 표준 0–10 추천 의향 척도 |
| 페이지 체류시간 기록 | `timing` | 화면에 보이지 않는 초 단위 기록 |
| 고정 합계 배분 | `constant_sum` | 예산, 시간, 비율 배분 |
| 그룹으로 나누고 순위 정하기 | `pick_group_rank` | 범주화 후 그룹 안 우선순위 |
| 계층을 좁혀 선택 | `drill_down` | 지역–국가–도시 같은 경로 |
| 합의된 특수 interaction | `custom` | 지원되는 base control을 신중하게 확장 |

매트릭스 문항은 desktop에서 일반 설문 도구의 표 형태를 사용합니다. 진술문은 행에, 응답 선택지는 열 제목에, 라디오 버튼이나 체크박스는 각 셀에 배치됩니다. 핸드폰에서는 진술문마다 별도 card를 만들고 응답 선택지를 순서대로 2개 또는 3개 column group으로 표시하여 horizontal page scroll을 피합니다.

`audio`와 `video`는 surveydown의 독립 built-in question type이 아니라 안전한 greedyQ extension입니다. 검증된 local 또는 HTTPS media를 받고 기본적으로 browser playback control을 사용하며 response variable은 만들지 않습니다. 연구 자료가 허용하면 caption과 transcript를 함께 요청하십시오.

Page의 Previous와 Next는 표시, 숨김 또는 눈에 보이는 비활성화 상태로 설정할 수 있습니다. 승인된 연구설계에 최소 stimulus 노출 시간이 있다면 Next를 지정한 시간 동안 비활성화하고 남은 시간을 표시할 수도 있습니다. 단순히 required answer가 비었다는 이유로 Next를 미리 비활성화하지는 않으며, 눌렀을 때 필요한 응답을 설명합니다.

항상 지원 control을 우선합니다. 맞는 control이 없으면 AI는 custom control에 시간과 AI usage가 더 들 수 있음을 먼저 안내하고 모양, interaction, validation, mobile behavior, accessibility, 저장 결과가 모두 확정될 때까지 핵심 질문을 합니다. 연구자가 요약을 확인한 뒤에만 가장 가까운 base control을 재사용하여 구현합니다.

## 복사해서 쓰는 프롬프트 예제

아래 예제는 그대로 복사한 뒤 대괄호 안만 바꾸면 됩니다. 모든 작업의 시작에는 AI에게 `START-HERE.md`를 따르라고 요청하세요.

### 만족도 설문

```text
우리 서비스를 한 번 이상 사용한 사람을 위한 짧은 만족도 설문을 만들어줘. 전반적 만족도, 사용 편의성, 유용성, 결과물 품질, 재사용 의향, 개선점 하나를 물어봐. 3분 안에 끝나게 하고 배포 전에 실제 인터랙티브 프리뷰를 보여줘.
```

### 참여 대상 분기

```text
서비스를 사용해 본 사람만 계속할 수 있게 해줘. 명확한 대상 확인 문항 하나를 넣고, 아니오를 고르면 이전 버튼이 없는 정중한 참여 제외 화면으로 보내줘. 데스크톱과 모바일에서 이 경로를 보여줘.
```

### 일반 매트릭스

```text
사용 편의성, 속도, 안정성, 설명의 명확성을 평가하는 매트릭스를 추가해줘. 열은 매우 나쁨, 나쁨, 보통, 좋음, 매우 좋음으로 하고 각 행에서 하나를 반드시 선택하게 해줘. 데스크톱에서는 일반 표로, 모바일에서는 가로 스크롤 없는 별도 row card로 보여줘.
```

### 복수 선택 매트릭스

```text
제품 범주마다 어디에서 구매했는지 물어봐. 제품 범주는 행에, 오프라인 매장·온라인·모바일 앱은 열에 두고 각 행에서 여러 개를 고를 수 있게 해줘.
```

### 오디오와 비디오 자극 추가

```text
일반 재생 컨트롤, 짧은 caption, transcript가 있는 audio stimulus를 넣고 그다음에는 poster image와 transcript가 있는 video stimulus를 넣어줘. 검증된 project file이나 HTTPS URL만 사용하고 둘 다 자동 재생하지 마. 재생 자체를 survey response로 취급하지 마.
```

### Previous와 Next 동작 지정

```text
Consent page에서는 Previous를 숨기고 questionnaire page에서는 정상 표시하며 마지막 review page에서는 눈에 보이지만 비활성화해줘. Stimulus page의 Continue는 12초 동안 비활성화하고 남은 시간을 보여줘. Desktop과 mobile preview에서 모든 상태를 보여줘.
```

### Advanced control 사용

```text
응답자가 다섯 가지 우선순위의 순위를 정하고, 세 활동에 정확히 100점을 배분한 다음, 지역·국가·도시 drill-down으로 도시를 고르게 해줘. 문항을 승인하기 전에 저장되는 데이터 형태를 설명하고 desktop과 mobile 동작을 보여줘.
```

### Custom control 요청

```text
제품 카드 형태의 custom control이 필요할 수 있어. 코드를 만들기 전에 추가 시간과 AI usage를 안내하고 가장 가까운 기존 greedyQ control을 찾아줘. 모양, 선택 방식, validation, mobile layout, accessibility, export value를 한 번에 하나씩 물어봐. 합의 내용을 요약하고 내 확인을 받은 뒤에만 구현해줘.
```

### 문항 품질 점검

```text
두 가지를 한꺼번에 묻는 문항, 유도 문구, 불균형한 척도, 겹치는 선택지, 빠진 응답 거부 선택지, 잘못된 분기를 점검해줘. 각 문제를 쉬운 말로 설명하고 연구적으로 중요한 변경은 반드시 내게 확인받아.
```

### 동의서 작업 미루기

```text
먼저 설문과 프리뷰를 만들어줘. IRB, 동의 문구, 데이터 보관 기간, 철회 방식은 미결정 사항으로 기록해. 선택 사항처럼 취급하지 말고 실제 배포 전에 반드시 다시 확인해줘.
```

### 랜덤화 실험

```text
두 조건의 무작위 실험을 만들어줘. 처치, 통제, 배정 시점, 주 결과변수, 조작 점검, 제외 기준, 분석에 대해 한 번에 하나씩 질문해줘. 중요한 결정을 추측하지 말고 모든 조건을 프리뷰할 수 있게 해줘.
```

### 모든 경로 시험

```text
가상 참가자로 도달 가능한 모든 경로를 시험해줘. 필수 응답, 이전·다음, 새로고침 후 재개, 참여 제외, 동의 거부, 완료, 철회를 확인해. 문제를 쉬운 말로 보고하고 구현 오류는 고친 뒤 다시 시험해줘.
```

### 구조와 모바일 확인

```text
프리뷰와 스트럭처 보기를 열어 페이지 순서, 안내문, 문항 ID, 컨트롤 종류, 종료 페이지를 설명해줘. 390픽셀 모바일에서 터치 영역, 대비, 빈 스크롤, 상단 이동, image와 media 크기, matrix row card에 horizontal page scroll이 없는지도 시험해줘.
```

### 한 부분만 수정

```text
[문항 ID 또는 정확한 문구]의 문구만 바꿔줘. 저장 값, 분기, 무작위 배정과 다른 모든 연구 결정은 유지해. 다시 빌드한 뒤 전후 차이와 수정된 프리뷰를 보여줘.
```

### 안전하게 포크

```text
이 연구를 [새 이름]이라는 독립 사본으로 포크해줘. 새 연구 ID를 부여하고 원본 폴더를 보존하며 배포 식별자와 참가자 데이터는 초기화해. 새 사본에 속하는 항목을 정확히 알려줘.
```

### 사전등록 초안

```text
내가 승인한 결정만 사용해서 사전등록 문서를 작성해줘. 가설, 제외 기준, 표본 크기, 종료 규칙, 결과변수, 분석에서 미결정인 부분을 표시해. 빠진 결정을 추측하거나 이미 등록되었다고 말하지 마.
```

### 외부 연결 전 준비

```text
Vercel, Supabase, Prolific 연결 전 체크리스트를 준비해줘. 로컬 시험은 가상 응답과 가상 무작위 배정을 사용해. 내가 별도로 승인하기 전에는 로그인, 인증정보 생성, 배포, 모집을 하지 마.
```

### 다운로드 묶음

```text
설계 대화는 여기에서 멈춰. 현재 연구를 검증하고 다시 빌드한 뒤 설문 원본, 설정, 데스크톱·모바일 프리뷰, 스트럭처 보기, 결정 기록, 검증 보고서를 ZIP으로 묶어줘. 실제 조사 전에 남은 결정을 알려줘.
```
