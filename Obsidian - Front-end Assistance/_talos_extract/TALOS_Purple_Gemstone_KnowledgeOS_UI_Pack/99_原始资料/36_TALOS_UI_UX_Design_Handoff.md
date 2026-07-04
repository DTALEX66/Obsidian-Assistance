---
title: TALOS UI/UX 设计师交接包
type: talos-ui-ux-design-handoff
status: active
created: 2026-07-04
updated: 2026-07-04
tags: [talos, ui, ux, design-handoff, purple-gemstone]
cssclasses: [talos-purple-gemstone, knowledgeos-v5, talos-nocode-page, talos-global-page]
---

# TALOS UI/UX 设计师交接包

> [!summary] 给设计师的任务边界
> 这是 Obsidian KnowledgeOS / TALOS 的 UI 与交互设计交接清单。设计师负责 **界面、信息架构、交互状态、组件规范、Figma 原型与视觉系统**；不负责改课程内容、移动源文件、伪造证据或实现插件逻辑。

## 0. 当前产品状态

| 项目 | 当前值 |
|---|---:|
| 正式课程门户 | 30 |
| 已有视觉索引课程 | 29 |
| 已有真实截图/关键帧/PDF页图课程 | 16 |
| 已有项目转化课程 | 30 |
| 已有 OER 交叉对比课程 | 4 |
| 复习卡片/复习中心文件 | 92 |
| TALOS 相关入口页 | 26 |

## 1. 设计总目标

| 目标 | 说明 |
|---|---|
| TALOS 系统控制台感 | 像一个深紫黑的知识作战系统，不是普通文件夹列表。 |
| Purple Gemstone 风格 | 深黑/蓝黑背景、紫晶发光边框、玻璃拟态卡片、柔和高光、细线框、圆角面板。 |
| Obsidian 原生可落地 | 设计可以落到 Obsidian Markdown、Callout、Table、Dataview、Canvas、Kanban、CSS snippet，不依赖大段 HTML。 |
| 证据优先 | 任何“课程证据”界面都必须显式显示来源、页码、时间戳、验证状态，避免把参考图/OER/AI摘要伪装成证据。 |
| 高效学习闭环 | 入口应支持：课程阅读 → 证据核验 → 主动回忆 → 项目转化 → 执行日志。 |
| 不依赖左侧原始文件树 | 通过 Home、Bookmarks、导航矩阵、课程卡墙、领域地图提供使用层。 |

## 2. 设计师需要输出的交付物

| 交付物 | 格式 | 必须包含 |
|---|---|---|
| UI 总览信息架构 | Figma FigJam / 流程图 | 全局壳层、主页、课程、证据、复习、项目、OER、睡觉模式入口关系。 |
| Purple Gemstone Design System | Figma Variables / Styles | 色彩、字体、间距、圆角、阴影、发光、边框、状态色、图标风格。 |
| Obsidian Shell 视觉稿 | Figma Frames | Ribbon、左侧导航、顶部 tabs/search、正文区、右侧 Inspector、状态栏。 |
| 核心页面高保真 | Desktop 1440/1600 优先 | Home Console、Course Reader、Evidence Matrix、Review + AI、Project Atlas、Kanban、Visual Dashboard。 |
| 交互原型 | Figma Prototype | 页面跳转、卡片 hover、筛选、搜索、弹窗、抽屉、图片预览、复习卡评分、任务状态变化。 |
| 组件库 | Figma Components | Cards、Buttons、Badges、Tables、Callouts、Panels、Toast、Modal、Menu、Search、Progress、Heatmap、Gallery。 |
| 响应式规范 | Breakpoint Frames | 1680、1440、1280、1040、760、520px；禁止窄屏竖排挤压。 |
| 实现标注 | Dev Notes | 对应 Obsidian 组件/Markdown/CSS 选择器，说明哪些可做、哪些只是原型。 |

## 3. 信息架构：所有可设计界面环节

### 3.1 全局 Obsidian 壳层

| 界面 | 设计内容 | 交互 |
|---|---|---|
| 左侧 Ribbon | 图标组、当前激活态、悬停发光、禁用态 | 点击切换 File/Bookmarks/Search/Graph/Calendar/Tasks；hover 显示 tooltip。 |
| 左侧导航/Bookmarks | TALOS 分组、课程分组、证据分组、复习分组 | 折叠/展开、当前页高亮、长标题省略、搜索过滤。 |
| 文件树 | 不作为主要入口，但要美化 | hover、active、folder collapse、拖动边界、长中文路径安全显示。 |
| 顶部标题栏与 Tabs | 活动 tab、未激活 tab、关闭按钮、tab overflow | 切换、关闭、固定、拖拽重排、窄屏收缩。 |
| 全局搜索/Quick Switcher | 搜索框、建议列表、匹配高亮 | 输入、键盘上下选择、Enter 打开、空状态、无结果状态。 |
| Command Palette | 命令搜索、最近命令、危险命令提示 | 键盘导航、确认、Esc 关闭。 |
| 右侧 Inspector | Properties、Backlinks、Graph、AI 建议、Evidence meta | 折叠/展开、面板切换、固定、滚动同步。 |
| 底部 Status Bar | vault 状态、模式、同步/提交、证据边界提示 | 状态 hover、错误提示、点击打开日志。 |
| 右键菜单/更多菜单 | 文件/标题/卡片上下文菜单 | 新建、复制链接、打开证据、加入复习、创建任务。 |
| Modal/Prompt/Suggestion | 弹窗、确认、输入建议 | 关闭、确认、危险动作二次确认、加载/错误态。 |

### 3.2 TALOS Home Console

| 模块 | 设计内容 | 交互 |
|---|---|---|
| Hero Command Bar | 标题、搜索、主入口链接、当前系统建议 | 全局搜索、快捷入口、今日建议展开。 |
| Command Center 指标卡 | Review、OER、Projects、Evidence 四类指标 | 点击跳转、hover 展示二级信息、状态色变化。 |
| Workspace Navigation 三栏 | Navigation / Operating Queue / Inspector | 三栏转两栏/单栏，自适应，链接可点击。 |
| Recent Focus | 当前建议、下一步动作、边界提示 | 任务展开、复制任务、跳转日志。 |
| Status Strip | Vault、Mode、Theme、Guardrail | 显示当前运行模式与安全边界。 |

### 3.3 课程系统界面

| 界面 | 设计内容 | 交互 |
|---|---|---|
| 课程库总览 | 课程表、领域、状态、证据/项目/OER 标记 | 搜索、筛选、排序、点击课程。 |
| 课程卡片墙 | 课程卡、封面图、进度、标签、操作按钮 | hover lift、点击进入、筛选领域、显示证据状态。 |
| 领域仪表盘 | 设计/AI/学习力/运营等领域入口 | 领域切换、展开课程列表。 |
| 单课程门户 | Hero、模块矩阵、学习路线、证据入口、项目入口 | 模块跳转、学习进度、收藏、加入复习。 |
| Course Reader | 左侧目录、正文阅读、右侧属性/证据/卡片 | 阅读进度、目录定位、证据预览、双栏/单栏切换。 |
| 课程视觉索引 | 参考图墙、生成图、真实图分类 | 图片放大、来源查看、标记“非证据/verified”。 |
| 真实截图与关键帧页 | 视频帧/PDF页图、来源路径、时间戳、页码 | Lightbox、复制来源、跳转源课程页、验证状态 badge。 |

### 3.4 证据系统界面

| 界面 | 设计内容 | 交互 |
|---|---|---|
| Evidence Matrix | verified / pending / missing 指标矩阵 | 过滤 verified、pending、missing；点击课程进入证据页。 |
| 证据热力图 | 课程×证据类型热力图 | hover 查看数量/来源，点击打开细节。 |
| 视觉覆盖仪表盘 | 实际图片嵌入、路径提及、视觉索引类型 | 排序、筛选“仅参考图/真实图/PDF页图”。 |
| 图片证据浏览器 | 缩略图网格、证据类型、来源 metadata | 图片预览、左右切换、复制 Obsidian embed。 |
| Rejected/待核验队列 | 不匹配帧、错误帧、待源核验 | 查看原因、重新抽帧、标记为 rejected/verified。 |

### 3.5 Review + AI 学习界面

| 界面 | 设计内容 | 交互 |
|---|---|---|
| Review Overview | Retention、Streak、Due Cards | 点击进入复习队列。 |
| 今日问题卡 | 问题、证据提示、Show Answer | 展开答案、跳证据、加入错题日志。 |
| 评分条 | Again / Hard / Good / Easy | 键盘快捷键、点击评分、反馈动画。 |
| AI Assistant | Chat、Summarize、Connect、Plan 四入口 | 输出建议但必须提示“回本地证据核验”。 |
| Daily Mission | 今日复习、项目动作、证据补全 | 勾选、推迟、完成、写入日志。 |
| 错题/复盘日志 | 错因、证据、下一次复习 | 添加标签、关联课程、生成任务。 |

### 3.6 Project Atlas / Kanban / 项目推进

| 界面 | 设计内容 | 交互 |
|---|---|---|
| Project Atlas | Canvas 节点、连线、分组、右侧属性 | 缩放、拖拽节点、选择节点、打开详情。 |
| 项目 Kanban | 阶段列、课程项目卡、状态 badge | 拖拽卡片、状态转换、打开项目转化页。 |
| 项目推进台 | 项目指标、下一动作、风险 | 标记完成、创建日志、链接课程来源。 |
| 项目详情抽屉 | 背景、目标、证据、下一步、输出物 | 右侧 drawer 展开/关闭、复制任务。 |

### 3.7 OER / 开放知识交叉验证界面

| 界面 | 设计内容 | 交互 |
|---|---|---|
| OER 覆盖率仪表盘 | 课程覆盖、来源类型、许可证/状态 | 筛选来源、查看缺口、打开交叉对比。 |
| OER Crosswalk | 本地课程 vs OpenStax/MDN/Wikimedia/MIT OCW 等 | 对比展开、证据边界提示。 |
| FAQ 问题驱动入口 | 问题、上下文、答案线索、采纳标准 | 搜索问题、按标签筛选、跳课程/OER来源。 |
| 来源可信度标记 | 官方/社区/未知/不可访问 | hover 解释、警告状态。 |

### 3.8 睡觉模式 / 自动循环控制台

| 界面 | 设计内容 | 交互 |
|---|---|---|
| Sleep Mode Console | 当前轮次、边界、任务队列、最近提交 | 暂停/继续/停止状态展示；不需要真实按钮也要有设计状态。 |
| 执行日志 | 时间线、提交、校验结果、阻塞 | 筛选轮次、展开日志、复制 resume point。 |
| 自动复盘汇总 | 完成率、失败原因、下一轮建议 | 点击查看报告、生成下一轮队列。 |
| 安全边界提示 | 不上传、不删源、不伪造、不移动课程 | 固定警示、危险状态红色提示。 |

### 3.9 插件与 Obsidian 原生组件

| 组件 | 设计内容 | 交互/状态 |
|---|---|---|
| Dataview 表格 | 表头、排序、行 hover、空状态 | 排序、筛选、加载中、错误 query。 |
| Tasks | checkbox、完成线、due date、priority | 勾选、延期、过滤完成/未完成。 |
| Kanban 插件 | 列、卡片、拖拽占位、标签 | 拖拽、卡片菜单、空列。 |
| Calendar | 月/周/日、选中日期、今日高亮 | 切换月份、点击日期打开 Daily。 |
| Canvas | 节点、边、缩放工具、minimap | 选中、拖拽、缩放、连线。 |
| Excalidraw | 画布、工具栏、图形选择态 | 编辑、缩放、导出提示。 |
| Properties | 属性行、标签、多值、空值 | 编辑、添加属性、错误类型。 |
| Graph / Backlinks | 节点、链接、引用列表 | hover highlight、点击打开。 |
| File embed / Image embed | 图片墙、PDF 页图、视频帧 | 预览、放大、复制 embed、加载失败。 |

## 4. 组件库清单

| 组件族 | 组件 |
|---|---|
| Navigation | Sidebar item、Breadcrumb、Tab、Top search、Command palette item、Bookmark group。 |
| Data Display | Stat card、Metric strip、Badge、Tag、Progress bar、Heatmap cell、Evidence status chip。 |
| Content | Hero callout、Panel callout、Warning callout、Course card、Evidence card、Project card、Review card。 |
| Inputs | Search input、Filter chip、Segmented control、Checkbox、Rating button、Toggle、Date selector。 |
| Overlays | Modal、Drawer、Tooltip、Context menu、Toast、Image lightbox。 |
| Tables | Dashboard table、Dataview table、Evidence table、Responsive overflow table。 |
| Media | Thumbnail grid、Image preview、PDF page preview、Video keyframe card、Rejected frame card。 |
| AI/Review | AI message bubble、Suggestion card、Show answer panel、Again/Hard/Good/Easy buttons。 |

## 5. 状态设计清单

| 状态 | 必须设计 |
|---|---|
| Default | 正常可点击/可阅读。 |
| Hover | 紫晶边框增强、轻微抬升、文字变亮。 |
| Active/Selected | 左侧发光条、背景高亮、状态 chip。 |
| Focus | 键盘可访问焦点环。 |
| Loading | 骨架屏/轻量 shimmer，避免强闪烁。 |
| Empty | 无课程、无证据、无复习任务、无搜索结果。 |
| Error | Dataview query 失败、图片丢失、PDF 渲染失败、来源不可访问。 |
| Warning | OER 不是证据、参考图不是课程证据、候选帧未核验。 |
| Verified | 真实截图/关键帧/PDF页图；显示来源路径、页码/时间戳。 |
| Rejected | 视觉不匹配或错误帧；显示剔除原因。 |
| Disabled | 不允许上传/删除/移动/伪造的操作。 |
| Narrow Screen | 表格横向滚动，三栏降两栏/单栏，禁止竖排文字。 |

## 6. 核心用户路径

### 路径 A：日常学习

1. 打开 Home Console。
2. 看今日建议与 Review 指标。
3. 进入 Review + AI。
4. 回答今日问题。
5. 打开证据页核验。
6. 评分 Again/Hard/Good/Easy。
7. 写入 Daily Mission / 执行日志。

### 路径 B：课程阅读

1. 课程库总览或课程卡片墙搜索课程。
2. 打开课程门户。
3. 进入 Course Reader。
4. 左侧目录定位模块。
5. 右侧 Inspector 查看属性、证据、复习卡。
6. 打开真实截图/关键帧/PDF页图。
7. 生成复习卡或项目动作。

### 路径 C：证据核验

1. 打开 Evidence Matrix 或视觉覆盖仪表盘。
2. 筛选 pending/missing/reference-only。
3. 进入课程证据页。
4. 查看图片、来源路径、页码/时间戳、视觉核验说明。
5. 标记 verified / rejected / pending source。
6. 返回仪表盘刷新状态。

### 路径 D：项目转化

1. 打开 Project Atlas 或 Project Kanban。
2. 按课程/领域筛选项目卡。
3. 查看项目详情抽屉。
4. 打开对应课程证据和项目转化页。
5. 标记下一步动作。
6. 写入执行日志。

### 路径 E：睡觉模式监控

1. 打开睡觉模式执行台。
2. 查看当前轮次、队列、边界。
3. 查看执行日志和提交。
4. 遇到阻塞进入报告页。
5. 用户停止/继续后显示明确 resume point。

## 7. 页面优先级

| 优先级 | 页面/界面 | 原因 |
|---|---|---|
| P0 | Obsidian 全局壳层 | 决定整体专业度和“不是普通文件夹”的第一印象。 |
| P0 | Home Console | 主入口，承载系统感和日常路径。 |
| P0 | Course Reader | 用户真实长时间阅读区，必须舒适、不卡、无竖排。 |
| P0 | Evidence Matrix + 图片/PDF页图浏览 | 证据驱动是核心差异。 |
| P0 | Review + AI Center | 主动训练层，是 KnowledgeOS 价值闭环。 |
| P1 | Course Library/Card Wall/Domain Dashboard | 提升课程浏览与选择效率。 |
| P1 | Project Atlas/Kanban | 课程转项目、任务推进的工作区。 |
| P1 | Visual Coverage Dashboard | 监控纯文字/配图/真实证据升级。 |
| P1 | Sleep Mode Console/Execution Log | 让自动循环可见、可控、可信。 |
| P2 | OER Crosswalk/FAQ | 辅助学习，不可盖过本地证据。 |
| P2 | Plugin QA/No-Code Audit/Pixel Audit | 内部质量页面，可做轻量但要统一风格。 |

## 8. 已存在 TALOS 页面清单

| 文件 | 类型 | 设计用途 |
|---|---|---|
| [[00_TALOS_Home_Console|TALOS Home Console]] | talos-home-console | 可作为设计稿的信息架构参考。 |
| [[01_TALOS任务雷达|01_TALOS任务雷达]] | talos-radar | 可作为设计稿的信息架构参考。 |
| [[02_TALOS证据矩阵|TALOS 证据矩阵]] | talos-evidence-matrix | 可作为设计稿的信息架构参考。 |
| [[03_TALOS项目推进台|03_TALOS项目推进台]] | talos-project-console | 可作为设计稿的信息架构参考。 |
| [[04_TALOS课程指挥舱|04_TALOS课程指挥舱]] | talos-course-command | 可作为设计稿的信息架构参考。 |
| [[05_TALOS系统日志|05_TALOS系统日志]] | talos-system-log | 可作为设计稿的信息架构参考。 |
| [[06_TALOS领域作战地图|06_TALOS领域作战地图]] | talos-field-command-map | 可作为设计稿的信息架构参考。 |
| [[07_TALOS项目Kanban|TALOS 项目 Kanban]] | talos-project-kanban | 可作为设计稿的信息架构参考。 |
| [[08_TALOS证据热力图|08_TALOS证据热力图]] | talos-evidence-heatmap | 可作为设计稿的信息架构参考。 |
| [[09_TALOS主动训练中心|09_TALOS主动训练中心]] | talos-active-training-center | 可作为设计稿的信息架构参考。 |
| [[10_TALOS每日任务生成器|TALOS Daily Mission — {{date}}]] | talos-daily-mission-generator | 可作为设计稿的信息架构参考。 |
| [[11_TALOS执行日志|11_TALOS执行日志]] | talos-execution-log | 可作为设计稿的信息架构参考。 |
| [[13_TALOS训练复盘雷达|TALOS 训练复盘雷达]] | talos-training-streak-radar | 可作为设计稿的信息架构参考。 |
| [[14_TALOS自动复盘汇总|14_TALOS自动复盘汇总]] | talos-retro-summary | 可作为设计稿的信息架构参考。 |
| [[15_TALOS开放知识交叉对比|15_TALOS开放知识交叉对比]] | talos-open-knowledge-crosswalk | 可作为设计稿的信息架构参考。 |
| [[16_TALOS睡觉模式执行台|16_TALOS睡觉模式执行台]] | talos-sleep-mode-console | 可作为设计稿的信息架构参考。 |
| [[17_TALOS界面导航矩阵|17_TALOS界面导航矩阵]] | talos-interface-index | 可作为设计稿的信息架构参考。 |
| [[18_TALOS_OER覆盖率仪表盘|TALOS OER 覆盖率仪表盘]] | talos-oer-coverage-dashboard | 可作为设计稿的信息架构参考。 |
| [[28_TALOS设计系统|TALOS Purple Gemstone 设计系统]] | talos-design-system | 可作为设计稿的信息架构参考。 |
| [[29_TALOS_Project_Atlas|TALOS Project Atlas]] | talos-project-atlas | 可作为设计稿的信息架构参考。 |
| [[30_TALOS_Review_AI_Center|TALOS Review + AI Center]] | talos-review-ai-center | 可作为设计稿的信息架构参考。 |
| [[31_TALOS_Course_Reading_Layout|TALOS Course Reading Layout]] | talos-course-reading-layout | 可作为设计稿的信息架构参考。 |
| [[32_TALOS_Workspace_QA|32_TALOS_Workspace_QA]] | talos-ui-qa | 可作为设计稿的信息架构参考。 |
| [[33_TALOS_Plugin_Component_QA|33_TALOS_Plugin_Component_QA]] | talos-plugin-component-qa | 可作为设计稿的信息架构参考。 |
| [[34_TALOS_NoCode_Audit|34_TALOS_NoCode_Audit]] | talos-nocode-audit | 可作为设计稿的信息架构参考。 |
| [[35_TALOS_Pixel_Parity_Audit|35_TALOS_Pixel_Parity_Audit]] | talos-ui-qa | 可作为设计稿的信息架构参考。 |

## 9. 实现约束，设计师必须知道

| 约束 | 说明 |
|---|---|
| Obsidian 原生优先 | 最终大部分要落为 Markdown、Callout、Table、Dataview、CSS snippet。不要设计必须依赖复杂前端框架的交互。 |
| 禁止 raw HTML 外露 | 页面不应依赖大段 HTML；如果设计要复杂布局，交给 CSS snippet 或插件实现。 |
| 不移动课程文件 | 设计使用层可以重组入口，但不能要求移动 `02_课程库/**` 里的正式课程结构。 |
| 参考图与证据分离 | `参考配图` 只改善视觉；`真实截图/关键帧/PDF页图` 才是证据。界面必须清楚区分。 |
| 本地优先 | 源材料、证据路径、本地 Git 是可信根；OER/AI 只辅助。 |
| 窄屏安全 | 不能出现英文/中文被挤成竖排、卡片重叠、表格溢出遮挡。 |
| 性能优先 | 少用高频动画和重玻璃模糊；长表格和图片墙要可滚动/分页/懒加载。 |
| 中英混排 | 页面会出现中文课程名、英文术语、文件路径；要设计长文本截断和 tooltip。 |

## 10. 响应式断点建议

| 宽度 | 布局 |
|---|---|
| 1680+ | 完整三栏：左导航 + 主内容 + 右 Inspector。 |
| 1440 | 三栏压缩，右侧 Inspector 变窄。 |
| 1280 | 主内容优先，右侧 Inspector 可折叠。 |
| 1040 | 两栏：左导航窄栏 + 主内容；右侧内容下移。 |
| 760 | 单栏，导航变顶部/折叠入口。 |
| 520 | 移动安全：只保留核心卡片、表格横向滚动、图片单列。 |

## 11. 验收标准

| 验收项 | 标准 |
|---|---|
| 视觉一致性 | 全局壳层、主页、课程页、证据页、复习页都符合 Purple Gemstone。 |
| 可点击性 | 主要入口都能用 Obsidian 链接/Bookmarks/命令打开。 |
| 无代码外露 | 阅读视图不出现 HTML/CSS/脚本代码块。 |
| 证据边界可见 | 参考图、OER、AI 摘要、真实证据的状态明显区分。 |
| 表格/卡片不挤压 | 窄屏下横向滚动或单列，不出现竖排错位。 |
| 交互状态完整 | hover、active、loading、empty、error、warning、verified、rejected 都有设计。 |
| 可实现 | 每个组件都能映射到 Obsidian 原生元素、CSS snippet 或明确插件。 |
| 性能可接受 | 动画克制、图片可控、不要让 Obsidian 卡顿。 |

## 12. 设计师可以直接开始的 Figma 文件结构

```text
TALOS Purple Gemstone UI
├── 00 Cover & Product Principles
├── 01 IA / User Flows
├── 02 Foundations / Tokens
├── 03 Obsidian Shell
├── 04 Home Console
├── 05 Course Library + Reader
├── 06 Evidence Matrix + Media Viewer
├── 07 Review + AI Center
├── 08 Project Atlas + Kanban
├── 09 OER + Sleep Mode Console
├── 10 Native Plugin Components
├── 11 Responsive Frames
└── 12 Dev Notes / Obsidian Mapping
```

## 13. 交接备注

- 这不是普通网页产品，而是 **Obsidian vault 的使用层 UI**。
- 设计师可以大胆做视觉与交互，但需要给出“Obsidian 可实现降级方案”。
- 核心风格参考：Purple Gemstone、系统控制台、AI Study Companion、Canvas/Graph/Inspector、证据驱动知识库。
- 最终实现优先用 CSS snippet 和 Markdown 页面，不优先做独立 Web App。
