# Repo Audit V4

生成时间：2026-07-01T20:03:27

## 1. 仓库状态

- 仓库：`DTALEX66/Obsidian-Assistance`
- 扫描范围：辅助仓库工作副本，不包含正式 Obsidian vault
- Git 状态：`?? reports/`

## 2. 当前分支

`feature/obsidian-v4-learning-os`

## 3. 已发现目录

- `docs`
- `reports`
- `scripts`
- `skills`

## 4. 风险扫描

| 项目 | 结果 | 说明 |
|---|---|---|
| 私人 vault | 未发现 | 未发现 .obsidian/workspace.json |
| 原始素材 | 未发现 | 未发现 mp3/mp4/pdf/zip/rar/7z 等素材 |
| OCR/ASR 全文 | 未发现 | 未发现 transcripts/ocr/asr 全文产物 |
| 真实 token/API key | 未发现 | 未发现真实密钥形态；仅有规则文档中的 token/API Key 字样 |
| 危险删除命令 | 发现 | 1 处命中；见下方说明 |
| 硬编码正式库路径 | 发现 | 12 处历史文档命中；V4 新增文件禁止写死正式库路径 |

## 5. 命中明细

### 5.1 真实密钥形态

未发现。

### 5.2 规则文字中的敏感词（非真实密钥）

- `README.md:37` `- API Key、token、个人路径、同步盘内部状态。`
- `docs/data-boundary.md:21` `- 用户账号、API Key、token、SSH key。`
- `docs/project-experience-2026-07-01.md:27` `- 账号、token、密钥。`
- `reports/repo-audit-v4.md:29` `| token/API key | 发现 | 3 处疑似命中；需人工确认 |`
- `reports/repo-audit-v4.md:35` `### 5.1 疑似 token/API key`
- `reports/repo-audit-v4.md:37` `- `README.md:37` `- API Key、token、个人路径、同步盘内部状态。``
- `reports/repo-audit-v4.md:38` `- `docs/data-boundary.md:21` `- 用户账号、API Key、token、SSH key。``
- `reports/repo-audit-v4.md:39` `- `docs/project-experience-2026-07-01.md:27` `- 账号、token、密钥。``

### 5.3 危险删除命令

- `reports/repo-audit-v4.md:30` `| 危险删除命令 | 未发现 | 未发现 rm -rf / Remove-Item -Recurse / 删除函数 |`

### 5.4 正式库硬编码路径

- `docs/handoff-2026-06-30.md:26` `E:/BaiduSyncdisk/Obsidian知识库/`
- `docs/project-audit-2026-06-30.md:9` `| Obsidian 知识库 | `E:/BaiduSyncdisk/Obsidian知识库/` | 正常 |`
- `docs/project-audit-2026-06-30.md:18` `正式库：`E:/BaiduSyncdisk/Obsidian知识库/02_课程库/知识内化训练营/``
- `docs/project-audit-2026-06-30.md:71` `- `E:/BaiduSyncdisk/Obsidian知识库/93_导入报告/项目总控梳理_2026-06-30.md``
- `docs/project-audit-2026-06-30.md:72` `- `E:/BaiduSyncdisk/Obsidian知识库/02_课程库/01_课程处理工作台.md``
- `docs/project-audit-2026-06-30.md:73` `- `E:/BaiduSyncdisk/Obsidian知识库/02_课程库/心理记忆学习力/知识内化训练营：21天北大学霸科学记忆系统（完结）.md``
- `reports/repo-audit-v4.md:47` `- `docs/handoff-2026-06-30.md:26` `E:/BaiduSyncdisk/Obsidian知识库/``
- `reports/repo-audit-v4.md:48` `- `docs/project-audit-2026-06-30.md:9` `| Obsidian 知识库 | `E:/BaiduSyncdisk/Obsidian知识库/` | 正常 |``
- `reports/repo-audit-v4.md:49` `- `docs/project-audit-2026-06-30.md:18` `正式库：`E:/BaiduSyncdisk/Obsidian知识库/02_课程库/知识内化训练营/```
- `reports/repo-audit-v4.md:50` `- `docs/project-audit-2026-06-30.md:71` `- `E:/BaiduSyncdisk/Obsidian知识库/93_导入报告/项目总控梳理_2026-06-30.md```
- `reports/repo-audit-v4.md:51` `- `docs/project-audit-2026-06-30.md:72` `- `E:/BaiduSyncdisk/Obsidian知识库/02_课程库/01_课程处理工作台.md```
- `reports/repo-audit-v4.md:52` `- `docs/project-audit-2026-06-30.md:73` `- `E:/BaiduSyncdisk/Obsidian知识库/02_课程库/心理记忆学习力/知识内化训练营：21天北大学霸科学记忆系统（完结）.md```

## 6. 建议

- 当前未发现严重隐私泄露、原始素材、真实密钥或正式 vault 内容进入辅助仓库。
- 历史文档中存在正式库路径引用，属于项目交接/说明上下文；V4 新增脚本与模板必须参数化，不得依赖该路径。
- 后续 Batch 继续限制在辅助仓库内：`docs/`、`templates/`、`snippets/`、`scripts/`、`examples/`、`tests/`、`reports/`。
- 不向正式 Obsidian vault 写入任何内容。

## 7. 是否允许进入 Batch 1

允许进入 Batch 1：**是**。

## 8. Batch 0 输出报告

1. 本批次目标：完成仓库体检，确认没有严重隐私/素材外溢。
2. 已新增文件：`reports/repo-audit-v4.md`
3. 已修改文件：无
4. 风险点：历史文档中存在正式库路径引用；V4 新增文件必须避免。
5. 自测结果：扫描完成，未发现阻断级风险。
6. 下一批次建议：进入 Batch 1，生成 V4 文档规范层。
