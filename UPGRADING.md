# Resume and upgrade a draft

<!-- GREEDYQ_DESKTOP_POLICY -->
**greedyQ requires an installed desktop AI app for creating or modifying studies. AI web apps are officially unsupported.** Download ChatGPT desktop or Claude Desktop from the official provider. Gemini is not officially supported, including its desktop app. Use an agent-enabled mode that can read the complete guide, create real files and run the canonical preview; installing an app or paying for a model alone does not establish these capabilities. Ordinary desktop chat without these tools is not a supported authoring route. Participant surveys, computer/mobile previews and the researcher results page still run in a web browser. [Supported authoring environment](SUPPORTED-ENVIRONMENTS.md).
<!-- /GREEDYQ_DESKTOP_POLICY -->

[한국어](./UPGRADING(kor).md)

Ask: “Resume this downloaded study. Compare its greedyQ version with the current repository. Explain the changes, then upgrade a separate copy and show me both previews.”

The agent must read the current START-HERE and selected guides, inspect the prior guide lock and source version, and ask before upgrading. Continuing the pinned version remains an option. A new version is not permission to change hypotheses, questions, consent, sampling or analysis.

## Agent operation

`python3 tools/upgrade_study.py ORIGINAL NEW_FOLDER --profile simple`

The destination must not exist and must be outside the original. If a valid prior guide lock exists, its profile and modules are reused; otherwise specify them. The command verifies current registry hashes, preserves sources and assets, archives prior JSON records under `.greedyq/before-upgrade-*`, replaces the QMD release identifier, rebuilds canonical runtime files and native export, and regenerates a preregistration draft when configured. It writes `.greedyq/upgrade-report.json` with the outcome and hashes. It never deploys or changes the original folder.

Connections and common local databases are excluded: `.env*`, `.vercel`, `.git`, dependency/cache directories, SQLite files and ZIPs. This is not a general privacy scrubber: review other copied files before sharing. Symlinks are rejected. Failed upgrades remain in the destination for diagnosis and must not be deployed. Choose a new destination for another attempt.

The generated copy requires renewed desktop/mobile preview review and updated decision/state records before deployment. Prior approvals are historical, not automatically reapproved. Runtime file checksums detect local changes even when a working tree still carries the same release identifier.

## Boundaries

Only draft/test studies are supported by this automatic operation. Production-mode studies require a separately reviewed migration/new-study plan; never change an active session's randomization, question IDs, or response meaning. The command does not upgrade a remote database, reconnect cloud accounts, import historical CSV data, or guarantee arbitrary obsolete/custom syntax can be converted. Invalid source constructs fail visibly for agent/researcher review.
