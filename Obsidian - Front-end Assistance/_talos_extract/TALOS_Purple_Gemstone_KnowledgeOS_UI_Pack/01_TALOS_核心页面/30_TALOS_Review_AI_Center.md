---
title: TALOS Review + AI Center
type: talos-review-ai-center
status: active
tags: [talos, review, ai, active-recall]
cssclasses: [talos-purple-gemstone, talos-review-page]
---

# TALOS Review + AI Center

> [!talos-hero] Review + AI 主动训练中心
> 主动训练闭环：今日问题 → 展开答案 → 回证据核验 → Again/Hard/Good/Easy → 错题日志 → 下一次复习。

## Review Overview

| 指标 | 值 | 说明 |
|---|---:|---|
| Retention | 62% | 示例值，后续用插件/Dataview 驱动 |
| Due Cards | 52 | 今日到期卡 |
| Streak | 14 days | 连续复习 |
| Accuracy | 92% | 今日正确率 |

## 今日问题卡

> [!talos-evidence] Question
> 什么内容可以被算作 TALOS 的真实课程证据？

<details>
<summary>Show Answer</summary>

真实课程证据必须可追溯到本地源材料，例如真实截图、视频关键帧、PDF 页图，并显示来源路径、页码或时间戳、验证状态。参考图、OER、AI 摘要只能辅助，不能伪装成证据。

</details>

## 评分条

| 按钮 | 含义 | 下一次复习建议 |
|---|---|---|
| Again | 完全不会 | 10 分钟 / 今日再次 |
| Hard | 模糊 | 1 天 |
| Good | 掌握 | 3 天 |
| Easy | 很熟 | 7 天 |

## Due Cards 查询

```dataview
TASK
FROM ""
WHERE contains(text, "#review") AND !completed
SORT due ASC
```

> [!talos-ai] AI Assistant
> Chat / Summarize / Connect / Plan 四个入口都必须加一句提示：**“请回本地证据页核验。”**

## 错题/复盘日志

| 日期 | 问题 | 错因 | 证据 | 下一步 |
|---|---|---|---|---|
| 2026-07-04 | 真实证据定义 | 混淆参考图 | [[02_TALOS证据矩阵]] | 补卡 |
