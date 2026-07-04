---
cssclasses:
  - pg-dashboard-page
type: ai-panel
status: active
created: 2026-07-04
---

<div class="pg-page">
<div class="pg-hero">
<p class="pg-kicker">AI Assistant Panel</p>
<h1 class="pg-title">AI 助手操作台</h1>
<p class="pg-subtitle">这里不绑定某一个模型，作为 Hermes / Codex / DeepSeek / ChatGPT 的统一提示词面板。</p>
</div>

<div class="pg-grid-3">
<div class="pg-card"><p class="pg-kicker">Chat</p><p>基于当前笔记问答。</p></div>
<div class="pg-card"><p class="pg-kicker">Summarize</p><p>把长文转为摘要、卡片、行动项。</p></div>
<div class="pg-card"><p class="pg-kicker">Connect</p><p>补全双链、标签、MOC。</p></div>
</div>

## 标准提示词

### 1. 课程拆解
```text
你是我的 Obsidian 知识库整理助手。请读取当前笔记，把内容拆为：
1. 3-8 条原子笔记
2. 关键概念表
3. 可复习卡片
4. 应链接到的旧笔记
5. 放入哪个 MOC
输出 Markdown，保留来源，不要编造。
```

### 2. 设计项目沉淀
```text
请把当前设计项目笔记整理为：客户要求、设计风格、空间限制、可执行清单、材料工艺、风险点、下一步。
每条都要能落地执行，不要只写抽象形容词。
```

### 3. GitHub AI 项目筛选
```text
请把收集到的 GitHub 项目按：用途、star、活跃度、可吸收模块、接入 Obsidian/Hermes/Codex 的方式、风险，生成筛选表。
```
</div>
