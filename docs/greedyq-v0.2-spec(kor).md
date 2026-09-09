# greedyQ v0.2 스펙

[English](./greedyq-v0.2-spec.md)

**상태:** Draft normative specification
**스펙 버전:** `0.2.0-draft.1`
**주요 conformance fixture:** `examples/complete-study/` 및 `examples/simple-satisfaction-study/`

## 1. 목적 및 규범 언어

이 스펙은 완전한 최소 greedyQ 연구 형식, web-native runtime 동작, validation contract, native surveydown export 경계를 정의합니다. MUST, MUST NOT, SHOULD, SHOULD NOT, MAY는 규범적 의미로 사용합니다.

greedyQ는 online academic research를 위한 specification-driven, AI-native application입니다. 모듈형 greedyQ bundle은 agent-executable application specification입니다. Capable general-purpose GenAI와 결합하면 이 normative format을 적용하고 연구 artifact와 실행 가능한 survey software를 만드는 greedyQ research agent를 instantiate합니다. greedyQ 자체는 agent가 아니며 그렇게 표현해서는 안 됩니다. Host AI나 interface의 차이가 이 문서의 conformance requirement를 약화해서도 안 됩니다.

greedyQ는 독립 구현입니다. Surveydown 소스 코드를 포함하거나 실행해서는 안 됩니다. 호환성은 공개적으로 문서화된 surveydown-style `survey.qmd` 작성 관례를 대상으로 합니다. 주 runtime은 Vercel과 Supabase에서 실행되는 greedyQ이며, 생성된 native surveydown 파일은 핵심 병렬 출력입니다.

구현은 complete reference study를 parse·validate하고 결정론적으로 normalize할 수 있을 때만 v0.2에 conform합니다. Deployment와 native export conformance는 별도 capability이며 따로 보고해야 합니다.

## 2. 프로젝트 contract

Study root에는 다음 파일이 반드시 있어야 합니다.

```text
survey.qmd
greedyq.yml
```

다음 파일을 선택적으로 포함할 수 있습니다.

```text
design/*.csv
assets/*
supabase/migrations/*.sql
vercel.json
preview.html
export/surveydown/*
```

`survey.qmd`는 순서가 있는 page, 표시 content, question, navigation의 source of truth입니다. `greedyq.yml`은 study identity, governance metadata, consent, logic, randomization, persistence, respondent source, outcome, export policy의 source of truth입니다.

모든 규범 artifact는 `spec_version: "0.2"`을 선언해야 합니다. 알 수 없는 key는 기본적으로 warning을 생성해야 하며 strict mode에서는 error로 승격할 수 있습니다.

## 3. 식별자 및 reference

ID는 `^[a-z][a-z0-9_]{1,63}$`와 일치하고 namespace 내에서 유일해야 하며 데이터 수집이 시작된 뒤에는 안정적으로 유지해야 합니다. Page와 question ID는 하나의 namespace를 공유합니다. Outcome, rule, randomization, consent ID는 별도 namespace를 사용합니다.

다음 ID는 호환성을 위해 reserve하며 page 또는 question ID로 사용해서는 안 됩니다.

```text
session_id time_start time_end exit_survey_rating current_page browser ip_address
```

모든 reference는 정적으로 resolve되어야 합니다. Duplicate ID, missing reference, 아직 사용할 수 없는 이후 값을 참조하면 error입니다.

## 4. `survey.qmd` grammar

### 4.1 Front matter

파일은 `greedyq.spec_version`과 `greedyq.version`을 포함하는 YAML front matter로 시작해야 합니다. `greedyq.version`은 repository의 current release identifier와 같아야 하며 형식은 `0.2_YYYY-MM-DD_<short-commit>`입니다. 새 연구는 participant에게 보이는 연구 주체 또는 연구팀 label인 `greedyq.organization`을 포함해야 하며 1–120자여야 합니다. 이 값이 없는 기존 파일은 중립적인 “Research team” fallback을 표시합니다. v0.2은 문서화된 `theme-settings`, `survey-settings`, `system-messages` namespace를 허용합니다. 지원되지 않는 Quarto 실행 option은 거부해야 합니다.

```yaml
---
greedyq:
  spec_version: "0.2"
  version: "0.2_2026-09-09_3aefdd0"
  organization: "Example University Research Team"
survey-settings:
  show-previous: true
  required: [support_post]
---
```

인식하는 setting key의 hyphen과 underscore는 normalize 이후 동일합니다. Boolean 값은 true 또는 false로 normalize합니다.

### 4.2 Page

Page는 단독 line의 `--- page_id`로 시작하고 다음 page marker 또는 파일 끝에서 종료됩니다. 첫 page marker 앞의 content는 invalid입니다. 명시적인 forward target이 없으면 source order가 page order입니다.

### 4.3 Markdown

v0.2은 heading, paragraph, emphasis, strong text, link, ordered/unordered list, block quote, thematic break, inline code, 실행 불가능한 fenced code, relative 또는 HTTPS source의 image를 지원합니다. Raw HTML과 실행 가능한 Quarto extension은 지원하지 않습니다. Rendered output은 sanitize해야 합니다.

### 4.4 Question

Question은 allowlist된 `sd_question()` call 하나를 포함하는 실행되지 않는 R-style fenced chunk로 선언합니다. Parser는 제한된 expression을 parse해야 하며 R을 실행해서는 안 됩니다.

필수 argument는 `id`, `type`, `label`입니다. v0.2은 surveydown이 문서화한 16개 question control을 모두 구현합니다. `text`, `textarea`, `numeric`, `mc`, `mc_multiple`, `mc_buttons`, `mc_multiple_buttons`, `mc_image`, `mc_multiple_image`, `select`, `slider`, `slider_numeric`, `date`, `daterange`, `matrix`, `matrix_multiple`입니다.

Button control은 `direction`, `selected`, `justified`를 지원합니다. Image control은 option마다 하나의 안전한 relative 또는 HTTPS `image` source가 필요합니다. `daterange`는 순서가 있는 두 날짜 array를 저장합니다. `matrix_multiple`은 row별 선택 value array를 저장합니다. greedyQ native persistence는 array와 row object를 사용하고, surveydown export 시 필요한 pipe-separated 및 wide-column 표현으로 변환합니다.

`slider`는 named option vector를 순서가 있는 labeled scale로 사용하고 선택한 option value를 저장합니다. `slider_numeric`은 숫자 `min`, `max`, 선택적인 양수 `step` argument를 사용합니다. 둘 다 drag와 keyboard 조작이 가능한 native range control로 표시됩니다. `orientation`은 `horizontal`(portable default) 또는 `vertical`일 수 있습니다. Vertical orientation은 greedyQ extension이므로 native surveydown export diagnostic에서 반드시 알려야 합니다.

허용되는 value form은 string, number, boolean, null, `c(...)`, named `c(label = value, ...)`입니다. 임의의 function call, variable lookup, assignment, interpolation, side effect는 error입니다.

모든 named option vector에서 왼쪽은 respondent에게 보이는 표시 label이고 오른쪽은 저장 value입니다. Generator는 반드시 `"Displayed label" = "stored_value"` 방향을 사용해야 하며 반대로 만들면 안 됩니다. 같은 규칙이 `option`, `options`, matrix `row` vector에 적용됩니다. Logic, consent contract, scoring, derivation, data dictionary, analysis plan에서는 저장 value만 사용합니다. Validator는 표시 label/저장 value symbol table을 만들고 consent value, show/skip/validate expression, attention/manipulation-check scoring, derived variable, data-dictionary value를 교차 검사해야 합니다. 참조되거나 문서화된 저장 value가 없으면 blocking error입니다.

### 4.5 Navigation

`sd_nav()` call 또는 terminal outcome을 선언하지 않으면 page에 자동 Next action을 추가합니다. v0.2은 `show_previous`, `show_next`, `page_next`, `label_previous`, `label_next`를 지원합니다. Back navigation은 유효한 answer를 보존해야 하며 저장된 random assignment를 변경해서는 안 됩니다.

## 5. `greedyq.yml`

Root key는 다음과 같습니다.

```text
spec_version study governance consent respondents runtime persistence
logic randomization preregistration outcomes export
```

알 수 없는 root key는 strict mode에서 error입니다. Secret은 이 파일에 포함해서는 안 됩니다.

Generator는 `examples/complete-study/greedyq.yml`의 canonical key name과 shape을 사용해야 하며 alias나 대체 object shape을 발명하면 안 됩니다. 이 specification이 normalization을 명시적으로 정의한 경우에만 alias를 허용합니다.

## 6. Expression language

Expression은 greedyQ가 parse하는 string입니다. v0.2은 literal, answer 및 stored-value identifier, parenthesis, `==`, `!=`, `<`, `<=`, `>`, `>=`, `and`, `or`, `not`, `in`, pure function `answered(id)`, `length(value)`, `contains(collection, value)`를 허용합니다.

평가는 결정론적이고 side-effect free여야 합니다. Missing value는 null로 평가합니다. `value == null`을 제외한 null 비교는 false입니다. Type-invalid expression은 조용히 coerce하지 않고 validation에 실패해야 합니다.

## 7. Logic 및 lifecycle

`logic.show`는 visibility를, `logic.skip`은 forward destination을, `logic.validate`는 page 이탈 차단을 제어합니다. Rule은 stable ID를 가져야 하며 declaration order로 평가합니다. 동시에 true일 수 있는 충돌 skip rule은 명시적 priority가 없으면 error입니다.

숨겨진 미응답 question은 null을 유지합니다. 이전 answer 변경으로 응답한 question이 숨겨질 때 기본 policy는 `clear_on_hide`이며 clearing event를 기록해야 합니다. Unreachable page, 명시적 bounded loop가 없는 cycle, outgoing navigation이 있는 terminal page는 error입니다.

Lifecycle state는 `created`, `consented`, `in_progress`, `completed`, `screened_out`, `consent_refused`, `withdrawn`, `technical_error`입니다. 정의된 transition만 허용하며 모든 terminal transition에는 timestamp를 기록해야 합니다.

## 8. Governance 및 consent

Governance metadata는 승인 또는 compliance를 주장하지 않으면서 기관 context를 기록합니다. Protocol title, institution, review status, protocol identifier, investigator contact, data contact, jurisdiction note를 지원합니다.

AI workflow는 초기 topic, objective, broad design을 이해한 뒤 `governance_timing`을 `now` 또는 `after_instrument_draft`로 기록해야 합니다. Detailed governance collection은 연기할 수 있지만, 초기 minimal triage에서 vulnerable population, sensitive/directly identifying data, deception/incomplete disclosure, elevated-risk procedure, regulated intervention, known institutional restriction을 확인해야 합니다. Design-changing concern은 instrument work를 계속하기 전에 해결하거나 blocking으로 명시해야 합니다.

Consent는 versioned여야 하며 ID, version, effective date, document path, confirmation question, refusal outcome을 포함해야 합니다. Consent acceptance는 연구 response를 수집하기 전에 document version, content hash, timestamp, session ID를 기록해야 합니다. Refusal은 최소 operational event record 외에 연구-response row를 만들면 안 됩니다.

Consent amendment는 재확인을 요구해야 합니다. Withdrawal policy는 연구자 설정과 적용 의무에 따라 이미 수집한 response를 retain, anonymize, delete 중 어떻게 처리하는지 명시해야 하며 greedyQ는 설정된 policy가 법적으로 충분하다고 주장해서는 안 됩니다.

Detailed work를 연기하면 draft preview에 눈에 띄는 placeholder governance 및 consent content를 사용할 수 있습니다. 이를 reviewed 또는 approved로 표현하면 안 됩니다. Detailed governance, privacy, withdrawal, retention, participant-facing consent는 coherent instrument draft 후 interactive preview approval 전에 확인해야 합니다. 이 confirmation이 기록되기 전에는 production deployment를 차단해야 합니다.

Deletion-on-withdrawal을 선택하면 runtime은 operation을 atomic하고 idempotent하게 수행해야 합니다. Session을 lock하고, 설정에 따라 research answer, assignment, external identifier를 삭제하고, 명시된 최소 operational record만 유지하며, terminal lifecycle event를 append하고, 실패 시 전체 operation을 rollback해야 합니다. 생성되는 Supabase project는 `examples/complete-study/supabase/migrations/001_initial.sql`의 검토된 canonical implementation을 출발점으로 사용해야 합니다. Study-specific deviation은 문서화하고 researcher 승인을 받아야 합니다.

## 9. Respondent source 및 Prolific

Generic respondent contract는 allowlist된 inbound parameter, validation, canonical identifier, duplicate policy, outcome redirect를 정의합니다. Raw query parameter는 명시적으로 allowlist하지 않으면 저장해서는 안 됩니다.

Prolific preset은 `PROLIFIC_PID`, `STUDY_ID`, `SESSION_ID`를 인식합니다. Panel run에서는 consent 전에 유효한 participant ID가 필요합니다. Duplicate behavior는 `resume`, `reject`, `allow` 중 하나여야 하며 v0.2 default는 `resume`입니다. Completion, screen-out, consent-refusal, technical-error route는 서로 달라야 하고 test mode에서는 production redirect를 차단해야 합니다.

## 10. Randomization

v0.2은 simple 및 fixed-block between-subject assignment를 지원합니다. Randomization은 ID, unit, method, condition, allocation, assignment point, persistence key, stored metadata를 선언합니다.

Assignment는 consent 이후이면서 첫 condition-dependent page 직전에만 이루어져야 합니다. Stimulus 표시 전에 atomic하게 저장하고 refresh/resume 동안 불변이어야 하며 동일한 persistence key에 대해 다시 계산해서는 안 됩니다. Stored metadata에는 condition, method, seed 또는 draw identifier, 해당되는 경우 block identifier, assignment timestamp, specification version을 포함해야 합니다.

## 11. Persistence 및 privacy

Supabase/PostgreSQL은 v0.2 live persistence target입니다. Native schema는 session, consent event, answer, assignment, lifecycle event, external identifier를 분리합니다. Server credential은 deployment environment variable에만 둬야 합니다. Browser와 IP 수집은 기본적으로 꺼져 있습니다.

Partial answer는 성공한 page transition에서 저장해야 합니다. Resume은 마지막 committed page, valid answer, consent version, lifecycle state, random assignment를 복원해야 합니다. Multiple-choice response는 pipe-delimited string이 아니라 array로 저장합니다. Analysis export는 문서화된 wide representation을 만들 수 있습니다.

Row Level Security는 respondent가 다른 respondent의 데이터를 읽지 못하게 해야 합니다. Administrative analysis access는 별도로 인증된 role을 사용해야 합니다.

RLS enablement, grant, policy는 함께 검증해야 합니다. 일치하는 policy가 없는 grant는 usable access가 아닙니다. Canonical migration은 제한된 analyst access boundary를 제공하고 external identifier를 제외하며 completed non-test session과 answer를 문서화된 export shape으로 노출해야 합니다. 생성 migration은 canonical migration을 기반으로 하고 문서화되고 검증된 변경으로만 확장해야 합니다.

## 12. Validation 및 diagnostic

Diagnostic은 `code`, `severity`, `message`, `file`, `location`, 선택적인 `related_ids`, `suggested_fix`를 포함해야 합니다. Stable v0.2 code는 다음과 같습니다.

| Code | Severity | 의미 |
| --- | --- | --- |
| `GQ001` | error | Invalid 또는 duplicate identifier |
| `GQ002` | error | Unresolved reference |
| `GQ003` | error | 지원하지 않는 executable expression |
| `GQ004` | error | Unreachable page 또는 invalid cycle |
| `GQ005` | error | Ambiguous navigation 또는 skip logic |
| `GQ006` | error | 누락되거나 invalid한 consent contract |
| `GQ007` | error | Randomization persistence 정의 누락 |
| `GQ008` | error | 불완전한 respondent-source contract |
| `GQ009` | error | Secret 또는 unsafe redirect 감지 |
| `GQ010` | error | Preregistration에 unresolved 또는 inconsistent commitment 포함 |
| `GQ011` | error | 표시 label/저장 value contract 불일치 |
| `GQ012` | error | AI state artifact가 published JSON Schema 검증 실패 |
| `GQ013` | error | 생성된 persistence, withdrawal, RLS 또는 analysis-export contract 불완전 |
| `GQ110` | warning | Methodological concern이 researcher 검토 대기 중 |
| `GQ101` | warning | Native export에서 greedyQ-only인 기능 |
| `GQ102` | warning | Native export가 storage representation을 변경함 |

Validation은 결정론적이어야 합니다. 동일한 byte와 validator version은 동일한 diagnostic과 normalized AST를 생성합니다.

`greedyq`, `theme-settings`, `survey-settings`, `system-messages`의 unknown front-matter key는 strict 또는 generation mode에서 error여야 합니다. Implementation은 accepted-key allowlist, type, enum value, canonical spelling을 공개해야 하며 비슷해 보이는 invented key를 조용히 normalize하면 안 됩니다.

모든 `.greedyq/*.json` artifact는 generation manifest에 기록하기 전에 `schemas/ai/`의 정확한 published schema로 검증해야 합니다. Generator는 schema를 읽고 canonical template을 사용하며 field나 enum value를 발명하지 않아야 합니다. 실패 시 `validated` checkpoint를 보고하면 안 되며 schema validation을 사용할 수 없으면 unvalidated로 표시해야 합니다.

Treatment confounding, contamination, construct validity, questionable exclusion 같은 methodological concern은 hard syntax error가 아닙니다. LLM은 concern과 구체적 option을 설명하고 unresolved decision으로 기록한 뒤 해당 checkpoint에서 명시적 researcher 결정을 받아야 합니다. Validator는 `GQ110`을 낼 수 있지만 design을 조용히 변경하면 안 됩니다.

## 13. Preregistration output 및 fielding gate

Preregistration은 핵심 generated output입니다. `greedyq.yml`은 template adapter, output directory, registration status, fielding gate를 식별해야 합니다. v0.2은 `osf_preregistration`과 `generic_markdown`을 지원하며 추가 registry template은 study model 변경이 아니라 adapter입니다.

Package는 사람이 읽을 수 있는 Markdown draft, 기계가 읽을 수 있는 JSON representation, 등록 대상 study·consent·stimuli·analysis-plan의 정확한 version을 다루는 SHA-256 artifact manifest를 포함해야 합니다. Hypothesis, design, sampling plan, stopping rule, exclusion, condition, randomization, variable, primary/secondary outcome, analysis model, missing-data handling, 알려진 deviation 또는 unresolved decision을 포함해야 합니다.

LLM은 누락된 중요한 commitment를 연구자에게 질문해야 하며 이를 지어내면 안 됩니다. 모든 unresolved item은 눈에 띄게 표시하고 `ready_for_submission`을 차단해야 합니다. Draft 생성은 submission이 아닙니다. External draft 생성, 제출, public release 또는 embargo 선택, sample collection 시작은 서로 다른 action입니다. 각 external mutation에는 적절한 권한이 필요하며 submission과 public/embargo 선택에는 연구자의 명시적 승인 및 결과 registry state 검증이 필요합니다.

연구자가 preregistration package를 승인하면 greedyQ는 immutable local snapshot을 기록하고 대상 artifact hash가 변경된 경우 fielding을 차단해야 합니다. 변경에는 문서화된 amendment 또는 새 preregistration version이 필요하며 greedyQ는 승인된 record를 조용히 다시 생성하면 안 됩니다. Registry-specific behavior는 변경될 수 있으므로 adapter는 대상 external template/version을 선언해야 하고 검증 없이 성공적인 registration을 주장하면 안 됩니다.

## 14. Web-native runtime

Primary renderer는 static asset으로 Vercel에 배포할 수 있는 browser-native JavaScript application입니다. 검증된 AST만 사용하고 sanitize된 content를 render하며 client feedback과 authoritative Supabase/PostgreSQL validation 및 transaction을 수행하고 로컬 Python, Node.js 또는 framework runtime을 요구하지 않습니다.

Instrument review는 prose-first가 아니라 preview-first여야 합니다. Coherent instrument가 생기면 generator는 browser-testable preview를 생성하고 host가 interactive artifact 또는 browser control을 지원하면 직접 열어야 합니다. 그렇지 않으면 self-contained `preview.html`을 제공해야 합니다. `study.md`를 함께 제공할 수 있지만 respondent-flow review를 대신하면 안 됩니다.

Normative layout, question state, validation, responsive, accessibility, researcher control, safety, scenario suite, review evidence requirement는 `docs/preview-ui-spec.md`에 정의합니다. 해당 문서와 canonical runtime은 full AI guide에 내장되므로 guide가 유일한 attachment인 경우에도 적용됩니다.

Preview는 validated AST 위에서 fixed trusted runtime을 사용하고 survey-authored JavaScript를 실행하지 않으며 external write와 production redirect를 차단해야 합니다. Navigation, required check, show/skip logic, stored value, assignment, back navigation, resume, terminal outcome을 실행할 수 있어야 합니다. Researcher-only debug panel과 deterministic condition/path selector를 제공하는 것이 좋습니다. 생성 또는 자동 열기만으로 review가 되지는 않습니다. `interactive_preview_reviewed`는 hands-on test 후 명시적 researcher confirmation을 요구하며, preview 불가를 명시적으로 수용하고 기록하지 않는 한 `deployment_candidate` gate입니다.

Preview mode는 production이 아닌 outcome handling을 사용하고 preview임을 눈에 띄게 표시해야 합니다. 필수 environment variable, migration, redirect configuration이 없으면 production deployment는 fail closed해야 합니다. Tool 또는 AI는 live endpoint와 persistence health를 검증하지 않고 성공적인 deployment를 보고해서는 안 됩니다.

## 15. Native surveydown export

Exporter는 동일한 검증된 AST를 사용하고 최소한 `survey.qmd`, `app.R`, 필요한 question/design file, asset, `compatibility-report.json`을 포함하는 self-contained export directory를 생성합니다.

모든 기능은 다음과 같이 분류합니다.

- `directly_portable`: semantic change 없이 compatible QMD로 생성
- `generated`: 결정론적 `app.R` 또는 보조 파일로 변환
- `greedyq_only`: 명시적 warning이 있을 때만 생략 또는 근사
- `unsupported`: export 실패

생성된 `app.R`은 surveydown R package에 의존할 수 있지만 surveydown 소스를 복사하지 않고 greedyQ template과 AST transform으로 작성해야 합니다. Compatibility report에 중요한 mismatch가 있으면 export가 behavior equivalence를 주장해서는 안 됩니다.

## 16. Reference study acceptance criteria

Complete reference study는 다음을 입증해야 합니다.

1. Governance metadata와 versioned consent
2. Prolific parameter validation과 duplicate resume
3. Pre-treatment measure
4. 저장되는 treatment/control assignment
5. Condition-specific stimulus display
6. Manipulation, attention, Likert, choice, numeric, free-text question
7. Conditional display와 skip logic
8. Privacy를 존중하는 demographic
9. Partial save, resume, withdrawal, deletion-request 기록
10. 구분된 completion, screen-out, refusal, error outcome
11. 사람이 읽고 기계가 읽을 수 있는 preregistration artifact 및 artifact-hash manifest
12. Supabase migration과 Vercel configuration
13. Native surveydown export expectation

Python reference implementation은 개발 중 예상 grammar와 runtime semantics를 확립할 수 있지만 최종 사용자 prerequisite로 제시하면 안 됩니다. Production parser, validator, compiler, preview, respondent renderer는 로컬 Python 또는 Node.js 설치 없이 modern browser에서 실행되어야 합니다. Platform-neutral core는 text/data input을 받아야 하며 filesystem 또는 Node-specific API에 의존하면 안 됩니다.

Browser implementation은 Python reference와 동일하게 독립 작성된 conformance fixture로 테스트해야 합니다. 동일 input은 의미론적으로 동등한 normalized AST, stable diagnostic, route, condition, stored value, participant-visible behavior를 생성해야 합니다. 의미적 영향이 없는 implementation-language-specific metadata와 serialization ordering은 다를 수 있습니다. Cross-runtime conformance suite를 통과하기 전에는 production ready라고 주장하면 안 됩니다.

## 17. v0.2에서 deferred된 기능

임의의 R/Shiny 또는 JavaScript, raw HTML, custom Quarto extension, image question, date range, multiple-response matrix, arbitrary widget, weighted/stratified allocation, factorial/conjoint 실행, electronic signature, 관할별 compliance automation은 deferred입니다.

## 18. Versioning

Breaking grammar 또는 semantic change에는 새 specification version이 필요합니다. Fielded study는 greedyQ specification, validator, runtime, schema migration, consent document, preregistration package, guide, export-generator version을 고정해야 합니다. 생성 artifact는 source commit과 configuration을 재현하기에 충분한 provenance를 포함해야 합니다.
