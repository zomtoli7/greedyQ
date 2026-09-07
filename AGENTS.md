# Repository Instructions

[한국어](./AGENTS(kor).md)

## Communication

- Use Korean as the default language when communicating with the project owner.
- Use English when it improves technical precision or preserves an established term.

## Documentation

- Write every Markdown document in English as the source of truth.
- Create a synchronized Korean copy beside it with `(kor)` immediately before `.md`.
- Example: `docs/example.md` and `docs/example(kor).md`.
- Keep headings, structure, examples, links, specification versions, and material content aligned across each pair.
- Do not translate code, identifiers, file paths, configuration keys, or normative syntax.
- Link each language version to its counterpart near the top of the document.
- Update both language versions in the same change.

## Product direction

- Define greedyQ as a specification-driven, AI-native application for online academic research, and its normative bundle as an agent-executable application specification.
- Keep the entities distinct: greedyQ is not an agent; the greedyQ specification plus a capable host GenAI instantiates a greedyQ research agent, which then produces research artifacts and respondent-facing survey software.
- Treat cross-model portability and conformance as core research and engineering goals; host-specific interfaces may differ, but normative decisions, participant protections, artifact semantics, and truthful status must remain testable invariants.
- Treat `docs/product-brief.md` as the current product-direction reference.
- Treat `docs/greedyq-v0.1-spec.md` as the current normative-format draft and `examples/complete-study/` as its pre-implementation golden reference.
- Treat `docs/roadmap.md` as the current implementation-order reference.
- Treat AI-guided study creation and deployment as the primary user experience.
- Treat `START-HERE.md` plus the generated guide registry as the default distribution path; keep the self-contained full guide as an attachment-only fallback.
- Treat researchers as nontechnical end users. Keep ordinary conversation and `study-plan.md` free of implementation diagnostics; store detailed validation evidence under `.greedyq/`.
- Model studies as a core `greedyQObject`, one public study profile, and composable capability modules pinned by `.greedyq/guide-lock.json`.
- Treat direct QMD authoring as an expert path and PPTX conversion as an import path.
- Let the chosen LLM provide research reasoning; keep interview workflow, approval checkpoints, artifact contracts, validation, and reproducibility deterministic in greedyQ.
- Require explicit researcher confirmation for material research decisions.
- Treat preregistration as a first-class generated artifact and pre-fielding gate; never invent unresolved commitments or submit to a registry without explicit approval and verification.
- Distinguish chat mode from agent mode and never claim an external service was configured without connected tools and verified results.
- Prioritize specification work before runtime implementation.
- Target public, user-facing surveydown compatibility without copying its internal implementation.
- Do not incorporate surveydown source code, tests, or copied fixtures; author implementations and conformance fixtures independently from public documentation and observable behavior.
- Keep the Vercel/Supabase web-native runtime primary while treating generated native surveydown projects, including `app.R`, as a first-class output.
- Classify export behavior as directly portable, generated, greedyQ-only, or unsupported, and report every material mismatch.
- Do not execute arbitrary R or JavaScript from survey definitions.
- Preserve researcher ownership and control of respondent data.
- Do not introduce a GUI survey builder unless the product direction is explicitly changed.

## Engineering

- Prefer deterministic, statically validatable formats and behavior.
- Version normative specifications and generated artifacts.
- Add conformance tests for documented syntax and behavior.
- Keep the core workflow usable without R, RStudio, Quarto, or Shiny.
