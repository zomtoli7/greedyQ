# Connect a Supabase Project

> **Recovery guide:** The normal greedyQ flow provisions Supabase through Vercel and does not ask the researcher to use this page. Follow these manual steps only when automatic provisioning is unavailable or being diagnosed. See the [Results Dashboard guide](./RESULTS-DASHBOARD.md).

[한국어](./SUPABASE-SETUP(kor).md)

**greedyQ release:** `0.2_2026-09-10_c4a8405`
**Current state:** ready for account creation; no external project connected

This page begins where local questionnaire testing ends. You do not need database knowledge. The AI should handle one step at a time and keep the survey in test mode until every connected test passes.

## Already prepared

- Ordered setup files: `001_initial.sql` through `006_withdrawal_preview.sql`; apply all six without rewriting previously applied files.
- Browser code for secure session creation, saving, resume, stable assignment, Prolific duplicate detection, and withdrawal deletion
- A browser-native connection tester that uses synthetic data only
- A static deployment bundle requiring only the project URL and publishable/anon key
- Automated checks for missing RPCs, browser-visible privileged credentials, and incomplete deployment files

## What to do after creating the project

1. Create one new Supabase project for testing.
2. Choose its region according to the approved data-location policy. Do not guess if IRB or institutional policy has not resolved this.
3. In the SQL editor, run [`001_initial.sql`](./examples/complete-study/supabase/migrations/001_initial.sql) once.
4. Run [`002_browser_rpc.sql`](./examples/complete-study/supabase/migrations/002_browser_rpc.sql) second.
   Then run [`003_results_dashboard.sql`](./templates/supabase/003_results_dashboard.sql), [`004_randomization.sql`](./templates/supabase/004_randomization.sql), [`005_prolific.sql`](./templates/supabase/005_prolific.sql) and [`006_withdrawal_preview.sql`](./templates/supabase/006_withdrawal_preview.sql) in order. Have the connected agent register your reviewed study model with `registerStudy(client, model)`; the public browser key cannot perform this privileged step. See [upgrade restrictions](./RANDOMIZATION.md). The separate synthetic connection-test model is provisioned by 004 automatically. Migration 006 handles new withdrawal erasure and private repeat-test grants; it does not delete historical responses.
5. Copy the project URL and **publishable key** or legacy `anon` key. Never copy a service-role key or database password.
6. Give those two public browser values to the AI and approve inserting them into the test survey's `greedyq-deployment` block in `index.html`.
7. Open `supabase-connection-test.html`, enter the same two values, and select **Run all connection tests**.
8. Require every test to pass before discussing Vercel deployment.

## Required results

The tester must confirm synthetic session creation, rejection of a wrong capability token, stable assignment, consent-gated save and resume, duplicate synthetic Prolific participant blocking, prevention of anonymous response listing, withdrawal deletion, and test-session cleanup. It uses `is_test = true`; these rows are excluded from analysis. Never use real participant identifiers.

## Browser-safe values

Only the project URL and publishable/legacy anon key belong in respondent-facing files. Never place a `service_role` key, database password, Supabase account access token, private API key, or signing secret in the repository, survey folder, browser, chat attachment, Vercel client configuration, or screenshots.

## Stop conditions

Keep local mock mode if a migration or connection test fails, the region is not approved, a privileged key was exposed, consent rules remain unresolved, or the project contains unrelated production data. A successful test is not approval to deploy or recruit.

## Message to use when you return

```text
I created the Supabase test project. Help me connect it using SUPABASE-SETUP.md. Keep the survey in test mode, use only synthetic participant data, ask before transmitting the project URL or publishable key, and do not deploy to Vercel or recruit participants.
```
