# greedyQ Results Dashboard

[한국어](./RESULTS-DASHBOARD(kor).md)

The results dashboard is the researcher's everyday view of collected data. Supabase remains the private storage layer; researchers should not need to navigate its tables or write database queries.

## The two links researchers receive

After a connected deployment succeeds, greedyQ returns exactly two primary links:

1. **Survey link** — the public respondent application.
2. **Results link** — a separate Vercel deployment protected by the researcher's Vercel account.

The survey and dashboard are built from the same versioned study bundle and read or write the same Supabase project. They are separate deployments so the survey can be public without exposing the dashboard.

## What the dashboard shows

The initial dashboard follows the useful parts of the sdstudio Responses view: headline response statistics, response summaries, a data-sheet view, and CSV download. greedyQ adds research-operation information that is needed before and during fielding:

- started, completed, active, screened-out, consent-refused, withdrawn, and technical-error counts;
- completion rate and current-page drop-off distribution;
- direct versus Prolific recruitment source;
- test versus real fielding mode;
- random-assignment counts by condition;
- per-question answer summaries;
- a response-record table; and
- a CSV export of the currently filtered records.

External participant identifiers are deliberately absent from ordinary results. They require a separate, more restricted workflow.

## Test responses are never analysis responses

Each session stores two independent classifications:

| Field | Values | Meaning |
| --- | --- | --- |
| `is_test` | `true`, `false` | Whether the response was created before real fielding was enabled |
| `respondent_source` | `direct`, `prolific` | How the participant entered the survey |

A direct test is therefore `is_test = true` and `respondent_source = direct`. A Prolific test remains a test. The dashboard opens on **Real responses**, so tests are excluded from counts, summaries, and CSV files unless the researcher deliberately selects **Test responses** or **All responses**.

## One-login deployment experience

The target researcher journey is:

1. Sign in to Vercel.
2. Approve the Supabase resource inside Vercel once.
3. Let greedyQ provision the database, install the migrations, inject environment variables, deploy the public survey, and deploy the protected results application.
4. Receive the survey and results links.

The Vercel Supabase Marketplace integration can create a Supabase project and synchronize its environment variables. The researcher must not copy keys, paste SQL, or use the Supabase table editor in the normal flow.

## Security boundary

The public survey uses only the Supabase URL and publishable key, with capability-token RPCs and row-level security. The results page never contains a Supabase secret. Its `/api/results` server function reads the secret from Vercel environment variables and returns a deliberately limited dataset.

The results deployment must have Vercel Authentication enabled. Do not publish `results.html` and its API as an unprotected production site. A deployment is not ready until an unauthenticated browser is denied and the authorized researcher can load it.

## Researcher walkthrough

1. Open the results link and sign in to Vercel if asked.
2. Leave **Responses** set to **Real responses** during fielding.
3. Use **Test responses** when checking trial submissions made before launch.
4. Use **Source** to compare Direct and Prolific traffic without changing the test filter.
5. Select **Refresh** after submitting a response in another tab.
6. Check **Where participants stopped** for unexpected drop-off.
7. For an experiment, verify that **Conditions** is reasonably balanced and investigate large discrepancies before continuing recruitment.
8. Review answer summaries for broken choices or unexpected values.
9. Select **Download CSV**. The file contains only the currently selected response mode and source.

## Required acceptance test

Before fielding, greedyQ must create at least one direct test response, save answers, refresh the dashboard, and confirm that the counts and answer summary change. It must then repeat the check through a complete Prolific test URL when that module is enabled. Real-response mode must remain empty during these tests. Database rows alone are not sufficient evidence; the researcher-facing dashboard must show the update.

The current v0.2 dashboard is an operational review surface, not a statistical analysis package. Researchers should use the filtered CSV export with their approved analysis workflow.
