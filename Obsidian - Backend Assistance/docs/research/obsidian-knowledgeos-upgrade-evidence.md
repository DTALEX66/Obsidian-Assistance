# Obsidian 知识库全方位升级：参考核验与可吸收结论

> 范围限定：本轮只吸收“升级 Obsidian 知识库本身”的内容：信息架构、笔记模板、MOC、Dashboard、Dataview、主题/CSS、Talos-like 中控视觉和健康度面板。暂不落地 Hermes/CC/Codex 工作流模板。

## 1. 已下载公开参考

| 文件 | 来源 | 用途 | 吸收方式 |
|---|---|---|---|
| `docs/research/downloaded/dataview-readme.md` | `blacksmithgu/obsidian-dataview` README | Dataview 查询能力、动态索引、dashboard 表格/列表 | 用于 Dashboard/MOC/健康度模板中的 Dataview block 设计 |
| `docs/research/downloaded/obsidian-sample-plugin-readme.md` | `obsidianmd/obsidian-sample-plugin` README | 后续插件化中控的结构参考 | 本轮只作参考，不生成插件工作流 |
| `docs/research/downloaded/obsidian-sample-plugin-manifest.json` | `obsidianmd/obsidian-sample-plugin` manifest | 插件 manifest 字段参考 | 本轮只作参考，不安装、不运行 |

## 2. 设计系统对比

| 参考 | 可吸收点 | 不吸收点 |
|---|---|---|
| Linear | 深色原生、低噪声、细边框、极少色彩、卡片层级、工程感 | 不照搬品牌色和商业文案 |
| Supabase | 深色 + 绿色状态信号、边框代替阴影、开发者控制台感 | 不引入外部字体依赖作为强需求 |
| Sentry | 数据密集、错误/健康度/信号面板、深色可观测性 UI | 不采用过多高饱和紫色/营销插画 |
| Talos-like 中控 | 总览、模块、热力图、能力中心、信号面板、作战室 | 不把未核验 Talos 项目写成生产依赖 |

## 3. 对本项目最有用的吸收项

### 3.1 立刻落地

- `docs/v5-obsidian-knowledgeos-upgrade-analysis.md`：全方位升级分析与取舍。
- `docs/v5-talos-ai-os-dashboard-spec.md`：Talos-like 中控规格。
- `snippets/v5/talos-dashboard.css`：Obsidian CSS snippet 原型。
- `templates/obsidian/*.md`：通用标准笔记、MOC、Dashboard、健康度、课程卡片墙、领域主页模板。
- `examples/v5-talos-dashboard/`：可在测试 vault 复制打开的 demo 页面。
- `tests/v5/test_obsidian_knowledgeos_assets.py`：确保模板/CSS/文档可维护。

### 3.2 暂缓

- 自研 Obsidian 插件：先把 dashboard/snippet/template 跑顺，再插件化。
- Cognee/GBrain：先不用，避免把知识库升级变成图数据库工程。
- CC Switch/Codex/Hermes 工作流模板：用户明确“工作流先不用”。

## 4. 验收标准

- 不包含正式 vault 内容。
- 不包含 `.obsidian/` 私有配置。
- 不包含课程正文/转写/OCR/媒体/压缩包。
- 所有模板使用占位符和 demo 内容。
- CSS 必须限定在 `.knowledgeos-v5` / `.talos-*` 作用域，避免全局污染主题。
- Dataview block 只引用通用字段，不硬编码用户路径。
