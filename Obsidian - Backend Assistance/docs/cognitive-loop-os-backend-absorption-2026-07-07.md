# Cognitive-Loop-OS 后端能力吸收记录（2026-07-07）

> 脱敏 helper-repo 记录：本文件只记录可复用工程能力和复制/改造落点，不复制 Cognitive-Loop-OS 运行数据库、日志、缓存、私密配置，也不复制正式 Obsidian vault 内容或原始课程资料。

## 本轮目标

用户要求检查：

```text
D:/All projects/Cognitive-Loop-OS
```

并把 OBS 后端可用的能力复制过来。

## 已检查到的可用后端能力

| Cognitive-Loop-OS 模块 | 能力 | 对 OBS 后端价值 | 本轮处理 |
|---|---|---|---|
| `shared/auto_tagger.py` | 关键词抽取、标签建议、atomic note 检测、渐进式摘要 | 用于课程页/知识卡片的自动标签、薄弱主题、拆分建议 | 已吸收进 V10 脚本 |
| `shared/backlinks.py` | Obsidian-style wikilink/embed/markdown link 解析 | 用于检查课程页双链、孤岛笔记、未解析链接 | 已吸收进 V10 脚本 |
| `shared/knowledge_gardener.py` | orphan 检测、连接建议、知识缺口雷达 | 用于课程库/知识卡片花园维护 | 已吸收进 V10 脚本 |
| `shared/dataview.py` | 轻量 Dataview-like DSL | 可作为后续 OBS 只读查询层参考 | 暂不复制；需先设计脱敏查询输入/输出 |
| `shared/fact_extractor.py` | 零依赖 SPO fact extraction | 可作为英文/技术类课程结构化抽取参考 | 暂不复制；中文课程需另做适配测试 |
| `app/ingestion/multi_format.py` | PDF/DOCX/PPTX/HTML/image 转换 fallback 链 | 可作为后续 OCR/转写入口升级参考 | 暂不复制；依赖较重，需单独边界设计 |
| `shared/sleep_loop_engine.py` | SQLite 持久化任务账本、真实任务证据、防假完成 | 可用于 OBS 睡觉模式/无人值守课程循环 | 已拆成 helper-repo 本地任务账本 mini 版 |
| `shared/evidence_index.py` | evidence health scoring | OBS 已有 V6 evidence 工具，可对照增强 | 暂不复制；避免与现有 V6 重复 |
| `shared/source_discovery.py` | source inventory | OBS 已有 V5/V6 source discovery | 暂不复制；现有脚本更贴合 vault |

## 本轮实际复制/改造落点

新增：

```text
scripts/v10/cognitive_vault_garden.py
scripts/v10/obs_task_ledger.py
scripts/v10/course_transform_ledger.py
scripts/v10/course_intake_adapter.py
scripts/v10/obs_dataview_query.py
scripts/v10/course_fact_extractor.py
scripts/v10/course_pipeline_candidate.py
scripts/v10/obs_v10_index_exporter.py
```

测试：

```text
tests/v10/test_cognitive_vault_garden.py
tests/v10/test_obs_task_ledger.py
tests/v10/test_course_transform_ledger.py
tests/v10/test_course_intake_adapter.py
tests/v10/test_obs_dataview_query.py
tests/v10/test_course_fact_extractor.py
tests/v10/test_course_pipeline_candidate.py
tests/v10/test_obs_v10_index_exporter.py
```

文档入口：

```text
scripts/README_SCRIPTS.md
README.md
```

## V10 脚本能力

`scripts/v10/cognitive_vault_garden.py` 提供：

1. 关键词抽取：从 Markdown 内容中提取候选关键词。
2. 标签建议：根据关键词和领域信号给出候选 tags。
3. Atomic note 检测：发现过长、多主题、可拆分笔记。
4. Wikilink/embed/本地 Markdown link 解析。
5. 孤岛笔记发现：无入链且无出链的笔记。
6. 未解析笔记链接发现：跳过媒体附件，只报告未匹配到扫描笔记的 note link。
7. 薄弱主题雷达：根据 frontmatter tags 或建议 tags 统计覆盖薄弱主题。
8. 候选连接建议：基于关键词重叠发现可能应互链的笔记。
9. JSON/Markdown 报告输出。

`scripts/v10/obs_task_ledger.py` 提供：

1. SQLite 本地任务账本：记录 OBS 后端/课程转化循环任务。
2. 真实任务校验：阻止 `echo`、`heartbeat`、`context_pack_build`、`taskpack_generate`、`preview`、`dry_run` 计入真实任务。
3. 真实完成校验：只有 `file_read` 的 path+content、`safe_write/report_write` 的 written+path、`source_scan` 的 count+items、`vault_audit` 的 ok+issues、`course_transform` 的 course+files_written+report_path 才能标记 `done`。
4. blocked 可审计：虚拟任务或缺证据任务会保留为 `blocked`，不被伪装为完成。
5. CLI：`init`、`add`、`record`、`list`、`summary`、`report`。

`scripts/v10/course_transform_ledger.py` 提供：

1. 扫描 `02_课程库/<课程名>/` 的课程页覆盖情况。
2. 汇总 `93_导入报告` 中与课程名匹配的导入/处理报告。
3. 读取 `99_附件/verified-keyframes/keyframe-registry.json`，统计课程真实关键帧资产。
4. 生成“原始来源 → 扫描报告 → 生成资产 → registry → 课程页 → 下一步”的 Markdown/JSON 总账。
5. 显式 `--seed-ledger` 时，把真实缺口转成 `course_transform` pending 任务写入 V10 SQLite 账本。

`scripts/v10/course_intake_adapter.py` 提供：

1. 统一识别 PDF/DOCX/PPTX/XLSX/HTML/Markdown/TXT/图片/音频/视频源文件格式。
2. 生成不含正文的 source manifest，适合扫描 `E:/学习数据` 后进入课程匹配队列。
3. 对 Markdown/TXT 做本地 passthrough，对 PDF/Office/HTML/图片懒加载 markitdown/docling/trafilatura 等可选引擎。
4. 未安装重型引擎时返回 `candidate-only` 错误，不伪装为已转换。

`scripts/v10/obs_dataview_query.py` 提供：

1. Dataview-like DSL：`FROM`/`WHERE`/`SORT`/`LIMIT`/`LIST`/`TABLE`。
2. 查询只读虚拟表：`courses`、`tasks`、`sources`。
3. 用于前端/Bridge 查询课程缺口、任务状态、源文件 manifest，不读取课程正文。

`scripts/v10/course_fact_extractor.py` 提供：

1. 中文课程术语候选抽取。
2. 中文关系模式候选抽取：contains / depends_on / uses / used_for / generates。
3. 候选知识图谱节点/边输出；全部 `candidate_only`，不得直接写正式事实。

`scripts/v10/course_pipeline_candidate.py` 提供：

1. OBS-safe 候选管道：extract → tag → summarize → facts → credibility/crossref。
2. OER/参考来源可信度评分：domain trust + content signals。
3. 多来源候选对比：agreements / contradictions / unique_keywords。
4. 全程不写 vault、DB、日志、缓存；输出 `candidate_only` JSON。

`scripts/v10/obs_v10_index_exporter.py` 提供：

1. 生成 `obs-v10-course-transform-index.json`。
2. 生成 `obs-v10-source-manifest-index.json`。
3. 生成 `obs-v10-task-ledger-index.json`。
4. 默认 stdout；只有显式 `--output-dir` 才写轻量 JSON。

## 使用方式

只读预览：

```bash
python scripts/v10/cognitive_vault_garden.py --vault "<formal-vault-path>" --include "02_课程库" --limit 30
```

写报告：

```bash
python scripts/v10/cognitive_vault_garden.py --vault "<formal-vault-path>" --include "02_课程库" --apply --output-dir "<report-output-dir>"
```

本地任务账本：

```bash
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
```

## 安全边界

- 默认只读。
- `--apply` 只写报告，不修改课程正文。
- 不创建、升格或伪造 verified evidence。
- 不读取原始媒体，不复制课程资料。
- 不读取/提交运行数据库、日志、缓存、私密配置。
- 所有连接/标签/拆分建议都是 `candidate-only`，必须经过课程管道核验后才能进入正式页面。
- `obs_task_ledger.py` 只写 helper-repo 指定的 SQLite 账本；不启动后台循环、不提交、不推送、不写正式 vault。
- `course_transform_ledger.py` 默认只读；只有显式 `--seed-ledger` 才写 helper-repo SQLite 账本。
- `course_intake_adapter.py` 的 inventory 不包含文件正文；重型转换依赖全部懒加载，未安装时必须显式返回错误。
- `obs_dataview_query.py` 只查询 V10 派生表；不直接读取课程正文全文。
- `course_fact_extractor.py` 只输出候选术语/事实/图谱边；必须经课程管线核验才能入库。
- `course_pipeline_candidate.py` 只做候选分析；不吸收 COS 的 KB 写入、FTS5、vector index、RSS/search/youtube 自动采集。
- `obs_v10_index_exporter.py` 默认只输出 stdout；显式写入也只写轻量 JSON，不写课程正文。
- 账本中的 `done` 必须有真实工具/文件/扫描/写入证据，不能由心跳、预览、dry-run 或上下文打包结果充数。

## 后续可继续吸收

建议按这个顺序继续：

1. **真实课程闭环试跑**：选择一门 pending 课程，执行 source manifest → candidate pipeline → report → ledger 证据关闭。
2. **Bridge/Open Design 接入**：把 `obs-v10-*.json` 接入现有三件套索引校验。
3. **OCR/ASR sidecar**：在明确安装 tesseract / faster-whisper 后再接入重型链路。

## 不复制内容

本轮没有复制：

- `data/`、`logs/`、`.pytest_cache/`、`.ruff_cache/`、`__pycache__/`。
- Cognitive-Loop-OS 的运行数据库或本地状态。
- `.env`、tokens、私密配置。
- 任意正式 vault 内容、原始课程素材、媒体、OCR/ASR 全文。
