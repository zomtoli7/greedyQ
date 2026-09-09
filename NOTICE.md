# Notices and Attribution

[한국어](./NOTICE(kor).md)

## greedyQ

greedyQ is an independent open-source project distributed under the MIT License. See [`LICENSE`](./LICENSE).

## Relationship to surveydown

greedyQ independently implements compatibility with a documented subset of surveydown-style `survey.qmd` authoring conventions. It does not incorporate or redistribute surveydown source code. Its parser, AST, validator, web-native runtime, deployment integration, export generator, templates, and conformance fixtures are intended to be independently authored.

Surveydown is prior open-source work distributed under the MIT License:

- Project: [surveydown-dev/surveydown](https://github.com/surveydown-dev/surveydown)
- License: [surveydown MIT License](https://github.com/surveydown-dev/surveydown/blob/main/LICENSE.md)

For scholarly use, greedyQ asks researchers to cite both the greedyQ GitHub repository and the surveydown PLOS ONE paper, including when the independent greedyQ runtime is used without executing surveydown. This academic citation policy is separate from software-license compliance. See [CITATION.md](./CITATION.md).
- Copyright (c) 2025 John Paul Helveston, Pingfan Hu, Bogdan Bunea

greedyQ is not affiliated with, endorsed by, sponsored by, or maintained by the surveydown project or its maintainers. References to surveydown describe compatibility, provenance, or an export target; they do not imply an official relationship.

## Compatibility claims

Compatibility claims apply only to the feature and version boundaries documented by greedyQ. A feature may be directly portable, generated into native surveydown files, available only in the greedyQ runtime, or unsupported. Native export must report any behavior that cannot be preserved faithfully.
