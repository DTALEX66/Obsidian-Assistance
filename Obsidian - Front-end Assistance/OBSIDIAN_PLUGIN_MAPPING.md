# TALOS × Obsidian 插件能力映射

## 边界

- 本报告只基于用户粘贴的插件目录名。
- 不读取 `.obsidian` 插件配置正文。
- 不写入 `D:\BaiduSyncdisk\Obsidian知识库`。
- 不上传课程内容、插件配置、索引或附件。
- 后续若需要真实接入，应先在当前项目生成插件规格，再由用户决定是否复制到 Vault。

## 插件分层

### P0：TALOS 核心数据与操作层

| 插件 | TALOS 用途 | 对应页面 |
|---|---|---|
| `dataview` | 查询课程、证据卡、复习状态、项目索引 | `evidence-matrix.html`, `index.html` |
| `templater-obsidian` | 生成 Course / Evidence / Daily Mission / Review 模板 | `course-reading.html`, Daily Mission |
| `quickadd` | 快速捕获摘记、创建证据卡、写入收件箱 | `course-reading.html`, Home Console |
| `obsidian-meta-bind-plugin` | 在笔记中提供可交互字段、按钮、状态切换 | `course-reading.html`, `evidence-matrix.html` |
| `obsidian-tasks-plugin` | 任务、执行日志、每日任务筛选 | Home Console, 执行日志 |
| `obsidian-kanban` | 项目推进台和证据审核队列 | 项目 Kanban, `95_待审核` |
| `obsidian-spaced-repetition` | 复习卡片和 Review AI 队列 | Review AI Center, `04_复习卡片` |
| `omnisearch` | 全库检索、证据定位、课程片段查找 | 全局搜索, Course Reading |

### P1：智能增强层

| 插件 | TALOS 用途 | 约束 |
|---|---|---|
| `copilot` | Review AI、课程摘要、证据卡草稿建议 | 不自动上传课程内容；需要用户确认模型与隐私设置 |
| `smart-connections` | 语义关联、知识卡片推荐、Project Atlas 连接 | 先匹配索引和标签，不默认读取全文 |
| `text-extractor` | 从 PDF / 图片附件提取课程材料 | 只对用户指定文件执行，不批量处理附件 |
| `obsidian-excalidraw-plugin` | Project Atlas、知识图谱、课程概念草图 | 适合生成 Canvas / 图谱视图，不替代证据矩阵 |

### P2：体验、维护与系统层

| 插件 | TALOS 用途 | 约束 |
|---|---|---|
| `calendar` | 日志日期入口、学习日历 | 可连接 `01_收件箱` 与 Daily Notes |
| `periodic-notes` | 日报、周报、复盘周期 | 对应 Daily Mission 与 Review |
| `obsidian-git` | Vault 版本备份 | 不自动 commit / push；只作为用户手动备份能力 |
| `obsidian-style-settings` | 紫晶主题参数和密度配置 | 可映射 TALOS 设计系统 token |
| `table-editor-obsidian` | 表格编辑和证据矩阵维护 | 辅助 Dataview / Markdown 表 |
| `cmdr` | 自定义命令入口 | 可承载 TALOS 命令面板 |
| `lang-plus` | 代码块、语法、语言增强 | 支撑 Dataview / 模板片段可读性 |

## 页面级映射

### `course-reading.html`

目标：从课程库读取片段，生成 Evidence Card 草稿。

推荐插件组合：

- `quickadd`：一键创建课程摘记或证据卡。
- `templater-obsidian`：套用课程阅读模板。
- `obsidian-meta-bind-plugin`：状态、来源、证据强度、下一步按钮。
- `dataview`：显示相关课程、相关证据、待复习卡片。
- `omnisearch`：查找课程库中的相似片段。
- `text-extractor`：只在用户指定 PDF / 图片附件时提取材料。
- `copilot` / `smart-connections`：作为可选智能建议层，不默认上传内容。

应保留的 HTML 原型语义：

- Vault 左栏 → Obsidian 文件树。
- Markdown / Live Preview 双栏 → 原生编辑区 + 自定义 ItemView。
- Properties 面板 → frontmatter / Meta Bind 字段。
- Evidence Draft → QuickAdd + Templater 生成草稿。

### `evidence-matrix.html`

目标：证据卡筛选、热力图、交叉对比。

推荐插件组合：

- `dataview`：核心查询层。
- `table-editor-obsidian`：手工维护矩阵表。
- `obsidian-meta-bind-plugin`：复核状态、证据强度、项目绑定。
- `quickadd`：从矩阵快速新增证据卡。
- `obsidian-spaced-repetition`：把证据转为复习卡。

### Home Console / `index.html`

目标：总览今日任务、项目推进、课程状态、Review 队列。

推荐插件组合：

- `dataview`：聚合所有目录。
- `obsidian-tasks-plugin`：每日任务和执行日志。
- `calendar` + `periodic-notes`：日期维度和复盘周期。
- `obsidian-kanban`：项目推进台。
- `obsidian-git`：显示备份状态，但不自动提交。
- `cmdr`：命令面板入口。

### Project Atlas / 图谱视图

目标：连接领域知识、课程、项目和证据。

推荐插件组合：

- `obsidian-excalidraw-plugin`：概念图和项目地图。
- `smart-connections`：发现潜在连接。
- `dataview`：按 frontmatter 聚合。
- `omnisearch`：跨库检索。

### Review AI Center

目标：复习卡片、AI 辅助复盘、下一步行动。

推荐插件组合：

- `obsidian-spaced-repetition`：复习卡核心。
- `copilot`：生成复盘建议，需用户确认隐私设置。
- `obsidian-tasks-plugin`：复盘后生成行动项。
- `dataview`：按状态聚合待复习卡。

## 推荐实施顺序

1. **先做数据契约**：定义 Course / Evidence / Review / Project 四类 frontmatter。
2. **再做模板**：用 `templater-obsidian` 和 `quickadd` 定义创建入口。
3. **再做索引**：用 `dataview` 驱动 Evidence Matrix 和 Home Console。
4. **再做交互**：用 `meta-bind` 给状态、强度、下一步加按钮。
5. **最后做智能层**：再接 `copilot`、`smart-connections`、`text-extractor`，并逐项确认隐私边界。

## 建议的最小可迁移目标

优先把 `course-reading.html` 转成 Obsidian 插件规格：

- 一个 `CourseReadingView` 自定义视图。
- 一个 `EvidenceCard` Markdown 模板。
- 一个 QuickAdd capture：从当前课程片段生成证据卡草稿。
- 一个 Dataview 查询：显示同课程、同主题、待复习证据。
- 一个 Meta Bind 表单：状态、证据强度、项目绑定、下一步。

## 暂不执行

- 不执行 `96_脚本`。
- 不修改 `.obsidian/plugins`。
- 不自动写入真实课程库。
- 不调用 Copilot / Smart Connections 上传正文。
- 不执行 Git commit / push。
