# Local Respondent Runtime

[한국어](./local-respondent-runtime(kor).md)

Use the canonical browser runtime for all participant screen checks:

```sh
python3 -m greedyq run examples/complete-study
```

Open `http://localhost:4180/index.html`. This serves the same fixed JavaScript renderer used by the dual preview and deployment. With mock mode enabled, responses stay in browser test storage and are not sent to a researcher. Use `python3 -m greedyq preview PATH_TO_STUDY` for desktop and mobile panes together. `--port` changes the local port; `--database` is no longer supported by `run`.

Python remains the independent parser, validator, compiler and backend-state reference for development. Its internal `Store` and legacy server are tested independently, but their old server-rendered form is not a participant UI conformance test or a substitute for reviewing the canonical browser. Database behavior is separately tested with disposable PostgreSQL and canonical RPC migrations. A local mock test does not verify a real Supabase/Vercel connection.

Create a new draft with `python3 -m greedyq init NEW_FOLDER --id study_id --profile simple --language en`. Opening and ending pages, pending review records, seven migrations and static deployment files are included; questions and approvals are not invented. `preflight NEW_FOLDER` checks the local package and reports warnings. `preflight NEW_FOLDER --stage deployment` also blocks mock mode and pending deployment decisions/approvals. Even a passing check does not establish a live connection. Do not recruit participants from a local test server.

When the configured candidate lives in a separate directory, use `preflight PATH_TO_STUDY --stage deployment --deployment-index PREPARED_SURVEY/index.html`. Keep the original preview in mock mode; the check also verifies the candidate contains the current validated model.
