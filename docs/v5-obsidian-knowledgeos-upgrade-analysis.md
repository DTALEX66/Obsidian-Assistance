# V5 Obsidian KnowledgeOS 全方位升级分析

> 本文只针对 Obsidian 知识库本身升级：信息架构、模板、MOC、Dashboard、Dataview、CSS、Talos-like 中控。暂不落地 Hermes/CC/Codex 工作流。

## 1. 当前项目已有能力

| 层 | 已有资产 | 评价 |
|---|---|---|
| V4 课程包 | `templates/v4/`、`scripts/v4/generate_course_pack.py` | 已有课程级生成底座 |
| 安全写入 | `safe_vault_writer.py`、dry-run/apply、备份 | 可复用到未来真实 vault 安装 |
| 可视化 | Canvas、Mermaid、V4 CSS snippets | 偏课程 demo，还不是全库中控 |
| 测试 | `tests/v4/`、GitHub Actions | 安全边界较好 |
| 文档 | V4 规范 + fullchain roadmap | 有规划，但 V5 资产不足 |

## 2. 缺口

1. **通用知识库模板不足**：V4 偏课程卡片，缺标准笔记、MOC、Dashboard、健康度、领域主页、卡片墙模板。
2. **Talos-like 中控未落地**：只有路线图，没有 dashboard 规格、CSS、demo。
3. **Dataview 使用层不足**：V4 有 Dataview block，但缺全库健康/项目/领域/卡片级 dashboard 契约。
4. **CSS 作用域需要升级**：旧 KnowledgeOS snippet 容易覆盖主题；V5 应使用 `.knowledgeos-v5` 和 `.talos-*` 作用域。
5. **没有模板质量测试**：需要测试 frontmatter、占位符、Dataview、CSS 作用域和禁止私有路径。

## 3. 设计取舍

### 吸收

- Linear：深色、克制、低噪声、卡片层级、细边框、命令中心感。
- Supabase：状态绿、开发者控制台、边框层级、简洁深色。
- Sentry：可观测性、健康度、信号面板、异常/风险可视化。
- Talos-like：总览、热力图、信号、能力中心、作战室、模块页。
- Dataview：动态表格/列表/分组，用于健康度和 MOC 自动索引。

### 不吸收

- 大面积渐变和高饱和装饰。
- 全局 CSS 覆盖主题。
- 未核验 Talos 项目作为依赖。
- 一次性移动正式 vault 目录结构。
- 插件化工作流和外部 AI 调度链路。

## 4. V5 KnowledgeOS 资产结构

```text
docs/
  v5-obsidian-knowledgeos-upgrade-analysis.md
  v5-talos-ai-os-dashboard-spec.md
  research/obsidian-knowledgeos-upgrade-evidence.md

templates/obsidian/
  standard-note.md
  moc.md
  dashboard-home.md
  knowledge-health-dashboard.md
  course-card-wall.md
  domain-home.md

snippets/v5/
  talos-dashboard.css

examples/v5-talos-dashboard/
  README.md
  50_Dashboard/今日工作台_Talos.md
  50_Dashboard/知识库健康度_Talos.md
  40_Wiki/MOC/MOC_示例主题.md

tests/v5/
  test_obsidian_knowledgeos_assets.py
```

## 5. 推荐安装到正式 vault 的方式

正式 vault 不从 GitHub 直接同步。未来应使用安全写入器：

1. dry-run 生成写入计划；
2. 只安装模板、CSS snippet、demo dashboard；
3. 覆盖前备份；
4. 不移动旧笔记；
5. 不删除旧 dashboard；
6. 用户确认后再 `--apply`。
