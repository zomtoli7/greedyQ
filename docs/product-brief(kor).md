# greedyQ 제품 개요

[English](./product-brief.md)

**상태:** 초안

**제품 단계:** 구현 전 스펙 정의

**문서 역할:** 제품 방향 및 의사결정 기준

## 1. 제품 정의

greedyQ는 online academic research를 위한 specification-driven, AI-native application입니다. Application 자체를 conventional source code로 구현하는 대신, greedyQ는 general-purpose generative AI agent가 application을 어떻게 instantiate하고 operate해야 하는지 명시합니다. Markdown guide, schema, checkpoint, exact template이 portable **agent-executable application specification**을 이룹니다.

greedyQ 자체는 agent가 아닙니다. greedyQ specification과 capable host GenAI가 결합하여 greedyQ research agent를 instantiate합니다. 이 research agent가 연구자와 협업하고 연구설계 artifact와 실행 가능한 respondent-facing survey software를 만듭니다.

이 제품은 Qualtrics를 화면 단위로 복제하거나 또 다른 GUI form builder 또는 독점 AI 서비스가 되는 것을 목표로 하지 않습니다. 주요 사용자 interface는 안내형 대화이며 지속 가능한 abstraction은 버전 관리되는 연구 스펙입니다. QMD 직접 작성은 expert path로 유지합니다.

greedyQ는 MIT License를 사용하는 독립 구현입니다. 주 제품은 자체 Vercel/Supabase web runtime이며, 작성 호환성을 위해 문서화된 surveydown-style `survey.qmd` 관례의 일부를 채택하고 고급 R, Shiny, Quarto 사용자 정의를 위한 native surveydown 프로젝트를 생성합니다. Surveydown 소스 코드를 포함하지 않으며 제휴 또는 보증 관계를 주장하지 않습니다.

### 핵심 제안

> 재현 가능한 연구방법론과 workflow를 agent-executable specification으로 package하여 capable general-purpose GenAI를 domain-specific research application으로 전환합니다.

### Architecture 정체성

1. **Architecture:** normative behavior가 사람이 읽고 agent가 실행할 수 있는 specification으로 배포되는 specification-driven AI-native application입니다.
2. **Domain:** 연구설계, consent, measurement, experiment, respondent collection, data planning, preregistration, deployment, fielding을 포함하는 online academic research입니다.
3. **Implementation:** 이 architecture를 구체적이고 검증 가능하게 구현한 greedyQ입니다.

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
- 설문 DSL을 배우지 않고 대화를 통해 엄밀한 설문을 만들고 싶은 연구자
- Text file과 Git을 직접 검사하거나 편집하려는 expert user
- 무작위화, 요인 설계, conjoint/CBC가 필요한 실험 연구자
- Web-native runtime을 사용하면서도 native R/Shiny 사용자 정의 경로를 유지하려는 surveydown 사용자

### 초기 대상이 아닌 사용자

드래그앤드롭 방식의 시각적 설문 에디터가 최우선 요구사항인 사용자는 초기 대상이 아닙니다.

## 4. 제품 원칙

1. **연구 스펙이 source of truth입니다.** 설문 콘텐츠, 로직, 설계를 검사하고 버전 관리할 수 있어야 합니다.
2. **호환성은 사용자 문법을 대상으로 하며 독립 구현합니다.** surveydown 소스 코드를 포함하지 않고 공개적으로 문서화된 작성 관례를 목표로 합니다.
3. **임의 코드를 실행하지 않습니다.** R chunk는 지원되는 제한적 `sd_*()` expression 집합으로만 parse합니다.
4. **로직은 선언적입니다.** 분기, 검증, 무작위화에는 안전하고 문서화된 DSL을 사용합니다.
5. **연구를 우선합니다.** 재현 가능한 무작위화, 실험 metadata, 분석 가능한 데이터가 핵심 고려사항입니다.
6. **연구자가 데이터를 소유합니다.** 응답은 연구자의 Supabase 프로젝트로 전송하며 greedyQ는 중앙 응답 데이터 서비스를 운영하지 않습니다.
7. **GUI에 의존하지 않습니다.** 작성이나 배포에 GUI 설문 빌더가 필요하지 않습니다.
8. **Agent-executable specification이 application core입니다.** Capable general-purpose GenAI가 이를 greedyQ research agent로 instantiate하고, 이 agent가 연구자를 인터뷰하며 study state를 유지하고 유효한 artifact를 생성합니다.
9. **배포는 평범하고 단순해야 합니다.** GitHub, Vercel, Supabase만으로 production 설문을 운영할 수 있어야 합니다.
10. **연구 governance를 명시해야 합니다.** 법적 또는 기관 compliance를 보증하지 않으면서 ethics-review metadata, consent, respondent-source 기록을 구조화하고 버전 관리하며 감사할 수 있어야 합니다.
11. **LLM이 연구 지능을 제공합니다.** greedyQ는 모델의 발전하는 방법론 지식을 중복 구현하지 않고 review 시점, 확인이 필요한 결정, 결정 기록 방식을 정의합니다.
12. **연구자의 권한을 보존합니다.** AI는 문제를 설명하고 대안을 제시하지만 중요한 연구 결정을 조용히 변경하지 않습니다.
13. **Capability를 정직하게 다룹니다.** Chat mode는 artifact와 handoff instruction을 만들고, agent mode는 필요한 도구와 권한이 있을 때만 외부 서비스를 설정하고 검증합니다.
14. **Web-native runtime이 우선입니다.** Vercel과 Supabase가 주 실행 경로이며 native surveydown export는 greedyQ runtime이 아닌 핵심 병렬 출력입니다.
15. **고급 사용자 정의에는 escape hatch가 있습니다.** 제한 없는 R, Shiny, Quarto가 필요할 때 연구자가 surveydown에서 직접 이어갈 수 있도록 `app.R`과 관련 native 프로젝트 파일을 생성합니다.
16. **Preregistration은 핵심 출력입니다.** 확인된 연구 및 분석 결정에서 검토 가능하고 versioned된 preregistration package를 생성하고 registry 제출 또는 sample collection 전에 연구자의 명시적 승인을 요구합니다.

## 5. 호환성 전략

| 계층 | greedyQ 정책 |
| --- | --- |
| `survey.qmd` 페이지 및 문항 문법 | 가능한 범위에서 호환 |
| surveydown YAML 설정 | 문서화되고 구현 가능한 범위에서 호환 |
| 기존 `app.R` 입력 | 절대 실행하지 않으며 인식 가능한 pattern만 diagnostic과 함께 migration 가능 |
| 생성되는 `app.R` 출력 | 검증된 AST에서 생성하는 핵심 native surveydown export |
| 임의의 R/Shiny reactive code | 미지원 |
| 문항 타입 | surveydown의 공개 question API 우선 구현 |
| 조건 로직 | 네이티브 선언형 DSL |
| 무작위화 | 네이티브 first-class feature |
| 데이터베이스 | 연구자 소유 Supabase/PostgreSQL |
| 런타임 | TypeScript, React, 웹 네이티브 server/runtime 계층 |
| 호스팅 | Vercel 우선 |

모든 기능은 두 출력 경로에 걸쳐 다음과 같이 분류해야 합니다.

- **Directly portable:** 호환 QMD로 표현되며 native surveydown 출력에서도 보존
- **Generated:** greedyQ에서 native로 구현하고 생성된 `app.R` 또는 보조 파일로 변환
- **greedyQ-only:** web-native runtime에서 사용할 수 있지만 export 시 명시적인 제한 또는 대안 제공
- **Unsupported:** 조용히 변경하지 않고 안정적인 diagnostic으로 거부

목표로 하는 실행 및 export pipeline은 다음과 같습니다.

```text
survey.qmd + greedyq.yml + design/*.csv + assets
                         |
                         v
              parser -> validated AST
                    /             \
                   v               v
       greedyQ web runtime    export generator
                   |               |
                   v               v
         Vercel + Supabase   survey.qmd + app.R
                                     |
                                     v
                           native surveydown project
```

## 6. 제안 기술 모델

```text
Versioned guide + 자연어 연구 요청
      |
      v
Guided interview + 연구자 approval checkpoint
      |
      v
survey.qmd
greedyq.yml
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
      +-- native surveydown export generator
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
├── greedyq.yml
├── design/
│   └── choice_sets.csv
├── assets/
├── export/
│   └── surveydown/
│       ├── survey.qmd
│       ├── app.R
│       └── compatibility-report.json
└── supabase/
    └── migrations/
```

- `survey.qmd`: 페이지, Markdown 콘텐츠, 문항, navigation
- `greedyq.yml`: 표시 규칙, 분기, 검증, 무작위화
- `design/*.csv`: conjoint/CBC 및 반복 실험 설계
- `assets/`: 이미지와 실험 자극물
- `export/surveydown/`: 생성된 native surveydown 프로젝트 및 호환성 보고서
- `supabase/`: 재현 가능한 데이터베이스 migration

## 8. 선언형 로직

`greedyq.yml`은 지원되는 runtime 동작을 제한된 언어로 표현합니다. greedyQ runtime은 이를 직접 평가하며, native export generator는 parsing, validation, preview, deployment 과정에서 임의의 R을 실행하지 않고 지원 동작을 `app.R`로 변환합니다.

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

## 11. 주요 경험 및 대안 작성 경로

### 11.1 메인 기능: greedyQ research agent instantiate

Versioned greedyQ repository는 agent-executable application specification을 제공합니다. Capable general-purpose GenAI가 이 specification을 불러와 greedyQ research agent를 instantiate합니다. Host마다 interface와 native capability가 달라도 생성된 agent는 같은 normative checkpoint, artifact contract, conformance test를 따라야 합니다.

```text
START-HERE.md + registry + resolved specification
                   |
                   v
         capable general-purpose GenAI
                   |
                   v
          greedyQ research agent
                   |
     +-------------+--------------+
     | research design            |
     | eligibility and consent    |
     | questions and measurement  |
     | logic and randomization    |
     | respondent source          |
     | data, privacy, deployment  |
     +-------------+--------------+
                   |
                   v
         연구자 approval checkpoint
                   |
                   v
     survey.qmd + greedyq.yml + design/*.csv
                   |
                   v
 validate -> preregister -> preview -> approve -> deploy
```

Interview는 한 번에 하나의 집중된 질문을 하고, 확인된 결정을 구조적으로 기록하며, 안정된 checkpoint에서 artifact를 갱신합니다. Fielding 전에 hypothesis, design, sampling, exclusion, variable, analysis를 다루는 preregistration package를 생성합니다. LLM은 자체 연구 지식을 이용해 방법론적 위험을 발견하고 설명하며 대안을 제시할 수 있지만 해결되지 않은 preregistration commitment를 지어내면 안 됩니다. Guide는 설문 방법론 백과사전을 유지하려 하지 않습니다. Review workflow를 정의하고 중요한 결정이 바뀌기 전에 연구자의 확인을 요구합니다.

### 11.2 Chat mode 및 agent mode

Guide는 먼저 사용 가능한 capability를 감지합니다.

- **Chat mode:** 인터뷰를 수행하고 모든 project artifact를 생성하며 guide 기반 self-check를 실행하고 정확한 validation/deployment handoff instruction을 제공합니다.
- **Agent mode:** 도구와 권한이 허용할 때 repository 편집, validator 실행, Supabase 및 Vercel provision/연결, environment variable 설정, 배포, live survey 검증까지 수행합니다.

Workflow는 실제 operation을 수행하고 검증하지 않은 repository, database, deployment 또는 external panel을 설정했다고 주장해서는 안 됩니다.

### 11.3 책임 구분

| Actor | 책임 |
| --- | --- |
| LLM | 연구 reasoning, question critique, design concern, 대안, 자연어 협업 |
| greedyQ guide | Interview sequence, 필수 review 시점, approval checkpoint, artifact 및 deployment workflow |
| greedyQ validator | ID, reference, reachability, cycle, configuration completeness, deterministic constraint |
| 연구자 | 중요한 연구 결정 및 최종 승인 |

### 11.4 Guide artifact

```text
guides/greedyq-guide.md
guides/greedyq-guide-compact.md
examples/complete-study/
```

전체 guide는 다음을 정의해야 합니다.

- Role, scope, 금지 동작
- Capability detection 및 mode 선택
- Phase별 interview protocol
- 한 번에 하나의 질문을 하는 interaction
- Research review 및 연구자 확인 checkpoint
- Study-state 및 decision-log format
- QMD, YAML, logic, randomization, CSV contract
- IRB/ethics, consent, respondent-source workflow
- Preregistration interview, template 선택, artifact hash, pre-fielding approval gate
- Artifact 생성 및 갱신 규칙
- Validation 및 LLM correction loop
- Preview 및 배포 전 승인
- GitHub, Vercel, Supabase, Prolific 절차
- Deployment verification 및 study handoff

### 11.5 Expert path: 직접 작성

숙련된 사용자는 `survey.qmd`, `greedyq.yml`, design 파일을 직접 편집할 수 있습니다. 해당 artifact도 같은 validation, preview, approval, deployment pipeline에 들어갑니다.

### 11.6 Import path: PPTX converter

Converter는 완벽한 semantic recovery를 주장하는 대신 수정 가능한 고품질 초안을 생성합니다.

```text
survey.pptx
    |
    v
greedyq convert survey.pptx
    |
    +-- survey.qmd
    +-- greedyq.yml
    +-- assets/*
    +-- conversion-report.md
    |
    v
guided AI review -> validate -> preview -> deploy
```

PPTX 구조, layout, table, speaker notes, optional metadata를 사용하여 페이지와 문항을 추론하고 모호한 변환을 보고해야 합니다.

## 12. 초기 성공 기준

첫 end-to-end milestone은 연구자가 다음을 수행할 수 있을 때 성공한 것입니다.

1. Guide를 첨부하고 새 설문을 요청하며 한 번에 하나씩 진행되는 인터뷰를 완료합니다.
2. 기록된 중요한 연구 결정을 검토하고 승인합니다.
3. 유효한 QMD, configuration, design, consent, deployment artifact를 받습니다.
4. R을 설치하지 않고 연구를 검증합니다.
5. Sample collection 전에 생성된 preregistration package를 검토하고 승인합니다.
6. Chat-mode handoff 또는 agent-mode execution으로 연구를 preview하고 배포합니다.
7. 지속적인 실험 배정으로 respondent를 등록합니다.
8. 연구자의 Supabase에 부분 및 완료 응답을 저장합니다.
9. 분석 가능한 데이터를 export합니다.
10. Git commit과 기록된 스펙 버전으로 interview decision과 배포 당시 연구를 재현합니다.

## 13. 연구 governance 및 respondent source

### 13.1 Ethics 및 IRB metadata

greedyQ는 ethics-review 정보를 위한 구조화된 metadata와 재사용 가능한 presentation block을 제공해야 합니다.

```yaml
study:
  title: Hotel Choice Study

  ethics:
    institution: Example University
    protocol-id: IRB-2026-0123
    approval-date: 2026-08-01
    principal-investigator: Jane Doe
    contact: jane@example.edu
```

엔진은 필수 project field를 검증하고 선언된 정보를 render하며 실제 배포된 연구 버전과 함께 보존할 수 있습니다. 연구가 IRB 승인, 법적 compliance 또는 윤리적 충분성을 갖췄다고 주장해서는 안 됩니다. 승인과 compliance는 연구자 및 소속 기관의 책임입니다.

### 13.2 First-class consent

Consent는 관례적으로 일반 multiple-choice question을 사용하는 것이 아니라 semantic study primitive여야 합니다.

```yaml
consent:
  page: consent
  question: consent_agreement
  accepted-value: yes
  rejected-page: consent_declined
  required: true
  record:
    - consent-version
    - consent-timestamp
    - consent-document-hash
```

v0.2 스펙은 다음을 정의해야 합니다.

- 필수 consent가 수락될 때까지 study question 접근 차단
- Consent 거부 시 결정론적 route
- Consent document version 및 content hash
- Server에 기록되는 acceptance timestamp
- Fielding 중 consent 문구가 바뀔 때의 동작
- Withdrawal 및 response-retention policy hook
- 관할 규칙을 가정하지 않는 optional parental/guardian-consent extension
- 불완전하거나 일관되지 않은 consent configuration에 대한 validator error

전자서명과 관할별 compliance workflow는 법적·운영 요구사항을 별도로 정의할 때까지 deferred로 둡니다.

### 13.3 External respondent collector

greedyQ는 provider-neutral integration contract와 일반 respondent platform을 위한 named preset을 제공해야 합니다.

```yaml
respondent-source:
  provider: prolific

  capture:
    participant-id: PROLIFIC_PID
    study-id: STUDY_ID
    session-id: SESSION_ID

  completion:
    complete: https://app.prolific.com/submissions/complete?cc=ABC123
    screenout: https://app.prolific.com/submissions/complete?cc=SCREEN1
```

Generic contract는 다음을 지원해야 합니다.

- Allowlist된 inbound URL parameter
- Required-parameter validation
- Canonical participant, study, external-session identifier
- Duplicate-participation policy
- Complete, screen-out, quota-full, technical-error outcome별 completion route
- Allowlist된 redirect destination에 대한 안전한 parameter interpolation
- Raw external parameter의 명시적 storage 및 privacy policy
- 실수로 production completion redirect를 실행하지 않게 하는 test mode

Prolific preset은 초기 target입니다. 다른 provider는 provider-specific runtime logic을 추가하는 대신 같은 generic contract를 사용해야 합니다.

## 14. 미결정 사항

- 정확한 v0.2 surveydown 호환 범위
- Parser 구현 및 grammar 전략
- Next.js 및 runtime architecture
- Supabase 관계형/JSONB schema 경계
- 안전한 expression-language grammar
- 균형 무작위화를 위한 transaction 모델
- 공개 배포 전 제품명 및 상표 검토
- 최소 필수 ethics metadata 및 study template별 차이
- Consent amendment, withdrawal, response-retention semantics
- Prolific completion-status mapping 및 duplicate-participation default
