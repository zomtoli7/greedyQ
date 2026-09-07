# Surveydown Compatibility Research

[한국어](./surveydown-compatibility(kor).md)

**Status:** Research draft

**Research snapshot:** 2026-09-07

**Surveydown package snapshot:** `1.3.0`, commit [`8af8f55`](https://github.com/surveydown-dev/surveydown/commit/8af8f5504a54246b9c01706a6dd484389afaf588), committed 2026-06-23

**Documentation snapshot:** commit [`f1325a3`](https://github.com/surveydown-dev/website/commit/f1325a32ad937817bb23bc017356f0636ef6d8da)

**Document role:** Descriptive inventory of surveydown's public authoring surface and a proposed compatibility boundary for greedyQ v0.1

## 1. Scope and terminology

This document records publicly observable surveydown authoring behavior from official documentation, package references, repository metadata, and maintained examples. It is research input for the normative greedyQ v0.1 specification; it is not itself an implementation guarantee or a source-code reuse plan.

greedyQ is an independent implementation. It does not incorporate surveydown source code. The parser, AST, validator, web-native runtime, deployment integration, export generator, templates, and conformance fixtures must be authored independently. Repository links in this document establish provenance and version snapshots, not permission to copy implementation details. Surveydown is prior open-source work distributed under the MIT License; attribution and non-affiliation terms are recorded in the repository `NOTICE.md`.

The proposed greedyQ classifications are:

| Classification | Meaning |
| --- | --- |
| **v0.1 target** | Intended for the first normative greedyQ specification and MVP |
| **Post-v0.1** | Compatible or equivalent behavior is desirable after the MVP |
| **Native implementation** | The use case is supported through a greedyQ declarative feature in the web-native runtime |
| **Generated export** | Validated behavior is translated into `app.R` or supporting native surveydown files |
| **greedyQ-only** | The feature requires an explicit limitation or alternative in the export report |
| **Deferred** | Valuable, but the compatibility shape needs more research or implementation maturity |
| **Unsupported by design** | Conflicts with greedyQ's security, runtime, or product principles |

Compatibility means compatibility with the documented authoring contract where practical. It does not mean reproducing surveydown's R objects, Shiny internals, generated HTML, CSS, database implementation, or source code. Each normative feature must separately declare greedyQ runtime support and native surveydown export behavior.

## 2. Executive findings

1. A surveydown project is centered on `survey.qmd` and `app.R`. The former contains static pages, questions, content, and navigation; the latter creates the Shiny application, database connection, reactive questions, conditional logic, and randomization.
2. Current surveydown supports two page syntaxes: recommended `--- page_id` shorthand and explicit `::: {.sd_page id=page_id}` fences.
3. Navigation is automatically injected. `sd_nav()` overrides a page, and `show-previous` controls the global Previous button.
4. The public `sd_question()` API currently lists 16 question types, including button, image, and multiple-response matrix variants.
5. Questions may be declared inline or loaded by ID from a root or custom YAML file.
6. YAML contains complete theme, behavior, and system-message surfaces, plus three storage modes: `database`, `preview`, and `local`.
7. Conditional showing, forward skipping, stopping/validation, reactive values, reactive questions, and arbitrary calculations live in R/Shiny server code.
8. Randomization is a programming pattern rather than a declared study primitive. Authors generate or load randomized values in `app.R`, store them explicitly, and display reactive questions through `sd_output()`.
9. Surveydown uses one wide response row per session. It creates and extends a PostgreSQL table automatically, uses `session_id` as the primary key, and writes values as text columns.
10. Cookies preserve the session ID, current page, and answers. Database/CSV data is updated on page transitions and browser/session end.
11. greedyQ can preserve most static QMD authoring while expressing runtime behavior in a versioned declarative specification. The web-native runtime consumes it directly, and the export generator produces `app.R` for supported native surveydown behavior. Arbitrary user-authored R and Shiny behavior cannot be generally translated and remains unsupported as input.
12. Because AI-guided creation is greedyQ's primary experience, compatibility details must be expressible as deterministic generation rules and validator diagnostics, not merely prose for expert authors.

## 3. Project and runtime model

### 3.1 Surveydown

The official [Basic Components](https://surveydown.org/docs/basic-components) documentation defines two required files:

```text
survey.qmd  # pages, Markdown, questions, navigation, static outputs
app.R       # database, Shiny server, reactivity, logic, runtime launch
```

The minimal runtime model is:

```r
library(surveydown)

db <- sd_db_connect()
ui <- sd_ui()

server <- function(input, output, session) {
  sd_server(db)
}

shiny::shinyApp(ui = ui, server = server)
```

`survey.qmd` is parsed and rendered into a generated `_survey/` directory. The documentation warns authors not to edit generated `settings.yml`; source configuration belongs in `survey.qmd`.

### 3.2 greedyQ boundary

```text
survey.qmd             -> compatible static authoring surface
questions*.yml         -> compatible question definitions where specified
greedyq.yml            -> native logic, randomization, lifecycle, persistence
design/*.csv           -> native experimental designs
existing app.R         -> optional migration input; never executed
generated app.R        -> native surveydown export from the validated AST
```

| Surveydown component | Proposed greedyQ treatment |
| --- | --- |
| `survey.qmd` | **v0.1 target** |
| Root `questions.yml` | **v0.1 target** |
| Custom question YAML paths | **Post-v0.1** |
| Existing `app.R` standard patterns | Optional migration input; never executed |
| Generated `app.R` | **Generated export** plus compatibility diagnostics |
| Arbitrary R/Shiny code | **Unsupported by design** |
| Generated `_survey/` files | Not a compatibility target |
| RStudio gadgets / sdstudio | Not a product target |

## 4. QMD document and page grammar

### 4.1 YAML front matter

The YAML header is optional; surveydown applies defaults when it is absent. Quarto format options may also appear there.

```yaml
---
theme-settings:
  theme: default

survey-settings:
  show-previous: no
  all-required: no
---
```

greedyQ should parse the three surveydown namespaces it understands and issue diagnostics, rather than silently accepting arbitrary Quarto configuration.

### 4.2 Page syntax

Recommended shorthand:

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

| Feature | Surveydown behavior | Proposed greedyQ classification |
| --- | --- | --- |
| `--- page_id` | Opens a page and implicitly closes the previous page | **v0.1 target** |
| `.sd_page` fence | Explicit page boundary | **Post-v0.1** |
| Markdown content | Rendered through Quarto/Markdown | **v0.1 target**, documented safe subset |
| Raw HTML | Permitted by the upstream rendering stack | **Deferred**, sanitize by default |
| Arbitrary Quarto extensions | Available through Quarto | **Unsupported by design** unless explicitly adopted |
| Duplicate/overlapping IDs | Rejected, including reserved IDs | **v0.1 target** |

Reserved upstream IDs observed in package source are:

```text
session_id
time_start
time_end
exit_survey_rating
current_page
browser
ip_address
```

greedyQ should reserve these for migration compatibility, even if its native data model uses different physical column names.

## 5. Questions

The official [Question Types](https://surveydown.org/docs/question-types) and [`sd_question()` reference](https://pkg.surveydown.org/reference/sd_question) define the public question surface.

### 5.1 Declaration forms

Inline declaration:

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

`option` and `options` are aliases; `option` wins if both appear. Named vectors separate display labels from stored values. Except for image questions, unnamed values are both displayed and stored. For image questions, unnamed options suppress captions.

### 5.2 Question-type matrix

| Type | Upstream semantics | Important data behavior | Proposed greedyQ classification |
| --- | --- | --- | --- |
| `text` | Single-line text input | One scalar value | **v0.1 target** |
| `textarea` | Multi-line text input | One scalar value | **v0.1 target** |
| `numeric` | Numeric input | One numeric-looking value | **v0.1 target** |
| `mc` | Single-choice radio group | Option value | **v0.1 target** |
| `mc_multiple` | Multiple-choice checkbox group | Pipe-separated upstream storage | **v0.1 target** |
| `mc_buttons` | Single-choice buttons | Option value | **Post-v0.1** |
| `mc_multiple_buttons` | Multiple-choice buttons | Pipe-separated upstream storage | **Post-v0.1** |
| `mc_image` | Single-choice image cards | Option value; optional caption | **Post-v0.1** |
| `mc_multiple_image` | Multiple-choice image cards | Multiple values | **Post-v0.1** |
| `select` | Dropdown | Option value | **v0.1 target** |
| `slider` | Discrete labeled slider | Selected option value | **v0.1 target** |
| `slider_numeric` | Numeric single/range slider | Scalar or range | **v0.1 target** |
| `date` | Date input, today as upstream default | Date value | **v0.1 target** |
| `daterange` | Date-range input | Two endpoints | **Post-v0.1** |
| `matrix` | One radio selection per row | `<id>_<row_id>` columns upstream | **v0.1 target** |
| `matrix_multiple` | Multiple checkbox selections per row | Per-row values; upstream pipe joining | **Post-v0.1** |

greedyQ should preserve the logical response shape and migration/export behavior, but its native database does not need to reproduce pipe-separated or wide-column physical storage internally.

### 5.3 `sd_question()` argument inventory

| Argument | Upstream purpose | Proposed greedyQ classification |
| --- | --- | --- |
| `id`, `type`, `label` | Identity and core definition | **v0.1 target** |
| `option`, `options` | Display/stored-value choices | **v0.1 target** |
| `row` | Matrix row label/ID mapping | **v0.1 target** |
| `selected`, `default` | Initial choice or slider value/range | **v0.1 target** |
| `placeholder` | Text/textarea placeholder | **v0.1 target** |
| `width`, `height`, `cols`, `resize` | Size/layout controls | **Post-v0.1** |
| `direction` | Horizontal/vertical button groups | **Post-v0.1** |
| `status`, `individual`, `justified` | Shiny button styling | **Deferred**, map only if portable |
| `label_select` | Select placeholder | **v0.1 target** |
| `grid`, `force_edges` | Slider presentation | **Post-v0.1** |
| `image` | Image paths/URLs parallel to options | **Post-v0.1** |
| `option_attr` | Per-option HTML attributes | **Unsupported by design** in its raw form |
| `yml` | External question-definition path | **Post-v0.1**; root default is v0.1 |
| `matrix_question_width` | Matrix prompt-column width | **Post-v0.1** |
| `...` | Arbitrary input-specific Shiny arguments | **Unsupported by design**; explicitly whitelist portable arguments |

Labels and regular option labels accept Markdown upstream. Raw HTML is also possible, but greedyQ should specify sanitization and a portable Markdown subset.

## 6. Navigation and termination

The official [Page Navigation](https://surveydown.org/docs/page-navigation) documentation states that a Next button is injected automatically unless page-level navigation or close behavior is explicitly defined.

| Surface | Upstream behavior | Proposed greedyQ classification |
| --- | --- | --- |
| Automatic Next | Added to pages by default | **v0.1 target** |
| Global `show-previous` | Enables Previous across pages | **v0.1 target** |
| `sd_nav()` | Page-level Previous/Next override | **v0.1 target** |
| `page_next` | Direct forward target | **v0.1 target** |
| Custom navigation labels | `label_previous`, `label_next` | **v0.1 target** |
| Hide buttons | `show_previous`, `show_next` | **v0.1 target** |
| `sd_next()` | Legacy single Next button | **Post-v0.1** parser alias |
| `sd_close()` | Exit flow, optional rating/restart/cookie clearing | Basic exit **v0.1**; extended options **Post-v0.1** |
| `sd_redirect()` | Static/reactive redirect, delay, new tab | Static redirect **v0.1**; reactive redirect **Native implementation** |
| Empty terminal page | No forward control | **v0.1 target** |

The current `sd_nav()` source signature uses `show_previous`; some narrative documentation uses `show_prev`. greedyQ must follow the package reference/source signature and may emit a helpful diagnostic for the narrative alias.

## 7. Survey settings

The official [Survey Settings](https://surveydown.org/docs/survey-settings) default structure has three sections. Hyphens and underscores are accepted interchangeably in YAML keys; YAML `yes`/`no` and `true`/`false` booleans are accepted.

### 7.1 Theme settings

| Key | Upstream default/behavior | Proposed greedyQ classification |
| --- | --- | --- |
| `theme` | `default`; Bootswatch/custom SCSS through Quarto | Named portable themes **Post-v0.1**; arbitrary SCSS deferred |
| `barposition` | `top`; `bottom` or `none` | **v0.1 target** |
| `barcolor` | Theme primary color | **v0.1 target** |
| `footer`, `footer-left`, `footer-center`, `footer-right` | Footer content | **v0.1 target** |

Upstream progress advances per answered question, not per page.

### 7.2 Survey settings

| Key | Upstream default | Proposed greedyQ classification |
| --- | --- | --- |
| `mode` | `database`; also `preview`, `local` | Equivalent environments **Native implementation** |
| `show-previous` | `no` | **v0.1 target** |
| `use-cookies` | `yes` | **v0.1 target**, with explicit privacy semantics |
| `auto-scroll` | `no` | **Post-v0.1** |
| `rate-survey` | `no` | **Post-v0.1** |
| `all-required` | `no` | **v0.1 target** |
| `required` | `[]` | **v0.1 target** |
| `start-page` | First page in practice; default material names `initial_page` | **v0.1 target** |
| `system-language` | `en`; upstream includes `de`, `es`, `fr`, `it`, `zh-CN` | **Post-v0.1**, i18n-ready from v0.1 |
| `highlight-unanswered` | `yes` | **v0.1 target** |
| `highlight-color` | `gray`; documented palette | **Post-v0.1** |
| `capture-metadata` | `yes`; browser and IP | **Deferred**, privacy-first and opt-in for greedyQ |
| `all-shuffled` | `no` | **v0.1 target** for supported types |
| `shuffled` | `[]` | **v0.1 target** for supported types and index syntax |

Upstream option shuffling applies to `mc`, `mc_buttons`, `mc_multiple`, and `mc_multiple_buttons`; row shuffling applies to `matrix`. `shuffled` accepts entire-question IDs or 1-based ranges/lists such as `1-5`, `[1, 2, 4]`, and `[1-5, 8-10]`.

### 7.3 System messages

The public keys are:

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

Core navigation, validation, selection, exit, and redirect messages are a **v0.1 target**. Survey-rating messages are **Post-v0.1** with that feature.

## 8. Conditional logic and values

The official [Conditional Logic](https://surveydown.org/docs/conditional-logic), [Accessing Values](https://surveydown.org/docs/accessing-values), and [Reactivity](https://surveydown.org/docs/reactivity) pages describe R/Shiny behavior.

| Upstream function/pattern | Semantics | Proposed greedyQ treatment |
| --- | --- | --- |
| `sd_show_if(condition ~ target)` | Show question or page when true | **Native implementation**, v0.1 declarative rule |
| `sd_skip_if(condition ~ page)` | Skip forward when true | **Native implementation**, v0.1 declarative rule |
| `sd_stop_if(condition ~ message)` | Block navigation and show validation errors | **Native implementation**, v0.1 declarative rule |
| `sd_is_answered(id)` | Answer-completeness predicate; matrix requires all rows | **Native implementation**, v0.1 expression function |
| `sd_value()` / `sd_values()` | Reactive answer lookup and type conversion | **Native implementation**, expression references |
| `sd_store_value()` | Store a derived/custom value | **Native implementation**, v0.1 assignment primitive |
| `sd_output(type = "value")` | Display an answer or stored value | **Native implementation**, v0.1 interpolation |
| `sd_output(type = "question")` | Render a server-defined reactive question | **Deferred**; prefer declared dynamic properties |
| `sd_output()` label modes | Display option or question labels | **Post-v0.1** |
| `sd_reactive()` | Calculate and persist a reactive value | **Native implementation**, safe expression graph after v0.1 core |
| `sd_copy_value()` | Work around unique Shiny output IDs | No compatibility need in web renderer |
| Custom R functions | Arbitrary condition/calculation logic | **Unsupported by design** |
| `observe()` and Shiny reactives | Arbitrary reactive programming | **Unsupported by design** |

The greedyQ expression language should cover literals, answer references, stored values, boolean operators, comparisons, membership, length, answer status, and a small whitelist of pure functions. It must reject arbitrary function calls and side effects.

## 9. Randomization

Surveydown's official [Randomization](https://surveydown.org/docs/randomization) guidance uses ordinary R in `app.R`:

1. Generate values live with functions such as `sample()`, or select a row from a predefined design file.
2. Call `sd_store_value()` for any assignment or stimulus metadata that must be analyzed later.
3. Build a server-side `sd_question()` when labels/options vary by respondent.
4. Render it from `survey.qmd` with `sd_output(type = "question")`.

There is no single public declarative upstream contract for balanced, blocked, stratified, factorial, or seeded assignment. Therefore greedyQ should not call its native randomization syntax “surveydown compatible.” It is an intentional extension that replaces common R patterns.

| Capability | Upstream | greedyQ direction |
| --- | --- | --- |
| Option/row shuffle | YAML-declared for supported question types | **v0.1 target compatibility** |
| Simple respondent assignment | User-written R | **v0.1 native primitive** |
| Persistent stored assignment | `sd_store_value()` plus session behavior | **v0.1 native primitive** |
| Predefined design selection | User-written R/CSV | **Post-v0.1 native primitive** |
| Weighted assignment | User-written R | **Post-v0.1 native primitive** |
| Block/stratified assignment | User implementation | **v0.1 block target**, stratified later |
| Factorial design | User implementation | **Post-v0.1 native primitive** |
| Seeded reproducibility | User implementation | **v0.1 native requirement** |
| Concurrency-safe balancing | User/database implementation | **v0.1 database requirement** |

## 10. Persistence and database behavior

The official [Storing Data](https://surveydown.org/docs/storing-data) documentation and package source establish the following behavior:

- PostgreSQL is the live storage target, with Supabase recommended.
- `database`, `preview`, and `local` modes store to PostgreSQL, `preview_data.csv`, and `local_data.csv`, respectively.
- A database table is created automatically and extended with missing text columns.
- `session_id` is the primary key; writes use insert-or-update behavior.
- One session is represented by one wide row.
- The database is updated on page transitions and session/browser end.
- Multiple-response values are pipe-separated; arbitrary stored vectors are collapsed to text.
- Matrix rows become separate `<question_id>_<row_id>` columns.
- Cookies retain the session identifier, progress, and answers so a returning respondent can resume.
- Metadata capture adds `browser` and `ip_address` when enabled.
- Timestamps include `time_start`, `time_end`, and generated question/page timestamp fields in current source.

### Proposed compatibility boundary

| Behavior | Proposed greedyQ classification |
| --- | --- |
| Anonymous stable respondent/session ID | **v0.1 target** |
| Resume current page and existing answers | **v0.1 target** |
| Save on page navigation | **v0.1 target** |
| Best-effort save on browser/session end | **v0.1 target**, not sole durability mechanism |
| Supabase/PostgreSQL support | **v0.1 target** |
| Preview environment | **v0.1 native equivalent** |
| Offline local CSV collection | **Deferred** |
| One wide mutable row per respondent | Export compatibility only; **not native schema target** |
| Pipe-separated multiple responses | Export compatibility only |
| Automatic schema mutation in production | **Unsupported by design**; use versioned migrations |
| Database password in a server `.env` | Replace with Vercel/Supabase environment configuration |
| Browser and IP capture enabled by default | **Not compatible**; greedyQ should be privacy-first |

greedyQ's native schema should separate respondent identity/session state, answers, assignments, repeated tasks, and event data while providing a surveydown-compatible wide export where useful.

## 11. Redirects, metadata, and external panels

`sd_get_url_pars()` reads all or named URL parameters. `sd_redirect()` supports static or reactive URLs, optional buttons, delay, and new-tab behavior. These primitives underpin panel integrations such as participant IDs and completion destinations.

Proposed v0.1 support:

- Allowlisted URL parameters mapped into declared respondent metadata
- Static completion redirects with parameter interpolation
- Declared completion codes and persistent storage
- Explicit consent/privacy configuration for collected metadata

Deferred:

- Arbitrary reactive URL construction
- Provider-specific Prolific presets, which should build on the generic primitives

### 11.1 IRB and research-information forms

No dedicated `irb`, `ethics`, or research-information authoring primitive was found in the pinned official documentation or package source. Authors can place IRB-approved information, investigator contacts, risks, benefits, compensation, withdrawal terms, and document links on ordinary Markdown pages.

This is presentational capability, not structured IRB support. Surveydown does not validate required ethics fields, bind displayed wording to a protocol/version, or provide evidence that a study is approved or compliant.

greedyQ classification: structured ethics/IRB metadata and reusable information blocks are a **v0.1 native target**. They provide authoring, validation, display, and audit metadata only; they must not make compliance claims.

### 11.2 Informed consent

No dedicated `consent` question type or consent schema was found. Official examples construct informed consent with an ordinary Markdown page, an `mc` question, required-question behavior, and conditional navigation. Package examples also use consent as a normal condition in `sd_skip_if()`.

This composition can collect an answer but does not define consent-specific semantics such as document version, content hash, server acceptance time, amendments, withdrawal, parental/guardian consent, or response-retention policy.

greedyQ classification: consent is a **v0.1 native target** with a semantic, versioned contract. Electronic signatures and jurisdiction-specific compliance workflows are **Deferred**.

### 11.3 External respondent collectors

Surveydown explicitly supports generic panel workflows rather than a turnkey provider connector:

- `sd_get_url_pars()` reads participant and study identifiers from inbound URL parameters.
- `sd_store_value()` can persist those identifiers.
- `sd_redirect()` supports static and reactive completion destinations, optional buttons, delays, and new-tab behavior.
- `sd_completion_code()` can generate a stored per-session numeric completion code when called in server code.

The official external-redirect documentation names Prolific and Dynata as use cases. However, authors must still write provider mappings, missing-ID checks, storage calls, completion/screen-out routes, and duplicate-participation policy themselves.

greedyQ classification: the generic provider contract and a Prolific preset are **v0.1 native targets**. Additional provider presets are **Post-v0.1**.

## 12. Compatibility matrix summary

| Domain | v0.1 target | Post-v0.1 / native extension | Unsupported by design |
| --- | --- | --- | --- |
| Pages | Shorthand pages, Markdown subset | Fence pages | Arbitrary Quarto extensions |
| Questions | Core input, choice, select, slider, date, matrix | Buttons, images, daterange, matrix multiple | Arbitrary Shiny inputs through `...` |
| Question sources | Inline and root `questions.yml` | Multiple/custom YAML files | Executable YAML values |
| Navigation | Auto Next, Previous, `sd_nav`, direct forward, exit, static redirect | Legacy aliases, extended exit | Imperative browser scripts |
| Settings | Core behavior, required, shuffle, progress, messages | Themes, rating, languages, auto-scroll | Arbitrary Quarto runtime configuration |
| Logic | Declarative show/skip/stop and safe expressions | Derived reactive graph | Arbitrary R/Shiny |
| Randomization | Shuffle, simple/block persistent seeded assignment | Weighted, stratified, factorial, CSV design | Arbitrary executable code in definitions |
| Persistence | Supabase, resume, partial save, completion | Additional backends, offline mode | Runtime schema mutation as core model |
| Data | Normalized native model and wide export | Rich event/revision data | Central greedyQ-owned respondent store |
| Research governance | Ethics metadata and versioned consent | Electronic signatures and jurisdiction-specific workflows | Claims of automatic IRB/legal compliance |
| Preregistration | Versioned draft, structured data, and artifact manifest | Additional registry adapters and verified submission | Invented commitments or unverified registration claims |
| Respondent sources | Generic URL/redirect contract and Prolific preset | Additional provider presets | Unvalidated arbitrary redirect code |

## 13. Implications for the AI-guided workflow

Surveydown compatibility is an implementation and export constraint beneath the primary conversational experience. The primary execution target remains the independent greedyQ web runtime on Vercel and Supabase. A researcher should not need to know whether a requirement maps to compatible QMD syntax or a greedyQ-native declaration, but must be told when native surveydown export changes or cannot preserve behavior.

The versioned guide and validator should therefore:

1. Ask for research intent in domain language rather than asking the user to choose syntax.
2. Map confirmed intent to surveydown-compatible QMD where the compatibility matrix permits.
3. Use native declarative configuration for logic, randomization, consent, governance, privacy, and respondent-source behavior.
4. Explain a compatibility limitation only when it changes the study's behavior or migration path.
5. Preserve a structured decision log separately from generated survey artifacts.
6. Require researcher confirmation before changing a material research decision in response to a limitation.
7. Produce stable diagnostic codes and locations that an LLM can use in a correction loop.
8. Detect Chat mode versus Agent mode before promising repository, database, deployment, or panel operations.
9. Verify every external mutation before reporting it as complete.
10. Keep generated artifacts model-independent so they can be inspected, edited, validated, and reproduced without the originating conversation.
11. Generate `survey.qmd`, `app.R`, supporting files, and a compatibility report whenever native surveydown export is requested.
12. Never imply that greedyQ is affiliated with, endorsed by, or maintained by the surveydown project.
13. Treat preregistration as a greedyQ-native research-workflow output rather than a surveydown syntax compatibility claim.

The LLM is responsible for applying its research-methods knowledge to critique questions and designs. greedyQ is responsible for ensuring that the review occurs at the correct checkpoint, concerns are explained, the researcher retains final authority, and confirmed decisions become valid deterministic artifacts.

## 14. Implications for the v0.1 specification

The normative specification should make the following decisions explicitly:

1. Define a restricted grammar for accepted R chunks instead of attempting to parse or execute general R.
2. Define exact ID grammar, uniqueness rules, reserved identifiers, and cross-file references.
3. Define the Markdown and HTML sanitization boundary.
4. Define normalized response values independently from surveydown's text-column storage representation.
5. Define deterministic page navigation ordering and rule priority.
6. Define what happens to hidden, skipped, changed, or invalidated answers.
7. Define randomization timing, seed derivation, persistence, concurrency, and audit metadata.
8. Define versioned database migrations and Row Level Security policies.
9. Define privacy-safe defaults for cookies, IP addresses, browser metadata, and URL parameters.
10. Define stable validator diagnostics suitable for both people and LLM correction loops.
11. Define deterministic `app.R` generation rules and the boundary between directly portable, generated, greedyQ-only, and unsupported behavior.
12. Require independently authored conformance fixtures rather than copied surveydown source or test material.

## 15. Known ambiguities and follow-up checks

- Documentation and source occasionally use different parameter names or legacy terminology, such as `show_prev` versus the current `show_previous` signature.
- The default material lists `start-page: initial_page`, while narrative documentation says the first page is the effective default. greedyQ should specify one unambiguous behavior.
- The public package reference exposes broad `...` input arguments that cannot be a stable cross-runtime contract.
- Quarto and Shiny make arbitrary formatting and behavior possible; only documented portable subsets can be compatibility targets.
- The current GitHub `main` reports package version `1.3.0`, while GitHub Releases is not maintained through that version. This research therefore pins the exact commit rather than relying on the Releases page.
- Before freezing v0.1, executable fixtures should be collected for every targeted question type, navigation path, shuffle form, and persistence transition.

## 16. Primary sources

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
