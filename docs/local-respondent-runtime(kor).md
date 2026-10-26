# 로컬 참가자 화면

<!-- GREEDYQ_DESKTOP_POLICY -->
**greedyQ로 설문을 만들거나 수정할 때는 컴퓨터에 설치한 AI 데스크톱 앱이 반드시 필요합니다. AI 웹 앱은 공식 지원하지 않습니다.** ChatGPT 데스크톱 또는 Claude Desktop을 공식 제공처에서 다운로드하세요. Gemini는 데스크톱 앱을 포함해 공식 지원하지 않습니다. 앱에서 파일을 읽고 만들고 작업을 실행하는 에이전트 기능을 사용해야 합니다. 앱 설치나 유료 구독만으로 이 기능이 보장되지는 않습니다. 필요한 도구가 없는 일반 채팅으로는 설문 제작을 진행하지 않습니다. 참여자가 설문에 응답하거나 연구자가 컴퓨터·모바일 미리보기와 결과 화면을 보는 데에는 계속 웹브라우저를 사용합니다. [설문 제작에 사용할 앱](../SUPPORTED-ENVIRONMENTS(kor).md).
<!-- /GREEDYQ_DESKTOP_POLICY -->

[English](./local-respondent-runtime.md)

모든 참가자 화면 검토에는 동일한 브라우저 실행 코드를 사용합니다.

```sh
python3 -m greedyq run examples/complete-study
```

`http://localhost:4180/index.html`을 엽니다. 컴퓨터·모바일 미리보기 및 배포와 같은 고정 JavaScript 렌더러를 사용합니다. mock 모드의 응답은 브라우저 시험 저장소에만 남으며 연구자에게 전송되지 않습니다. 두 화면을 함께 보려면 `python3 -m greedyq preview PATH_TO_STUDY`를 사용하세요. `--port`로 포트를 바꿀 수 있으며 `run`의 `--database`는 더 이상 지원하지 않습니다.

Python은 개발용 독립 파서·검증기·컴파일러·백엔드 상태 기준 구현으로 유지합니다. 내부 `Store`와 기존 서버는 별도로 시험하지만, 예전 서버 렌더링 화면은 참가자 UI 적합성 시험이나 실제 브라우저 검토를 대신하지 않습니다. 데이터베이스 동작은 임시 PostgreSQL과 기본 RPC 마이그레이션으로 별도 검증합니다. 로컬 가상 시험이 실제 Supabase/Vercel 연결을 입증하지는 않습니다.

`python3 -m greedyq init NEW_FOLDER --id study_id --profile simple --language ko`로 새 초안을 만듭니다. 시작·종료 페이지, 미승인 검토 기록, 일곱 마이그레이션과 정적 배포 파일이 포함되며 문항·승인은 만들어내지 않습니다. `preflight NEW_FOLDER`는 로컬 묶음을 검사하고 경고도 보여줍니다. `preflight NEW_FOLDER --stage deployment`는 mock 모드와 미해결 배포 결정·승인도 차단합니다. 검사를 통과해도 실제 연결이 입증되지는 않습니다. 로컬 시험 서버로 참가자를 모집하지 마세요.

연결 정보가 삽입된 후보가 별도 폴더에 있으면 `preflight PATH_TO_STUDY --stage deployment --deployment-index PREPARED_SURVEY/index.html`로 검사합니다. 원본 미리보기는 mock 상태로 유지하며 후보의 연구 내용이 현재 검증 결과와 같은지도 확인합니다.
