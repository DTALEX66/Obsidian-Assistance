# V4 测试计划

## 目标

用自动化测试证明 V4 不会误写 vault、不生成非法 YAML/Canvas/Mermaid、不泄露隐私。

## 测试范围

- safe_vault_writer。
- YAML schema。
- course pack generator。
- Canvas generator。
- Mermaid generator。
- no private data scan。

## 必测项

- dry-run 不写文件。
- apply 写文件。
- 覆盖前备份。
- 路径穿越阻止。
- 中文路径可用。
- Canvas JSON 可解析。
- Mermaid 文件含代码块。
- 不含 token/API key。
- 不含硬编码正式库路径。

## 执行要求

使用 `python -m pytest tests -q`。失败时生成 `reports/test-failure-v4.md`。

## 验收标准

所有安全相关测试必须通过，不允许跳过。

## 安全边界

- 本规范只服务辅助仓库，不要求写入正式 Obsidian vault。
- 文档中不得包含真实课程正文、原始素材、转写全文、OCR 全文、token 或 API key。
- 所有示例路径必须使用占位符或 demo 路径，不能依赖用户正式库路径。
