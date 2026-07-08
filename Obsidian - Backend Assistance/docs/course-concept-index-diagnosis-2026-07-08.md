# 剩余 8 门课程概念/分类页诊断（2026-07-08）

> 边界：helper repo 侧诊断；不修改正式 vault 正文；不把未核验内容标完成。

- 当前 verified: `31`
- 当前 needs_review: `8`
- risk_counts: `{'raw_text_not_cross_confirmed': 8, 'audio_video_asr_unusable': 1, 'missing_visual_evidence': 1}`

| 课程 | 诊断类型 | 风险 | overlap | sidecar | formal核心词 | sidecar核心词 | 下一步 |
|---|---|---|---:|---|---|---|---|
| Photoshop AIGC商业设计 | `no_text_extractable_core` | raw_text_not_cross_confirmed | 0 | 0/0/3/3 | 商业设计, aigc, photoshop, png, baidusyncdisk, 灵感库, 原创作品, 站酷 | 哈囉各位小伙伴大家好, 零技球, 越新過萬, 喜歡, 學艾體, 就來坑一馬程序員, 歡迎來到福德少伯家, 商業設計 | 现有源主要是视频/图片/素材，缺少可抽取正文；需要中段 ASR 或归档/课件清单。 |
| 传统文化与术数 | `category_index` | raw_text_not_cross_confirmed | 0 | 8/8/0/0 | 传统文化与术数, 文档资料, 课程库, 术数资料, priority, size_gb, 学习数据, next_action | 第一节, 第二节, 第三节, 癸亥, 辛酉, com, 己酉, www | 更像领域/分类索引：raw_matches 极大或覆盖多个子课程，单一 formal 页面不应按一门课闭环。 |
| 品牌全案AI设计实战班 | `media_unusable` | raw_text_not_cross_confirmed、audio_video_asr_unusable | 0 | 5/5/0/0 | 品牌全案, 设计实战班, jpg, 灵感库, 美式炸鸡汉堡品牌全案设计, aigc, baidusyncdisk, library | brand, coconut, design, tea, market, wine, also, health | .sz/视频源存在，但当前可转写片段无有效 ASR；PDF/素材证明视觉资产，不证明课程正文。 |
| 大脑训练 | `concept_mapping_needed` | raw_text_not_cross_confirmed | 0 | 1/1/0/0 | 大脑训练, pdf, 课程库, 模块总结, 用一个真实学习材料做, 分钟练习, 附件, 记录编码方式 | http, joinwell, kpengidc, sell | 已有 sidecar，但正式页词汇与源材料是不同层级表达，需要人工概念映射或子课程化。 |
| 敏感与待确认 | `sensitive_hold` | raw_text_not_cross_confirmed、missing_visual_evidence | 0 | 0/0/0/0 | 敏感与待确认, 课程库, 美女教你社会工程学系列教, priority, 混合资料, size_gb, 学习数据, next_action | - | 敏感/待确认内容不补操作性视觉和正文，只允许防护/伦理侧证据。 |
| 有趣有料心理学 | `no_text_extractable_core` | raw_text_not_cross_confirmed | 1 | 0/0/3/3 | 有趣有料心理学, 这个概念如何解释一个真实, 行为, 消费, 关系案例, 课程库, 模块总结, 应用问题 | 來定你自己, 年到, 這一次我們有講的主題是做, 我概念, 也就是我蠻如何理解自己和, 看待自己, 那這個主題呢, 他可以幫助我們去思考一些 | 现有源主要是视频/图片/素材，缺少可抽取正文；需要中段 ASR 或归档/课件清单。 |
| 设计师职业加速营 | `concept_mapping_needed` | raw_text_not_cross_confirmed | 0 | 1/0/3/3 | 设计师职业加速营, 附件, 行动, 结果, 课程库, 模块总结, 写一张职业复盘卡, 场景 | 大家好, 我是老型, 第二, 如何搞清楚领导的发展规划, http, 更多优质稀有资源请访问, 学习网, 或者 | 已有 sidecar，但正式页词汇与源材料是不同层级表达，需要人工概念映射或子课程化。 |
| 设计转岗运营加速版 | `no_text_extractable_core` | raw_text_not_cross_confirmed | 0 | 0/0/3/3 | 设计转岗运营加速版, 产出一个可放作品集, 面试的运营小项目证据, 附件, 课程库, 模块总结, type, status | 大家好, mobless, 本視頻是世紀周考運營課程, 的新黨課, 本課程是由人生家屬制度出, 聯合時思維再成大長總監共, 同之間內容, 幫你四周搞定世紀周考運營 | 现有源主要是视频/图片/素材，缺少可抽取正文；需要中段 ASR 或归档/课件清单。 |

## 类型统计
- `no_text_extractable_core`: 3
- `category_index`: 1
- `media_unusable`: 1
- `concept_mapping_needed`: 2
- `sensitive_hold`: 1

## 下一批策略
1. `category_index`：生成子资源映射清单，不按单页强行关闭。
2. `concept_mapping_needed`：生成 helper-sidecar 概念映射表，人工可复核后再决定是否放宽 audit。
3. `no_text_extractable_core`：继续找课件/归档清单或中段 ASR，不重复跑开头。
4. `media_unusable`：保留 unusable 状态，除非找到可正常转写的主体文件。
5. `sensitive_hold`：保持隔离。
