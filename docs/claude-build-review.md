# Claude first-study review follow-up

[한국어](./claude-build-review(kor).md)

Reviewed 2026-10-25 against the supplied `greedyQ-build-deploy-test.md`. The pasted HTML is byte-identical to the current website embed, not a second independent test report. The original Claude study folder was not supplied. Findings were reproduced using independently created synthetic studies, without touching the live paid Prolific pilot.

| Report | Response and verification boundary |
| --- | --- |
| P0-A, P1-D: missing files and records | `init` creates a complete draft folder and pending decisions, without questions or approvals. Build supplies canonical migrations 001–007, Vercel configuration and an environment example. Package preflight checks study records, declared documents, contained paths, identities and hashes. |
| P0-B: untouched slider accepted | Numeric and labeled sliders remain unanswered until interaction or an explicit configured default. Optional untouched sliders remain blank. Desktop/mobile browser tests cover required validation, keyboard interaction and preserved explicit defaults. Dates no longer silently use today. |
| P0-C, P2-B: differing Python screen and lost form values | `run` now serves the same JavaScript screen as preview/deployment. Python remains a backend/parser reference; the legacy Python form is no longer a participant UI review path. Canonical JavaScript validation retains input. |
| P1-A: conditional syntax | Whitelisted `contains`, `in`, `length`, `not` and grouped expressions compile and evaluate in Python/JavaScript. Native export renders the same parsed conditions with generated R collection handling. Invalid rules name the rule and give supported examples. Arbitrary code remains unsupported. |
| P1-B: hidden warnings | CLI shows warnings on success, counts only blocking errors as required changes, and identifies deployment checks separately. Unsupported footer/highlight settings were removed from golden studies. |
| P1-C, P1-E: account and mock ambiguity | Early guidance explains human account approval. Mock index shows an explicit local-only banner; deployment-stage preflight blocks mock mode and pending approvals. A complete folder is not evidence of an actual connection. |
| P1-F, P2-E: loading and migrations | Core-only bootstrap avoids premature profile choice; the final lock still requires a profile. Guides list all seven migrations and require one complete repository snapshot. Existing studies keep their lock unless an upgrade is approved. |
| P2-A, P2-F: language/display | Korean wrapping preserves words; preview tools follow the survey language for Korean, simplified/traditional Chinese and English. User-authored questions are not automatically translated. |
| P2-C: document title | The canonical respondent template already sets the title and language from the model. Regression coverage protects this existing behavior; no fictitious new fix is claimed. |
| P2-D: Python warning | The formatting expression uses a raw regular-expression string. |

Verification covers fresh draft creation, missing records/documents, unsafe paths, approval invalidation, CLI output, expression parity, actual browser sliders/follow-ups and the full existing suite. Generated native R source is syntax-checked when R is available; this is not proof of complete surveydown behavioral equivalence. External deployment remains unverified by Claude’s report because login was its stopping point.

Vercel’s optional new onboarding route is reviewed separately in [Vercel agent onboarding](./vercel-agent-onboarding.md). No global installation, authentication, paid recruitment or cloud mutation was performed for this review.
