# Citing greedyQ

[한국어](./CITATION(kor).md)

Until a peer-reviewed greedyQ paper is available, any publication, preprint, thesis, report, or other scholarly output that uses greedyQ should cite both:

1. the greedyQ GitHub repository, including the exact greedyQ release identifier used to create the study; and
2. the surveydown paper, in recognition of the prior survey-as-code work and `survey.qmd` authoring conventions on which greedyQ builds.

This dual-citation policy applies even when a study uses only the independent greedyQ browser runtime and does not execute the surveydown R package. Describe the software actually used accurately; do not state that surveydown executed the survey unless it did.

## Recommended greedyQ citation

Replace `<release identifier>` with the value stored in `greedyq.version` in the study's `survey.qmd`.

> greedyQ project. (2026). *greedyQ: A specification-driven, AI-native application for online academic research* (Version <release identifier>) [Computer software]. GitHub. https://github.com/zomtoli7/greedyQ

BibTeX:

```bibtex
@software{greedyq,
  author  = {{greedyQ project}},
  title   = {greedyQ: A Specification-Driven, AI-Native Application for Online Academic Research},
  year    = {2026},
  version = {<release identifier>},
  url     = {https://github.com/zomtoli7/greedyQ}
}
```

## Required companion citation

> Hu, P., Bunea, B., & Helveston, J. (2025). surveydown: An open-source, markdown-based platform for programmable and reproducible surveys. *PLOS ONE, 20*(8), e0331002. https://doi.org/10.1371/journal.pone.0331002

```bibtex
@article{hu2025surveydown,
  title   = {surveydown: An open-source, markdown-based platform for programmable and reproducible surveys},
  author  = {Hu, Pingfan and Bunea, Bogdan and Helveston, John Paul},
  journal = {PLOS ONE},
  year    = {2025},
  volume  = {20},
  number  = {8},
  pages   = {e0331002},
  doi     = {10.1371/journal.pone.0331002}
}
```

## Suggested methods wording

> The questionnaire was created and deployed using greedyQ (version <release identifier>), whose survey specification builds on the survey-as-code approach and `survey.qmd` authoring conventions established by surveydown (Hu, Bunea, & Helveston, 2025).

If the generated native surveydown project was actually used, say so explicitly and report the surveydown package version as well.
