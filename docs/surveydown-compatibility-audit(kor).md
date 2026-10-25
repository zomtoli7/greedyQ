# Surveydown 호환성 점검

[English](./surveydown-compatibility-audit.md)

2026-09-10 아래 공개 매뉴얼과 대조했습니다. 동작 점검이며 전체 R/Shiny 호환성을 주장하지 않습니다. Surveydown 내부 소스·테스트 예제는 포함하지 않았습니다. “설정을 읽는다”와 “기능이 작동한다”는 다르므로 내보내기 전에 아래 차이를 설명해야 합니다.

## 셔플과 무작위 배정

[공식 설정](https://surveydown.org/docs/survey-settings)의 `all-shuffled`, `shuffled`는 선택지·matrix 행을 섞으며 페이지 순서가 아닙니다. greedyQ는 문항명 또는 1부터 시작하는 위치·범위를 받아 고정 위치와 저장값을 보존합니다. 공통 지원 유형은 mc, mc_buttons, mc_multiple, mc_multiple_buttons, matrix입니다. Matrix 열과 matrix_multiple을 암묵적으로 섞지 않습니다. `question_order`, `page_order`는 별도 greedyQ 확장입니다. 페이지 셔플은 고정 시작·종료 사이 독립적인 연속 묶음 하나, 자동 이동, show/skip 없는 설문에 제한합니다. 동의·배정·조건 페이지는 섞지 않습니다.

표시 순서는 세션별 `question_orders`, `option_orders`, `page_order`에 보존합니다. 이는 표시 계획이지 읽었다는 증거가 아닙니다. Native export는 공식 선택지 셔플 설정을 보존하지만 새로고침 후 순서 유지까지 동등하다고 주장하지 않습니다. Native 문항·페이지 순서 셔플은 명시적으로 미지원입니다.

[공식 무작위화](https://surveydown.org/docs/randomization)는 서버 실시간 추첨 또는 사전 설계와 추첨값 기록을 설명합니다. greedyQ는 서버 기록 시점이 정해진 자체 가중 단순·고정 블록 참가자 배정을 구현합니다. 임의 R 설계 파일 추첨, 군집·층화·적응 배정, native 고정 블록 동등성은 미구현입니다. [무작위 배정](../RANDOMIZATION(kor).md)을 참고하세요.

## 설정 목록

| 설정 계열 | 브라우저 런타임 상태 | Native export |
| --- | --- | --- |
| 하이픈/밑줄 별칭, YAML yes/no | 읽기 지원, 중복 별칭 거부 | 원본 보존, preview용 네임스페이스 정규화 |
| all-required / required | 실제 문항에 적용 | 보존 |
| show-previous / start-page | 적용, 종료 화면 이전 숨김 | 보존 |
| barcolor | 적용, 현재 6자리 hex 제한 | 보존 |
| theme / barposition / footer 계열 | 기존에 허용하지만 화면 반영 불완전 | Surveydown용 보존 |
| use-cookies | 브라우저 저장소를 사용하며 끄기 동등성 미구현 | 보존 |
| highlight-unanswered | 필수 응답 검사 있음, 선택적 강조 설정 동등성 없음 | 보존 |
| capture-metadata | 자동 브라우저/IP 수집 없음, true 미구현 | native 모집 전 개인정보 검토 |
| mode | respondents.mode·배포 분리 사용, QMD mode 미지원 | 생성물은 preview 강제 |
| auto-scroll | 페이지 전환 시 상단 이동 있음, 문항 진행 스크롤 미지원 | 지원되지 않는 입력을 지어내지 않음 |
| rate-survey | 미지원, 명시적 평가 문항으로 대체 | native 전용 작성 필요 |
| system-language / highlight-color | 미지원 | native 전용 작성 필요 |
| system-messages | previous, next, required 지원, 나머지 미지원 | 지원 원본 키 보존 |

따라서 이 빌드를 “모든 Surveydown 설정 지원”이라고 설명하면 안 됩니다.

## 포맷팅·값·조건 로직

- [포맷팅](https://surveydown.org/docs/question-formatting): 너비, textarea 높이, matrix 문항 열 너비를 처리합니다. 브라우저는 문항·선택지 라벨에서 이스케이프한 굵게·기울임·인라인 코드를 지원하지만 전체 Markdown·임의 HTML과 동등하지 않습니다. 페이지 raw HTML은 거부하며 native export는 라벨 문자열을 보존합니다. 신뢰되지 않는 HTML로 우회하면 안 됩니다.
- [값 접근](https://surveydown.org/docs/accessing-values): 타입이 있는 응답과 저장 상태 재개를 지원하며 지원 조건의 R 출력은 `sd_value()`, `sd_is_answered()`를 사용합니다. 임의 R 표현식, 타입 변환 옵션, 파생 계산, 전체 벡터 연산은 greedyQ 원본 언어가 아닙니다.
- [조건 로직](https://surveydown.org/docs/conditional-logic): 제한된 비교 언어로 문항·페이지 표시, 출발 페이지 지정 분기, 중단 검사를 처리합니다. 기본 응답 여부·숫자·필수 검사를 지원하며 복합 논리 우선순위와 인용문 안의 접속사를 처리합니다. 일반 R 함수·벡터 연산·임의 표현식은 미지원입니다. Native 전역 skip과 출발 페이지 제한의 일치, matrix 전체 응답 여부, 복잡한 규칙 범위는 추가 검증이 필요합니다.
- [반응성](https://surveydown.org/docs/reactivity): 같은 페이지 종속 문항 표시를 구현했습니다. 일반 반응형 계산, 복제 출력, 응답값 삽입, 서버 생성 문항을 무제한 Shiny 프로그램으로 지원하지 않습니다. 향후 명시적 확장 범위이며 에이전트의 런타임 임의 수정으로 구현하지 않습니다.

## 외부 반환

[공식 리디렉션](https://surveydown.org/docs/external-redirect)은 고정 주소와 URL 인자 기반 주소를 구분합니다. greedyQ는 종료 결과별 고정 HTTPS 호스트, 승인된 쿼리 이름 매핑, 버튼, 선택적인 동일 탭 지연 이동을 컴파일합니다. 인자가 누락·중복되면 막고 인증정보는 전달하지 않습니다. 미리보기에서는 외부 이동을 차단하고, 연결된 참가자는 저장 성공 후 이동할 수 있습니다. 자동 팝업의 불확실성 때문에 새 탭은 클릭 방식입니다. Native 반환 버튼을 생성하지만 preview 자동 타이머는 제외하며 저장 후 반환 동작은 R 검증이 필요합니다. Prolific 계정 연동은 미시험입니다.

## 릴리스 조건

위 차이가 남은 상태에서 Prolific 외 모든 호환성 작업이 완료됐다고 설명하면 안 됩니다. 승인된 마이그레이션·재배포 전에는 기존 외부 프로젝트를 수정하지 않습니다. 아직 적용하지 않은 로컬 migration 004에 표시 순서 기록을 포함했습니다. 다른 004를 이미 적용한 설치는 새 추가 마이그레이션이 필요하며 해시를 덮어쓰면 안 됩니다.
