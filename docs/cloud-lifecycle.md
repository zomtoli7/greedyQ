# Cloud setup and archive operator contract

[한국어](./cloud-lifecycle(kor).md)

Use the canonical `tools/cloud_lifecycle.cjs` module unchanged in the agent's environment. Researchers approve decisions; they do not operate these commands. Never upload private working directories, `.env` files, archive files or management tools to Vercel.

## Setup lessons promoted to reusable code

`onboardingCommands({team,name,region})` returns Vercel CLI argument arrays, not shell strings. Confirm `whoami` and team, inspect existing installations/resources to avoid duplicates, and use the explicitly approved region and free plan. A terms-required response is a user checkpoint, not a provisioning success. Re-inspect the resource before retrying an uncertain create. Wait for availability and synchronized environment variables; initial linking can finish before credentials arrive.

Connect the Supabase resource only to the results project, which receives server secrets. Pull credentials privately. `databaseClient(pg.Client, POSTGRES_URL)` downloads the official CA, removes conflicting connection-string SSL options, and verifies TLS. `migrate(client,migrationDirectory)` checks migration checksums and records applied files transactionally for idempotent retries. An old database without this ledger requires explicit reconciliation; do not blindly rerun the original CREATE TABLE migration or claim it is up to date.

`prepareDeployments({repo,model,directory,url,publishableKey})` creates separate allowlisted survey/results bundles from canonical templates. It accepts a publishable key only. Apply returned results protection (`ssoProtection.deploymentType=all`) **before deployment**. Confirm unauthenticated access is denied on every results alias and API, including the stable production alias. Protecting only preview URLs is insufficient. Only the survey project may have protection disabled. Verify Test/Direct saves, zero change to real counts, resume and access boundaries before handoff. Do not silently change the research model or its test/production mode.

## Archive execution

Before using a new runtime, apply 001–008 and call `registerStudy(client, model)` for every reviewed study. This registration is mandatory even for a nonexperimental survey. See [randomization and upgrade requirements](../RANDOMIZATION.md). Do not apply 004 to an active shared database without registering its other studies and coordinating a maintenance window; the new save boundary fails closed for unregistered studies. Older acceptance records describe the version tested at that time, not automatic validation of this upgrade.

The agent needs Node, the `pg` package, and Python for the archive writer in its own environment. No extra software is required on the researcher's machine. Tests can use injected provider/database adapters without external accounts.

Run `node tools/archive_study.cjs snapshot PRIVATE_CONFIG.json` with `POSTGRES_URL` and `SUPABASE_URL` in a private process environment. Configuration:

```json
{
  "studyId": "study-id",
  "approvedStudyId": "study-id",
  "model": "/private/study/preview-model.json",
  "output": "/private/archives/new-unique-directory",
  "targets": {
    "team": "team_exact",
    "survey": "prj_survey",
    "results": "prj_results",
    "supabase": "exactprojectref"
  }
}
```

Verify the model belongs to the deployed study, exact resource IDs and database credentials refer to the same project, and all other linked apps/empty studies have been inventoried. `closeAndSnapshot` installs per-study write guards, drains concurrent writes using table locks, closes the study and reads all seven data tables in one transaction. It does not use the dashboard's limited/paginated API. If the transaction fails, it rolls back. If local file generation fails afterward, collection remains closed: retry export, never silently reopen. The private snapshot enables offline recovery of the ZIP writer. Closure blocks inserts/updates/deletes, including online withdrawal; arrange a researcher contact path and separately authorized maintenance for later requests.

`greedyq.archive.make_archive` writes and rereads a ZIP, checks content hashes, splits real/test CSV, keeps incomplete responses and historical question IDs, and preserves structured values in JSON cells. The operator CLI also creates separately downloadable CSV files. Downloading these private files is not authorization to send them to a third-party AI or public host. Keep original study files/media separately: this is not a full SQL/Storage restore backup.

After the researcher confirms saving the archive and explicitly approves pausing these exact projects, run `node tools/archive_study.cjs pause PRIVATE_CONFIG.json`. The second configuration contains:

```json
{
  "archivePath": "/private/archives/new-unique-directory/study-archive.zip",
  "expectedHash": "sha256-returned-by-snapshot",
  "approvedStudyId": "study-id",
  "downloadConfirmed": true,
  "exclusiveResources": true,
  "resourceOwnershipReviewed": true,
  "freePlanReviewed": true,
  "linkedProjectsReviewed": true,
  "targets": {
    "team": "team_exact",
    "survey": "prj_survey",
    "results": "prj_results",
    "supabase": "exactprojectref"
  }
}
```

These booleans are records of real approvals/reviews, never defaults to fill automatically. `VERCEL_TOKEN` and `SUPABASE_ACCESS_TOKEN` must be authorized management credentials; the publishable/service-role database key is not a Supabase management token. In a Marketplace-only account the connected agent may need an additional provider approval. Never request passwords or secrets in chat. If no permitted management route exists, stop at download-ready and guide the human through Pause; no delete/uninstall fallback.

The finalizer rechecks ZIP contents, SHA-256, study/resource binding, sharing evidence and ownership before mutations. It pauses survey, results, then Supabase. It records each requested/verified state in private `pause-events.jsonl`. A timeout or pending asynchronous pause is not success: rerun status verification later; already-paused resources are skipped. Partial failures remain partial, without deletion or automatic resume. Confirm all relevant aliases and direct database writes cannot collect data; verify free-slot availability separately in the provider, never infer it from HTTP success alone.

## Verification scope

Run `python3 -m unittest tests.test_archive` and `node --test tests/cloud_lifecycle.cjs`, followed by the full Python suite. Live closure/reopening and researcher-assisted Supabase pause/resume are now verified; see [repeat-user acceptance](./repeat-user-acceptance.md) for exact coverage and current resource state. Paid-plan behavior, load/concurrency stress and unattended Supabase management authorization are not verified. ZIP restoration is outside required scope. Use **Resume project** for provider resumption, and the separately approved `reopen` CLI operation for collection.

Sources: [Vercel pause](https://vercel.com/docs/projects/managing-projects), [Supabase pause API and permission](https://supabase.com/docs/reference/api/v1-pause-a-project), [Supabase TLS](https://supabase.com/docs/guides/platform/ssl-enforcement).

The established CLI operations route remains supported. Prefer an authorized official Vercel connection after checking account and team for operations it supports; use the established route for missing capabilities with the same approval and acceptance boundaries. Onboard your agent is not required. Verify CLI and MCP credentials independently; resolve denied team access with the specific team grant rather than silently bypassing it with other credentials. Follow the [connection selection policy](../guides/modules/deployment-vercel-supabase/guide.md).
