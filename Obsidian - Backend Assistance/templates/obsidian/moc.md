---
title: "MOC_{{topic}}"
type: moc
status: active
created: "{{date}}"
updated: "{{date}}"
tags:
  - moc
  - knowledgeos
related: []
---

# MOC_{{topic}}

<div class="knowledgeos-v5 talos-dashboard">

## 模块总览

> 这个 MOC 是主题入口，不存放长正文，只提供导航、索引和判断。

<div class="talos-grid talos-grid-3">
<div class="talos-card"><strong>核心概念</strong><br><span>本主题的基础定义和术语。</span></div>
<div class="talos-card"><strong>方法流程</strong><br><span>可复用步骤、检查表、操作法。</span></div>
<div class="talos-card"><strong>案例与证据</strong><br><span>课程、项目、文章、实践记录。</span></div>
</div>

## 自动索引

```dataview
TABLE status, updated, tags
FROM ""
WHERE contains(related, this.file.link) OR contains(tags, "{{topic}}")
SORT updated DESC
LIMIT 50
```

## 手动精选

- [[待补充]]

## 待补空白

- [ ] 概念是否完整？
- [ ] 是否有重复笔记？
- [ ] 是否缺少来源？

</div>
