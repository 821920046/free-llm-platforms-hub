# FREE LLM HUB · 免费大模型平台导航

单文件静态站点：收录 **14 个可免费接入的大模型 API 平台**、**15 项免费额度**、**22 张厂商卡册**与 **TOP 30 模型排行榜**。深色科技风视觉，榜单由 GitHub Actions 自动同步，页面零外部依赖。

## 查看方式

- **在线**：https://821920046.github.io/free-llm-platforms-hub/ （GitHub Pages，榜单自动保持最新）
- **本地**：双击 `index.html`，无需依赖或服务器；离线时自动回退到内置榜单快照

## 视觉与交互

- **深色科技风**：网格背景、霓虹渐变光晕、玻璃拟态卡片、发光描边、扫描线、等宽数字；右上角可切换**浅色主题**（本机记忆）
- 22 枚厂商官方 Logo 内联为 data URI，断网可见，统一出现在厂商卡册、平台卡片标题、快速对比表首列
- 全局搜索 + 三组独立筛选、卡册点选联动筛选与打卡、排行榜表头排序、结果计数与空状态提示
- 移动端自适应，支持 `prefers-reduced-motion`

## 榜单自动更新

AIHOT 没有公开 API，本站用「定时抓取 + 前端拉取」把静态页面做到接近实时：

| 环节 | 实现 |
| --- | --- |
| 抓取 | `scripts/update_leaderboard.py` 解析 AIHOT 综合榜服务端渲染的表格，提取 30 个模型的名次、厂商、上线日期、评测覆盖、缓存/输入/输出价、评分，以及官网更新时间、评测数、机构数、汇率日期；含名次连续、评分递减等校验，纯标准库无第三方依赖 |
| 数据文件 | `data/leaderboard.json`，内容无变化时不写文件，避免定时任务刷提交 |
| 定时任务 | `.github/workflows/update-leaderboard.yml` 每 6 小时运行（UTC 0:20 / 6:20 / 12:20 / 18:20，覆盖北京时间 20:06 的日更），也可在 Actions 页手动触发；失败重试 3 次，仍失败则任务报错并保留上一份数据 |
| 离线快照 | 抓到新数据后由 `scripts/sync_snapshot.py` 同步 `index.html` 内的 `SNAPSHOT`，保证「下载 HTML 离线打开」也拿到同一份数据 |
| 页面 | 打开时 `fetch('./data/leaderboard.json')` 拉最新数据；成功显示绿色 **LIVE** 状态，失败（`file://`、离线、网络故障）回退内置快照并显示琥珀 **SNAPSHOT**。状态条展示官网更新时间、距今多久、评测数、模型数，支持「立即刷新」，新鲜度每分钟重算 |

> 「实时」= 官网更新后最多约 6 小时同步到线上，不是秒级推送。免费额度、平台政策与核实日期仍为人工维护的快照，请以各平台官方说明为准。

本地手动同步一次：

```bash
python scripts/update_leaderboard.py
python scripts/sync_snapshot.py
```

## 页面板块

1. **厂商卡册**：22 张紧凑小卡，含额度值、官方 Logo、厂商名、稀有度、×N 收录数；彩色渐变描边表示稀有度，灰度虚线表示「限产品内使用」；点卡片联动筛选，点左上角圆点记录「已领」（localStorage）
2. **平台卡片**：14 家平台，标注免费方式、代表免费模型、OpenAI 兼容性、官网 / 文档链接
3. **免费额度羊毛榜**：15 项额度，按每日 5 / 每月 4 / 限时 6 分类，含限制条件、核实日期与领取链接；11 项「可当 API 用」
4. **模型排行榜 TOP 30**：AIHOT 综合榜全 30 名，含厂商、上线日期、评测覆盖、输入 / 输出价、评分条与「与免费额度的关系」；支持国产 / 开源 / 免费相关筛选及表头排序
5. **平台快速对比**：14 行表格，一屏看清各平台差异

## 收录平台

| 地区 | 平台 |
| --- | --- |
| 国内（7） | 硅基流动 SiliconFlow、智谱 AI BigModel、DeepSeek、腾讯云混元、百度千帆、讯飞星火、魔搭社区 ModelScope |
| 国际（7） | OpenRouter、Google AI Studio (Gemini)、Groq、Mistral AI、NVIDIA NIM、AMD Token Factory、Cloudflare Workers AI |

## 项目结构

```
index.html                                单文件页面（内嵌 CSS/JS/Logo/榜单快照）
data/leaderboard.json                     定时任务生成的榜单数据
scripts/update_leaderboard.py             抓取与校验
scripts/sync_snapshot.py                  同步页面内离线快照
.github/workflows/update-leaderboard.yml  定时同步工作流
README.md
```

## 数据来源

- [AIHOT · 大模型排行榜](https://aihot.news/leaderboard)：评分、评测覆盖、价格与榜单元信息（最近同步：2026-11-11 20:06，56 项评测 / 16 家机构，美元按 2026-11-10 汇率折算）
- [AIHOT · Token 羊毛](https://aihot.news/free-tokens)：额度、限制条件、核实日期与卡册视觉参考
- [free-llm-resources](https://github.com/cheahjs/free-llm-resources)：47 家提供商、210+ 免费模型，用于查漏补缺
- 厂商 Logo：各平台官网 favicon / 官方品牌资源，部分国际厂商使用 [Simple Icons](https://simpleicons.org)

> 免费政策、额度与截止时间随时可能调整；「可当 API 用」与「限产品内使用」差别很大。评分只反映第三方实测表现，不代表免费额度可用性。
