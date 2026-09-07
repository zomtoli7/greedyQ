# greedyQualt

[한국어](./README(kor).md)

> Surveydown-compatible survey-as-code, without R, RStudio, Quarto, or Shiny.

greedyQualt is an open-source, Markdown-first survey and experimental research engine. Researchers define studies in version-controlled text files, deploy survey applications through Vercel, and store responses in a Supabase project they own.

The project is intended for reproducible academic research, particularly studies that require branching, persistent random assignment, factorial experiments, or conjoint/CBC designs.

## Why greedyQualt?

Commercial survey platforms can be expensive, difficult to reproduce, and restrictive for complex experimental designs. Surveydown offers a strong survey-as-code model, but its R, Quarto, and Shiny toolchain can be a barrier for researchers.

greedyQualt keeps the good parts:

- Human-readable survey definitions
- Git-based version control and reproducibility
- Researcher-owned PostgreSQL data
- Programmable research workflows

It replaces the required R/Shiny runtime with a web-native TypeScript and React stack designed for GitHub, Vercel, and Supabase.

## Product principles

- `survey.qmd` is the source of truth for survey content and questions.
- The user-facing QMD syntax should be compatible with surveydown wherever practical.
- Arbitrary R and Shiny code is not executed.
- Conditional logic and randomization are declarative, safe, and reproducible.
- Researchers own and control their respondent data.
- No GUI survey builder is required.
- The specification must be readable by people and reliably usable by general-purpose language models.

## Intended workflow

```text
survey.qmd + greedyqualt.yml + design/*.csv
                       |
                       v
        parser -> Survey AST -> validator
                       |
                       v
             React/Next.js renderer
                       |
                       v
                    Vercel
                       |
                       v
         Researcher's own Supabase
```

The target onboarding experience is:

1. Fork a greedyQualt template.
2. Edit `survey.qmd` directly or generate it with an LLM.
3. Create a Supabase project.
4. Deploy the repository to Vercel.
5. Enter the Supabase environment variables.
6. Publish the survey.

## Authoring paths

greedyQualt is planned to support three authoring paths:

1. Direct authoring in `survey.qmd` and `greedyqualt.yml`.
2. Conversion of a PowerPoint survey draft into QMD, configuration, and extracted assets.
3. Generation of valid project files by GPT, Claude, or another LLM using a versioned Markdown authoring vignette.

## Project status

greedyQualt is in the specification phase. The first milestone is to document surveydown's public user-facing specification and define the greedyQualt v0.1 compatibility boundary before implementing the runtime.

See the [product brief](./docs/product-brief.md), [surveydown compatibility research](./docs/surveydown-compatibility.md), and [roadmap](./docs/roadmap.md) for the current direction.

## Documentation policy

English Markdown files are the source of truth. Every Markdown document has a synchronized Korean copy whose filename ends in `(kor).md`. Code, identifiers, paths, configuration keys, and normative syntax remain unchanged in translations.

## License

The open-source license has not yet been selected. MIT and Apache-2.0 are under consideration.
