# 고지 및 출처 표시

[English](./NOTICE.md)

## greedyQ

greedyQ는 MIT License로 배포되는 독립 오픈소스 프로젝트입니다. [`LICENSE`](./LICENSE)를 참고하십시오.

## surveydown과의 관계

greedyQ는 문서화된 surveydown-style `survey.qmd` 작성 관례의 일부와 호환되도록 독립 구현합니다. surveydown 소스 코드를 포함하거나 재배포하지 않습니다. Parser, AST, validator, web-native runtime, deployment integration, export generator, template, conformance fixture는 독립적으로 작성하는 것을 원칙으로 합니다.

Surveydown은 MIT License로 배포되는 선행 오픈소스 작업입니다.

- 프로젝트: [surveydown-dev/surveydown](https://github.com/surveydown-dev/surveydown)
- 라이선스: [surveydown MIT License](https://github.com/surveydown-dev/surveydown/blob/main/LICENSE.md)
- Copyright (c) 2025 John Paul Helveston, Pingfan Hu, Bogdan Bunea

greedyQ는 surveydown 프로젝트 또는 maintainer와 제휴하지 않으며, 이들의 보증·후원·유지 관리를 받지 않습니다. Surveydown에 대한 언급은 호환성, 출처 또는 export 대상을 설명할 뿐 공식적인 관계를 의미하지 않습니다.

## 호환성 표기의 범위

호환성 표기는 greedyQ가 문서화한 기능 및 버전 경계에만 적용됩니다. 기능은 directly portable, native surveydown 파일로 generated, greedyQ runtime에서만 사용 가능, 또는 unsupported일 수 있습니다. Native export는 동작을 충실하게 보존할 수 없는 경우 이를 반드시 보고해야 합니다.
