# Repeat-user cloud journey: verified behavior

[한국어](./repeat-user-acceptance(kor).md)

## Product scope

- Finish: close collection, download real/test CSV and private ZIP, confirm storage, pause dedicated services.
- Temporary interruption: choose whether to close collection only or pause services too. Service **Resume project** does not reopen collection.
- Reopen collection: separately approve the exact study; the agent checks outstanding data requests and calls the canonical reopening operation. Keep previously collected responses.
- Next study: reuse the account, create a distinct study ID and dedicated database/survey/results projects, copy questionnaire definitions if desired, never copy past responses by default.
- ZIP is for retention and analysis. ZIP-to-database restoration is **not a required feature or a pending completion criterion**.

## Live acceptance evidence

The original `greedyq-fresh-account-test` produced a verified archive with 2 test sessions, 16 answers and 2 assignments. After researcher-assisted Supabase Pause/Resume and agent-operated Vercel pause/unpause, all seven table counts matched the archive. Existing/new response writes remained blocked. Vercel results authentication remained enforced. Resume initially reported `Initializing`; the agent waited until database access worked before restarting Vercel. Do not equate clicking Resume with readiness.

With that project paused, another Supabase Free resource was successfully created in Seoul using the same account. It was then connected to `greedyq-next-results`, with a new `greedyq-repeat-satisfaction-test` model and separate survey project. Canonical TLS setup, all three migrations and repeated migration execution passed on the new database. No paid upgrade or old data import was used.

The new study passed real backend checks for create, pre-consent write rejection, save/resume, collection closure, rejection of new/existing writes, explicit reopening, successful write after reopening, and reclosure. The final state is closed. Real Chrome at 390px and 1280px verified welcome → consent → eligibility without a save-error banner. This browser check covers that segment, not a full questionnaire completion. Full-response backend fixtures test storage separately. Test rows include incomplete browser attempts; never count them as real respondents.

- New survey: https://greedyq-next-survey.vercel.app
- New protected results: https://greedyq-next-results.vercel.app
- Original protected results: https://greedyq-fresh-results.vercel.app

Both databases remain active after acceptance, and both studies' collection is closed. Do not advertise another free slot without checking current account limits. No resource was deleted. The public survey can load but a closed study may display the generic unavailable/save-error message; a dedicated end-of-study screen is not yet implemented.

## Canonical operator actions

Follow [cloud lifecycle instructions](./cloud-lifecycle.md). Provision with explicit account/region and free-plan approval; inspect before retries. Use `prepareDeployments`, never regenerate the runtime. Apply results protection to **all** deployments/aliases before deploy, and check both public denial and authenticated API retrieval.

For collection reopening, use `node tools/archive_study.cjs reopen PRIVATE_CONFIG.json`. Use the same verified `studyId`, `approvedStudyId`, `model`, `targets` and private database environment as snapshot, plus `"approveReopen": true` only after a separate researcher decision. Resume Supabase first, wait for a verified connection, resume Vercel, then reopen collection only when explicitly requested. The existing archive remains a historical snapshot; create a new archive after collecting more responses.

Supabase Marketplace provisioning did not grant management pause/resume permission in this account. Therefore this journey is verified with **researcher-assisted Supabase Pause project / Resume project**, not unattended one-login automation. Keep this approval boundary visible; do not request secrets in chat or substitute deletion. Vercel pause/resume is automated through its scoped CLI/API. A future authorized management connection can use the existing provider adapter for pause; do not claim it was available here.
