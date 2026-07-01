---
title: 知识库健康度 Talos Demo
type: dashboard
status: active
created: 2026-07-01
updated: 2026-07-01
tags: [dashboard, health, demo, knowledgeos-v5]
---

# 知识库健康度 Talos Demo

<div class="knowledgeos-v5 talos-dashboard">

<div class="talos-grid talos-grid-3">
<div class="talos-stat"><span>缺 YAML</span><strong>待脚本统计</strong><em>质量基础</em></div>
<div class="talos-stat"><span>待审核</span><strong>Dataview</strong><em>人工队列</em></div>
<div class="talos-stat"><span>最近更新</span><strong>7 days</strong><em>活跃信号</em></div>
</div>

```dataview
TABLE status, tags, file.mtime AS updated
FROM ""
WHERE status = "review" OR status = "blocked" OR contains(tags, "待审核")
SORT file.mtime DESC
LIMIT 20
```

</div>
