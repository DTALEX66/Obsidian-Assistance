# TALOS 页面优先级与验收清单

## P0 必做页面

| 页面 | 验收重点 |
|---|---|
| Obsidian 全局壳层 | Ribbon、左导航、tabs/search、右侧 Inspector、状态栏统一紫晶风格 |
| Home Console | 主入口清晰，Review/Evidence/Projects/OER 一眼可见 |
| Course Reader | 长时间阅读舒适，右侧能看属性、证据、复习卡 |
| Evidence Matrix | verified/pending/missing/reference-only 明确区分 |
| Review + AI Center | 今日问题、答案、评分、AI核验提示完整 |

## P1 增强页面

| 页面 | 验收重点 |
|---|---|
| Course Library/Card Wall | 能搜索、筛选、排序、显示证据状态 |
| Project Atlas/Kanban | 课程转项目，卡片可推进 |
| Visual Coverage Dashboard | 监控纯文字/配图/真实证据升级 |
| Sleep Mode Console/Execution Log | 自动循环有轮次、边界、阻塞、resume point |

## P2 辅助页面

| 页面 | 验收重点 |
|---|---|
| OER Crosswalk/FAQ | 辅助学习，不盖过本地证据 |
| Plugin QA/No-Code Audit/Pixel Audit | 内部质量页，风格统一即可 |

## 总体验收标准

- 全局壳层、主页、课程页、证据页、复习页都符合 Purple Gemstone。
- 主要入口都能用 Obsidian 链接/Bookmarks/命令打开。
- 阅读视图不出现无意义 HTML/CSS 代码。
- 参考图、OER、AI 摘要、真实证据的状态明显区分。
- 窄屏下横向滚动或单列，不出现竖排错位。
- hover、active、loading、empty、error、warning、verified、rejected 都有设计。
- 每个组件都能映射到 Obsidian 原生元素、CSS snippet 或明确插件。
- 动画克制、图片可控、不会拖慢 Obsidian。
