# Add CBC tasks to your survey

[한국어](./CBC-MODULE(kor).md) · [简体中文](./CBC-MODULE(zh-CN).md)

CBC is a **v0.3 module**, not a separate survey you must start over to create. Keep writing questions with your AI. When you reach the desired position, ask it to insert CBC tasks; you can continue with ordinary questions afterwards.

## Start or insert a module

Use <https://greedyq.netlify.app/> in a supported desktop agent. For example:

```text
Read and follow <https://greedyq.netlify.app/>.
Continue the attached study. Keep its existing questions. Insert a CBC module after the background questions, then let me add ordinary questions afterwards. Ask one central question at a time before deciding the design.
```

The AI first asks which design route you prefer:

- **Design together:** explain your research goal and discuss attributes and levels. Review the proposed design table; an AI draft does not establish statistical efficiency or research validity.
- **Fill a blank table:** receive CSV files or an Excel workbook with attribute columns matching your confirmed choices. Save the editable study ZIP as well. Return the filled workbook, or both CSVs, when ready.
- **Use an existing design:** attach your design. The AI checks its codes and structure and explains any changes before asking you to approve them.

You confirm attributes, level wording/units, alternatives per task, tasks per person, blocks, neither and order rules. Choose button profiles or comparison tables and their computer/phone layout. These are research decisions; the AI must not fill them silently.

## Review the complete experience

The integrated preview has independent computer and mobile respondents and a structure dialog. It shows participant information, the ordinary questions, the CBC module and the remaining questions in one continuous session. It stores only local virtual responses. The desktop comparison remains horizontal when the preview is opened on a narrow device; responsive mobile comparisons stack vertically.

Try missing answers, neither, Previous, refresh, completion and withdrawal. Completion time is recorded only after the final ordinary page; finishing the CBC tasks alone is not survey completion. When connected to the database, withdrawal removes ordinary and CBC answers together, including CBC exposures and orders.

The first module contract supports **one CBC sequence in a linear survey**. The module gets its own page; your AI handles splitting an existing page when needed. Conditional question visibility and supported ordinary controls work within surrounding pages. A separate experimental assignment, page branching across the module, page/question/ordinary-option shuffling or several CBC sequences must not be silently approximated. The agent must explain a requested unsupported combination before altering the study. CBC's own block/task/alternative randomization remains available. Native surveydown CBC export is explicitly blocked until an equivalent implementation is verified.

## Save and return later

Ask for an **editable study ZIP** when stopping. It contains questionnaire sources, design files, collection settings, decisions and the locked guide version. It excludes response downloads, cloud keys, deployment credentials and generated publication folders.

```text
Read and follow <https://greedyq.netlify.app/>.
Resume the attached editable study ZIP at its saved step. Preserve the confirmed questions and CBC design. Tell me if the greedyQ version changed; ask before upgrading, and preserve the original if I approve a new copy.
```

If waiting for a design table, the AI remembers which files are expected. Resuming does not redraw or approve the design. A version upgrade uses a separate copy, keeps the original, refreshes the guide lock and requires review before fielding.

An **analysis archive ZIP** is different: it preserves collected data, CSVs and the registered model for analysis. It is not offered as a database-restore or survey-editing route. Keep the editable study ZIP too.

## Modify or duplicate

Ask to change only the parts you name. A fork gets a new study identity, keeps the original, and starts in Test mode with collection approvals reset. Existing stored responses and immutable registered designs are not rewritten. For a materially changed deployed design, publish a new reviewed study rather than changing the plan underneath existing participants.

## Connect, collect and finish

The existing Vercel/Supabase journey remains: the AI reuses an approved account connection, prepares separate Survey and protected Results links, and verifies synthetic Test data first. In Results, choose **Test responses** to inspect trials; **Real responses** remains the default and excludes those trials. Overview CSV contains ordinary answers; CBC choice CSV contains alternative-level choice/exposure rows. Withdrawn answers are absent from both kinds of response data.

Ending a study first stops collection and creates a verified seven-table archive, ordinary-response CSV and CBC choice CSV. For real research, the researcher must confirm saving the download before services are paused. A shared database stays active unless every affected study/service has been reviewed and the temporary interruption is explicitly approved. Service resume waits for database health; reopening collection is a separate deliberate action. Reusing an existing account does not require a fresh account or a new database for every logical study.

Small paid-participant testing is the next acceptance step after the researcher approves the actual instrument, consent/contact, data plan, recruitment route, return paths, time and compensation. Synthetic checks do not authorize recruitment or payment. See [collection](./CBC-COLLECT.md) and [cloud evidence](./docs/cbc-cloud-verification-2026-10-26.md).

## Agent implementation notes

The researcher does not need these commands. Use the ordinary study profile plus the `cbc` capability module. `sd_cbc(name = "course_choices", design = "study.design.json")` is the fixed marker inside an R-style fenced block on a QMD page; it is parsed as data, not executed as R. Normal `build` detects it and produces the mixed preview/private CBC package. Publish only folders produced by `prepareCBCDeployments`.

- `cbc-new`, `cbc-route`, `cbc-insert`, `cbc-blank`: record the design route, insertion point and attribute-specific CSV/XLSX handoff without inventing decisions.
- `cbc-pack-source`, `cbc-resume`, `cbc-fork`, `cbc-upgrade --approve-upgrade`: source-only ZIP, safe extraction, isolated identity and explicit copied upgrades.
- `cbc-preflight --stage package` / `--stage fielding`: distinguish a valid Test package from unresolved real-fielding approvals. The fielding check does not itself prove a deployment or paid test.
- `010_cbc_module.sql`: additive sequence and ordinary-answer validation. Keep applied 001–010 bytes unchanged. Do not use the generic v0.2 writer to bypass the CBC module contract.
- `tools/archive_study.cjs snapshot|pause|resume|reopen`: keep collection closure, service state and reopening separate. Management authorization is different from a database/service key; account-specific permissions may still require owner action.

Current module journey evidence: [verified and pending checks](./docs/cbc-module-verification-2026-10-26.md).

The authorized existing-account Supabase pause/resume acceptance now passed, including preservation of ten table fingerprints and a full post-resume mixed-survey/Results/withdrawal/CSV run. See the module verification record; this does not approve human fielding.
