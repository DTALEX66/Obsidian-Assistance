---
title: TALOS 课程指挥舱
type: talos-course-command
status: active
tags: [talos, course, command]
cssclasses: [talos-purple-gemstone, talos-course-page]
---

# TALOS 课程指挥舱

> [!talos-hero] Course Command Center
> 入口支持：课程库总览 → 课程卡片墙 → 单课程门户 → Course Reader → 证据页 → 复习卡 / 项目动作。

## 课程库总览

```dataview
TABLE field, status, progress, evidence_status, project_status, oer_status
FROM "02_课程库"
WHERE type = "course"
SORT field ASC, progress DESC
```

## 课程卡片墙字段规范

| 字段 | 用途 | 示例 |
|---|---|---|
| `field` | 领域 | AI / 设计 / 学习力 / 运营 |
| `status` | 学习状态 | inbox / active / done |
| `progress` | 进度 | 35% |
| `evidence_status` | 证据状态 | verified / pending / missing |
| `project_status` | 项目转化 | none / in-progress / done |
| `oer_status` | OER 对比 | none / matched / conflict |

> [!talos-evidence] 进入 Course Reader
> 打开 [[31_TALOS_Course_Reading_Layout]]，按“左目录 / 中正文 / 右证据 Inspector”的布局阅读课程。
