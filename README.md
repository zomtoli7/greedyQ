# greedyQ

[한국어](./README(kor).md)

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
     GitHub -> Vercel -> Supabase
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

greedyQ is an independent implementation that supports a documented subset of surveydown-style `survey.qmd` syntax. It does not incorporate surveydown source code and is not affiliated with or endorsed by the surveydown project or its maintainers. Compatibility does not limit greedyQ-native features: each feature is classified as directly portable, generated into `app.R`, or greedyQ-only with an explicit export diagnostic. See [NOTICE.md](./NOTICE.md) for attribution and license information.

## Project status

greedyQ is in the specification and working-preview phase. The current Python-based reference implementation requires a Python interpreter but no third-party Python packages. It parses the supported v0.2 QMD subset, validates structural and routing errors, builds a normalized model, and serves a self-contained researcher preview. It is the semantic reference for development, not the final-user dependency. The browser-native JavaScript core and production Supabase/Vercel runtime are not implemented yet.

## Try the current reference preview

From the repository root, run:

```bash
python3 -m greedyq preview examples/complete-study
```

Your browser should open `http://localhost:4173/preview.html`. To try the simple survey instead:

```bash
python3 -m greedyq preview examples/simple-satisfaction-study
```

Use `python3 -m greedyq validate PATH_TO_STUDY` to check a study without generating a preview, or `python3 -m greedyq build PATH_TO_STUDY` to create `preview-model.json`, `preview.html`, and normalized validation artifacts without starting a server. No respondent data leaves the browser in preview mode. See the [browser preview guide](./docs/browser-preview.md).

These commands currently require Python 3 and are intended for development and conformance work. The planned final-user path needs only a capable AI and a modern browser. To test durable respondent sessions locally, run `python3 -m greedyq run examples/complete-study` and open `http://localhost:4180/study`. This test runtime writes responses to a local ignored SQLite database; it is not yet the Supabase/Vercel production runtime. See the [runtime architecture](./docs/runtime-architecture.md) and [local respondent runtime guide](./docs/local-respondent-runtime.md).

See [START-HERE.md](./START-HERE.md), the [research framing](./docs/research-framing.md), [AI guides](./guides/README.md), [modular guide architecture](./docs/modular-guide-architecture.md), [product brief](./docs/product-brief.md), [greedyQ v0.2 specification](./docs/greedyq-v0.2-spec.md), [browser preview guide](./docs/browser-preview.md), [local respondent runtime](./docs/local-respondent-runtime.md), [golden reference studies](./examples/README.md), [surveydown compatibility research](./docs/surveydown-compatibility.md), and [roadmap](./docs/roadmap.md) for the current direction.

## Documentation policy

English Markdown files are the source of truth. Every Markdown document has a synchronized Korean copy whose filename ends in `(kor).md`. Code, identifiers, paths, configuration keys, and normative syntax remain unchanged in translations.

## License

greedyQ is distributed under the [MIT License](./LICENSE).
