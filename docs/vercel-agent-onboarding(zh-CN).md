# Vercel 连接与可选代理准备

[English](./vercel-agent-onboarding.md) · [한국어](./vercel-agent-onboarding(kor).md)

## 默认流程

保留既有研究者流程：审阅问卷，登录 Vercel，批准必要 Vercel/Supabase 访问，收到已验证的问卷与结果链接。**Onboard your agent 是可选项，不是必须步骤。** 普通使用不要求研究者安装 CLI、配置插件或重启应用。

AI 先检查现有连接。有已批准的官方 Vercel 连接时，确认用户及目标团队后优先用于支持的操作；否则采用原有受支持 CLI/集成路径。分别核对每条连接的权限范围，并保持同样的研究批准、固定文件、数据边界和部署验收。官方连接不会改变谁能批准或访问研究。

## 缺少团队授权

登录成功时，团队列表仍可能为空，或目标团队仍无法访问。不要认定没有项目，不要重连整个账户、清除凭据或用其他认证绕过拒绝。对已知团队使用提供商的恢复流程。`authorize_team_access` 返回 `requires_user_action` 时，展示准确链接及有效期，等研究者亲自批准后在原连接重试。没有 SSO 也可能需要这种授权。临时批准链接和凭据不能公开。

简单说明：“账户已连接。请批准这个研究团队的访问，然后我会重新检查。”

## 可选 Onboard your agent

Vercel 按钮复制 `Set up Vercel for me. Fetch https://vercel.com/get-started.md and follow it.`。[官方说明](https://vercel.com/get-started.md) 准备 CLI、指南/插件和官方 MCP 连接，本身不创建 greedyQ 研究、不配置 Supabase、不验证保存，也不部署问卷。

研究者请求，或希望为重复使用准备受支持 AI 环境时，可介绍此选项。检查并复用工具；插件与独立技能只选一种，安装一次。保留其他配置，不重复添加连接。遵循最新[官方主机说明](https://vercel.com/docs/agent-resources/vercel-mcp)。CLI 完成不证明桌面/浏览器主机已经加载工具。先刷新，仅在新工具仍未出现时重启。全局准备不创建/连接项目、不配置数据库、不部署、不招募；修改操作保留确认。

## 实际验证范围

2026-10-25 在维护者测试环境执行了可选流程：Vercel CLI 65.2.0、复用现有登录、安装 Codex Vercel 插件、官方 MCP 认证、重启主机以加载工具，以及单独批准目标团队。官方文档搜索、认证团队列表与目标团队读取均成功。最初列表为空，直接读取团队才暴露缺少授权，说明不能把登录视为团队访问已完成。

这些证据只验证该环境的连接准备与读取，不验证新 MCP 路径下的部署、Supabase 配置、其他账户/主机、招募或付款。已有问卷/结果部署和付费 Prolific 试验没有改变。此前 Claude 试验停在 Vercel 登录，也不提供部署证据。

实际部署依照[部署模块](../guides/modules/deployment-vercel-supabase/guide(zh-CN).md)，包括模拟回答保存、受保护结果和明确的正式收集批准。两条路径都不可用时保留完整研究文件夹并提供准确交接。
