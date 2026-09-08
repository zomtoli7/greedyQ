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

## 5. 참여자처럼 테스트하기

모든 설문에서 다음을 확인합니다.

- 필수 문항에 답하지 않고 진행해 봅니다.
- Previous와 Continue를 사용하고 새로고침 후 진행 상태가 이어지는지 봅니다.
- 응답 거부, 기타 및 자유응답 선택지를 시험합니다.
- 숨겨진 문항이 의도한 때에만 나타나는지 확인합니다.
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
