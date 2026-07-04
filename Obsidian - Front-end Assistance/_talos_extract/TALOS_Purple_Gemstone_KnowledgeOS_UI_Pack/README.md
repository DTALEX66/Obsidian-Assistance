# TALOS Purple Gemstone KnowledgeOS UI Pack

这是一套把上一轮 **Purple Gemstone Obsidian UI 组图** 与你上传的 **TALOS UI/UX 设计师交接包** 合并后的可执行包。

它的定位不再只是“美化 Obsidian”，而是：

> 在 Obsidian 里搭建一个深紫黑、紫晶发光、证据驱动、课程/复习/项目/AI 闭环的 TALOS KnowledgeOS 操作台。

## 1. 安装方式

1. 先备份你的 Vault。
2. 将本包内容复制到你的 Obsidian Vault 根目录。
3. 打开 Obsidian → Settings → Appearance → CSS snippets → Reload snippets。
4. 启用 `talos-purple-gemstone-knowledgeos.css`。
5. 打开核心插件：Canvas、Graph view、Backlinks、Outline、Templates、Daily notes、Bookmarks、Properties、Bases。
6. 建议安装社区插件：Dataview、Tasks、Calendar、Templater、Style Settings、Homepage、Commander、QuickAdd、Kanban、Excalidraw、Smart Connections / Copilot。
7. 打开 `00_TALOS_入口/00_TALOS_Home_Console.md`，切换阅读模式。

## 2. 这次合并后的核心变化

| 原 Purple Gemstone 包 | 合并 TALOS 后 |
|---|---|
| Dashboard 首页 | TALOS Home Console 主操作台 |
| Reading Workspace | Course Reader 课程阅读 + 证据 Inspector |
| Canvas 脑图 | Project Atlas / 领域作战地图 / 课程转项目 |
| Review + AI | 主动训练中心 + AI 证据核验提示 |
| 组件库 | Design System + Figma + Dev Notes + 验收标准 |
| 视觉资产 | 区分参考图、真实截图、PDF页图、OER、AI摘要 |

## 3. 包内结构

```text
.obsidian/snippets/talos-purple-gemstone-knowledgeos.css
00_TALOS_入口/00_TALOS_Home_Console.md
00_TALOS_入口/17_TALOS界面导航矩阵.md
01_TALOS_核心页面/02_TALOS证据矩阵.md
01_TALOS_核心页面/04_TALOS课程指挥舱.md
01_TALOS_核心页面/09_TALOS主动训练中心.md
01_TALOS_核心页面/16_TALOS睡觉模式执行台.md
01_TALOS_核心页面/29_TALOS_Project_Atlas.md
01_TALOS_核心页面/30_TALOS_Review_AI_Center.md
01_TALOS_核心页面/31_TALOS_Course_Reading_Layout.md
02_TALOS_模板/*.md
03_TALOS_Canvas/TALOS_Project_Atlas.canvas
04_TALOS_设计规范/TALOS_全量匹配一比一执行方案.md
04_TALOS_设计规范/TALOS_Purple_Gemstone_Design_System.md
04_TALOS_设计规范/TALOS_页面优先级与验收清单.md
05_TALOS_Codex开发包/CODEX_TALOS_UI_Implementation_Brief.md
06_TALOS_Figma交付包/Figma_TALOS_UI_File_Structure.md
07_TALOS_视觉参考图/*.png
99_原始资料/36_TALOS_UI_UX_Design_Handoff.md
_legacy_purple_gemstone_ui_kit/ 上一版包
```

## 4. 第一阶段执行顺序

1. 先启用 CSS snippet，完成全局壳层美化。
2. 设置 `00_TALOS_Home_Console.md` 为首页。
3. 把已有 TALOS 页面链接到 `17_TALOS界面导航矩阵.md`。
4. 先做 P0 页面：Home Console、Course Reader、Evidence Matrix、Review + AI。
5. 再做 P1 页面：Project Atlas、Kanban、Visual Coverage、Sleep Mode。
6. 最后交给 Codex 做轻插件化：命令、侧栏、状态栏、数据聚合。

## 5. 不可破坏的边界

- 不移动正式课程文件。
- 不把参考图伪装成证据。
- 不把 OER/AI 摘要伪装成本地证据。
- 不依赖大段 raw HTML。
- 窄屏不得出现竖排、挤压、重叠。
- AI 只辅助总结与关联，所有结论回本地证据核验。
