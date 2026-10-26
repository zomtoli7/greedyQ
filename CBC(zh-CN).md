# 预览选择型联合分析设计

**开发线：v0.3。** CBC 不属于受支持的 v0.2 发布。现有共享源码发布标识仅记录来源，不代表 CBC 已正式可用。本地虚拟验证与云端／付费验收不同。

<!-- GREEDYQ_DESKTOP_POLICY -->
**使用 greedyQ 创建或修改研究必须使用已安装的 AI 桌面应用。AI 网页应用不在官方支持范围内。** 请从官方提供方下载 ChatGPT 桌面应用或 Claude Desktop。Gemini（包括桌面版）不在官方支持范围内。请启用能读取和创建文件、执行任务的代理功能。安装应用或付费订阅并不保证这些能力。没有所需工具的普通聊天不能用于正式制作。参与者问卷、电脑与手机预览及研究者结果页面仍可在浏览器中使用。 [制作问卷所需的应用](SUPPORTED-ENVIRONMENTS(zh-CN).md).
<!-- /GREEDYQ_DESKTOP_POLICY -->

[English](./CBC.md) · [한국어](./CBC(kor).md)

CBC 让参与者在特征组合之间作选择，例如价格、支持方式不同的课程订阅。**v0.3 预览现可读取、检查设计表，并显示电脑和手机作答界面；此单文件不发送回答，服务器存储与结果见独立 [CBC 收集流程](./CBC-COLLECT(zh-CN).md)。** 现有 v0.2 问卷继续受支持。

## 与 AI 开始

可以说：“我想做选择型联合分析。帮我确定属性和水平，或给我空白表。检查填好的表后，显示电脑和手机预览。” AI 必须先让您选择共同设计、独立填写 CSV/Excel 空白表，或导入已有设计。不得擅自决定方法、填补缺失值或改变设计。

下载[空白 Excel](./drafts/v0.3/cbc/templates/cbc-design-template.xlsx)或[两个 CSV 模板](./drafts/v0.3/cbc/templates/README.md)。Excel 工作表必须名为 `Attributes`、`Design`，首行为表头；用已确认的属性 ID 替换占位表头。`001` 等代码保持文本。仅允许值；拒绝公式、宏、外部链接、合并单元格。空白表需要填写后才能预览。

## 无需安装，体验完整示例

通过 GitHub 下载按钮保存 [cbc-preview.html](./drafts/v0.3/cbc/golden-reference/cbc-preview.html)，再用现代浏览器打开。GitHub 源码页面不执行 HTML。示例包含全部运行代码，无需 Python、Node、Vercel 或 Supabase。Excel 导入需要支持 Web Crypto、DecompressionStream 的现代 Chrome、Edge、Firefox 或 Safari；不支持 Excel 时可用两个 CSV。

虚构课程订阅示例包含四个属性、两个区组，每组四题，每题两个普通选项和“都不选”。它只演示软件，不代表统计高效或获批的研究设计。

自己的设计请选择 `study.design.json` 加一个 XLSX 或两个 CSV，再点击“检查并预览”。请 AI 按您确认的决定准备 JSON，您不必手写。列名和代码必须与设置完全一致。AI 应解释错误并在修改设计前取得确认。

## 可以检查什么

- 电脑、手机窗口是独立的虚拟参与者。手机打开预览时，电脑布局仍保持宽屏；手机窗口最大 390 像素。
- 按已确认的正整数权重分配一个区组。启用随机顺序时，题目与选项只在开始时随机一次，作答、返回、刷新后保留。“都不选”始终最后；新虚拟参与者重新开始。
- 手机用紧凑表格比较两个普通选项；超过两个时使用竖向卡片，避免横向滚动。布局可能影响比较，需研究者审核。
- 未选择而继续时，在题目上方显示提示并移动焦点。“都不选”是明确选择，未回答不能当成“都不选”。
- “查看结构”可检查所有区组。区组切换器只用于研究者预览，不是参与者功能。
- 每个窗口可下载预览 CSV，含已展示选项、实际位置、选择、设计版本与哈希、展示状态。未回答选择留空，none 行的属性代码留空，只含访问过的题。这是虚构浏览器测试资料，不是正式研究数据或完整总体资料。
- 浏览器存储可用时刷新可恢复当前会话。设计哈希改变则使用独立会话。隐私模式、清除存储或文件变化可能使恢复失败；这不是云端备份。
- “退出预览”删除该窗口本地回答与显示顺序，仅保留退出标记，并禁用其 CSV；不会删除已下载的文件。新建虚拟参与者可重试。

结构详情包含水平频数、未使用水平及题内重叠计数，仅为描述信息，不代表统计批准。属性 ID 不得使用 `chosen`、`block_id`、`design_sha256` 等导出管理列名。

## 收集回答

单文件预览仍不发送回答。独立 [CBC 收集流程](./CBC-COLLECT(zh-CN).md)已实现服务器存储、同意、退出、受保护结果及真实/测试长 CSV，并通过本地 PostgreSQL/浏览器验证。现有账户的虚拟回答云端存储、结果、退出及 CSV 已通过测试；新账户连接、付费 CBC 验收仍待完成，线性普通 QMD 可通过 CBC 模块连接；高级分支、原生导出及统计推断仍为独立范围。

## 供代理使用的固定实现

使用 Python 参考 `greedyq/cbc.py`、浏览器实现 `web/greedyq-cbc.js`、固定模板 `templates/browser/cbc-preview.html`，不要为每项研究重写。仅改变经确认的设置和数据表。浏览器用户无需 Python；核心不依赖 Node 或网络下载库。

开发者/代理可执行：

```sh
python3 -m greedyq cbc-validate drafts/v0.3/cbc/golden-reference
python3 -m greedyq cbc-build drafts/v0.3/cbc/golden-reference
# 可选择导入只有值的 Excel，而非两个 CSV。
python3 -m greedyq cbc-build path/to/study --workbook path/to/design.xlsx
```

输出 `cbc-preview.html`，之后可在浏览器直接检查其他本地 CSV/XLSX。Python、JavaScript 生成相同的 `0.3-preview.1` 规范化结果；SHA-256 记录内容与顺序规则，不记录 ZIP 格式。输入仍使用 `0.3-draft.1`、`fielding_approval=false`，不代表可正式收集。参见[规格](./drafts/v0.3/cbc/spec.md)和[验证记录](./docs/cbc-preview-verification-2026-10-26.md)。

问题与错误报告请使用[项目联系方式](./CONTACT(zh-CN).md)。参与者联系方式由研究团队提供。

## CBC 显示方式

正式收集前与研究者确认外观。固定 greedyQ 运行代码支持**按钮式方案**（点击整个方案选择）和**比较表格**。两者均可横向、纵向或电脑横向／手机纵向。例如：“电脑上按钮方案并排，手机上纵向排列。”这只是显示决定，不改变区组分配、题序、方案代码、均不选择及保存选择的含义。

代理在 `study.design.json` 中记录可选设置：

```json
"presentation": {"type": "buttons", "orientation": "responsive"}
```

`type` 为 `buttons` 或 `table`；`orientation` 为 `horizontal`、`vertical` 或 `responsive`。预览双屏上方也提供相同选择。更改会生成不同的设计哈希及独立虚拟会话，须重新审阅参与体验，部署前重建并注册已审阅收集计划。已注册计划不能静默修改。省略设置则保留原布局与哈希。小屏幕明确选择横向时比较区域可内部横向滚动；纵向及手机响应式无需页面横向滚动。预览选择不会修改已部署问卷。

显示类别参考公开的 [surveydown 按钮式](https://surveydown.org/templates/conjoint_buttons)与[表格式](https://surveydown.org/templates/conjoint_tables)，代码独立实现，没有复制其源码。这是 greedyQ CBC 设置，并不表示可与原生 surveydown 联合分析代码互换。


## 问卷中的 CBC 模块

请使用 [CBC 模块指南](./CBC-MODULE(zh-CN).md)。普通问题保留在 survey.qmd，按研究者要求的位置插入 CBC，无需另写前测／后测问卷。当前支持线性问卷中的一个 CBC 序列。
