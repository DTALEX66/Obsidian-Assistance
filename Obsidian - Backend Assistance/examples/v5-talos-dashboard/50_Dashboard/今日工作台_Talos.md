---
title: 今日工作台 Talos Demo
type: dashboard
status: active
created: 2026-07-01
updated: 2026-07-01
tags: [dashboard, demo, knowledgeos-v5]
---

# 今日工作台 Talos Demo

<div class="knowledgeos-v5 talos-dashboard">

<section class="talos-hero">
  <div>
    <p class="talos-kicker">DEMO / KNOWLEDGE OS</p>
    <h2>从文件仓库变成知识中控台</h2>
    <p>这个 demo 展示 V5 Talos-like Dashboard 的视觉和信息架构，不包含真实笔记。</p>
  </div>
  <div class="talos-orb">V5</div>
</section>

<div class="talos-grid talos-grid-4">
<div class="talos-card"><strong>课程库</strong><span>课程门户和学习路径。</span></div>
<div class="talos-card"><strong>知识卡片</strong><span>概念、方法、证据。</span></div>
<div class="talos-card"><strong>健康度</strong><span>缺 YAML、待审核、阻塞项。</span></div>
<div class="talos-card"><strong>MOC</strong><span>主题级入口。</span></div>
</div>

## Demo 查询

```dataview
TABLE type, status, tags
FROM ""
SORT file.mtime DESC
LIMIT 10
```

</div>
