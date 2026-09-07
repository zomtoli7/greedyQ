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

- Treat `docs/product-brief.md` as the current product-direction reference.
- Treat `docs/roadmap.md` as the current implementation-order reference.
- Treat AI-guided study creation and deployment as the primary user experience.
- Treat direct QMD authoring as an expert path and PPTX conversion as an import path.
- Let the chosen LLM provide research reasoning; keep interview workflow, approval checkpoints, artifact contracts, validation, and reproducibility deterministic in greedyQualt.
- Require explicit researcher confirmation for material research decisions.
- Distinguish chat mode from agent mode and never claim an external service was configured without connected tools and verified results.
- Prioritize specification work before runtime implementation.
- Target public, user-facing surveydown compatibility without copying its internal implementation.
- Do not execute arbitrary R or JavaScript from survey definitions.
- Preserve researcher ownership and control of respondent data.
- Do not introduce a GUI survey builder unless the product direction is explicitly changed.

## Engineering

- Prefer deterministic, statically validatable formats and behavior.
- Version normative specifications and generated artifacts.
- Add conformance tests for documented syntax and behavior.
- Keep the core workflow usable without R, RStudio, Quarto, or Shiny.
