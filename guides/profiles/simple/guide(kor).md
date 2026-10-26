# greedyQSimple Profile Guide

<!-- GREEDYQ_DESKTOP_POLICY -->
**greedyQ로 설문을 만들거나 수정할 때는 컴퓨터에 설치한 AI 데스크톱 앱이 반드시 필요합니다. AI 웹 앱은 공식 지원하지 않습니다.** ChatGPT 데스크톱 또는 Claude Desktop을 공식 제공처에서 다운로드하세요. Gemini는 데스크톱 앱을 포함해 공식 지원하지 않습니다. 앱에서 파일을 읽고 만들고 작업을 실행하는 에이전트 기능을 사용해야 합니다. 앱 설치나 유료 구독만으로 이 기능이 보장되지는 않습니다. 필요한 도구가 없는 일반 채팅으로는 설문 제작을 진행하지 않습니다. 참여자가 설문에 응답하거나 연구자가 컴퓨터·모바일 미리보기와 결과 화면을 보는 데에는 계속 웹브라우저를 사용합니다. [설문 제작에 사용할 앱](../../../SUPPORTED-ENVIRONMENTS(kor).md).
<!-- /GREEDYQ_DESKTOP_POLICY -->

[English](./guide.md) · [简体中文](./guide(zh-CN).md)

**Object:** `greedyQSimple`

배정된 실험 조건이나 반복 conjoint choice task가 없는 기술조사, 피드백, 선별 또는 일반 설문에 이 profile을 사용합니다.

연구 목적과 대상을 들은 뒤, 필요한 핵심 정보, 모집과 참여 자격, 문항 주제, 응답 형식, 순서, 조건부 표시, 완료 결과, 예정 분석을 질문합니다. Core의 초기 위험 점검은 즉시 수행하되, 자세한 IRB와 consent 작업은 지금 할지 일관된 설문 초안 뒤에 할지 묻습니다.

Double-barreled 또는 leading wording, 불균형 척도, 겹치는 선택지, 빠진 opt-out, 과도한 부담, 잘못된 skip logic, 접근하기 어려운 control을 점검합니다. 문제가 있으면 설명하고 연구자가 선택하게 합니다. 전체 문항 흐름이 일관되면 즉시 참여자 preview를 만듭니다.

설문 데이터에서 집단을 비교한다는 이유만으로 random assignment를 추가하지 않습니다. 설문이 조건이나 stimulus를 배정하게 하려면 `experiment` profile을 추천하고 변경을 확인받습니다.
