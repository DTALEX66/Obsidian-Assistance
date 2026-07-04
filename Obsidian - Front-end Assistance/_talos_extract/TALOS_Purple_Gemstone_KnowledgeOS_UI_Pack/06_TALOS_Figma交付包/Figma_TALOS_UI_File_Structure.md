# Figma：TALOS Purple Gemstone UI 文件结构

```text
TALOS Purple Gemstone UI
├── 00 Cover & Product Principles
├── 01 IA / User Flows
├── 02 Foundations / Tokens
├── 03 Obsidian Shell
├── 04 Home Console
├── 05 Course Library + Reader
├── 06 Evidence Matrix + Media Viewer
├── 07 Review + AI Center
├── 08 Project Atlas + Kanban
├── 09 OER + Sleep Mode Console
├── 10 Native Plugin Components
├── 11 Responsive Frames
└── 12 Dev Notes / Obsidian Mapping
```

## 必须输出的 Frame

| Frame | 尺寸 | 内容 |
|---|---:|---|
| Obsidian Shell | 1600×1000 | Ribbon、左导航、tabs/search、正文、Inspector、状态栏 |
| Home Console | 1600×1000 | Hero、指标卡、三栏导航、Recent Focus、Status Strip |
| Course Reader | 1600×1000 | 左目录、中正文、右属性/证据/复习卡 |
| Evidence Matrix | 1600×1000 | 状态矩阵、热力图、图片证据浏览器 |
| Review + AI | 1600×1000 | 复习概览、问题卡、评分条、AI助手 |
| Project Atlas | 1600×1000 | Canvas、节点、分组、资产区、右侧属性 |
| Sleep Mode | 1600×1000 | 当前轮次、队列、日志、安全边界 |
| Responsive | 1440/1280/1040/760/520 | 断点规范 |

## Dev Notes

每个组件都必须标注 Obsidian 落地方式：

- Markdown table
- Callout
- YAML Properties
- Dataview query
- Tasks query
- Canvas node
- Kanban card
- CSS selector
- 需要自研插件
