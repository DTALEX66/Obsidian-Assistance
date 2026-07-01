# V4 YAML Schema 标准

## 目标

统一 Obsidian 学习系统输出文件的 frontmatter 字段。

## 必填字段

```yaml
type: course|lesson|concept|method|case|review|action|evidence|pending|report|visual
status: inbox|processing|verified|blocked|done
course: 文本
lesson: 文本或空字符串
source_type: demo|pdf|video|audio|manual|generated
source_path: 文本
evidence_id: 文本
confidence: high|medium|low|unknown
review_level: new|learning|reviewing|mastered
difficulty: 1
priority: 1
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: []
aliases: []
links: {}
cssclasses: []
```

## 执行要求

- 模板变量统一使用 `{{variable}}`。
- `type/status/confidence` 必须在允许枚举内。
- 日期由生成器填充。

## 验收标准

- 所有模板 Markdown 含 YAML。
- Demo 课程 Markdown 通过 schema 校验。

## 安全边界

- 本规范只服务辅助仓库，不要求写入正式 Obsidian vault。
- 文档中不得包含真实课程正文、原始素材、转写全文、OCR 全文、token 或 API key。
- 所有示例路径必须使用占位符或 demo 路径，不能依赖用户正式库路径。

