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
  course_verify.py          本地证据索引、查询、核验脚本
  setup_obsidian_mvp_flow.ps1 参数化 Obsidian 全流程 MVP 写入脚本
docs/
  data-boundary.md                  数据边界与防外溢规则
  pipeline-acceleration.md          加速转化与状态机方案
  pipeline-v2-full-flow.md          课程处理全流程规范
  project-experience-2026-07-01.md  项目经验总结：长循环、自检、全网比校
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

