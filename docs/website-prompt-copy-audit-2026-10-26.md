# Website prompt-copy audit — 26 October 2026

[한국어](./website-prompt-copy-audit-2026-10-26(kor).md)

## Reproduction and diagnosis

The researcher pasted a Korean website prompt into Gemini and Claude. Newlines disappeared in the receiving text: `START-HERE.md` joined the following `새 연구...`, producing `START-HERE.md새`. The canonical GitHub and raw URLs themselves returned HTTP 200. Original source strings contain actual LF newlines; this is a cross-application copy/paste boundary failure, not proof that the repository is private or Gemini cannot read public repositories. We did not instrument the reporter's OS clipboard or re-run a live Gemini session, so we do not attribute the rich-text flattening to one particular client implementation.

The old renderer relied on newline-only separation and tried legacy `execCommand` before plain-text Clipboard API. Those assumptions were fragile. The replacement preserves normal line breaks but also remains intelligible after all LF characters are dropped.

## Implemented safeguards

- Shared `box`/`promptText` formatting applies to every generated example prompt, not only the Korean Start page. Normalize CRLF, Unicode line separators and nonbreaking spaces; remove invisible zero-width/BOM separators.
- Keep literal ASCII spaces on both sides of internal lines. Enclose prose URLs in `<...>` so an adjacent sentence cannot become part of the address even when line breaks disappear.
- Copy with `navigator.clipboard.writeText` first. On failure, a dedicated `copy` handler writes only `text/plain` from the fallback textarea. Manual selection within a prompt also copies only `text/plain`, avoiding a rich HTML alternative with different whitespace semantics.
- If both automatic paths are blocked, retain the visible selection/manual-copy fallback and truthful status; never claim the clipboard was written.
- Treat BibTeX as code and preserve its exact content, indentation and braces; do not insert prose URL delimiters into citation syntax. Preserve the existing gallery, images, translations and site navigation.

## Exhaustive browser audit

`tests/website_prompt_copy.cjs` visits Start, every Guide and About page, the dedicated Prolific page and Examples in English, Korean and Simplified Chinese, at 320 and 1280 pixels. It finds **135 rendered copy blocks across the three languages**, then checks each at both widths: **270 exact-copy checks**, including 6 width-specific code-block checks. That is 132 prose prompt blocks plus 3 citation code blocks before repeating widths. All 270 preserve exact copied plain text. Every prose URL remains delimited after LF removal; the known entry URL remains exactly the intended address, and `.md새` cannot be formed at that boundary.

Separate checks force modern clipboard success, modern rejection with legacy fallback, and complete automatic-copy denial with manual selection for all three languages. The existing restricted iframe/manual fallback test is retained. These are real headless Chrome tests of the website; they are not a live Google Sites publication or a Gemini-account retest.

## Publication boundary

`website/google-sites-template.html`, language content, generated `google-sites-embed.html`, copy helper and release/history source are prepared together. Google Sites still needs the new embed saved and published by the homepage Work. A source commit or a generated HTML file is not evidence that the old public site's copy blocks changed. Verify the public site's decoded embed against the prepared SHA-256 after publication, then paste a freshly copied Korean/Chinese prompt and confirm the exact URL separately from the next sentence.


The [audit JSON](./website-prompt-copy-audit-2026-10-26.json) records the release/source, block counts and prepared HTML hash. It deliberately marks public-site verification and live Gemini retesting false until performed.
