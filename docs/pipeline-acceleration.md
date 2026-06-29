# 加速转化与全流程跑通方案

## 核心判断

课程转化慢，通常不是某个工具慢，而是没有状态机和缓存：

- 每门课重复识别、重复转写、重复核验。
- OCR / ASR 结果没有统一复用。
- 课程总结必须等所有材料齐，导致整体阻塞。
- Obsidian 入口和处理脚本没有统一调度。

## 三档处理模式

### 快速入库

目标：先让课程出现在 Obsidian。

输出：

- 课程总览
- 素材识别报告
- 转写/OCR 队列
- Obsidian 入口卡片

### 标准入库

目标：课程可学习、可复习、可检索。

输出：

- 逐节课总结
- 术语索引
- 实操工作流
- 知识卡片
- 复习卡片
- 导入报告

### 精修模式

目标：高准确度、可长期复习。

输出：

- 关键图表解释
- 关键帧 OCR
- 外部资料核验
- Canvas / Bases / 学习路线

## 状态机

```text
new
  -> inventoried
  -> needs_ocr / needs_asr
  -> collected
  -> verified
  -> drafted
  -> imported
  -> archived
```

每次运行只推进能推进的步骤，不等待整门课全部完成。

## 缓存策略

每门课建议维护：

```text
work/courses/<course-id>/manifest.json
work/courses/<course-id>/text/
work/courses/<course-id>/ocr/
work/courses/<course-id>/asr/
work/courses/<course-id>/reports/
outputs/courses/<course-id>/final/
```

manifest 记录：

- 源文件路径、大小、修改时间、hash。
- 是否已 OCR。
- 是否已 ASR。
- 是否已核验。
- 是否已生成 Obsidian 包。
- 是否已入库。

## 下一步模块

建议新增：

```text
skills/course-pipeline/
scripts/course_pipeline.py
```

用于扫描课程、生成 manifest、推进状态、调用 `course_verify.py`、生成 Obsidian 写入包。

