# V4 安全写入与回滚

## 目标

通过安全写入层防止误写正式 vault、路径穿越、未备份覆盖和删除操作。

## 写入规则

- 默认 dry-run。
- 显式 `--apply` 才写入。
- 所有目标路径必须位于指定 vault/output 根目录内。
- 覆盖已有文件前必须备份。
- 禁止删除用户文件。

## 回滚原则

- 首选 `git revert <commit>` 回滚辅助仓库。
- Demo/test 输出可以重新生成。
- 对 vault 的应用必须依赖备份复制覆盖，不写自动删除式回滚。

## 执行要求

安全写入脚本不得包含 `shutil.rmtree`、`os.remove`、`Path.unlink`、`Path.rmdir`。

## 验收标准

测试覆盖 dry-run、apply、备份、路径穿越、中文路径。

## 安全边界

- 本规范只服务辅助仓库，不要求写入正式 Obsidian vault。
- 文档中不得包含真实课程正文、原始素材、转写全文、OCR 全文、token 或 API key。
- 所有示例路径必须使用占位符或 demo 路径，不能依赖用户正式库路径。

