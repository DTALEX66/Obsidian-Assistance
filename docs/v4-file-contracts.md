# V4 文件契约

## 目标

定义 V4 每类文件必须满足的结构、字段和用途，避免脚本输出不一致。

## Markdown 文件契约

- 必须包含 YAML frontmatter。
- 必须包含 `type`、`status`、`course`、`confidence`、`created`、`updated`。
- 必须包含 `cssclasses`，至少含 `knowledgeos-v4`。
- 不允许大段真实课程原文。

## Canvas 文件契约

- 文件扩展名为 `.canvas`。
- JSON 顶层必须包含 `nodes` 和 `edges`。
- 每个 node 必须有 `id`、`type`、`x`、`y`、`width`、`height`。

## CSS 文件契约

- 只能作用于 `.knowledgeos-v4` 或其子类。
- 不允许外部 URL。
- 不允许全局污染 `body`、`html`。

## 报告文件契约

- 报告必须说明目标、输入、输出、风险、自测结果。
- 失败报告必须包含复现命令和建议修复。

## 执行要求

生成器必须按本文件契约输出，测试必须覆盖这些契约。

## 验收标准

`python scripts/v4/validate_yaml_schema.py <dir>` 能通过核心 Markdown 文件检查。

## 安全边界

- 本规范只服务辅助仓库，不要求写入正式 Obsidian vault。
- 文档中不得包含真实课程正文、原始素材、转写全文、OCR 全文、token 或 API key。
- 所有示例路径必须使用占位符或 demo 路径，不能依赖用户正式库路径。

