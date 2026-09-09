# greedyQ Roadmap

[한국어](./roadmap(kor).md)

**Current line:** v0.2 stabilization
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
- [ ] Native Surveydown behavioral review of every generated custom control in a running Shiny application.
- [ ] Fresh-account, one-click Vercel/Supabase provisioning test; this requires user-approved OAuth connections.
- [ ] Cross-model creation/modification/fork evaluations with GPT, Claude, Gemini, and other capable hosts.
- [ ] Accessibility audit with assistive technology and a recruited non-technical researcher usability study.

## Next product work

1. Complete the external OAuth provisioning experience so a researcher signs into Vercel and receives only a survey URL and results URL.
2. Add production observability, researcher-configurable retention controls, and live disaster-recovery exercises. Offline migration versioning, integrity checks, and recovery guidance are complete.
3. Expand experimental designs: weighted/stratified assignment, factorial studies, reproducible seeds, CBC/conjoint, and external design tables.
4. Add multilingual authoring and respondent presentation.
5. Add live OSF/preregistration adapters while preserving an explicit final-submission approval gate.
6. Build the PPTX import path with confidence and conversion reports.
7. Conduct the portability/conformance study that will support the greedyQ white paper.

## Permanent requirements

- English Markdown is authoritative and every file has a synchronized `(kor).md` copy.
- Never execute arbitrary survey-authored R or JavaScript in the primary runtime.
- Keep the primary workflow usable with a capable AI and a modern browser, without Python, R, Quarto, or Node on the researcher's device.
- Preserve researcher ownership, consent-first storage, reproducible assignment, and truthful verification of external operations.
- Use independently authored code based on public Surveydown documentation; attribute Surveydown and recommend citing both Surveydown and greedyQ.
