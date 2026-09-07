# greedyQualt

[English](./README.md)

> R, RStudio, Quarto, Shiny 없이 사용하는 surveydown 호환 survey-as-code.

greedyQualt는 오픈소스 Markdown-first 설문 및 실험 연구 엔진입니다. 연구자는 버전 관리되는 텍스트 파일로 연구를 정의하고, Vercel을 통해 설문 앱을 배포하며, 자신이 소유한 Supabase 프로젝트에 응답을 저장합니다.

이 프로젝트는 재현 가능한 학술 연구를 목적으로 하며, 특히 분기, 지속적인 무작위 배정, 요인 실험, conjoint/CBC 설계가 필요한 연구를 지원합니다.

## 왜 greedyQualt인가?

상용 설문 플랫폼은 비용이 높고, 정확한 재현이 어려우며, 복잡한 실험 설계에 제약이 있을 수 있습니다. surveydown은 훌륭한 survey-as-code 모델을 제공하지만 R, Quarto, Shiny 도구 체인이 연구자의 진입 장벽이 될 수 있습니다.

greedyQualt는 다음 장점을 유지합니다.

- 사람이 읽을 수 있는 설문 정의
- Git 기반 버전 관리와 재현성
- 연구자가 소유하는 PostgreSQL 데이터
- 프로그래밍 가능한 연구 워크플로

대신 필수 R/Shiny 런타임을 GitHub, Vercel, Supabase에 맞춘 웹 네이티브 TypeScript 및 React 스택으로 교체합니다.

## 제품 원칙

- `survey.qmd`가 설문 콘텐츠와 문항의 source of truth입니다.
- 사용자 대상 QMD 문법은 가능한 범위에서 surveydown과 호환되어야 합니다.
- 임의의 R 및 Shiny 코드를 실행하지 않습니다.
- 조건 로직과 무작위화는 선언적이고 안전하며 재현 가능해야 합니다.
- 연구자가 응답 데이터를 소유하고 통제합니다.
- GUI 설문 빌더를 요구하지 않습니다.
- 스펙은 사람이 읽을 수 있고 범용 언어 모델이 신뢰성 있게 사용할 수 있어야 합니다.

## 목표 워크플로

```text
survey.qmd + greedyqualt.yml + design/*.csv
                       |
                       v
        parser -> Survey AST -> validator
                       |
                       v
             React/Next.js renderer
                       |
                       v
                    Vercel
                       |
                       v
             연구자 소유 Supabase
```

목표로 하는 온보딩 경험은 다음과 같습니다.

1. greedyQualt 템플릿을 fork합니다.
2. `survey.qmd`를 직접 수정하거나 LLM으로 생성합니다.
3. Supabase 프로젝트를 생성합니다.
4. 저장소를 Vercel에 배포합니다.
5. Supabase 환경 변수를 입력합니다.
6. 설문을 공개합니다.

## 설문 작성 경로

greedyQualt는 다음 세 가지 설문 작성 경로를 지원할 예정입니다.

1. `survey.qmd`와 `greedyqualt.yml` 직접 작성
2. PowerPoint 설문 초안을 QMD, 설정 파일, 추출된 asset으로 변환
3. 버전이 명시된 Markdown authoring vignette을 GPT, Claude 등의 LLM에 제공하여 유효한 프로젝트 파일 생성

## 프로젝트 상태

greedyQualt는 현재 스펙 정의 단계입니다. 첫 번째 milestone은 런타임을 구현하기 전에 surveydown의 공개된 사용자 대상 스펙을 문서화하고 greedyQualt v0.1의 호환 범위를 확정하는 것입니다.

현재 방향은 [제품 개요](./docs/product-brief(kor).md), [surveydown 호환성 조사](./docs/surveydown-compatibility(kor).md), [로드맵](./docs/roadmap(kor).md)을 참고하십시오.

## 문서 정책

영문 Markdown 파일이 source of truth입니다. 모든 Markdown 문서에는 파일명이 `(kor).md`로 끝나는 동기화된 한국어 사본을 둡니다. 코드, 식별자, 경로, 설정 키, 규범적 문법은 번역하지 않습니다.

## 라이선스

오픈소스 라이선스는 아직 결정하지 않았습니다. MIT와 Apache-2.0을 후보로 검토합니다.
