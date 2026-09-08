# Browser-Native Preview and Runtime

[한국어](./browser-preview(kor).md)

greedyQ v0.2 has one fixed browser core and three rendering modes:

| Mode | Purpose | Selection |
| --- | --- | --- |
| `desktop` | Respondent experience for wide screens and precise pointers | Detected automatically in `index.html` |
| `mobile` | Touch-friendly respondent experience for narrow/mobile devices | Detected automatically in `index.html` |
| `preview` | Researcher review showing independent desktop and mobile sessions together | Always used in `preview.html` |

The browser core performs `QMD/YAML text → parse → validate → normalized model → render`. It does not require Python, Node.js, R, Quarto, or a build tool. `templates/browser/studio.html` accepts local `survey.qmd` and `greedyq.yml` files through browser file selection and performs the entire transformation locally.

## Generated bundle

The current Python reference builder can generate the same static bundle while cross-runtime conformance is being developed:

```bash
python3 -m greedyq build examples/complete-study
```

It writes `index.html`, dual-mode `preview.html`, fixed `greedyq-core.js`, fixed `greedyq-runtime.css`, `preview-model.json`, and internal validation evidence under `.greedyq/`. Generated JavaScript and CSS must match the pinned repository files byte-for-byte. An AI agent may replace only documented study-data slots and must not regenerate or customize the runtime.

## Local simulation

Preview uses virtual participant IDs and a local mock adapter. It tests required answers, display/skip logic, desktop and mobile layouts, balanced persistent assignment, partial-save resume, terminal outcomes, and withdrawal deletion without transmitting data. Desktop and mobile preview panes have independent sessions so both paths can be exercised side by side.

Mock data is synthetic browser-local state, not a claim that Supabase has been configured or verified. Reset removes the virtual sessions. Production credentials and participant identifiers are prohibited in preview.

## Structure overview

Use **View structure** in `preview.html` to see every page, text block, question ID, question type, required marker, and terminal outcome without completing the survey. Pages can be expanded or collapsed. This is a read-only aid inspired by the useful hierarchy view in sdstudio's Build tab; it does not implement sdstudio and cannot edit the QMD.

## Live control gallery

The built [control gallery](https://zomtoli7.github.io/greedyQ/examples/control-gallery/preview.html) exercises every supported control in the same desktop/mobile preview. GitHub Pages publishes the canonical static example from `main`; no Vercel or Supabase account is needed to view it.

## Deployment boundary

All deterministic behavior must pass locally before external connection. Vercel receives the already-tested static bundle and serves it; it must not reinterpret the questionnaire. Supabase replaces only the persistence/assignment adapter through approved RPCs and row-level security. Connecting Supabase must not alter parsing, validation, rendering, routing, consent, or outcome semantics.

The preview Content Security Policy blocks network writes. The participant entry point permits HTTPS only because production Supabase RPCs require it. Service-role keys, database passwords, administrator credentials, and randomization secrets must never be placed in browser files.

## Required review scenarios

Before deployment, test desktop and mobile completion; required answers and numeric limits; consent refusal and screening; every condition; conditional questions and hidden-answer removal; back, save, refresh, and resume; withdrawal/deletion; every terminal outcome; keyboard focus, zoom, and narrow-screen overflow.
