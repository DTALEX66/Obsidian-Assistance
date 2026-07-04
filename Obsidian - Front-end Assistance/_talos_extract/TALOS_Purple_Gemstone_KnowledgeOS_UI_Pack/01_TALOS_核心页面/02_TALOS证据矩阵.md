---
title: TALOS 证据矩阵
type: talos-evidence-matrix
status: active
tags: [talos, evidence, verified, pending, missing]
cssclasses: [talos-purple-gemstone, talos-evidence-page]
---

# TALOS 证据矩阵

> [!talos-hero] Evidence Matrix
> 目标：所有课程证据必须显示来源、页码/时间戳、验证状态。参考图、OER、AI 摘要不得伪装成真实证据。

## 证据状态定义

| 状态 | 含义 | 可用于课程证据 | UI 显示 |
|---|---|---:|---|
| `#verified` | 真实截图 / 关键帧 / PDF页图，来源可追溯 | 是 | 绿色 |
| `#pending` | 候选帧或来源待核验 | 否 | 金色 |
| `#missing` | 课程缺少证据 | 否 | 红色 |
| `#reference-only` | 参考图、风格图、AI配图 | 否 | 蓝色 |
| `#oer` | 外部开放知识交叉对比 | 辅助 | 紫色 |

## 证据矩阵表

| 课程 | 视觉索引 | 真实截图/关键帧/PDF页图 | OER 对比 | 当前状态 | 下一步 |
|---|---:|---:|---:|---|---|
| 示例课程 A | 有 | 有 | 有 | #verified | 进入复习 |
| 示例课程 B | 有 | 无 | 有 | #reference-only | 补真实证据 |
| 示例课程 C | 无 | 无 | 无 | #missing | 建立证据页 |
| 示例课程 D | 有 | 待核验 | 无 | #pending | 核验来源 |

## Dataview：证据页自动汇总

```dataview
TABLE course, evidence_type, source_path, page, timestamp, status
FROM ""
WHERE type = "evidence"
SORT status ASC, course ASC
```

> [!talos-warning] 核验规则
> 每个 evidence 文件至少要包含：`course`、`evidence_type`、`source_path`、`status`。视频关键帧必须含 `timestamp`；PDF页图必须含 `page`。

## Rejected / 待核验队列

```dataview
TABLE course, reason, source_path, updated
FROM ""
WHERE type = "evidence" AND contains(tags, "rejected") OR contains(tags, "pending")
SORT updated DESC
```
