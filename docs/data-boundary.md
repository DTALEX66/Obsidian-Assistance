# 数据边界与防外溢规则

本项目是 Obsidian 辅助项目，不是正式知识库本体。

## 允许进入仓库

- 通用脚本。
- 参数化模板。
- 不含私人内容的流程说明。
- Skill / 插件设计文档。
- 开源对标分析。
- 示例结构和空白样例。

## 禁止进入仓库

- Obsidian 正式 vault 的私人笔记。
- `.obsidian` 真实配置目录。
- `.smart-env` 嵌入索引。
- 原始课程文件。
- ASR/OCR 全文。
- 用户账号、API Key、token、SSH key。
- 含具体私人路径的配置文件。
- 不能公开的课程内容、讲义、截图、字幕。

## 工作流边界

建议保持三层目录：

```text
原始资料目录       只读，不修改
项目工作目录       存放脚本、中间产物、核验报告
Obsidian 正式库    只写最终笔记、卡片、索引、报告
```

仓库只保存“项目工作目录中可复用、可公开、已脱敏”的部分。

## Git 提交前检查

提交前至少检查：

```powershell
git status --short
git diff --cached --stat
git diff --cached --name-only
```

如果出现以下目录或文件类型，应停止提交：

- `.obsidian/`
- `work/`
- `outputs/`
- `transcripts/`
- `ocr/`
- `asr/`
- `*.sqlite`
- `*.mp3`
- `*.mp4`
- `*.pdf`
- `*.zip`

