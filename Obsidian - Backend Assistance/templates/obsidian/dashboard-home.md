---
title: 今日工作台 Talos
type: dashboard
status: active
created: "{{date}}"
updated: "{{date}}"
tags:
  - dashboard
  - knowledgeos-v5
  - talos
---

# 今日工作台 Talos

<div class="knowledgeos-v5 talos-dashboard">

<section class="talos-hero">
  <div>
    <p class="talos-kicker">KNOWLEDGE OS</p>
    <h2>今天从这里进入知识库</h2>
    <p>这不是文件树首页，而是使用层中控：课程、卡片、复习、领域、信号全部从这里进入。</p>
  </div>
  <div class="talos-orb">OBS</div>
</section>

<div class="talos-grid talos-grid-5">
  <div class="talos-stat"><span>课程库</span><strong>Dataview</strong><em>动态统计</em></div>
  <div class="talos-stat"><span>知识卡片</span><strong>Cards</strong><em>沉淀资产</em></div>
  <div class="talos-stat"><span>待审核</span><strong>Review</strong><em>人工确认</em></div>
  <div class="talos-stat"><span>最近更新</span><strong>7 days</strong><em>活跃信号</em></div>
  <div class="talos-stat"><span>健康度</span><strong>Check</strong><em>质量入口</em></div>
</div>

## 快速入口

<div class="talos-grid talos-grid-4">
  <a class="talos-card talos-link" href="obsidian://open?file=02_课程库/02_课程卡片墙">课程卡片墙</a>
  <a class="talos-card talos-link" href="obsidian://open?file=03_知识卡片/00_知识卡片总览">知识卡片总览</a>
  <a class="talos-card talos-link" href="obsidian://open?file=04_复习卡片/00_复习中心">复习中心</a>
  <a class="talos-card talos-link" href="obsidian://open?file=93_导入报告">导入报告</a>
</div>

## 最近更新

```dataview
TABLE file.mtime AS 修改时间, type, status
FROM ""
WHERE file.name != this.file.name
SORT file.mtime DESC
LIMIT 20
```

## 待处理信号

```dataview
TABLE status, updated, tags
FROM ""
WHERE status = "blocked" OR status = "review" OR contains(tags, "待审核")
SORT updated DESC
LIMIT 30
```

</div>
