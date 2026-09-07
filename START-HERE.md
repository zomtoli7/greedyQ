# Start greedyQ

[한국어](./START-HERE(kor).md)

Use this file as the entry point when a researcher asks you to create, modify, or fork a greedyQ survey. Speak to the researcher as a nontechnical end user. Do not turn repository loading, validation, or file generation into their problem.

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

For modification, summarize the existing study in plain language and ask what the researcher wants to change. For a fork, first create an independent copy according to the core guide, then ask what should differ.

Ask one focused question at a time. Show the interactive participant preview—not an implementation report—as soon as a coherent questionnaire exists.
