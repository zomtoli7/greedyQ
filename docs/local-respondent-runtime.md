# Local Respondent Runtime

[한국어](./local-respondent-runtime(kor).md)

The local runtime tests the same respondent behaviors required before connecting a study to Supabase and Vercel. It uses server-rendered pages, an HttpOnly session cookie, and a local SQLite database.

```bash
python3 -m greedyq run examples/complete-study
```

Open `http://localhost:4180/study`. Each new browser cookie creates an anonymous test session. Successful page transitions save answers; refreshing or reopening the page resumes the current session.

Implemented test behavior:

- consent acceptance or refusal is recorded before research answers;
- required questions and numeric limits are enforced by the server;
- partial responses and the current page persist across refreshes;
- simple/fixed-block conditions are assigned atomically and remain unchanged;
- screening, completion, refusal, and withdrawal become terminal states;
- deletion-on-withdrawal removes answers and assignments in one transaction;
- conditional questions update in the browser and are checked again by the server;
- the browser cannot choose its experimental condition or next page.

Test data is stored at `STUDY_DIR/.greedyq/runtime.sqlite3` by default and is ignored by Git. Use `--database PATH` to select another local database and `--port PORT` to change the port.

This is not a production runtime. It binds only to localhost and does not implement Supabase authentication/RLS, Vercel deployment, external respondent identifiers, production redirects, encrypted secrets, operational monitoring, or analysis export. Do not recruit real participants with it.
