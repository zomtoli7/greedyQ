# greedyQ 런타임 아키텍처

[English](./runtime-architecture.md)

## 결정

greedyQ는 **Python 우선 reference implementation과 browser-native JavaScript 최종 사용자 구현**을 함께 사용합니다.

초기 개발에서는 Python으로 문법, 검증, 경로, 상태 의미론을 명확히 고정합니다. Python은 reference 및 conformance 기준이지 최종 사용자의 필수 환경이 아닙니다. 최종적으로 연구자는 capable general-purpose AI와 modern web browser만으로 greedyQ를 사용할 수 있어야 합니다.

## 런타임 계층

```text
survey.qmd + greedyq.yml
           |
           v
 platform-neutral JavaScript core
 parse -> AST -> validate -> compile/render
       /                         \
      v                           v
browser preview          respondent application
                                    |
                                    v
                      Supabase RPC + PostgreSQL RLS
                                    |
                                    v
                            static Vercel hosting

Python reference implementation
           |
           v
shared conformance fixtures <-> JavaScript core
```

JavaScript core는 string과 plain data만 입력으로 사용합니다. Filesystem access, Node.js API, React, Next.js, local build tool을 요구해서는 안 됩니다. Browser adapter는 file selection, drag and drop, embedded study text 또는 repository artifact fetch를 사용할 수 있습니다. CI와 개발 편의를 위한 Node adapter는 추가할 수 있지만 browser에서 사용할 수 없는 의미론을 정의해서는 안 됩니다.

## Conformance 계약

Python 개발이 JavaScript 구현보다 먼저 진행될 수 있지만, 각 동작은 browser core가 shared contract와 일치해야 완성된 것으로 봅니다. 테스트 범위는 다음과 같습니다.

- normalized Survey AST
- 안정적인 validation code와 severity
- label, stored value, identifier
- route, skip/display logic, unreachable page
- consent gate와 terminal outcome
- deterministic assignment input과 persisted condition 의미론
- 안전한 participant-visible rendering
- unsupported 또는 executable survey content 거부

Object key 순서, source location, implementation metadata 차이는 non-semantic으로 명시된 경우에만 허용합니다. 동작이 다르면 specification과 fixture에서 의도적으로 결정해야 하며 production JavaScript 구현이 reference contract를 조용히 덮어쓰면 안 됩니다.

## Preview와 production

Preview와 production은 동일한 JavaScript parser, validator, AST, renderer를 사용합니다. Preview는 external write와 production redirect를 차단하고 researcher control을 추가합니다. Production은 validated application을 Supabase에 연결합니다.

Static HTML/CSS/JavaScript는 server-side application framework 없이 Vercel에 배포할 수 있습니다. Duplicate-participation check, durable assignment, response persistence, withdrawal/deletion, lifecycle transition, protected export 같은 보안 작업은 row-level security로 보호되는 PostgreSQL transaction 또는 Supabase RPC에서 수행합니다. 적절한 보안 정책 아래 browser에 Supabase project URL과 anonymous key를 포함할 수 있지만 service-role key, database password, randomization secret, administrator credential은 절대 포함하면 안 됩니다.

## 개발 순서

1. Python reference implementation에서 동작을 명시하고 테스트합니다.
2. 이를 language-neutral fixture와 stable expected output으로 기록합니다.
3. Platform-neutral JavaScript core에 같은 동작을 구현합니다.
4. Cross-runtime conformance test를 실행합니다.
5. 동일 renderer를 browser preview와 production mode에서 시험합니다.
6. Conformance, security, hands-on researcher review gate를 모두 통과한 뒤에만 production release를 허용합니다.
