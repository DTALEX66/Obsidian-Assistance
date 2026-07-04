---
title: TALOS Home Console
type: talos-home-console
status: active
created: 2026-07-04
updated: 2026-07-04
tags: [talos, home-console, purple-gemstone, knowledgeos]
cssclasses: [talos-purple-gemstone, knowledgeos-v5, talos-global-page]
---

# TALOS Home Console

> [!talos-hero] TALOS KnowledgeOS Command Center
> **深紫黑知识作战系统 / Purple Gemstone Console**
> 今日主线：课程阅读 → 证据核验 → 主动回忆 → 项目转化 → 执行日志。
> 快捷入口：[[17_TALOS界面导航矩阵|导航矩阵]] · [[04_TALOS课程指挥舱|课程指挥舱]] · [[02_TALOS证据矩阵|证据矩阵]] · [[30_TALOS_Review_AI_Center|Review + AI]] · [[29_TALOS_Project_Atlas|Project Atlas]] · [[16_TALOS睡觉模式执行台|睡觉模式]]

> [!talos-warning] 证据边界
> `参考配图` 只改善视觉；`真实截图/关键帧/PDF页图` 才能作为证据。OER 与 AI 摘要必须显示为辅助来源，不得伪装成本地证据。

## Command Center 指标卡

| 模块 | 当前状态 | 点击入口 | 验收标准 |
|---|---:|---|---|
| Review | 92 张复习卡/中心文件 | [[30_TALOS_Review_AI_Center]] | 能进入今日问题卡、评分、错题日志 |
| Evidence | 16 门课程有真实截图/关键帧/PDF页图 | [[02_TALOS证据矩阵]] | verified/pending/missing 明确区分 |
| Projects | 30 门已有项目转化课程 | [[29_TALOS_Project_Atlas]] | 项目卡可追踪下一步动作 |
| OER | 4 门已有 OER 交叉对比 | [[15_TALOS开放知识交叉对比]] | OER 显示为辅助，不覆盖本地证据 |
| TALOS Pages | 26 个相关入口页 | [[17_TALOS界面导航矩阵]] | 入口可点击、分组清晰 |

## Workspace Navigation

| Navigation | Operating Queue | Inspector |
|---|---|---|
| [[04_TALOS课程指挥舱]] | 今日课程阅读 | 查看课程属性、证据、复习卡 |
| [[02_TALOS证据矩阵]] | 待核验证据 | 查看来源路径、页码、时间戳、状态 |
| [[09_TALOS主动训练中心]] | 今日主动回忆 | 查看错题、下一次复习、AI建议 |
| [[03_TALOS项目推进台]] | 项目下一步动作 | 查看目标、风险、输出物 |
| [[16_TALOS睡觉模式执行台]] | 自动循环队列 | 查看轮次、边界、resume point |

## Recent Focus

> [!talos-ai] 今日建议
> 1. 先打开 [[02_TALOS证据矩阵]]，筛选 `#pending` 与 `#missing`。
> 2. 再进入 [[30_TALOS_Review_AI_Center]]，只复习带本地证据的卡。
> 3. 把高价值课程转入 [[29_TALOS_Project_Atlas]]。
> 4. 所有执行过程写入 [[11_TALOS执行日志]]。

## Dataview 可选模块：最近 TALOS 页面

```dataview
TABLE type, status, updated
FROM ""
WHERE contains(tags, "talos")
SORT updated DESC
LIMIT 12
```

## Status Strip

| Vault | Mode | Theme | Guardrail |
|---|---|---|---|
| KnowledgeOS / TALOS | Local-first | Purple Gemstone | 不上传、不删源、不伪造、不移动课程 |
