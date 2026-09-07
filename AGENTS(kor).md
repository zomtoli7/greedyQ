# 저장소 작업 지침

[English](./AGENTS.md)

## 커뮤니케이션

- 프로젝트 소유자와 대화할 때 한국어를 기본 언어로 사용합니다.
- 기술적 정확성을 높이거나 확립된 용어를 유지하는 데 도움이 될 때 영어를 사용합니다.

## 문서

- 모든 Markdown 문서는 영문판을 source of truth로 작성합니다.
- 같은 위치에 `.md` 바로 앞에 `(kor)`를 붙인 동기화된 한국어 사본을 생성합니다.
- 예: `docs/example.md`와 `docs/example(kor).md`
- 각 문서 쌍의 제목, 구조, 예제, 링크, 스펙 버전, 주요 내용을 일치시킵니다.
- 코드, 식별자, 파일 경로, 설정 키, 규범적 문법은 번역하지 않습니다.
- 각 문서 상단에서 상대 언어판으로 연결합니다.
- 문서를 변경할 때 두 언어판을 같은 변경에서 함께 갱신합니다.

## 제품 방향

- `docs/product-brief.md`를 현재 제품 방향의 기준으로 사용합니다.
- `docs/greedyq-v0.1-spec.md`를 현재 normative-format draft로, `examples/complete-study/`를 pre-implementation golden reference로 사용합니다.
- `docs/roadmap.md`를 현재 구현 순서의 기준으로 사용합니다.
- AI-guided study creation 및 deployment를 주요 사용자 경험으로 취급합니다.
- QMD 직접 작성을 expert path로, PPTX conversion을 import path로 취급합니다.
- 선택한 LLM이 연구 reasoning을 제공하게 하고 interview workflow, approval checkpoint, artifact contract, validation, reproducibility는 greedyQ에서 결정론적으로 유지합니다.
- 중요한 연구 결정에는 연구자의 명시적 확인을 요구합니다.
- Preregistration을 핵심 generated artifact 및 pre-fielding gate로 다루며 unresolved commitment를 지어내거나 명시적 승인과 검증 없이 registry에 제출하지 않습니다.
- Chat mode와 agent mode를 구분하고 연결된 도구와 검증 결과 없이 외부 서비스를 설정했다고 주장하지 않습니다.
- 런타임 구현보다 스펙 작업을 우선합니다.
- surveydown 내부 구현을 복제하지 않고 공개된 사용자 대상 문법과의 호환을 목표로 합니다.
- surveydown 소스 코드, test, 복사한 fixture를 포함하지 않으며 공개 문서와 관찰 가능한 동작을 바탕으로 구현과 conformance fixture를 독립 작성합니다.
- Vercel/Supabase web-native runtime을 우선하면서 `app.R`을 포함한 native surveydown 프로젝트 생성을 핵심 출력으로 다룹니다.
- Export 동작을 directly portable, generated, greedyQ-only, unsupported로 분류하고 중요한 불일치를 모두 보고합니다.
- 설문 정의에서 임의의 R 또는 JavaScript를 실행하지 않습니다.
- 연구자가 응답 데이터의 소유권과 통제권을 유지하도록 합니다.
- 제품 방향이 명시적으로 변경되지 않는 한 GUI 설문 빌더를 도입하지 않습니다.

## 엔지니어링

- 결정론적이고 정적으로 검증 가능한 형식과 동작을 우선합니다.
- 규범적 스펙과 생성 결과물에 버전을 부여합니다.
- 문서화된 문법과 동작에 conformance test를 추가합니다.
- R, RStudio, Quarto, Shiny 없이 핵심 workflow를 사용할 수 있도록 유지합니다.
