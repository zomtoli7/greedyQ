# greedyQ 指南目录

<!-- GREEDYQ_DESKTOP_POLICY -->
**使用 greedyQ 创建或修改研究必须使用已安装的 AI 桌面应用。AI 网页应用不在官方支持范围内。** 请从官方提供方下载 ChatGPT 桌面应用或 Claude Desktop。Gemini（包括桌面版）不在官方支持范围内。请启用能读取和创建文件、执行任务的代理功能。安装应用或付费订阅并不保证这些能力。没有所需工具的普通聊天不能用于正式制作。参与者问卷、电脑与手机预览及研究者结果页面仍可在浏览器中使用。 [制作问卷所需的应用](../SUPPORTED-ENVIRONMENTS(zh-CN).md).
<!-- /GREEDYQ_DESKTOP_POLICY -->

[English](./README.md) · [한국어](./README(kor).md)

这些指南共同组成 greedyQ **可由 AI 代理执行的应用规范**。greedyQ 本身不是代理；具备相应能力的通用 AI 读取并遵循后，成为 greedyQ 研究助手。

## 默认：从仓库开始

- 普通使用从 [公开开始页面](https://greedyq.netlify.app/)开始。AI 按 `registry/guide-index.json` 读取固定版本的核心、一个研究类型及需要的模块。英文规范为权威来源，中文帮助理解，不替换 registry 中的代码或哈希。
- 不能读取仓库时才附上 [`greedyq-guide(zh-CN).md`](./greedyq-guide(zh-CN).md)。它包含原样固定代码、预览规范及数据库/部署/记录结构。
- [`greedyq-guide-compact(zh-CN).md`](./greedyq-guide-compact(zh-CN).md)是精简对话辅助，单独使用不能可靠生成研究文件。
- `examples/complete-study/` 是参考，不把其中虚构内容直接放进无关真实研究。

从“我们来做问卷吧”开始。AI 应识别能力、恢复已有研究，并一次只问一个研究决定。

## 中文模块

- [核心指南](./core/guide(zh-CN).md)与[沟通规范](./core/communication(zh-CN).md)
- [普通问卷](./profiles/simple/guide(zh-CN).md)与[实验](./profiles/experiment/guide(zh-CN).md)
- [知情同意](./modules/consent/guide(zh-CN).md)、[IRB](./modules/governance-irb/guide(zh-CN).md)、[预注册](./modules/preregistration/guide(zh-CN).md)
- [Vercel/Supabase](./modules/deployment-vercel-supabase/guide(zh-CN).md)、[Prolific](./modules/prolific/guide(zh-CN).md)、[surveydown 导出](./modules/export-surveydown/guide(zh-CN).md)

## 标准研究的设计检查

下表说明应有行为，不代表已完成所有 GPT/Claude 行为评估。

| 场景 | 预期行为 | 依据 |
| --- | --- | --- |
| 新对话 | 确认目的/对象，并先询问自行编题还是 AI 起草 | 开始协议 |
| 单一附件 | 从完整指南提取原样代码并核对哈希 | 内嵌固定文件 |
| 继续研究 | 读取当前状态、未决决定和批准，不编造进度 | `.greedyq` 记录 |
| 请求 OSF 提交 | 只交草稿，实际注册由研究者自行完成 | 预注册模块 |
| 请求招募 | 核对同意、分析/预注册和部署等适用批准 | 正式收集检查点 |
| 改样本量 | 新增替代决定，使受影响文件/批准失效 | 决定与文件清单 |
| 任意 R | 不执行，提供声明式或原生导出替代 | 核心规范 |
| 声称已上线 | 要求实际外部验证证据 | 外部状态记录 |

结构、记录、文件哈希和 QMD 已有自动检查。Python/JavaScript、数据库与指定云端路径的实际范围见[当前准备状态](../docs/external-connection-readiness.md)，不要把过去证据当成另一账户、任意模型或新部署的保证。

## 后续模型行为评估

在 GPT 与 Claude 分别试验：从简短说明生成研究、恢复 `.greedyq`、修复错误 ID/路径/同意时点、拒绝编造样本量或提交未批准材料，以及一致生成 QMD/YAML/记录/预注册。

评估提问节奏、决定保真、方法问题升级、语法、可恢复性、纠错与外部状态的准确陈述。

## 连接选择

默认仍是 Vercel 登录与必要 Supabase 授权后取得两个已验证链接。现有官方连接优先，缺少时使用既有受支持路径。Onboard your agent 可选，不作普通研究者必经步骤。见[中文连接说明](../docs/vercel-agent-onboarding(zh-CN).md)。

## CBC 预览与项目联系

选择型联合分析请参见 [CBC 导入及电脑/手机预览](../CBC(zh-CN).md)。v0.3 预览不开放正式 CBC 收集；正式收集仍使用受支持的 v0.2 Simple/Experiment 流程。项目问题或错误报告：[greedyq.contact@gmail.com](../CONTACT(zh-CN).md)。各研究须提供自己的研究团队联系人。
