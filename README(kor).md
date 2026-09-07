# greedyQ

[English](./README.md)

> **Be greedy with your time. Just ask your AI to make your questionnaire.**

greedyQ는 online academic research를 위한 specification-driven, AI-native application입니다. Application 자체를 conventional source code로 구현하는 대신, greedyQ는 general-purpose generative AI agent가 application을 어떻게 instantiate하고 operate해야 하는지 명시합니다.

Portable Markdown, schema, checkpoint, exact template의 묶음이 **agent-executable application specification**을 이룹니다. 연구자는 GPT, Claude 등의 유능한 범용 AI에게 버전이 명시된 greedyQ 저장소를 알려주고 “설문 만들자!”와 같은 일상적인 요청으로 시작합니다. 그렇게 instantiate된 research agent는 안내형 연구 workflow를 수행하고 연구설계 artifact와 실행 가능한 respondent-facing survey software를 함께 만듭니다.

## AI-native application으로서의 greedyQ

greedyQ 자체는 agent가 아닙니다. 둘의 관계는 다음과 같습니다.

```text
greedyQ agent-executable application specification
                         +
              capable host GenAI
                         =
             greedyQ research agent
                         |
                         v
       research-design artifacts + survey application
```

Architecture는 세 층으로 구성됩니다.

1. **Architecture — specification-driven AI-native application.** Application behavior는 conventional application codebase만으로 구현되지 않고, 사람이 읽을 수 있으며 agent가 실행할 수 있는 specification을 중심으로 정의·배포됩니다.
2. **Domain — online academic research.** 범위는 survey에 한정되지 않고 연구설계, consent, questionnaire, experiment, randomization, respondent panel, data plan, preregistration, deployment, fielding을 포함합니다.
3. **Implementation — greedyQ.** greedyQ는 이 architecture를 재현 가능한 online academic research에 적용한 concrete application입니다.

Host model은 서로 다른 interface나 native capability를 사용할 수 있지만 같은 normative research specification을 적용해야 합니다. 따라서 portability란 GPT, Claude, Gemini 또는 다른 유능한 범용 AI가 greedyQ를 instantiate하면서 공통 conformance requirement로 검증 가능하다는 뜻입니다.

AI는 연구 reasoning과 자연어 협업을 제공합니다. greedyQ specification은 interview protocol, 승인 checkpoint, artifact contract, validation requirement, preregistration workflow, runtime template, deployment contract, reproducibility boundary를 제공합니다.

## 왜 greedyQ인가?

상용 설문 플랫폼은 비용이 높고, 정확한 재현이 어려우며, 복잡한 실험 설계에 제약이 있을 수 있습니다. surveydown은 훌륭한 survey-as-code 모델을 제공하지만 R, Quarto, Shiny 도구 체인이 연구자의 진입 장벽이 될 수 있습니다.

greedyQ는 다음 장점을 유지합니다.

- 사람이 읽을 수 있는 설문 정의
- Git 기반 버전 관리와 재현성
- 연구자가 소유하는 PostgreSQL 데이터
- 프로그래밍 가능한 연구 워크플로

자체 TypeScript 및 React runtime을 GitHub, Vercel, Supabase에 맞춰 제공하고, 이 결정론적 스택을 안내형 AI 대화로 사용할 수 있게 합니다. 또한 제한 없는 R, Shiny, Quarto 사용자 정의가 필요한 연구자를 위한 핵심 escape hatch로 `app.R`과 관련 native surveydown artifact를 생성합니다.

## 제품 원칙

- `survey.qmd`가 설문 콘텐츠와 문항의 source of truth입니다.
- 사용자 대상 QMD 문법은 가능한 범위에서 surveydown과 호환되어야 합니다.
- Vercel/Supabase runtime이 주 실행 대상입니다.
- 생성된 `app.R`을 포함하는 native surveydown export는 핵심 출력 경로입니다.
- 호환성은 공개 문서를 바탕으로 독립 구현하며 surveydown 소스 코드를 포함하지 않습니다.
- 임의의 R 및 Shiny 코드를 실행하지 않습니다.
- 조건 로직과 무작위화는 선언적이고 안전하며 재현 가능해야 합니다.
- 연구자가 응답 데이터를 소유하고 통제합니다.
- GUI 설문 빌더를 요구하지 않습니다.
- 주요 사용자 경험은 범용 LLM과의 안내형 대화입니다.
- LLM은 연구 지능을 제공하고, greedyQ는 workflow, specification, validation, reproducibility를 제공합니다.
- 중요한 연구 결정에는 연구자의 명시적 확인이 필요합니다.
- Fielding-ready study는 sample collection 시작 전에 검토 가능한 preregistration package를 생성해야 합니다.
- Workflow는 연결 도구로 직접 작업할 수 있는지, 사용자에게 파일과 지침을 제공해야 하는지 감지해야 합니다.

## 주요 workflow

```text
Versioned greedyQ repository + 연구자의 연구 아이디어
                         |
                         v
                 안내형 AI 인터뷰
                         |
     연구 설계 -> consent -> questions
     -> logic -> randomization -> analysis plan
                         |
                         v
 survey files + preregistration package + assets
                         |
                         v
           parser -> Survey AST -> validator
                    /             \
                   v               v
        preview 및 승인       native export
              |              survey.qmd + app.R
              v
     GitHub -> Vercel -> Supabase
```

목표로 하는 온보딩 경험은 다음과 같습니다.

1. Tag가 지정된 greedyQ `START-HERE.md` URL을 유능한 LLM 또는 repository agent에게 공유합니다. Repository link를 읽을 수 없을 때만 자체 포함 bundle을 사용합니다.
2. 만들고 싶은 연구를 말합니다.
3. 한 번에 하나씩 제시되는 질문에 답하고 중요한 결정을 확인합니다.
4. 생성된 연구, consent, logic, randomization, data plan, preregistration draft를 검토합니다.
5. 생성된 프로젝트를 validate하고 preview합니다.
6. Preregistration package를 명시적으로 승인하고 fielding 전에 직접 제출하거나 권한 있는 연결 agent를 통해 제출합니다.
7. 연결된 agent가 GitHub, Vercel, Supabase를 설정하게 하거나 생성된 handoff 안내를 따릅니다.
8. Web-native 설문을 승인·공개하고, 필요하면 native surveydown 프로젝트를 export합니다.

## Interaction mode 및 대안 경로

Guide는 capability에 따라 두 mode를 지원합니다.

- **Chat mode:** AI가 인터뷰하고 프로젝트 파일을 만들며 guide에 따라 reasoning을 검증하고 사용자에게 배포 방법을 안내합니다.
- **Agent mode:** 연결된 agent가 추가로 repository 편집, validation 실행, 서비스 설정, 배포, live survey 검증까지 수행합니다.

Expert user는 계속 `survey.qmd`와 `greedyq.yml`을 직접 작성할 수 있습니다. 제한 없는 R, Shiny, Quarto 사용자 정의가 필요한 연구자는 생성된 native surveydown 프로젝트에서 작업을 이어갈 수 있습니다. 향후 PPTX importer는 기존 slide 기반 초안을 편집 가능한 study artifact로 바꾸고 동일한 안내형 review workflow에 넣습니다.

## surveydown과의 관계

greedyQ는 문서화된 surveydown-style `survey.qmd` 문법의 일부를 지원하는 독립 구현입니다. surveydown 소스 코드를 포함하지 않으며 surveydown 프로젝트 또는 maintainer와 제휴하거나 이들의 보증을 받지 않습니다. 호환성이 greedyQ native 기능을 제한하지 않으며, 각 기능은 직접 이동 가능, `app.R`로 생성 가능, 또는 명시적인 export diagnostic이 있는 greedyQ-only로 분류합니다. 출처 및 라이선스 정보는 [NOTICE(kor).md](./NOTICE(kor).md)를 참고하십시오.

## 프로젝트 상태

greedyQ는 현재 specification 및 prototyping 단계입니다. Repository-first modular guide architecture가 호환 구조로 준비되었으며, 다음 milestone은 v0.2 parser와 runtime contract를 완성하는 동안 여러 LLM에서 behavioral evaluation을 수행하는 것입니다.

현재 방향은 [START-HERE(kor).md](./START-HERE(kor).md), [연구 framing](./docs/research-framing(kor).md), [AI guide](./guides/README(kor).md), [모듈형 guide architecture](./docs/modular-guide-architecture(kor).md), [제품 개요](./docs/product-brief(kor).md), [greedyQ v0.2 스펙](./docs/greedyq-v0.2-spec(kor).md), [골든 레퍼런스 연구](./examples/README(kor).md), [surveydown 호환성 조사](./docs/surveydown-compatibility(kor).md), [로드맵](./docs/roadmap(kor).md)을 참고하십시오.

## 문서 정책

영문 Markdown 파일이 source of truth입니다. 모든 Markdown 문서에는 파일명이 `(kor).md`로 끝나는 동기화된 한국어 사본을 둡니다. 코드, 식별자, 경로, 설정 키, 규범적 문법은 번역하지 않습니다.

## 라이선스

greedyQ는 [MIT License](./LICENSE)로 배포합니다.
