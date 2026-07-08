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

## V10 — Cognitive-Loop-OS 能力吸收

| 脚本 | 作用 | 默认 |
|---|---|---|
| `scripts/v10/cognitive_vault_garden.py` | 吸收 Cognitive-Loop-OS 的 auto-tagging / backlinks / knowledge-gardener 思路，对 Obsidian vault 做只读知识花园审计、孤岛笔记发现、薄弱主题雷达、候选连接建议 | read-only |
| `scripts/v10/obs_task_ledger.py` | 吸收 Cognitive-Loop-OS sleep-loop 的 SQLite 任务账本/真实证据规则，为 OBS 课程转化循环记录本地任务；虚拟/预览/dry-run 任务不能计入 done | local-only |
| `scripts/v10/course_transform_ledger.py` | 扫描正式 vault 的课程页、`93_导入报告`、`99_附件` registry，生成“原始来源 → 扫描报告 → 生成资产 → registry → 课程页 → 下一步”总账，并可显式写入 V10 SQLite 任务账本 | read-only / explicit ledger write |
| `scripts/v10/course_intake_adapter.py` | 吸收 Cognitive-Loop-OS multi-format ingestion 思路，统一扫描 PDF/DOCX/PPTX/HTML/图片/音视频源文件并懒加载可选转换引擎 | read-only / candidate-only |
| `scripts/v10/obs_dataview_query.py` | 吸收 Dataview-like DSL，查询 `courses`/`tasks`/`sources` 三张只读虚拟表，支持 WHERE/SORT/LIMIT/LIST/TABLE | read-only |
| `scripts/v10/course_fact_extractor.py` | 吸收 fact_extractor 思路并做中文课程适配，输出术语/事实/图谱边候选 | candidate-only |
| `scripts/v10/course_pipeline_candidate.py` | 吸收 pipeline/cross_reference 思路，串联 tag/summarize/facts/credibility/crossref/fuse，输出 OBS-safe 候选 JSON | read-only / candidate-only |
| `scripts/v10/obs_v10_index_exporter.py` | 把 V10 course/source/task 索引导出为前端/Bridge/Open Design 可消费的轻量 JSON | stdout by default / explicit write |
| `scripts/v10/course_verification_audit.py` | 对全部课程执行本地转化多源交叉识别：正式页、原始源、二次文本抽取、报告、视觉资产、OER，未多源印证则 `needs_review` | read-only / conservative verification |
| `scripts/v10/course_evidence_sidecar.py` | 为单门课程生成补证 sidecar：PDF 文本、PDF 源页图、视频关键帧、可选 faster-whisper ASR，不写正式正文 | sidecar evidence only |

示例：

```bash
python scripts/v10/cognitive_vault_garden.py --vault "<formal-vault-path>" --include "02_课程库" --limit 30
python scripts/v10/cognitive_vault_garden.py --vault "<formal-vault-path>" --include "02_课程库" --apply --output-dir "<report-output-dir>"

python scripts/v10/obs_task_ledger.py init
python scripts/v10/obs_task_ledger.py add --title "读取课程处理工作台" --executor file_read --payload "{\"path\":\"02_课程库/01_课程处理工作台.md\"}"
python scripts/v10/obs_task_ledger.py summary

python scripts/v10/course_transform_ledger.py --vault "<formal-vault-path>" --format markdown --limit 30
python scripts/v10/course_transform_ledger.py --vault "<formal-vault-path>" --tasks --limit 10
python scripts/v10/course_transform_ledger.py --vault "<formal-vault-path>" --tasks --seed-ledger --limit 10

python scripts/v10/course_intake_adapter.py engines
python scripts/v10/course_intake_adapter.py inventory "<source-root>" --limit 50
python scripts/v10/course_intake_adapter.py convert "<source-file>"

python scripts/v10/obs_dataview_query.py --vault "<formal-vault-path>" "FROM courses WHERE missing_count>0 SORT missing_count DESC LIMIT 10"
python scripts/v10/obs_dataview_query.py "LIST course FROM tasks WHERE status='pending' LIMIT 10"
python scripts/v10/obs_dataview_query.py --source-root "<source-root>" "TABLE relative_path, format FROM sources WHERE format='pdf' LIMIT 20"

python scripts/v10/course_fact_extractor.py "<markdown-or-transcript-file>" --mode graph
python scripts/v10/course_fact_extractor.py "<markdown-or-transcript-file>" --mode terms --limit 20

python scripts/v10/course_pipeline_candidate.py text --text "RAG 依赖向量数据库和知识库检索。"
python scripts/v10/course_pipeline_candidate.py file --root "<safe-root>" --path "<safe-root>/note.md"
python scripts/v10/course_pipeline_candidate.py crossref --root "<safe-root>" --paths "<safe-root>/a.md" "<safe-root>/b.md"

python scripts/v10/obs_v10_index_exporter.py --vault "<formal-vault-path>" --source-root "<source-root>" --limit 200
python scripts/v10/obs_v10_index_exporter.py --vault "<formal-vault-path>" --source-root "<source-root>" --output-dir "<light-index-output-dir>"

python scripts/v10/course_verification_audit.py --vault "<formal-vault-path>" --source-root "<source-root>" --sidecar-root docs/course-evidence-sidecars --format markdown --output "docs/course-local-verification-audit-YYYY-MM-DD.md"

python scripts/v10/course_evidence_sidecar.py --course "<course>" --vault "<formal-vault-path>" --source-root "<source-root>" --output-root docs/course-evidence-sidecars --max-text-files 3 --max-media-files 1 --asr --asr-model tiny
```

边界：V10 建议全部是 `candidate-only`；脚本不修改课程正文、不读取原始媒体（除 `course_evidence_sidecar.py` 按单门课程显式读取少量源文件并写 helper repo sidecar 证据）。`obs_task_ledger.py` 默认把 SQLite 写到用户本地状态目录（`LOCALAPPDATA/obsidian-assistance/`），不进仓库、不启动守护进程、不提交/推送、不写正式 vault；`course_transform_ledger.py` 默认只读，只有 `--seed-ledger` 才写 SQLite 任务账本；`course_intake_adapter.py` 的 inventory 不包含文件正文，convert 只对指定文件执行且重型引擎懒加载；`obs_dataview_query.py` 只查询 V10 派生虚拟表；`course_fact_extractor.py` 和 `course_pipeline_candidate.py` 输出候选事实/术语/图谱边/融合摘要，必须人工或课程管线核验后才能写入正式页；`obs_v10_index_exporter.py` 默认只输出 stdout，只有显式 `--output-dir` 才写轻量 JSON；`course_verification_audit.py` 不声称绝对零错误，只有本地源、二次文本抽取、报告、视觉资产、OER 等多种证据互相印证时才标 `verified_by_available_methods`；`course_evidence_sidecar.py` 只写 `docs/course-evidence-sidecars/`，不修改正式课程正文；`echo`、`heartbeat`、`context_pack_build`、`taskpack_generate`、`preview`、`dry_run` 不能标记为真实完成。

## 旧 OCR / ASR 说明

早期 01–06 PowerShell 流水线已不再是主入口。后续若恢复 OCR/ASR ingestion，应先生成 manifest / course spec，再接入 V4–V9 工具链；不得把转写全文、OCR 全文或原始媒体提交到云端仓库。
