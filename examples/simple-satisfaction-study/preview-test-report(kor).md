# greedyQSimple 만족도 설문 테스트 보고서

[English](./preview-test-report.md)

## 자동 검증 결과

2026-09-08 기준 95개 repository test suite 안에서 이 연구의 전용 테스트가 모두 통과했습니다. Suite에는 browser-native cross-runtime, device-selection, validation, mock-persistence, static-bundle, Supabase fail-closed scenario 8개가 포함됩니다.

이제 preview는 `survey.qmd`와 `greedyq.yml`에서 직접 다시 생성되며 `preview-model.json`을 별도의 source로 관리하지 않습니다.

자동 검사는 다음을 다룹니다.

- `greedyQSimple` object와 고정된 modular guide resolution
- 모든 내부 state schema와 artifact hash
- QMD와 preview 사이의 정확한 page 및 question 일치
- 화면 표시 label과 stored value의 정확한 mapping
- Randomization과 experimental-condition route가 없음
- 참여 가능 완료, consent 거부, 미성년자 및 비사용자 선별 탈락, withdrawal, technical-error outcome
- 낮은 만족도, 기타 사용 목적, 문제, deletion request 후속 문항의 표시 및 숨김 상태
- Age와 recommendation score 범위
- 제품 feedback 문항보다 앞선 consent timing
- Participant redirect와 직접 identifier 문항이 없음
- 고정 desktop/mobile browser runtime bundle의 재현 가능한 생성
- 기술적이고 비인과적인 분석 표현

## 연구설계 선택

성공한 사용자만 선별하지 않고 실패하거나 중단한 greedyQ 경험도 받습니다. 전반적 만족도를 주요 기술 결과로 사용하고 구체적인 경험 요소는 별도로 측정하며, 일반적인 추천 점수를 수집하되 이를 유일한 제품 성과로 취급하지 않습니다. 서술형 prompt는 credential이나 비공개 연구정보를 입력하지 않도록 경고합니다. Attention check는 짧고 자발적인 feedback 설문에 부담을 추가하면서 기준 연구의 핵심 목적에는 도움이 되지 않으므로 포함하지 않았습니다.

## 남은 수동 승인 단계

자동 검사는 직접 조작하는 검토를 대신하지 않습니다. 실제 사용 전 연구자가 `preview.html`을 열어 모든 조기 종료와 조건부 경로를 시험하고, 휴대전화와 desktop layout을 확인하고, keyboard 사용을 시험하며, 가상 연락처를 교체해야 합니다. 실제 기관 검토, 배포, 응답 수집은 수행하지 않았습니다.
