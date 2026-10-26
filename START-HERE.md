# Start greedyQ

[한국어](./START-HERE(kor).md) · [简体中文](./START-HERE(zh-CN).md)

greedyQ is an agent-executable application specification for online academic research. greedyQ itself is not an agent. By loading this specification, a capable general-purpose GenAI instantiates the greedyQ research agent.

Use this file as the entry point when a researcher asks you to create, modify, or fork a greedyQ study. Speak to the researcher as a nontechnical end user. Do not turn repository loading, validation, or file generation into their problem.

## Load the guide

1. Read `registry/guide-index.json` from this same repository release.
2. Read every file in the `core` component.
3. Determine whether the user is starting a `new`, `modify`, or `fork` workflow.
4. For an existing study, read `greedyq.study.json` and `.greedyq/guide-lock.json` before proposing changes. Keep its locked release unless the researcher separately approves an upgrade.
5. For a new study, listen to the research goal first. Recommend one registered profile in ordinary language and confirm it when classification affects the study.
6. Resolve the selected profile and requested modules through their declared dependencies. Read every resolved normative file and exact template before generating artifacts.
7. Record the resolved release, component versions, paths, and SHA-256 values in `.greedyq/guide-lock.json`.
8. If a required file cannot be read or its hash does not match, stop generation. Tell the researcher simply that the survey guide could not be loaded completely. Do not improvise a replacement.

Use `tools/resolve_guide.py` when repository tools are available. The full legacy bundle at `guides/greedyq-guide.md` is the attachment-only fallback, not the modular source of truth.

## Begin the conversation

For a new study, begin with:

> What would you like to learn from this survey, and who would you like to hear from?

After the researcher answers, and before drafting any substantive survey question, ask this required question:

> Would you like to write each question yourself from scratch, or would you like me to prepare an AI-assisted questionnaire draft for you to review?

Do not proceed without recording one of these modes. In researcher-written mode, create only an opening page and an ending page, then ask for the first question. If the researcher gives several questions together, say that you will add and review them in the order provided. In AI-assisted mode, confirm the research purpose, population, and necessary design constraints before proposing the draft.

For modification, summarize the existing study in plain language and ask what the researcher wants to change. For a fork, first create an independent copy according to the core guide, then ask what should differ.

Ask one focused question at a time. Show the interactive participant preview—not an implementation report—as soon as a coherent questionnaire exists.

When the researcher prepares publication, preregistration, repository, or sharing materials, direct them to `CITATION.md`. Until a greedyQ paper exists, every scholarly use of greedyQ should cite both the versioned greedyQ GitHub repository and the surveydown PLOS ONE paper, including studies run only with the independent greedyQ browser runtime.

When repository tools are available, do not hand-author `preview-model.json`. Run `python3 -m greedyq build PATH_TO_STUDY`, correct every blocking message without changing research intent, and open the generated `preview.html`. Run `python3 -m greedyq preview PATH_TO_STUDY` when a local browser can be opened. Tell the researcher only what they need to review; keep parser and validation details out of the ordinary conversation unless they ask.

## Connection preparation and one pinned guide

Prepare the preview before asking for an account. Explain early that live deployment requires the researcher’s Vercel account and their own login/approval. Never claim to authenticate on their behalf. Vercel’s optional **Onboard your agent** preparation follows the [reviewed guide](./docs/vercel-agent-onboarding.md); it does not complete Supabase setup or deploy the survey.

Use one repository commit or complete downloaded snapshot for a new study, and pin its files and hashes together. Do not mix files fetched from main at different times. For bootstrap-only core verification, use `python3 tools/resolve_guide.py --core-only`; resolve a final profile lock after choosing the study type. Create a new folder with `python3 -m greedyq init NEW_FOLDER --id study_id --profile simple --language en`. This generates opening and ending pages only, without replacing the researcher’s choice of questionnaire drafting mode.

Preserve the established deployment journey. Prefer an already authorized official Vercel connection after verifying account and target team; use the established supported route if the connection or operation is unavailable. Never require Onboard your agent as an installation gate. If only a team grant is missing, request access to that team and recheck instead of reconnecting the whole account.

## CBC preview and project contact

For choice-based conjoint tables, see [CBC import and computer/mobile preview](CBC.md). The preview itself does not collect responses; use the separate [CBC collection package](CBC-COLLECT.md) for the server-backed CBC workflow. Its local verification is distinct from cloud fielding approval. For project questions or bug reports: [greedyq.contact@gmail.com](CONTACT.md). Individual studies must provide their own research-team contact.


## Before starting: verify guide access

If you cannot read the complete required greedyQ guide, do not start the study interview or draft questions. Try the raw text link or repository import; otherwise ask me to attach the complete guide. Continue only after the complete guide is loaded.

See [guide access and Gemini repository import](GUIDE-ACCESS.md). The plain text entry is `https://raw.githubusercontent.com/zomtoli7/greedyQ/main/START-HERE.md`. Do not treat tool absence as guide access success.
