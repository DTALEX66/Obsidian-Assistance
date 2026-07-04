---
type: "{{type}}"
status: "{{status}}"
course: "{{course}}"
lesson: "{{lesson}}"
source_type: "{{source_type}}"
source_path: "{{source_path}}"
evidence_id: "{{evidence_id}}"
confidence: "{{confidence}}"
review_level: new
difficulty: 1
priority: 1
created: "{{date}}"
updated: "{{updated}}"
tags:
  - knowledgeos
aliases: []
links:
  concepts: []
  methods: []
  cases: []
cssclasses:
  - knowledgeos-v4
---
# {{course}}｜课程流程图

```mermaid
flowchart TD
  A[输入素材] --> B[素材识别]
  B --> C[核验]
  C --> D[生成卡片]
  D --> E[复习与行动]
```
