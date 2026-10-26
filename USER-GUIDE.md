# greedyQ User Guide

<!-- GREEDYQ_DESKTOP_POLICY -->
**greedyQ requires an installed desktop AI app for creating or modifying studies. AI web apps are officially unsupported.** Download ChatGPT desktop or Claude Desktop from the official provider. Gemini is not officially supported, including its desktop app. Use an agent-enabled mode that can read the complete guide, create real files and run the canonical preview; installing an app or paying for a model alone does not establish these capabilities. Ordinary desktop chat without these tools is not a supported authoring route. Participant surveys, computer/mobile previews and the researcher results page still run in a web browser. [Supported authoring environment](SUPPORTED-ENVIRONMENTS.md).
<!-- /GREEDYQ_DESKTOP_POLICY -->

[한국어](./USER-GUIDE(kor).md) · [简体中文](./USER-GUIDE(zh-CN).md)

> **Be greedy with your time. Just ask your AI to make your questionnaire.**

This guide takes a nontechnical researcher from an idea to a survey that can be tested on desktop and mobile. Connected deployment requires approval. After collection, use [Finish and archive a survey](./ARCHIVING.md) to download responses and pause dedicated services for your next study.

## What you need

Returning users: see [pause, resume, and start another survey](./docs/repeat-user-acceptance.md). Resume the existing project for an interruption; use a new study ID for another survey. Archived ZIP files are for analysis, not rebuilding the online service.

- An installed ChatGPT or Claude desktop app with working file and agent tools; AI web apps are officially unsupported
- A short description of what you want to learn and whose opinions you want
- Time to answer questions and personally test the result

You do not need to know programming, Markdown, databases, or deployment tools.

## 1. Give greedyQ to your AI

Open the [greedyQ start page](./START-HERE.md), or give your AI this URL:

```text
Read and follow the greedyQ start page. If you cannot read it, stop and tell me:
<https://greedyq.netlify.app/>
```

The AI should read that file and the linked files in the same repository. You do not need to attach every guide and template separately.

## 2. Choose how to start

### Create a new survey

Copy this message:

```text
Read and follow the greedyQ start page. If you cannot read it, stop and tell me:
<https://greedyq.netlify.app/>

Create a new greedyQ study. Treat me as a nontechnical researcher, ask one focused question at a time, and take me through a working desktop-and-mobile preview.

I want to learn: [your question].
I want to hear from: [your intended participants].
```

### Modify an existing survey

Give the AI access to your existing greedyQ study folder, then copy:

```text
Read and follow the greedyQ start page. If you cannot read it, stop and tell me:
<https://greedyq.netlify.app/>

This is an existing greedyQ study. Summarize it in plain language and help me modify it. Preserve its history and current greedyQ version unless I approve an upgrade. Ask one focused question at a time.

I want to change: [your change].
```

This changes the original study. Ask for a plain-language change summary before accepting the result.

### Fork an existing survey

Give the AI access to the existing study folder, then copy:

```text
Read and follow the greedyQ start page. If you cannot read it, stop and tell me:
<https://greedyq.netlify.app/>

Fork this greedyQ study. Preserve the original, create an independent copy with a new study identity, and help me change only the copy. Ask one focused question at a time.

The new version should differ in this way: [your change].
```

Confirm that the AI created a separate copy and did not overwrite the original.

## Returning to a study and preparing to share

- Resume a downloaded draft: “Compare this study with the current greedyQ release. Upgrade a separate copy and show me the changes.” See [safe upgrades](./UPGRADING.md). Your original remains unchanged and your research decisions need not change.
- Shuffle choices: “Shuffle the first four options, but keep Other last.” See [ordering settings](./RANDOMIZATION.md). Page shuffling is available only for independent linear page groups; the AI must explain restrictions before changing your design.
- Prepare registration text: “Give me the OSF draft, with undecided fields clearly marked.” See [draft files](./PREREGISTRATION.md). No OSF login or submission is involved.
- Add a return link: “Save the response before enabling the return button; don't navigate away in preview.” See [external returns](./EXTERNAL-RETURNS.md).
- Ask about compatibility: “Which of my features differ in native Surveydown export?” Read the [current audit](./docs/surveydown-compatibility-audit.md). Not every Surveydown setting or reactive R expression is implemented.

For experiments and randomized question presentation, see [Random assignment and question order](./RANDOMIZATION.md). It explains simple versus fixed-block assignment, includes copyable requests, and describes which questions can be shuffled while preserving their order on resume. Your AI must ask before choosing these settings. The results CSV records both assignment details and presented question order. Existing deployed studies are not automatically upgraded by a repository update.

## 3. Have the guided conversation

The AI should act like a research assistant, not a software engineer. It will ask about the research purpose, intended participants, design, main outcome, recruitment, questionnaire, survey flow, consent and privacy, analysis, and preregistration.

Immediately after you explain what you want to learn and whom you want to hear from, the AI must ask how you want to write the questions:

- **Write them yourself from scratch:** the AI initially creates only the opening and ending pages, then asks you for the first question. You may provide one question or several; several questions are added and reviewed in the order you give them.
- **Ask the AI to prepare a draft:** the AI confirms the purpose, participants, and essential design choices, then proposes a complete draft for your review. You remain responsible for approving every research decision.

The AI must not silently assume the second option merely because it can generate questions.

Near the beginning, it will also ask what participant-visible name should appear at the top of the survey—for example, a company, university, laboratory, or research-team name. This is stored as `greedyq.organization` and can be changed later.

It is fine to answer “not decided yet.” The AI should record an unresolved decision instead of inventing an answer.

After the purpose and broad design are clear, choose whether to complete detailed IRB and consent work now or after the first questionnaire draft. The details may be deferred, but they cannot be skipped before deployment.

The AI may identify wording or research-design concerns. It should explain the concern and offer choices, but it must ask before changing a meaningful research decision.

## 4. Get the interactive preview

Once a coherent questionnaire exists, the AI should create the survey and show the participant-facing preview. If it provides only `study.md` or a technical report, copy:

```text
Follow the greedyQ preview checkpoint. Show me the actual interactive respondent-facing preview with both desktop and mobile views. Do not use an implementation report as the main review surface.
```

The study folder should include at least:

```text
survey.qmd
greedyq.yml
index.html
preview.html
studio.html
greedyq-core.js
greedyq-runtime.css
```

The AI may open the preview, show an interactive artifact, or give you a folder to download. If you receive a ZIP, extract it first. Keep the extracted files together and open `preview.html` in a modern browser. Do not open the HTML from inside the ZIP. If your AI supplies `studio.html` instead, open it, choose `survey.qmd` and `greedyq.yml` from that same folder, and select **Preview questionnaire**. No installation or external service is needed; rebuilding starts fresh imaginary responses.

Preview mode shows desktop and mobile versions, uses imaginary participants, and keeps test responses local. It must not send responses to an external service.

To inspect every supported control in one place, open the [live control gallery](https://zomtoli7.github.io/greedyQ/examples/control-gallery/preview.html). It contains all 16 surveydown-compatible question types, both numeric-slider forms, responsive matrices, navigation policies, and every fixed greedyQ extension including advanced and custom-base examples. The repository copy is available at [`examples/control-gallery/`](./examples/control-gallery/) if the live page has not finished publishing.

Use **View structure** at the top of any preview to inspect the questionnaire before clicking through it. The read-only outline shows pages in respondent order, identifies text blocks with `T`, identifies questions with `Q`, and shows each question ID and control type. Expand or collapse pages to focus on one part of the survey. This view never changes the questionnaire or saves responses.

## 5. Test it like a participant

For every survey:

- Try to continue without answering a required question.
- Use Previous and Continue, then refresh and check that progress resumes.
- Try opt-out, other, and open-text choices.
- Check that hidden questions appear only when intended.
- On a phone, confirm matrices use row cards and two- or three-column groups without horizontal page scrolling.
- Play every audio or video stimulus and inspect its caption or transcript.
- Check every declared hidden, disabled, or delayed navigation action.
- Test completion, consent refusal, screening, and withdrawal routes that apply.
- Confirm both desktop and mobile views are readable and easy to use.
- Confirm the test-state value matches the answer you selected.

For an experiment, also test every condition. Confirm that treatment material appears only in the intended condition, assignment happens at the intended point, and going backward or refreshing does not change the assigned condition.

Describe problems in ordinary language, such as “The choices are hard to read on mobile” or “Selecting No on consent should go directly to the refusal ending.”

## 6. Revise and approve

After giving feedback, copy:

```text
Apply these changes without altering any other research decision. Rebuild and validate the survey, then show the updated desktop-and-mobile preview and a short plain-language summary of what changed.
```

Repeat until you have personally clicked through the survey and are satisfied. A successful validation alone is not your approval.

When ready, say:

```text
I personally tested the desktop and mobile preview and approve this questionnaire version. Record the approval, but do not connect external accounts, submit a preregistration, deploy, or recruit participants yet.
```

## What comes next

After preview approval, greedyQ can prepare a preregistration draft, a Vercel-ready survey, Supabase setup files, Prolific settings, and a native surveydown export. Account connection, deployment, and recruitment each require separate approval and external verification. Preregistration is delivered as files only; researchers submit independently if desired. Continue with [External Connection Readiness](./docs/external-connection-readiness.md).

The agent must complete the [local operations and recovery checks](./docs/operations-runbook.md) before requesting those connections.

## Cite your study software

If the study appears in a publication, preprint, thesis, or report, cite both greedyQ and surveydown—even if the survey ran only on greedyQ's independent browser runtime. Use the exact release identifier stored as `greedyq.version` in `survey.qmd`. See [CITATION.md](./CITATION.md) for copy-ready references and accurate methods wording.

Use [Connect a Supabase Project](./SUPABASE-SETUP.md) only for recovery when automatic setup is unavailable. It is not part of the normal researcher journey.

## 7. Connect once and receive two links

A connected AI agent needs file and account-operation tools to complete this stage. An AI without the required file/preview tools must stop authoring and offer a desktop agent handoff; missing deployment authorization is checked separately. Preview needs no service account.

The normal deployment flow does not ask you to operate Supabase. Sign in to Vercel, approve the Supabase resource presented inside Vercel, and allow the connected AI agent to finish setup. It must install the database migrations, connect environment variables, deploy the public survey, deploy a Vercel-authenticated results application, and verify both links.

The completion message must contain a **survey link** to share with participants and a **results link** for researchers authorized through the Vercel team. Instructions to copy database keys, paste SQL, find Supabase tables, or manually connect environment variables are recovery instructions, not the normal greedyQ experience.

If an official Vercel connection is already available, your AI uses it first. Otherwise it can continue with the established supported connection route. **Onboard your agent is optional, not required.** You should not normally need to install tools or plugins yourself. If an additional team grant is needed, the AI gives you the approval link for that team only. Login and team authorization can be separate steps.

## 8. Check test responses in the dashboard

The results link identifies the study and opens on **Real responses**, which excludes every test submission. An empty real-response view after a trial is expected. If Test responses is also empty after Refresh, ask the AI to check the two links and saved record before recruiting. Select **Test responses**, leave **Source** set to **Direct**, and submit the ordinary test survey once. Select **Refresh** and confirm that the counts, current-page distribution, answer summaries, and response table update.

For a Prolific test, keep **Test responses** selected and change **Source** to **Prolific**. A valid panel identifier never turns a test into an analysis response.

| Mode | Source | Expected use |
| --- | --- | --- |
| Test | Direct | Ordinary connected-database test |
| Test | Prolific | Panel-link and identifier test |
| Real | Direct | Public recruitment without a panel |
| Real | Prolific | Live Prolific recruitment |

**Download CSV** follows the visible filters. Every survey variable remains a column even when the current records did not answer it; missing answers are blank. Matrix rows and advanced structured controls are expanded into stable analysis columns, and **Variable guide** explains those names. See the [detailed Results Dashboard guide](./RESULTS-DASHBOARD.md).

## 9. Finish collection and keep your data

When collection has ended, ask:

```text
Help me finish this study and archive its responses. Check for participants still responding and any shared projects. Confirm which study to close, then give me the real-response CSV, test-response CSV and archive ZIP. Wait until I confirm that I downloaded and safely saved them before pausing services. Do not delete projects.
```

The dashboard CSV contains only its selected filters; it is not the complete archive. Check the archive’s row counts, keep a secure second copy, and retain your original study folder and media separately. After you confirm safe storage, the AI may pause dedicated services under your approval. Shared services stay running. A local practice run tests this sequence without actually pausing Vercel or Supabase. See [the detailed archive guide](./ARCHIVING.md).

To create another survey, give the AI the repository link and request a new study or an independent fork with a new study ID. To continue collecting the same survey later, ask to resume the existing project and reopen collection separately. A downloaded archive is for analysis, not automatic database restoration.

## Common problems

### Recruit with Prolific

Ask: “Connect this reviewed survey to Prolific, prepare a draft and test it before recruitment.” Follow [Prolific setup](./PROLIFIC-SETUP.md). Your AI prepares the survey/ID capture/return paths, while you confirm the study settings and completion actions in your researcher account. Results and CSV keep Prolific IDs alongside answers and separate test responses. Account Preview and real submission/payment checks are separate from local simulation.

For repeated draft testing, open **Repeat Prolific preview** in the protected results page, enter the survey URL and create a private test link. Put that link in the Prolific draft with URL-parameter ID recording enabled. Use **Start a new test** in the survey to try another ending without deleting earlier test responses or changing participant IDs. The link expires after 24 hours and works only in Test mode. Before real collection, remove it and use the reviewed production link.

A successfully saved withdrawal deletes this session's answers and assignment from the active database and removes them from subsequent results/CSV downloads. Minimal panel identifiers and withdrawal status remain for returning to Prolific and preventing duplicate participation; disclose this to participants. Existing downloads and provider backups are outside automatic deletion. See [withdrawal and repeat-preview details](./PROLIFIC-SETUP.md#withdrawal-deletion-and-verification).

Before paid recruitment, replace the repeat-test link with an ordinary Production survey URL and review the real participant task, consent, duration, reward and total cost. A Prolific Preview of that Production URL can create a Real-mode record; use the separate account-free preview for wording review. If Prolific pauses for routine review and says no action is needed, preserve settings and wait for its decision. Stored answers alone do not prove a platform submission or payment. After matching genuine completed work, approve through Prolific and record the agreed retention deadline. See the [complete implementation and evidence summary](./docs/prolific-integration-status.md).

### Survey language

You can work with your AI in Korean while publishing a Chinese survey. At the start, the AI asks for the participant language; for Chinese it confirms Simplified or Traditional. Say: “Keep speaking Korean with me, but make all participant-facing content Simplified Chinese, including errors and buttons.” Built-in UI packs support English, Korean, Simplified Chinese and Traditional Chinese. The AI translates authored content separately and asks you to review it. Changing only the language setting does not translate your questions or consent form. IDs and saved values stay unchanged.

Expert setting: `language: zh-CN` under the QMD `greedyq:` header; use `zh-TW` for Traditional Chinese, `ko` for Korean or `en` for English. Older studies without this setting retain English defaults. Browser-owned date/media menus may still use the device language. Researcher tools are separate from the participant interface; native Surveydown exports require target-language verification.

### Appearance and navigation

Visual design is part of your research. Ask your AI to change supported colors, research-team name, question/choice wording, button labels and navigation. Review computer and mobile previews. Use supported settings rather than rewriting the shared runtime; ask the AI to explain unsupported appearance requests.

- “Use our approved blue for the progress bar and our team name at the top.”
- “Hide Previous on the stimulus page and enable Next after 15 seconds.”
- “Show Previous but disable it here. Rename Next to Continue.”
- “Remove Select all that apply from this question only.”
- “Change that instruction to Choose every service you have used.”

`selection_hint = FALSE` or `selection_hint = ""` removes the multiple-selection instruction; a string replaces it. This greedyQ extension covers checkbox, button, image and multiple-selection matrix templates, including custom variants. Review native export compatibility. Existing navigation settings are `previous_mode`, `next_mode` and `next_delay_seconds`. A delay is not proof of reading; visual changes must not accidentally reveal experimental conditions.

On Next, explanations appear above every invalid question and focus moves to the first. Constant-sum totals use a warning color until the target is reached. Timing shows a faint running clock only in preview. The custom gallery example is an emotion-card variation on single-choice buttons, not a validated psychological scale.

### Other issues

- **The AI cannot read GitHub:** Download and attach the single [full fallback guide](./guides/greedyq-guide.md), then repeat your starting message.
- **The AI is too technical:** Say, “Follow greedyQ's communication rules. Treat me as a nontechnical researcher and ask one focused question at a time.”
- **The AI invents a choice:** Say, “Mark that decision unresolved, restore my last confirmed design, and ask me before deciding.”
- **The preview does not open:** Keep `preview.html`, `greedyq-core.js`, and `greedyq-runtime.css` together and ask the AI to rebuild and locally verify the browser bundle.
- **The AI says recruitment can begin:** A working preview is not deployment or fielding approval. Ask for the remaining consent, preregistration, connection, security, and production-test checkpoints.

## Final checklist

- [ ] I chose new, modify, or fork.
- [ ] The AI loaded the current greedyQ repository instructions.
- [ ] I confirmed important research decisions; undecided items remain visible.
- [ ] I reviewed consent and privacy decisions.
- [ ] I personally tested desktop, mobile, and all important routes or conditions.
- [ ] I approved the exact questionnaire version.
- [ ] No external account was connected and no participant was recruited without separate approval.

## Control reference

Ask for controls in research language; you do not need to remember their code names.

| What you need | greedyQ control | Best used for |
| --- | --- | --- |
| One short written answer | `text` | Codes, brief labels, one-line responses |
| A longer written answer | `textarea` | Feedback and explanations |
| A number | `numeric` | Age, quantity, percentage, or amount |
| One choice | `mc` | Mutually exclusive categories |
| Several choices | `mc_multiple` | “Select all that apply” questions |
| One prominent button | `mc_buttons` | A short, action-like choice set |
| Several prominent buttons | `mc_multiple_buttons` | A compact multi-select set |
| One image choice | `mc_image` | Visual stimuli or image categories |
| Several image choices | `mc_multiple_image` | Selecting multiple visual items |
| A dropdown | `select` | A long category list |
| A labeled slider | `slider` | Ordered named categories |
| A numeric slider or range | `slider_numeric` | A value or bounded interval |
| One date | `date` | A single calendar date |
| A date interval | `daterange` | Start and end dates |
| One response in every row | `matrix` | A standard rating grid |
| Several responses in every row | `matrix_multiple` | A row-by-column multi-select grid |
| Play an audio stimulus | `audio` | A sound clip with optional caption and transcript |
| Play a video stimulus | `video` | A video with optional poster, caption, and transcript |
| Put items in preference order | `rank_order` | Complete ranking of a list |
| Rate parallel versions together | `side_by_side` | Several compact grids sharing items and scales |
| Ask recommendation likelihood | `nps` | A standard 0–10 likelihood scale |
| Record page time | `timing` | Hidden seconds-on-page metadata |
| Allocate a fixed total | `constant_sum` | Budgets, time, or percentage allocation |
| Sort into groups and rank | `pick_group_rank` | Categorization followed by within-group priority |
| Narrow a hierarchy | `drill_down` | Region–country–city and similar paths |
| Confirmed special interaction | `custom` | A carefully agreed extension of a supported base control |

Matrix questions use the familiar survey-table layout on desktop: statements are rows, response choices are column headings, and each cell contains a radio button or checkbox. On a phone, every statement becomes a separate card and response choices are shown in ordered groups of two or three columns, avoiding horizontal page scrolling.

`audio` and `video` are safe greedyQ extensions rather than standalone built-in surveydown question types. They accept validated local or HTTPS media, use native playback controls by default, and do not create response variables. Ask for captions and transcripts whenever the research material permits them.

Page navigation can be shown, hidden, or left visibly disabled. A Next button may also remain disabled for a stated number of seconds when a minimum stimulus-exposure time is part of the approved design. Required unanswered questions alone do not disable Next in advance; clicking it explains what needs an answer.

Always prefer a supported control. If none fits, the AI must warn that a custom control can take more time and AI usage, then ask focused questions until its appearance, interaction, validation, phone behavior, accessibility, and saved result are all confirmed. Implementation begins only after that confirmation and must reuse the closest supported base control.

## Prompt library

These examples are intended to be copied and edited. In every case, begin by asking the AI to follow `START-HERE.md`.

### Draft a plain-language satisfaction survey

```text
Create a short satisfaction survey for people who have used our service at least once. Ask about overall satisfaction, ease of use, usefulness, result quality, intention to use it again, and one improvement. Keep it under three minutes and show me the interactive preview before discussing deployment.
```

### Add an eligibility route

```text
Only people who have used the service may continue. Add one clear eligibility question. People who answer No should reach a polite screened-out ending with no Previous button. Show me that route in desktop and mobile preview.
```

### Add a standard matrix

```text
Add a matrix asking respondents to rate ease of use, speed, reliability, and clarity. Use the columns Very poor, Poor, Fair, Good, and Excellent. Require one response per row. Show the standard table on desktop and separate row cards with no horizontal page scrolling on mobile.
```

### Add a multi-select matrix

```text
For each product category, ask where it was purchased. Put product categories in rows and In store, Online, and Mobile app in columns. Allow more than one selection in each row.
```

### Add audio and video stimuli

```text
Add an audio stimulus with normal playback controls, a short caption, and a transcript, followed by a video stimulus with a poster image and transcript. Use only validated project files or HTTPS URLs. Do not autoplay either item and do not treat playback as a survey response.
```

### Control Previous and Next

```text
Hide Previous on the consent page, show it normally on questionnaire pages, and display it disabled on the final review page. On the stimulus page, keep Continue disabled for 12 seconds and show the remaining time. Demonstrate every state in desktop and mobile preview.
```

### Use advanced controls

```text
Ask respondents to rank five priorities, allocate exactly 100 points across three activities, and then choose a city through region, country, and city drill-down fields. Explain the stored data shape and demonstrate desktop and phone behavior before I approve the questions.
```

### Request a custom control

```text
I may need a custom product-card control. Before creating code, warn me about extra time and AI usage, identify the closest existing greedyQ control, and ask me one question at a time about appearance, selection behavior, validation, mobile layout, accessibility, and exported values. Summarize the agreement and wait for my confirmation before implementing it.
```

### Review question quality without silently rewriting

```text
Review the questionnaire for double-barreled wording, leading language, unbalanced scales, overlapping choices, missing opt-out choices, and broken routing. Explain each concern in plain language and ask me before making any research-significant change.
```

### Defer detailed consent work

```text
Build the questionnaire preview first. Record IRB, consent wording, data retention, and withdrawal details as unresolved decisions. Do not treat them as optional, and return to them before any deployment-ready package.
```

### Create an experiment

```text
Create a two-condition randomized experiment. Ask me one question at a time about the treatment, control, assignment point, primary outcome, manipulation check, exclusion rules, and analysis. Never invent a consequential design choice. Let me preview every condition.
```

### Test routing

```text
Simulate every reachable route with imaginary participants. Check required answers, Previous and Continue, refresh/resume, screen-out, consent refusal, completion, and withdrawal. Report problems in plain language, fix implementation defects, rebuild, and test again.
```

### Inspect structure

```text
Open the interactive preview and then open View structure. Walk me through the page order, text blocks, question IDs, control types, and terminal pages without using software-engineering jargon.
```

### Check mobile usability

```text
Test the entire questionnaire at a 390-pixel mobile width. Check touch-target size, contrast, unwanted blank scrolling, automatic scroll-to-top after navigation, image and media sizing, and that matrix row cards never create horizontal page scrolling.
```

### Modify without changing anything else

```text
Change only the wording of [question ID or exact wording]. Preserve stored values, routes, randomization, and every other research decision. Rebuild and show me a plain-language before-and-after summary plus the updated preview.
```

### Fork safely

```text
Fork this study into an independent copy named [new name]. Give it a new study ID, preserve the source folder, reset deployment identity and participant data, and list exactly what belongs to the new fork.
```

### Prepare preregistration

```text
Using only decisions I have approved, draft the preregistration. Mark unresolved hypotheses, exclusions, sample size, stopping rule, outcomes, and analysis choices clearly. Do not infer missing decisions or claim that the draft has been registered.
```

### Prepare external connections without connecting them

```text
Prepare the Vercel, Supabase, and Prolific handoff checklist. Use mock responses and mock randomization for all local tests. Do not log in, create credentials, deploy, or recruit participants until I separately approve those actions.
```

### Package the current draft

```text
Stop the design conversation here. Validate and rebuild the current study, include the survey source, configuration, desktop/mobile preview, structure view, decision records, and validation report, then create it as one downloadable ZIP. State clearly which fielding decisions remain unresolved.
```

## Troubleshooting

If the AI gives you only a planning document, ask for the **interactive respondent-facing preview**. If a control looks wrong, name the page and question and describe what you see rather than diagnosing code. If the preview opens but answers disappear after refresh, ask the AI to test the local mock session and revision handling. If the live gallery is unavailable, use the repository copy or wait for the GitHub Pages publication workflow to finish.

## Preview versus online publishing

Create the preview without an account. If you choose to publish, sign in to your own Vercel account and personally approve the connection. Do not give your AI a password. Vercel’s optional [Onboard your agent](./docs/vercel-agent-onboarding.md) helps prepare tools; it does not replace login or storage verification. If your host cannot connect, keep the complete study folder and resume in a supported environment.

A local-only banner means answers stay in the browser. Verify actual storage separately with an online test and the results page. Required sliders need interaction unless you explicitly chose a starting value. Ask the AI not to add an unwanted default.

## Ask for an assignment procedure that fits your research

Describe the procedure you want to your AI. For example: “Randomly assign participants to four groups, then show my prepared text list in participation order within each group.” Group assignment is random; the within-group list is sequential. First ask what the existing tools can do and what needs additional implementation. Agree what happens when a list ends or someone stops. A study-specific extension can take extra implementation and testing. Review refresh and simultaneous-participation tests before approving it. See [assignment guidance and prompt examples](./RANDOMIZATION.md).

## CBC preview and project contact

For choice-based conjoint tables, see [CBC import and computer/mobile preview](CBC.md). The preview itself does not collect responses; use the separate [CBC collection package](CBC-COLLECT.md) for the server-backed CBC workflow. Its local verification is distinct from cloud fielding approval. For project questions or bug reports: [greedyq.contact@gmail.com](CONTACT.md). Individual studies must provide their own research-team contact.


## Before starting: verify guide access

If you cannot read the complete required greedyQ guide, do not start the study interview or draft questions. Try the raw text link or repository import; otherwise ask me to attach the complete guide. Continue only after the complete guide is loaded.

See [guide access in supported desktop agents](GUIDE-ACCESS.md). The plain text entry is `https://raw.githubusercontent.com/zomtoli7/greedyQ/main/START-HERE.md`. Do not treat tool absence as guide access success.
