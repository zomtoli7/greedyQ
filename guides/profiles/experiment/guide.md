# greedyQExperiment Profile Guide

<!-- GREEDYQ_DESKTOP_POLICY -->
**greedyQ requires an installed desktop AI app for creating or modifying studies. AI web apps are officially unsupported.** Download ChatGPT desktop or Claude Desktop from the official provider. Gemini is not officially supported, including its desktop app. Use an agent-enabled mode that can read the complete guide, create real files and run the canonical preview; installing an app or paying for a model alone does not establish these capabilities. Ordinary desktop chat without these tools is not a supported authoring route. Participant surveys, computer/mobile previews and the researcher results page still run in a web browser. [Supported authoring environment](../../../SUPPORTED-ENVIRONMENTS.md).
<!-- /GREEDYQ_DESKTOP_POLICY -->

[한국어](./guide(kor).md) · [简体中文](./guide(zh-CN).md)

**Object:** `greedyQExperiment`

Use this profile when the study assigns participants, sessions, clusters, stimuli, order, or another unit to conditions and estimates an effect of that assignment.

The profile describes research intent, not a promise that every assignment unit is implemented. The fixed runtime currently supports one respondent-level simple or fixed-block assignment. Explain the distinction and confirm the method, weights, block size when relevant, and timing. Follow [RANDOMIZATION.md](../../../RANDOMIZATION.md); reject unsupported units or multiple stages instead of ignoring them. Selected within-page question shuffling is a separate opt-in feature, with stable recorded order and fixed anchors.

Confirm the research question, primary outcome, hypotheses, assignment unit, conditions, allocation probabilities, timing of assignment, persistence across resume, stimuli, manipulation checks, contamination risks, exclusions, stopping rule, and primary analysis. Never invent a condition, stimulus, hypothesis direction, sample size, exclusion, or analysis commitment.

Randomization must happen once at the declared unit, use a documented source of randomness, persist before condition-dependent content is shown, and remain stable after refresh or resume. Preview controls may force conditions for review but must be visibly separate from respondent controls and must never alter production assignment behavior.

Check that baseline measures precede treatment when intended, treatment-dependent measures follow exposure, hidden answers cannot contaminate analysis, and every condition reaches valid outcomes. Ask the researcher to review every condition in the interactive preview before approving the instrument.

Do not present the fixed assignment methods as the limit of research designs the AI can help develop. For a different requested procedure, confirm intent using the extension process in [RANDOMIZATION.md](../../../RANDOMIZATION.md), and distinguish built-in behavior, additional implementation and unverified work. “Four random groups plus a group-specific stimulus sequence” is an example, not a newly built-in feature. Preserve fixed core files and prepare a versioned study extension with concurrency and resume verification.
