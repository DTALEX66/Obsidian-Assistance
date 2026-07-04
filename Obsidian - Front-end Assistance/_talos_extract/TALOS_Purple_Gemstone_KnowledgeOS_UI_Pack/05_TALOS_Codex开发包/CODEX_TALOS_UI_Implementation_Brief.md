# CODEX：TALOS Purple Gemstone UI 实施任务包

## 0. 任务目标

把 `TALOS_Purple_Gemstone_KnowledgeOS_UI_Pack` 安装到 Obsidian Vault，并在不移动课程源文件、不伪造证据的前提下，完成 UI 使用层搭建。

## 1. 禁止动作

- 禁止删除 Vault 之外的文件。
- 禁止移动 `02_课程库/**` 正式课程结构。
- 禁止把参考配图、OER、AI 摘要写成 verified 证据。
- 禁止大规模重命名源课程文件。
- 禁止在没有备份前覆盖 `.obsidian` 配置。

## 2. 实施步骤

1. 备份 `.obsidian/snippets`。
2. 复制 `.obsidian/snippets/talos-purple-gemstone-knowledgeos.css`。
3. 确认 CSS snippet 可启用。
4. 复制 `00_TALOS_入口`、`01_TALOS_核心页面`、`02_TALOS_模板`、`03_TALOS_Canvas`。
5. 建立 Bookmarks：Home、Course、Evidence、Review、Project、Sleep。
6. 检查所有内部链接是否能打开。
7. 检查 Dataview 查询失败时页面仍可阅读。
8. 检查 1680、1440、1280、1040、760、520px 下不出现竖排与遮挡。
9. 输出安装日志到 `11_TALOS执行日志`。

## 3. 插件建议

- 必装：Dataview、Tasks、Calendar、Templater、Style Settings。
- 增强：Homepage、Commander、QuickAdd、Kanban、Excalidraw。
- AI：Smart Connections / Copilot / 本地 Ollama 接入。

## 4. 第一阶段不做

- 不写复杂插件。
- 不改 Obsidian 核心。
- 不做 Web App。
- 不做云同步。

## 5. 第二阶段插件化方向

- TALOS Home View：自动聚合 Review/Evidence/Projects/OER。
- Evidence Inspector：右侧显示来源、页码、时间戳、状态。
- Review Scheduler：真实 Again/Hard/Good/Easy 调度。
- Guardrail Status Bar：显示不上传、不删源、不伪造、不移动课程。
- Theme Settings：通过 Style Settings 调整紫色、圆角、密度。
