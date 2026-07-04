# Obsidian-Assistance 项目定义

更新时间：2026-07-04

## 1. 云端归属

- GitHub 仓库：`DTALEX66/Obsidian-Assistance`
- 本地工作区：`D:\All projects\Obsidian-Assistance\Obsidian - Backend Assistance`
- 项目性质：**Obsidian 后端增强项目**
- 主要调用方：Hermes Agent

该仓库只代表后端增强方向，不再代表整个 `D:\All projects\Obsidian-Assistance` 父级工作区，也不包含本地 Open Design 前端/UI 工作区。

## 2. 本地父级工作区分类

```text
D:\All projects\Obsidian-Assistance\
├─ Obsidian - Backend Assistance\
│  └─ GitHub: DTALEX66/Obsidian-Assistance
│     用途：OBS/Obsidian 后端增强、脚本、模板、流程、安全写入、测试、脱敏文档
│     负责人/调用：Hermes
│
└─ Obsidian - Front-end Assistance\
   └─ Local workspace only for now
      用途：OBS/Obsidian 前端 UI、界面设计、Open Design 调用与产物承接
      负责人/调用：Open Design
```

## 3. 后端仓库边界

本仓库允许保存：

- 后端辅助脚本、生成器、核验器、dry-run 工具；
- Obsidian 模板、CSS snippet、示例 demo vault 结构；
- 测试、GitHub Actions、脱敏项目文档；
- 与本地 vault 写入相关的安全边界和回滚规则。

本仓库不保存：

- 正式 Obsidian vault；
- 私人笔记、同步盘状态、账号 token、API key；
- 原始课程资料、音视频、PDF/PPT/图片等大文件；
- ASR/OCR 全文、中间产物、未脱敏证据包；
- `Obsidian - Front-end Assistance` 的本地 Open Design 工作产物，除非后续明确迁移或新建前端仓库。

## 4. 前端/UI 工作区边界

`D:\All projects\Obsidian-Assistance\Obsidian - Front-end Assistance` 当前定义为本地 UI 增强目录：

- 主要方向：全部 UI 界面、Open Design 设计产物、前端视觉/交互验证；
- 当前状态：不属于 `DTALEX66/Obsidian-Assistance` 云端仓库；
- 后续如需云端化，优先独立定义前端仓库，避免与后端增强仓库混淆。

## 5. 操作规则

1. 对 `DTALEX66/Obsidian-Assistance` 的 pull/commit/push 默认只在 `Obsidian - Backend Assistance` 内执行。
2. Hermes 默认负责后端增强仓库的开发、验证、提交和推送。
3. Open Design 默认负责前端/UI 本地工作区，不把前端目录误提交到后端仓库。
4. 若需要把前端产物纳入云端，必须先重新定义仓库归属和同步策略。
