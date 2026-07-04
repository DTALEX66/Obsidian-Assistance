# Hermes 负责范围

更新时间：2026-07-04

本文件定义 Hermes 在 `D:\All projects\Obsidian-Assistance` 总目录下默认负责的部分，避免与 Open Design 的前端/UI职责混淆。

## 1. 总原则

```text
D:\All projects\Obsidian-Assistance\
├─ Obsidian - Backend Assistance\      Hermes 主责
└─ Obsidian - Front-end Assistance\    Open Design 主责，Hermes 只做协作/接线/安全检查
```

Hermes 的默认职责是：**后端增强、自动化脚本、数据边界、安全写入、测试验证、Git整理与云端同步**。

Open Design 的默认职责是：**前端界面、视觉、UI原型、交互稿、设计资产与界面验收**。

## 2. Hermes 主责目录

### `Obsidian - Backend Assistance/`

Hermes 直接负责该目录的设计、开发、验证和维护，包括：

- Obsidian 后端增强脚本；
- 课程资料处理流程、生成器、核验器；
- vault 安全写入、dry-run、备份与回滚逻辑；
- evidence / keyframe / OER / radar 等后端工具链；
- Obsidian 模板、CSS snippet、demo vault 结构；
- Python 测试、GitHub Actions、项目文档；
- 私密数据边界、上传前审计、`.gitignore` 与云端清理。

默认工作方式：

1. 在总目录执行 Git 操作：`D:\All projects\Obsidian-Assistance`。
2. 后端代码修改后在 `Obsidian - Backend Assistance` 内运行针对性测试。
3. 上传前检查大文件、密钥、正式 vault、缓存和临时产物。
4. 小步 commit + push，保持云端为最新事实源。

## 3. Hermes 协作目录

### `Obsidian - Front-end Assistance/`

该目录由 Open Design 主责。Hermes 默认不主导 UI 视觉，不把前端审美实现当作自己的主责；但可以做以下协作：

- 整理 Open Design 产物到云端目录结构；
- 检查前端产物是否含私密路径、压缩包、缓存或不应上传文件；
- 编写/维护前后端交接文档、接口说明、验收清单；
- 在用户明确要求时，辅助修复 HTML/CSS/JS、做浏览器预览、做兼容性检查；
- 将前端设计需求转化为后端脚本、模板、数据协议或导出格式。

Hermes 默认不做：

- 未经要求重设计 UI 风格；
- 用后端逻辑覆盖 Open Design 的视觉决策；
- 把 Open Design 本地运行缓存、`.od-skills`、压缩包或正式 vault 文件上传；
- 在没有验收目标时批量改前端视觉资产。

## 4. Hermes 负责的总目录级事项

在 `D:\All projects\Obsidian-Assistance` 根目录，Hermes 负责：

- Git 仓库状态、提交、推送；
- 根目录 `README.md`、`PROJECT_DEFINITION.md`、`HERMES_SCOPE.md`；
- 根目录 `.gitignore` 与上传边界；
- 云端目录结构一致性；
- 上传前安全审计：密钥、私人 vault、原始资料、大文件、缓存；
- 后端测试与必要的 ad-hoc 验证。

## 5. 责任边界一句话

> Hermes 管后端增强和云端工程卫生；Open Design 管前端 UI 和视觉产物。Hermes 可以协助前端接线、验证和整理，但默认不越权接管 UI 设计。
