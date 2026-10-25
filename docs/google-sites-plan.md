# greedyq.org: Google Sites plan

[한국어](./google-sites-plan(kor).md)

The owner has an existing published Google Site. This document describes its structure, not proof that a new edit was saved or published. The current embed's renderer, gallery and English/Korean/Chinese content are preserved under `website/`; use `tools/build_website_embed.py` to generate the replacement. Keep Google Sites as the host. Use Surveydown's task-oriented organization as inspiration, not copied text or visual assets.

## Navigation and source mapping

| Public section | Contents | Repository source |
| --- | --- | --- |
| Home | What greedyQ does, three-step workflow, Start / Try examples buttons | README.md, docs/product-brief.md |
| Start here | New study, resume, modify and fork; copyable first prompt | START-HERE.md, USER-GUIDE.md |
| Your first survey | Manual question-by-question versus AI draft; team name; ethics now/later | USER-GUIDE.md, guides/core/communication.md |
| Question gallery | Interactive examples, mobile view, short “ask your AI” prompts | examples/control-gallery, USER-GUIDE.md |
| Survey flow | Required answers, conditional questions, navigation and structure | USER-GUIDE.md, preview specification |
| Experiments | Assignment versus ordering, fixed options, limits and examples | RANDOMIZATION.md, compatibility audit |
| Try and review | Desktop/mobile preview, synthetic data, revision prompts | USER-GUIDE.md, examples/simple-satisfaction-study |
| Publish and collect | Account approvals, survey link and protected results link, test/live separation | SUPABASE-SETUP.md, RESULTS-DASHBOARD.md |
| Connect to Prolific | Standalone Guide → Collect page directly after Deploy and collect and before Review responses; setup, repeated Preview, paid transition and review pauses | PROLIFIC-SETUP.md, website/prolific-content.json |
| Finish and return | Archive/download, close collection, pause/resume, new study, draft upgrade | ARCHIVING.md, UPGRADING.md |
| Preregistration | Draft files only; decisions still needed; independent submission | PREREGISTRATION.md |
| Advanced / compatibility | Native Surveydown export, supported subset, custom-control process | compatibility audit, export guide |
| About / cite / updates | Application identity, both citations, MIT, release and short history | CITATION.md, NOTICE.md, updates/ |

Keep the same order and scope in English, Korean and Simplified Chinese. Group navigation into Start, Guide, Examples and About. Each guide page should have a purpose, copyable prompt, numbered actions, expected result, troubleshooting and next step. Footer version and About → Version and updates use `release.json`; all release notes under `updates/0.2/` populate history. Never place private results links, actual participant data or pilot completion codes on the documentation site.

## Home draft

Headline: **Be greedy with your time. Just ask your AI to make your questionnaire.**

Explanation: “greedyQ helps your AI guide you from a research idea to a working survey and a protected results page. You decide the research; your AI handles the files and setup.”

Primary action: Start my survey. Secondary action: Try a sample survey.

Below the fold: Describe your study → Review a working preview → Approve publishing. Explain that preview works without connecting research services; publishing may require account/integration approvals. Do not promise unlimited free hosting, no approvals, or support for every Surveydown feature.

## Interactive gallery

Google Sites is the documentation layer, not the respondent runtime or private dashboard. Link or embed an already-public, versioned static control gallery; provide an “Open in a new tab” fallback. GitHub blob HTML is not a hosted interactive page. Confirm the real published gallery URL before adding it. Do not embed respondent records, credentials, protected results, or a live research survey. Use synthetic examples only. Verify embeds, keyboard access and narrow screens in the published site, not just editor preview. [Google's embedding guide](https://support.google.com/sites/answer/90569?hl=en) describes supported insertion paths.

## What the owner needs to provide

1. The Google Sites **editing URL**, or authorization to create a blank site in the already signed-in Google account.
2. Whether that account is personal or university/work Google Workspace; managed accounts may need administrator permission.
3. The current browser session with appropriate editor access. Do not send a password, verification code, or ask to share ownership with a nonexistent AI email address.
4. Registrar/DNS provider name for greedyq.org, and willingness to enter or approve the exact required DNS records. Never replace existing mail or unrelated records.
5. Approval of the navigation, public contact information, logo if any, language priority and publicly hosted gallery URL.
6. Separate final approval to publish publicly and connect the domain. Draft editing, public sharing and DNS changes are different actions.

Google's documented custom-domain setup requires a subdomain, so plan **www.greedyq.org** for Sites and a registrar-supported redirect from **greedyq.org** to it. Only the site owner can connect the domain. Domain ownership verification and DNS changes may be needed; propagation can take up to 48 hours. Work/school accounts may need an administrator. [Official domain setup](https://support.google.com/sites/answer/9068867?hl=en).

Draft editor access should stay restricted. Public viewers receive view-only access, not edit access. Check the logged-out site after publishing. [Sharing/publishing](https://support.google.com/sites/answer/6372880?hl=en), [editor permissions](https://support.google.com/sites/answer/97934?hl=en).

## Publication checklist

- First-time researcher completes the start path without reading GitHub code.
- All prompts copy correctly; English/Korean counterparts and next-step links work.
- Gallery uses the released runtime and never writes external responses.
- Preview, real survey and private results are clearly distinguished.
- Desktop and mobile navigation, images, contrast and embeds are checked.
- Release footer, limitations, citations and download links match the repository.
- Owner approves public content, domain mapping and publication separately.
- If connected browser editing is unavailable, deliver page-by-page copy/paste material; do not claim to have edited Google Sites.
