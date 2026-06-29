# Obsidian UI 与插件体检清单

## 常见问题

Obsidian “不够绚丽好用”通常不是因为内容少，而是以下层缺失：

| 层级 | 常见缺口 |
|---|---|
| 主题 | 未安装/启用社区主题 |
| CSS | 没有 dashboard、cards、callout 样式 |
| 首页 | 没有统一总控台 |
| QuickAdd | 没有 choices |
| Templater | 模板未自动套用 |
| Meta Bind | 没有按钮和输入控件 |
| Dataview | 只有表格，没有卡片式视图 |
| Bases | 没有 `.base` 数据库视图 |
| AI 插件 | API / 索引 / 报错未处理 |

## MVP 路线

1. 先建立总控台。
2. 建立输入箱、课程处理、复习中心、待审核、导入报告入口。
3. 增强 CSS snippet。
4. 让 Dataview 查询出现在首页。
5. 再安装主题和配置 QuickAdd / Templater / Meta Bind。

## 推荐插件优先级

### P0

- Dataview
- Tasks
- Templater
- QuickAdd
- Style Settings

### P1

- Minimal Theme
- Minimal Theme Settings
- Meta Bind
- Commander
- Omnisearch
- Calendar / Periodic Notes

### P2

- Smart Connections
- Copilot
- Obsidian Local REST API
- MAKE.md

AI 插件建议晚一点接入，先保证本地流程和数据边界稳定。

