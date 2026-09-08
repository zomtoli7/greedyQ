# Browser-Native Preview와 Runtime

[English](./browser-preview.md)

greedyQ v0.2는 하나의 고정 browser core와 세 가지 rendering mode를 사용합니다.

| Mode | 목적 | 선택 방식 |
| --- | --- | --- |
| `desktop` | Wide screen 및 precise pointer용 respondent experience | `index.html`에서 자동 감지 |
| `mobile` | Narrow/mobile device용 touch-friendly respondent experience | `index.html`에서 자동 감지 |
| `preview` | 독립된 desktop/mobile session을 동시에 표시하는 researcher review | `preview.html`에서 항상 사용 |

Browser core가 `QMD/YAML text → parse → validate → normalized model → render` 전 과정을 수행합니다. Python, Node.js, R, Quarto 또는 build tool을 요구하지 않습니다. `templates/browser/studio.html`은 browser file selection으로 local `survey.qmd`와 `greedyq.yml`을 받아 전체 변환을 로컬에서 수행합니다.

## Generated bundle

Cross-runtime conformance 개발 중에는 현재 Python reference builder도 동일 static bundle을 생성할 수 있습니다.

```bash
python3 -m greedyq build examples/complete-study
```

`index.html`, dual-mode `preview.html`, 고정 `greedyq-core.js`, 고정 `greedyq-runtime.css`, `preview-model.json`, `.greedyq/` 아래 internal validation evidence를 생성합니다. Generated JavaScript와 CSS는 pin된 repository file과 byte-for-byte 일치해야 합니다. AI agent는 문서화된 study-data slot만 교체할 수 있으며 runtime을 다시 생성하거나 customize하면 안 됩니다.

## 로컬 simulation

Preview는 virtual participant ID와 local mock adapter를 사용합니다. 데이터를 전송하지 않고 required answer, display/skip logic, desktop/mobile layout, balanced persistent assignment, partial-save resume, terminal outcome, withdrawal deletion을 시험합니다. Desktop과 mobile preview pane은 독립 session을 사용하므로 양쪽 경로를 나란히 테스트할 수 있습니다.

Mock data는 synthetic browser-local state이며 Supabase가 설정 또는 검증되었다는 뜻이 아닙니다. Reset은 virtual session을 제거합니다. Production credential과 participant identifier는 preview에서 금지합니다.

## 구조 개요

`preview.html`의 **View structure**를 누르면 설문을 완료하지 않고도 모든 page, text block, question ID, question type, required 표시 및 terminal outcome을 볼 수 있습니다. Page는 펼치거나 접을 수 있습니다. 이는 sdstudio Build tab의 유용한 hierarchy view에서 영감을 받은 읽기 전용 보조 기능이며, sdstudio를 구현하지 않고 QMD도 편집하지 않습니다.

## 온라인 컨트롤 갤러리

[컨트롤 갤러리](https://zomtoli7.github.io/greedyQ/examples/control-gallery/preview.html)는 지원되는 모든 컨트롤을 같은 desktop/mobile preview에서 시험합니다. GitHub Pages가 `main`의 canonical static example을 게시하므로 Vercel이나 Supabase 계정 없이 볼 수 있습니다.

## Deployment 경계

모든 deterministic behavior는 external connection 전에 로컬에서 통과해야 합니다. Vercel은 이미 테스트한 static bundle을 받아 제공할 뿐 questionnaire를 다시 해석하면 안 됩니다. Supabase는 승인된 RPC와 row-level security를 통해 persistence/assignment adapter만 교체합니다. Supabase 연결은 parsing, validation, rendering, routing, consent 또는 outcome semantics를 바꾸면 안 됩니다.

Preview Content Security Policy는 network write를 차단합니다. Participant entry point는 production Supabase RPC에 필요하므로 HTTPS만 허용합니다. Service-role key, database password, administrator credential, randomization secret은 browser file에 절대 넣으면 안 됩니다.

## 필수 review scenario

배포 전에 desktop/mobile completion, required answer와 numeric limit, consent refusal와 screening, 모든 condition, conditional question과 hidden-answer removal, back/save/refresh/resume, withdrawal/deletion, 모든 terminal outcome, keyboard focus, zoom, narrow-screen overflow를 시험합니다.
