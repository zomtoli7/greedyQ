# Preregistration draft files

[한국어](./PREREGISTRATION(kor).md)

Ask: “Prepare an OSF preregistration draft from our confirmed decisions. Ask me about missing decisions one at a time. Do not log in to OSF or submit anything.”

greedyQ delivers English and Korean Markdown drafts for download, with original confirmed answers preserved in their supplied language. An AI can translate those answers only with researcher review. Internal JSON and source hashes support traceability; they are not a registration or an approval.

The current field list is maintained in `greedyq/osf_fields.py`. On 2026-09-10 we checked the [official OSF-linked offline form](https://docs.google.com/document/d/1gkN0Jp6Gu7GIA4Ne4YCDZ61nCLQRgt32moRdUg9AnVg/edit), reached from [OSF Support](https://help.osf.io/article/330-welcome-to-registrations). It contains 29 response fields including metadata. This is not the older short template often described online.

The draft covers metadata; questions/hypotheses and data foreknowledge; study type, causal interpretation, blinding, design and randomization; collection procedures, sample counts, justification and start/stop rules; manipulated/measured/derived variables; models, transformations, inference, exclusions, missing data and other analyses; and additional context. Optional fields remain visible. Confirm “not applicable” when appropriate rather than silently omitting a section.

## Workflow

1. Confirm whether a preregistration draft is wanted. It is not necessary just to preview a questionnaire.
2. Review each field with the researcher. Never invent sample counts, power calculations, hypotheses, data-access claims, blinding or approvals. Distinguish synthetic preview data from observed research data.
3. Store approved prose under `preregistration.fields` using the published field identifiers. Leave missing fields marked TO CONFIRM.
4. Generate with `python3 -m greedyq preregister STUDY_FOLDER` in agent/development environments. The researcher need not install Python.
5. Download the Markdown draft. The researcher handles registration independently if needed. greedyQ does not request OSF credentials, create registry projects, submit registrations, choose embargoes, or verify registry state.
6. If the design changes, revise a new draft and compare it with the retained prior draft. Do not rewrite a previously approved record silently.

The MIT license of greedyQ does not determine the license of the researcher's registration. A complete draft is still unregistered. There is no automatic “ready to submit” or recruitment authorization.
