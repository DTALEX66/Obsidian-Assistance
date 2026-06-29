# Obsidian Assistance — Scripts

## 流水线脚本（按执行顺序）

| # | 脚本 | 功能 | 依赖 |
|---|------|------|------|
| 01 | `01_scan_course_materials.ps1` | 扫描课程目录，统计文件类型，标记风险文件 | PowerShell 5.1+ |
| 02 | `02_ocr_pipeline.py` | PDF 转图片 → OCR → JSON 输出 | poppler, tesseract, pytesseract |
| 03 | `03_asr_pipeline.ps1` | 音频/视频 → whisper 转写 → txt | ffmpeg, openai-whisper |
| 04 | `04_integrity_check.ps1` | 对比原始素材 vs 转写/OCR 结果，输出完整性报告 | — |
| 05 | `05_obsidian_prepare.ps1` | 汇总转写+OCR文本，生成写入计划（等待确认） | — |
| 06 | `06_obsidian_write.ps1` | 确认后写入 Obsidian 正式库 | Obsidian vault 路径 |

## Obsidian UI 增强

| 文件 | 用途 |
|------|------|
| `obsidian-dashboard.css` | 首页总控台、知识卡片网格、状态卡、进度条 |
| `obsidian-knowledgeos-styles.css` | 同上（别名，内容一致） |

## 使用说明

所有 .ps1 文件已添加 UTF-8 BOM，PowerShell 中运行不会乱码。
所有脚本均有 -SourceDir 参数，可重复运行。

## 数据边界

- 脚本不读写 Obsidian 正式库（06 除外，需要用户确认和 -Force）
- 脚本不上传任何内容到 GitHub
- 脚本不修改原始资料目录（E:\学习数据）
