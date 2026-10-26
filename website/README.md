# Google Sites website source

[한국어](./README(kor).md)

This directory preserves the renderer, embedded gallery and images from the owner's publicly accessible Google Sites embed retrieved on 2026-10-25. `content.json` holds the existing English, Korean and Simplified Chinese content; `prolific-content.json` supplies the dedicated Collect page and adjacent-page revisions. The template retains the original application; it is not a replacement hosting service.

Run `python3 tools/build_website_embed.py`. It reads `release.json` and every English/Korean update note to build `google-sites-embed.html`. The footer, About → Version and updates, and update-history links share the current release identifier. No real survey, private results page, credentials, participant IDs or operator snapshots are embedded.

## Apply to the existing Google Site

1. Open the owner's Google Sites editor and select the existing full-page custom embed.
2. Choose its edit/pencil control and the HTML embed-code editor. Preserve the existing site page, permissions, domain forwarding and layout.
3. Replace the embed code with the complete contents of `google-sites-embed.html`, preview and save the embed.
4. Verify Guide → Collect: Deploy and collect → Connect to Prolific → Review responses. Check English, Korean and Chinese; previous/next, mobile navigation, prompt copying and About → Version and updates.
5. A draft edit/save is not public publication. Follow the owner's publishing decision and the browser tool's applicable permission policy before pressing Publish. Check the public site after publication; do not claim it changed merely because this file was regenerated.

The owner supplied the editor page ending `/p/1f5xyMm0_Og8HeJkxgVDcRC8tJC2GTsQO/edit`. On 2026-10-25, after the owner enabled macOS accessibility and requested direct Safari updates, the existing embed was replaced, saved and published through Safari. The public site's decoded `data-code` embed was fetched independently and matched `google-sites-embed.html` exactly, including `0.2_2026-10-25_0af2387` and the dedicated Prolific guide. This records that publication only; future edits still require their own verification. TinyFish was not used.

The subsequent first-researcher audit release `0.2_2026-10-25_7beafe4` was also saved and published through Safari on 2026-10-25. An independent public fetch again matched the complete generated embed exactly (SHA-256 `37c382b094e3ec977600a3b7f09c7fdbed64b8eb51dd85b8bffdbed989e51614`). The paid survey/results deployments were not changed.

The Claude review and AI-assisted allocation guidance release `0.2_2026-10-25_15d4d3e` was saved and published through Safari on 2026-10-25. The complete public embed matched all 687739 generated source bytes exactly (SHA-256 `a774a5a2c8544d4b56d04a2b879f9d822b4ad4a8c0bb6d1e2faea3754d1bef44`). Guides include optional Vercel agent onboarding and the four-group/group-specific text-sequence example. After release stamping, all 187 Python and 41 Node/browser tests passed without skips. Vercel/Supabase deployments and the paid Prolific pilot were not changed.

## Current publication handoff

Use [the publication request](./publication-request.md) and the generated `publication-manifest.json` for the latest prepared embed. The manifest identifies the release, byte length and SHA-256. The homepage-update Work must separately save, publish and verify the public site; this source update does not claim publication. The current Prolific page distinguishes the completed basic paid pilot, researcher-confirmed approval/payment and remaining checks.

## Verified publication history — 2026-10-26

The existing homepage was saved and published using the in-app Browser. The complete decoded public `data-code` embed at https://sites.google.com/view/greedyq matched the verified source exactly:

| Website revision | Release | UTF-8 bytes | SHA-256 |
| --- | --- | ---: | --- |
| Paid-trial guidance | `0.2_2026-10-26_e10197b` | 710863 | `df215e941e0844a0a4c335479872753b8cce9132d2cf792281bbc22fadda85c2` |
| Contact information | `0.2_2026-10-26_e10197b` | 711794 | `c0295255f6a03c8ed417da926011da7d6c0ce918b583df492c5382f5022b7700` |

English, Korean and Chinese Prolific guidance distinguishes the completed one-person paid trial, agent-checked response/CSV matching, researcher-confirmed approval/payment, and remaining completion-time, screening and cleanup checks. No separate payment receipt was inspected. Results guidance, previous/next navigation, the mobile contents menu at 390 px, and About → Version and updates were checked on the public site. Other pages, layout, sharing and domain settings were preserved. Safari and the desktop mouse were not used; participant/results deployments, databases and Prolific settings/payments were not changed.

The contact-information revision adds About → Project → Contact in all three website languages, with `mailto:greedyq.contact@gmail.com` for bug reports, questions and suggestions. It retains the same release identifier; its distinct website revision and file hash identify this content-only change.

The contact-information revision was also saved and published through the in-app Browser on 2026-10-26. The complete decoded public HTML matched the generated source exactly, with the byte length and SHA-256 recorded above. The public Contact page displayed the invitation and email link. `publication-manifest.json` records `published_and_verified` for this contact revision. Any later file change requires a fresh build, publication and verification.
