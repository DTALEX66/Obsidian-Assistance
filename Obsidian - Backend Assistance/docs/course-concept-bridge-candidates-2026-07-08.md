# 剩余课程概念桥接与保留原因（2026-07-08）

> helper repo 侧候选映射；不自动放宽 audit，不修改正式 vault。只有人工复核或脚本可解释匹配通过后才可关闭。

- verified_by_available_methods: `31`
- needs_review: `8`
- risk_counts: `{'raw_text_not_cross_confirmed': 8, 'audio_video_asr_unusable': 1, 'missing_visual_evidence': 1}`

| 课程 | 当前状态 | formal 术语 | sidecar/ASR 术语 | 候选桥接 | 保留/下一步 |
|---|---|---|---|---|---|
| Photoshop AIGC商业设计 | raw_text_not_cross_confirmed | 商业设计, aigc, photoshop, png, baidusyncdisk, 灵感库, 原创作品, 站酷, library, images | 对不对, 属性, 你会发现, 我们担击它, 是不是, 再到这, 這次我要忘記把完成到課程, 作業上傳到評論區, 讓大家的優秀彼此被看到, 同時我們也會不定期的安排 | 商业设计 ⇄ 商業設計/黑马程序员/Photoshop; AIGC ⇄ AI/生成/绘图/商業設計; 海报文案创意排版 ⇄ 海报/文案/排版/案例 | 需要人工确认桥接词是否成立，或实现可解释 ngram/同义词匹配后重跑。 |
| 传统文化与术数 | raw_text_not_cross_confirmed | 传统文化与术数, 文档资料, 课程库, 术数资料, priority, size_gb, 学习数据, next_action, type, status | 第一节, 第二节, 第三节, 癸亥, 辛酉, com, www, 滴天髓, 己酉, 第四节 | 分类索引 ⇄ 八字/大六壬/术数资料/子资源; 传统文化 ⇄ 古籍/术数/五行 | 拆成子资源/子课程核验；父级分类页不按单门课程关闭。 |
| 品牌全案AI设计实战班 | raw_text_not_cross_confirmed、audio_video_asr_unusable | 品牌全案, 设计实战班, jpg, 灵感库, 美式炸鸡汉堡品牌全案设计, aigc, baidusyncdisk, library, images, info | brand, coconut, design, tea, market, wine, also, health, sweet, jasmine | 品牌全案 ⇄ brand/design/VI/视觉识别; AIGC辅助 ⇄ AIGC/IP/三维效果图; 品牌策略 ⇄ 市场/品牌/提案 | 保留 unusable；继续找可转写主体或只认视觉/素材存在，不认正文一致。 |
| 大脑训练 | raw_text_not_cross_confirmed | 大脑训练, pdf, 课程库, 模块总结, 用一个真实学习材料做, 分钟练习, 附件, 记录编码方式, 回忆正确率和下次改进, type | http, joinwell, kpengidc, sell | 编码方式/记忆练习 ⇄ 超级记忆法/全脑训练/潜意识; 练习记录 ⇄ 教材/训练/音频 | 需要人工确认桥接词是否成立，或实现可解释 ngram/同义词匹配后重跑。 |
| 敏感与待确认 | raw_text_not_cross_confirmed、missing_visual_evidence | 敏感与待确认, 课程库, 美女教你社会工程学系列教, priority, 混合资料, size_gb, 学习数据, next_action, type, status | - | 保留原因 ⇄ 敏感内容隔离/只允许防护伦理侧证据 | 安全保留：不补操作性正文/视觉；仅可做防护、伦理、风险提示侧证据。 |
| 有趣有料心理学 | raw_text_not_cross_confirmed | 有趣有料心理学, 这个概念如何解释一个真实, 行为, 消费, 关系案例, 课程库, 模块总结, 应用问题, 附件, type | 大家注意, 在中学阶段, 很多学一些学生可能家长, 或是会, 以及老师, 会跟他们讲, 只用你考上大学, 就好了, 那这个时候, 他中学阶段的理想 | 行为/消费/关系案例 ⇄ 理解自己/看待自己/主题讨论; 心理学概念应用 ⇄ 自我/关系/思考 | 需要人工确认桥接词是否成立，或实现可解释 ngram/同义词匹配后重跑。 |
| 设计师职业加速营 | raw_text_not_cross_confirmed | 设计师职业加速营, 附件, 行动, 结果, 课程库, 模块总结, 写一张职业复盘卡, 场景, 问题, 下次改进 | 大家好, 我是老型, 第二, 如何搞清楚领导的发展规划, http, 更多优质稀有资源请访问, 学习网, 或者, 欢迎来到车机师的观点学客, 前击讲我们分别讲了 | 职业复盘卡 ⇄ 领导/发展规划/职场; 结构化表达 ⇄ 沟通/职场/领导 | 需要人工确认桥接词是否成立，或实现可解释 ngram/同义词匹配后重跑。 |
| 设计转岗运营加速版 | raw_text_not_cross_confirmed | 设计转岗运营加速版, 产出一个可放作品集, 面试的运营小项目证据, 附件, 课程库, 模块总结, type, status, 输出练习, 流程 | 产品内部云音乐员, 像现在我们在屏幕上看到的, 显纳批评的介面, 标红的局部主题叫做新鲳积, 下面分别叫说迪数码, 保证社品等, 点净者是一些特定商品做成, 了这题业, 云统绝把产品内部的商品和, 内容机简二字组织 | 运营小项目证据 ⇄ 课程/运营/四周搞定/转岗; 面试作品集 ⇄ 作品集/运营案例/项目 | 需要人工确认桥接词是否成立，或实现可解释 ngram/同义词匹配后重跑。 |

## 本批结论
- 中段 ASR 已证明“继续机械转写”对剩余 8 门收益很低。
- 可关闭路径只剩两类：①拆分分类/父级索引；②把候选桥接做成人工可复核的概念映射规则。
- 敏感项必须保持隔离，不应为了清零而扩写。
