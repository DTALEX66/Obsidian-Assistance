# Obsidian-Assistance

GitHub：`DTALEX66/Obsidian-Assistance`

这是 Obsidian / OBS 增强项目的云端总目录。当前仓库按本地总目录重新归类，统一包含后端增强与前端增强两个子目录。

## 目录结构

```text
Obsidian-Assistance/
├─ Obsidian - Backend Assistance/      后端增强目录
└─ Obsidian - Front-end Assistance/    前端增强目录
```

## 子项目定义

### `Obsidian - Backend Assistance/`

- 方向：Obsidian 后端增强、脚本、模板、流程、安全写入、测试、脱敏文档。
- 调用：Hermes Agent。
- 内容：course verifier、vault 写入工具、课程包生成器、证据索引、回归测试、GitHub Actions 等。

### `Obsidian - Front-end Assistance/`

- 方向：Obsidian 前端/UI 增强、界面设计、Open Design 产物承接、视觉/交互验证。
- 调用：Open Design。
- 内容：UI 原型、TALOS 前端包、设计交接、兼容性/插件映射、视觉参考资产等。

## Hermes 负责范围

Hermes 默认主责：

- `Obsidian - Backend Assistance/`：后端增强、脚本、模板、测试、安全写入、脱敏文档；
- 根目录工程卫生：Git、`.gitignore`、上传前安全审计、README/项目定义；
- 前后端协作：把 Open Design 产物整理进仓库、检查边界、维护交接和数据协议。

Hermes 不默认接管 Open Design 的 UI 视觉主导权。详细边界见：`HERMES_SCOPE.md`。

## 云端清理边界

本仓库上传的是可公开、可复用、可继续开发的增强项目文件；不上传正式 Obsidian vault、私人笔记、同步盘状态、密钥、token、原始课程资料、音视频/PDF/PPT 大文件、ASR/OCR 全文或临时缓存。

压缩包、运行缓存、Open Design 本地运行技能缓存等已通过 `.gitignore` 排除；必要素材以解包后的脱敏项目文件形式保留。
