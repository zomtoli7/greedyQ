# 호환성 검증 — 2026-09-10

[English](./compatibility-verification-2026-09-10.md)

로컬 작업본 검증 기록입니다. 공개 릴리스나 실제 외부 서비스 인증을 뜻하지 않습니다.

## 확인한 변경

- Surveydown 문서에 따른 선택지·행렬 행 셔플: 지정 위치, 고정 항목, 저장된 순서 유지. 문항 순서와 제한된 독립 페이지 순서는 별도의 greedyQ 확장입니다.
- 브라우저 답변 자동 저장, 새로고침·이전 이동, 조건부 표시·페이지 건너뛰기, 진행 차단 검사, 안전한 인라인 서식.
- 종료 화면의 HTTPS 반환과 명시적 파라미터 연결. 미리보기에서는 외부로 이동하지 않으며, 연결된 설문도 저장에 실패하면 반환하지 않습니다.
- 서버가 저장된 표시 순서의 변경 요청을 거부합니다. 가상 PostgreSQL 검사는 연구자 계정이 아닌 임시 로컬 데이터베이스를 사용합니다.
- OSF 공식 템플릿의 메타데이터 포함 29개 항목. 영문·한국어 초안은 미정 결정을 보존하며 OSF 로그인·제출을 하지 않습니다.
- 초안 업그레이드는 별도 사본을 만들고 원본을 보존하며 알려진 배포 비밀정보를 제외하고 기준 런타임을 다시 생성합니다. 운영 중인 설문은 별도 검토가 필요합니다.

## 검증 근거

Python 전체 155개 테스트와 JavaScript·계정 여정·브라우저 26개 테스트가 통과했습니다. 후자는 실패·건너뛰기가 없습니다. 실제 Chrome에서 390px·1280px 화면, 순서 유지, 답변 복원, 외부 반환 안전성을 검사했습니다. 기준 예제 세 개를 재생성·export했고 두 연구의 사전 검사를 통과했습니다. 공백 오류 검사도 통과했습니다.

실행 명령: `python3 -m unittest discover -s tests -q`; `node --test tests/cloud_lifecycle.cjs tests/randomization_browser.cjs tests/ordering_browser.cjs`; `python3 -m greedyq preflight <study>`; `git diff --check`.

## 남은 제한

[기능별 점검표](./surveydown-compatibility-audit(kor).md)를 확인하세요. 일부 설정, 자유로운 R/Shiny 반응형 기능, 행렬 전체 응답 여부 판정은 미완성 또는 비동등합니다. Native R export는 대상 환경 실행으로 인증하지 않았습니다. 로컬 검사 통과가 Surveydown 전체 호환성을 뜻하지 않습니다.

Vercel/Supabase 변경·배포, Prolific 설정, OSF 제출, Google Sites 공개, DNS 변경은 하지 않았습니다. Migration 004와 대응 모델·런타임은 승인 후 적용해야 합니다. [Google Sites 계획서](./google-sites-plan(kor).md)에 다음 단계에서 필요한 편집 접근과 도메인 정보를 정리했습니다. 존재하지 않는 커밋으로 릴리스 번호를 올리지 않았습니다.
