# First-researcher usability audit — 25 October 2026

[한국어](./first-user-usability-2026-10-25(kor).md)

This is a scripted researcher/participant simulation, not a study with novice human researchers or a cross-model GPT/Claude evaluation. Start with the public website’s prompts and instructions, create a separate synthetic Direct study, then exercise the canonical browser runtime, database RPCs, results handler and archive operations together. The paid Prolific pilot and its deployments, accounts, settings, responses and budget were not changed.

## Journey and evidence

| Researcher action | Verification |
| --- | --- |
| Open Home → Start and copy the starting prompt | English/Korean/Chinese; 320px restricted iframe; denied clipboard permission falls back to selecting the complete prompt for manual copying. |
| Choose researcher-written questions | Opening and ending pages build with no invented questions; two researcher-supplied questions are then added in the given order. |
| Review an AI-assisted synthetic questionnaire | Six imaginary sessions: two completed, one consent refusal, one eligibility exclusion, one withdrawal, one incomplete. This tests artifacts and behavior, not another hosted AI’s reasoning. |
| Download and open a draft | `file://` preview and source-file studio at 320/390/1280px; no Python, Node or local server in the researcher’s browser path. Invalid replacement source hides the obsolete preview. |
| Respond, change an answer and refresh | Canonical session-capability RPCs on a disposable local PostgreSQL database with migrations 001–007; refresh resumes; cleared conditional answers disappear from database/results/CSV. |
| Open results | The actual results API and dashboard read local database records. Real and Prolific views exclude all six Direct tests; Test/Direct shows them. Study and question labels are readable. |
| Download CSV | Parsed with Python’s CSV reader: six filtered rows, all question columns, multilingual quoted/multiline text, empty hidden answers and no withdrawn research answers. Formula-like text is protected. |
| Close collection and archive | Actual transactional close/snapshot and actual ZIP creation/checksum verification. Archive has zero real rows and six test rows, including the incomplete record; exact original text remains in `data.json`. An already-open participant receives the closed-study message. |
| Confirm download, then pause | A fake provider receives no calls before download confirmation. After confirmation it receives exactly the two survey/results pause operations and the database pause. No external project is paused. |
| Reopen the same study | Wrong study approval is rejected; the authorized local reopening restores writes. ZIP-to-database restoration remains outside scope. |

## Corrections made

- **Conditional answer persistence:** the UI cleared hidden answers while earlier database saves retained them. Additive migration `007_answer_snapshot.sql` makes a newly accepted complete snapshot remove omitted answers in that session, under the existing lock and capability/consent checks. It does not bulk rewrite historical records. Migrations 001–006 remain unchanged.
- **Results and CSV:** identify the study and show authored question/page labels; explain empty views; prevent stale asynchronous responses from replacing newer filters; disable download while updating or after failure. Export UTF-8 with spreadsheet-safe text, expand custom-base structured answers, and disambiguate question IDs that overlap metadata columns.
- **Downloaded source preview:** preserve a desktop-width frame on a phone, constrain the phone frame, show a plain-language result, make diagnostics optional, and hide stale previews when a rebuild fails. Preview has a no-network connection policy and preview-only timing.
- **Closed collection:** a running survey recognizing the canonical database closure now explains that collection is closed rather than blaming the participant’s connection. Paused hosting can still show the provider’s unavailable page.
- **Consent reference examples:** display their existing versioned participant information in the actual questionnaire; a local Markdown document reference was not a readable consent screen. Placeholder contacts remain explicitly fictional.
- **Guides:** explain ZIP extraction, file-tool/account-tool requirements, empty test/real views, private panel identifiers in CSV/ZIP, complete versus filtered downloads, confirmation before pause, and starting or resuming another study. Synchronize English/Korean documents and the three website languages.

## Reproduce

Run `python3 -m unittest discover -s tests -v` and the Node test files using `node --test`. The complete local journey is `PostgresRandomizationTests.test_first_researcher_browser_results_and_archive_journey`, invoking `tests/first_user_journey.cjs`. Dashboard race/error/export coverage is in `tests/results_usability_browser.cjs`; restricted-iframe website coverage is in `tests/website_browser.cjs`. These are agent/developer checks; the researcher does not install this toolchain.

Final pre-release regression: **176 Python tests and 38 Node/browser tests passed, with no skips**. The release metadata and generated artifacts are checked again after stamping.

## Remaining external boundary

Migration 007 and these runtime changes have local evidence. Existing cloud studies need their own approved migration/rebuild/registration/deployment review; a repository or website update does not upgrade a live survey. In particular, do not change the pilot while Prolific reviews it. Genuine paid submission matching, approval and payment remain pending. Local fake-provider checks do not establish current account permissions, billing limits, Vercel Authentication behavior or provider pause/resume on another account. Previously recorded live acceptance remains evidence for the version tested at that time.
