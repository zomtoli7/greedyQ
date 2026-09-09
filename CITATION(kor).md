# greedyQ 인용 안내

[English](./CITATION.md)

Peer-reviewed greedyQ 논문이 나오기 전까지 greedyQ를 사용한 논문, preprint, 학위논문, 보고서 및 기타 학술 산출물은 다음 두 자료를 모두 인용해야 합니다.

1. 연구 생성에 사용한 정확한 greedyQ release identifier를 포함한 greedyQ GitHub 저장소
2. greedyQ가 계승한 survey-as-code 작업과 `survey.qmd` 작성 관례의 선행 연구인 surveydown 논문

이 공동 인용 정책은 surveydown R package를 실행하지 않고 독립적인 greedyQ browser runtime만 사용한 연구에도 적용됩니다. 단, 실제 사용한 software는 정확히 설명해야 하며 surveydown으로 설문을 실행하지 않았다면 그렇게 실행했다고 표현하면 안 됩니다.

## 권장 greedyQ 인용

`<release identifier>`를 해당 연구 `survey.qmd`의 `greedyq.version` 값으로 바꾸십시오.

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

## 함께 인용할 surveydown 논문

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

## 권장 연구방법 문구

> The questionnaire was created and deployed using greedyQ (version <release identifier>), whose survey specification builds on the survey-as-code approach and `survey.qmd` authoring conventions established by surveydown (Hu, Bunea, & Helveston, 2025).

생성된 native surveydown project를 실제 사용했다면 그 사실과 surveydown package version도 명시하십시오.
