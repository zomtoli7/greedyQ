# greedyQ User Guide

[한국어](./USER-GUIDE(kor).md)

> **Be greedy with your time. Just ask your AI to make your questionnaire.**

This guide takes a nontechnical researcher from an idea to a survey that can be tested on desktop and mobile. It stops before real accounts are connected or real participants are recruited.

## What you need

- GPT, Claude, or another capable AI that can read a public GitHub repository
- A short description of what you want to learn and whose opinions you want
- Time to answer questions and personally test the result

You do not need to know programming, Markdown, databases, or deployment tools.

## 1. Give greedyQ to your AI

Open the [greedyQ start page](./START-HERE.md), or give your AI this URL:

```text
https://github.com/zomtoli7/greedyQ/blob/main/START-HERE.md
```

The AI should read that file and the linked files in the same repository. You do not need to attach every guide and template separately.

## 2. Choose how to start

### Create a new survey

Copy this message:

```text
Read and follow the current greedyQ instructions at:
https://github.com/zomtoli7/greedyQ/blob/main/START-HERE.md

Create a new greedyQ study. Treat me as a nontechnical researcher, ask one focused question at a time, and take me through a working desktop-and-mobile preview.

I want to learn: [your question].
I want to hear from: [your intended participants].
```

### Modify an existing survey

Give the AI access to your existing greedyQ study folder, then copy:

```text
Read and follow the current greedyQ instructions at:
https://github.com/zomtoli7/greedyQ/blob/main/START-HERE.md

This is an existing greedyQ study. Summarize it in plain language and help me modify it. Preserve its history and current greedyQ version unless I approve an upgrade. Ask one focused question at a time.

I want to change: [your change].
```

This changes the original study. Ask for a plain-language change summary before accepting the result.

### Fork an existing survey

Give the AI access to the existing study folder, then copy:

```text
Read and follow the current greedyQ instructions at:
https://github.com/zomtoli7/greedyQ/blob/main/START-HERE.md

Fork this greedyQ study. Preserve the original, create an independent copy with a new study identity, and help me change only the copy. Ask one focused question at a time.

The new version should differ in this way: [your change].
```

Confirm that the AI created a separate copy and did not overwrite the original.

## 3. Have the guided conversation

The AI should act like a research assistant, not a software engineer. It will ask about the research purpose, intended participants, design, main outcome, recruitment, questionnaire, survey flow, consent and privacy, analysis, and preregistration.

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

The AI may open the preview, show an interactive artifact, or give you a folder to download. If you receive a folder, keep its files together and open `preview.html` in a modern browser.

Preview mode shows desktop and mobile versions, uses imaginary participants, and keeps test responses local. It must not send responses to an external service.

## 5. Test it like a participant

For every survey:

- Try to continue without answering a required question.
- Use Previous and Continue, then refresh and check that progress resumes.
- Try opt-out, other, and open-text choices.
- Check that hidden questions appear only when intended.
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

After preview approval, greedyQ can prepare a preregistration draft, a Vercel-ready survey, Supabase setup files, Prolific settings, and a native surveydown export. Account connection, submission, deployment, and recruitment each require separate approval and external verification. Continue with [External Connection Readiness](./docs/external-connection-readiness.md).

## Common problems

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
