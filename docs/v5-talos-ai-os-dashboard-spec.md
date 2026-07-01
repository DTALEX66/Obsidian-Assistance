# V5 Talos-like Obsidian AI OS Dashboard Spec

> 目标：把 Obsidian 从“笔记树 + 插件列表”升级为一个可操作的 KnowledgeOS 中控台。本文只定义知识库 UI/信息架构，不落地 AI 工作流。

## 1. 设计原则

- **Storage layer 与 Usage layer 分离**：原始文件树负责存储，Dashboard/MOC/Bookmarks 负责使用入口。
- **少色高质感**：深色底、细边框、低透明卡片、一个主色、状态色语义化。
- **所有数字可追溯**：不要假进度，不要写死统计；能 Dataview 查就动态查，不能查就标注“待统计”。
- **作用域 CSS**：所有样式挂在 `.knowledgeos-v5` 或 `.talos-dashboard` 下，避免主题切换无效。
- **模块化页面**：总览、健康、课程、领域、卡片、复习、信号分别成页。

## 2. 页面地图

```text
50_Dashboard/
  今日工作台_Talos.md        # 总览页
  知识库健康度_Talos.md      # 健康度/异常/待处理
  课程作战室_Talos.md        # 课程处理/课程卡片墙
  AI运行记录_Talos.md        # 仅展示日志，不负责工作流执行
  信号面板_Talos.md          # 最近更新、阻塞、待审核

40_Wiki/MOC/
  MOC_<主题>.md              # 主题入口

02_课程库/
  02_课程卡片墙.md           # 全课程卡片入口
  <领域>/00_领域主页.md      # 领域主页
```

## 3. 总览页结构

1. Hero：当天焦点、知识库状态、快速入口。
2. Stat cards：笔记数、课程数、待审核、最近更新、健康风险。
3. Command cards：课程库、知识卡片、复习中心、领域地图、导入报告。
4. Signal panel：最近变更、阻塞项、待补来源、待人工确认。
5. Heatmap placeholder：后续可由脚本/Dataview 填充。
6. Recent activity：最近修改笔记。

## 4. 健康度页结构

- 缺 YAML 的笔记。
- 状态为 blocked/needs-review 的笔记。
- 最近 7 天修改。
- 空文件或近空文件。
- 未归属 MOC 的候选。
- 大文件/性能风险候选。

## 5. 视觉 Token

```css
--ko-bg: #08090a;
--ko-panel: rgba(255,255,255,0.035);
--ko-panel-2: rgba(255,255,255,0.055);
--ko-border: rgba(255,255,255,0.08);
--ko-text: #f7f8f8;
--ko-muted: #8a8f98;
--ko-accent: #7c3aed;
--ko-good: #22c55e;
--ko-warn: #f59e0b;
--ko-bad: #ef4444;
```

## 6. Dataview 契约

模板只依赖通用字段：

```yaml
type: note|moc|dashboard|course|concept|review|report
status: draft|active|review|done|blocked
created:
updated:
tags: []
related: []
```

避免硬编码真实路径；示例路径只用通用目录：`02_课程库`、`03_知识卡片`、`04_复习卡片`、`93_导入报告`。

## 7. 分阶段落地

### Phase A：Snippet + Markdown Dashboard

- 安装 `snippets/v5/talos-dashboard.css`。
- 复制 `templates/obsidian/dashboard-home.md` 到测试 vault。
- 用 Dataview 动态查数据。

### Phase B：全库使用层

- 领域主页。
- 课程卡片墙。
- 知识卡片总览。
- 复习中心。

### Phase C：插件化候选

本轮不做。等 Markdown + snippet 证明有效后，再考虑 Obsidian 插件。
