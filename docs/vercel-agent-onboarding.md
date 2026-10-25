# Vercel: Onboard your agent

[한국어](./vercel-agent-onboarding(kor).md)

Reviewed on 2026-10-25. The public button copies: `Set up Vercel for me. Fetch https://vercel.com/get-started.md and follow it.`

The [official playbook](https://vercel.com/get-started.md) prepares a coding agent with the Vercel CLI, platform guidance (plugin first, standalone skills as fallback), and the official MCP connection. It separates machine setup, agent setup, and later project operations. It still requires the account owner to log in and approve access. It does not create a greedyQ study, provision Supabase, verify response storage, or publish a survey by itself.

Use this as an optional connection-preparation route once the researcher requests Vercel setup. First inspect existing tools and connections. Reuse an authenticated official connection when available; do not install duplicate plugins and skills, overwrite other MCP entries, or create/link a project during global onboarding. Follow the current [official MCP client instructions](https://vercel.com/docs/agent-resources/vercel-mcp), since host support differs. CLI configuration is not proof that a desktop or browser-only host can use it. Verify the connection with a read-only team listing before project work.

A researcher-facing explanation: “Your preview is ready. To put it online, sign in to Vercel and approve the connection when asked. I will then prepare and check the survey, results link and data connection.” If the host cannot operate Vercel, preserve the complete study folder and explain the supported handoff. Never ask for passwords or paste private access tokens into ordinary conversation.

For this review, only public documentation and the public button were inspected. No global tools were installed, no authentication was started, and no cloud project was changed. Claude’s test stopped at login, so that report provides no evidence of successful external deployment. The paid Prolific pilot remains outside this review.
