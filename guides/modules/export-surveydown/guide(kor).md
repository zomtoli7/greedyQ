# surveydown Export Module

[English](./guide.md)

`survey.qmd`와 `app.R`을 포함한 native surveydown-compatible project를 중요한 보조 산출물로 만듭니다. greedyQ Vercel/Supabase runtime이 기본입니다. 공개된 surveydown behavior와 documentation만 사용하고 source, test, internal fixture를 복사하지 않습니다.

각 기능을 directly portable, generated, greedyQ-only, unsupported로 분류합니다. 화면 표시 라벨과 저장값을 정확히 검증합니다. 달라지거나 export할 수 없는 동작은 연구자에게 쉬운 말로 설명하고 중요한 차이는 승인받습니다. greedyQ가 지원하는 runtime을 넘어선 고급 customization에는 native surveydown을 권합니다.

모든 greedyQ 전용 컨트롤(`audio`, `video`, `rank_order`, `side_by_side`, `nps`, `timing`, `constant_sum`, `pick_group_rank`, `drill_down`, 그리고 확정된 `custom` 컨트롤)은 내보낼 때 greedyQ `sd_question()` 블록을 Surveydown의 공개 `sd_question_custom()` 인터페이스로 바꿔야 합니다. `app.R`에는 대응하는 Shiny 출력과 reactive 값 바인딩을 생성해야 하며, 내보낸 QMD에 Surveydown이 모르는 greedyQ 타입을 남기면 안 됩니다. native Surveydown runtime에서 검토하기 전까지 이 변환은 `generated_custom` 및 `generated_unverified`로 표시합니다. 코드가 생성되었다는 이유만으로 정확한 동작 동일성을 주장하면 안 됩니다.

호환성 보고서에는 변환된 모든 문항, 계속 greedyQ 전용으로 남는 모든 동작, 중요한 차이를 기록해야 합니다. 생성된 프로젝트는 보조 산출물이며, 결정론적 브라우저 runtime이 greedyQ의 주 runtime입니다.
