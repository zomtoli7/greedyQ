# Publish the public start page on Netlify

[한국어](./NETLIFY-START(kor).md)

This is a project-maintainer setup, not an account required from researchers. The public, script-free start page is generated from `START-HERE.md` and its Korean/Chinese counterparts. The full operational workflow is in `INITIALIZE.md` and its required modules. Markdown and HTML use one source; do not maintain separate copies of instructions.

## Connect the repository once

In the signed-in Netlify team, choose **Add new project → Import an existing project → GitHub**, authorize access to `zomtoli7/greedyQ`, and select that repository. Use these settings:

| Field | Value |
| --- | --- |
| Project name | `greedyq-start`, if available; otherwise an assigned name is fine |
| Production branch | `main` |
| Framework preset | Other / no framework |
| Base directory | Empty, repository root |
| Build command | `python3 tools/build_bootstrap.py --output dist/bootstrap` |
| Publish directory | `dist/bootstrap` |
| Environment secrets | None |

The committed `netlify.toml` supplies the build/publish settings. Publish only after the files are pushed. Make the project publicly readable without sign-in or a password; some teams default to private visibility. No custom domain is required. Copy the actual assigned public `https://…netlify.app/START-HERE.html` URL after deployment; do not guess it. This does not deploy a survey, access a database or change existing Vercel projects.

## Verify before changing website prompts

Open the assigned URL without signing in. Its text must include `greedyq-start-bootstrap-1`, the desktop support condition, `INITIALIZE.md` and the saved-study continuation guidance. Check English/Korean/Chinese pages, working language links, phone layout and readability with JavaScript disabled. Check `bootstrap-manifest.json` and its actual file hashes. The build pins initialization links to Netlify's exact Git `COMMIT_REF`, not a changing main branch.

Ask Gemini to report the reading-check marker and supported apps, without creating a study. Success proves only that this page was readable in that session. It does not establish provider-wide domain policies or restore Gemini support. A failed read must not be reported as successful setup.

Only after the real URL and publication are verified should the main website's copied requests be shortened and redirected to this public front door. Keep one short fail-closed sentence: if the guide cannot be read, stop and report it. Never publish a guessed Netlify address.

## Saved studies

The public entry routes the researcher; it does not replace a study's saved lock or history. Resume an authoring folder/ZIP at its pinned guide/runtime and verify matching hashes. A metadata stamp can postdate its source commit, so the source commit alone is not enough to reconstruct every locked file. Use the complete matching snapshot or stop and discuss an approved upgrade copy. Never silently upgrade an active survey. A closed-study data archive remains analysis/storage material, not an online-service restoration package.

## Local maintainer checks

After committing the source, run `python3 tools/build_bootstrap.py`. Only the dedicated `dist/bootstrap` directory is public output. The builder refuses unrelated nonempty output folders and a `COMMIT_REF` different from the checked-out commit. It copies no survey responses, private study records, credentials or full repository. `robots.txt` permits crawling but cannot guarantee any AI provider will read the page.

References: [Netlify repository deployment](https://docs.netlify.com/start/quickstarts/deploy-from-repository/), [build/publish configuration](https://docs.netlify.com/build/configure-builds/overview/).


Local preparation verification: 241 Python tests passed. The website navigation/copy checks passed (4 tests), and the static start page was readable with JavaScript disabled in all three languages at 320/1280px, with working language links and no page overflow. A source-document language-pair check now scopes to tracked Markdown; generated public Markdown/HTML have separate direct parity/link tests. Live Netlify setup, assigned URL, Gemini reading and homepage prompt replacement are still pending.
