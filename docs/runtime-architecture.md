# greedyQ Runtime Architecture

[한국어](./runtime-architecture(kor).md)

## Decision

greedyQ uses a **Python-first reference implementation and a browser-native JavaScript delivery implementation**.

Python is used during early development to make grammar, validation, routing, and state semantics explicit. It is a reference and conformance oracle, not a final-user dependency. Researchers using greedyQ should ultimately need only a capable general-purpose AI and a modern web browser.

## Runtime layers

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

The JavaScript core operates on strings and plain data. It must not require filesystem access, Node.js APIs, React, Next.js, or a local build tool. Browser adapters may use file selection, drag and drop, embedded study text, or fetched repository artifacts. A Node adapter may be added for CI and developer convenience, but it cannot define semantics that are unavailable in the browser.

## Conformance contract

Python development may precede JavaScript implementation, but each behavior becomes complete only when the browser core matches the shared contract. Tests cover:

- normalized Survey AST;
- stable validation codes and severity;
- labels, stored values, and identifiers;
- routes, skip/display logic, and unreachable pages;
- consent gates and terminal outcomes;
- deterministic assignment inputs and persisted condition semantics;
- safe participant-visible rendering; and
- rejection of unsupported or executable survey content.

Differences in object-key ordering, source locations, or implementation metadata are acceptable only when declared non-semantic. Any behavioral disagreement is resolved deliberately in the specification and fixture; the production JavaScript implementation does not silently override the reference contract.

## Preview and production

Preview and production use the same JavaScript parser, validator, AST, and renderer. Preview disables external writes and production redirects and adds researcher controls. Production connects the validated application to Supabase.

Static HTML/CSS/JavaScript may be deployed to Vercel without a server-side application framework. Secure operations—including duplicate-participation checks, durable assignment, response persistence, withdrawal/deletion, lifecycle transitions, and protected export—belong in PostgreSQL transactions or Supabase RPCs protected by row-level security. The browser may contain a Supabase project URL and anonymous key under an appropriate security policy, but it must never contain service-role keys, database passwords, randomization secrets, or administrator credentials.

## Results boundary

The public survey and researcher results application are generated together but deployed separately. The survey is public. The results deployment is protected by Vercel Authentication and uses a server-only API whose Supabase secret is supplied by the Vercel integration. Both share one Supabase project; no administrator credential appears in browser files. Test status and respondent source are independent fields. See the [Results Dashboard](../RESULTS-DASHBOARD.md).

## Development sequence

1. Specify and test behavior in the Python reference implementation.
2. Record it as a language-neutral fixture and stable expected output.
3. Implement the behavior in the platform-neutral JavaScript core.
4. Run cross-runtime conformance tests.
5. Exercise the same renderer in browser preview and production modes.
6. Permit production release only after conformance, security, and hands-on researcher review gates pass.
