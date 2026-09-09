# greedyQ

[English](./README.md)

- **현재 specification:** `0.2`
- **현재 release:** `0.2_2026-09-09_2f20a8c`
- **Release source commit:** [`3aefdd0`](https://github.com/zomtoli7/greedyQ/commit/5ce7a3a) · [업데이트 히스토리](./updates/README(kor).md)

[설문 시작](./START-HERE(kor).md) · [사용자 가이드](./USER-GUIDE(kor).md) · [결과 대시보드](./RESULTS-DASHBOARD(kor).md) · [컨트롤 갤러리](https://zomtoli7.github.io/greedyQ/examples/control-gallery/preview.html)

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

자체 browser-native JavaScript runtime을 GitHub, Vercel, Supabase에 맞춰 제공하고, 이 결정론적 스택을 안내형 AI 대화로 사용할 수 있게 합니다. 또한 제한 없는 R, Shiny, Quarto 사용자 정의가 필요한 연구자를 위한 핵심 escape hatch로 `app.R`과 관련 native surveydown artifact를 생성합니다.

## 제품 원칙

- `survey.qmd`가 설문 콘텐츠와 문항의 source of truth입니다.
- 사용자 대상 QMD 문법은 가능한 범위에서 surveydown과 호환되어야 합니다.
- Vercel/Supabase runtime이 주 실행 대상입니다.
- 최종 사용자용 parser, validator, preview, renderer는 Python이나 Node.js 없이 modern browser에서 실행됩니다.
- Third-party Python package가 필요 없는 Python 구현으로 개발 과정의 reference semantics를 먼저 확립하고 conformance test 및 개발 도구로 유지합니다.
- Python과 JavaScript 구현은 동일 fixture를 통과하고 normalized AST, diagnostic, rendering behavior가 의미론적으로 일치해야 합니다.
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

비기술 사용자를 위한 단계별 안내는 [greedyQ 사용자 설명서](./USER-GUIDE(kor).md)에서 시작하십시오.

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

greedyQ는 surveydown-style `survey.qmd` 문법의 독립 구현입니다. v0.2 browser runtime은 현재 공식 question-types documentation의 control 16종을 모두 구현하고 안전한 `audio`와 `video` stimulus를 greedyQ extension으로 추가하며, 나머지 문법은 compatibility level을 명시적으로 구분합니다. surveydown 소스 코드를 포함하지 않으며 surveydown 프로젝트 또는 maintainer와 제휴하거나 이들의 보증을 받지 않습니다. 호환성이 greedyQ native 기능을 제한하지 않으며, 각 기능은 직접 이동 가능, `app.R`로 생성 가능, 또는 명시적인 export diagnostic이 있는 greedyQ-only로 분류합니다. 출처 및 라이선스 정보는 [NOTICE(kor).md](./NOTICE(kor).md)를 참고하십시오.

## 인용

greedyQ 논문이 나오기 전까지 greedyQ를 사용한 학술 연구는 `survey.qmd`에 기록된 정확한 release identifier와 함께 [greedyQ GitHub 저장소](https://github.com/zomtoli7/greedyQ)를 인용하고, [surveydown PLOS ONE 논문](https://doi.org/10.1371/journal.pone.0331002)도 함께 인용해야 합니다. 이 정책은 독립적인 greedyQ browser runtime만 사용한 경우에도 적용됩니다. 복사해서 사용할 수 있는 reference와 연구방법 문구는 [CITATION(kor).md](./CITATION(kor).md)에 있습니다.

## 프로젝트 상태

greedyQ에는 이제 계정 없이 검증할 수 있는 connection-ready v0.2 runtime candidate가 있습니다. 고정 JavaScript core가 지원 QMD/YAML 문법을 parse·validate·compile하고 공식 surveydown question control을 adaptive desktop/mobile respondent view에 모두 render하며 mock persistence/assignment를 사용하는 동시 preview를 제공합니다. Golden study, 전체 control gallery 및 잘못된 validator fixture에서 normalized output이 Python reference와 conform합니다. Static Vercel file, canonical Supabase RPC migration, Prolific launch validation, preregistration draft, native surveydown export, offline preflight가 구현되었습니다. Live service 연결 및 검증은 의도적으로 수행하지 않았습니다. 자세한 내용은 [외부 연결 준비 상태](./docs/external-connection-readiness(kor).md)를 참고하십시오.

## Responsive preview 사용하기

No-install 경로에서는 modern browser로 `examples/complete-study/preview.html`을 직접 엽니다. 독립 desktop/mobile session을 동시에 보여줍니다. 같은 폴더의 `studio.html`을 열고 `survey.qmd`와 `greedyq.yml`을 선택하면 browser 안에서 parse, validate, compile, preview 전 과정을 실행합니다.

다음 Python command는 reference 개발 및 deterministic regeneration을 위해 계속 제공합니다.

Repository root에서 다음을 실행합니다.

```bash
python3 -m greedyq preview examples/complete-study
```

브라우저에서 `http://localhost:4173/preview.html`이 열립니다. Simple survey를 시험하려면 다음을 실행합니다.

```bash
python3 -m greedyq preview examples/simple-satisfaction-study
```

Preview를 생성하지 않고 검사하려면 `python3 -m greedyq validate PATH_TO_STUDY`, 서버를 시작하지 않고 고정 browser bundle(`index.html`, `preview.html`, `studio.html`, JavaScript, CSS, normalized artifact)을 만들려면 `python3 -m greedyq build PATH_TO_STUDY`를 사용합니다. Preview mode에서는 respondent data가 브라우저 밖으로 전송되지 않습니다. 자세한 내용은 [브라우저 프리뷰 안내](./docs/browser-preview(kor).md)를 참고하십시오.

이 명령은 현재 Python 3가 필요하며 개발 및 conformance 작업을 위한 것입니다. 목표로 하는 최종 사용자 경로에는 capable AI와 modern browser만 필요합니다. 로컬에서 실제로 저장되는 respondent session을 시험하려면 `python3 -m greedyq run examples/complete-study`를 실행하고 `http://localhost:4180/study`를 엽니다. 이 test runtime은 git에서 제외되는 로컬 SQLite database에 응답을 기록하며 아직 Supabase/Vercel production runtime은 아닙니다. [런타임 아키텍처](./docs/runtime-architecture(kor).md)와 [로컬 respondent runtime 안내](./docs/local-respondent-runtime(kor).md)를 참고하십시오.

현재 방향은 [START-HERE(kor).md](./START-HERE(kor).md), [연구 framing](./docs/research-framing(kor).md), [AI guide](./guides/README(kor).md), [모듈형 guide architecture](./docs/modular-guide-architecture(kor).md), [제품 개요](./docs/product-brief(kor).md), [greedyQ v0.2 스펙](./docs/greedyq-v0.2-spec(kor).md), [브라우저 프리뷰 안내](./docs/browser-preview(kor).md), [로컬 respondent runtime](./docs/local-respondent-runtime(kor).md), [골든 레퍼런스 연구](./examples/README(kor).md), [surveydown 호환성 조사](./docs/surveydown-compatibility(kor).md), [로드맵](./docs/roadmap(kor).md)을 참고하십시오.

## 문서 정책

영문 Markdown 파일이 source of truth입니다. 모든 Markdown 문서에는 파일명이 `(kor).md`로 끝나는 동기화된 한국어 사본을 둡니다. 코드, 식별자, 경로, 설정 키, 규범적 문법은 번역하지 않습니다.

## 라이선스

greedyQ는 [MIT License](./LICENSE)로 배포합니다.
