# Fresh account connection test

[한국어](./fresh-account-connection-test(kor).md)

Date: 2026-09-10. Runtime: `0.2_2026-09-10_c4a8405`.

## Verified

- New Vercel account `zomtoli-3542`, team `dong-soo-kim01`; existing account resources were not reused.
- Researcher approved Vercel device login and Supabase Marketplace terms.
- Supabase Free resource `greedyq-fresh-account-test` was provisioned in `icn1` and connected to `greedyq-fresh-results`. Vercel synchronized credentials automatically.
- All three canonical migrations executed successfully over certificate-verified TLS; seven greedyQ tables exist. The official Supabase dashboard source identifies its CA download at `https://supabase-downloads.s3-ap-southeast-1.amazonaws.com/prod/ssl/prod-ca-2021.crt`.
- Public survey: https://greedyq-fresh-survey.vercel.app
- Protected results: https://greedyq-fresh-results.vercel.app
- Results protection explicitly uses `ssoProtection.deploymentType = all`. The initial `all_except_custom_domains` setting left the production alias accessible; this was corrected before inserting test responses. Unauthenticated results HTML and API requests now return a login redirect (302).
- Canonical JavaScript backend passed session creation, consent-gated writes, stable assignment, save/resume, invalid capability rejection, and anonymous session-listing checks against the new database.
- One synthetic completed Direct/Test session with three answers is retained for dashboard inspection. The deployed authenticated results API reports one Test/Direct session and zero production sessions.

## Boundaries and follow-up

The deployed survey is an isolated complete-study test fixture with direct entry and test mode. It is not approved for real recruitment. Runtime files were copied unchanged; only embedded study/deployment configuration was adjusted. No secret was placed in public assets. The results deployment alone receives database secrets.

This run verified deployed HTTP/API behavior, not interactive browser rendering or a full participant click-through. The researcher should test both links; real recruitment, Prolific and full cross-device acceptance remain separate steps. Deployment names called “production” by Vercel do not change the study's test classification.

Local orchestration and private credentials are outside the repository at `/tmp/greedyq-fresh-connect.vRL9tI`; do not publish that directory. It contains the isolated deployment bundles and synthetic check scripts, not a finished reusable onboarding implementation. Vercel CLI generated an automation protection-bypass credential for authenticated API testing; it must remain private.
