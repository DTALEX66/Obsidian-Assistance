---
title: "{{domain}}领域主页"
type: dashboard
domain: "{{domain}}"
status: active
created: "{{date}}"
updated: "{{date}}"
tags:
  - domain
  - knowledgeos-v5
related: []
---

# {{domain}}领域主页

<div class="knowledgeos-v5 talos-dashboard">

## 领域地图

<div class="talos-grid talos-grid-3">
<div class="talos-card"><strong>核心知识</strong><span>稳定概念与原则。</span></div>
<div class="talos-card"><strong>项目/课程</strong><span>实践材料与学习路径。</span></div>
<div class="talos-card"><strong>待补空白</strong><span>需要继续收集或验证。</span></div>
</div>

## 本领域笔记

```dataview
TABLE type, status, updated, tags
FROM ""
WHERE domain = "{{domain}}" OR contains(tags, "{{domain}}")
SORT updated DESC
LIMIT 80
```

## 精选入口

- [[MOC_{{domain}}]]

</div>
