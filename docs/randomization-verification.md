# Randomization implementation and verification

[한국어](./randomization-verification(kor).md)

Date: 2026-09-10. Working-tree update based on release `0.2_2026-09-10_c4a8405`; not a newly published release or a claim that existing cloud deployments were upgraded.

## Changes

- Replaced least-count allocation with independent weighted simple draws and randomly permuted fixed blocks. Python, browser, and PostgreSQL implement the same contract.
- Added approved within-page question shuffling with fixed anchors, persistent order, validator diagnostics, and explicit export limitations.
- Added server-registered plans, additive migration 004, protected future block schedules, test/real isolation, rollback-safe draws, a browser/server contract check, and serialized browser saves.
- Included assignment metadata and page ordering in results/archives. Updated canonical guides, bilingual user documentation, connection diagnostics, all three bundled examples, registries and artifact hashes.

## Local evidence

The full Python suite contains **145 tests**, including real PostgreSQL integration tests, Python/JavaScript parser/compiler/validator comparisons, SQLite persistence, archive and deployment regression checks. The Node suites contain **23 tests**, including actual headless Chrome interaction at 390px and 1280px. Final checks are repeated after synchronization; they are not checks against a live Supabase project.

Specific scenarios exercised:

- Independent simple draws (a repeated condition is permitted), unequal weights, two/three arms, exact complete-block totals, and wide statistical sanity bounds.
- 40 concurrent PostgreSQL assignments, 16 concurrent retries of one participant, and eight browser tabs sharing 40 simulated assignments.
- Repeated browser tests exposed lost updates with shared localStorage. Replaced shared HTTP-preview state with IndexedDB transactions, isolated file-preview tabs, and reran concurrent draws. This is a tested correction, not a claim that Web Locks alone make localStorage transactions atomic.
- No assignment before consent or before valid required answers; no stimulus display before the assignment response.
- Separate test/real schedules; saved method/block/draw metadata; refresh, back navigation, retries and process restart.
- Withdrawal does not reuse consumed block slots; failed database writes roll back both the assignment and its block position.
- Question permutations preserve fixed anchors and answers; revisiting/resuming preserves order; the database rejects altered orders and clears them on deletion.
- Old server contracts are rejected; mocked connected-browser saves are serialized. Real database tests use pgcrypto, RLS/grants, and the canonical migration SQL.
- Registration retry/change/legacy-record checks, canonical bundle copying, migration checksums, and both golden-study preflights.

The distributions are sanity tests, not a proof of random-number-generator quality. Statistical tests use deliberately broad bounds to avoid ordinary sampling variation causing failures.

## Reproduce

```sh
python3 -m unittest discover -s tests -q
node --test tests/cloud_lifecycle.cjs tests/randomization_browser.cjs
python3 -m greedyq preflight examples/complete-study
python3 -m greedyq preflight examples/simple-satisfaction-study
git diff --check
```

The development environment needs Python and Node. PostgreSQL tests use `GREEDYQ_PG_BIN` (defaulting to the local Homebrew PostgreSQL 17 path), create a private temporary cluster with Unix sockets and TCP disabled, and stop it afterward. Browser tests use Playwright and Chrome in the agent's environment. These are development requirements, not researcher/participant requirements. Preview still needs only a capable modern browser. If those tools are unavailable, a skipped test is not equivalent to passing it.

## Remaining external acceptance

No existing study was migrated, relabeled, reopened, or deployed during this update. Apply 004 and register the reviewed model in an approved test environment, deploy the matching runtime, and verify direct test completion and CSV records. Experiments with previous least-count assignments require a new study ID. Follow [the upgrade contract](../RANDOMIZATION.md) before applying this to any existing/shared database. The prior three-migration live acceptance remains historical evidence only.

Answer-option shuffling, whole-page shuffling, multiple assignment stages, stratification, variable block sizes, cluster assignment, and native Surveydown equivalence for these features are not claimed.
