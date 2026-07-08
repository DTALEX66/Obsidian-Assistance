# 课程全流程开源项目调研与吸收优先级（2026-07-07）

> 本文是 helper repo 脱敏调研记录。目标是先找可直接用于 OBS 课程全流程的本地/无 API 开源项目，再决定增强顺序。正式安装前仍需逐项核验 license、版本、Windows 可用性和项目锁定依赖。

## 调研边界

- 优先：本地运行、无 API key、可在 Windows/Python 管线中调用、不会上传正式 vault 或原始课程资料。
- 不优先：云端 SaaS、必须联网处理课程内容、强绑定商业 API、license/模型权重不清晰的项目。
- 当前 GitHub API 查询遇到 rate limit，因此本文采用 web search + 已知项目文档入口做首轮筛选；后续安装前再做精确 license/version 验证。

## P0：优先接入的低风险能力

| 能力 | 候选项目 | 价值 | 集成建议 | 风险 |
|---|---|---|---|---|
| 多格式转 Markdown | Microsoft MarkItDown | PDF/DOCX/PPTX/XLSX/HTML 等统一转 Markdown，适合先形成课程素材预览 | 先做轻量 adapter：存在则调用，不存在则跳过；输出 manifest，不提交全文 | 复杂版式/扫描 PDF 质量有限 |
| PDF/文档结构解析 | Docling | 复杂 PDF、表格、版面理解比纯文本提取更强 | 作为 MarkItDown 后的增强 fallback；先只在 demo/小 PDF smoke test | 依赖较重，安装时间和模型下载需验证 |
| 本地转写 | faster-whisper | 本地音频/视频转写，适合课程音视频批处理 | 先实现接口规范与 manifest；实际模型下载/运行另开验证 | 模型体积、CPU/GPU 性能差异 |
| 视频场景/关键帧 | PySceneDetect + ffmpeg | 自动找场景切分点，给 V6 keyframe plan 提供更稳候选 | 先接到 V6 `video_keyframe_plan` 或新 adapter，只输出 candidate | 低动态课件视频可能需要阈值调参 |
| PDF 页图 | PyMuPDF / pymupdf | 已适合生成 PDF 源页图证据 | 保持 V6 现有做法；补进统一 intake registry | 部分 PDF 加密/字体异常 |

## P1：增强课程质量与中文结构化

| 能力 | 候选项目 | 价值 | 集成建议 | 风险 |
|---|---|---|---|---|
| OCR | PaddleOCR / RapidOCR / Tesseract | 扫描 PDF、课件截图、图片课程资料文字提取 | 优先 RapidOCR/PaddleOCR 小样本；Tesseract 作轻量兜底 | 中文识别、表格、公式仍需人工/规则核验 |
| 中文分词/关键词 | jieba / HanLP / TextRank 类工具 | 术语索引、知识卡片候选、自动标签 | 先用 jieba 做无模型 baseline；HanLP 作为增强候选 | HanLP 模型下载/Java/依赖需验证 |
| 网页/OER 提取 | trafilatura / BeautifulSoup / readability | OER 交叉对比和公开资料结构化 | 只抽结构和 license/provenance，不把网页当课程证据 | 网站反爬/版权边界 |
| 事实/实体抽取 | Cognitive-Loop-OS fact_extractor baseline + 后续中文适配 | 生成概念图谱/OER 对比候选 | 先做规则+关键词，不直接写确定事实 | 中文语义抽取误差 |

## P2：后续可评估但不先接入

| 能力 | 候选项目 | 说明 |
|---|---|---|
| 高精 PDF OCR/版面模型 | Marker / MinerU / Surya | 质量可能高，但依赖/模型/license 边界较重；先不作为默认链路。 |
| 工作流编排 | Prefect / Dagster | 对大型夜间课程循环有价值，但当前先用 SQLite ledger 和脚本闭环，不引入服务化复杂度。 |
| 知识图谱/RAG | GraphRAG / NetworkX / sqlite-vec | helper repo 先做 Markdown/frontmatter 只读索引；向量/图谱后续接前端或 Cognitive-Loop-OS。 |

## 当前应落地的增强顺序

1. **课程转化与处理产物总账**：先把 `02_课程库`、`93_导入报告`、`99_附件` 映射到 V10 ledger，避免任务虚假完成。
2. **轻量 multi-format adapter**：先定义统一接口和 manifest，不急着安装重依赖。
3. **Dataview-like read-only query**：为前端/Bridge 提供只读查询层。
4. **转写/OCR adapter 骨架**：只记录工具可用性、命令、输出路径，不默认下载模型。
5. **真实小课 smoke test**：从小 PDF 或单文件课程开始验证，不直接全量跑大课。

## 安全边界

- 所有工具默认生成 manifest/report，不提交 ASR/OCR 全文。
- 本地源文件候选是 `candidate-only`，不能升级为 verified evidence。
- OER/网页内容只能做交叉结构/出处，不替代课程真实来源。
- 任何模型下载、依赖安装、正式 vault 写入都需要单独验证命令和输出。
