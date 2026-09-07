# greedyQ 로드맵

[English](./roadmap.md)

**상태:** 초안

**계획 원칙:** 구현보다 스펙 우선

## Phase 0: 프로젝트 기반

- [x] 초기 제품 방향 수립
- [x] 영문 문서를 source of truth로 지정
- [x] 모든 Markdown 문서에 동기화된 `(kor).md` 사본 요구
- [x] 초기 README, 제품 개요, 로드맵 생성
- [x] greedyQ에 MIT License 선택
- [x] 로컬 Git 저장소 초기화
- [x] GitHub 저장소 생성 및 연결

## Phase 1: Surveydown 스펙 조사

Primary source와 실행 가능한 예제로 현재 surveydown의 공개된 사용자 대상 동작을 조사합니다.

- [x] 프로젝트 및 파일 구조 목록화
- [x] QMD front matter와 페이지 grammar 문서화
- [x] 모든 공개 문항 타입과 인수 목록화
- [x] Navigation과 설문 lifecycle 동작 문서화
- [x] Theme 및 survey settings 문서화
- [x] Required, validation, shuffle, metadata 동작 분석
- [x] `app.R` logic의 show, skip, stop, reactive 동작 분석
- [x] Randomization과 stored-value 동작 분석
- [x] Session persistence와 PostgreSQL/Supabase 동작 분석
- [ ] 문서화된 공개 동작을 바탕으로 독립 작성한 conformance fixture 생성
- [x] 독립 구현을 위한 소스 코드 비사용 정책 확립

결과물:

```text
docs/surveydown-compatibility.md
docs/surveydown-compatibility(kor).md
```

## Phase 2: greedyQ v0.1 스펙

- [ ] 지원할 QMD grammar 정의
- [ ] 제한된 `sd_*()` expression grammar 정의
- [ ] Survey AST / JSON schema 정의
- [ ] `greedyq.yml`과 expression language 정의
- [ ] Navigation, validation, lifecycle semantics 정의
- [ ] Randomization semantics와 저장 metadata 정의
- [ ] Persistence 및 session 동작 정의
- [ ] Supabase schema 정의
- [ ] Compliance를 주장하지 않는 ethics/IRB metadata 정의
- [ ] Versioned consent, refusal, amendment, withdrawal semantics 정의
- [ ] Generic external-respondent contract 및 Prolific preset 정의
- [ ] 안정적인 validator diagnostic code 정의
- [ ] 모든 기능을 directly portable, native surveydown으로 generated, greedyQ-only, unsupported로 분류
- [ ] `survey.qmd`, 생성된 `app.R`, 보조 파일, 호환성 보고서에 대한 native surveydown export contract 정의

결과물:

```text
docs/greedyq-v0.1-spec.md
docs/greedyq-v0.1-spec(kor).md
```

## Phase 3: AI-guided workflow 스펙

런타임 구현 전에 주요 제품 경험을 정의합니다.

- [ ] Capability detection 및 Chat/Agent mode 선택 정의
- [ ] Phase별 one-question-at-a-time interview protocol 정의
- [ ] Study-state, assumption, unresolved-decision, decision-log format 정의
- [ ] LLM의 research review 시점과 연구자 확인 필수 시점 정의
- [ ] Artifact update checkpoint 및 재개 가능한 conversation handoff 정의
- [ ] IRB/ethics, consent, respondent-source, privacy, deployment interview 단계 정의
- [ ] LLM output-file contract 및 generation notes 정의
- [ ] Validation/correction loop 및 안정적인 LLM-facing diagnostic 정의
- [ ] Preview 전 및 deployment 전 approval gate 정의
- [ ] 외부 operation의 정직한 완료 및 검증 요구사항 정의
- [ ] 완전한 reference study와 full/compact versioned guide 공개
- [ ] 여러 유능한 LLM로 guided creation 및 correction workflow 테스트

결과물:

```text
guides/greedyq-guide.md
guides/greedyq-guide(kor).md
guides/greedyq-guide-compact.md
guides/greedyq-guide-compact(kor).md
examples/complete-study/
```

## Phase 4: Architecture 및 배포 skeleton

- [ ] Parser library 선택 및 grammar 구현 접근법 확정
- [ ] TypeScript parser 및 정규화 AST package 생성
- [ ] Validator 및 LLM-friendly diagnostic format 생성
- [ ] Native surveydown exporter 및 결정론적 `app.R` generator 생성
- [ ] React/Next.js renderer skeleton 생성
- [ ] Supabase migration 및 access policy 생성
- [ ] Vercel 배포 template 생성
- [ ] 로컬 validation 및 preview 명령 구현
- [ ] 독립 작성한 conformance fixture 및 native export snapshot 자동 테스트 추가

## Phase 5: AI-guided end-to-end MVP

가장 작은 완전한 대화형 연구 경로를 구현합니다.

- [ ] Versioned guide와 자연어 연구 요청으로 시작
- [ ] 재개 가능한 one-question-at-a-time interview 수행
- [ ] 중요한 연구 결정을 기록하고 승인 획득
- [ ] 유효한 study, consent, respondent-source, deployment artifact 생성
- [ ] 동일한 검증된 study에서 native surveydown 프로젝트와 명시적 호환성 보고서 생성
- [ ] Markdown 페이지 및 기본 navigation render
- [ ] Text, textarea, numeric, single-choice, multiple-choice 문항 구현
- [ ] Required field와 기본 validation 구현
- [ ] 익명 respondent session 생성
- [ ] 부분 진행 상태 및 완료 응답 저장
- [ ] 단순 및 block random assignment 구현
- [ ] 재개된 session 전반에 배정 metadata 유지
- [ ] Chat-mode deployment handoff 및 Agent-mode verified deployment 지원
- [ ] 분석 가능한 데이터 export
- [ ] 완전한 예제 연구를 Vercel과 Supabase에 배포하고 검증

## Phase 6: 호환성 확장

- [ ] Select, slider, date, Likert, matrix 문항 구현
- [ ] 지원되는 surveydown 설정 구현
- [ ] 선언형 show, skip, stop, validation rule 구현
- [ ] Option, item, page, task-order shuffle 구현
- [ ] 지원되지 않는 `app.R` 코드에 대한 migration diagnostics 개선
- [ ] Compatibility matrix regression test 추가

## Phase 7: 연구 특화 기능

- [ ] Weighted 및 stratified randomization
- [ ] Factorial experiment 정의
- [ ] 재현 가능한 seeded assignment
- [ ] Attention check
- [ ] Timer 및 page dwell time
- [ ] Response revision history
- [ ] Prolific participant 및 completion-code 지원
- [ ] 구조화된 ethics/IRB metadata 및 재사용 가능한 information block
- [ ] Document version, hash, timestamp를 포함한 first-class consent
- [ ] Generic respondent-collector integration contract
- [ ] Completion 및 screen-out route를 포함한 Prolific preset
- [ ] Duplicate-participation 및 external-ID validation policy
- [ ] Conjoint/CBC render 및 데이터 수집
- [ ] 외부 CSV experimental design
- [ ] 다국어 설문

## Phase 8: PPTX import path

- [ ] PPTX에서 text, table, image, speaker notes 추출
- [ ] Slide layout에서 페이지와 일반 문항 구조 추론
- [ ] 결정론적 변환을 위한 optional authoring metadata 지원
- [ ] `survey.qmd`, `greedyq.yml`, asset 생성
- [ ] Confidence와 warning이 포함된 conversion report 생성
- [ ] 생성된 artifact를 guided AI review workflow에 전달
- [ ] 생성된 프로젝트 자동 검증

## 모든 단계에 적용되는 요구사항

다음 요구사항은 모든 phase에 적용됩니다.

- 영문/한국어 문서 parity 유지
- 모든 규범 형식과 생성 결과물에 버전 부여
- 결정론적이고 테스트 가능한 동작 우선
- 설문 정의에서 임의의 R 또는 JavaScript를 실행하지 않음
- 연구자의 응답 데이터 소유권 유지
- 배포된 실험을 재현하기에 충분한 metadata 기록
- R, RStudio, Quarto, Shiny 없이 핵심 workflow 사용 가능
- Vercel/Supabase web-native runtime을 주 실행 경로로 유지
- 제한 없는 R, Shiny, Quarto 사용자 정의를 위한 핵심 경로로 native surveydown 프로젝트 생성
- surveydown 소스 코드를 포함하지 않고 공개 문서를 바탕으로 호환성을 독립 구현
- 제휴, 보증, 공동 유지 관리를 암시하지 않으면서 출처 표시
- 주요 경험을 model-agnostic하게 유지하고 여러 유능한 LLM에서 사용할 수 있게 함
- 중요한 결정의 명시적 승인을 통해 연구자 권한 보존
- 외부 설정이나 배포를 실제 수행하고 검증하지 않은 상태에서 성공했다고 주장하지 않음

## 바로 다음 작업

1. 조사 결과를 규범적 greedyQ v0.1 스펙으로 전환
2. Guided interview, study-state, researcher-approval protocol 정의
3. Full/compact versioned greedyQ guide 초안 작성
4. Native surveydown export contract와 `app.R` 생성 규칙 작성
5. 독립적인 executable conformance fixture를 만들고 runtime과 export artifact를 모두 테스트
