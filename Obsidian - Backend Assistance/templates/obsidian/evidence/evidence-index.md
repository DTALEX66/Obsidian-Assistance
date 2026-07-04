---
title: V6 证据索引模板
type: evidence-index
course: "{{course}}"
status: active
created: {{date}}
updated: {{date}}
tags:
  - evidence
  - v6
  - course-verification
---

# {{course}}｜11_证据索引

> [!warning] 证据边界
> 本页只登记已打开核验或待核验的证据。文件名/路径候选不是证据，必须记录页码/时间点后才能升级为 A/B 级证据。

## 证据表

| ID | 类型 | 来源 | 页码/时间点 | 输出图片 | 置信度 | 状态 | 说明 |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  | C | candidate-only | 待核验 |

## 待核验队列

```dataview
TABLE confidence AS 置信度, status AS 状态, source_path AS 来源
FROM "02_课程库/{{course}}"
WHERE contains(tags, "evidence") AND status != "verified"
SORT file.mtime DESC
```
