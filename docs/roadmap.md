# greedyQ Roadmap

[한국어](./roadmap(kor).md)

**Current line:** v0.2 supported-scope maintenance; v0.3 CBC specification and golden-reference design
**Planning principle:** Specification before implementation

## Delivered in v0.2

- Specification-driven, AI-native research workflow with repository-first start, resumable decisions, and researcher approval gates.
- `greedyQSimple` and `greedyQExperiment` profiles, modular guides, hashed registry, English/Korean documentation pairs, and two golden studies plus a control gallery.
- Dependency-light Python reference parser, validator, compiler, local runtime, and browser preview server.
- Platform-neutral JavaScript parser, validator, renderer, respondent runtime, dual desktop/mobile preview, and researcher structure view.
- The 16 documented Surveydown question controls plus greedyQ media and advanced controls: rank order, side-by-side, NPS, timing, constant sum, pick/group/rank, drill down, and confirmed custom controls.
- Consent-first collection, persistent sessions, withdrawal deletion, deterministic assignment, direct/Prolific source marking, test-response separation, Supabase RPC boundary, and Vercel static deployment bundle.
- Researcher results dashboard with real/test and direct/Prolific filters, progress and condition summaries, analysis-ready structured CSV columns, and a variable guide.
- Preregistration drafts, manifests, Prolific routes, native Surveydown project export, and explicit compatibility reports.
- Standard Prolific launches with atomic ID binding, duplicate protection, private expiring repeat-preview grants, withdrawal answer erasure, protected identity-bearing CSV and explicit provider-review waiting states.
- Stable checks for syntax/routes, stored-value references, durable `.greedyq` state, manifest hashes, migration safety contracts, and secret placement.

## v0.2 stabilization gates

- [x] Python/JavaScript parser and normalized-model conformance fixtures.
- [x] Desktop, mobile, and dual-preview rendering with responsive matrix and NPS behavior.
- [x] Structured advanced-control collection and analysis-ready CSV export.
- [x] Surveydown `sd_question_custom()` generation for greedyQ-only controls.
- [x] R syntax validation for generated `app.R` in the development environment.
- [x] Offline deployment preflight and deterministic unit/regression suite.
- [x] Real-browser E2E at 320px, 390px, 768px, and 1280px, including conditional display, structured controls, resume, terminal navigation, dashboard filters, and CSV download.
- [x] Ordered Supabase migration manifest with checksum verification, tamper detection, and recovery guidance.
- [x] Scripted AI-workflow conformance scenarios for new researcher-written and AI-assisted studies, modification, fork, custom controls, preview approval, and external-action truthfulness.
- [x] Generated Surveydown projects checked against the public Surveydown 1.3.0 API; generated app and QMD R blocks pass R syntax validation.
- [x] The complete native Surveydown control gallery renders and starts in safe preview mode with Surveydown 1.3.0, R, Quarto, and Shiny without a database account.
- [ ] Deferred scope: native Surveydown behavioral review of every generated custom control in a running Shiny application; no full-equivalence claim.
- [x] Researcher-assisted fresh-account Vercel/Supabase connection test on 2026-09-10; migrations through 008 additionally verified on the dedicated connected test resource. See the dated evidence rather than assuming acceptance for every future account/version.
- [x] Actual Prolific draft Preview for completion, refusal, withdrawal and repeat starts; protected results and erasure checked.
- [x] One genuine paid Prolific submission matched to stored answers and CSV; approval/payment explicitly confirmed by the researcher on 2026-10-26, not independently fetched from a payment API.
- [x] Dedicated closed-study screen already implemented; startup/in-flight closure and distinct network failures rechecked at desktop/mobile widths in four participant languages.
- [x] Researcher-authorized immediate cleanup on 2026-10-26: active trial response/ID tables empty, known private copies removed, collection closed; Prolific payment records preserved.
- [ ] Deferred research: cross-model creation/modification/fork evaluations with capable hosts.
- [ ] Deferred research: assistive-technology audit and recruited researcher usability study; existing keyboard/responsive regression remains required.

## Next product work

1. Make CBC the core v0.3 feature. Start with the [draft contract and golden fixture](../drafts/v0.3/cbc/README.md): offer AI collaboration, blank CSV/XLSX to fill independently, or existing design import. This is design-only, not an activated v0.2 capability.
2. Implement reference import/validation, then the same browser-native contract, CBC presentation, durable assignments/orders, withdrawal-safe storage and long-format export. Register CBC only after conformance passes.
3. Keep v0.2's approved Vercel/Supabase/direct/Prolific journey stable. A first new real post-008 timestamp and actual paid custom-screening policy remain target-specific checks, not reasons to repeat the completed paid pilot.
4. Later: monitoring, configurable retention, live disaster recovery, stratified/adaptive allocation, factorial designs and reproducible design generators. Simple weighted ratios and supported question/option/page shuffling already exist; do not list them as unimplemented.
5. Later: additional participant-language packs, PPTX import and the portability/conformance study for the white paper. Maintain downloadable OSF drafts; registry login/submission remains out of scope.
6. Website publication belongs to the separate homepage Work. Do not claim publication from source generation. The paid trial's active-data cleanup is complete, while provider backups and researcher-controlled copies were not inspected.

## Closure evidence and limits

See [v0.2 closeout](./v0.2-closeout-2026-10-26.md), [paid completion](./prolific-paid-test-completion-2026-10-26.md), and [CBC planning](../drafts/v0.3/cbc/README.md). Supported-scope closure does not promise full Surveydown settings equivalence, every native custom-control behavior, signed Prolific links, payment automation, all environments or statistical design efficiency.

## Permanent requirements

- English Markdown is authoritative and every file has a synchronized `(kor).md` copy.
- Never execute arbitrary survey-authored R or JavaScript in the primary runtime.
- Keep the primary workflow usable with a capable AI and a modern browser, without Python, R, Quarto, or Node on the researcher's device.
- Preserve researcher ownership, consent-first storage, reproducible assignment, and truthful verification of external operations.
- Use independently authored code based on public Surveydown documentation; attribute Surveydown and recommend citing both Surveydown and greedyQ.
