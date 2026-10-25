# Compatibility verification — 2026-09-10

[한국어](./compatibility-verification-2026-09-10(kor).md)

Local working-tree verification, not a published release or live-cloud certification.

## Verified changes

- Documented Surveydown choice/matrix-row shuffling with selected positions, fixed anchors and persistent stored orders. Question and restricted independent-page ordering remain separate greedyQ extensions.
- Browser answer autosave, reload/back navigation, conditional visibility/page skipping, stop checks and escaped inline formatting.
- Terminal HTTPS returns with explicit parameter mapping; preview cannot navigate externally, and a failed save prevents a connected return.
- Server validation rejects altered saved presentation orders. Synthetic PostgreSQL tests use temporary local databases, not researcher accounts.
- Official OSF template inventory: 29 fields including metadata. English/Korean draft files preserve unresolved decisions; no OSF login or submission.
- Draft upgrade creates a separate copy, preserves the original, excludes known deployment secrets and rebuilds pinned runtime files. Production upgrades require separate review.

## Evidence

The full Python suite passed 155 tests. The combined JavaScript/cloud-lifecycle/browser suites passed 26 tests with no failures or skips. Actual Chrome tests cover 390px and 1280px widths, ordering persistence, answer restoration and external-return safety. All three reference examples rebuilt and exported; both study preflight checks passed. Whitespace validation passed.

Commands: `python3 -m unittest discover -s tests -q`; `node --test tests/cloud_lifecycle.cjs tests/randomization_browser.cjs tests/ordering_browser.cjs`; `python3 -m greedyq preflight <study>`; `git diff --check`.

## Remaining limits

Read the [feature-by-feature audit](./surveydown-compatibility-audit.md). Some settings, unrestricted R/Shiny reactivity and matrix-wide answered semantics remain incomplete or non-equivalent. Native R export has not been certified by running the target stack. A passing local suite does not establish complete Surveydown compatibility.

No Vercel/Supabase migration, deployment, Prolific setup, OSF submission, Google Sites publication or DNS change was performed. Migration 004 and the corresponding model/runtime require approved rollout. The [Google Sites plan](./google-sites-plan.md) lists the editing access and domain information needed next. The current release identifier was not advanced to a nonexistent commit.
