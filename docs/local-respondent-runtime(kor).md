# 로컬 Respondent Runtime

[English](./local-respondent-runtime.md)

로컬 runtime은 연구를 Supabase 및 Vercel에 연결하기 전에 필요한 respondent 동작을 시험합니다. Server-rendered page, HttpOnly session cookie, 로컬 SQLite database를 사용합니다.

```bash
python3 -m greedyq run examples/complete-study
```

`http://localhost:4180/study`를 엽니다. 새로운 browser cookie마다 anonymous test session이 생성됩니다. 성공적인 page transition에서 응답을 저장하며 새로고침하거나 page를 다시 열면 현재 session을 이어갑니다.

구현된 test 동작:

- Research answer보다 먼저 consent 수락 또는 거부 기록
- Server의 required question 및 numeric limit 검사
- 새로고침 이후 partial response 및 current page 유지
- Atomic simple/fixed-block condition 배정 및 condition 고정
- Screening, completion, refusal, withdrawal terminal state
- 하나의 transaction에서 deletion-on-withdrawal 응답 및 배정 삭제
- Browser에서 조건부 문항 즉시 갱신 후 server에서 재검사
- Browser가 experimental condition이나 next page를 선택하지 못하도록 제한

Test data는 기본적으로 `STUDY_DIR/.greedyq/runtime.sqlite3`에 저장되며 Git에서 제외됩니다. 다른 local database는 `--database PATH`, 다른 port는 `--port PORT`를 사용합니다.

이 기능은 production runtime이 아닙니다. Localhost에만 연결되며 Supabase authentication/RLS, Vercel deployment, external respondent identifier, production redirect, secret encryption, operational monitoring, analysis export를 구현하지 않습니다. 실제 participant를 모집하는 데 사용하면 안 됩니다.
