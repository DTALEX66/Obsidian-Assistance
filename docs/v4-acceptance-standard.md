# V4 最终验收标准

## 目标

定义 V4 工程完成的最终可验收条件。

## 验收清单

- Batch 0-8 全部完成。
- `reports/repo-audit-v4.md` 存在。
- 10 个 V4 文档存在。
- `templates/v4/` 模板完整。
- `snippets/v4/` CSS 完整。
- `scripts/v4/` 安全写入层与生成器完整。
- `examples/v4-demo-course/` 完整。
- `tests/v4/` 完整。
- README 有 V4 使用说明。
- `reports/hermes-v4-delivery-report.md` 存在。
- `python -m pytest tests -q` 通过。

## 安全验收

- 没有真实课程内容。
- 没有 token/API key。
- 没有硬编码正式库路径。
- 没有删除用户文件逻辑。
- 所有写入默认 dry-run。
- `--apply` 前会备份。

## 执行要求

交付报告必须逐项说明完成状态和未完成事项。

## 验收标准

用户可以只看 README 和交付报告，独立运行 demo 生成与测试。

## 安全边界

- 本规范只服务辅助仓库，不要求写入正式 Obsidian vault。
- 文档中不得包含真实课程正文、原始素材、转写全文、OCR 全文、token 或 API key。
- 所有示例路径必须使用占位符或 demo 路径，不能依赖用户正式库路径。

