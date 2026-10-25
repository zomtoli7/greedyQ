# Google Sites editing handoff

[한국어](./google-sites-handoff(kor).md)

Read `google-sites-plan.md` beside this file first. The current versioned website sources and complete replacement embed are under `website/`; their release/history come from `release.json` and `updates/0.2/`. Open `website/copy-embed.html` for the single-copy replacement workflow. Generating or pushing these files does not itself save or publish an edit to Google Sites. Do not replace an existing checkout with a partial handoff bundle.

## Current owner decisions

- Google Sites is the chosen host, using a personal Google account.
- Public address: https://sites.google.com/view/greedyq
- The owner reports that greedyq.org already forwards to the site. Preserve that setup; do not change DNS or require a new domain mapping.
- The owner reports that the local task has successfully accessed the editor. Continue using that local task's authorized browser, not a remote filesystem path.
- Inspect existing pages before editing; preserve existing content. Draft editing and automatic saving are authorized. Do not click Publish, change sharing, or alter the domain without separate approval.

## Work scope

Use the plan and bundled English/Korean guides to prepare a nontechnical, task-oriented website draft. Read the compatibility audit before writing feature claims. Preregistration is draft-file delivery only, not OSF integration. Do not promise complete Surveydown parity. Verify public gallery links before embedding; never embed private results or real responses. Present the draft for owner review, with a list of pages changed and remaining checks. If a needed source is missing, identify it rather than inventing its contents.
