# Surveydown compatibility audit

[한국어](./surveydown-compatibility-audit(kor).md)

Checked 2026-09-10 against the public manuals below. This is a behavior audit, not a claim of complete R/Shiny compatibility. No Surveydown internal source or fixtures were incorporated. “Accepted” does not mean “implemented”; differences below must be explained before choosing an export.

## Ordering and randomization

[Official settings](https://surveydown.org/docs/survey-settings) define `all-shuffled` and `shuffled` for choice options and matrix rows, not page ordering. greedyQ accepts names or one-based positions/ranges, preserving fixed positions and stored values. The shared types are mc, mc_buttons, mc_multiple, mc_multiple_buttons and matrix. Matrix columns and matrix_multiple are not implicitly shuffled. `question_order` and `page_order` are distinct greedyQ extensions. Page ordering currently requires one independent contiguous group with fixed opening/ending, automatic navigation and no show/skip rules. Consent, assignment and condition pages cannot be shuffled.

Presentation orders persist per session as `question_orders`, `option_orders` and `page_order`; they describe planned presentation, not proof of reading. Native export preserves the official option-shuffle header but cannot yet claim refresh persistence. Native question/page-order export is explicitly unsupported, not silently equivalent.

[Official randomization](https://surveydown.org/docs/randomization) describes server-side live draws or predefined designs and recording drawn values. greedyQ implements its own simple weighted and fixed-block respondent allocation with a server-recorded boundary. Arbitrary R design-file sampling, cluster/stratified/adaptive allocation and native fixed-block equivalence are not implemented. See [randomization](../RANDOMIZATION.md).

## Settings inventory

| Setting family | Browser-native status | Native export |
| --- | --- | --- |
| Hyphen/underscore aliases; YAML yes/no | Parsed; duplicate alias keys rejected | Source retained; namespace normalized for preview mode |
| all-required / required | Applied to rendered controls | Retained |
| show-previous / start-page | Applied; terminal previous hidden | Retained |
| barcolor | Applied, currently constrained to six-digit hex | Retained |
| theme / barposition / footer variants | Accepted historically but not fully rendered; do not claim effect | Retained for Surveydown |
| use-cookies | Native backend uses browser storage instead; disabling not yet equivalent | Retained |
| highlight-unanswered | Required checks exist; optional highlighting setting not equivalent | Retained |
| capture-metadata | No automatic browser/IP collection; true not implemented | Must review privacy before native fielding |
| mode | greedyQ uses respondents.mode and deployment separation; QMD mode unsupported | Generated export forced to preview |
| auto-scroll | Page-change top scrolling exists; question-progress scrolling unsupported | Unsupported input must not be invented |
| rate-survey | Unsupported; author an explicit rating question instead | Requires native-specific authoring |
| system-language / highlight-color | Unsupported | Requires native-specific authoring |
| system-messages | previous, next, required supported; other official keys unsupported | Supported source keys retained |

These differences mean “all Surveydown settings supported” is not an accurate description of this build.

## Formatting, values and logic

- [Formatting](https://surveydown.org/docs/question-formatting): width, textarea height and matrix question-column width are handled. The browser supports escaped bold/italic/inline-code formatting in question and choice labels; full Markdown and arbitrary HTML remain non-equivalent. Raw page HTML is rejected. Native export preserves label strings for Surveydown rendering. Never bypass escaping with untrusted HTML.
- [Values](https://surveydown.org/docs/accessing-values): greedyQ keeps typed answers and resumes saved state; generated R uses `sd_value()` and `sd_is_answered()` for supported conditions. Arbitrary quoted/unquoted R expressions, coercion flags, derived-value calculations and full vector operations are not a greedyQ source language.
- [Conditional logic](https://surveydown.org/docs/conditional-logic): question/page visibility, explicit from-page skip routes and stop checks use a bounded comparison language. Basic answered checks and numeric/required checks are available; compound boolean precedence and quoted connectors are handled. General custom R functions, vector operations and unrestricted expressions are not supported. The native global skip translation needs target-runtime review against greedyQ's from-page restriction. Matrix-wide answered semantics and complex rule coverage remain open verification items.
- [Reactivity](https://surveydown.org/docs/reactivity): same-page dependent visibility is implemented. General reactive calculations, copied outputs, answer piping and server-generated questions are not implemented as unrestricted Shiny programs. They remain an explicitly scoped future extension, not agent-generated runtime patches.

## External returns

[Official redirects](https://surveydown.org/docs/external-redirect) distinguish fixed and URL-parameter-based destinations. greedyQ now compiles terminal outcome redirects with fixed HTTPS hosts, approved query-name mappings, explicit buttons and optional same-tab delay. Missing/repeated parameters fail closed. Credentials are not forwarded. Preview navigation is disabled; connected respondents can leave only after a successful save. New tabs require a click because automatic pop-ups are unreliable. Native return buttons are generated, but timers are omitted in native preview and save-before-return needs R verification. The primary browser-native Prolific paid route is verified with researcher-confirmed approval/payment; equivalent native Surveydown identity and erasure behavior remains unverified.

## Release gate

Do not describe all non-Prolific compatibility work as complete while the gaps above remain. Keep existing cloud projects untouched until a reviewed migration and redeployment is approved. The local un-applied migration 004 now covers saved presentation order; installations that already applied a different 004 need a new additive migration, never checksum rewriting.

## 2026-10-26 scope correction

The primary browser-native Prolific route has completed a one-person paid trial with researcher-confirmed approval/payment; its earlier untested label is historical. Native Surveydown identity/save-before-return/withdrawal parity and every generated custom control remain separately unverified. See the current integration and closeout records.
