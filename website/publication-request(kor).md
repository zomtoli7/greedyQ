# 홈페이지 워크: 현재 검증된 소스 게시

[English](./publication-request.md)

현재 main의 `release.json`, `website/publication-manifest.json`, `website/google-sites-embed.html`, `docs/website-prompt-copy-audit-2026-10-26(kor).md`를 함께 읽으세요. 준비 릴리스는 `0.2_2026-10-26_beac897`이며 HTML SHA-256은 `78ae3e7f7662c659076c1636f5d80aee3d46f378811a1795abe1f37eac627605`, 크기는 801385바이트입니다. `source_commit`은 실질 코드 커밋이며 버전을 찍은 HTML은 뒤의 메타데이터 커밋에 있습니다. `source_commit`만 보고 이전 HTML을 가져오면 안 됩니다.

기존 Google Sites 편집기에서 현재 공개/편집 내용을 비교해 무관한 변경을 보존하고, 사이트·페이지·도메인·메뉴·갤러리·이미지·연락처를 유지한 채 기존 전체 페이지 custom embed만 준비 HTML 전문으로 교체하세요. 사용자의 기존 승인과 현재 브라우저 도구 정책에 따라 저장·게시합니다. 홈페이지 갱신이지 CBC 배포·계정 변경·응답 편집·모집·지급 승인이 아닙니다.

영문·한글·중문에서 버전·업데이트 기록을 확인하세요. About → Project → Contact는 `greedyq.contact@gmail.com`을 유지합니다. 한국어·중국어 시작 프롬프트를 복사해 URL이 `<...>`로 감싸지고 줄바꿈을 모두 지워도 별도 주소로 남는지 확인하세요. 복사 버튼과 클립보드 거부 후 수동 선택을 확인하고 BibTeX 문법을 보존하세요. 로컬 전수 검사는 블록 135개를 두 폭에서 270회 대조했습니다. 이 자동 시험만으로 실제 Gemini/Claude 성공을 추정하지 마세요.

공개 사이트의 전체 `data-code` embed를 가져와 복호화하고 manifest의 바이트·SHA-256과 완전히 일치한 뒤에만 게시 완료로 기록하세요. 제공업체 정규화나 차이가 있으면 명시하고, 편집기 저장을 공개 증거로 삼지 마세요. CBC 수집은 로컬 PostgreSQL/브라우저 검증이며 새 클라우드·유료 CBC 승인 시험이 아닙니다. 접근할 수 없으면 pending을 유지하고 정확히 보고하세요.


Gemini는 데스크톱도 공식 지원하지 않습니다. 가이드·파일 확인 전에 앱 종류를 확인하고 ChatGPT 데스크톱 Work/Codex 또는 Claude Desktop으로 안내합니다. Gemini 저장소 가져오기나 첨부는 예외가 아닙니다.


시작하기 설명 바로 아래, 복사 프롬프트 위에 지원 안내가 표시되는지 확인하세요. Gemini 미지원 이유를 확인되지 않은 Google의 GitHub 차단 정책으로 바꾸지 마세요.


Verify About > Compatibility > Available AI agents (`about/agents`) in all three languages. Current support: capable ChatGPT/Claude desktop apps. Future support review: Gemini. Additional evaluation candidates only: Meta AI, Grok, DeepSeek. START-HERE now gates the app before any study interview and stops unsupported hosts; do not offer attachments as an exception.
