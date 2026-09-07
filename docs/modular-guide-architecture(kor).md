# greedyQ 모듈형 가이드 아키텍처

[English](./modular-guide-architecture.md)

**상태:** 승인된 아키텍처; 호환 구조 구현 완료

**대상:** greedyQ `0.2` 구조 개편

**범위:** AI용 가이드 배포, 연구 유형 분류, 재사용 규약·템플릿, 최종 사용자 대화

## 1. 제품 결정

greedyQ는 online academic research를 위한 specification-driven, AI-native application입니다. 차별점은 단순히 AI를 사용한다는 것이 아닙니다. Application logic을 portable하고 사람이 읽을 수 있는 **agent-executable application specification**으로 배포하여 general-purpose GenAI가 application을 어떻게 instantiate하고 operate할지 알려줍니다.

greedyQ 자체는 agent가 아닙니다. `greedyQ specification + host GenAI = greedyQ research agent`입니다. Instantiate된 agent가 연구자와 협업하고 연구설계 artifact와 실행 가능한 respondent-facing survey software를 만듭니다. 이러한 분리로 model 간 portability와 conformance가 핵심 architecture property가 됩니다.

greedyQ는 개발자에게 말하는 코드 생성기가 아니라 연구자를 위한 설문 제작 서비스처럼 행동해야 합니다.

연구자는 다음처럼 일상적인 요청 하나로 시작합니다.

> greedyQ 시작 가이드를 열고 할인 프레이밍에 관한 무작위 설문 실험을 만들도록 도와줘.

AI는 공개 greedyQ 저장소를 읽고 적절한 연구 프로필을 찾은 다음, 쉬운 말로 핵심 질문을 하나씩 하고, 브라우저에서 시험할 수 있는 설문을 만들며, 중요한 연구 결정마다 승인을 요청합니다. 기술 검증은 엄격하게 수행하되 평소에는 뒤에서 처리합니다.

매번 큰 파일을 첨부하는 대신 저장소를 기준 가이드 배포 경로로 사용합니다. 링크된 저장소 파일을 읽지 못하는 환경을 위해서는 자체 포함 release bundle 하나를 보조 수단으로 유지합니다.

## 2. 세 가지 커뮤니케이션 층 분리

### 2.1 연구자와의 대화

기본적으로 사용자에게 보이는 층입니다. 연구자가 프로그래밍, 배포, 데이터베이스, schema, hash, routing, build 용어를 모른다고 가정합니다.

AI는 다음과 같이 행동해야 합니다.

- 중요한 질문을 한 번에 하나씩 묻습니다.
- 왜 필요한 질문인지 평범한 연구 언어로 설명합니다.
- 부담을 줄일 수 있다면 구체적인 선택지 두세 개를 제안합니다.
- 참여자가 실제로 무엇을 보게 되는지 설명합니다.
- 작업 중인 실제 설문 화면을 기본 검토 수단으로 사용합니다.
- 막힌 사항은 연구자가 취할 수 있는 행동으로 설명합니다.
- 지금까지 확정된 내용을 짧고 친절하게 정리합니다.

AI는 일반적으로 `schema`, `manifest`, `AST`, `referential integrity`, `route graph`, `RLS`, `CSP`, `hash`, `deployment candidate` 같은 말을 사용하지 않습니다. 예시는 다음과 같습니다.

| 내부 사실 | 연구자에게 하는 표현 |
|---|---|
| schema validation 통과 | “설문 구조를 확인했고 끊어진 문항은 발견되지 않았습니다.” |
| 미결정 항목이 생성을 막음 | “설문을 마치려면 누가 참여할 수 있는지에 대한 답이 아직 필요합니다.” |
| 도달 불가능한 종료 경로 | “현재 참여자가 완료 페이지까지 갈 수 없습니다.” |
| 산출물 hash 변경 | “사전등록 초안을 만든 뒤 설문이 바뀌었기 때문에 초안도 갱신해야 합니다.” |
| 운영 배포 미검증 | “설문 파일은 준비됐지만 실제 링크는 아직 시험하지 않았습니다.” |

### 2.2 연구 기록

`study-plan.md`, 동의문, 사전등록 초안 같은 사람이 읽는 파일이 여기에 속합니다. 필요한 연구 용어는 사용하지만 소프트웨어 구현 세부사항은 피합니다. `study-plan.md`는 연구자 승인을 위한 간결한 기록이지 기술 build 보고서나 기본 preview가 아닙니다.

### 2.3 기계 및 개발자 진단

Schema, manifest, hash, 검증 코드, 생성 소스의 출처, 상세 테스트 로그는 `.greedyq/` 또는 개발자 보고서에 둡니다. 사용자가 요청하거나 기술적 실패를 설명해야 할 때만 보여주며, 일상적인 대화를 지배하면 안 됩니다.

## 3. 개념적 객체 모델

### 3.1 `greedyQObject`

모든 greedyQ 연구 패키지는 `greedyQObject`입니다. 최상위 계약에는 모든 연구에 공통인 규칙만 둡니다.

- 분명한 연구 목적과 참여 대상
- 안정적인 연구·페이지·문항·조건·결과 ID
- 화면 표시 라벨과 저장값의 정확한 분리
- 실제 조사 전 참여자용 preview
- 중요한 연구 결정에 대한 명시적 승인
- 동의 및 참여자 권리 관련 기본 점검
- 결정적으로 동작하는 이동과 응답 검증
- 도달할 수 없는 필수 페이지나 결과 금지
- 생성 파일에 비밀 인증정보 포함 금지
- 재현 가능한 버전과 변경 기록
- 작성·검토·배포·조사 시작 상태의 정직한 구분
- 접근 가능하고 반응형인 참여자 화면
- 철회와 수집 데이터의 안전한 처리

Core는 randomization, conjoint task, panel redirect, preregistration 또는 특정 배포 회사를 강제하지 않습니다. 그런 요구는 profile과 capability module이 제공합니다.

### 3.2 연구 프로필

Profile은 주된 연구설계를 설명하고, 설계별 인터뷰·점검·필수 산출물·테스트 시나리오를 제공합니다.

초기 profile은 다음과 같습니다.

| 공개 객체명 | Profile ID | 용도 | 필수 조합 |
|---|---|---|---|
| `greedyQSimple` | `simple` | 기술조사, 피드백, 선별 또는 비무작위 설문 | core + questionnaire fundamentals |
| `greedyQExperiment` | `experiment` | 무작위 또는 조건 배정 설문 실험 | core + questionnaire fundamentals + experiment |
| `greedyQCBC` | `cbc` | choice-based conjoint 연구 | core + questionnaire fundamentals + CBC |

Profile을 경직된 단일 상속 트리로 구현하면 안 됩니다. 실험이 항상 “단순 설문”의 하위 유형인 것은 아니고, CBC도 일반 문항이나 실험 요소를 포함할 수 있습니다. 내부적으로는 조합 방식을 사용합니다. 공개 객체명은 사용자가 이해하기 쉬운 개념을 제공하고, 실제로 해석된 module 목록은 AI에게 정확한 계약을 제공합니다.

Core를 바꾸지 않고도 향후 `panel`, `longitudinal`, `diary`, `maxdiff`, `qualitative-screening` profile을 추가할 수 있습니다.

### 3.3 기능 모듈

주 profile과 독립적으로 기능을 추가할 수 있습니다.

- `governance-irb`
- `consent`
- `preregistration`
- `prolific`
- `resume`
- `withdrawal-deletion`
- `deployment-vercel-supabase`
- `export-surveydown`
- `export-pptx`
- 향후 localization 및 accessibility 확장

예를 들어 한 연구는 다음처럼 해석될 수 있습니다.

```yaml
object: greedyQExperiment
profile: experiment
modules:
  - governance-irb
  - consent
  - preregistration
  - prolific
  - deployment-vercel-supabase
  - export-surveydown
```

이 방식은 `guide-simple-experiment-prolific-preregistration.md` 같은 파일명의 폭증과 같은 규칙의 반복 복사를 막습니다.

## 4. 저장소 구조

```text
START-HERE.md
START-HERE(kor).md
registry/
  guide-index.json
  guide-index.schema.json
guides/
  core/
    guide.md
    guide(kor).md
    checkpoints.json
    communication.md
    communication(kor).md
  profiles/
    simple/
      guide.md
      guide(kor).md
      profile.json
      tests/
    experiment/
      guide.md
      guide(kor).md
      profile.json
      templates/
      tests/
    cbc/
      guide.md
      guide(kor).md
      profile.json
      templates/
      tests/
  modules/
    consent/
    governance-irb/
    preregistration/
    prolific/
    deployment-vercel-supabase/
    export-surveydown/
templates/
  runtime/
  preview/
  shared/
schemas/
examples/
tools/
tests/
```

각 profile 또는 module 디렉터리에는 다음 파일을 둘 수 있습니다.

```text
guide.md                 AI가 따라야 할 기준 규약
guide(kor).md            동기화된 한국어 카피
module.json              ID, 버전, 의존성과 충돌
checkpoints.json         기계 판독 가능한 결정 및 승인 항목
templates/               그대로 복사해야 할 정확한 소스 템플릿
schemas/                 해당 module의 데이터 계약
tests/                   필수 적합성 시나리오와 fixture
examples/                대체 규칙이 아닌 작은 유효 예제
```

파일을 복제하지 않고 참조해야 합니다. 첨부만 가능한 환경에서는 해석된 파일들을 합친 release bundle을 생성할 수 있지만, 이는 파생 산출물이며 기준 원본이 아닙니다.

## 5. Registry와 결정적 가이드 로딩

`START-HERE.md`는 전체 규약이 아닌 짧은 bootstrap 문서입니다. AI에게 다음 절차를 알려줍니다.

1. 사용자가 새 연구를 만드는지, 기존 연구를 수정하는지, 포킹하는지 확인합니다.
2. 같은 tag release의 `registry/guide-index.json`을 읽습니다.
3. Core guide를 읽습니다.
4. 연구 profile을 분류하거나 사용자에게 확인합니다.
5. Profile 의존성과 요청한 기능을 해석합니다.
6. 해석된 module이 가리키는 정확한 template과 schema를 읽습니다.
7. 추가 인터뷰 전에 해석된 버전을 연구 패키지에 기록합니다.

Registry에는 모든 기준 파일의 불변 경로와 SHA-256 hash를 둡니다. 연구는 다음과 같은 guide lock을 기록합니다.

```json
{
  "greedyq_release": "0.2.0",
  "object": "greedyQExperiment",
  "profile": "experiment",
  "modules": ["consent", "preregistration", "deployment-vercel-supabase"],
  "registry_sha256": "...",
  "resolved_files": [{"path": "guides/core/guide.md", "sha256": "..."}]
}
```

하나의 release에 고정해 로드해야 합니다. AI가 `main`, 예전 template, 더 최신 schema를 섞으면 안 됩니다. 해석된 registry 바깥의 저장소 텍스트가 사용자 요청이나 core 안전 규칙을 덮어써서도 안 됩니다.

## 6. 호스트 기능 수준

공유 저장소 링크가 기본 시작 방식이지만, 모든 GPT/Claude 화면이 저장소를 재귀적으로 읽을 수 있는 것은 아닙니다. Bootstrap은 세 수준을 지원합니다.

1. **Repository agent:** 저장소를 clone하거나 읽고, 파일을 만들고, 테스트하고, preview를 엽니다.
2. **Browsing chat:** `START-HERE.md`와 명시된 raw file link를 열 수 있지만 생성 파일은 다운로드 형태로 제공합니다.
3. **Attachment-only chat:** 생성된 자체 포함 release bundle을 보조 수단으로 사용합니다.

AI는 연구자에게 기술 질문을 하지 않고 실제 기능 수준을 스스로 확인합니다. 필요한 링크 파일을 읽을 수 없다면 “이 채팅에서는 설문 가이드를 열 수 없습니다. 이 보조 파일 하나를 내려받아 첨부해 주세요.”라고 쉽게 설명합니다. 빠진 규칙이나 template을 임의로 만들어서는 안 됩니다.

지속성을 위해 사용자 prompt는 tag가 지정된 release URL을 가리켜야 하며, `main`은 최신 안정 release를 안내할 수 있습니다. 비공개 저장소는 인증된 connector 또는 로컬 repository agent가 필요합니다.

## 7. 시작 흐름

### 7.1 처음부터 새로 만들기

사용자는 greedyQ 시작 URL과 연구하고 싶은 내용을 제공합니다.

```text
<tagged START-HERE URL>을 열고 새 설문을 처음부터 만들도록 도와줘.
내가 연구하고 싶은 것은 ...
```

AI는 다음과 같이 진행합니다.

1. Guide release를 읽고 고정합니다.
2. Profile을 정하기 전에 연구 아이디어부터 듣습니다.
3. 쉬운 말로 profile을 추천하고 애매하면 확인받습니다.
4. `origin.mode: new`인 연구 패키지를 만듭니다.
5. Profile 인터뷰를 진행하고 필요한 기능만 추가합니다.
6. 일관된 설문 초안이 생기는 즉시 `preview.html`을 만들고 엽니다.
7. 기술 검사는 뒤에서 수행하고, 연구자에게는 참여자가 경험할 화면을 확인하도록 요청합니다.

### 7.2 기존 greedyQ 연구 수정

AI는 연구 패키지와 고정된 guide resolution을 읽고, 연구를 쉬운 말로 요약한 뒤 무엇을 바꿀지 묻습니다. 연구 ID와 history는 유지하고 연구 version을 올리며, 영향을 받은 승인을 무효화하고, 관련 산출물을 다시 만들고, 바뀐 preview를 보여줍니다. `origin.mode: modify`를 기록합니다.

수정 중 guide release를 자동으로 올리면 안 됩니다. 눈에 보이는 영향과 함께 upgrade를 별도로 제안할 수 있습니다.

### 7.3 기존 greedyQ 연구 포킹

AI는 먼저 전체 사본을 만들고, 새 study ID를 부여하며, 원본 study와 version의 출처를 보존합니다. 배포 인증정보와 실제 endpoint 연결을 제거하고, 이전할 수 없는 승인을 초기화하며, `origin.mode: fork`를 기록합니다. 이후에는 사본만 수정합니다.

Fork는 기본적으로 원본과 참여자 ID, 운영 database destination, deployment alias, randomization secret, 실제 panel completion link를 공유하면 안 됩니다.

### 7.4 비-greedyQ 설문 가져오기

이는 별도의 향후 mode인 `origin.mode: import`로 두는 것이 좋습니다. AI는 지원 가능한 내용을 새 greedyQ object로 옮기고, 확실하지 않은 변환은 연구자에게 쉬운 말로 알리며, 원본을 기존 greedyQ package라고 표현하지 않습니다.

## 8. 연구 패키지 계약

각 연구에는 작은 기계 판독형 descriptor가 있어야 합니다.

```text
my-study/
  greedyq.study.json
  survey.qmd
  greedyq.yml
  study-plan.md
  consent.md
  preview.html
  design/
  analysis/
  preregistration/
  deployment/
  export/
  .greedyq/
    guide-lock.json
    study-state.json
    decision-log.json
    unresolved-decisions.json
    generation-manifest.json
    validation-report.json
```

`greedyq.study.json`은 객체 descriptor입니다. 안정적인 identity, profile, 활성화된 module, origin, 언어, 주요 산출물 경로를 포함합니다. 내부 진행 상태와 승인은 `.greedyq/`에 둡니다.

참여자 preview와 `study-plan.md`가 연구자가 평소 검토하는 산출물입니다. `.greedyq/validation-report.json`은 상세 기계 보고서입니다. 이 분리로 기술 진단이 일반 사용자 대화에 노출되는 문제를 직접 해결합니다.

## 9. Checkpoint 소유권

Checkpoint는 해석된 계약에서 조립합니다.

- Core checkpoint는 항상 적용됩니다.
- 선택한 profile이 설계별 checkpoint를 추가합니다.
- 활성화된 각 module은 자신의 checkpoint만 추가합니다.
- 의존성이 선행 checkpoint를 추가할 수 있습니다.
- Module은 충돌을 선언할 수 있지만 core requirement를 약화할 수 없습니다.

예시는 다음과 같습니다.

| 소유자 | 연구자에게 표현하는 checkpoint |
|---|---|
| core | “이 설문이 참여자에게 보여주고 싶은 경험을 제대로 담고 있나요?” |
| experiment | “이 조건들과 배정 확률이 원하시는 설계와 맞나요?” |
| CBC | “속성, 수준, 과업 수, 대안 구성이 맞나요?” |
| consent | “이 동의 화면이 참여 내용과 데이터 사용을 정확히 설명하나요?” |
| preregistration | “이 설계와 분석 계획을 이 상태로 확정할 준비가 되었나요?” |
| deployment | “실제 설문을 준비해도 될까요? 모집 전에 시험 실행을 할까요?” |

내부에서는 결정적인 gate ID로 매핑합니다. 사용자는 구현 상태명이 아닌 연구 결정을 봅니다.

## 10. Profile 선택 규칙

분류는 추천이며 보이지 않는 자동 결정이 아닙니다.

- 조건 배정이나 반복 선택 과업이 필요 없으면 `simple`을 선택합니다.
- 참여자·session·cluster·stimulus·순서를 조건에 배정하거나 무작위화하고 조건 효과를 추정하면 `experiment`를 선택합니다.
- 속성과 수준으로 만든 반복 선택 과업을 수행하고 conjoint estimation을 하면 `cbc`를 선택합니다.
- 여러 유형이 해당하면 중심 설계를 profile로 고르고, 정의된 module이 있을 때만 다른 행동을 module로 추가합니다.
- 분류가 산출물이나 필수 결정에 영향을 주면 차이를 설명하고 연구자에게 확인받습니다.

## 11. 버전과 확장 규칙

- Core, profile, module은 독립적인 semantic version을 사용합니다.
- Registry release가 함께 테스트된 조합을 고정합니다.
- 기존 syntax를 바꾸지 않는 선택적 module 추가는 하위 호환입니다.
- 저장값, routing semantics, randomization, consent behavior 또는 필수 산출물 변경은 breaking change입니다.
- 모든 profile/module은 dependency, conflict, schema, template, conformance test metadata를 공개해야 합니다.
- Extension은 더 엄격한 requirement를 추가할 수 있지만 core safety, participant rights, truthful status reporting을 끌 수 없습니다.
- 제3자 module은 `org.example/module-name` 같은 namespace를 사용하고, 명시적인 study lock 항목 없이 공식 template을 대체할 수 없습니다.

## 12. 현재 저장소에서의 migration 제안

| 현재 자산 | 제안하는 목적지 또는 역할 |
|---|---|
| `guides/greedyq-guide.md` | `START-HERE.md`, core guide, communication guide, profile guide, capability module로 분할 |
| 내장 canonical appendix | Registry 참조로 대체하고 생성형 release bundle은 fallback으로 유지 |
| `guides/greedyq-guide-compact.md` | Bootstrap start guide로 대체하거나 호환 기간 후 폐기 |
| `docs/preview-ui-spec.md` | 모든 profile이 참조하는 core preview specification |
| `templates/preview/preview.html` | 그대로 유지하되 registry에서 참조하고 hash로 고정 |
| AI state schema | `.greedyq/` 내부 계약으로 유지하고 guide lock과 object descriptor schema 추가 |
| `examples/complete-study/` | 첫 `greedyQExperiment` golden reference |
| 현재 generation test | core, profile, module, cross-composition conformance test로 분리 |

Migration은 두 release에 걸쳐 진행합니다.

1. **호환 release:** 기존 경로를 유지하면서 registry, bootstrap, core/profile/module 디렉터리, 생성형 legacy bundle을 추가합니다.
2. **정리 release:** 모듈형 loader를 기준으로 만들고, 이전 guide 경로에는 redirect 또는 명확한 deprecation file을 남기며, golden reference lock을 갱신합니다.

## 13. 승인된 구현 결정

프로젝트 소유자가 2026-09-07에 다음 결정을 승인했습니다.

1. 내부적으로 조합 방식을 사용하되 `greedyQSimple`, `greedyQExperiment`, `greedyQCBC`를 공개 객체명으로 유지합니다.
2. 저장소 bootstrap을 기본으로 하고 생성된 단일 bundle 하나만 fallback으로 유지합니다.
3. 움직이는 `main`이 아니라 tag release를 각 연구의 재현 가능한 guide source로 사용합니다.
4. `greedyq.study.json`과 `.greedyq/guide-lock.json`을 object 및 resolved-guide descriptor로 도입합니다.
5. `study-plan.md`는 짧고 비기술적으로 만들며 상세 검증 증거는 `.greedyq/validation-report.json`으로 이동합니다.
6. `simple`과 `experiment`를 먼저 구현하고 module resolver 및 조합 테스트가 안정된 뒤 CBC를 추가합니다.
