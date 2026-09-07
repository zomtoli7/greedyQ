# greedyQualt

[English](./README.md)

> 이미 사용하는 AI와의 안내형 대화로 엄밀하고 재현 가능한 연구 설문을 만듭니다.

greedyQualt는 결정론적인 Markdown-first 엔진을 기반으로 하는 오픈소스 AI-guided 설문 및 실험 연구 workflow입니다. 연구자는 버전이 명시된 greedyQualt guide를 GPT, Claude 등의 유능한 agent에게 제공하고 “설문 만들자!”와 같은 간단한 요청으로 시작합니다. AI는 연구자를 인터뷰하고, 확인된 결정을 기록하며, 유효한 연구 파일을 생성·검증하고, 연결된 도구가 있으면 GitHub, Vercel, Supabase도 설정합니다.

AI는 연구 reasoning과 자연어 협업을 제공합니다. greedyQualt는 interview protocol, 승인 checkpoint, specification, validator, runtime, deployment contract, reproducibility를 제공합니다. 이 프로젝트는 감사 가능한 consent, 외부 respondent panel, 분기, 지속적인 무작위 배정, 요인 실험, conjoint/CBC 설계가 필요한 학술 연구를 대상으로 합니다.

## 왜 greedyQualt인가?

상용 설문 플랫폼은 비용이 높고, 정확한 재현이 어려우며, 복잡한 실험 설계에 제약이 있을 수 있습니다. surveydown은 훌륭한 survey-as-code 모델을 제공하지만 R, Quarto, Shiny 도구 체인이 연구자의 진입 장벽이 될 수 있습니다.

greedyQualt는 다음 장점을 유지합니다.

- 사람이 읽을 수 있는 설문 정의
- Git 기반 버전 관리와 재현성
- 연구자가 소유하는 PostgreSQL 데이터
- 프로그래밍 가능한 연구 워크플로

대신 필수 R/Shiny 런타임을 GitHub, Vercel, Supabase에 맞춘 웹 네이티브 TypeScript 및 React 스택으로 교체하고, 이 결정론적 스택을 안내형 AI 대화로 사용할 수 있게 합니다.

## 제품 원칙

- `survey.qmd`가 설문 콘텐츠와 문항의 source of truth입니다.
- 사용자 대상 QMD 문법은 가능한 범위에서 surveydown과 호환되어야 합니다.
- 임의의 R 및 Shiny 코드를 실행하지 않습니다.
- 조건 로직과 무작위화는 선언적이고 안전하며 재현 가능해야 합니다.
- 연구자가 응답 데이터를 소유하고 통제합니다.
- GUI 설문 빌더를 요구하지 않습니다.
- 주요 사용자 경험은 범용 LLM과의 안내형 대화입니다.
- LLM은 연구 지능을 제공하고, greedyQualt는 workflow, specification, validation, reproducibility를 제공합니다.
- 중요한 연구 결정에는 연구자의 명시적 확인이 필요합니다.
- Workflow는 연결 도구로 직접 작업할 수 있는지, 사용자에게 파일과 지침을 제공해야 하는지 감지해야 합니다.

## 주요 workflow

```text
Versioned greedyQualt guide + 연구자의 연구 아이디어
                         |
                         v
                 안내형 AI 인터뷰
                         |
     연구 설계 -> consent -> questions
     -> logic -> randomization -> respondent source
                         |
                         v
     survey.qmd + greedyqualt.yml + design/*.csv
                         |
                         v
           parser -> Survey AST -> validator
                         |
                         v
                 preview 및 승인
                         |
                         v
          GitHub -> Vercel -> Supabase
```

목표로 하는 온보딩 경험은 다음과 같습니다.

1. 버전이 명시된 greedyQualt guide를 유능한 LLM 또는 agent에 첨부합니다.
2. 만들고 싶은 연구를 말합니다.
3. 한 번에 하나씩 제시되는 질문에 답하고 중요한 결정을 확인합니다.
4. 생성된 연구, consent, logic, randomization, data plan을 검토합니다.
5. 생성된 프로젝트를 validate하고 preview합니다.
6. 연결된 agent가 GitHub, Vercel, Supabase를 설정하게 하거나 생성된 handoff 안내를 따릅니다.
7. 설문을 승인하고 공개합니다.

## Interaction mode 및 대안 경로

Guide는 capability에 따라 두 mode를 지원합니다.

- **Chat mode:** AI가 인터뷰하고 프로젝트 파일을 만들며 guide에 따라 reasoning을 검증하고 사용자에게 배포 방법을 안내합니다.
- **Agent mode:** 연결된 agent가 추가로 repository 편집, validation 실행, 서비스 설정, 배포, live survey 검증까지 수행합니다.

Expert user는 계속 `survey.qmd`와 `greedyqualt.yml`을 직접 작성할 수 있습니다. 향후 PPTX importer는 기존 slide 기반 초안을 편집 가능한 study artifact로 바꾸고 동일한 안내형 review workflow에 넣습니다.

## 프로젝트 상태

greedyQualt는 현재 스펙 정의 단계입니다. 현재 milestone은 완료된 surveydown 호환성 조사를 greedyQualt v0.1 스펙과 버전이 명시된 guided-interview protocol로 전환한 후 런타임을 구현하는 것입니다.

현재 방향은 [제품 개요](./docs/product-brief(kor).md), [surveydown 호환성 조사](./docs/surveydown-compatibility(kor).md), [로드맵](./docs/roadmap(kor).md)을 참고하십시오.

## 문서 정책

영문 Markdown 파일이 source of truth입니다. 모든 Markdown 문서에는 파일명이 `(kor).md`로 끝나는 동기화된 한국어 사본을 둡니다. 코드, 식별자, 경로, 설정 키, 규범적 문법은 번역하지 않습니다.

## 라이선스

오픈소스 라이선스는 아직 결정하지 않았습니다. MIT와 Apache-2.0을 후보로 검토합니다.
