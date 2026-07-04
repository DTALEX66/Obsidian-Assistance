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
# {{course}} 导入报告

## 1. 处理范围

{{summary}}

## 2. 生成文件

{{content}}

## 3. 过滤内容

{{pending_review}}

## 4. 安全检查

- [ ] 未包含真实课程大段原文
- [ ] 未包含 token/API key
- [ ] 未写入正式 vault
