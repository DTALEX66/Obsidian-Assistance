# Obsidian 后端增强目录定义

更新时间：2026-07-04

## 1. 云端归属

- GitHub 仓库：`DTALEX66/Obsidian-Assistance`
- 云端路径：`Obsidian - Backend Assistance/`
- 本地路径：`D:\All projects\Obsidian-Assistance\Obsidian - Backend Assistance`
- 项目性质：**Obsidian 后端增强目录**
- 主要调用方：Hermes Agent

该目录是 Obsidian-Assistance 云端总仓库中的后端增强子目录，与同级 `Obsidian - Front-end Assistance/` 前端增强目录共同组成当前云端总目录结构。

## 2. 本地/云端分类

```text
D:\All projects\Obsidian-Assistance\
├─ Obsidian - Backend Assistance\
│  └─ 用途：OBS/Obsidian 后端增强、脚本、模板、流程、安全写入、测试、脱敏文档
│     负责人/调用：Hermes
│
└─ Obsidian - Front-end Assistance\
   └─ 用途：OBS/Obsidian 前端 UI、界面设计、Open Design 调用与产物承接
      负责人/调用：Open Design
```

## 3. 后端目录边界

本目录允许保存：

- 后端辅助脚本、生成器、核验器、dry-run 工具；
- Obsidian 模板、CSS snippet、示例 demo vault 结构；
- 测试、GitHub Actions、脱敏项目文档；
- 与本地 vault 写入相关的安全边界和回滚规则。

本目录不保存：

- 正式 Obsidian vault；
- 私人笔记、同步盘状态、账号 token、API key；
- 原始课程资料、音视频、PDF/PPT/图片等大文件；
- ASR/OCR 全文、中间产物、未脱敏证据包。

## 4. 操作规则

1. Git 仓库根目录现在是 `D:\All projects\Obsidian-Assistance`，不是本子目录。
2. 对本目录的修改应从总目录执行 `git status/add/commit/push`。
3. 后端增强仍由 Hermes 主要负责；前端/UI 由 Open Design 主要负责。
4. 提交前必须确保不把正式 vault、私密资料或大文件缓存带入云端。
