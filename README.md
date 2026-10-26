# greedyQ

<!-- GREEDYQ_DESKTOP_POLICY -->
**greedyQ requires an installed desktop AI app for creating or modifying studies. AI web apps are officially unsupported.** Download ChatGPT desktop or Claude Desktop from the official provider. Gemini is not officially supported, including its desktop app. Use an agent-enabled mode that can read the complete guide, create real files and run the canonical preview; installing an app or paying for a model alone does not establish these capabilities. Ordinary desktop chat without these tools is not a supported authoring route. Participant surveys, computer/mobile previews and the researcher results page still run in a web browser. [Supported authoring environment](SUPPORTED-ENVIRONMENTS.md).
<!-- /GREEDYQ_DESKTOP_POLICY -->

- **Current specification:** `0.2`
- **Current release:** `0.2_2026-10-26_df6d737`
- **Release source commit:** [`df6d737`](https://github.com/zomtoli7/greedyQ/commit/df6d7375a20141a46e5b3bb13eed3dd51ea694b7) · [Update history](./updates/README.md)

[Compatibility audit](./docs/surveydown-compatibility-audit.md) · [Preregistration drafts](./PREREGISTRATION.md) · [Resume and upgrade](./UPGRADING.md) · [External returns](./EXTERNAL-RETURNS.md) · [Google Sites plan](./docs/google-sites-plan.md)

[Finish and archive a study](./ARCHIVING.md) · [Cloud lifecycle operator contract](./docs/cloud-lifecycle.md)

[Random assignment and question shuffling](./RANDOMIZATION.md) · [Local verification and upgrade status](./docs/randomization-verification.md)

[한국어](./README(kor).md) · [简体中文](./README(zh-CN).md)

[Start a survey](./START-HERE.md) · [User guide](./USER-GUIDE.md) · [Connect to Prolific](./PROLIFIC-SETUP.md) · [Results dashboard](./RESULTS-DASHBOARD.md) · [Control gallery](https://zomtoli7.github.io/greedyQ/examples/control-gallery/preview.html)

> **Be greedy with your time. Just ask your AI to make your questionnaire.**

greedyQ is a specification-driven, AI-native application for online academic research. Rather than implementing the application itself in conventional source code, greedyQ specifies how a general-purpose generative AI agent should instantiate and operate the application.

Its portable Markdown, schemas, checkpoints, and exact templates form an **agent-executable application specification**. A researcher opens a supported ChatGPT or Claude desktop agent and points it to the versioned greedyQ repository and starts with an ordinary request such as “Let's build a survey.” The instantiated research agent then conducts the guided research workflow and produces both research-design artifacts and executable respondent-facing survey software.

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
6. Review and approve the preregistration draft files; handle any actual registration independently before fielding when required.
7. Let a connected agent configure GitHub, Vercel, and Supabase, or follow the generated handoff instructions.
8. Approve and publish the web-native survey and, when useful, export the native surveydown project.

## Interaction modes and alternative paths

Study authoring requires a supported installed ChatGPT or Claude desktop agent with working file and preview tools. A tool-less Chat mode is not supported. Account tools and researcher authorization are checked separately before deployment; local preview needs no service account. See [supported AI environments](./SUPPORTED-ENVIRONMENTS.md).

Expert users may still author `survey.qmd` and `greedyq.yml` directly. Researchers who need unrestricted R, Shiny, or Quarto customization can continue from the generated native surveydown project. A later PPTX importer will turn existing slide-based drafts into editable study artifacts that enter the same guided review workflow.

## Relationship to surveydown

greedyQ is an independent implementation of surveydown-style `survey.qmd` syntax. Its v0.2 browser runtime implements all 16 question controls in the current official question-types documentation and adds media, ranking, side-by-side, NPS, timing, constant-sum, grouping/ranking, drill-down, and confirmed custom controls as greedyQ extensions; other syntax remains explicitly classified by compatibility level. It does not incorporate surveydown source code and is not affiliated with or endorsed by the surveydown project or its maintainers. Compatibility does not limit greedyQ-native features: each feature is classified as directly portable, generated into `app.R`, or greedyQ-only with an explicit export diagnostic. See [NOTICE.md](./NOTICE.md) for attribution and license information.

## Citation

Until a greedyQ paper is available, scholarly work using greedyQ should cite both the [greedyQ GitHub repository](https://github.com/zomtoli7/greedyQ), with the exact release identifier recorded in `survey.qmd`, and the [surveydown PLOS ONE paper](https://doi.org/10.1371/journal.pone.0331002). This applies even when only the independent greedyQ browser runtime is used. Copy-ready references and methods wording are provided in [CITATION.md](./CITATION.md).

## Project status

greedyQ provides a browser-native v0.2 runtime with account-free local preview. The fixed JavaScript core parses QMD/YAML, validates and compiles supported syntax, renders adaptive desktop/mobile surveys and dual previews, and conforms to the Python reference on the golden studies, control gallery and negative fixtures. Vercel/Supabase deployment, protected results, canonical migrations 001–008, Prolific identifier capture, preregistration drafts, native surveydown export and offline preflight are implemented.

On 2026-10-26, the one-person Prolific paid pilot was matched to saved responses and exported CSV. The researcher confirmed participant approval and payment; a separate provider payment receipt was not independently inspected. The previously paused review is historical, not the current pilot status. The test data were deleted at the researcher's request during closeout; provider payment records were preserved. Normal completion, refusal, withdrawal, repeat draft previews, protected results and real/test separation have recorded evidence. Signed links, repeated production submissions and a paid screened-out path remain outside verified scope. See [paid completion](./docs/prolific-paid-test-completion-2026-10-26.md), [closeout](./docs/v0.2-closeout-2026-10-26.md), and [current Prolific status](./docs/prolific-integration-status.md).

CBC is the **v0.3 development line**, not a supported v0.2 profile or control. Its opt-in draft code and local fixtures may exist in this repository; that does not make CBC a completed v0.2 feature. Cloud and paid CBC acceptance remain pending.

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

Developer commands require Python 3; participant screen checks always use the same JavaScript renderer. Run `python3 -m greedyq run examples/complete-study` and open `http://localhost:4180/index.html`. Mock responses stay in the browser. See the [local respondent runtime guide](./docs/local-respondent-runtime.md).

See [START-HERE.md](./START-HERE.md), the [research framing](./docs/research-framing.md), [AI guides](./guides/README.md), [modular guide architecture](./docs/modular-guide-architecture.md), [product brief](./docs/product-brief.md), [greedyQ v0.2 specification](./docs/greedyq-v0.2-spec.md), [browser preview guide](./docs/browser-preview.md), [local respondent runtime](./docs/local-respondent-runtime.md), [local operations and recovery runbook](./docs/operations-runbook.md), [golden reference studies](./examples/README.md), [surveydown compatibility research](./docs/surveydown-compatibility.md), and [roadmap](./docs/roadmap.md) for the current direction.

## Documentation policy

English Markdown files are the source of truth. Every Markdown document has a synchronized Korean copy whose filename ends in `(kor).md`. Code, identifiers, paths, configuration keys, and normative syntax remain unchanged in translations.

## License

greedyQ is distributed under the [MIT License](./LICENSE).

## Vercel connection approach

The main journey is survey review → Vercel sign-in and required Supabase connection approval → verified Survey and Results links. The AI prefers an existing official Vercel connection after checking account and target team, and uses the established supported route when the connection or operation is unavailable. **Onboard your agent is optional, not a required setup step.** See the [user guide](./USER-GUIDE.md) and [optional preparation guide](./docs/vercel-agent-onboarding.md).

Entry, user and AI guides also have Simplified Chinese `(zh-CN).md` copies. This does not imply that every developer document is translated.

Next: [v0.3 CBC specification and blank design tables](./drafts/v0.3/cbc/README.md) — CSV/XLSX import and local browser preview now work; live collection remains on v0.2.

## CBC preview and project contact

For choice-based conjoint tables, see [CBC import and computer/mobile preview](CBC.md). The preview itself does not collect responses; use the separate [CBC collection package](CBC-COLLECT.md) for the server-backed CBC workflow. Its local verification is distinct from cloud fielding approval. For project questions or bug reports: [greedyq.contact@gmail.com](CONTACT.md). Individual studies must provide their own research-team contact.
