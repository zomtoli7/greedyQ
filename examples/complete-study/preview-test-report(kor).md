# 골든 레퍼런스 프리뷰 테스트 보고서

영문 원본: [preview-test-report.md](preview-test-report.md)

## 범위

이 보고서는 골든 레퍼런스 연구의 프리뷰 모델, 고정 browser-native runtime bundle, 생성된 HTML, 그리고 이를 보호하는 AI 생성 계약을 다룹니다. 프리뷰는 연구자 검토용 산출물이며 실제 데이터 수집용 운영 런타임이 아닙니다.

## 자동 검증 결과

- 2026-09-08 기준 browser-native cross-runtime, device-selection, validation, mock-persistence, static-bundle, Supabase fail-closed scenario 8개를 포함한 저장소 테스트 95개가 통과했습니다.
- 별도로 직접 작성한 모델을 사용하지 않고 `survey.qmd`와 `greedyq.yml`에서 프리뷰 모델과 HTML을 다시 생성했습니다.
- 기준 런타임 JavaScript가 `node --check`를 통과했습니다.
- 프리뷰 모델이 전용 JSON Schema를 통과했습니다.
- QMD의 모든 페이지와 문항이 프리뷰 모델에 포함되었습니다.
- 화면 표시 라벨과 저장값이 QMD 원본과 정확히 일치합니다.
- 두 실험 조건과 5개 종료 결과의 모든 경로가 정상적으로 해석됩니다.
- 동의 거부, 미성년자 탈락, 철회, 조건부 삭제 요청, 숨겨진 응답 제거, 검증, 조건 전환을 검사합니다.
- 생성 프리뷰가 기준 모델을 그대로 포함하고 generated JavaScript/CSS는 repository runtime과 byte-for-byte로 일치하며 manifest hash도 일치합니다.
- 영문/한국어 Markdown 쌍과 저장소 공백 검사도 통과했습니다.

## 발견하고 수정한 결함

1. 프리뷰 모델의 일부 지지도 척도 라벨이 QMD 원본과 정확히 같지 않았습니다. 이제 응답자용 전체 라벨과 저장값을 그대로 보존합니다.
2. 조건부 삭제 요청 필드가 필수 문항 일치 검사에서 빠져 있었습니다. 이제 조건부 필수 문항으로 표현하고 `greedyq.yml`과 대조합니다.
3. 연구자 패널에서 조건을 강제 변경하면 배정 이후의 이전 응답이 남을 수 있었습니다. 이제 해당 응답을 삭제하고 삭제된 ID를 `condition_forced` 감사 이벤트에 기록합니다.
4. 기존 프리뷰는 연구자가 실질적으로 검토하기에 지나치게 단순했습니다. 이제 독립 desktop/mobile session을 동시에 render하고 condition/page control, mock-state inspection, validation, progress, routing, terminal outcome, 안전한 no-network boundary를 제공합니다.

## 시나리오 범위

모델 테스트는 control과 treatment의 정상 경로, 동의 거부와 선별 탈락, 삭제 요청이 있는 철회와 없는 철회, 모든 종료 결과, 조건부 문항의 표시·비표시 상태, 필수 응답 오류, 숫자 범위, 경로 해석, 진행 경로, ID 중복, 선택지 매핑을 다룹니다. 실패 simulation은 잘못된 QMD call, 누락된 question ID, 존재하지 않는 route target, 뒤집힌 display/store mapping, 안전하지 않은 raw HTML, 지원되는 모든 preview input type을 포함합니다.

시각·상호작용 승인 기준은 [`docs/preview-ui-spec(kor).md`](../../docs/preview-ui-spec\(kor\).md)에 있습니다. 데스크톱, 태블릿, 휴대전화, 키보드, 포커스, 검증, 매트릭스 가로 스크롤, 200% 확대, 연구자 도구 검토 사례를 포함합니다.

## 남은 수동 승인 단계

로컬 인앱 브라우저 연결은 Node 런타임 브리지의 운영체제 “No such file or directory” 오류로 시작되지 않았습니다. 따라서 실제 브라우저의 화면 크기별 표시, 키보드 조작, 스크린리더 검토가 통과했다고 주장하지 않습니다. 사람이 `preview.html`을 열어 필수 시나리오를 수행하고 증거를 남길 때까지 `interactive_preview_reviewed`는 미완료 상태여야 합니다. 모델·보안·문법·계약 자동 검사는 이 제한과 무관하게 모두 통과했습니다.
