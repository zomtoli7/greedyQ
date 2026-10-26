# Preview a choice-based conjoint design

[한국어](./CBC(kor).md) · [简体中文](./CBC(zh-CN).md)

CBC lets people choose between combinations of features, such as two course subscriptions with different prices and support. **The v0.3 preview can now read a design table, check it, and show working computer and mobile screens. This standalone file sends no responses; the separate [CBC collection path](./CBC-COLLECT.md) supplies server-backed storage and results.** Existing v0.2 surveys remain supported.

## Start with your AI

Say: “I want a choice-based conjoint study. Help me choose attributes and levels, or give me a blank table to fill. Then check the returned table and show both previews.” The AI must first offer AI-assisted design, a blank CSV/Excel table, or an existing design. It must not silently choose the design, fill missing cells or change your methodological decisions.

Use the [blank Excel workbook](./drafts/v0.3/cbc/templates/cbc-design-template.xlsx), or the [two CSV templates](./drafts/v0.3/cbc/templates/README.md). Excel has two sheets named `Attributes` and `Design`; keep the headings on the first row. Replace placeholder attribute headings with your confirmed attribute IDs. Keep codes such as `001` as text. Use only values: formulas, macros, outside links and merged cells are rejected. An empty template needs to be filled before previewing.

## Try the complete example without installing anything

Download [cbc-preview.html](./drafts/v0.3/cbc/golden-reference/cbc-preview.html) using GitHub's download button, then open the saved file in a modern browser. GitHub's source-code view does not run HTML. Everything needed for this example is inside the file; no Python, Node, Vercel or Supabase account is required. A modern Chrome, Edge, Firefox or Safari with Web Crypto and DecompressionStream support is needed for Excel import. If a browser cannot read Excel, use the two CSV files.

The fictional example compares online-course plans: four attributes, two blocks, four tasks per block, two ordinary alternatives plus “neither”. It demonstrates software behavior, not a statistically efficient or approved research design.

For your own table, choose `study.design.json` plus either one XLSX or both CSV files, then press “Check and preview”. Ask the AI to prepare the JSON from your confirmed decisions; you do not need to write it yourself. CSV headings and codes must match the settings exactly. The AI should explain errors before proposing corrections and obtain approval for design changes.

## What you can review

- Computer and mobile panes are independent virtual respondents. The computer layout stays wide even when the preview is opened on a phone; the mobile pane stays at most 390 pixels wide.
- One block is selected per virtual respondent, using the confirmed positive integer weights. Task and alternative orders are randomized once when enabled and retained through answers, Previous and reload. A new virtual respondent starts again. “Neither” stays last.
- Mobile compares two alternatives in a compact grid. More than two alternatives use stacked profile cards to avoid sideways scrolling. The layout may affect comparison and must be reviewed by the researcher.
- Next without a choice shows a message above the task and focuses that task. “Neither” is an explicit choice; an unanswered task is never treated as “neither”.
- “View structure” shows every block for researcher inspection. Block selectors are preview tools, not participant features.
- Download each virtual respondent's preview CSV. It includes presented alternatives, displayed positions, selected values, design version/hash and presentation state. Unanswered choices stay blank. None rows have blank feature codes. Only visited tasks appear; this is synthetic browser data, not live research data or a full population dataset.
- Reload restores this browser's local session when storage is available. Different design hashes use separate sessions. Private browsing, clearing storage or changing files may prevent restoration; this is not a cloud backup.
- “Withdraw preview” removes that pane's local answers and orders, leaves only a withdrawn marker and disables its CSV. It does not delete an already downloaded file. Start a new virtual respondent to try again.

Structure details include level frequencies, unused levels and within-task overlaps. These are descriptive counts, not statistical approval. Attribute IDs must not reuse export metadata names such as `chosen`, `block_id` or `design_sha256`.

## Collecting responses

The self-contained preview still sends no responses. The separate [CBC collection path](./CBC-COLLECT.md) now implements server storage, consent, withdrawal, protected results and real/test long CSV. It has local PostgreSQL/browser verification; fresh cloud deployment and paid CBC acceptance remain pending. Mixed QMD authoring, native CBC export and statistical inference are not enabled.

## Fixed implementation for agents

Use `greedyq/cbc.py` as the Python reference, `web/greedyq-cbc.js` as the platform-neutral browser implementation, and `templates/browser/cbc-preview.html` as the fixed preview template without rewriting them per study. Only confirmed settings and input tables vary. Browser users do not run the Python reference. The browser core has no Node dependency or external library/network download.

For developers/agents with Python:

```sh
python3 -m greedyq cbc-validate drafts/v0.3/cbc/golden-reference
python3 -m greedyq cbc-build drafts/v0.3/cbc/golden-reference
# Optional: read a values-only workbook instead of the two CSV sources.
python3 -m greedyq cbc-build path/to/study --workbook path/to/design.xlsx
```

The build emits `cbc-preview.html`. The browser can then check other local CSV/XLSX files directly. The normalized `0.3-preview.1` model is deterministic across Python and JavaScript; SHA-256 covers content and ordering rules, not raw ZIP formatting. Input settings remain `0.3-draft.1` with `fielding_approval=false`; do not mistake this for permission to collect responses. See the [specification](./drafts/v0.3/cbc/spec.md) and [verification record](./docs/cbc-preview-verification-2026-10-26.md).

Questions or bug reports: [greedyQ project contact](./CONTACT.md). Study participant contacts remain the research team's responsibility.
