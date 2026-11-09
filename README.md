# 免费大模型平台导航 | Free LLM Platforms Hub

一个单文件静态网页，收录**国内外 14 个可免费接入的大模型 API 平台**与**15 项可领取的免费额度**，并附模型能力 / 价格对照，帮你判断「能不能接进代码」和「免费模型大概能干什么」。

## 查看方式

- **在线查看**：https://821920046.github.io/free-llm-platforms-hub/ （GitHub Pages）
- **本地查看**：双击打开 `index.html`，无需任何依赖或服务器

## 三个板块

1. **平台卡片**：14 家平台，标注免费方式、代表免费模型、OpenAI 兼容性、官网 / 文档链接
2. **免费额度羊毛榜**：15 项额度，按每日 5 / 每月 4 / 限时 6 分类，每条标注额度、适用模型、限制条件、核实日期与领取链接；其中 11 项标注「可当 API 用」
3. **模型能力参考**：引用 AIHOT 综合榜 8 个代表模型，附实测评分条与输入 / 输出价，用于对照免费额度的能力位置

另有 14 行「平台快速对比」表格。

## 收录平台

| 地区 | 平台 |
| --- | --- |
| 国内（7） | 硅基流动 SiliconFlow、智谱 AI BigModel、DeepSeek、腾讯云混元、百度千帆、讯飞星火、魔搭社区 ModelScope |
| 国际（7） | OpenRouter、Google AI Studio (Gemini)、Groq、Mistral AI、NVIDIA NIM、AMD Token Factory、Cloudflare Workers AI |

## 页面功能

- 全局搜索框：按平台名、模型名、额度关键词实时过滤，并显示结果计数
- 两组独立筛选：平台（全部 / 国内 / 国际）、额度（全部 / 每日 / 每月 / 限时 / 仅 API 可用）
- 无匹配结果时给出空状态提示
- 纯 HTML + 内嵌 CSS/JS，无外部依赖，移动端自适应

## 数据来源

- [AIHOT · Token 羊毛](https://aihot.news/free-tokens)：额度、限制条件与核实日期（2026-11-08 ~ 11-09 核实）
- [AIHOT · 大模型排行榜](https://aihot.news/leaderboard)：模型实测评分与价格（54 项评测 / 16 家机构，2026-11-09 20:05 更新）
- [free-llm-resources](https://github.com/cheahjs/free-llm-resources)：47 家提供商、210+ 免费模型，用于查漏补缺

> 免费政策、额度与截止时间随时可能调整；「可当 API 用」与「限产品内使用」差别很大，领取与接入前请以各平台官方说明为准。
