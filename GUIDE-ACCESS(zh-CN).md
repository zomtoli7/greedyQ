# AI 无法打开指南链接时

[English](./GUIDE-ACCESS.md) · [한국어](./GUIDE-ACCESS(kor).md)

## 已确认的复制粘贴问题

研究者随后复现了失败粘贴：换行丢失，韩文接在地址后成为 `START-HERE.md새`。这次观察到的失败可以由被改变的地址解释，而非标准仓库地址不可用。未对目标应用的剪贴板/富文本内部作探测，不能推论为 Gemini 整个平台不支持网页读取。

网站复制框现优先使用 text/plain，兼容复制及手工选择也输出纯文本。URL 包在 `<...>` 中，行边界保留真实 ASCII 空格，即使丢失换行，也不会把 `.md` 与后面的韩文/中文连接成另一地址。BibTeX 保持原样。更新网站发布后重新复制，或给正确 URL 加 `<...>` 并在后文前留真实空格。下列纯文本、仓库导入、完整附件仍是实际访问失败时的备用方案。

发送链接不等于 AI 已读取内容。如果它说“无法访问网站”却继续生成问卷，请先停止；这并不证明结果遵循了 greedyQ。模型名称或付费订阅不能单独证明网页读取、文件生成、浏览器测试或部署能力。

## 先试纯文本链接

```text
https://raw.githubusercontent.com/zomtoli7/greedyQ/main/START-HERE.md
```

它去掉 GitHub 界面的外围内容，但不能突破客户端本身无法读取链接的限制。仅阅读入口文件不够：还须读取同一版本的 registry、所需指南及固定源码，或完整指南包。不得根据项目名、搜索摘要或第一个访谈问题猜测其余规范。

## Gemini 网页应用

Google 提供独立的仓库导入路径：Add files → More Uploads → Import Code，输入 `https://github.com/zomtoli7/greedyQ`，然后要求 AI 阅读 `START-HERE.md` 及其依赖。菜单和可用性因账户或环境而异。导入仓库与在聊天中粘贴 URL 不同。[Google 官方导入说明](https://support.google.com/gemini/answer/14903178?hl=en)

自建 Gemini API 应用可显式启用 URL Context 工具；提供链接并不证明客户端启用了工具。这不能诊断某次 Gemini Apps 对话的具体故障。[URL Context 文档](https://ai.google.dev/gemini-api/docs/url-context)

## 导入或网页读取不可用时

从 GitHub 下载[英文完整指南](./guides/greedyq-guide.md)、[韩文完整指南](./guides/greedyq-guide(kor).md)或[中文完整指南](./guides/greedyq-guide(zh-CN).md)并附件上传。请使用下载按钮，不要只截图或复制开头。如果不接受 `.md`，可把同一完整 UTF-8 内容保存为 `.txt`，保留嵌入固定代码。简版及 `START-HERE.md` 不能代替完整包。文件太大或被截断时，改用仓库导入或可读取完整包的客户端。

完整加载后，AI 应简要确认并说明真实能力。没有文件生成或代码执行工具的客户端可以讨论研究，但不能声称已构建并测试可用的 greedyQ 应用；生成产物前应提出转交至有代理能力的环境。读取指南不需要先登录外部服务或付费。

## 安全的起始提示

```text
请阅读同一版本的 greedyQ 指南和所有必需文件：
https://github.com/zomtoli7/greedyQ/blob/main/START-HERE.md
如果无法读取，不要开始研究访谈、起草问卷或声称遵循 greedyQ。先尝试纯文本链接、仓库导入或让我附上完整指南。完整加载后才开始，并简要说明实际文件、预览与部署能力。
```

## 此次报告能证明什么

2026 年 10 月 26 日，我们无需登录即可打开 GitHub 页面及纯文本链接，均返回 HTTP 200。截图证明 AI 声称读取失败却继续工作，不能证明当时的原因、工具配置或 Gemini 整个平台的限制。因此修改了复制的起始提示，而非只修改无法读取的网页内部规则。未使用报告者账户重新测试 Gemini Apps。
