---
title: TALOS Course Reading Layout
type: talos-course-reading-layout
status: active
tags: [talos, course-reader, reading]
cssclasses: [talos-purple-gemstone, talos-reader-page]
---

# TALOS Course Reading Layout

> [!talos-hero] Course Reader
> 长时间阅读区必须舒适、不卡、无竖排；右侧 Inspector 必须能看到属性、证据、复习卡。

## 推荐工作区布局

| 区域 | 内容 | Obsidian 执行方式 |
|---|---|---|
| 左侧 | 课程目录 / Bookmarks / 文件树 | 原生侧栏 + Bookmarks |
| 中间 | 课程正文阅读 | Reading view |
| 右侧 | Properties / Backlinks / Outline / Evidence meta | 右侧边栏 |
| 底部 | 字数、反链、Vault 状态 | Status bar |

## 当前课程属性模板

```yaml
type: course
status: active
field: AI
progress: 0%
evidence_status: pending
project_status: none
oer_status: none
tags: [course]
cssclasses: [talos-purple-gemstone, talos-course-page]
```

## 证据 Inspector

| 证据项 | 来源 | 页码/时间戳 | 状态 | 动作 |
|---|---|---|---|---|
| PDF 页图 | `assets/evidence/course-a/page-12.png` | p.12 | #verified | 打开图片 |
| 视频关键帧 | `assets/evidence/course-a/00-12-30.png` | 00:12:30 | #pending | 复核 |
| 参考配图 | `assets/reference/course-a/ref-01.png` | 无 | #reference-only | 不作为证据 |

> [!talos-ai] AI 使用边界
> AI 可以总结、连接、生成问题，但所有答案必须回到本地证据页核验。
