# External return links

<!-- GREEDYQ_DESKTOP_POLICY -->
**greedyQ requires an installed desktop AI app for creating or modifying studies. AI web apps are officially unsupported.** Download ChatGPT desktop or Claude Desktop from the official provider. Gemini is not officially supported, including its desktop app. Use an agent-enabled mode that can read the complete guide, create real files and run the canonical preview; installing an app or paying for a model alone does not establish these capabilities. Ordinary desktop chat without these tools is not a supported authoring route. Participant surveys, computer/mobile previews and the researcher results page still run in a web browser. [Supported authoring environment](SUPPORTED-ENVIRONMENTS.md).
<!-- /GREEDYQ_DESKTOP_POLICY -->

[한국어](./EXTERNAL-RETURNS(kor).md)

Ask your AI: “After the completed response is saved, show a return button. Keep it inactive in preview. Forward only the approved participant reference from the incoming link.”

Configure a terminal outcome in `greedyq.yml`:

```yaml
outcomes:
  complete:
    page: complete
    lifecycle_state: completed
    redirect: https://example.org/return
    redirect_label: Return to the study provider
    redirect_params:
      participant: PARTICIPANT_ID
    redirect_newtab: false
```

`redirect_params` is an explicit output-name → incoming-URL-name mapping. Values are URL-encoded, not interpolated as code. Unlisted incoming parameters and questionnaire answers are not forwarded. Missing/empty/repeated mapped parameters prevent navigation. Credential-like parameter names, non-HTTPS destinations, URL credentials, dynamic fragments and duplicate fixed query keys are rejected.

Omit `redirect_params` for a fixed URL. Optionally set `redirect_delay: 5` to navigate after five seconds in the same tab. Omit delay for a click-only button. A new tab requires a click and cannot combine with delay. Record researcher approval for the destination and any identifier transmission before fielding.

Browser previews never navigate externally, including when a delay is zero. Connected respondents get an enabled return button only after terminal state is saved. A failed save keeps the return disabled. This is not a Prolific account connection or a verified completion-credit workflow; those require a later end-to-end panel test.

Native Surveydown export emits return buttons but omits automatic timers in its safe preview. Dynamic parameter handling and save-before-return need verification in the target R runtime. The export report states this limitation.
