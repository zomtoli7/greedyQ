# greedyQ 연구 Framing

[English](./research-framing.md)

**상태:** 향후 white paper를 위한 작업 중인 conceptual framing

## 제안 제목

**greedyQ: A Specification-Driven AI-Native Application for Online Academic Research**

제안 부제:

**Turning General-Purpose Generative AI into a Reproducible Research Agent**

## 중심 정의

> greedyQ is a specification-driven, AI-native application for online academic research.

> Rather than implementing the application itself in conventional source code, greedyQ specifies how a general-purpose generative AI agent should instantiate and operate the application.

Portable greedyQ Markdown, schema, checkpoint, template, conformance fixture가 함께 **agent-executable application specification**을 구성합니다.

“AI-native application”이라는 용어 자체를 greedyQ만의 고유 개념으로 제시하지 않습니다. 제안하는 기여는 더 구체적인 architecture입니다. Application behavior의 상당 부분을 portable normative specification으로 배포하여 capable general-purpose GenAI가 이를 실행하게 하고, 동시에 deterministic artifact와 conformance test에 책임지게 합니다.

## Architecture 구분

```text
greedyQ
agent-executable application specification
                    |
                    v
       general-purpose host GenAI
         (GPT / Claude / Gemini / ...)
                    |
                    v
        instantiated greedyQ research agent
                    |
                    v
                researcher
                    |
                    v
       research-design artifacts
                    +
       executable survey application
```

greedyQ 자체는 agent가 아닙니다. 관계는 다음과 같습니다.

```text
greedyQ specification + host GenAI = greedyQ research agent
```

Research agent는 instantiate된 application process입니다. 질문하고, 연구 reasoning을 적용하고, 승인을 기록하고, artifact를 만듭니다. Respondent-facing survey는 이 process가 생성하는 별도의 software입니다.

## 세 층의 positioning

### Architecture

**Specification-driven AI-native application.** 실행 가능한 application behavior를 conventional source-code implementation만으로 완결하지 않고 agent-executable specification으로 정의하고 배포합니다.

### Domain

**Online academic research.** Research question, study design, measurement, consent, governance, experiment, randomization, respondent collector, data plan, preregistration, survey execution, fielding을 포함합니다.

### Implementation

**greedyQ.** 이 architecture를 재현 가능한 online academic research에 적용한 concrete application입니다.

## 중심 연구 질문

> Can a research methodology and workflow be packaged into a portable specification that turns an arbitrary capable general-purpose AI into a domain-specific research application?

이 질문은 특정 chatbot이 유용한 collaborator가 될 수 있는지를 넘어섭니다. Normative application specification이 서로 다른 host model에서도 충분히 일관되고 감사 가능하며 유용한 application behavior를 만들 수 있는지를 묻습니다.

## Portability 및 conformance 가설

greedyQ의 identity는 특정 model vendor나 interface가 아니라 normative specification에 고정되므로, 서로 다른 capable host model이 instantiate해도 greedyQ로 남습니다. 표면적인 interaction은 달라도 필수 결정, 금지된 추측, artifact contract, deterministic validation은 invariant해야 합니다.

향후 validation study에서는 같은 tagged greedyQ specification과 study brief를 GPT, Claude, Gemini 등의 capable system에 독립적으로 제공한 뒤 다음을 평가할 수 있습니다.

- Profile 및 module 선택
- 질문 순서와 decision escalation
- 연구자 authority 보존
- 최종 artifact validity와 semantic equivalence
- 미결정 정보 처리
- 검증되지 않은 외부 작업을 완료했다고 주장하지 않는지
- Participant-flow equivalence
- 반복 실행 간 reproducibility
- Host-specific interface 차이
- Deterministic validator가 탐지할 수 있는 conformance failure

목표는 byte-for-byte로 동일한 prose나 UI가 아닙니다. 중요한 invariant는 연구 결정, 참여자 권리, 연구 semantics, stored value, lifecycle behavior, 선언된 output contract입니다.

## 주장 범위

Specification이 conventional code를 없애는 것은 아닙니다. 정확한 preview, runtime, database, validation, export template에는 code가 들어갈 수 있습니다. Architecture claim은 application의 domain workflow, decision logic, normative behavior, artifact-generation contract를 주로 agent-executable specification으로 정의하고 배포한다는 것입니다. Model 간 equivalence, reliability, superiority를 주장하기 전에는 empirical validation이 필요합니다.
