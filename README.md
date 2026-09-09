# greedyQ

[한국어](./README(kor).md)

- **Current specification:** `0.2`
- **Current release:** `0.2_2026-09-09_236d2a3`
- **Release source commit:** [`3aefdd0`](https://github.com/zomtoli7/greedyQ/commit/5ce7a3a) · [Update history](./updates/README.md)

[Start a survey](./START-HERE.md) · [User guide](./USER-GUIDE.md) · [Results dashboard](./RESULTS-DASHBOARD.md) · [Control gallery](https://zomtoli7.github.io/greedyQ/examples/control-gallery/preview.html)

> **Be greedy with your time. Just ask your AI to make your questionnaire.**

greedyQ is a specification-driven, AI-native application for online academic research. Rather than implementing the application itself in conventional source code, greedyQ specifies how a general-purpose generative AI agent should instantiate and operate the application.

Its portable Markdown, schemas, checkpoints, and exact templates form an **agent-executable application specification**. A researcher points GPT, Claude, or another capable general-purpose AI to the versioned greedyQ repository and starts with an ordinary request such as “Let's build a survey.” The instantiated research agent then conducts the guided research workflow and produces both research-design artifacts and executable respondent-facing survey software.

## greedyQ as an AI-native application

greedyQ itself is not an agent. The distinction is:

```text
greedyQ agent-executable application specification
                         +
              capable host GenAI
                         =
             greedyQ research agent
                         |
                         v
       research-design artifacts + survey application
```

This architecture has three layers:

1. **Architecture — specification-driven AI-native application.** Application behavior is defined and distributed primarily through a human-readable, agent-executable specification rather than a conventional application codebase alone.
2. **Domain — online academic research.** The scope includes research design, consent, questionnaires, experiments, randomization, respondent panels, data plans, preregistration, deployment, and fielding—not surveys alone.
3. **Implementation — greedyQ.** greedyQ is the concrete application of this architecture to reproducible online academic research.

The host model may present different interfaces or use different native capabilities, but it must apply the same normative research specification. Portability therefore means that GPT, Claude, Gemini, or another capable general-purpose AI can instantiate greedyQ while remaining testable against common conformance requirements.

The AI supplies research reasoning and natural-language collaboration. The greedyQ specification supplies the interview protocol, approval checkpoints, artifact contracts, validation requirements, preregistration workflow, runtime templates, deployment contract, and reproducibility boundaries.

## Why greedyQ?

Commercial survey platforms can be expensive, difficult to reproduce, and restrictive for complex experimental designs. Surveydown offers a strong survey-as-code model, but its R, Quarto, and Shiny toolchain can be a barrier for researchers.

greedyQ keeps the good parts:

- Human-readable survey definitions
- Git-based version control and reproducibility
- Researcher-owned PostgreSQL data
- Programmable research workflows

It provides its own deterministic, browser-native JavaScript runtime designed for GitHub, Vercel, and Supabase, then makes that stack usable through a guided AI conversation. It also generates `app.R` and related native surveydown artifacts as a first-class escape hatch for researchers who need unrestricted R, Shiny, or Quarto customization.

## Product principles

- `survey.qmd` is the source of truth for survey content and questions.
- The user-facing QMD syntax should be compatible with surveydown wherever practical.
- The Vercel/Supabase runtime is the primary execution target.
- The final-user parser, validator, preview, and renderer run in a modern browser without requiring Python or Node.js.
- A dependency-light Python implementation establishes reference semantics during development and remains available for conformance testing and developer tooling.
- The Python and JavaScript implementations must pass the same fixtures and produce semantically equivalent normalized ASTs, diagnostics, and rendered behavior.
- Native surveydown export, including generated `app.R`, is a core output path.
- Compatibility is implemented independently from public documentation; surveydown source code is not incorporated.
- Arbitrary R and Shiny code is not executed.
- Conditional logic and randomization are declarative, safe, and reproducible.
- Researchers own and control their respondent data.
- No GUI survey builder is required.
- The primary user experience is a guided conversation with a general-purpose LLM.
- The LLM provides research intelligence; greedyQ provides workflow, specification, validation, and reproducibility.
- Material research decisions require explicit researcher confirmation.
- A fielding-ready study should generate a reviewable preregistration package before sample collection begins.
- The workflow must detect whether it can act through connected tools or must provide files and instructions for the user.

## Primary workflow

For a nontechnical, click-by-click walkthrough, begin with the [greedyQ User Guide](./USER-GUIDE.md).

```text
Versioned greedyQ repository + researcher's study idea
                         |
                         v
              Guided AI interview
                         |
     research design -> consent -> questions
     -> logic -> randomization -> analysis plan
                         |
                         v
 survey files + preregistration package + assets
                         |
                         v
           parser -> Survey AST -> validator
                    /             \
                   v               v
      preview and approval    native export
              |              survey.qmd + app.R
              v
     GitHub -> Vercel public survey + protected results -> Supabase
```

The target onboarding experience is:

1. Share the tagged greedyQ `START-HERE.md` URL with a capable LLM or repository agent. Use the self-contained bundle only when repository links cannot be read.
2. Say what study you want to build.
3. Answer one focused question at a time and confirm material decisions.
4. Review the generated study, consent, logic, randomization, data plan, and preregistration draft.
5. Validate and preview the generated project.
6. Explicitly approve the preregistration package and submit it manually or through an authorized connected agent before fielding.
7. Let a connected agent configure GitHub, Vercel, and Supabase, or follow the generated handoff instructions.
8. Approve and publish the web-native survey and, when useful, export the native surveydown project.

## Interaction modes and alternative paths

The guide supports two capability-dependent modes:

- **Chat mode:** The AI conducts the interview, creates the project files, validates its reasoning against the guide, and gives the user deployment instructions.
- **Agent mode:** A connected agent can additionally edit the repository, run validation, configure services, deploy, and verify the live survey.

Expert users may still author `survey.qmd` and `greedyq.yml` directly. Researchers who need unrestricted R, Shiny, or Quarto customization can continue from the generated native surveydown project. A later PPTX importer will turn existing slide-based drafts into editable study artifacts that enter the same guided review workflow.

## Relationship to surveydown

greedyQ is an independent implementation of surveydown-style `survey.qmd` syntax. Its v0.2 browser runtime implements all 16 question controls in the current official question-types documentation and adds media, ranking, side-by-side, NPS, timing, constant-sum, grouping/ranking, drill-down, and confirmed custom controls as greedyQ extensions; other syntax remains explicitly classified by compatibility level. It does not incorporate surveydown source code and is not affiliated with or endorsed by the surveydown project or its maintainers. Compatibility does not limit greedyQ-native features: each feature is classified as directly portable, generated into `app.R`, or greedyQ-only with an explicit export diagnostic. See [NOTICE.md](./NOTICE.md) for attribution and license information.

## Citation

Until a greedyQ paper is available, scholarly work using greedyQ should cite both the [greedyQ GitHub repository](https://github.com/zomtoli7/greedyQ), with the exact release identifier recorded in `survey.qmd`, and the [surveydown PLOS ONE paper](https://doi.org/10.1371/journal.pone.0331002). This applies even when only the independent greedyQ browser runtime is used. Copy-ready references and methods wording are provided in [CITATION.md](./CITATION.md).

## Project status

greedyQ now has an account-free, connection-ready v0.2 runtime candidate. The fixed JavaScript core parses QMD/YAML, validates and compiles the supported syntax, renders all documented surveydown question controls in adaptive desktop/mobile respondent views, and renders both views together with mock persistence and assignment for local review. Its normalized output conforms to the Python reference on the golden studies, the complete control gallery, and negative validator fixtures. Static Vercel files, canonical Supabase RPC migrations, Prolific launch validation, preregistration drafts, native surveydown export, and offline preflight are implemented. Live service connection and verification remain deliberately unperformed; see [external connection readiness](./docs/external-connection-readiness.md).

## Try the responsive preview

No-install path: open `examples/complete-study/preview.html` directly in a modern browser. It shows independent desktop and mobile sessions together. Open `studio.html` in the same folder to select a `survey.qmd` and `greedyq.yml` and parse, validate, compile, and preview them entirely in the browser.

The following Python commands remain available for reference development and deterministic regeneration:

From the repository root, run:

```bash
python3 -m greedyq preview examples/complete-study
```

Your browser should open `http://localhost:4173/preview.html`. To try the simple survey instead:

```bash
python3 -m greedyq preview examples/simple-satisfaction-study
```

Use `python3 -m greedyq validate PATH_TO_STUDY` to check a study without generating a preview, or `python3 -m greedyq build PATH_TO_STUDY` to create the fixed browser bundle (`index.html`, `preview.html`, `studio.html`, JavaScript, CSS, and normalized artifacts) without starting a server. No respondent data leaves the browser in preview mode. See the [browser preview guide](./docs/browser-preview.md).

These commands currently require Python 3 and are intended for development and conformance work. The planned final-user path needs only a capable AI and a modern browser. To test durable respondent sessions locally, run `python3 -m greedyq run examples/complete-study` and open `http://localhost:4180/study`. This test runtime writes responses to a local ignored SQLite database; it is not yet the Supabase/Vercel production runtime. See the [runtime architecture](./docs/runtime-architecture.md) and [local respondent runtime guide](./docs/local-respondent-runtime.md).

See [START-HERE.md](./START-HERE.md), the [research framing](./docs/research-framing.md), [AI guides](./guides/README.md), [modular guide architecture](./docs/modular-guide-architecture.md), [product brief](./docs/product-brief.md), [greedyQ v0.2 specification](./docs/greedyq-v0.2-spec.md), [browser preview guide](./docs/browser-preview.md), [local respondent runtime](./docs/local-respondent-runtime.md), [golden reference studies](./examples/README.md), [surveydown compatibility research](./docs/surveydown-compatibility.md), and [roadmap](./docs/roadmap.md) for the current direction.

## Documentation policy

English Markdown files are the source of truth. Every Markdown document has a synchronized Korean copy whose filename ends in `(kor).md`. Code, identifiers, paths, configuration keys, and normative syntax remain unchanged in translations.

## License

greedyQ is distributed under the [MIT License](./LICENSE).
