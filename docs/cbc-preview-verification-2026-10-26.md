# CBC import and preview verification — 26 October 2026

[한국어](./cbc-preview-verification-2026-10-26(kor).md)

## Implemented scope

Python reference (`greedyq/cbc.py`) first, then matching browser-native JavaScript (`web/greedyq-cbc.js`) and the fixed single-file computer/mobile preview. CSV and values-only XLSX import produce normalized `0.3-preview.1` models. Public live profiles and the stable survey format remain v0.2; this is an isolated v0.3 preview implementation, not a live CBC rollout.

Golden design: four attributes, twelve levels, two blocks, eight tasks, sixteen ordinary profiles. Default normalized design SHA-256: `1ebf1ff0ac5890af59a46987099f7b8e58934e9ae868b1dee21ac2d4ae3990bc`. This differs intentionally from the earlier planning manifest hash, which represented a different draft structure. Original source CSVs and earlier synthetic fixtures were preserved.

## Executed checks

- `tests/test_cbc_import.py`: Python CSV, inline/shared-string XLSX equivalence; actual blank workbook; incomplete/duplicate/unknown codes; repeated profiles; invalid counts/weights/order modes; reviewed prohibitions; non-ASCII labels, quoted commas/newlines, BOM/CRLF, leading-zero IDs; hashes; metadata-column collisions; integral JSON number parity; unsafe archives, formulas, external links, macros, DTD/entities, merged cells; source path confinement; safe self-contained HTML; CLI failure does not leave an output.
- `tests/cbc_browser.cjs`: browser CSV/XLSX results exactly equal Python, including SHA-256; rejected workbook variants and actual blank template; matching errors; unanswered versus explicit none; export fields and chosen rows; independent desktop/mobile answers; required-message focus; back/reload/order preservation; completion; downloaded CSV; withdrawal clears local choices/orders and persists a minimal marker; structure dialog; import failure hides stale preview; no outbound HTTP requests.
- Responsive dimensions: 320, 390, 900 and 1280 pixels. The computer pane keeps a wide layout inside its own scroll frame; mobile stays at most 390 pixels, with no horizontal page scroll. Two-alternative comparison grid and three-alternative mobile cards, none disabled, escaped hostile text, keyboard selection and design-hash session isolation were exercised.
- Interface messages checked in English, Korean, Simplified Chinese and Traditional Chinese. Authored attribute/level labels are retained, not machine-translated silently.
- Existing Python and browser regression suites rerun after source and release regeneration; see commit-associated update history for final counts.

A real browser test caught file-input intrinsic width overflowing the 320-pixel page; fixed with bounded grid children. Import review caught attribute IDs overwriting response metadata in CSV; such IDs are now rejected. No test-only bypass was added to production code.

## Limits and remaining acceptance

Browser UI tests run in headless installed Chrome on macOS. This is not evidence of every browser version, touch device or assistive technology; unsupported XLSX decompression reports an error and offers CSV. Local storage can be unavailable or cleared. Downloaded CSVs are not erased by withdrawing the local virtual respondent.

No live CBC schema/RPC, consent pipeline, cloud results integration, real/test authorization or native surveydown CBC export was installed or verified. No Prolific study was published, paid, or edited. No Vercel/Supabase participant records were read or changed for this work. Statistical balance, efficiency, estimability, power and estimator validity remain separate researcher/statistical checks.

## Project contact synchronization

`greedyq.contact@gmail.com` was checked against the public site's About → Project → Contact content at `https://sites.google.com/view/greedyq` (greedyq.org destination). English/Korean/Chinese contact and guide sources now point to it. Existing website contact content was retained. This work prepares repository sources only and does not claim Google Sites was republished. Individual study participant/ethics contacts are not replaced by this project address.


Final regenerated-release result: **221 Python + 50 Node/browser tests passed (271 total), zero failures and zero skips**. Dedicated CBC coverage is 16 Python and 8 browser tests, plus 3 project-contact checks. The [machine-readable record](./cbc-preview-verification-2026-10-26.json) records the release and source commit.
