# greedyQ

- **Current specification:** `0.2`
- **Current release:** `0.2_2026-10-25_f2afa11`
- **Release source commit:** [`f2afa11`](https://github.com/zomtoli7/greedyQ/commit/f2afa113f55ff6502d433d899665d40e62a6b06f) · [更新记录](./updates/README.md)

[English](./README.md) · [한국어](./README(kor).md)

[开始问卷](./START-HERE(zh-CN).md) · [使用指南](./USER-GUIDE(zh-CN).md) · [AI 指南](./guides/README(zh-CN).md) · [Prolific 连接说明（英文）](./PROLIFIC-SETUP.md) · [结果页（英文）](./RESULTS-DASHBOARD.md) · [互动题型示例](https://zomtoli7.github.io/greedyQ/examples/control-gallery/preview.html)

> **Be greedy with your time. Just ask your AI to make your questionnaire.**

greedyQ 是面向在线学术研究、由规范驱动的 AI 原生应用。它以人可阅读的规范，规定通用生成式 AI 应如何建立并操作研究应用，而不是只用传统程序代码实现整个应用。

可移植的 Markdown、数据结构、检查点和原样模板共同构成 **agent-executable application specification**，即“可由代理执行的应用规范”。研究者把有版本的仓库交给 GPT、Claude 或其他具备相应能力的 AI，再说“我们来做问卷吧”。遵循规范的研究助手会引导研究流程，生成设计材料和参与者实际使用的问卷程序。

## AI 原生应用的结构

greedyQ 本身不是代理：

```text
greedyQ 可由代理执行的应用规范
               +
      具备相应能力的通用 AI
               =
       greedyQ 研究助手
               |
               v
   研究设计材料 + 可运行的问卷
```

1. **架构：** 主要用人可读、代理可执行的规范分发应用行为。
2. **领域：** 在线学术研究，包括设计、同意、问卷、实验、分配、招募、数据、预注册和实际收集。
3. **实现：** greedyQ 将这一架构用于可重复的在线研究。

不同模型可以有不同界面和能力，但必须遵守相同研究规范。因此跨 GPT、Claude、Gemini 等模型的可移植性需要共同的适配检查。AI 提供研究推理与自然语言协作；greedyQ 提供访谈顺序、批准检查点、文件约定、验证、预注册、固定运行代码和重复性边界。

## 为什么使用 greedyQ

商业问卷平台可能昂贵，复杂设计与可重复性也有门槛。surveydown 提供优秀的“用代码定义问卷”方式，但 R、Quarto、Shiny 对一些研究者较难。greedyQ 保留易读定义、Git 历史、研究者拥有的数据及可编程工作流，使用独立的浏览器 JavaScript 程序与 Vercel/Supabase，并通过 AI 对话协助使用。需要自由使用 R、Shiny 或 Quarto 时，可继续开发生成的原生 surveydown 项目及 `app.R`。

## 产品原则

- `survey.qmd` 是题目和内容的主要来源，语法在可行范围内兼容 surveydown。
- Vercel/Supabase 为主要运行路径；参与者的解析、检查、预览和显示在现代浏览器完成，无需安装 Python/Node.js。
- Python 作为开发期独立参考及检查工具，与 JavaScript 按共同样例核对分析结果、提示和行为。
- 原生 surveydown 项目（含 `app.R`）是重要输出。仅依据公开文档独立实现，不复制 surveydown 源码，不执行问卷中的任意 R/Shiny 代码。
- 条件与分配采用声明式、安全、可重复的规则。
- 数据归研究者拥有和控制，不要求图形化问卷编辑器。
- 普通体验是与通用 AI 对话；AI 提供研究建议，规范提供流程与重复性。
- 重要决定须研究者明确批准；正式收集前准备可审阅的预注册草稿。
- 区分可直接操作的代理环境与只能提供文件/交接的聊天环境，不编造外部成功。

## 主要流程

没有技术经验的研究者从[使用指南](./USER-GUIDE(zh-CN).md)开始。

```text
有版本的仓库 + 研究想法
            |
            v
       AI 逐步询问
            |
   设计 → 同意 → 题目 → 路径
   → 分配 → 分析 → 预注册草稿
            |
            v
   生成文件 → 检查 → 电脑/手机预览
            |
            v
      研究者审阅并批准
            |
            v
 Vercel 问卷与受保护结果页 + Supabase
            |
            v
      收集、查看、下载与归档
```

一般步骤：提供 `START-HERE.md`，说明研究，逐项回答并批准重要决定，审阅同意、题目、路径、分配、分析和预注册草稿，亲自试填，再单独批准账户连接、上线及招募。预注册只交付文件，实际登记由研究者自行完成。

## 对话方式与其他路径

**Chat mode** 的 AI 负责访谈、文件与交接；**Agent mode** 还可在有工具和批准的情况下编辑仓库、验证、配置服务、上线和检查实际结果。专家也能直接编辑 `survey.qmd`、`greedyq.yml`。需要完全自由定制时可使用原生 surveydown 导出。PPTX 导入仍是后续方向，不应声称已支持。

## 与 surveydown 的关系

greedyQ 独立实现 surveydown 风格语法。v0.2 浏览器实现公开文档中的 16 种题型，另有媒体、排序、并排评分、NPS、计时、固定总分、分组排序、逐级选择和经确认的自定义扩展。其他语法逐项报告兼容程度。项目不包含 surveydown 源码，不属于 surveydown，也不代表其维护者背书。功能可能直接兼容、生成到 `app.R`，或仅限 greedyQ；导出必须说明差异。许可与归属见 [NOTICE.md](./NOTICE.md)。

## 引用

greedyQ 论文发表前，学术使用应同时引用 [greedyQ GitHub 仓库](https://github.com/zomtoli7/greedyQ)及 `survey.qmd` 的确切版本，以及 [surveydown PLOS ONE 论文](https://doi.org/10.1371/journal.pone.0331002)。仅运行独立 greedyQ 程序也适用，并须准确说明实际运行的软件。可复制引用见 [CITATION.md](./CITATION.md)。

## 当前状态

v0.2 提供无需账户的浏览器预览。固定 JavaScript 核心解析 QMD/YAML、检查和编译支持语法、显示电脑/手机与双预览，并通过标准研究、题型示例和错误样例与 Python 核对。Vercel/Supabase 部署、受保护结果、001–007 迁移、Prolific ID、预注册草稿、原生导出和离线准备检查均已实现。

2026-10-25 已验证 Prolific 草稿 Preview 的完成、拒绝、退出与重复尝试；新退出先删除回答，保留已告知的最少管理标识；也核对结果/CSV 与测试/正式分离。首次付费试验由研究者发布后，等待 Prolific 常规审查，真实付费提交、批准及付款仍未验证。签名 URL 与正式重复提交尚不支持。见[连接状态](./docs/prolific-integration-status.md)、[云端证据](./docs/prolific-cloud-test-2026-10-25.md)、[付费状态](./docs/prolific-paid-pilot-2026-10-25.md)。仓库更新不会自动修改已上线研究。

## 试用电脑与手机预览

无需安装：解压研究文件夹，用现代浏览器打开 `examples/complete-study/preview.html`，同时查看独立电脑和手机试填。也可打开同目录 `studio.html`，选择 QMD/YAML 后在浏览器中检查并预览。

以下命令只供开发者参考与确定性重建：

```bash
python3 -m greedyq preview examples/complete-study
python3 -m greedyq preview examples/simple-satisfaction-study
```

预览地址通常是 `http://localhost:4173/preview.html`。`python3 -m greedyq validate PATH_TO_STUDY` 只检查；`python3 -m greedyq build PATH_TO_STUDY` 生成固定浏览器文件。预览不发送回答。`python3 -m greedyq run examples/complete-study` 在 `http://localhost:4180/index.html` 提供同一 JavaScript 参与者界面，mock 仅在浏览器保存。见[本地运行说明](./docs/local-respondent-runtime.md)。

更多资料：[AI 指南](./guides/README(zh-CN).md)、[架构](./docs/modular-guide-architecture.md)、[项目方向](./docs/product-brief.md)、[v0.2 规范](./docs/greedyq-v0.2-spec.md)、[恢复操作](./docs/operations-runbook.md)、[参考研究](./examples/README.md)、[兼容检查](./docs/surveydown-compatibility-audit.md)、[随机分配](./RANDOMIZATION.md)、[归档](./ARCHIVING.md)、[安全升级](./UPGRADING.md)、[预注册](./PREREGISTRATION.md)。部分开发资料只有英文与韩文。

## 文档语言

英文 Markdown 是权威来源，每份文档保留 `(kor).md` 韩文副本。入门与 AI 指南另有 `(zh-CN).md` 简体中文，不表示全部开发文档都已译成中文。代码、ID、路径、配置键和规定语法不翻译；参与者语言另行确认。

## 许可

greedyQ 使用 [MIT License](./LICENSE)。

## Vercel 连接方式

默认保留审阅 → Vercel 登录与所需 Supabase 授权 → 已验证问卷/结果链接。已有官方连接时确认账户与团队后优先复用，没有或操作不可用时采用既有受支持流程。**Onboard your agent 是可选准备，不是必需步骤。** 见[使用指南](./USER-GUIDE(zh-CN).md)和[连接准备说明](./docs/vercel-agent-onboarding(zh-CN).md)。
