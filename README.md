# Obsidian Assistance

一个用于辅助本地 Obsidian 知识库的工具与流程项目。

本仓库只保存 **Obsidian 辅助工具、流程规范、脚本模板和本地核验模块**，不保存正式 Obsidian vault、原始课程资料、音视频转写、OCR 全文、私人笔记或同步盘内容。

## 目标

- 加速课程资料从“原始文件”到“Obsidian 可复习知识库”的转化。
- 建立本地优先的证据检索与核验流程，减少重复联网和人工确认。
- 跑通 Obsidian 全流程：输入箱 → 素材识别 → 转写/OCR → 核验 → 总结 → 卡片 → 复习 → 入库报告。
- 提供可复用的脚本和模板，而不是绑定某一个私人 vault。

## 当前模块

```text
skills/
  course-verifier/          本地证据检索与课程术语核验 Skill
scripts/
  course_verify.py                  本地证据索引、查询、核验脚本
  setup_obsidian_mvp_flow.ps1       参数化 Obsidian 全流程 MVP 写入脚本
  v4/generate_course_pack.py        V4 课程包生成器，默认 dry-run，显式 --apply 才写
  v4/generate_canvas_map.py         V4 Canvas 生成器，默认 dry-run
  v4/generate_mermaid_graph.py      V4 Mermaid 图生成器，默认 dry-run
  v4/generate_bases_views.py        V4 Bases 视图草案生成器，默认 dry-run
  v4/safe_vault_writer.py           V4 安全写入层，阻止路径穿越并覆盖前备份
  v4/obsidian_v4_audit.py           V4 安全审计脚本
  v5/course_diversity_audit.py      V5 课程验证与内容多样化审计脚本
templates/v4/                       V4 Markdown/Canvas 模板
templates/obsidian/                 V5 通用 Obsidian 知识库模板
snippets/v4/                        V4 Obsidian CSS snippets
snippets/v5/talos-dashboard.css     V5 Talos-like KnowledgeOS 中控 CSS
examples/v5-talos-dashboard/        V5 中控 demo vault 页面
tests/v4/                           V4 回归测试与安全边界测试
tests/v5/                           V5 KnowledgeOS 模板/CSS/参考资产测试
.github/workflows/v4-validation.yml GitHub Actions 自动验证
docs/
  data-boundary.md                  数据边界与防外溢规则
  pipeline-acceleration.md          加速转化与状态机方案
  pipeline-v2-full-flow.md          课程处理全流程规范
  project-experience-2026-07-01.md  项目经验总结：长循环、自检、全网比校
  obsidian-ai-fullchain-absorption-plan.md  Obsidian AI 全链路可吸收路线图
  v5-obsidian-knowledgeos-upgrade-analysis.md  V5 Obsidian 知识库升级分析
  v5-talos-ai-os-dashboard-spec.md             V5 Talos-like 中控规格
  v5-course-diversity-standard.md              V5 课程验证与内容多样化标准
  research/obsidian-knowledgeos-upgrade-evidence.md  V5 公开参考核验与吸收结论
  ui-audit.md                       Obsidian UI/插件体检清单
  open-source-counterparts.md       开源对标项目
```

## 不上传的内容

- Obsidian 正式库 `.obsidian/` 和笔记正文。
- 原始资料目录。
- 课程音频、视频、PDF、PPT、图片、压缩包。
- ASR/OCR 全文和中间产物。
- API Key、token、个人路径、同步盘内部状态。

## 快速使用

### 1. 构建本地证据索引

```powershell
python scripts/course_verify.py --root "你的项目目录" build
```

### 2. 查询课程术语

```powershell
python scripts/course_verify.py --root "你的项目目录" query --q "121工作流"
```

### 3. 批量核验术语

```powershell
python scripts/course_verify.py --root "你的项目目录" verify --terms "121工作流,卡片指数,个人成长速度"
```

### 4. 给 Obsidian vault 写入最小全流程入口

```powershell
powershell -ExecutionPolicy Bypass -File scripts/setup_obsidian_mvp_flow.ps1 -VaultPath "你的Obsidian库路径"
```

## 核心原则

1. 本地证据优先。
2. 缓存复用优先。
3. 不确定内容不写成确定事实。
4. 非课程主线内容不入库。
5. 正式库只保存最终可用结果。

## Obsidian-Assistance V4

### V4 是什么

V4 是 Obsidian-Assistance 的工程化学习系统生成器版本。它不是正式 Obsidian vault，也不包含真实课程内容；它提供一套可测试、可回滚、默认 dry-run 的工具链，用于生成课程学习包。

### V4 能生成什么

一门课程可以生成：

- 课程主页
- 课程地图 Canvas
- 逐节总结
- 知识卡片：概念 / 方法 / 案例
- 复习卡片
- 行动任务
- 视觉图解：流程图 / 思维导图 / 时间线
- 证据索引
- 导入报告

### 安全边界

- 不写正式 Obsidian vault。
- 不上传真实课程内容、原始素材、OCR/ASR 全文或私人配置。
- 所有写入默认 dry-run。
- 只有显式 `--apply` 才写文件。
- 对 vault 路径写入必须走 `scripts/v4/safe_vault_writer.py`。
- 覆盖已有文件前必须备份。
- V4 脚本不包含删除用户文件的逻辑。

### 如何生成 demo 课程

```powershell
python scripts/v4/generate_course_pack.py --course "V4 Demo课程" --output "examples/v4-demo-course" --apply
```

如果只想预览计划，不写文件：

```powershell
python scripts/v4/generate_course_pack.py --course "V4 Demo课程" --output "examples/v4-demo-course" --dry-run
```

### 如何从 JSON 课程规格生成

V4 也支持用 JSON 规格文件驱动生成，而不是只能生成固定 Demo。示例规格：

```text
examples/v4-course-spec.json
```

运行：

```powershell
python scripts/v4/generate_course_pack.py --spec examples/v4-course-spec.json --output "examples/spec-demo-course" --apply
```

`--spec` 至少需要提供 `course` 字段，可选提供 `lessons`、`concepts`、`methods`、`cases`、`reviews`、`actions`、`evidence` 等数组。

### V4 子生成器安全用法

以下子生成器与课程包生成器一样，默认只输出 dry-run 计划；只有显式 `--apply` 才写文件：

```powershell
python scripts/v4/generate_canvas_map.py --output "tmp/课程地图.canvas"
python scripts/v4/generate_canvas_map.py --output "tmp/课程地图.canvas" --apply

python scripts/v4/generate_mermaid_graph.py --course "Demo课程" --output "tmp/视觉图解"
python scripts/v4/generate_mermaid_graph.py --course "Demo课程" --output "tmp/视觉图解" --apply

python scripts/v4/generate_bases_views.py --course "Demo课程" --output "tmp/bases-view.json"
python scripts/v4/generate_bases_views.py --course "Demo课程" --output "tmp/bases-view.json" --apply
```

### 如何安装到测试 vault

推荐先建立一个空测试 vault，例如：

```text
D:/OBS-V4-DEMO
```

然后执行：

```powershell
python scripts/v4/generate_course_pack.py --course "V4 Demo课程" --vault "D:/OBS-V4-DEMO" --apply
```

写入前会通过 safe writer 校验路径；覆盖已有文件前会备份。

### 如何迁移到正式 vault

1. 先在测试 vault 中打开 Demo，确认 CSS、Dataview、Canvas、Mermaid 表现正常。
2. 确认无真实隐私内容进入输出。
3. 将 `snippets/v4/` 中 CSS 复制到正式 vault 的 snippets 目录并手动启用。
4. 对正式 vault 的课程生成必须显式 `--apply`，且保留 safe writer 备份报告。
5. 不建议直接把 examples 复制成真实课程内容；真实课程应从本地证据/OCR/转写生成。

### 推荐插件

P0：

- Dataview
- Tasks
- Canvas
- Mermaid 支持

P1：

- QuickAdd
- Style Settings
- Excalidraw

P2：

- Spaced Repetition
- Omnisearch
- Text Extractor

### 常见问题

**Q：V4 会不会直接改正式知识库？**  
A：不会。默认 dry-run；写 vault 必须显式 `--apply`。

**Q：Demo 是否包含真实课程？**  
A：不包含。Demo 明确标注“示例，不含用户真实课程内容”。

**Q：没有安装 pytest 怎么办？**  
A：仓库内提供了一个极小的 `python -m pytest` 兼容入口，仅用于本项目离线环境下运行当前测试。真实 CI 环境可替换为标准 pytest。

**Q：如何验证安全边界？**  
A：运行：

```powershell
python -m pytest tests -q
python scripts/v4/obsidian_v4_audit.py .
```

