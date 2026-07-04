# Obsidian-Assistance 项目定义

更新时间：2026-07-04

## 1. 云端总目录

- GitHub 仓库：`DTALEX66/Obsidian-Assistance`
- 本地总目录：`D:\All projects\Obsidian-Assistance`
- 项目性质：Obsidian / OBS 增强项目总仓库

该 GitHub 仓库现在按本地总目录结构重新上传和清理，仓库根目录包含后端增强与前端增强两个子目录。

## 2. 目录分类

```text
D:\All projects\Obsidian-Assistance\
├─ Obsidian - Backend Assistance\
│  ├─ 云端路径：Obsidian - Backend Assistance/
│  ├─ 项目性质：Obsidian/OBS 后端增强
│  └─ 调用方：Hermes
│
└─ Obsidian - Front-end Assistance\
   ├─ 云端路径：Obsidian - Front-end Assistance/
   ├─ 项目性质：Obsidian/OBS 前端 UI 增强
   └─ 调用方：Open Design
```

## 3. 后端增强目录

`Obsidian - Backend Assistance` 保存：

- Obsidian 后端辅助脚本、生成器、核验器、dry-run 工具；
- Obsidian 模板、CSS snippet、示例 demo vault 结构；
- 测试、GitHub Actions、脱敏项目文档；
- 与本地 vault 写入相关的安全边界和回滚规则。

## 4. 前端增强目录

`Obsidian - Front-end Assistance` 保存：

- Obsidian UI 原型、Open Design 设计产物、前端视觉/交互验证文件；
- TALOS / Purple Gemstone 风格界面参考；
- 前端兼容性、插件映射、vault 匹配与 UI 审计资料；
- 脱敏后的可复用设计素材。

## 5. 不上传内容

- 正式 Obsidian vault；
- 私人笔记、同步盘状态、账号 token、API key；
- 原始课程资料、音视频、PDF/PPT/图片等大文件；
- ASR/OCR 全文、中间产物、未脱敏证据包；
- 压缩包、运行缓存、Open Design 本地技能缓存。

## 6. 操作规则

1. Git pull/commit/push 默认在 `D:\All projects\Obsidian-Assistance` 总目录执行。
2. Hermes 主要负责后端增强目录的开发、验证、提交和推送。
3. Open Design 主要负责前端/UI 增强目录的设计产物与界面验证。
4. 上传云端前必须检查 `.gitignore`、大文件、密钥和私人 vault 边界。
