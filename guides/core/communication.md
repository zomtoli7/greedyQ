# Researcher Communication Contract

Communicate with the user in the user's language, regardless of the language of this specification. Confirm participant-facing language separately.

<!-- GREEDYQ_DESKTOP_POLICY -->
**greedyQ requires an installed desktop AI app for creating or modifying studies. AI web apps are officially unsupported.** Download ChatGPT desktop or Claude Desktop from the official provider. Gemini is not officially supported, including its desktop app. Use an agent-enabled mode that can read the complete guide, create real files and run the canonical preview; installing an app or paying for a model alone does not establish these capabilities. Ordinary desktop chat without these tools is not a supported authoring route. Participant surveys, computer/mobile previews and the researcher results page still run in a web browser. [Supported authoring environment](../../SUPPORTED-ENVIRONMENTS.md).
<!-- /GREEDYQ_DESKTOP_POLICY -->

[한국어](./communication(kor).md) · [简体中文](./communication(zh-CN).md)

The default audience is a researcher who may have no software knowledge.

## Participant language checkpoint

Before drafting participant-visible content, ask which language participants should see. Keep the researcher's conversation language separate. If Chinese is requested, confirm Simplified (`zh-CN`) or Traditional (`zh-TW`); do not guess from the conversation. Record the confirmed choice as `greedyq.language` in QMD. Built-in participant UI packs currently support `en`, `ko`, `zh-CN`, `zh-TW`. Explain unsupported languages rather than silently using English.

Translate and have the researcher review all authored content: title, team name as appropriate, pages, consent, questions, choices, validation messages, custom hints, button labels, image descriptions, media transcripts/captions, and terminal/return wording. Changing the language flag does not translate these strings. Do not translate IDs, stored values, conditions, URLs, or response data. A later language change requires explicit review of translations, not a new research design. Test empty, invalid, loading/failure, completion and refusal screens as well as ordinary pages. Browser-owned date pickers and media menus follow browser/OS settings and must not be promised to follow the survey language. Researcher preview tools and results dashboards have a separate interface language scope.

## Say this, not the implementation detail

- “I checked the survey structure” instead of “schema validation passed.”
- “Participants cannot reach the completion page” instead of “the route graph has an unreachable terminal.”
- “I still need your decision about eligibility” instead of “an unresolved decision blocks generation.”
- “The preregistration draft must be updated because the survey changed” instead of “the artifact hash no longer matches.”
- “The live survey link has not been tested yet” instead of “deployment verification is pending.”

Use research terms when they help the researcher make a decision. Define unfamiliar terms briefly. Do not expose internal file lists, hashes, schema names, validation codes, or deployment mechanics unless requested or necessary to explain a failure.

At the end of a work period, report only: what the researcher can review now, decisions still needed, anything that prevents a safe launch, and the single recommended next action. Put exhaustive technical evidence in the internal validation report.
