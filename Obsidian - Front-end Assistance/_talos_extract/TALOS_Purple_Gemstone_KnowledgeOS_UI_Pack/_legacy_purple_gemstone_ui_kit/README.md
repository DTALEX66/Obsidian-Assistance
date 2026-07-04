# Purple Gemstone Console｜Obsidian 全量匹配界面美化包

这是一套把“紫色晶石 / 科技暗色 / 操作台 / 知识图谱 / 复习系统 / AI 助手”落地到 Obsidian 的可执行方案。

> 目标：不是只看效果图，而是能放进 Vault 里启用、能改、能继续开发。

## 一、安装方式

1. 先备份你的 Vault。
2. 把本包内容复制到你的 Obsidian Vault 根目录。
3. 打开 Obsidian → Settings → Appearance → CSS snippets → Reload snippets → 启用 `purple-gemstone-console.css`。
4. 打开核心插件：Canvas、Graph view、Backlinks、Outline、Templates、Daily notes、Bases。
5. 建议安装社区插件：Dataview、Tasks、Calendar、Templater、Style Settings、Homepage、Commander、Smart Connections 或 Obsidian Copilot。
6. 打开 `00_操作台/00-Dashboard.md`，右上角阅读模式查看。
7. 打开 `02_Canvas/AI知识工作流.canvas`，查看知识画布模板。

## 二、包内文件

```text
.obsidian/snippets/purple-gemstone-console.css   # 全局主题与卡片组件 CSS
00_操作台/00-Dashboard.md                       # 首页仪表盘
00_操作台/01-Review-Session.md                  # 复习操作台
00_操作台/02-AI-Assistant-Panel.md              # AI 助手页
01_模板/Daily Note Template.md                  # 每日笔记模板
01_模板/Book Note Template.md                   # 书籍/课程笔记模板
01_模板/Project Atlas Template.md               # 项目中控模板
02_Canvas/AI知识工作流.canvas                   # Canvas 示例
03_设计规范/一比一拆解执行方案.md                # 逐图拆解与落地说明
03_设计规范/组件库与尺寸规范.md                  # 组件、尺寸、颜色、状态
04_可选脚本/install-purple-gemstone.ps1          # Windows 安装辅助脚本
assets/svg/*.svg                                # 可替换视觉素材
assets/prompts/visual-prompts.md                # 后续生成配图提示词
```

## 三、最重要的执行原则

- 先用 CSS Snippet 做全局视觉。
- 再用 Markdown + HTML class 做 dashboard 卡片。
- 用 Canvas 复刻“知识图谱 / 项目脑图”。
- 用 Dataview / Bases 做“最近笔记、项目、阅读、标签、资产表”。
- 用 Tasks 做“复习卡片、任务、今日队列”。
- 用 AI 插件做右侧助手；如果不想联网，就只做“AI 指令面板”，由 Codex/Hermes/本地模型读取对应 Markdown。

## 四、推荐项目命名

- Vault 名：`Purple Gemstone Knowledge OS`
- 主题名：`Purple Gemstone Console`
- 首页：`00-Dashboard.md`
- 项目中控：`Project Atlas`
