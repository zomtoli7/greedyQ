# Vercel 与 Supabase 部署模块

[English](./guide.md) · [한국어](./guide(kor).md)

使用登记的固定应用和数据库策略模板。秘密只放在提供商环境设置中；浏览器使用最少权限，管理操作保留在服务器，不能暴露 service-role 凭据。

按顺序应用全部 001–008，再用 `tools/cloud_lifecycle.cjs` 的 `registerStudy(client, model)` 注册每个审阅模型。遵循 [RANDOMIZATION.md](../../../RANDOMIZATION.md) 的已有数据库限制；没有规划仍需工作的其他研究注册之前，不更改正在使用的共享数据库。旧连接验收不证明新运行时或迁移可用。

文件准备、服务配置、部署、在线地址验证和开始招募是不同状态。只有具备工具且得到授权时才能执行外部变更，只报告实际看到的结果。正式收集前在已部署版本测试同意、恢复、分配持续性、所有结束、重复参与、退出、删除请求和分析导出。

默认只让研究者登录 Vercel 并批准所需的 Vercel 原生 Supabase 资源。AI 配置迁移、环境连接、公开问卷，以及单独由 Vercel Authentication 保护的结果应用。明确提供 Survey 与 Results 链接，不让普通研究者操作数据库。

请求账户前先构建研究，准备 `supabase-connection-test.html` 和全部迁移。连接浏览器须先建立带访问能力令牌的会话再保存，记录确切 `greedyq_version`，把 Prolific 外部 `SESSION_ID` 与内部 UUID 分开。普通启动用原子 `greedyq_start_prolific`，不能拆为创建/注册两步。只有服务器验证的 Test 权限可使用 `greedyq_start_prolific_preview`。`is_test` 与 `respondent_source` 分别记录。正式收集前提交 Direct 测试回答，在结果页 Test/Direct 核对，同时 Real 数量不变。研究者说明见 [RESULTS-DASHBOARD.md](../../../RESULTS-DASHBOARD.md)，[SUPABASE-SETUP.md](../../../SUPABASE-SETUP.md) 仅作恢复指南。

007 根据新接受的完整快照清理当前会话不再存在的回答，隐藏清除后结果/CSV 也须消失。不批改其他会话或历史数据；已有安装按审阅升级流程补充 007，本地审查不改变付费试验。

早期解释预览无需账户，正式上线需研究者自己登录授权。[可选连接准备](../../../docs/vercel-agent-onboarding(zh-CN).md) 不代替登录、Supabase 配置或保存验证。`init` 生成起止页、记录和部署文件。`preflight PATH_TO_STUDY` 检查本地包；`preflight PATH_TO_STUDY --stage deployment` 阻止 mock、未决决定和待批准状态。通过后仍须验证实际连接。

配置后的候选文件在另一目录时，用 `preflight PATH_TO_STUDY --stage deployment --deployment-index PREPARED_SURVEY/index.html` 检查。原预览保留 mock，检查候选内容是否与当前验证模型相同。

## 连接方式选择规范

默认流程不变：审阅问卷 → Vercel 登录 → 必要 Vercel/Supabase 授权 → 已验证问卷与结果链接。**Onboard your agent 是可选项，不能作为先决条件。** 不把工具安装、插件设置或应用重启放进普通首次使用清单。

1. 任何安装配置之前先检查现有连接。已有官方 Vercel 连接时，用只读调用确认用户与目标团队，再优先用于所支持的操作。团队列表为空不证明没有团队或项目。
2. 没有官方连接或缺少操作时，使用已独立核对账户/团队的既有 CLI/集成路径。不要切换账户、采用个人默认范围或重复建立项目。CLI 登录不等于 MCP 授权；两条路径必须遵守相同模板、研究批准、隐私和在线验收要求。
3. 团队被拒绝时，对已知团队使用 `authorize_team_access`，展示返回的批准链接，等研究者批准，再在同一连接重试。没有 SSO 也可能需要此授权。不要重连全账户、清除凭据或用别的凭据暗中绕过拒绝。临时授权链接不得出现在公开文档或问卷文件。
4. 仅在研究者要求，或希望为重复使用准备受支持环境时，介绍可选 Onboard。复用工具，只为当前主机安装一次指南；仅在新工具不可发现时刷新/重启。保留无关配置。全局准备期间不创建/连接项目、不配置 Supabase、不部署、不收集。
5. 配置后真正调用文档搜索、团队列表及目标团队读取。安装、认证、工具发现、团队访问、部署和保存验证是不同状态，不能因准备成功就认定整个研究可用。两种路径都不可用时保留完整研究，准确说明交接。

对账户/项目变更保留确认，仅用日常语言请求确实缺少的登录或批准，不让研究者粘贴认证信息或学习内部工具名称。
