# greedyQ Preview UI 스펙

[English](./preview-ui-spec.md)

**상태:** Draft normative specification
**적용 대상:** self-contained preview 및 web-native respondent renderer

## 1. 목적

Preview는 primary instrument-review surface입니다. Researcher가 questionnaire를 respondent처럼 경험하면서 보이지 않는 state를 검사할 수 있어야 합니다. Prose study summary는 보조 문서이며 대체물이 아닙니다.

Canonical renderer에는 정확히 `desktop`, `mobile`, `preview` 세 mode가 있습니다. Respondent entry point는 현재 viewport와 pointer capability로 desktop 또는 mobile을 runtime에서 감지하며 user-agent brand sniffing을 authoritative signal로 사용하면 안 됩니다. Preview mode는 독립된 desktop 및 mobile respondent session을 동시에 render합니다. 세 mode는 동일한 고정 parser, validator, normalized AST, question component, routing engine, state semantics를 사용합니다. Responsive presentation은 달라도 되지만 question meaning, stored value, validation, navigation, randomization, lifecycle behavior는 달라지면 안 됩니다.

Preview는 엄격히 분리된 두 layer를 갖습니다.

- **Respondent layer:** participant가 실제로 경험해야 하는 questionnaire
- **Researcher layer:** preview-only control, state inspection, route forcing, test evidence

Researcher control은 시각적으로 표시하고 production respondent mode에는 절대 나타나면 안 됩니다.

## 2. Default layout

Preview는 flexible desktop frame과 390 CSS-pixel mobile frame이라는 두 labelled viewport를 사용합니다. 각 frame은 독립 virtual session을 가집니다. Preview workspace 자체가 좁아지면 forced respondent mode를 바꾸지 않고 frame을 세로로 배치합니다. Production desktop은 최대 760 pixel의 centered respondent card를 사용합니다. Production mobile은 decorative card elevation을 제거하고 available width를 사용하며 touch target을 최소 44 CSS pixel로 키우고 navigation이 question을 가리지 않으면서 접근 가능하게 유지합니다.

Persistent top bar에는 greedyQ wordmark, 눈에 띄는 `RESEARCHER PREVIEW` badge, page progress, accessible progress value를 둡니다. Questionnaire 완료와 관계없는 application chrome, decorative dashboard, nested card, control은 피합니다.

차분한 neutral canvas, white questionnaire surface, 절제된 primary color 하나, 명확한 1-pixel boundary, 적당한 elevation을 사용합니다. 최소 content width는 320 CSS pixel입니다. 200% zoom에서는 wide matrix의 labelled scroll region을 제외하고 horizontal scroll 없이 reflow해야 합니다.

## 3. Respondent page anatomy

다음 순서로 render합니다.

1. preview에서만 study title과 stable page ID eyebrow
2. page heading 하나
3. 간결한 intro 또는 stimulus content
4. 선언 순서의 question
5. 필요할 때 page-level validation summary 하나
6. Previous 및 primary Continue/Submit action
7. 또는 outgoing production action이 없는 명확한 terminal outcome

Page마다 primary action은 하나입니다. Previous는 secondary입니다. History가 비었거나 policy가 금지할 때만 Previous를 disable합니다. Required answer가 비었다고 Continue를 미리 disable하지 않습니다. 활성화하면 actionable error를 보여주고 첫 invalid question으로 focus를 이동합니다.

## 4. Question presentation

- 가능하면 native semantic control을 사용합니다.
- 모든 control에는 persistent visible label이 있습니다. Placeholder만 label로 사용하지 않습니다.
- Required question은 color만이 아니라 text 또는 accessible label로 표시합니다.
- Single choice는 `fieldset`, `legend`, native radio를 사용하고 option row 전체를 클릭할 수 있게 합니다.
- Preview option은 display label 아래 stored value를 표시합니다. Production respondent mode에서는 stored value를 숨깁니다.
- Select는 선택되지 않은 empty prompt를 사용하고 display/stored 구분을 보존합니다.
- Discrete scale은 native radio와 의미 있는 endpoint label을 사용하며 keyboard로 조작할 수 있어야 합니다. Categorical Likert data에 label 없는 custom range slider를 사용하지 않습니다.
- Matrix는 실제 table header와 row마다 고유한 radio-group name을 사용합니다. 작은 화면에서는 row 단위 표시 또는 labelled horizontal scroll table을 사용하며 base size 아래로 text를 축소하지 않습니다.
- Optional textarea는 visible help 또는 label에 `Optional`을 표시합니다.
- Hidden question은 focus order에서 제거합니다. `clear_on_hide`이면 answer를 지우고 event를 기록합니다.

## 5. Validation 및 feedback

Forward navigation에서 authoritative validation을 수행합니다. 첫 invalid question을 text로 식별하고 `aria-invalid=true`, `aria-describedby`를 설정하며 invalid control 또는 legend로 focus를 이동하고 화면에 보이게 합니다. 다른 valid answer는 보존합니다.

Error는 해결 방법을 설명하고 red color에만 의존하지 않습니다. 수정한 응답의 stale error는 제거합니다. Required value, numeric range, required matrix row 완성, 선언된 cross-field rule을 검증합니다.

## 6. Progress 및 navigation

Progress는 모든 condition page의 raw count가 아니라 reachable respondent path를 기준으로 합니다. 일반 forward navigation에서 뒤로 움직이면 안 됩니다. Preview page jump로 변경되면 researcher behavior임을 표시합니다.

Back navigation은 valid answer와 persisted assignment를 보존합니다. Refresh/resume은 마지막 committed page, answer, condition, 안전한 history, lifecycle state를 복원합니다. Reset은 명시적 action 후 preview-local state만 지웁니다.

## 7. Researcher controls

Researcher panel은 다음을 제공합니다.

- deterministic condition 선택
- page 및 terminal-outcome jump
- current page, reachable next page, condition, lifecycle state, visit history
- question ID, display label, stored value, type을 포함한 모든 answer
- hidden-answer clearing 및 validation event
- copyable state snapshot
- reset
- automated case가 내장되면 scenario runner result summary
- external write 및 production redirect가 꺼졌다는 visible statement

Forced condition을 바꾸면 condition-dependent answer를 reset하고 assignment boundary로 돌아갑니다. Researcher가 raw page jump를 명시적으로 선택한 경우는 예외입니다. Debug control은 production service를 변경하면 안 됩니다.

## 8. Preview safety

Preview runtime은 fixed trusted code입니다. Survey-authored JavaScript, study content의 inline event handler, `eval`, dynamic code construction, remote script, external font, analytics, network write, production redirect를 금지합니다. Study content는 삽입 전 escape 또는 sanitize합니다. Secret과 service-role credential은 절대 embed하지 않습니다.

Default Content Security Policy는 self-contained artifact에 필요한 local document resource만 허용해야 합니다. Unresolved consent, IRB, redirect, data-policy field는 눈에 띄는 draft text로 표시하고 approved로 표시할 수 없습니다.

## 9. Accessibility baseline

WCAG 2.2 AA를 목표로 합니다. ARIA보다 semantic HTML을 우선하고 visible keyboard focus, logical heading order, native keyboard behavior, 충분한 contrast, labelled status/error message, reduced-motion mode를 제공합니다. Interactive target은 최소 24×24 CSS pixel이고 더 큰 option row를 권장합니다. Radio group은 native browser behavior와 WAI-ARIA Authoring Practices radio-group interaction model을 따릅니다.

Automated check는 keyboard 및 screen-reader review를 대체하지 않습니다. 최소한 Tab/Shift+Tab, radio group의 arrow/Space, disclosure/button의 Enter/Space, validation 후 focus, zoom/reflow, high-contrast 또는 forced-color를 수동 테스트합니다.

## 10. Responsive 및 visual acceptance

320×568, 390×844, 768×1024, 1280×800, 1440×900 CSS pixel과 200% browser zoom에서 테스트합니다. Clipped label, overlapping action, 접근할 수 없는 debug control, 읽기 어려운 matrix, 예상치 않은 page horizontal scroll, sticky region에 가려진 content가 없어야 합니다.

UI는 신뢰할 수 있는 research instrument처럼 조용하고 넓으며 직접적이고 decorative product-marketing 요소가 없어야 합니다. Preview tooling은 더 dense할 수 있지만 respondent layer가 시각적으로 dominant해야 합니다.

## 11. Required scenario suite

Complete reference study는 다음을 모두 실행해야 합니다.

1. 모든 condition의 happy-path completion
2. 모든 required question type의 required-field failure
3. research answer 없는 consent refusal
4. 모든 screen-out route
5. technical error를 포함한 모든 terminal outcome
6. 모든 show/hide branch와 hidden-answer clearing
7. 모든 skip route 및 priority decision
8. Previous와 answer revision
9. assignment 전후 refresh/resume
10. navigation/refresh 동안 assignment invariance
11. display-label/stored-value 정확성
12. complete matrix capture
13. withdrawal/deletion-request 동작
14. production redirect suppression
15. network write 및 secret 부재
16. keyboard-only completion
17. responsive viewport 및 zoom 검사
18. malformed model의 명확한 researcher-facing diagnostic

## 12. Review evidence

`interactive_preview_reviewed`는 preview version/hash, scenario-suite result, viewport/accessibility review result, unresolved deviation, researcher identity 또는 decision reference, 가능한 경우 confirmation timestamp를 요구합니다. Preview 생성 또는 열기만으로 approval이 되지 않습니다.

## References

- [W3C WCAG 2.2: Error Identification](https://www.w3.org/WAI/WCAG22/Understanding/error-identification)
- [W3C WCAG 2.2: Focus Appearance](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html)
- [WAI-ARIA Authoring Practices: Radio Group Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/radio/)
