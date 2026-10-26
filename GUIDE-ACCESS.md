# When your AI cannot open the guide

[한국어](./GUIDE-ACCESS(kor).md) · [简体中文](./GUIDE-ACCESS(zh-CN).md)

## Confirmed copy/paste failure

The researcher subsequently reproduced the failed paste: line breaks disappeared and the Korean sentence attached to the address as `START-HERE.md새`. This malformed address, rather than the canonical repository URL, explains that observed failed attempt. The exact clipboard/rich-text behavior in the destination app was not instrumented; do not generalize it to a Gemini-wide browsing limitation.

The website copy blocks now use text/plain first, an explicit plain-text legacy copy handler and plain-text manual-selection handling. URLs are enclosed in `<...>` and lines have literal ASCII separators, so removing line breaks cannot turn `.md` plus the next Korean/Chinese sentence into a different address. BibTeX remains unchanged code. Use a fresh copy from the updated website after it is published, or wrap the correct URL in `<...>` with a real space before following text. The alternative raw/import/attachment paths below still apply to genuine guide access failures.

A link in a message does not prove the AI has read it. If it says “I cannot access the website” and then starts drafting a survey, stop that attempt: the result has not followed verified greedyQ instructions. Model names or a paid subscription alone do not establish browsing, file creation, browser preview or deployment capabilities.

## First try the plain text link

Ask it to read:

```text
https://raw.githubusercontent.com/zomtoli7/greedyQ/main/START-HERE.md
```

This avoids the surrounding GitHub interface. It does not overcome a host that cannot fetch links. The entry guide alone is not enough: the AI must load the same release's registry, resolved guides and fixed source files, or a complete full bundle. It must not infer the missing rules from the project name, search snippets or the first interview question.

## In the Gemini web app

Google documents a separate repository import route: Add files → More Uploads → Import Code → enter `https://github.com/zomtoli7/greedyQ`. If that route is shown for your account, use it and then ask the AI to read `START-HERE.md` and its required files. Availability and menu wording can differ. Attaching a repository is different from pasting a URL into the conversation. [Google's file/import instructions](https://support.google.com/gemini/answer/14903178?hl=en)

For custom Gemini API applications, URL Context is an explicitly supplied tool; a link alone is not an assertion that the client enabled it. This does not diagnose a particular Gemini Apps conversation. [Google's URL Context documentation](https://ai.google.dev/gemini-api/docs/url-context)

## If import or browsing is unavailable

Download the [complete English guide](./guides/greedyq-guide.md), [Korean guide](./guides/greedyq-guide(kor).md), or [Chinese guide](./guides/greedyq-guide(zh-CN).md) from GitHub and attach the saved file. Use the download button, not a screenshot or a copy of only the first page. If the host rejects `.md`, save the same complete UTF-8 content as `.txt`; do not remove the embedded fixed code. The compact guide and `START-HERE.md` alone are not substitutes for the full bundle. If the file is too large or truncated, use repository import or a host that can read the complete bundle.

After the complete guide is available, the AI should confirm briefly that it loaded the guide and state its actual capabilities. A host with no file-generation or execution tools may help with research discussion, but cannot truthfully claim it built or tested a working greedyQ runtime. It should offer an agent-enabled handoff before artifact generation. No account login or payment is needed just to resolve guide access.

## Prompt that handles this safely

```text
Read the current greedyQ guide and all required files from the same release:
https://github.com/zomtoli7/greedyQ/blob/main/START-HERE.md
If you cannot read them, do not start the study interview, draft questions or claim to follow greedyQ. First try the raw text URL, repository import, or ask me to attach the complete guide. Continue only after the complete required guide is available; explain your actual file, preview and deployment capabilities briefly.
```

## What the reported screenshot establishes

On 26 October 2026 the public GitHub page and raw text link both returned HTTP 200 without login from our check. The screenshot shows the AI reported access failure and continued. It does not establish the original failure's cause, the app's enabled tools or a platform-wide Gemini limitation. We changed the copied starter prompt because a guard contained only inside an unread page cannot help. Gemini Apps itself was not retested under the reporter's account.
