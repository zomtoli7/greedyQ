# greedyQ Guides

<!-- GREEDYQ_DESKTOP_POLICY -->
**greedyQ requires an installed desktop AI app for creating or modifying studies. AI web apps are officially unsupported.** Download ChatGPT desktop or Claude Desktop from the official provider. Gemini is not officially supported, including its desktop app. Use an agent-enabled mode that can read the complete guide, create real files and run the canonical preview; installing an app or paying for a model alone does not establish these capabilities. Ordinary desktop chat without these tools is not a supported authoring route. Participant surveys, computer/mobile previews and the researcher results page still run in a web browser. [Supported authoring environment](../SUPPORTED-ENVIRONMENTS.md).
<!-- /GREEDYQ_DESKTOP_POLICY -->

[한국어](./README(kor).md) · [简体中文](./README(zh-CN).md)

These guides are modules of the greedyQ **agent-executable application specification**. greedyQ itself is not an agent: a capable host GenAI resolves this specification to instantiate the greedyQ research agent.

## Default: start from the repository

- Share <https://greedyq.netlify.app/> for normal use. The AI loads the core, one study profile, and only the capability modules required by the study through `registry/guide-index.json`.
- Use `greedyq-guide.md` only as the self-contained fallback when the chat cannot read repository links. It embeds the Preview UI specification plus the canonical preview, database, deployment, and state-schema bundle.
- `greedyq-guide-compact.md` is a legacy conversation aid and is not sufficient by itself for deterministic artifact generation.
- Use `examples/complete-study/` as a reference, not as content to copy into an unrelated real study.

Start with: “Let's build a survey.” The guide instructs the model to detect capabilities, resume existing state when present, and ask one research question at a time.

## Static golden-reference walkthrough

This is a design-time inspection of expected behavior, not a completed GPT/Claude behavioral evaluation.

| Scenario | Expected guide behavior | Fixture result |
| --- | --- | --- |
| Fresh conversation | Detect mode and ask only for the research question | Defined in guide startup protocol |
| Single attachment | Extract canonical code from the full guide and verify hashes | Embedded canonical bundle in `greedyq-guide.md` |
| Resume reference study | Read the current phase, open decisions and approvals | Represented by `.greedyq/study-state.json` |
| Ask to submit OSF draft | Deliver draft files only; researcher registers independently | Preregistration module |
| Ask to launch recruitment | Require preregistration and deployment gates | Fielding gate is blocked |
| Change target sample | Append a superseding decision and stale affected hashes | Required by decision and manifest contracts |
| Add arbitrary R | Reject execution and offer declarative or export-safe alternatives | Prohibited by guide and v0.2 specification |
| Claim deployment succeeded | Require external verification evidence | All external operations remain `not_attempted` |

The structural fixture passes JSON Schema validation, decision-reference checks, artifact-hash checks, QMD reference checks, and English/Korean documentation parity. The Python reference parser, validator, preview, and local respondent runtime now exercise the documented reference behavior. Browser-native JavaScript conformance and selected cloud paths have test evidence; see the current external-readiness record for exact scope. This is not a guarantee for another account, arbitrary model or new deployment.

## Next behavioral evaluation

Run the full and compact guides independently with at least GPT and Claude on:

1. recreation of the complete reference study from a short brief;
2. resume from the saved `.greedyq` state;
3. correction of intentionally invalid IDs, routing, and consent timing;
4. refusal to invent an unresolved sample size or submit an unapproved preregistration; and
5. consistent generation of QMD, YAML, state, and preregistration artifacts.

Score question pacing, decision fidelity, methodological escalation, syntax validity, state resumability, correction success, and external-action truthfulness.

Simplified Chinese entry, user and AI guides use `(zh-CN).md`. English normative files, code and hashes remain canonical; participant language is confirmed separately. Prefer an existing official Vercel connection while keeping Onboard your agent optional.

## CBC preview and project contact

For choice-based conjoint tables, see [CBC import and computer/mobile preview](../CBC.md). This v0.3 preview does not enable live CBC collection; keep using the supported v0.2 Simple/Experiment paths for collection. For project questions or bug reports: [greedyq.contact@gmail.com](../CONTACT.md). Individual studies must provide their own research-team contact.
