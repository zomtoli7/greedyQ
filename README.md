# greedyQ

[한국어](./README(kor).md)

> **Be greedy with your time. Just ask your AI to make your questionnaire.**

greedyQ is an open-source, AI-guided survey and experimental research workflow backed by a deterministic Markdown-first engine. Its primary target is an independent web-native runtime deployed with Vercel and Supabase, while the same study can also be exported as a native surveydown project. A researcher gives a versioned greedyQ guide to GPT, Claude, or another capable agent and starts with a simple request such as “Let's build a survey.” The AI interviews the researcher, records confirmed decisions, produces valid study files, validates them, and—when connected tools are available—sets up deployment services.

The AI supplies research reasoning and natural-language collaboration. greedyQ supplies the interview protocol, approval checkpoints, specification, validator, runtime, deployment contract, and reproducibility. The project is intended for academic studies that require auditable consent, external respondent panels, branching, persistent random assignment, factorial experiments, or conjoint/CBC designs.

## Why greedyQ?

Commercial survey platforms can be expensive, difficult to reproduce, and restrictive for complex experimental designs. Surveydown offers a strong survey-as-code model, but its R, Quarto, and Shiny toolchain can be a barrier for researchers.

greedyQ keeps the good parts:

- Human-readable survey definitions
- Git-based version control and reproducibility
- Researcher-owned PostgreSQL data
- Programmable research workflows

It provides its own TypeScript and React runtime designed for GitHub, Vercel, and Supabase, then makes that deterministic stack usable through a guided AI conversation. It also generates `app.R` and related native surveydown artifacts as a first-class escape hatch for researchers who need unrestricted R, Shiny, or Quarto customization.

## Product principles

- `survey.qmd` is the source of truth for survey content and questions.
- The user-facing QMD syntax should be compatible with surveydown wherever practical.
- The Vercel/Supabase runtime is the primary execution target.
- Native surveydown export, including generated `app.R`, is a core output path.
- Compatibility is implemented independently from public documentation; surveydown source code is not incorporated.
- Arbitrary R and Shiny code is not executed.
- Conditional logic and randomization are declarative, safe, and reproducible.
- Researchers own and control their respondent data.
- No GUI survey builder is required.
- The primary user experience is a guided conversation with a general-purpose LLM.
- The LLM provides research intelligence; greedyQ provides workflow, specification, validation, and reproducibility.
- Material research decisions require explicit researcher confirmation.
- The workflow must detect whether it can act through connected tools or must provide files and instructions for the user.

## Primary workflow

```text
Versioned greedyQ guide + researcher's study idea
                         |
                         v
              Guided AI interview
                         |
     research design -> consent -> questions
     -> logic -> randomization -> respondent source
                         |
                         v
 survey.qmd + greedyq.yml + design/*.csv + assets
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

1. Attach the versioned greedyQ guide to a capable LLM or agent.
2. Say what study you want to build.
3. Answer one focused question at a time and confirm material decisions.
4. Review the generated study, consent, logic, randomization, and data plan.
5. Validate and preview the generated project.
6. Let a connected agent configure GitHub, Vercel, and Supabase, or follow the generated handoff instructions.
7. Approve and publish the web-native survey and, when useful, export the native surveydown project.

## Interaction modes and alternative paths

The guide supports two capability-dependent modes:

- **Chat mode:** The AI conducts the interview, creates the project files, validates its reasoning against the guide, and gives the user deployment instructions.
- **Agent mode:** A connected agent can additionally edit the repository, run validation, configure services, deploy, and verify the live survey.

Expert users may still author `survey.qmd` and `greedyq.yml` directly. Researchers who need unrestricted R, Shiny, or Quarto customization can continue from the generated native surveydown project. A later PPTX importer will turn existing slide-based drafts into editable study artifacts that enter the same guided review workflow.

## Relationship to surveydown

greedyQ is an independent implementation that supports a documented subset of surveydown-style `survey.qmd` syntax. It does not incorporate surveydown source code and is not affiliated with or endorsed by the surveydown project or its maintainers. Compatibility does not limit greedyQ-native features: each feature is classified as directly portable, generated into `app.R`, or greedyQ-only with an explicit export diagnostic. See [NOTICE.md](./NOTICE.md) for attribution and license information.

## Project status

greedyQ is in the specification phase. The current milestone is to turn the completed surveydown compatibility research into the greedyQ v0.1 specification and the versioned guided-interview protocol before implementing the runtime.

See the [product brief](./docs/product-brief.md), [greedyQ v0.1 specification](./docs/greedyq-v0.1-spec.md), [complete reference study](./examples/complete-study/README.md), [surveydown compatibility research](./docs/surveydown-compatibility.md), and [roadmap](./docs/roadmap.md) for the current direction.

## Documentation policy

English Markdown files are the source of truth. Every Markdown document has a synchronized Korean copy whose filename ends in `(kor).md`. Code, identifiers, paths, configuration keys, and normative syntax remain unchanged in translations.

## License

greedyQ is distributed under the [MIT License](./LICENSE).
