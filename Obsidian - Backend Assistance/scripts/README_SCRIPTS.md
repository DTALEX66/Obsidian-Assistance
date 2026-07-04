# Obsidian Assistance — Backend Script Operator Index

本目录是 Hermes 负责的 Obsidian 后端增强脚本入口。仓库只保存可公开、可复用的脚本/模板/脱敏文档；正式 Obsidian vault、原始课程资料、ASR/OCR 全文、媒体文件和私密配置不进入云端仓库。

## 验证入口

在 `Obsidian - Backend Assistance` 目录运行：

```bash
python -m pytest tests -q
python scripts/v4/obsidian_v4_audit.py .
```

在仓库根目录运行跨目录 cloud-boundary 审计：

```bash
python "Obsidian - Backend Assistance/scripts/v4/obsidian_v4_audit.py" .
```

仓库 CI 位于：

```text
.github/workflows/repo-validation.yml
```

## 写入安全约定

- 默认使用 `--dry-run` 或无 `--apply` 的预览模式。
- 只有显式 `--apply` 才允许写文件。
- 写正式 vault 时必须提供 `--vault`，并优先提供 `--backup-dir`。
- 覆盖文件前必须备份；不得删除、移动或复制原始课程资料。
- 候选来源不是证据：`candidate-only` 不得自动升级为 `verified`。
- Demo vault 必须放在 workspace 内，例如：

```text
D:/All projects/Obsidian-Assistance/demo-vaults/OBS-V4-DEMO
```

## V4 — 课程包与安全写入底座

| 脚本 | 作用 | 默认 |
|---|---|---|
| `scripts/v4/generate_course_pack.py` | 生成 demo/规格驱动课程学习包 | dry-run |
| `scripts/v4/safe_vault_writer.py` | vault 安全写入、路径穿越拦截、覆盖前备份 | 库函数/显式写入 |
| `scripts/v4/generate_canvas_map.py` | 生成课程 Canvas 草案 | dry-run |
| `scripts/v4/generate_mermaid_graph.py` | 生成 Mermaid 流程图/脑图/时间线 | dry-run |
| `scripts/v4/generate_bases_views.py` | 生成 Obsidian Bases 视图草案 | dry-run |
| `scripts/v4/validate_yaml_schema.py` | 校验课程包 YAML/frontmatter 约束 | read-only |
| `scripts/v4/obsidian_v4_audit.py` | cloud-boundary、危险删除、secret/大文件审计 | read-only |

常用命令：

```bash
python scripts/v4/generate_course_pack.py --course "V4 Demo课程" --output "examples/v4-demo-course" --dry-run
python scripts/v4/generate_course_pack.py --course "V4 Demo课程" --vault "D:/All projects/Obsidian-Assistance/demo-vaults/OBS-V4-DEMO" --apply
```

## V5 — 课程多样化与视觉/复习补丁

| 脚本 | 作用 | 默认 |
|---|---|---|
| `scripts/v5/course_diversity_audit.py` | 扫描课程是否过度纯文字，统计图片/表格/Mermaid/复习/行动等形态 | read-only |
| `scripts/v5/course_image_evidence_audit.py` | 统计图片证据/关键帧候选与真实嵌入覆盖 | read-only |
| `scripts/v5/generate_course_diversity_pack.py` | 生成课程多样化补丁包 | dry-run |
| `scripts/v5/generate_course_review_cards.py` | 生成独立复习卡 | dry-run |
| `scripts/v5/generate_keyframe_tasks.py` | 生成关键帧采集任务单 | dry-run |
| `scripts/v5/source_candidate_audit.py` | 扫描本地源文件候选，输出候选而非证据 | read-only |

## V6 — 真实证据、PDF 页图与视频关键帧

| 脚本 | 作用 | 默认 |
|---|---|---|
| `scripts/v6/source_discovery_assistant.py` | 为课程定位本地来源候选 | read-only |
| `scripts/v6/pdf_page_snapshot.py` | 从本地 PDF 渲染页图和 metadata | dry-run |
| `scripts/v6/video_keyframe_plan.py` | 生成视频关键帧候选计划 | dry-run |
| `scripts/v6/video_keyframe_extract.py` | 抽取视频关键帧到 PNG + metadata | dry-run |
| `scripts/v6/evidence_index_builder.py` | 从 metadata 构建 `11_证据索引.md` / `12_真实截图与关键帧.md` | dry-run |
| `scripts/v6/visual_index_updater.py` | 更新 `04_关键图表与课件索引.md` | dry-run |
| `scripts/v6/vault_health_radar.py` | 汇总课程证据覆盖度雷达 | read-only |

## V7 — 课程项目化

| 脚本 | 作用 | 默认 |
|---|---|---|
| `scripts/v7/course_project_generator.py` | 生成课程到项目/行动方案的转化页 | dry-run |

## V8 — TALOS 主动训练与复盘

| 脚本 | 作用 | 默认 |
|---|---|---|
| `scripts/v8/daily_mission_generator.py` | 生成每日训练任务日志 | dry-run |
| `scripts/v8/training_streak_radar.py` | 生成训练连续性/复盘雷达 | dry-run |
| `scripts/v8/retro_summary_generator.py` | 汇总阶段复盘 | dry-run |

## V9 — OER / 开放知识交叉对比

| 脚本 | 作用 | 默认 |
|---|---|---|
| `scripts/v9/oer_crosswalk_generator.py` | 生成开放知识交叉对比页、FAQ 入口和可选 OER 样例 | dry-run |

示例：

```bash
python scripts/v9/oer_crosswalk_generator.py --vault "<formal-vault-path>" --course "<course-name>" --sample --dry-run
python scripts/v9/oer_crosswalk_generator.py --vault "<formal-vault-path>" --course "<course-name>" --sample --apply --backup-dir "<external-backup-dir>"
```

## 旧 OCR / ASR 说明

早期 01–06 PowerShell 流水线已不再是主入口。后续若恢复 OCR/ASR ingestion，应先生成 manifest / course spec，再接入 V4–V9 工具链；不得把转写全文、OCR 全文或原始媒体提交到云端仓库。
