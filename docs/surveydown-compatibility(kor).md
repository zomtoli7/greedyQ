# Surveydown 호환성 조사

[English](./surveydown-compatibility.md)

**상태:** 조사 초안

**조사 기준일:** 2026-09-07

**Surveydown package snapshot:** `1.3.0`, commit [`8af8f55`](https://github.com/surveydown-dev/surveydown/commit/8af8f5504a54246b9c01706a6dd484389afaf588), 2026-06-23 commit

**문서 snapshot:** commit [`f1325a3`](https://github.com/surveydown-dev/website/commit/f1325a32ad937817bb23bc017356f0636ef6d8da)

**문서 역할:** surveydown의 공개 authoring surface에 대한 기술적 목록과 greedyQualt v0.1의 제안 호환 범위

## 1. 범위 및 용어

이 문서는 surveydown 공식 문서, package reference, source repository, 유지 관리되는 예제를 바탕으로 동작을 기록합니다. 이는 규범적 greedyQualt v0.1 스펙을 위한 조사 자료이며 그 자체가 구현 보증은 아닙니다.

제안하는 greedyQualt 분류는 다음과 같습니다.

| 분류 | 의미 |
| --- | --- |
| **v0.1 target** | 첫 규범적 greedyQualt 스펙 및 MVP에 포함할 예정 |
| **Post-v0.1** | MVP 이후 호환 또는 동등 동작을 제공하는 것이 바람직함 |
| **Native replacement** | R/Shiny 대신 greedyQualt 선언형 기능으로 사용 사례 지원 |
| **Deferred** | 가치가 있지만 호환 방식에 추가 조사 또는 구현 성숙도가 필요함 |
| **Unsupported by design** | greedyQualt의 보안, 런타임 또는 제품 원칙과 충돌함 |

호환성은 가능한 범위에서 문서화된 authoring contract와 호환됨을 의미합니다. surveydown의 R object, Shiny internals, 생성 HTML, CSS 또는 데이터베이스 구현을 재현한다는 뜻은 아닙니다.

## 2. 핵심 조사 결과

1. surveydown 프로젝트의 중심은 `survey.qmd`와 `app.R`입니다. 전자는 정적 페이지, 문항, 콘텐츠, navigation을 포함하고 후자는 Shiny 앱, 데이터베이스 연결, reactive question, conditional logic, randomization을 생성합니다.
2. 현재 surveydown은 권장 `--- page_id` shorthand와 명시적 `::: {.sd_page id=page_id}` fence의 두 가지 페이지 문법을 지원합니다.
3. Navigation은 자동으로 삽입됩니다. `sd_nav()`가 개별 페이지를 override하고 `show-previous`가 전체 Previous 버튼을 제어합니다.
4. 공개 `sd_question()` API에는 button, image, multiple-response matrix variant를 포함한 16개 문항 타입이 있습니다.
5. 문항은 inline으로 선언하거나 root/custom YAML 파일에서 ID로 불러올 수 있습니다.
6. YAML은 완전한 theme, behavior, system-message surface와 `database`, `preview`, `local`의 세 storage mode를 제공합니다.
7. Conditional showing, forward skipping, stopping/validation, reactive value, reactive question, 임의 계산은 R/Shiny server code에 존재합니다.
8. Randomization은 선언된 study primitive가 아니라 programming pattern입니다. 작성자는 `app.R`에서 무작위 값을 생성하거나 불러오고, 명시적으로 저장하고, reactive question을 `sd_output()`으로 표시합니다.
9. surveydown은 session당 하나의 wide response row를 사용합니다. PostgreSQL table을 자동 생성·확장하고 `session_id`를 primary key로 사용하며 값을 text column으로 기록합니다.
10. Cookie가 session ID, current page, answer를 보존합니다. Database/CSV data는 페이지 전환과 browser/session 종료 시 갱신됩니다.
11. greedyQualt는 대부분의 정적 QMD authoring을 보존하면서 `app.R`을 버전이 명시된 선언형 스펙으로 교체할 수 있습니다. 임의의 R/Shiny 동작은 일반적으로 변환할 수 없으며 설계상 지원하지 않습니다.
12. AI-guided creation이 greedyQualt의 주요 경험이므로 compatibility detail은 expert author를 위한 prose에 머물지 않고 결정론적 generation rule과 validator diagnostic으로 표현할 수 있어야 합니다.

## 3. 프로젝트 및 런타임 모델

### 3.1 Surveydown

공식 [Basic Components](https://surveydown.org/docs/basic-components) 문서는 두 필수 파일을 정의합니다.

```text
survey.qmd  # pages, Markdown, questions, navigation, static outputs
app.R       # database, Shiny server, reactivity, logic, runtime launch
```

최소 runtime model은 다음과 같습니다.

```r
library(surveydown)

db <- sd_db_connect()
ui <- sd_ui()

server <- function(input, output, session) {
  sd_server(db)
}

shiny::shinyApp(ui = ui, server = server)
```

`survey.qmd`는 parse 및 render되어 `_survey/` directory를 생성합니다. 공식 문서는 생성된 `settings.yml`을 편집하지 말라고 안내하며 source configuration은 `survey.qmd`에 둡니다.

### 3.2 greedyQualt 경계

```text
survey.qmd             -> compatible static authoring surface
questions*.yml         -> compatible question definitions where specified
greedyqualt.yml        -> native logic, randomization, lifecycle, persistence
design/*.csv           -> native experimental designs
app.R                  -> migration input only; never executed
```

| Surveydown component | 제안 greedyQualt 처리 |
| --- | --- |
| `survey.qmd` | **v0.1 target** |
| Root `questions.yml` | **v0.1 target** |
| Custom question YAML path | **Post-v0.1** |
| `app.R` 표준 pattern | **Native replacement** 및 migration diagnostic |
| 임의의 R/Shiny code | **Unsupported by design** |
| 생성된 `_survey/` 파일 | 호환성 대상 아님 |
| RStudio gadget / sdstudio | 제품 대상 아님 |

## 4. QMD document 및 page grammar

### 4.1 YAML front matter

YAML header는 선택 사항이며 생략하면 surveydown default가 적용됩니다. Quarto format option도 여기에 포함될 수 있습니다.

```yaml
---
theme-settings:
  theme: default

survey-settings:
  show-previous: no
  all-required: no
---
```

greedyQualt는 이해하는 세 surveydown namespace를 parse하고 임의의 Quarto configuration을 조용히 수용하는 대신 diagnostic을 제공해야 합니다.

### 4.2 Page syntax

권장 shorthand:

```markdown
--- welcome

# Welcome

--- questions

# Questions
```

Legacy/explicit fence syntax:

```markdown
::: {.sd_page id=welcome}

# Welcome

:::
```

| 기능 | Surveydown 동작 | 제안 greedyQualt 분류 |
| --- | --- | --- |
| `--- page_id` | 페이지를 열고 이전 페이지를 암묵적으로 닫음 | **v0.1 target** |
| `.sd_page` fence | 명시적 페이지 경계 | **Post-v0.1** |
| Markdown content | Quarto/Markdown을 통해 render | **v0.1 target**, 문서화된 안전 subset |
| Raw HTML | Upstream rendering stack에서 허용 | **Deferred**, 기본 sanitize |
| 임의 Quarto extension | Quarto를 통해 사용 가능 | 명시적으로 채택하지 않는 한 **Unsupported by design** |
| 중복/겹치는 ID | Reserved ID를 포함해 거부 | **v0.1 target** |

Package source에서 확인된 upstream reserved ID는 다음과 같습니다.

```text
session_id
time_start
time_end
exit_survey_rating
current_page
browser
ip_address
```

greedyQualt의 실제 데이터 모델이 다른 column name을 사용하더라도 migration compatibility를 위해 이 이름을 reserve해야 합니다.

## 5. 문항

공식 [Question Types](https://surveydown.org/docs/question-types)와 [`sd_question()` reference](https://pkg.surveydown.org/reference/sd_question)가 공개 question surface를 정의합니다.

### 5.1 선언 형식

Inline 선언:

```r
sd_question(
  id = "favorite_penguin",
  type = "mc",
  label = "Which type of penguin do you like the best?",
  option = c(
    "Adélie" = "adelie",
    "Chinstrap" = "chinstrap",
    "Gentoo" = "gentoo"
  )
)
```

Question YAML:

```yaml
favorite_penguin:
  type: mc
  label: Which type of penguin do you like the best?
  options:
    Adélie: adelie
    Chinstrap: chinstrap
    Gentoo: gentoo
```

```r
sd_question("favorite_penguin")
sd_question(id = "age", yml = "questions/demographics.yml")
```

`option`과 `options`는 alias이며 둘 다 있으면 `option`이 우선합니다. Named vector는 표시 label과 저장 value를 구분합니다. Image question을 제외하면 unnamed value는 표시와 저장에 모두 사용됩니다. Image question에서 unnamed option은 caption을 숨깁니다.

### 5.2 문항 타입 matrix

| Type | Upstream semantics | 주요 데이터 동작 | 제안 greedyQualt 분류 |
| --- | --- | --- | --- |
| `text` | Single-line text input | Scalar value 하나 | **v0.1 target** |
| `textarea` | Multi-line text input | Scalar value 하나 | **v0.1 target** |
| `numeric` | Numeric input | Numeric-looking value 하나 | **v0.1 target** |
| `mc` | Single-choice radio group | Option value | **v0.1 target** |
| `mc_multiple` | Multiple-choice checkbox group | Upstream은 pipe-separated로 저장 | **v0.1 target** |
| `mc_buttons` | Single-choice button | Option value | **Post-v0.1** |
| `mc_multiple_buttons` | Multiple-choice button | Upstream은 pipe-separated로 저장 | **Post-v0.1** |
| `mc_image` | Single-choice image card | Option value, caption 선택 가능 | **Post-v0.1** |
| `mc_multiple_image` | Multiple-choice image card | Multiple value | **Post-v0.1** |
| `select` | Dropdown | Option value | **v0.1 target** |
| `slider` | Discrete labeled slider | 선택된 option value | **v0.1 target** |
| `slider_numeric` | Numeric single/range slider | Scalar 또는 range | **v0.1 target** |
| `date` | Date input, upstream default는 오늘 | Date value | **v0.1 target** |
| `daterange` | Date-range input | Endpoint 두 개 | **Post-v0.1** |
| `matrix` | Row당 radio 하나 | Upstream은 `<id>_<row_id>` column | **v0.1 target** |
| `matrix_multiple` | Row당 checkbox 복수 | Row별 value, upstream pipe joining | **Post-v0.1** |

greedyQualt는 논리적 response shape와 migration/export 동작을 보존해야 하지만 내부 native database에서 pipe-separated 또는 wide-column 물리 저장 방식을 재현할 필요는 없습니다.

### 5.3 `sd_question()` argument 목록

| Argument | Upstream 목적 | 제안 greedyQualt 분류 |
| --- | --- | --- |
| `id`, `type`, `label` | Identity와 핵심 정의 | **v0.1 target** |
| `option`, `options` | 표시/저장 value 선택지 | **v0.1 target** |
| `row` | Matrix row label/ID mapping | **v0.1 target** |
| `selected`, `default` | 초기 choice 또는 slider value/range | **v0.1 target** |
| `placeholder` | Text/textarea placeholder | **v0.1 target** |
| `width`, `height`, `cols`, `resize` | Size/layout control | **Post-v0.1** |
| `direction` | Horizontal/vertical button group | **Post-v0.1** |
| `status`, `individual`, `justified` | Shiny button styling | **Deferred**, portable한 경우만 mapping |
| `label_select` | Select placeholder | **v0.1 target** |
| `grid`, `force_edges` | Slider presentation | **Post-v0.1** |
| `image` | Option과 평행한 image path/URL | **Post-v0.1** |
| `option_attr` | Option별 HTML attribute | Raw form은 **Unsupported by design** |
| `yml` | 외부 question-definition path | **Post-v0.1**, root default는 v0.1 |
| `matrix_question_width` | Matrix prompt-column width | **Post-v0.1** |
| `...` | 임의의 input-specific Shiny argument | **Unsupported by design**, portable argument만 명시적으로 allowlist |

Label과 일반 option label은 upstream에서 Markdown을 지원합니다. Raw HTML도 가능하지만 greedyQualt는 sanitization과 portable Markdown subset을 정의해야 합니다.

## 6. Navigation 및 종료

공식 [Page Navigation](https://surveydown.org/docs/page-navigation) 문서에 따르면 page-level navigation 또는 close 동작이 명시되지 않은 경우 Next 버튼이 자동 삽입됩니다.

| Surface | Upstream 동작 | 제안 greedyQualt 분류 |
| --- | --- | --- |
| Automatic Next | 기본적으로 페이지에 추가 | **v0.1 target** |
| Global `show-previous` | 모든 페이지에서 Previous 활성화 | **v0.1 target** |
| `sd_nav()` | Page-level Previous/Next override | **v0.1 target** |
| `page_next` | 직접 forward target | **v0.1 target** |
| Custom navigation label | `label_previous`, `label_next` | **v0.1 target** |
| Button 숨김 | `show_previous`, `show_next` | **v0.1 target** |
| `sd_next()` | Legacy single Next button | **Post-v0.1** parser alias |
| `sd_close()` | Exit flow, optional rating/restart/cookie clear | Basic exit **v0.1**, 확장 option **Post-v0.1** |
| `sd_redirect()` | Static/reactive redirect, delay, new tab | Static redirect **v0.1**, reactive redirect **Native replacement** |
| 빈 terminal page | Forward control 없음 | **v0.1 target** |

현재 `sd_nav()` source signature는 `show_previous`를 사용하지만 일부 narrative documentation은 `show_prev`를 사용합니다. greedyQualt는 package reference/source signature를 따르고 narrative alias에는 유용한 diagnostic을 제공할 수 있습니다.

## 7. Survey settings

공식 [Survey Settings](https://surveydown.org/docs/survey-settings)의 default 구조는 세 section으로 구성됩니다. YAML key에서 hyphen과 underscore는 서로 바꾸어 사용할 수 있고 YAML boolean은 `yes`/`no` 및 `true`/`false`를 허용합니다.

### 7.1 Theme settings

| Key | Upstream default/동작 | 제안 greedyQualt 분류 |
| --- | --- | --- |
| `theme` | `default`, Quarto를 통한 Bootswatch/custom SCSS | Portable named theme **Post-v0.1**, arbitrary SCSS deferred |
| `barposition` | `top`, `bottom` 또는 `none` | **v0.1 target** |
| `barcolor` | Theme primary color | **v0.1 target** |
| `footer`, `footer-left`, `footer-center`, `footer-right` | Footer content | **v0.1 target** |

Upstream progress는 page가 아니라 답변한 question마다 증가합니다.

### 7.2 Survey settings

| Key | Upstream default | 제안 greedyQualt 분류 |
| --- | --- | --- |
| `mode` | `database`, `preview`, `local`도 지원 | 동등 environment **Native replacement** |
| `show-previous` | `no` | **v0.1 target** |
| `use-cookies` | `yes` | **v0.1 target**, 명시적 privacy semantics 필요 |
| `auto-scroll` | `no` | **Post-v0.1** |
| `rate-survey` | `no` | **Post-v0.1** |
| `all-required` | `no` | **v0.1 target** |
| `required` | `[]` | **v0.1 target** |
| `start-page` | 실제로 첫 페이지, default material은 `initial_page` 명명 | **v0.1 target** |
| `system-language` | `en`, upstream은 `de`, `es`, `fr`, `it`, `zh-CN` 포함 | **Post-v0.1**, v0.1부터 i18n-ready |
| `highlight-unanswered` | `yes` | **v0.1 target** |
| `highlight-color` | `gray`, 문서화된 palette | **Post-v0.1** |
| `capture-metadata` | `yes`, browser 및 IP | **Deferred**, greedyQualt에서는 privacy-first 및 opt-in |
| `all-shuffled` | `no` | 지원 타입에 대해 **v0.1 target** |
| `shuffled` | `[]` | 지원 타입과 index syntax에 대해 **v0.1 target** |

Upstream option shuffling은 `mc`, `mc_buttons`, `mc_multiple`, `mc_multiple_buttons`에 적용되고 row shuffling은 `matrix`에 적용됩니다. `shuffled`는 전체 question ID 또는 `1-5`, `[1, 2, 4]`, `[1-5, 8-10]`과 같은 1-based range/list를 허용합니다.

### 7.3 System messages

공개 key는 다음과 같습니다.

```text
cancel
confirm-exit
sure-exit
submit-exit
warning
required
rating-title
rating-text
rating-scale
previous
next
exit
close-tab
choose-option
click
redirect
seconds
new-tab
redirect-error
```

핵심 navigation, validation, selection, exit, redirect message는 **v0.1 target**입니다. Survey-rating message는 해당 기능과 함께 **Post-v0.1**입니다.

## 8. Conditional logic 및 value

공식 [Conditional Logic](https://surveydown.org/docs/conditional-logic), [Accessing Values](https://surveydown.org/docs/accessing-values), [Reactivity](https://surveydown.org/docs/reactivity) 문서는 R/Shiny 동작을 설명합니다.

| Upstream function/pattern | Semantics | 제안 greedyQualt 처리 |
| --- | --- | --- |
| `sd_show_if(condition ~ target)` | True일 때 question 또는 page 표시 | **Native replacement**, v0.1 선언형 rule |
| `sd_skip_if(condition ~ page)` | True일 때 forward skip | **Native replacement**, v0.1 선언형 rule |
| `sd_stop_if(condition ~ message)` | Navigation을 막고 validation error 표시 | **Native replacement**, v0.1 선언형 rule |
| `sd_is_answered(id)` | Answer-completeness predicate, matrix는 모든 row 필요 | **Native replacement**, v0.1 expression function |
| `sd_value()` / `sd_values()` | Reactive answer lookup 및 type conversion | **Native replacement**, expression reference |
| `sd_store_value()` | Derived/custom value 저장 | **Native replacement**, v0.1 assignment primitive |
| `sd_output(type = "value")` | Answer 또는 stored value 표시 | **Native replacement**, v0.1 interpolation |
| `sd_output(type = "question")` | Server-defined reactive question render | **Deferred**, declared dynamic property 선호 |
| `sd_output()` label mode | Option 또는 question label 표시 | **Post-v0.1** |
| `sd_reactive()` | Reactive value 계산 및 저장 | **Native replacement**, v0.1 core 이후 safe expression graph |
| `sd_copy_value()` | Shiny output ID uniqueness workaround | Web renderer에서는 호환 필요 없음 |
| Custom R function | 임의 condition/calculation logic | **Unsupported by design** |
| `observe()` 및 Shiny reactive | 임의 reactive programming | **Unsupported by design** |

greedyQualt expression language는 literal, answer reference, stored value, boolean operator, comparison, membership, length, answer status, 작은 pure-function allowlist를 지원해야 합니다. 임의 function call과 side effect는 거부해야 합니다.

## 9. Randomization

surveydown 공식 [Randomization](https://surveydown.org/docs/randomization) 안내는 `app.R`의 일반 R을 사용합니다.

1. `sample()`과 같은 함수로 live value를 생성하거나 predefined design file에서 row를 선택합니다.
2. 이후 분석에 필요한 assignment 또는 stimulus metadata에는 `sd_store_value()`를 호출합니다.
3. Label/option이 respondent별로 달라지면 server-side `sd_question()`을 만듭니다.
4. `survey.qmd`에서 `sd_output(type = "question")`으로 render합니다.

Balanced, blocked, stratified, factorial 또는 seeded assignment에 대한 단일 공개 선언형 upstream contract는 없습니다. 따라서 greedyQualt는 native randomization syntax를 “surveydown compatible”이라고 부르면 안 됩니다. 이는 일반적인 R pattern을 대체하는 의도적 확장입니다.

| Capability | Upstream | greedyQualt 방향 |
| --- | --- | --- |
| Option/row shuffle | 지원 문항 타입에 YAML 선언 | **v0.1 target compatibility** |
| 단순 respondent assignment | 사용자가 작성한 R | **v0.1 native primitive** |
| Persistent stored assignment | `sd_store_value()` 및 session 동작 | **v0.1 native primitive** |
| Predefined design 선택 | 사용자가 작성한 R/CSV | **Post-v0.1 native primitive** |
| Weighted assignment | 사용자가 작성한 R | **Post-v0.1 native primitive** |
| Block/stratified assignment | 사용자 구현 | **v0.1 block target**, stratified는 이후 |
| Factorial design | 사용자 구현 | **Post-v0.1 native primitive** |
| Seeded reproducibility | 사용자 구현 | **v0.1 native requirement** |
| Concurrency-safe balancing | 사용자/database 구현 | **v0.1 database requirement** |

## 10. Persistence 및 database 동작

공식 [Storing Data](https://surveydown.org/docs/storing-data) 문서와 package source에서 다음 동작을 확인했습니다.

- Live storage target은 PostgreSQL이며 Supabase를 권장합니다.
- `database`, `preview`, `local` mode는 각각 PostgreSQL, `preview_data.csv`, `local_data.csv`에 저장합니다.
- Database table을 자동 생성하고 누락된 text column을 추가합니다.
- `session_id`가 primary key이며 write는 insert-or-update 방식입니다.
- 하나의 session은 하나의 wide row로 표현됩니다.
- 페이지 전환과 session/browser 종료 시 database를 갱신합니다.
- Multiple-response value는 pipe-separated이며 임의의 stored vector는 text로 결합됩니다.
- Matrix row는 각각 `<question_id>_<row_id>` column이 됩니다.
- Cookie가 session identifier, progress, answer를 보존하여 respondent가 재개할 수 있습니다.
- Metadata capture를 활성화하면 `browser`와 `ip_address`가 추가됩니다.
- 현재 source에는 `time_start`, `time_end`, 생성된 question/page timestamp field가 있습니다.

### 제안 호환 범위

| 동작 | 제안 greedyQualt 분류 |
| --- | --- |
| 익명 stable respondent/session ID | **v0.1 target** |
| Current page와 기존 answer 재개 | **v0.1 target** |
| Page navigation 시 저장 | **v0.1 target** |
| Browser/session 종료 시 best-effort 저장 | **v0.1 target**, 유일한 durability mechanism으로 사용하지 않음 |
| Supabase/PostgreSQL 지원 | **v0.1 target** |
| Preview environment | **v0.1 native equivalent** |
| Offline local CSV collection | **Deferred** |
| Respondent당 하나의 wide mutable row | Export compatibility만 제공, **native schema target 아님** |
| Pipe-separated multiple response | Export compatibility만 제공 |
| Production에서 automatic schema mutation | **Unsupported by design**, versioned migration 사용 |
| Server `.env`의 database password | Vercel/Supabase environment configuration으로 교체 |
| Browser 및 IP capture 기본 활성화 | **호환하지 않음**, greedyQualt는 privacy-first |

greedyQualt native schema는 respondent identity/session state, answer, assignment, repeated task, event data를 분리하되 필요하면 surveydown-compatible wide export를 제공해야 합니다.

## 11. Redirect, metadata 및 external panel

`sd_get_url_pars()`는 전체 또는 이름이 지정된 URL parameter를 읽습니다. `sd_redirect()`는 static/reactive URL, optional button, delay, new-tab 동작을 지원합니다. 이 primitive는 participant ID와 completion destination 같은 panel integration의 기반입니다.

제안 v0.1 지원:

- Allowlist된 URL parameter를 선언된 respondent metadata에 mapping
- Parameter interpolation을 사용하는 static completion redirect
- 선언된 completion code 및 persistent storage
- 수집 metadata에 대한 명시적 consent/privacy configuration

Deferred:

- 임의의 reactive URL construction
- Generic primitive 위에 구축할 provider-specific Prolific preset

### 11.1 IRB 및 연구 안내 form

고정된 공식 문서와 package source에서 전용 `irb`, `ethics` 또는 research-information authoring primitive는 발견되지 않았습니다. 작성자는 일반 Markdown page에 IRB 승인 안내, 연구자 연락처, 위험, 이익, 보상, 철회 조건, document link를 배치할 수 있습니다.

이는 presentation capability이지 구조화된 IRB 지원이 아닙니다. surveydown은 필수 ethics field를 검증하거나, 표시된 문구를 protocol/version에 연결하거나, 연구가 승인 또는 compliant하다는 증거를 제공하지 않습니다.

greedyQualt 분류: 구조화된 ethics/IRB metadata와 재사용 가능한 information block은 **v0.1 native target**입니다. Authoring, validation, display, audit metadata만 제공하며 compliance를 주장해서는 안 됩니다.

### 11.2 Informed consent

전용 `consent` question type 또는 consent schema는 발견되지 않았습니다. 공식 예제는 일반 Markdown page, `mc` question, required-question 동작, conditional navigation을 조합하여 informed consent를 구성합니다. Package example도 consent를 `sd_skip_if()`의 일반 condition으로 사용합니다.

이 조합으로 answer를 수집할 수 있지만 document version, content hash, server acceptance time, amendment, withdrawal, parental/guardian consent 또는 response-retention policy 같은 consent-specific semantics를 정의하지는 않습니다.

greedyQualt 분류: consent는 semantic하고 versioned contract를 갖는 **v0.1 native target**입니다. 전자서명과 관할별 compliance workflow는 **Deferred**입니다.

### 11.3 External respondent collector

surveydown은 turnkey provider connector 대신 generic panel workflow를 명시적으로 지원합니다.

- `sd_get_url_pars()`가 inbound URL parameter에서 participant 및 study identifier를 읽습니다.
- `sd_store_value()`가 해당 identifier를 저장할 수 있습니다.
- `sd_redirect()`가 static/reactive completion destination, optional button, delay, new-tab 동작을 지원합니다.
- Server code에서 호출한 `sd_completion_code()`가 저장 가능한 session별 numeric completion code를 생성할 수 있습니다.

공식 external-redirect 문서는 Prolific과 Dynata를 사용 사례로 명시합니다. 그러나 작성자가 provider mapping, missing-ID check, storage call, completion/screen-out route, duplicate-participation policy를 직접 작성해야 합니다.

greedyQualt 분류: generic provider contract와 Prolific preset은 **v0.1 native target**입니다. 추가 provider preset은 **Post-v0.1**입니다.

## 12. 호환성 matrix 요약

| Domain | v0.1 target | Post-v0.1 / native extension | Unsupported by design |
| --- | --- | --- | --- |
| Pages | Shorthand page, Markdown subset | Fence page | 임의 Quarto extension |
| Questions | Core input, choice, select, slider, date, matrix | Button, image, daterange, matrix multiple | `...`을 통한 임의 Shiny input |
| Question sources | Inline 및 root `questions.yml` | Multiple/custom YAML file | Executable YAML value |
| Navigation | Auto Next, Previous, `sd_nav`, direct forward, exit, static redirect | Legacy alias, 확장 exit | Imperative browser script |
| Settings | Core behavior, required, shuffle, progress, message | Theme, rating, language, auto-scroll | 임의 Quarto runtime configuration |
| Logic | 선언형 show/skip/stop 및 safe expression | Derived reactive graph | 임의 R/Shiny |
| Randomization | Shuffle, simple/block persistent seeded assignment | Weighted, stratified, factorial, CSV design | Definition 내부 임의 executable code |
| Persistence | Supabase, resume, partial save, completion | 추가 backend, offline mode | Core model로서 runtime schema mutation |
| Data | Normalized native model 및 wide export | 풍부한 event/revision data | greedyQualt 중앙 소유 respondent store |
| Research governance | Ethics metadata 및 versioned consent | 전자서명 및 관할별 workflow | 자동 IRB/legal compliance 주장 |
| Respondent source | Generic URL/redirect contract 및 Prolific preset | 추가 provider preset | 검증되지 않은 임의 redirect code |

## 13. AI-guided workflow에 미치는 영향

Surveydown compatibility는 주요 대화형 경험 아래에 있는 implementation constraint입니다. 연구자가 자신의 요구사항이 compatible QMD syntax 또는 greedyQualt-native declaration 중 어디에 mapping되는지 알 필요는 없습니다.

따라서 versioned guide와 validator는 다음을 수행해야 합니다.

1. 사용자에게 syntax 선택을 요구하지 않고 domain language로 연구 의도를 질문합니다.
2. Compatibility matrix가 허용하는 경우 확인된 의도를 surveydown-compatible QMD로 mapping합니다.
3. Logic, randomization, consent, governance, privacy, respondent-source 동작에는 native declarative configuration을 사용합니다.
4. Compatibility limitation이 연구 동작이나 migration path를 바꿀 때만 이를 설명합니다.
5. 생성된 survey artifact와 별도로 구조화된 decision log를 보존합니다.
6. Limitation에 대응하여 중요한 연구 결정을 바꾸기 전에 연구자 확인을 요구합니다.
7. LLM이 correction loop에서 사용할 수 있는 안정적인 diagnostic code와 location을 생성합니다.
8. Repository, database, deployment, panel operation을 약속하기 전에 Chat mode와 Agent mode를 구분합니다.
9. 모든 external mutation을 완료했다고 보고하기 전에 검증합니다.
10. 생성 artifact를 model-independent하게 유지하여 원래 대화 없이도 검사·편집·검증·재현할 수 있게 합니다.

LLM은 자신의 research-methods knowledge를 적용하여 question과 design을 비평할 책임이 있습니다. greedyQualt는 올바른 checkpoint에서 review가 이루어지고, concern이 설명되며, 연구자가 최종 권한을 유지하고, 확인된 결정이 유효하고 결정론적인 artifact가 되도록 할 책임이 있습니다.

## 14. v0.1 스펙에 미치는 영향

규범적 스펙은 다음 사항을 명시적으로 결정해야 합니다.

1. 일반 R을 parse하거나 실행하려 하지 말고 허용된 R chunk의 제한된 grammar를 정의합니다.
2. 정확한 ID grammar, uniqueness rule, reserved identifier, cross-file reference를 정의합니다.
3. Markdown 및 HTML sanitization boundary를 정의합니다.
4. surveydown의 text-column 저장 representation과 독립적인 normalized response value를 정의합니다.
5. 결정론적인 page navigation order와 rule priority를 정의합니다.
6. Hidden, skipped, changed 또는 invalidated answer를 어떻게 처리할지 정의합니다.
7. Randomization timing, seed derivation, persistence, concurrency, audit metadata를 정의합니다.
8. Versioned database migration과 Row Level Security policy를 정의합니다.
9. Cookie, IP address, browser metadata, URL parameter에 privacy-safe default를 정의합니다.
10. 사람과 LLM correction loop 모두에 적합한 안정적 validator diagnostic을 정의합니다.

## 15. 알려진 모호성 및 후속 확인

- Documentation과 source는 때때로 `show_prev`와 현재 `show_previous` signature처럼 다른 parameter name 또는 legacy terminology를 사용합니다.
- Default material에는 `start-page: initial_page`가 있지만 narrative documentation은 실질적 default가 첫 페이지라고 설명합니다. greedyQualt는 하나의 모호하지 않은 동작을 정의해야 합니다.
- Public package reference는 광범위한 `...` input argument를 노출하며 이는 안정적인 cross-runtime contract가 될 수 없습니다.
- Quarto와 Shiny에서는 임의 formatting과 behavior가 가능하므로 문서화된 portable subset만 호환성 대상이 될 수 있습니다.
- 현재 GitHub `main`은 package version `1.3.0`을 보고하지만 GitHub Releases는 이 버전까지 유지되지 않았습니다. 따라서 이 조사는 Releases page에 의존하지 않고 정확한 commit을 고정합니다.
- v0.1을 확정하기 전에 모든 대상 문항 타입, navigation path, shuffle form, persistence transition에 대한 executable fixture를 수집해야 합니다.

## 16. Primary source

- [Surveydown documentation home](https://surveydown.org/docs/)
- [Basic Components](https://surveydown.org/docs/basic-components)
- [Page Navigation](https://surveydown.org/docs/page-navigation)
- [Defining Questions](https://surveydown.org/docs/defining-questions)
- [Question Types](https://surveydown.org/docs/question-types)
- [`sd_question()` package reference](https://pkg.surveydown.org/reference/sd_question)
- [Question Formatting](https://surveydown.org/docs/question-formatting)
- [Survey Settings](https://surveydown.org/docs/survey-settings)
- [Conditional Logic](https://surveydown.org/docs/conditional-logic)
- [Accessing Values](https://surveydown.org/docs/accessing-values)
- [Reactivity](https://surveydown.org/docs/reactivity)
- [Randomization](https://surveydown.org/docs/randomization)
- [Storing Data](https://surveydown.org/docs/storing-data)
- [External Redirect](https://surveydown.org/docs/external-redirect)
- [Surveydown package source](https://github.com/surveydown-dev/surveydown)
- [Surveydown documentation source](https://github.com/surveydown-dev/website)
