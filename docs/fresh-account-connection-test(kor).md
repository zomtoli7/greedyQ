# 새 계정 연결 테스트

[English](./fresh-account-connection-test.md)

날짜: 2026-09-10. 런타임: `0.2_2026-09-10_c4a8405`.

## 확인 완료

- 새 Vercel 계정 `zomtoli-3542`, 팀 `dong-soo-kim01`을 사용했으며 기존 계정의 리소스를 재사용하지 않았습니다.
- 연구자가 Vercel 기기 로그인과 Supabase Marketplace 약관을 승인했습니다.
- `icn1` 지역에 Supabase Free 리소스 `greedyq-fresh-account-test`를 생성하고 `greedyq-fresh-results`에 연결했습니다. Vercel이 연결 정보를 자동 동기화했습니다.
- 인증서를 검증하는 TLS 연결로 기준 마이그레이션 세 개를 모두 실행했고 greedyQ 테이블 일곱 개를 확인했습니다. 공식 Supabase 대시보드 소스의 CA 다운로드 주소는 `https://supabase-downloads.s3-ap-southeast-1.amazonaws.com/prod/ssl/prod-ca-2021.crt`입니다.
- 공개 설문: https://greedyq-fresh-survey.vercel.app
- 보호된 결과 화면: https://greedyq-fresh-results.vercel.app
- 결과 보호는 `ssoProtection.deploymentType = all`로 명시했습니다. 초기 `all_except_custom_domains` 설정에서는 운영 별칭 주소가 공개되어 있어 테스트 응답 입력 전에 수정했습니다. 현재 비로그인 결과 HTML·API 요청은 로그인으로 이동합니다(302).
- 기준 JavaScript 저장 코드로 새 데이터베이스에서 세션 생성, 동의 전 저장 차단, 배정 유지, 저장·재접속, 잘못된 접근 토큰 거부, 익명 세션 목록 접근 차단을 검증했습니다.
- 대시보드 확인용으로 답변 세 개가 있는 가상 완료 응답 Direct/Test 한 건을 남겼습니다. 배포된 인증 결과 API에서 Test/Direct 한 건, 실제 응답 0건을 확인했습니다.

## 범위와 후속 확인

배포한 설문은 직접 진입과 테스트 모드를 적용한 독립된 complete-study 테스트 예제입니다. 실제 모집 승인을 받은 설문이 아닙니다. 런타임 파일은 그대로 복사했으며 내장 연구·배포 설정만 조정했습니다. 공개 파일에 비밀키를 넣지 않았습니다. 결과 배포에만 데이터베이스 비밀키가 전달됩니다.

이번에는 배포된 HTTP/API 동작을 검증했으며, 실제 브라우저 화면 조작이나 참가자의 전체 클릭 경로는 검증하지 않았습니다. 연구자는 두 링크를 확인해야 하며 실제 모집, Prolific, 전체 기기별 인수 검사는 별도 단계입니다. Vercel의 배포명이 “production”이어도 연구의 테스트 분류는 바뀌지 않습니다.

로컬 작업 스크립트와 비공개 연결 정보는 저장소 밖 `/tmp/greedyq-fresh-connect.vRL9tI`에 있습니다. 이 폴더를 공개하지 마세요. 독립된 배포 묶음과 가상 응답 검사 스크립트이며, 완성된 재사용 온보딩 구현은 아닙니다. Vercel CLI가 인증 API 검사용 자동화 보호 우회 자격 증명을 생성했으며 비공개로 유지해야 합니다.
