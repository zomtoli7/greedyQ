# 브라우저 프리뷰

[English](./browser-preview.md)

v0.2 reference pipeline은 연구 source file을 안전한 self-contained 브라우저 preview로 변환합니다.

```text
survey.qmd + greedyq.yml
            ↓
       QMD/YAML parser
            ↓
 normalized-survey.json
            ↓
         validator
            ↓
 preview-model.json + preview.html
```

## 프리뷰 시작

greedyQ repository root에서 실행합니다.

```bash
python3 -m greedyq preview examples/complete-study
```

명령은 연구를 먼저 검사하고 다시 생성한 후 `http://localhost:4173/preview.html`에서 제공합니다. Control-C로 서버를 종료합니다. 기본 port가 사용 중이면 `--port 4174`, 브라우저를 자동으로 열지 않으려면 `--no-open`을 사용합니다.

## 확인할 내용

Respondent처럼 설문을 완료한 후 researcher control을 사용해 다음을 시험합니다.

- 모든 실험 조건
- Consent 거부와 screening 경로
- 필수 문항 메시지와 숫자 범위
- 조건부 문항과 숨겨진 응답 삭제
- Previous navigation과 로컬 preview 상태 저장
- 완료, 철회, technical-error 종료 화면
- Debug panel의 표시 label과 저장 value
- 좁은 화면과 모바일 너비

Preview는 Content Security Policy를 통해 network connection, form submission, production redirect를 의도적으로 차단합니다. 응답은 preview resume 시험을 위해 브라우저 `localStorage`에만 남으며 Reset으로 삭제할 수 있습니다.

## 명령

```bash
# 검사만 하고 생성 파일은 쓰지 않음
python3 -m greedyq validate PATH_TO_STUDY

# 검사하고 preview 파일 생성
python3 -m greedyq build PATH_TO_STUDY

# 검사, 생성, 서버 실행, 브라우저 열기
python3 -m greedyq preview PATH_TO_STUDY
```

성공하면 `preview-model.json`, `preview.html`, `.greedyq/normalized-survey.json`, `.greedyq/validation-report.runtime.json`을 생성합니다. Source of truth는 계속 `survey.qmd`와 `greedyq.yml`이며 생성된 preview 파일을 직접 수정하면 안 됩니다.

## 현재 경계

이 기능은 researcher preview이며 production respondent runtime이 아닙니다. Server session 생성, Supabase 저장, concurrency-safe randomization, Prolific participant 검증, completion redirect, 실제 응답 수집은 수행하지 않습니다. Preview가 통과해도 이러한 operation은 계속 차단됩니다.
