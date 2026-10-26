# surveydown 导出模块

<!-- GREEDYQ_DESKTOP_POLICY -->
**使用 greedyQ 创建或修改研究必须使用已安装的 AI 桌面应用。AI 网页应用不在官方支持范围内。** 请从官方提供方下载 ChatGPT 桌面应用或 Claude Desktop。Gemini（包括桌面版）不在官方支持范围内，并启用能读取和创建文件、执行任务的代理功能。安装应用或付费订阅并不保证这些能力。没有所需工具的普通聊天不能用于正式制作。参与者问卷、电脑与手机预览及研究者结果页面仍可在浏览器中使用。 [制作问卷所需的应用](../../../SUPPORTED-ENVIRONMENTS(zh-CN).md).
<!-- /GREEDYQ_DESKTOP_POLICY -->

[English](./guide.md) · [한국어](./guide(kor).md)

生成包含 `survey.qmd` 与 `app.R` 的原生 surveydown 兼容项目，作为重要的次级输出。greedyQ 的 Vercel/Supabase 运行时仍为主要路径。仅依照公开文档和行为，不复制 surveydown 源码、测试或内部示例。

逐项标为直接可移植、生成实现、greedyQ 专用或不支持。准确核对显示文字与保存值。用日常语言说明改变或无法导出的行为，重要差异须经批准。需要超出 greedyQ 支持范围的高级定制时，推荐原生 surveydown。

所有 greedyQ 专用控件（`audio`、`video`、`rank_order`、`side_by_side`、`nps`、`timing`、`constant_sum`、`pick_group_rank`、`drill_down` 及确认的 `custom`）必须用公开的 `sd_question_custom()` 接口替换原 QMD 的 `sd_question()` 块，并在 `app.R` 生成对应 Shiny 输出和响应值绑定。不得留下未知的 greedyQ 类型。在原生环境实际审阅前，将转换标为 `generated_custom` 与 `generated_unverified`，不能仅因代码生成就声称行为完全相同。

兼容报告须列出每道转换题、仍为 greedyQ 专用的行为及所有重要差异。浏览器确定性运行时保持主要地位。
