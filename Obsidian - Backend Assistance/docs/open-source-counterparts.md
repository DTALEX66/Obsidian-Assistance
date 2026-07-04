# 开源对标项目

本项目不直接搬入大型 RAG 平台，而是借鉴它们的结构：文件转换、证据索引、核验、必要时联网补证、Obsidian 写入。

| 项目 | 相关能力 | 借鉴点 |
|---|---|---|
| [Khoj](https://github.com/khoj-ai/khoj) | AI second brain、本地文档和网页问答、Obsidian 入口 | 本地文档优先、个人知识库问答 |
| [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm) | 本地优先 workspace RAG | 每门课一个 workspace / evidence space |
| [Onyx](https://github.com/onyx-dot-app/onyx) | 企业搜索、RAG、连接器、web search | 连接器 + 混合检索 + 必要时联网 |
| [PrivateGPT](https://github.com/zylon-ai/private-gpt) | 私有文档问答 | 隐私门禁和本地优先 |
| [Docling](https://github.com/docling-project/docling) | 多格式解析、OCR、ASR、Markdown/JSON 导出 | 未来作为复杂文档转换候选 |
| [MarkItDown](https://github.com/microsoft/markitdown) | 多格式转 Markdown | 未来作为轻量文档转换候选 |
| [Unstructured](https://github.com/Unstructured-IO/unstructured) | 文档 ETL、partition/chunking | 切块和元数据设计 |
| [Whisper](https://github.com/openai/whisper) | 多语言 ASR | 音视频转写候选 |
| [Obsidian Omnisearch](https://github.com/scambier/obsidian-omnisearch) | Obsidian 内搜索、PDF/OCR 索引 | 库内搜索体验 |
| [Obsidian Local REST API](https://github.com/coddingtonbear/obsidian-local-rest-api) | REST / MCP 读写 vault | 后续 Codex 与 Obsidian 桥接 |
