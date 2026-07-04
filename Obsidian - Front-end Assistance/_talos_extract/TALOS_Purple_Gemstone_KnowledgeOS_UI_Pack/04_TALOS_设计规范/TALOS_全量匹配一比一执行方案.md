# TALOS + Purple Gemstone 全量匹配一比一执行方案

## 0. 合并结论

上一套 Purple Gemstone 组图解决的是“Obsidian 如何变好看”；这份 TALOS 交接包解决的是“好看的界面要服务什么系统”。合并后，产品定义为：

> TALOS KnowledgeOS：Obsidian 原生可落地的知识作战系统，核心闭环是课程阅读 → 证据核验 → 主动回忆 → 项目转化 → 执行日志。

## 1. 图一 Dashboard → TALOS Home Console

| 原图模块 | TALOS 对应 | 执行文件 |
|---|---|---|
| Welcome Hero | Hero Command Bar | `00_TALOS_入口/00_TALOS_Home_Console.md` |
| Recent Notes | Recent Focus | Dataview 查询 |
| Tasks | Operating Queue | Tasks / Daily Mission |
| Reading Queue | 课程阅读队列 | Course Command |
| Plugin Status | Guardrail / Mode / Theme | Status Strip |
| Activity | 执行日志 / 自动复盘 | Execution Log |
| Calendar | Daily Mission | Calendar / Daily notes |

执行方式：使用 Obsidian Callout + Table + Dataview；CSS 负责紫晶玻璃卡片效果。

## 2. 图二 双栏阅读 → TALOS Course Reader

| 原图模块 | TALOS 对应 | 执行方式 |
|---|---|---|
| 左文件树 | Bookmarks / 课程分组 | 原生侧栏美化 |
| 编辑/预览双栏 | 课程正文 + 预览 | Split right 工作区 |
| Outline | 课程目录定位 | Outline 核心插件 |
| Properties | 课程属性 | YAML / Properties |
| Linked Mentions | 相关课程/复习卡 | Backlinks |
| Key Idea 卡片 | 重点证据/主动回忆 | talos callout |

重点：阅读界面必须不卡、舒适、无竖排，右侧必须显示证据与复习入口。

## 3. 图三 Canvas → TALOS Project Atlas

| 原图模块 | TALOS 对应 | 执行文件 |
|---|---|---|
| 中央 Synthesis | TALOS 项目中心 | `03_TALOS_Canvas/TALOS_Project_Atlas.canvas` |
| Research | Course Input | Canvas 节点 |
| Core Concepts | 核心概念 | Canvas 节点 |
| Applications | 项目应用 | Canvas 节点 |
| Experiments | 项目实验 | Canvas 节点 |
| Outcomes | 输出成果 | Canvas 节点 |
| Assets | 证据 / prompt / 文件 | Canvas file node |

执行方式：每个项目复制一份 Canvas，中央节点链接 Project Template。

## 4. 图四 Review + AI → TALOS 主动训练中心

| 原图模块 | TALOS 对应 | 执行文件 |
|---|---|---|
| Review Overview | Retention / Due / Streak | `30_TALOS_Review_AI_Center.md` |
| Question Card | 今日问题卡 | Markdown + details |
| Again/Hard/Good/Easy | 评分条 | 表格/后续插件 |
| AI Assistant | Chat/Summarize/Connect/Plan | AI 面板 |
| Today Progress | Daily Mission | 每日任务模板 |
| Top Topics | 高频主题 | Dataview 标签统计 |

核心规则：AI 输出必须提示“回本地证据核验”。

## 5. 图五 组件库 → TALOS Design System

| 原图模块 | TALOS 对应 | 执行文件 |
|---|---|---|
| 色板 | Tokens | CSS variables |
| Buttons | Inputs / Rating Buttons | CSS + Figma components |
| Widgets | Callout / Panel / Cards | talos callouts |
| Notifications | Toast / Warning / Danger | Callout states |
| Layouts | Shell / Home / Reader / Review | 核心页面 |
| Extra Assets | SVG / Prompt / 参考图 | assets + visual refs |

注意：上一张 OBS Studio 视觉图只保留“紫晶主题母版”的价值，不再按直播软件界面执行。

## 6. 可执行落地分层

| 层级 | 内容 | 技术 | 还原度 |
|---|---|---|---|
| A | 主题、页面、模板、Canvas | CSS snippet + Markdown + Callout + Table | 75%-85% |
| B | 自动数据、任务、复习队列 | Dataview + Tasks + Bases + Kanban | 85%-90% |
| C | 右侧 AI、命令、状态栏、自动聚合 | 自研 Obsidian 插件 | 90%-95% |
| D | 完整像素级壳层 | 自研主题 + 插件 + workspace layout | 95%+ |

## 7. 立即执行动作

1. 启用 `talos-purple-gemstone-knowledgeos.css`。
2. 打开 `00_TALOS_Home_Console.md`。
3. 安装 Dataview、Tasks、Calendar、Templater、Style Settings。
4. 用模板创建课程、证据、复习卡、项目卡。
5. 把 P0 页面固定到 Bookmarks。
6. 用 `TALOS_Project_Atlas.canvas` 作为项目脑图母版。
7. 后续把 `05_TALOS_Codex开发包` 交给 Codex 做插件化。
