# TALOS × Obsidian 知识库匹配报告

## 边界

- 来源知识库：`D:\BaiduSyncdisk\Obsidian知识库`
- 本报告只基于用户粘贴的顶层目录清单。
- 不上传、不删除、不移动任何课程内容。
- 课程正文默认不读取；只有在用户明确指定某个课程文件时才做内容级匹配。
- `.git`、`.smart-env`、`.copilot`、`.obsidian` 属于高敏/配置相关区域，只做能力识别，不复制凭据、不导出配置正文。

## 顶层目录解读

| Obsidian 目录 | TALOS 角色 | 当前匹配状态 |
|---|---|---|
| `00_主页` | Home Console / 入口仪表盘 | 对应 `index.html` |
| `01_收件箱` | 临时捕获、每日任务入口 | 可接 TALOS 每日任务生成器 |
| `02_课程库` | 课程内容源 | 对应 `course-reading.html`，只读索引，不批量读正文 |
| `03_知识卡片` | Evidence Card 输出区 | 对应 `evidence-matrix.html` 的证据卡 |
| `04_复习卡片` | Review / 间隔复习 | 对应 TALOS Review AI Center |
| `50_Dashboard` | 聚合看板 | 对应 TALOS Home Console 与 OER 覆盖率仪表盘 |
| `50_领域知识` | 领域图谱 / Project Atlas | 对应 TALOS Project Atlas |
| `80_索引数据库` | Dataview / 元数据索引 | 对应 Evidence Matrix、热力图、交叉对比 |
| `90_模板` | Markdown 模板 | 对应 Course / Evidence / Daily Mission / Review 模板 |
| `91_插件与设置` | 插件能力和配置 | 等待插件索引后匹配 |
| `93_导入报告` | 导入审计与迁移报告 | 对应本项目后续迁移日志 |
| `95_待审核` | QA / Review Queue | 对应 Pixel Parity Audit、Workspace QA |
| `96_脚本` | 本地自动化脚本 | 只读审查；不自动执行 |
| `99_附件` | 图片、PDF、附件资产 | 对应 TALOS 视觉参考和 Obsidian 附件 |

## 当前 HTML 原型映射

### `index.html`

应作为 `00_主页` / `50_Dashboard` 的视觉原型：保留 Home Console、项目推进台、课程指挥舱、Review AI、睡觉模式入口。后续 Obsidian 插件化时可拆为一个总览 `ItemView`。

### `course-reading.html`

应绑定 `02_课程库`、`03_知识卡片`、`80_索引数据库` 三类目录：

- 左侧 Vault 树展示课程路径和知识卡片路径。
- 中间阅读区模拟课程摘记和 Live Preview。
- 右侧 Properties 映射 Markdown frontmatter。
- 证据卡生成只产生草稿，不直接写入真实 Vault。

### `evidence-matrix.html`

应绑定 `03_知识卡片`、`04_复习卡片`、`80_索引数据库`：

- 证据卡来自知识卡片目录。
- 复习状态来自复习卡片目录。
- 热力图和矩阵来自索引数据库。

## Obsidian 插件化建议

等待 `obsidian-plugins-index.txt` 内容后再做精确匹配。当前先按目录推断插件能力需求：

| 需求 | 可能依赖 | TALOS 页面 |
|---|---|---|
| 文件树 / Vault 路径选择 | Obsidian 原生 Workspace API | `course-reading.html` |
| frontmatter 读取 | MetadataCache / Properties | `course-reading.html`, `evidence-matrix.html` |
| Dataview 查询 | Dataview 或自建索引 | `evidence-matrix.html` |
| 卡片复习 | Spaced repetition 类插件或自建队列 | Review AI Center |
| 图谱 / Project Atlas | Canvas / Graph / 自定义视图 | Project Atlas |
| 模板生成 | Templates / Templater 类插件 | Daily Mission / Evidence Template |

## 不做的事

- 不扫描整库正文。
- 不读取 `.env`、token、插件密钥、同步配置。
- 不执行 `96_脚本` 下任何脚本。
- 不写入 `D:\BaiduSyncdisk\Obsidian知识库`。
- 不修改 `.obsidian` 设置或插件目录。

## 下一步

1. 粘贴 `obsidian-plugins-index.txt` 内容。
2. 将插件名映射到 TALOS 页面功能。
3. 选择一个最小插件化目标：建议先做 `course-reading.html` 的 Obsidian `ItemView` 设计规格。
4. 生成 `OBSIDIAN_PLUGIN_MAPPING.md`，只写当前项目目录。
