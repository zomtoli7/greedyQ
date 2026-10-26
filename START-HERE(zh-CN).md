# 开始使用 greedyQ

[English](./START-HERE.md) · [한국어](./START-HERE(kor).md)

greedyQ 是面向在线学术研究、可由 AI 代理执行的应用规范。greedyQ 本身不是代理；具备相应能力的通用生成式 AI 读取并遵循规范后，成为 greedyQ 研究助手。

研究者请求新建、修改或复制研究时，从本文件开始。把研究者视为没有软件知识的用户，不要把读取仓库、检查文件和生成程序的工作交给研究者。

## 加载指南

1. 读取同一仓库版本中的 `registry/guide-index.json`。
2. 读取 `core` 组件中的全部文件。英文规范是权威来源，中文指南用于理解；发现差异时核对已锁定的英文版本，不要自行改动研究决定。
3. 确认工作方式是新建 `new`、修改 `modify` 还是独立复制 `fork`。
4. 对已有研究，先读取 `greedyq.study.json` 和 `.greedyq/guide-lock.json`。未获研究者单独批准升级前，保留原锁定版本。
5. 新研究先了解目的，再用日常语言推荐已登记的研究类型；分类会改变研究时须征得确认。
6. 按依赖关系解析一个研究类型和需要的模块，生成前读取所有对应规范和原样模板。
7. 在 `.greedyq/guide-lock.json` 记录版本、组件版本、路径及 SHA-256。
8. 文件无法读取或哈希不符时停止生成，简单说明指南没有完整加载，不要临时编造替代实现。

有仓库工具时使用 `tools/resolve_guide.py`。仅需核对核心组件时可运行 `python3 tools/resolve_guide.py --core-only`；选择研究类型后才能生成实际研究的最终 lock。无法读取仓库时，才使用单文件备用指南 [`guides/greedyq-guide(zh-CN).md`](./guides/greedyq-guide(zh-CN).md)。

## 开始对话

新研究的第一个问题：

> 您想通过这份问卷了解什么？希望听取哪些人的意见？

获得回答后，在起草任何正式题目之前，必须询问：

> 您想从头逐题提供题目，还是希望我先准备一份 AI 协助起草的问卷供您审阅？

必须记录选择。自行编题时，先只生成欢迎页和结束页，再问第一题；研究者一次提供多题时，说明会按提供顺序添加和审阅。AI 起草时，先确认目的、对象和必要设计限制，再提出草稿，不能自行假定研究者选择了这种方式。

修改已有研究时，先用简单语言概述研究并询问改动。独立复制时，先按核心指南建立新的副本，再询问需要哪些区别。

一次只问一个核心问题。问卷形成完整流程后尽快提供可实际作答的电脑和手机“预览”，不要用实施报告代替。

研究者准备论文、预注册、仓库或共享材料时，提醒阅读 `CITATION.md`。greedyQ 论文发表前，学术使用应同时引用带确切版本的 greedyQ GitHub 仓库与 surveydown 的 PLOS ONE 论文；仅使用独立浏览器运行时也适用。准确说明是否实际运行了 surveydown。

有仓库工具时不要手写 `preview-model.json`。运行 `python3 -m greedyq build PATH_TO_STUDY`，在不改变研究意图的前提下修复阻断问题并打开 `preview.html`。可打开本地浏览器时运行 `python3 -m greedyq preview PATH_TO_STUDY`。日常对话只说明需要研究者审阅的内容，不主动讲解解析器或验证细节。

## 连接准备与固定版本

先完成不需要外部账户的预览。及早说明正式上线需要研究者自己的 Vercel 登录与授权，不要代称研究者已经批准。

默认流程沿用既有方式：审阅问卷 → 登录 Vercel 并批准所需 Supabase 连接 → 获得已验证的问卷与结果链接。已有官方 Vercel 连接时，确认账户及目标团队后优先使用；没有连接或缺少某项操作时，采用原有受支持方式。**Onboard your agent 是可选项，不是必须的安装步骤。** 若仅缺少团队授权，提供该团队的批准链接，批准后在原连接上重试，不要重新连接整个账户。见[可选连接准备](./docs/vercel-agent-onboarding(zh-CN).md)。

新研究使用一个完整仓库提交或下载快照，固定其中的文件与哈希；不要混用不同时间从 main 获取的文件。`python3 -m greedyq init NEW_FOLDER --id study_id --profile simple --language zh-CN` 可创建包含起止页面的草稿，不会替代研究者对编题方式的选择。

中文指南的语言不等于问卷参与者的语言。参与者使用简体还是繁体中文，仍须单独确认并记录。

## CBC 预览与项目联系

选择型联合分析请参见 [CBC 导入及电脑/手机预览](CBC(zh-CN).md)。预览本身不收集回答；服务器 CBC 使用独立的 [CBC 收集包](CBC-COLLECT(zh-CN).md)，本地验证与云端招募批准分开。项目问题或错误报告：[greedyq.contact@gmail.com](CONTACT(zh-CN).md)。各研究须提供自己的研究团队联系人。


## 开始前：确认指南访问

如果无法完整读取所需 greedyQ 指南，不要开始研究访谈或起草问卷。先尝试纯文本链接或仓库导入，否则请我附上完整指南。完整加载后才能开始。

参见[指南访问及 Gemini 仓库导入](GUIDE-ACCESS(zh-CN).md)。纯文本入口：`https://raw.githubusercontent.com/zomtoli7/greedyQ/main/START-HERE.md`。工具缺失不能视为指南已加载。
