# 课程核验问题修复队列（2026-07-07）

> 只记录待办，不把未核验课程标完成。所有课程必须有真实 evidence 后才可关闭任务。

## 最新状态
- verified_by_available_methods: `31`
- needs_review: `8`
- environment: `tesseract=True`, `whisper=True`
- risk_counts: `{'raw_text_not_cross_confirmed': 8, 'audio_video_asr_unusable': 1, 'missing_visual_evidence': 1}`

## 修复队列
| 课程 | 优先动作 | 风险 | 原始源 | 本地索引 | Sidecar(text/visual/keyframe/asr) | OER | 视觉 | 文本交叉 |
|---|---|---|---:|---:|---|---:|---:|---|
| 品牌全案AI设计实战班 | text_crosscheck | raw_text_not_cross_confirmed、audio_video_asr_unusable | 35 | 0 | 5/5/0/0 | 0 | 47 | 0 terms / text-read |
| 敏感与待确认 | text_crosscheck, visual_evidence | raw_text_not_cross_confirmed、missing_visual_evidence | 1 | 0 | 0/0/0/0 | 0 | 0 | 0 terms / text-read |
| Photoshop AIGC商业设计 | text_crosscheck | raw_text_not_cross_confirmed | 99 | 0 | 0/0/3/3 | 3 | 53 | 1 terms / text-read |
| 传统文化与术数 | text_crosscheck | raw_text_not_cross_confirmed | 74 | 0 | 8/8/0/0 | 0 | 0 | 0 terms / text-read |
| 大脑训练 | text_crosscheck | raw_text_not_cross_confirmed | 5 | 0 | 1/1/0/0 | 0 | 23 | 0 terms / pymupdf,text-read |
| 有趣有料心理学 | text_crosscheck | raw_text_not_cross_confirmed | 3 | 0 | 0/0/3/3 | 0 | 23 | 0 terms / text-read |
| 设计师职业加速营 | text_crosscheck | raw_text_not_cross_confirmed | 74 | 0 | 1/0/3/3 | 0 | 29 | 0 terms / text-read |
| 设计转岗运营加速版 | text_crosscheck | raw_text_not_cross_confirmed | 44 | 0 | 0/0/3/2 | 0 | 29 | 0 terms / text-read |

## 关闭条件
- 不能用预览、dry-run、echo、上下文打包结果关闭。
- 每门课至少提供：原始源或本地来源索引、二次抽取文本重叠、视觉/关键帧或截图、OER/官方资料交叉、报告路径。
## 第十五批概念桥接结论
- 生成 `docs/course-concept-bridge-candidates-2026-07-08.md`。
- 剩余 8 门不再建议盲目 ASR；下一步是分类拆分或人工可复核概念映射。
- 当前仍不写正式 vault 正文，不把敏感/分类/不可转写项强行标完成。
