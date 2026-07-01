# Obsidian AI 全链路工作流：Obsidian-Assistance 可吸收清单

> 来源：用户提供的《本地 Obsidian AI 全链路工作流整合版》。本文只吸收脱敏流程、规则、目录、脚本和工程化任务，不上传正式 vault、课程正文、素材、转写、OCR、私有配置或凭据。

## 1. 本仓库的定位

`Obsidian-Assistance` 是辅助仓库，不是正式 Obsidian vault。

本仓库可以承载：

- 脱敏架构文档；
- 规则模板：`CLAUDE.md`、`.hermes.md`、`CODEX.md`、`CC_SWITCH.md`、`SECURITY.md`、`DESIGN.md`；
- Obsidian 目录/笔记/YAML/MOC 模板；
- 安全写入脚本、检查脚本、Markdown 清洗脚本；
- V4/V5 示例课程包、合成 demo、测试；
- GitHub Actions 验证；
- 插件原型和工程规则。

本仓库不承载：

- 正式 vault `.obsidian/`；
- 用户真实笔记正文；
- 原始课程资料、PDF、音视频、压缩包；
- ASR/OCR 全文；
- `.env`、API Key、token、SSH 私钥、浏览器 Cookie；
- 未审计的第三方规则文件原文。

## 2. 总体架构可吸收部分

用户给出的目标链路可以转为本仓库的长期工程目标：

```text
外部素材 / 文件 / 课程 / 项目资料
        ↓
素材预处理层：MarkItDown / OpenDataLoader / OCR / 音视频转写
        ↓
Obsidian 本地 Vault：Inbox / PARA / Wiki / 项目 / 日记 / Dashboard
        ↓
Hermes 调度层：GPT / DeepSeek 可切换，执行清洗、总结、归档、推理
        ↓
CC Switch 执行切换层：Claude Code / CCR / CCRelay / OpenClaw 路线切换
        ↓
Codex 工程开发层：插件、脚本、前端、测试、安全规则落地
        ↓
结果回写 Obsidian：标准笔记 / MOC / 项目文档 / 代码说明 / 日报复盘
```

对本仓库的含义：

- `docs/` 保存系统规则、执行协议、阶段路线图；
- `templates/` 保存标准笔记、MOC、任务单、规则文件模板；
- `scripts/` 保存转换、清洗、巡检、安全扫描脚本；
- `snippets/` 保存可选 CSS，不直接写正式 vault；
- `tests/` 验证安全边界、dry-run、YAML、链接、隐私扫描；
- `.github/workflows/` 自动跑测试和审计。

## 3. 立即吸收：第一优先级

### 3.1 Obsidian 标准化骨架

可落地为模板和脚本，不直接移动正式库目录。

建议新增或维护：

```text
templates/system/
  CLAUDE.md
  .hermes.md
  CODEX.md
  CC_SWITCH.md
  SECURITY.md
  DESIGN.md

templates/obsidian/
  standard-note.md
  moc.md
  project-note.md
  daily-note.md
  ai-run-log.md
  cc-switch-task.md
```

对应脚本：

```text
scripts/v5/yaml_normalizer.py
scripts/v5/backlink_checker.py
scripts/v5/vault_health_check.py
scripts/v5/inbox_router.py
scripts/v5/unicode_hidden_char_scan.py
scripts/v5/markdown_lint_runner.py
```

### 3.2 YAML 元数据规范

吸收为标准模板：

```yaml
---
title:
type: note
status: draft
source:
created:
updated:
tags: []
related: []
ai_processed: false
model_used: []
---
```

约束：

- 真实来源未知时不填假来源；
- `model_used` 只记录真实调用过的模型或工具；
- `source` 不写私有绝对路径，必要时用脱敏占位符；
- 标准化脚本默认 dry-run，显式 `--apply` 才改文件。

### 3.3 MOC 与 Dashboard 规范

可以吸收为模板，不直接改用户现有知识库结构。

推荐模板：

```text
40_Wiki/MOC/MOC_Obsidian_AI_工作流.md
40_Wiki/MOC/MOC_Hermes_调度系统.md
40_Wiki/MOC/MOC_Codex_插件开发.md
40_Wiki/MOC/MOC_AI安全规范.md
50_Dashboard/今日工作台.md
50_Dashboard/项目总览.md
50_Dashboard/知识库健康度.md
50_Dashboard/AI运行记录.md
```

本仓库只提供模板和 demo，正式 vault 应通过安全写入器安装。

### 3.4 Hermes Skill 分类

可吸收到 `docs/hermes-skill-taxonomy.md` 或未来 `skills/` 模板中：

| Skill | 用途 | 仓库落点 |
|---|---|---|
| `/ingest` | Inbox 清洗、YAML、分类、双链 | `scripts/v5/inbox_router.py` + 模板 |
| `/vault-health` | 断链、孤立笔记、YAML、空文件、重复检查 | `scripts/v5/vault_health_check.py` |
| `/wiki-synthesis` | 主题汇总、MOC、概念提取 | `templates/obsidian/moc.md` |
| `/morning-report` | 晨报、任务提取 | `templates/obsidian/daily-note.md` |
| `/weekly-review` | 周复盘 | `templates/obsidian/weekly-review.md` |
| `/build-plugin` | 插件需求转工程任务 | `templates/system/CODEX.md` |
| `/lesson-build` | 教学资料转教案/习题 | 后续教学模板 |
| `/lore-build` | TRPG/OC 世界观整理 | 后续角色/设定模板 |
| `/security-scan` | 规则/Unicode/凭据/危险命令审计 | `scripts/v5/security_scan.py` |

### 3.5 安全规则

必须吸收到 `templates/system/SECURITY.md` 和测试中。

最低安全规则：

- 禁止原封不动导入第三方 `CLAUDE.md`、`.cursorrules`、`.hermes.md`、`rules.md`、`agent.md`、`skills.md`；
- 先审计，再摘取有用规则；
- 检查零宽字符、控制字符、可疑 Base64；
- 禁止读取 `.env`、`.ssh/`、浏览器 Cookie、密码管理器；
- 禁止跨目录删除和递归清空；
- 第三方 Skill 必须检查网络访问、shell、删除、上传、Git Hook 修改。

这些规则应进入 CI 审计。

## 4. 稳定后吸收：第二优先级

### 4.1 素材预处理层

可作为后续脚本模块，而不是马上成为硬依赖：

| 工具 | 吸收方式 | 风险控制 |
|---|---|---|
| MarkItDown | 通用文件转 Markdown | 先做独立 demo，不批量处理正式素材 |
| OpenDataLoader PDF | PDF 深度解析 | 只记录接口和输出契约，真实接入前核验维护状态 |
| markdownlint / Markdig | Markdown 规范检查 | 可进入 CI 或本地脚本 |
| OCR / ASR | 课程处理增强 | 不上传全文，默认输出到本地工作区 |

建议未来目录：

```text
scripts/v5/convert_files.py
scripts/v5/pdf_loader_adapter.py
scripts/v5/markdown_lint_runner.py
scripts/v5/media_transcript_router.py
```

### 4.2 Codex 工程层

可吸收为工程规则和插件原型：

```text
templates/system/CODEX.md
templates/system/DESIGN.md
plugin-prototypes/dashboard/
plugin-prototypes/ai-logs/
plugin-prototypes/vault-health/
```

每个 Codex 任务必须输出：

1. 修改文件；
2. 新增功能；
3. 运行方式；
4. 测试方式；
5. 已知问题；
6. 回滚方法。

### 4.3 CC Switch 执行模式

吸收为 `templates/system/CC_SWITCH.md`：

```text
READONLY   只读分析
VAULT_EDIT vault 内受限编辑
CODE_EDIT  当前项目仓库内代码工程
AUDIT      安全审计
```

所有模式必须有：允许目录、禁止目录、操作要求、输出位置。

## 5. 仅吸收思想：第三优先级

这些不应立即写成生产依赖：

- Talos System：吸收 Dashboard/热力图/作战室/信号面板思想；
- Cognee：作为长期记忆候选，需要单独验证部署成本和数据边界；
- GBrain：吸收 `raw/wiki/schema` 架构思想，不承诺项目依赖；
- Agency-Agents：吸收为少量角色模板，不一次性加载大量 agent；
- 文件预览组件：先作为插件原型候选，不作为主流程硬依赖；
- PhET / GeoGebra：教学场景的后续资料源和链接模板。

## 6. 不吸收或暂缓吸收

以下内容不进入仓库或不作为当前阶段任务：

- 未核验的 Star 数、跑分说法、闭源资源宣传；
- 第三方规则文件原文；
- 任何真实 token、key、cookie、私钥；
- 真实 vault 内容、课程正文、转写全文、OCR 全文；
- 自动改正式 vault 目录结构的大迁移脚本；
- 未审计的下载脚本或联网安装脚本。

## 7. 可执行阶段规划

### 阶段 1：规则与模板层

目标：把用户提供的体系沉淀为可复用模板。

任务：

- 新建 `templates/system/SECURITY.md`；
- 新建 `templates/system/DESIGN.md`；
- 新建 `templates/system/CODEX.md`；
- 新建 `templates/system/CC_SWITCH.md`；
- 新建标准笔记、MOC、AI 运行日志模板；
- 加测试：模板不能包含真实路径、密钥或危险命令。

### 阶段 2：Vault Health 与 Inbox 脚本

目标：先做只读检查，再做 dry-run 清洗。

任务：

- `vault_health_check.py`：检查空文件、断链、YAML、孤立笔记、重复文件；
- `unicode_hidden_char_scan.py`：检查零宽字符和隐藏控制字符；
- `yaml_normalizer.py`：默认 dry-run 补 YAML；
- `inbox_router.py`：默认 dry-run 输出分类计划；
- 所有 `--apply` 写入都要备份。

### 阶段 3：素材预处理适配器

目标：接入转换工具，但不绑定正式 vault。

任务：

- MarkItDown adapter；
- PDF adapter；
- Markdown lint runner；
- 输出契约：Markdown + JSON metadata + report；
- 测试数据只用 synthetic demo。

### 阶段 4：插件与 Dashboard 原型

目标：Codex 工程化实现 Obsidian 中控雏形。

任务：

- Dashboard 插件原型；
- AI Logs 面板；
- Vault Health 面板；
- Inbox 批处理按钮；
- 读取 `DESIGN.md` 做 UI 约束；
- 不直接打包进正式 vault，先 demo vault 测试。

### 阶段 5：长期记忆/图谱候选验证

目标：把 Cognee/GBrain 思路转成可验证 spike。

任务：

- 只用 demo notes 建索引；
- 验证数据边界；
- 验证离线/本地存储位置；
- 输出 spike 报告后再决定是否进入主线。

## 8. 与当前 V4 的关系

当前 V4 已覆盖：

- synthetic demo course；
- safe writer；
- dry-run/apply；
- YAML/Canvas/Mermaid 测试；
- GitHub Actions；
- 危险删除审计；
- 子生成器 apply gate。

用户提供的新方案可以作为 V5 方向：

```text
V4：课程包生成器与安全写入底座
V5：Obsidian AI OS 规则/模板/脚本/插件一体化
```

V5 不应推翻 V4，而是在 V4 安全边界上扩展。

## 9. 验收标准

任何吸收任务必须满足：

- 只包含脱敏模板/脚本/demo；
- 默认 dry-run；
- 写入必须显式 `--apply`；
- 覆盖前备份；
- 不含真实 vault 内容；
- 不含密钥/令牌/私有路径；
- 测试通过；
- CI 通过；
- PR 合并后 main 干净。

## 10. 下一步推荐任务

按真实优先级，下一步不应直接做大迁移，而应做一个小而可验证的 PR：

1. 新增 `templates/system/SECURITY.md`；
2. 新增 `templates/system/DESIGN.md`；
3. 新增 `templates/system/CODEX.md`；
4. 新增 `templates/system/CC_SWITCH.md`；
5. 新增模板安全测试，确保不含真实路径、密钥、危险删除命令；
6. CI 跑通后再进入脚本层。
