# Vercel connection and optional agent onboarding

<!-- GREEDYQ_DESKTOP_POLICY -->
**greedyQ requires an installed desktop AI app for creating or modifying studies. AI web apps are officially unsupported.** Download ChatGPT desktop or Claude Desktop from the official provider. Gemini is not officially supported, including its desktop app. Use an agent-enabled mode that can read the complete guide, create real files and run the canonical preview; installing an app or paying for a model alone does not establish these capabilities. Ordinary desktop chat without these tools is not a supported authoring route. Participant surveys, computer/mobile previews and the researcher results page still run in a web browser. [Supported authoring environment](../SUPPORTED-ENVIRONMENTS.md).
<!-- /GREEDYQ_DESKTOP_POLICY -->

[한국어](./vercel-agent-onboarding(kor).md) · [简体中文](./vercel-agent-onboarding(zh-CN).md)

## Main journey

Keep the existing researcher journey: review the survey, sign in to Vercel, approve required Vercel/Supabase access, and receive verified Survey and Results links. **Onboard your agent is optional, not required.** Researchers do not normally install a CLI, configure plugins, or restart an app to use greedyQ.

The agent first inspects existing connections. Prefer an already available, authorized official Vercel connection for supported operations after checking the authenticated user and intended team. Otherwise use the established supported CLI/integration route. Verify scope independently for each connection and preserve the same study approvals, canonical files, data boundaries and deployment checks. An official connection does not change who may approve or access a study.

## Missing team access

A successful account login can coexist with an empty team list or denied access to the intended team. Do not conclude that there are no projects, reconnect the whole account, clear credentials or silently switch credentials to bypass a refusal. Use the provider's team-access recovery for the known team. If `authorize_team_access` returns `requires_user_action`, show its exact link and stated expiry, wait for the researcher's approval, then retry the original request on the same connection. This can apply without SSO. Never publish temporary authorization links or account credentials.

Explain simply: “The account is connected. Please approve access to this research team, then I will check it again.”

## Optional Onboard your agent

The Vercel button copies `Set up Vercel for me. Fetch https://vercel.com/get-started.md and follow it.` The [official playbook](https://vercel.com/get-started.md) prepares a CLI, guidance/plugin and official MCP connection. It does not create a greedyQ study, provision Supabase, verify storage or deploy the survey by itself.

Offer this optional preparation when the researcher requests it or wants a supported AI host ready for repeated use. Inspect and reuse existing tools; install the plugin or standalone guidance once, never both. Preserve unrelated configuration and do not add duplicate connections. Follow the current [official MCP host instructions](https://vercel.com/docs/agent-resources/vercel-mcp); CLI setup alone does not prove that a supported desktop host has loaded the tools. Refresh first, and restart only when the new tools remain unavailable. Do not create/link projects, provision databases, deploy or recruit during global onboarding. Keep confirmation enabled for changes.

## What was actually tested

On 2026-10-25, optional onboarding was exercised in the maintainer's test environment: Vercel CLI 65.2.0, existing login reuse, installation of the Codex Vercel plugin, official MCP authentication, host restart to load new tools, and a separate approval for the intended team. Official documentation search, authenticated team listing and access to that team all succeeded. The first team listing was empty; a direct team read exposed the missing grant. This is why login alone must not be reported as complete team access.

This evidence verifies connection preparation and read operations for that environment. It does not verify deployment or Supabase provisioning through the new MCP route, another account or host, recruitment, or payment. Existing survey/results deployments and the paid Prolific pilot were not changed. Earlier Claude testing stopped at Vercel login and likewise provides no deployment evidence.

For all actual deployments, follow the [deployment module](../guides/modules/deployment-vercel-supabase/guide.md), including synthetic saved-response tests, protected results and explicit collection approval. If neither supported connection route is available, preserve the complete study folder and provide an honest handoff.
