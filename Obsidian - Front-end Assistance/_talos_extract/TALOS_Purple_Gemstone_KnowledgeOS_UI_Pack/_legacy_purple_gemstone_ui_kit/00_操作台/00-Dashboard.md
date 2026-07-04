---
cssclasses:
  - pg-dashboard-page
aliases:
  - Home
  - Obsidian Console
type: dashboard
status: active
created: 2026-07-04
---

<div class="pg-dashboard">

<div class="pg-grid-main">

<div class="pg-stack">

<div class="pg-hero">
<p class="pg-kicker">Purple Gemstone Console</p>
<h1 class="pg-title">👋 Good morning, Alex</h1>
<p class="pg-subtitle">把课程、项目、设计资产、AI 调度与复习统一放进一个 Obsidian 操作台。</p>
<div class="pg-divider"></div>
<div class="pg-row">
<a class="pg-button" href="obsidian://new?vault=YOUR_VAULT_NAME&name=Daily%20Notes/{{date}}">打开今日笔记</a>
<a class="pg-button secondary" href="obsidian://open?vault=YOUR_VAULT_NAME&file=00_操作台/01-Review-Session">开始复习</a>
<a class="pg-button secondary" href="obsidian://open?vault=YOUR_VAULT_NAME&file=02_Canvas/AI知识工作流.canvas">打开知识画布</a>
</div>
</div>

<div class="pg-card">
<p class="pg-kicker">Today Focus</p>
<ul class="pg-list">
<li>✅ 课程拆解 → 原子笔记 → 双链入库</li>
<li>✅ 设计项目 → 素材收集 → 方案沉淀</li>
<li>✅ AI 项目 → GitHub 筛选 → 开发卡片</li>
<li>✅ 晚间复盘 → 明日计划</li>
</ul>
</div>

<div class="pg-grid-2">
<div class="pg-card">
<p class="pg-kicker">Quick Capture</p>
<p class="pg-subtitle">快速收集，不在入口处思考分类。</p>
<div class="pg-row">
<span class="pg-pill">Note</span><span class="pg-pill blue">Task</span><span class="pg-pill green">Idea</span><span class="pg-pill orange">Quote</span>
</div>

```dataview
TABLE WITHOUT ID file.link AS "最近收集", type AS "类型", status AS "状态"
FROM "00_Inbox" OR #inbox
SORT file.mtime DESC
LIMIT 8
```
</div>

<div class="pg-card">
<p class="pg-kicker">Vault Stats</p>
<div class="pg-grid-2">
<div class="pg-stat"><span class="num">= this.file.links.length</span><span class="label">当前页链接</span></div>
<div class="pg-stat"><span class="num">∞</span><span class="label">知识增长</span></div>
</div>
<p class="pg-subtitle">建议用 DataviewJS 扩展全库统计。</p>
</div>
</div>

</div>

<div class="pg-stack">

<div class="pg-card">
<p class="pg-kicker">Recent Notes</p>
```dataview
TABLE WITHOUT ID file.link AS "笔记", dateformat(file.mtime, "MM-dd HH:mm") AS "更新"
FROM ""
WHERE file.name != this.file.name
SORT file.mtime DESC
LIMIT 10
```
</div>

<div class="pg-card">
<p class="pg-kicker">Reading Queue</p>
```dataview
TABLE WITHOUT ID file.link AS "书籍/课程", progress AS "进度", status AS "状态"
FROM #book OR #course
SORT file.mtime DESC
LIMIT 8
```
</div>

<div class="pg-card">
<p class="pg-kicker">Project Atlas</p>
```dataview
TABLE WITHOUT ID file.link AS "项目", status AS "状态", priority AS "优先级"
FROM #project
WHERE status != "done"
SORT priority ASC, file.mtime DESC
LIMIT 8
```
</div>

</div>

<div class="pg-stack">

<div class="pg-card">
<p class="pg-kicker">Calendar</p>
<p class="pg-subtitle">这里由 Calendar / Periodic Notes 插件承接。</p>
<div class="pg-grid-4">
<div class="pg-stat"><span class="num">M</span><span class="label">Mon</span></div>
<div class="pg-stat"><span class="num">T</span><span class="label">Tue</span></div>
<div class="pg-stat"><span class="num">W</span><span class="label">Wed</span></div>
<div class="pg-stat"><span class="num">T</span><span class="label">Thu</span></div>
</div>
</div>

<div class="pg-card">
<p class="pg-kicker">Backlinks & Tags</p>
<span class="pg-pill">#project</span><span class="pg-pill">#ai</span><span class="pg-pill">#design</span><span class="pg-pill">#course</span>
<div class="pg-divider"></div>
```dataview
LIST FROM [[]]
LIMIT 8
```
</div>

<div class="pg-card">
<p class="pg-kicker">AI Actions</p>
<ul class="pg-list">
<li>总结当前笔记</li>
<li>生成双链建议</li>
<li>提取课程卡片</li>
<li>创建项目任务</li>
<li>同步到 Review 队列</li>
</ul>
</div>

</div>

</div>

</div>
