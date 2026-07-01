---
title: 知识库健康度 Talos
type: dashboard
status: active
created: "{{date}}"
updated: "{{date}}"
tags:
  - dashboard
  - health
  - knowledgeos-v5
---

# 知识库健康度 Talos

<div class="knowledgeos-v5 talos-dashboard">

## 健康检查入口

<div class="talos-grid talos-grid-4">
<div class="talos-card"><strong>缺 YAML</strong><span>需要脚本或人工巡检。</span></div>
<div class="talos-card"><strong>待审核</strong><span>status=review 或 tags 含待审核。</span></div>
<div class="talos-card"><strong>阻塞项</strong><span>status=blocked。</span></div>
<div class="talos-card"><strong>最近活跃</strong><span>7 天内修改。</span></div>
</div>

## 待审核 / 阻塞

```dataview
TABLE status, updated, tags
FROM ""
WHERE status = "blocked" OR status = "review" OR contains(tags, "待审核")
SORT updated DESC
LIMIT 50
```

## 最近 7 天活跃

```dataview
TABLE file.mtime AS 修改时间, type, status
FROM ""
WHERE file.mtime >= date(today) - dur(7 days)
SORT file.mtime DESC
LIMIT 50
```

## 导入报告

```dataview
TABLE updated, status, tags
FROM "93_导入报告"
SORT file.mtime DESC
LIMIT 30
```

</div>
