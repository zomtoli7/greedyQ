# greedyQ Update History

[한국어](./README(kor).md)

Each substantive greedyQ update has one short English note and a matching `(kor).md` copy. The filename is the release identifier: `version_date_source-commit.md`.

The source commit identifies the substantive code, specification, or documentation change. A following metadata-only commit may stamp that source commit into README, core guide, surveys, and this history. Metadata-only stamping commits do not receive separate entries because doing so would create an endless self-referential version update.

## 0.3 development

- [`0.3_2026-10-26_e0167e7`](./0.3/0.3_2026-10-26_e0167e7.md) — Verified the dedicated v0.3 CBC Test/Direct journey on existing Vercel/Supabase accounts: consent, assignment, persistent choices, completion timestamp, protected results, withdrawal and CSV. Three repeated journeys passed; all 21 retained sessions are synthetic Test records, with six completions and 81 long CSV rows.

## 0.2

- [`0.2_2026-10-26_e3958de`](./0.2/0.2_2026-10-26_e3958de.md) — Use https://greedyq.netlify.app/ as the canonical start URL throughout English, Korean and Chinese entry pages, guides and homepage prompts for both new and saved studies. Keep full initialization and access recovery on GitHub; retain source files and immutable study locks rather than silently upgrading studies.

- [`0.2_2026-10-26_1fbfcfd`](./0.2/0.2_2026-10-26_1fbfcfd.md) — Fix repeat Netlify builds that failed when cached output did not exactly match its old manifest. Generate and verify a fresh staging folder, preserve previous output outside the public directory and replace only the dedicated ignored publish path; restore it if replacement fails. Keep generic local output checks strict and reject tracked/symlink destinations.

- [`0.2_2026-10-26_4373f4f`](./0.2/0.2_2026-10-26_4373f4f.md) — Make the public start entry an explicit four-step protocol: communicate in the user's language; unsupported hosts inform and stop; supported hosts must read and obey GitHub INITIALIZE.md and use GUIDE-ACCESS.md for access failures; saved studies use the supplied authoring folder/ZIP and the initialization resume procedure.

- [`0.2_2026-10-26_ed1dc2b`](./0.2/0.2_2026-10-26_ed1dc2b.md) — Keep the English public start page in English and show the complete pinned GitHub INITIALIZE address visibly in all three languages. The full initialization remains on GitHub; START-HERE Markdown and HTML share one source.

- [`0.2_2026-10-26_df6d737`](./0.2/0.2_2026-10-26_df6d737.md) — Move the complete initialization workflow to INITIALIZE.md. Keep START-HERE.md as the short public front door and render its English/Korean/Chinese HTML directly from the same Markdown source; preserve existing links and pinned-study resume behavior.

- [`0.2_2026-10-26_fa94594`](./0.2/0.2_2026-10-26_fa94594.md) — Finalize v0.2 documentation with the desktop-host first-action gate and the available AI agents compatibility page. Current support is capable ChatGPT/Claude desktop apps; Gemini is for future review and Meta AI, Grok, DeepSeek are evaluation candidates only. Reconcile obsolete Chat-mode, paid-pilot, product-stage and migration descriptions across languages.

- [`0.2_2026-10-26_beac897`](./0.2/0.2_2026-10-26_beac897.md) — Add About > Compatibility > Available AI agents in English, Korean and Chinese. Support capable ChatGPT/Claude desktop apps; list Gemini for future support review and Meta AI, Grok and DeepSeek as evaluation candidates only.

- [`0.2_2026-10-26_ecadf63`](./0.2/0.2_2026-10-26_ecadf63.md) — Add a clearly visible support note immediately below the Start introduction in English, Korean and Chinese: use capable ChatGPT or Claude desktop apps; Gemini is currently unsupported. Describe unverified guide/execution support without inventing a Google GitHub-blocking policy. Website navigation and copy checks passed (4 tests).

- [`0.2_2026-10-26_2b581a3`](./0.2/0.2_2026-10-26_2b581a3.md) — Require ChatGPT desktop Work/Codex or Claude Desktop with working file and preview tools; Gemini (including desktop) and AI web apps are officially unsupported. Synchronize English, Korean and Chinese guides, website prompts, and the required host-readiness gate.

- [`0.2_2026-10-26_ac2c85a`](./0.2/0.2_2026-10-26_ac2c85a.md) — Implemented dedicated CBC server consent, block/order persistence, exposure/choice storage, withdrawal, protected results, real/test CSV and archives through additive migration 009; verified with synthetic participants in real local PostgreSQL and desktop/mobile browsers.

- [`0.2_2026-10-26_a4ad99e`](./0.2/0.2_2026-10-26_a4ad99e.md) — Implemented CBC CSV/Excel import, Python/browser parity, descriptive design checks and a standalone computer/mobile preview for the v0.3 preview line; live CBC collection remains disabled.

- [`0.2_2026-10-26_b3edd07`](./0.2/0.2_2026-10-26_b3edd07.md) — Close the supported v0.2 scope, correct stale verification/randomization guidance, and recheck the existing closed-study screen in four languages.

- [`0.2_2026-10-26_e10197b`](./0.2/0.2_2026-10-26_e10197b.md) — Complete the basic one-person Prolific paid connection test; approval and reward payment are explicitly researcher-confirmed.

- [`0.2_2026-10-26_4e977e4`](./0.2/0.2_2026-10-26_4e977e4.md) — Record the first server-side survey end time and preserve it across retries; leave historical timestamps and answers unchanged.

- [`0.2_2026-10-25_f2afa11`](./0.2/0.2_2026-10-25_f2afa11.md) — Keep the established Vercel/Supabase journey, prefer existing authorized official connections, and make Onboard your agent optional.


- [`0.2_2026-10-25_15d4d3e`](./0.2/0.2_2026-10-25_15d4d3e.md) — Fix untouched required sliders and conditional follow-up expressions; use the same browser screen for local checks and deployment.

- [`0.2_2026-10-25_7beafe4`](./0.2/0.2_2026-10-25_7beafe4.md) — Verify the first-researcher website → questionnaire → browser → results → archive journey with a disposable local database and synthetic responses.

- [`0.2_2026-10-25_0af2387`](./0.2/0.2_2026-10-25_0af2387.md) — Complete standard Prolific ID capture, isolated repeat Preview, atomic withdrawal erasure, protected results/CSV and routine-review evidence handling.
- [`0.2_2026-09-10_c4a8405`](./0.2/0.2_2026-09-10_c4a8405.md) — Responsive browser checks and native export stabilization.

- [`0.2_2026-09-09_fcb3c86`](./0.2/0.2_2026-09-09_fcb3c86.md) — stabilized exports, structured results, and integrity checks
- [`0.2_2026-09-09_236d2a3`](./0.2/0.2_2026-09-09_236d2a3.md) — fit the NPS scale to mobile width
- [`0.2_2026-09-09_9d9ffe9`](./0.2/0.2_2026-09-09_9d9ffe9.md) — advanced controls and confirmation-first custom controls
- [`0.2_2026-09-09_2f20a8c`](./0.2/0.2_2026-09-09_2f20a8c.md) — responsive matrices, media stimuli, conditional fields, and navigation policies
- [`0.2_2026-09-09_e770a9c`](./0.2/0.2_2026-09-09_e770a9c.md) — require joint citation of greedyQ and surveydown for scholarly use
- [`0.2_2026-09-09_5ce7a3a`](./0.2/0.2_2026-09-09_5ce7a3a.md) — preserve the desktop canvas when previewing on a phone
- [`0.2_2026-09-09_40c5053`](./0.2/0.2_2026-09-09_40c5053.md) — complete all survey columns in filtered CSV exports
- [`0.2_2026-09-09_825f6fb`](./0.2/0.2_2026-09-09_825f6fb.md) — protected results dashboard and two-link Vercel deployment
- [`0.2_2026-09-09_3aefdd0`](./0.2/0.2_2026-09-09_3aefdd0.md) — secure Supabase connection handoff prepared before account access
- [`0.2_2026-09-09_ee423e6`](./0.2/0.2_2026-09-09_ee423e6.md) — release provenance and required question-authoring choice
