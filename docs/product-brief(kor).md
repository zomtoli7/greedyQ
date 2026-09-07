# greedyQualt 제품 개요

[English](./product-brief.md)

**상태:** 초안

**제품 단계:** 구현 전 스펙 정의

**문서 역할:** 제품 방향 및 의사결정 기준

## 1. 제품 정의

greedyQualt는 학술 설문과 실험을 제작·배포·운영하기 위한 오픈소스 Markdown-first 플랫폼입니다. 가능한 범위에서 surveydown 호환 설문 정의를 받아 안전한 내부 schema로 compile하고, 웹 애플리케이션으로 render하며, 연구자가 소유한 인프라에 응답을 저장합니다.

이 제품은 Qualtrics를 화면 단위로 복제하거나 또 다른 GUI form builder가 되는 것을 목표로 하지 않습니다. 핵심 abstraction은 버전 관리되는 연구 스펙입니다.

### 핵심 제안

> Survey-as-code의 장점은 유지하고, 필수 도구 체인에서 R, RStudio, Quarto, Shiny를 제거합니다.

### 제품 약속

> 당신의 설문. 당신의 데이터베이스. 당신의 데이터.

## 2. 해결하려는 문제

학술 연구자는 강력한 설문과 실험 기능이 필요하지만 기존 접근법에는 피할 수 있는 비용이 존재합니다.

- 상용 플랫폼은 비용이 높고 학술 지원을 축소할 수 있습니다.
- GUI로 작성한 연구는 diff로 검토하거나 정확한 버전에서 재현하기 어렵습니다.
- 고급 실험에는 플랫폼 종속적인 custom JavaScript가 필요한 경우가 많습니다.
- 호스팅 플랫폼이 데이터 저장과 운영 통제권을 가집니다.
- R/Shiny 기반 survey-as-code 시스템에는 전문적인 로컬 및 배포 도구 체인이 필요합니다.

이러한 제약은 무작위 배정, 반복 선택 과제, 복잡한 분기, conjoint/CBC 또는 감사 가능한 연구 워크플로가 필요한 연구에서 특히 큰 비용이 됩니다.

## 3. 대상 사용자

### 주요 사용자

- 재현 가능한 설문 워크플로를 원하는 학술 연구자
- 비싼 독점 플랫폼을 대체하거나 보완하려는 연구자
- 직접 또는 AI의 도움을 받아 텍스트 파일과 Git을 사용할 의향이 있는 연구자
- 무작위화, 요인 설계, conjoint/CBC가 필요한 실험 연구자
- `survey.qmd`는 유지하면서 R/Shiny 런타임을 교체하고 싶은 surveydown 사용자

### 초기 대상이 아닌 사용자

드래그앤드롭 방식의 시각적 설문 에디터가 최우선 요구사항인 사용자는 초기 대상이 아닙니다.

## 4. 제품 원칙

1. **연구 스펙이 source of truth입니다.** 설문 콘텐츠, 로직, 설계를 검사하고 버전 관리할 수 있어야 합니다.
2. **호환성은 사용자 문법을 대상으로 합니다.** surveydown 내부 구현이 아니라 공개된 작성 스펙을 목표로 합니다.
3. **임의 코드를 실행하지 않습니다.** R chunk는 지원되는 제한적 `sd_*()` expression 집합으로만 parse합니다.
4. **로직은 선언적입니다.** 분기, 검증, 무작위화에는 안전하고 문서화된 DSL을 사용합니다.
5. **연구를 우선합니다.** 재현 가능한 무작위화, 실험 metadata, 분석 가능한 데이터가 핵심 고려사항입니다.
6. **연구자가 데이터를 소유합니다.** 응답은 연구자의 Supabase 프로젝트로 전송하며 greedyQualt는 중앙 응답 데이터 서비스를 운영하지 않습니다.
7. **GUI에 의존하지 않습니다.** 작성이나 배포에 GUI 설문 빌더가 필요하지 않습니다.
8. **AI는 독점 의존성이 아닌 작성 인터페이스입니다.** 범용 LLM이 유효한 연구를 생성할 수 있도록 스펙을 설계합니다.
9. **배포는 평범하고 단순해야 합니다.** GitHub, Vercel, Supabase만으로 production 설문을 운영할 수 있어야 합니다.

## 5. 호환성 전략

| 계층 | greedyQualt 정책 |
| --- | --- |
| `survey.qmd` 페이지 및 문항 문법 | 가능한 범위에서 호환 |
| surveydown YAML 설정 | 문서화되고 구현 가능한 범위에서 호환 |
| `app.R` | 실행하지 않고 선언형 설정으로 대체 |
| 임의의 R/Shiny reactive code | 미지원 |
| 문항 타입 | surveydown의 공개 question API 우선 구현 |
| 조건 로직 | 네이티브 선언형 DSL |
| 무작위화 | 네이티브 first-class feature |
| 데이터베이스 | 연구자 소유 Supabase/PostgreSQL |
| 런타임 | TypeScript, React, 웹 네이티브 server/runtime 계층 |
| 호스팅 | Vercel 우선 |

목표로 하는 migration 경로는 다음과 같습니다.

```text
기존 surveydown 프로젝트

survey.qmd  ----------------------> 호환 범위에서 유지
app.R       -- migration 도구 ---> greedyqualt.yml
                                      |
                                      v
                               greedyQualt runtime
                                      |
                                      v
                              Vercel + Supabase
```

## 6. 제안 기술 모델

```text
survey.qmd
greedyqualt.yml
design/*.csv
assets/*
      |
      v
QMD parser + restricted sd_* parser
      |
      v
Internal Survey AST / JSON schema
      |
      +-- validator
      +-- logic engine
      +-- randomization engine
      +-- migration diagnostics
      |
      v
React/Next.js survey renderer
      |
      v
Vercel deployment
      |
      v
연구자 소유 Supabase/PostgreSQL
```

정확한 라이브러리, framework 버전, schema 구조, 지원할 함수 인수는 스펙 단계에서 결정합니다.

## 7. 제안 프로젝트 형식

```text
my-survey/
├── survey.qmd
├── greedyqualt.yml
├── design/
│   └── choice_sets.csv
├── assets/
└── supabase/
    └── migrations/
```

- `survey.qmd`: 페이지, Markdown 콘텐츠, 문항, navigation
- `greedyqualt.yml`: 표시 규칙, 분기, 검증, 무작위화
- `design/*.csv`: conjoint/CBC 및 반복 실험 설계
- `assets/`: 이미지와 실험 자극물
- `supabase/`: 재현 가능한 데이터베이스 migration

## 8. 선언형 로직

`greedyqualt.yml`은 지원 가능한 `app.R` 사용 사례를 제한된 expression language로 대체합니다.

```yaml
logic:
  show:
    - question: q2
      if: q1 == "yes"

  skip:
    - if: age < 18
      to: screenout

  validate:
    - question: zipcode
      if: length(zipcode) != 5
      message: "Zip code must be 5 digits."
```

Expression language는 결정론적이어야 하고 정적 검증이 가능해야 하며 임의의 JavaScript를 실행할 수 없어야 합니다.

## 9. First-class feature로서의 무작위화

엔진은 궁극적으로 다음 기능을 지원해야 합니다.

- 단순 및 가중치 기반 무작위 배정
- block 및 stratified randomization
- 요인 설계
- 문항, 선택지, 페이지, 자극물, 과제 순서 무작위화
- 새로고침 및 재개된 session 전반에 유지되는 배정
- seed 기반 재현 가능한 배정
- condition, seed, block, timestamp를 포함한 배정 metadata 저장
- 동시 참여 상황에서도 transaction-safe한 배정

방향 예시:

```yaml
randomization:
  framing_experiment:
    type: between_subject
    method: block
    seed_by: respondent_id

    factors:
      frame: [gain, loss]
      information: [low, high]

    store:
      - frame
      - information
      - randomization_seed
      - block_id
```

## 10. Persistence와 데이터 소유권

초기 데이터 모델은 다음 영역을 포함할 것으로 예상합니다.

```text
studies
respondents
responses
assignments
choice_tasks
event_log
```

익명 session, 재개 가능한 진행 상태, 페이지 단위 저장, 완료 상태, Prolific ID와 같은 URL metadata, 분석 가능한 export가 필요합니다. 정규화된 관계형 table과 JSONB를 어디에 사용할지는 스펙 단계에서 결정합니다.

## 11. 설문 작성 경로

### 11.1 직접 작성

숙련된 사용자는 `survey.qmd`, `greedyqualt.yml`, design 파일을 직접 편집합니다. Git history가 실제 배포된 연구를 기록합니다.

### 11.2 후속 도구 1: PPTX converter

Converter는 완벽한 semantic recovery를 주장하는 대신 수정 가능한 고품질 초안을 생성합니다.

```text
survey.pptx
    |
    v
greedyqualt convert survey.pptx
    |
    +-- survey.qmd
    +-- greedyqualt.yml
    +-- assets/*
    +-- conversion-report.md
```

PPTX 구조, layout, table, speaker notes, optional metadata를 사용하여 페이지와 문항을 추론하고 모호한 변환을 보고해야 합니다.

### 11.3 후속 도구 2: LLM authoring vignette

독립적이고 버전이 명시된 Markdown vignette은 GPT, Claude 등의 범용 LLM이 자연어 연구 요구사항으로부터 유효한 greedyQualt 프로젝트를 생성하는 방법을 설명합니다.

```text
llm-authoring-vignette.md
             +
자연어 연구 요청
             |
             v
        GPT / Claude
             |
             +-- survey.qmd
             +-- greedyqualt.yml
             +-- design/*.csv
             +-- generation notes
             |
             v
greedyqualt validate --format llm
             |
             v
          LLM 보조 수정
```

Vignette에는 다음이 포함되어야 합니다.

- 규범적 프로젝트 및 출력 파일 계약
- 정확한 QMD, YAML, logic, randomization, CSV 문법
- 지원 및 금지 구문
- 완전하게 작동하는 예제
- 안정적인 스펙 버전 선언
- 필수 생성 self-check
- machine-actionable validation 안내

계획된 결과물:

```text
docs/llm-authoring-vignette.md
docs/llm-authoring-vignette-compact.md
examples/complete-study/
```

Validator는 사용자가 결과를 LLM에 다시 전달해 수정할 수 있도록 안정적인 diagnostic code와 정확한 위치를 제공해야 합니다.

## 12. 초기 성공 기준

첫 end-to-end milestone은 연구자가 다음을 수행할 수 있을 때 성공한 것입니다.

1. 문서화된 QMD subset으로 작은 연구를 정의합니다.
2. R을 설치하지 않고 검증합니다.
3. 웹 애플리케이션으로 preview하고 배포합니다.
4. 지속적인 실험 배정으로 respondent를 등록합니다.
5. 연구자의 Supabase에 부분 및 완료 응답을 저장합니다.
6. 분석 가능한 데이터를 export합니다.
7. Git commit과 기록된 스펙 버전으로 배포 당시 연구를 재현합니다.

## 13. 미결정 사항

- 정확한 v0.1 surveydown 호환 범위
- Parser 구현 및 grammar 전략
- Next.js 및 runtime architecture
- Supabase 관계형/JSONB schema 경계
- 안전한 expression-language grammar
- 균형 무작위화를 위한 transaction 모델
- 초기 라이선스: MIT 또는 Apache-2.0
- 공개 배포 전 제품명 및 상표 검토
