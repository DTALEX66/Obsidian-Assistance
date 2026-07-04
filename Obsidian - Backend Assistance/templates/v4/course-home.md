---
type: course
status: "{{status}}"
course: "{{course}}"
lesson: ""
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
  - course
  - knowledgeos
aliases: []
links:
  concepts: []
  methods: []
  cases: []
cssclasses:
  - knowledgeos-v4
  - course-home
  - dashboard
---
# {{course}}

> [!summary] 课程概览
> - 状态：`{{status}}`
> - 可信度：`{{confidence}}`
> - 来源类型：`{{source_type}}`
> - 来源路径：`{{source_path}}`
> - 说明：示例模板，不含用户真实课程内容。

## 今日入口

- [ ] 处理待审核内容
- [ ] 复习新卡片
- [ ] 完成项目行动
- [ ] 检查导入报告

## 学习进度

```dataview
TABLE WITHOUT ID
file.link AS 章节,
status AS 状态,
confidence AS 可信度
FROM "{{course_path}}/02_逐节总结"
SORT file.name ASC
```

## 课程地图 Canvas

![[01_课程地图.canvas]]

## 核心概念

```dataview
TABLE WITHOUT ID
file.link AS 概念,
review_level AS 复习,
confidence AS 可信度
FROM "{{course_path}}/03_知识卡片"
WHERE type = "concept"
SORT priority ASC
```

## 核心方法

```dataview
TABLE WITHOUT ID
file.link AS 方法,
difficulty AS 难度,
status AS 状态
FROM "{{course_path}}/03_知识卡片"
WHERE type = "method"
SORT priority ASC
```

## 关键案例

```dataview
TABLE WITHOUT ID
file.link AS 案例,
confidence AS 可信度
FROM "{{course_path}}/03_知识卡片"
WHERE type = "case"
```

## 复习中心

```dataview
TABLE WITHOUT ID
file.link AS 复习卡,
review_level AS 复习等级,
difficulty AS 难度
FROM "{{course_path}}/04_复习卡片"
SORT updated DESC
```

## 项目行动

```dataview
TASK
FROM "{{course_path}}/06_项目行动"
WHERE !completed
```

## 视觉图解

- [[05_视觉图解/课程流程图]]
- [[05_视觉图解/课程思维导图]]
- [[05_视觉图解/课程时间线]]

## 待人工确认

```dataview
TABLE WITHOUT ID
file.link AS 文件,
confidence AS 可信度,
pending_reason AS 原因
FROM "{{course_path}}"
WHERE confidence = "low" OR status = "blocked"
```

## 导入报告

![[08_导入报告]]
