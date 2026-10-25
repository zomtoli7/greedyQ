# 외부 반환 링크

[English](./EXTERNAL-RETURNS.md)

AI에게 요청하세요: “완료 응답을 저장한 뒤 반환 버튼을 보여줘. 미리보기에서는 비활성화하고, 시작 링크에서 승인한 참가자 참조값만 전달해줘.”

`greedyq.yml`의 종료 결과에 설정합니다:

```yaml
outcomes:
  complete:
    page: complete
    lifecycle_state: completed
    redirect: https://example.org/return
    redirect_label: Return to the study provider
    redirect_params:
      participant: PARTICIPANT_ID
    redirect_newtab: false
```

`redirect_params`는 전달할 이름 → 시작 URL의 이름을 명시적으로 연결합니다. 값은 URL 인코딩하며 코드로 삽입하지 않습니다. 명시하지 않은 URL 인자나 설문 응답은 전달하지 않습니다. 필요한 인자가 누락·빈 값·중복이면 이동을 막습니다. 인증정보처럼 보이는 인자명, HTTPS가 아닌 주소, 주소 내 로그인 정보, 동적 fragment, 기존 쿼리 키 중복을 거부합니다.

고정 주소는 `redirect_params`를 생략합니다. `redirect_delay: 5`를 넣으면 5초 후 같은 탭에서 이동합니다. 지연을 생략하면 클릭 전용입니다. 새 탭은 클릭이 필요하며 지연과 조합할 수 없습니다. 모집 전 목적지와 식별자 전달에 대한 연구자 승인을 기록합니다.

브라우저 미리보기는 지연이 0이어도 외부로 이동하지 않습니다. 연결된 참가자에게는 종료 상태 저장 성공 후에만 버튼을 활성화합니다. 저장 실패 시 비활성 상태를 유지합니다. 이는 Prolific 계정 연결이나 완료 보상 검증이 아니며 이후 패널 종단간 시험이 필요합니다.

Native Surveydown export는 반환 버튼을 만들지만 안전한 preview에서는 자동 타이머를 생략합니다. 동적 인자와 저장 후 반환은 대상 R 런타임에서 검증해야 하며 내보내기 보고서에 이 제한을 표시합니다.
