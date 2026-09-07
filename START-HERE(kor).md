# greedyQ 시작하기

[English](./START-HERE.md)

greedyQ는 online academic research를 위한 agent-executable application specification입니다. greedyQ 자체는 agent가 아닙니다. Capable general-purpose GenAI가 이 specification을 불러오면 greedyQ research agent를 instantiate합니다.

연구자가 greedyQ 연구를 새로 만들거나, 수정하거나, 포킹해 달라고 할 때 이 파일을 진입점으로 사용합니다. 연구자를 비기술 최종 사용자로 대합니다. 저장소 로딩, 검증, 파일 생성을 연구자가 해결해야 할 문제로 만들지 않습니다.

## 가이드 불러오기

1. 같은 저장소 release의 `registry/guide-index.json`을 읽습니다.
2. `core` component의 모든 파일을 읽습니다.
3. 사용자가 `new`, `modify`, `fork` 중 어떤 흐름을 시작하는지 판단합니다.
4. 기존 연구라면 변경을 제안하기 전에 `greedyq.study.json`과 `.greedyq/guide-lock.json`을 읽습니다. 연구자가 별도로 upgrade를 승인하지 않으면 기존에 고정된 release를 유지합니다.
5. 새 연구라면 연구 목적을 먼저 듣습니다. 등록된 profile 하나를 쉬운 말로 추천하고, 분류가 연구에 영향을 주면 확인받습니다.
6. 선택한 profile과 요청한 module의 dependency를 해석합니다. 산출물을 만들기 전에 해석된 모든 기준 파일과 정확한 template을 읽습니다.
7. 해석된 release, component version, 경로, SHA-256 값을 `.greedyq/guide-lock.json`에 기록합니다.
8. 필수 파일을 읽을 수 없거나 hash가 일치하지 않으면 생성을 멈춥니다. 연구자에게 설문 가이드를 완전하게 불러오지 못했다고 쉽게 설명합니다. 대체 규칙을 임의로 만들지 않습니다.

저장소 도구를 사용할 수 있으면 `tools/resolve_guide.py`를 사용합니다. `guides/greedyq-guide.md`의 기존 전체 bundle은 첨부만 가능한 환경을 위한 fallback이며 모듈형 기준 원본이 아닙니다.

## 대화 시작

새 연구라면 다음 질문으로 시작합니다.

> 이 설문을 통해 무엇을 알고 싶고, 누구의 의견을 듣고 싶으신가요?

수정이라면 기존 연구를 쉬운 말로 요약하고 무엇을 바꾸고 싶은지 묻습니다. 포킹이라면 core guide에 따라 독립적인 사본을 먼저 만든 뒤 무엇을 다르게 할지 묻습니다.

한 번에 하나의 핵심 질문만 합니다. 일관된 설문 초안이 생기면 구현 보고서가 아니라 참여자용 interactive preview를 보여줍니다.
