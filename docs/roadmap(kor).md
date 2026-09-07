# greedyQualt 로드맵

[English](./roadmap.md)

**상태:** 초안

**계획 원칙:** 구현보다 스펙 우선

## Phase 0: 프로젝트 기반

- [x] 초기 제품 방향 수립
- [x] 영문 문서를 source of truth로 지정
- [x] 모든 Markdown 문서에 동기화된 `(kor).md` 사본 요구
- [x] 초기 README, 제품 개요, 로드맵 생성
- [ ] 오픈소스 라이선스 선택
- [ ] 로컬 Git 저장소 초기화
- [ ] GitHub 저장소 생성 및 연결

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
- [ ] 대표 공식 예제를 conformance fixture로 수집

결과물:

```text
docs/surveydown-compatibility.md
docs/surveydown-compatibility(kor).md
```

## Phase 2: greedyQualt v0.1 스펙

- [ ] 지원할 QMD grammar 정의
- [ ] 제한된 `sd_*()` expression grammar 정의
- [ ] Survey AST / JSON schema 정의
- [ ] `greedyqualt.yml`과 expression language 정의
- [ ] Navigation, validation, lifecycle semantics 정의
- [ ] Randomization semantics와 저장 metadata 정의
- [ ] Persistence 및 session 동작 정의
- [ ] Supabase schema 정의
- [ ] 안정적인 validator diagnostic code 정의
- [ ] 모든 surveydown 기능을 supported, partial, unsupported, deferred로 분류

결과물:

```text
docs/greedyqualt-v0.1-spec.md
docs/greedyqualt-v0.1-spec(kor).md
```

## Phase 3: Architecture 및 배포 skeleton

- [ ] Parser library 선택 및 grammar 구현 접근법 확정
- [ ] TypeScript parser 및 정규화 AST package 생성
- [ ] Validator와 diagnostic format 생성
- [ ] React/Next.js renderer skeleton 생성
- [ ] Supabase migration 및 access policy 생성
- [ ] Vercel 배포 template 생성
- [ ] 로컬 validation 및 preview 명령 구현
- [ ] 문서화된 conformance fixture 자동 테스트 추가

## Phase 4: End-to-end MVP

가장 작은 완전한 설문 경로를 구현합니다.

- [ ] Markdown 페이지 및 기본 navigation render
- [ ] Text, textarea, numeric, single-choice, multiple-choice 문항 구현
- [ ] Required field와 기본 validation 구현
- [ ] 익명 respondent session 생성
- [ ] 부분 진행 상태 및 완료 응답 저장
- [ ] 단순 및 block random assignment 구현
- [ ] 재개된 session 전반에 배정 metadata 유지
- [ ] 분석 가능한 데이터 export
- [ ] 완전한 예제 연구를 Vercel과 Supabase에 배포

## Phase 5: 호환성 확장

- [ ] Select, slider, date, Likert, matrix 문항 구현
- [ ] 지원되는 surveydown 설정 구현
- [ ] 선언형 show, skip, stop, validation rule 구현
- [ ] Option, item, page, task-order shuffle 구현
- [ ] 지원되지 않는 `app.R` 코드에 대한 migration diagnostics 개선
- [ ] Compatibility matrix regression test 추가

## Phase 6: 연구 특화 기능

- [ ] Weighted 및 stratified randomization
- [ ] Factorial experiment 정의
- [ ] 재현 가능한 seeded assignment
- [ ] Attention check
- [ ] Timer 및 page dwell time
- [ ] Response revision history
- [ ] Prolific participant 및 completion-code 지원
- [ ] Conjoint/CBC render 및 데이터 수집
- [ ] 외부 CSV experimental design
- [ ] 다국어 설문

## Phase 7: LLM authoring vignette

범용 언어 모델이 연구를 신뢰성 있게 작성할 수 있도록 스펙과 validation surface를 설계합니다.

- [ ] 버전이 명시된 전체 authoring vignette 공개
- [ ] 토큰 효율적인 compact vignette 공개
- [ ] 완전한 reference study 제공
- [ ] LLM 출력 파일 계약 및 generation notes 정의
- [ ] 필수 pre-output self-check 추가
- [ ] `greedyqualt validate --format llm` 구현
- [ ] GPT와 Claude로 생성 및 수정 workflow 테스트
- [ ] 일반적인 자연어 연구 요청에 대한 conformance test 추가

결과물:

```text
docs/llm-authoring-vignette.md
docs/llm-authoring-vignette(kor).md
docs/llm-authoring-vignette-compact.md
docs/llm-authoring-vignette-compact(kor).md
examples/complete-study/
```

## Phase 8: PPTX converter

- [ ] PPTX에서 text, table, image, speaker notes 추출
- [ ] Slide layout에서 페이지와 일반 문항 구조 추론
- [ ] 결정론적 변환을 위한 optional authoring metadata 지원
- [ ] `survey.qmd`, `greedyqualt.yml`, asset 생성
- [ ] Confidence와 warning이 포함된 conversion report 생성
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

## 바로 다음 작업

1. v0.1 호환 대상을 위한 executable conformance fixture 수집
2. 조사 결과를 규범적 greedyQualt v0.1 스펙으로 전환
3. 제한된 QMD/R-expression grammar와 정규화 Survey AST 정의
4. Persistence, randomization, privacy, validation semantics 정의
