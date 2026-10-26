# Desktop support policy verification

[한국어](./desktop-support-verification-2026-10-26(kor).md)

The project owner set an official desktop-only researcher authoring policy. Installed provider apps must still pass actual guide/file/preview readiness checks. AI web apps, PWA shortcuts and tool-less chat cannot bypass the policy through attachments. Respondent browsers and researcher previews/results remain supported. This is a support policy, not a claim of provider-wide web incapability.

Direct anonymous HTTP checks on 2026-10-26 returned 200 for the raw START-HERE.md and registry/guide-index.json. The reporter’s later correctly delimited URL failure differs from the earlier malformed clipboard URL. The screenshot reports PERMISSION_DENIED, but does not expose the tool trace or establish its cause. Stopping authoring was correct. No full Gemini desktop authoring or deployment test was performed under that account.

Official app documentation was opened before documenting download routes: [Gemini](https://gemini.google/desktop/), [ChatGPT](https://learn.chatgpt.com/docs/app), [Claude](https://claude.com/download). Product availability is not greedyQ conformance certification. Website HTML is prepared for the separate homepage publication work; this work does not publish Google Sites.


Gemini (desktop included) is now officially unsupported. At that stage the shared Gemini conversation URL could not be read with this tool, so its full transcript had not yet been reviewed. The researcher subsequently supplied an eight-page PDF, reviewed below. The policy decision uses the researcher’s reports and supplied screenshots, not an invented diagnosis of Gemini internals. Official authoring paths are ChatGPT desktop Work/Codex and Claude Desktop with verified file/task tools.


Local regression result: 237 Python tests and 57 Node/browser tests passed, without failures or skips. The copy audit covers 270 cases over three languages and two widths, including unchanged BibTeX. The six CBC presentation combinations match Python/JavaScript models and hashes; vertical/responsive phone layouts avoid horizontal page scrolling at 320/390px. Existing omitted-presentation design hashes remain unchanged. These tests do not certify Gemini, a paid CBC study or the pending cloud CBC deployment.

## Subsequent eight-page PDF review

Read all eight pages of the researcher-provided Gemini conversation. The first extraction/rendering path mishandled its Korean font; macOS PDFKit recovered readable text and rendered the relevant pages. The original conversation and screenshots are private source material and are not copied into the public repository.

- Page 1 reports failure to load the guide and correctly stops the study interview. The transcript is evidence of that report; it does not include the underlying tool trace.
- Pages 2-5 attribute the failure to provider-wide raw-domain blocking, JavaScript rendering, API/CDN restrictions and crawler policies. The table labeled actual tests uses abbreviated/generic URLs and no captured request/response trace. These remain model assertions, not independently verified diagnoses. Our anonymous raw entry and registry checks returned HTTP 200; this establishes public availability from our environment, not access from Gemini's internal tools.
- Page 6 asserts a fully isolated Python environment with no outbound network. The transcript does not establish this as a universal provider policy or as the exact cause of this session's guide failure.
- Pages 7-8 propose ZIP uploads, a proxy and other developer tools. No uploaded repository, successful import, canonical build, functioning preview or connected deployment is demonstrated in the PDF. Promises of future execution do not establish end-to-end conformance. The proposed alternatives are not instructions to implement a proxy or to resume unsupported authoring.

Decision unchanged: Gemini, including desktop, remains outside official greedyQ support pending a separately verified end-to-end journey. Official authoring paths are ChatGPT desktop Work/Codex or Claude Desktop with verified file/preview tools. Do not republish unsupported claims about other providers' internal restrictions. Keep capability checks, guide-access failure and execution success as distinct evidence.
