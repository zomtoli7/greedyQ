# Finish a survey and archive it

[한국어](./ARCHIVING(kor).md)

When a survey is finished, tell your AI:

> This survey is finished. Help me save the responses and archive it so I can start my next study. Do not delete the projects.

## What happens

1. **Confirm the survey.** The AI names the study and account, checks for other studies sharing its services, asks whether recruitment has ended and whether participants still responding should finish first. Ending collection requires your approval.
2. **Close response collection.** The AI closes database writes for that study before taking the final copy. Already-open survey tabs cannot add or change responses afterward. When the running survey detects the database closure, it shows “Survey closed” and removes questionnaire navigation. A paused hosting service can instead show its own unavailable page. Stop distributing the link first.
3. **Download your files.** Receive `responses.csv` (all real responses, including incomplete ones), `test-responses.csv`, and `study-archive.zip`. The ZIP also contains the full question list, exact structured answers, study model, response-source information, consent records and data-request records. Do not assume that “archived” means every response is complete or eligible for analysis.
4. **Confirm safe storage.** Open the CSV, check the row count, and save the ZIP somewhere you control. Keep a second secure copy. The AI waits until you confirm the download; generating a file is not confirmation that you have saved it.
5. **Pause online services.** After your confirmation, the AI pauses both Vercel projects and the dedicated free Supabase project. This does not delete them. The survey and online results page will no longer be usable while paused. Your downloaded data remains available.
6. **Start another study.** Give the AI the repository again or your existing greedyQ folder. Ask for a new study with a new study ID; never overwrite the old responses. Existing authentication may be reusable, but a new resource or permission may still require approval.

The CSV retains every question, even unanswered ones. Structured controls are stored as JSON within a CSV cell in this archive export; the dashboard's flattened-column CSV is a different view. Potential spreadsheet formulas are escaped in CSV, while `data.json` retains exact values. For Prolific records, `PROLIFIC_PID`, `STUDY_ID` and `SESSION_ID` are included in both archive CSV files and the private ZIP; Direct records leave them blank. These are private research files, not anonymized public exports. Do not upload these files to a public repository or public Vercel folder. You may need institutional permission before giving identifiable response files to an AI service.

## Free accounts and retention

Supabase states that paused projects do not count toward its two active free project limit. Its paused-project resumption window is limited; check the current provider policy instead of assuming a fixed retention period. Pausing is **not permanent archiving**. Paid projects cannot simply be paused under the same rules. Account-wide storage, bandwidth, billing and Marketplace eligibility must still be checked; do not promise unlimited surveys or zero charges. [Supabase billing](https://supabase.com/docs/guides/platform/billing-on-supabase), [pausing and resumption](https://supabase.com/docs/guides/platform/free-project-pausing).

Vercel supports pausing projects. Production links then show an unavailable/paused response; do not promise a custom closing page. Preview deployments may have different availability, so the database closure is the authoritative collection stop. Pausing Vercel does not automatically pause Supabase. [Vercel project management](https://vercel.com/docs/projects/managing-projects).

If services are shared, archive the study's files but leave the shared services running. The AI must explain that this does not free a whole database project slot. Never delete a project, uninstall an integration, downgrade a paid plan, or cancel billing as a substitute for pause without separate approval.

## Return later

For analysis, use the downloaded files without restoring the online survey. To reopen collection, ask explicitly; do not assume unpausing the provider removes the study's database closure. A connected agent must review retention and withdrawal requests, reconcile any changes, remove only that study's closure under approval, and verify the survey before distributing it again. Automated restore/import is not implemented. The archive is a research-data package, not a full restorable database backup: it excludes passwords, access capabilities, uploaded media, Storage objects, SQL schema and application source. Retain your original greedyQ folder and media separately.

While collection is closed, ordinary online withdrawal writes are also blocked. Keep the research team's contact route active, handle later withdrawal/deletion requests through an authorized administrator, and update every retained archive copy. Do not interpret the closed snapshot as overriding participant rights or retention obligations.

## Implementation and current test boundary

The agent uses `tools/archive_study.cjs`, `tools/cloud_lifecycle.cjs` and `greedyq/archive.py`. These are operator-side tools; the researcher does not install Python, Node or a database client. See [operator instructions](./docs/cloud-lifecycle.md).

Live testing verified archive creation, provider pause/resume with researcher-assisted Supabase actions, retained data, creation of another free database, and a new survey/results deployment in the same account. See [repeat-user acceptance](./docs/repeat-user-acceptance.md). Marketplace setup credentials alone do not necessarily authorize Supabase Management API pause/resume. If that permission is unavailable, request the specific additional approval or guide the researcher to **Pause project / Resume project**. Do not claim Vercel approval covers every future management operation.

ZIP-to-database restoration is explicitly outside the required product scope. The ZIP is for retention and analysis; resume an existing project for temporary interruptions, or fork the original study folder with a new study ID for the next survey. Never import old responses into a new study by default. Service resume and collection reopening are separate operations: `reopenCollection` requires explicit approval and leaves unrelated studies unchanged.
