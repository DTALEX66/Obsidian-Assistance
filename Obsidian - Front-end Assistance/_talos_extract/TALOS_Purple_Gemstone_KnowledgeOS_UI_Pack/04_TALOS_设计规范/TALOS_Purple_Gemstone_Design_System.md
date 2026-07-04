# TALOS Purple Gemstone Design System

## 1. 视觉关键词

- 深紫黑知识作战系统
- 紫晶发光边框
- 玻璃拟态卡片
- 细线框、低频柔光、克制动画
- 证据驱动、AI Study Companion、Canvas/Graph/Inspector

## 2. 色彩 Tokens

| Token | 色值 | 用途 |
|---|---|---|
| `--talos-bg-deep` | `#080B14` | 最深背景 |
| `--talos-bg` | `#0B0E18` | 主背景 |
| `--talos-surface` | `rgba(20,24,42,.80)` | 玻璃卡片 |
| `--talos-accent` | `#8B5CF6` | 主紫色 |
| `--talos-accent-2` | `#A970FF` | 霓虹紫 |
| `--talos-blue` | `#38BDF8` | 信息/参考图 |
| `--talos-green` | `#78E08F` | verified |
| `--talos-orange` | `#F59E0B` | pending/warning |
| `--talos-red` | `#FF5F7E` | missing/danger/rejected |
| `--talos-gold` | `#F5C96B` | sleep mode / highlight |

## 3. Obsidian Callout 组件

| Callout | 用途 |
|---|---|
| `[!talos-hero]` | 页面 Hero / Command Bar |
| `[!talos-evidence]` | 证据卡 / 问题卡 |
| `[!talos-ai]` | AI 建议 / Summary / Connect / Plan |
| `[!talos-warning]` | OER、参考图、候选帧提醒 |
| `[!talos-danger]` | 危险动作、安全边界 |
| `[!talos-verified]` | 已核验证据 |
| `[!talos-sleep]` | 睡觉模式 / 自动循环 |

## 4. 状态规范

| 状态 | 视觉 |
|---|---|
| Default | 暗色玻璃卡片 + 紫晶细边框 |
| Hover | 边框增强、轻微抬升、文字变亮 |
| Active | 左侧发光条、背景高亮、状态 chip |
| Focus | 键盘焦点环 |
| Loading | 轻量 shimmer，不强闪烁 |
| Empty | 空状态文案 + 下一步按钮 |
| Error | 红色边框 + 失败原因 |
| Warning | 金色边框 + 核验说明 |
| Verified | 绿色 chip + 来源路径 |
| Rejected | 红色 chip + 剔除原因 |
| Disabled | 降低透明度 + 禁止说明 |

## 5. 响应式

| 宽度 | 布局 |
|---|---|
| 1680+ | 左导航 + 主内容 + 右 Inspector |
| 1440 | 三栏压缩 |
| 1280 | Inspector 可折叠 |
| 1040 | 两栏，右侧内容下移 |
| 760 | 单栏，导航折叠 |
| 520 | 移动安全，表格横向滚动，图片单列 |
