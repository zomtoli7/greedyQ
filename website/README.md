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

The owner supplied the editor page ending `/p/1f5xyMm0_Og8HeJkxgVDcRC8tJC2GTsQO/edit`. No Google Sites editing tool is connected in this conversation. The owner declined TinyFish; do not request it again as a prerequisite. The generated file and local preview remain usable without that plugin.
