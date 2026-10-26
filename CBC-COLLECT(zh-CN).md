# 收集 CBC 回答并查看结果

**开发线：v0.3。** CBC 不属于受支持的 v0.2 发布。现有共享源码发布标识仅记录来源，不代表 CBC 已正式可用。本地虚拟验证与云端／付费验收不同。

<!-- GREEDYQ_DESKTOP_POLICY -->
**使用 greedyQ 创建或修改研究必须使用已安装的 AI 桌面应用。AI 网页应用不在官方支持范围内。** 请从官方提供方下载 ChatGPT 桌面应用或 Claude Desktop。Gemini（包括桌面版）不在官方支持范围内。请启用能读取和创建文件、执行任务的代理功能。安装应用或付费订阅并不保证这些能力。没有所需工具的普通聊天不能用于正式制作。参与者问卷、电脑与手机预览及研究者结果页面仍可在浏览器中使用。 [制作问卷所需的应用](SUPPORTED-ENVIRONMENTS(zh-CN).md).
<!-- /GREEDYQ_DESKTOP_POLICY -->

[English](./CBC-COLLECT.md) · [한국어](./CBC-COLLECT(kor).md)

独立 CBC 流程已实现服务器存储、同意、退出、受保护结果页与 CSV，复用现有 greedyQ 数据表及部署流程。已用虚构参与者在真实本地 PostgreSQL 与电脑/手机浏览器测试；不代表已部署至您的账户或获得招募批准。

## 研究者的步骤

1. 按 [CBC 导入及预览](./CBC(zh-CN).md)选择 AI 协作、独立填 Excel/CSV 或导入已有设计，亲自确认属性、水平、退出选项、区组及顺序。
2. 提供团队名称、研究标题、真实参与说明、联系人、同意版本和数据计划。实际页面须显示全文，不能自动把项目邮箱当成研究联系人。
3. 分别确认问卷、同意、数据计划、部署与招募五项批准。模板、预览或验证通过不等于批准。生产模式需要五项明确为真及真实团队联系人。
4. 需要时登录 Vercel 并批准缺少的 Supabase 权限；优先复用已有官方授权，“Onboard your agent”仍可选。AI 准备两个独立站点：参与者的公开“问卷链接”和研究者的受保护“结果链接”。
5. 从结果页创建授权测试链接，在电脑和手机测试同意、拒绝、都不选、返回、刷新和退出，并核对数据库与 CSV。正式收集期间的测试仍必须标为 Test。
6. 招募须另行批准。继续遵循 Direct/Prolific 规则；平台研究设置、完成路径、补偿和 CBC 付费验收分别检查，不自动招募或付款。

## 参与者流程

先显示经批准的说明与同意。之前不分配区组、顺序或存储/返回 CBC 展示。拒绝后结束且不显示任务。同意记录版本和全文哈希，然后由服务器固定一个区组及题目/选项顺序，仅返回该区组。刷新和返回不会重新随机。

电脑与手机共用预览的固定渲染器。未选择时提示置于题目上方并移焦。下一题等待服务器确认；失败保留上次确认状态，重试使用同一请求 ID，避免已保存但回执丢失时重复前进。刷新恢复确认的进度。连接失败未解决时，不要不断改选或更换导航操作。

退出需要第二次确认，服务器删除成功后才显示回执。删除选择、展示、顺序、分配及参与者同意记录，仅保留已告知的最小会话/平台管理信息。已下载副本不会远程消失。归档或暂停后需联系研究团队按数据计划处理退出。完成时间由服务器首次记录，重试不覆盖。

## 结果与下载

默认显示真实回答；Test responses 为测试，All 有意合并。Source 独立筛选 Direct/Prolific。参与者不能用 `?test=true` 或自定义标志伪装测试。生产研究的测试使用受保护结果页发出的私密 24 小时授权。“重新测试”使用新的虚拟身份，不用于正式招募。

- **回答概览 CSV**：每会话一行，含所选视图中的未完成、拒绝、退出管理信息及 JSON 结构值，用于管理而非主要联合分析。
- **CBC 选择 CSV**：每个服务器提供的任务中每个选项一行，并区分显示确认状态，含普通/退出选项、选择、区组、实际位置、设计版本/哈希、服务器展示/回答时间、来源、测试标志及完成时间。分析准备使用此表。未回答留空，不能当成“都不选”；none 的属性留空；未访问任务不伪造观测；退出/拒绝不导出选择或展示。
- **归档 ZIP**：关闭收集并确认下载后，保留原始结构记录及分开的真实/测试 CBC 长 CSV 和校验值，同时保存批准设计和媒体。下载是私人研究数据，概览可含平台标识。

任务/none 计数只是描述，不是效用、WTP、拟合、统计效率或样本量建议。筛选同时作用于数字和下载；更新失败或过时请求期间禁用下载，空 CSV 仍保留表头。


服务器准备与显示不同：`served_at` 记录任务可提供，`presented_at` 由浏览器渲染回执或明确回答确认。`available` 表示显示未确认，`presented` 表示确认显示但未答，`answered` 表示已有选择。下一页回执丢失不能作为看过该页的证据。长 CSV 保留 available 行供审计，分析确认展示时应排除；渲染确认也不证明人的注意力。

## 代理固定实现

复用 `greedyq/cbc.py`、`web/greedyq-cbc.js`、`web/greedyq-cbc-collection.js`、固定模板和 `tools/cbc_cloud.cjs`，不要重写。`study.design.json` 仍是未经批准的导入合同；收集决定另存 `0.3-collection.1` 的 `collection.json`。[虚构测试设置](./drafts/v0.3/cbc/golden-reference/collection.test.example.json)的联系人和批准不能用于真实研究。

```sh
python3 -m greedyq cbc-package path/to/study --collection path/to/collection.json --output path/to/new-package
```

这是**准备包**，不能整体上传：包含私人 `registered-model.json` 及迁移。参与者 HTML 只含公开描述，不含完整设计。用 `registerCBCStudy` 注册审核后不可变模型，再用 `prepareCBCDeployments` 生成独立、仅含允许文件的 `survey/` 和 `results/`。服务器 Supabase 密钥仅放结果站点服务器环境，参与者只用公开密钥。结果项目的**全部部署、路由和 `/api/results` 都须 Vercel Authentication**，部署后验证未登录被拒绝。

保持 001–008 字节不变，通过迁移账本追加 **009_cbc.sql**；未启用 CBC 的旧 v0.2 不必升级。不得修改已应用迁移或已批准模型；设计、同意、收集模式的重大变更须新研究 ID。`migrate` 只接受原有顺序的八个或末尾追加 009 的九个。不可变 CBC 计划存于 `gq_study_plans`，参与者会话、同意、分配、生命周期及展示/选择结构留在现有七表归档边界，不新增遗漏的参与者表。

RPC 合同 `cbc-1` 包含开始/恢复、同意、服务器分配/展示、revision 检查及幂等步骤、退出。旧 v0.2 写入/创建/恢复不能绕过 CBC 或获取所有区组。以 `cbc:<task_id>` 保存 `kind=cbc` 结构值，ID 保持字符串，设计变化需新哈希与审阅。production 批准是研究者确认，不自动证明伦理批准或科学有效性。


具备浏览器/JavaScript 工具的代理可直接调用 `greedyQCBC.importDesign` 和 `greedyQCBC.collectionModel(cbc, settings, release)`，后者与 Python 参考对照。可将审核模型作为 `model` 传给 `prepareCBCDeployments`，或使用 Python 准备包，无需在研究者 Windows/Mac 上安装 Python。Excel 包可传 `--workbook path/to/design.xlsx`。准备根目录 `.vercelignore` 排除全部文件，并记录包校验 manifest；仅明确分离的发布目录是部署产物。

## 当前边界

这是独立 CBC 包流程，尚非 v0.2 `sd_cbc` 控件或任意 QMD 混合普通问题的流程。原生 surveydown CBC 导出、自动设计优化/推断、新账户 CBC 云验收、付费 CBC 招募仍按[验证记录](./docs/cbc-collection-verification-2026-10-26.md)区分未实现/未验证。不得退化为选择题后声称等价导出；旧 v0.2/Prolific 验证不能代替 CBC 招募验证。

## CBC 显示方式

正式收集前与研究者确认外观。固定 greedyQ 运行代码支持**按钮式方案**（点击整个方案选择）和**比较表格**。两者均可横向、纵向或电脑横向／手机纵向。例如：“电脑上按钮方案并排，手机上纵向排列。”这只是显示决定，不改变区组分配、题序、方案代码、均不选择及保存选择的含义。

代理在 `study.design.json` 中记录可选设置：

```json
"presentation": {"type": "buttons", "orientation": "responsive"}
```

`type` 为 `buttons` 或 `table`；`orientation` 为 `horizontal`、`vertical` 或 `responsive`。预览双屏上方也提供相同选择。更改会生成不同的设计哈希及独立虚拟会话，须重新审阅参与体验，部署前重建并注册已审阅收集计划。已注册计划不能静默修改。省略设置则保留原布局与哈希。小屏幕明确选择横向时比较区域可内部横向滚动；纵向及手机响应式无需页面横向滚动。预览选择不会修改已部署问卷。

显示类别参考公开的 [surveydown 按钮式](https://surveydown.org/templates/conjoint_buttons)与[表格式](https://surveydown.org/templates/conjoint_tables)，代码独立实现，没有复制其源码。这是 greedyQ CBC 设置，并不表示可与原生 surveydown 联合分析代码互换。
