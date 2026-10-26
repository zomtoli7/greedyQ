# greedyQExperiment Profile Guide

<!-- GREEDYQ_DESKTOP_POLICY -->
**greedyQ로 설문을 만들거나 수정할 때는 컴퓨터에 설치한 AI 데스크톱 앱이 반드시 필요합니다. AI 웹 앱은 공식 지원하지 않습니다.** ChatGPT 데스크톱 또는 Claude Desktop을 공식 제공처에서 다운로드하세요. Gemini는 데스크톱 앱을 포함해 공식 지원하지 않습니다. 앱에서 파일을 읽고 만들고 작업을 실행하는 에이전트 기능을 사용해야 합니다. 앱 설치나 유료 구독만으로 이 기능이 보장되지는 않습니다. 필요한 도구가 없는 일반 채팅으로는 설문 제작을 진행하지 않습니다. 참여자가 설문에 응답하거나 연구자가 컴퓨터·모바일 미리보기와 결과 화면을 보는 데에는 계속 웹브라우저를 사용합니다. [설문 제작에 사용할 앱](../../../SUPPORTED-ENVIRONMENTS(kor).md).
<!-- /GREEDYQ_DESKTOP_POLICY -->

[English](./guide.md) · [简体中文](./guide(zh-CN).md)

**Object:** `greedyQExperiment`

연구가 participant, session, cluster, stimulus, 순서 또는 다른 unit을 조건에 배정하고 그 배정의 효과를 추정할 때 이 profile을 사용합니다.

이 profile은 연구 의도를 설명하며 모든 배정 단위가 구현되었다는 약속은 아닙니다. 고정 runtime은 현재 참가자 단위의 단순 또는 고정 블록 배정 하나를 지원합니다. 차이를 설명하고 방식·가중치·해당하는 경우 블록 크기·시점을 확인합니다. [RANDOMIZATION(kor).md](../../../RANDOMIZATION(kor).md)를 따르며, 지원하지 않는 단위나 여러 단계 배정을 무시하지 말고 차단합니다. 같은 페이지에서 지정한 문항을 섞는 기능은 별도로 선택하며, 순서를 기록하고 고정 문항의 자리를 유지합니다.

연구 질문, primary outcome, hypothesis, assignment unit, condition, allocation probability, 배정 시점, 재접속 시 유지 방식, stimulus, manipulation check, contamination 위험, exclusion, stopping rule, primary analysis를 확인합니다. Condition, stimulus, hypothesis 방향, sample size, exclusion 또는 analysis commitment를 지어내지 않습니다.

Randomization은 선언된 unit에서 한 번만 수행하고, 문서화된 난수 원천을 사용하며, condition-dependent content를 보여주기 전에 저장되고, 새로고침이나 재접속 후에도 유지되어야 합니다. Preview control은 검토를 위해 condition을 강제할 수 있지만 respondent control과 시각적으로 분리되어야 하며 production assignment behavior를 바꾸면 안 됩니다.

의도한 경우 baseline measure가 treatment보다 앞서는지, treatment-dependent measure가 노출 뒤에 오는지, 숨겨진 응답이 분석을 오염시키지 않는지, 모든 condition이 유효한 outcome에 도달하는지 확인합니다. Instrument 승인 전에 interactive preview에서 모든 condition을 연구자가 검토하도록 요청합니다.

기본 배정 방식만 연구의 한계로 안내하지 마세요. 연구자가 다른 절차를 요청하면 [배정 안내](../../../RANDOMIZATION(kor).md)의 확장 절차로 의도를 확정하고, 기본 기능과 별도 구현·미검증 상태를 구분합니다. “4개 그룹 무작위 배정 + 그룹별 순차 자극물”은 예시일 뿐 새 기본 기능이 아닙니다. 고정 코드를 임의 수정하지 말고 버전별 연구 확장과 동시성·재접속 검증을 준비하세요.
