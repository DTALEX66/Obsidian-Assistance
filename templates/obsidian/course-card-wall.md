---
title: 课程卡片墙
type: dashboard
status: active
created: "{{date}}"
updated: "{{date}}"
tags:
  - course
  - dashboard
  - knowledgeos-v5
---

# 课程卡片墙

<div class="knowledgeos-v5 talos-dashboard">

## 课程总览

```dataview
TABLE status, updated, tags
FROM "02_课程库"
WHERE type = "course" OR contains(tags, "course") OR contains(tags, "课程")
SORT updated DESC
LIMIT 100
```

## 领域入口

<div class="talos-grid talos-grid-3">
<div class="talos-card"><strong>AI 工具链</strong><span>模型、代理、自动化、知识管理。</span></div>
<div class="talos-card"><strong>设计系统</strong><span>UI、Dashboard、视觉规范。</span></div>
<div class="talos-card"><strong>教学资料</strong><span>课程、教案、实验、习题。</span></div>
</div>

</div>
