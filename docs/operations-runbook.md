# Local Operations and Recovery Runbook

[한국어](./operations-runbook(kor).md)

This runbook covers every check that greedyQ can complete before an external account is connected. Researchers should not normally run these steps themselves; the connected AI agent performs them and reports only actionable results.

## Before connection

1. Validate and build the study, then run the full regression and real-browser E2E suites.
2. Confirm desktop, 390px mobile, 320px narrow-mobile, conditional, terminal, resume, withdrawal, and structured-answer paths.
3. Generate the preregistration draft and native Surveydown export. Parse generated `app.R` with R when available.
4. Run deployment preflight. It verifies required browser files, server-only secrets, RLS/withdrawal contracts, ordered migration names, and every migration checksum recorded in `supabase/migrations/manifest.json`.
5. Keep the study in test mode. A production switch is a material fielding action and requires the exact reviewed survey, resolved consent/privacy decisions, required preregistration gate, successful live persistence test, and explicit researcher approval.

## Migration recovery

- Never edit a migration that has already been applied. Add the next numbered migration.
- Rebuild after a migration change so `manifest.json` records the new ordered files and SHA-256 values.
- A checksum mismatch means the deployment bundle changed after it was prepared; stop and rebuild.
- Apply migrations in numeric order and record the deployed release identifier. Re-running canonical migrations must be tested on a disposable project before being used as recovery.

## Data recovery and retention

- Keep test and production responses separated by `is_test`; never relabel tests as research data.
- Backups, retention length, and deletion schedules are researcher decisions. Record them before fielding.
- A withdrawal/deletion test must show that answers, assignments, and external identifiers are removed atomically while a non-identifying lifecycle event remains.
- Exported CSV files are snapshots. Record the study release, filter, export time, and data dictionary with analysis files.
- Never claim restoration or deletion succeeded without checking the resulting database state and researcher dashboard.

## Connection-ready evidence

The local package is ready to request external connection only when automated tests pass, generated artifacts match their manifests, both golden studies pass preflight, no secret appears in browser artifacts, and the remaining items explicitly require live Vercel, Supabase, Prolific, OSF, or native Surveydown execution.
