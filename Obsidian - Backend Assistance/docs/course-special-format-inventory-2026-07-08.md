# 课程特殊格式与子课程拆分清点（2026-07-08）

> 边界：helper repo 侧清点报告；不写正式 vault 正文；不解压大体积归档到仓库。

## 工具探测
- `file`: available
- `7z`: available（可列 zip/rar，不全量解压）
- `antiword`: available（.doc 可抽文本）
- `libreoffice/catdoc/unrar`: unavailable
- `.sz`: `file` 识别为 ISO Media/MP4；ffprobe 可读流但有 NAL 警告，按视频源尝试 ASR/关键帧，失败则保留 unusable。

## 剩余 needs_review 源格式矩阵
| 课程 | 风险 | overlap | raw files | 特殊格式计数 | 样例特殊文件 | 下一步 |
|---|---|---:|---:|---|---|---|
| Photoshop AIGC商业设计 | raw_text_not_cross_confirmed | 0 | 99 | - | - | 重跑 sidecar：doc/docx 文本 + sz 视频尝试；归档只列清单 |
| 传统文化与术数 | raw_text_not_cross_confirmed | 2 | 74 | .doc:3 | E:\学习数据\07_传统文化与术数\文档资料\术数资料\术数资料\八字\八字基础.doc<br>E:\学习数据\07_传统文化与术数\文档资料\术数资料\术数资料\大六壬\六壬初学者的学习之路----------写给初学.doc<br>E:\学习数据\07_传统文化与术数\文档资料\术数资料\术数资料\大六壬\大六壬64课经精讲解注.doc | 分类页拆分；不按单一课程正文关闭 |
| 品牌全案AI设计实战班 | raw_text_not_cross_confirmed、audio_video_asr_unusable | 0 | 35 | .sz:27 | E:\学习数据\01_设计系统\文档资料\卢帅-2025年品牌全案·AI设计实战班【已完结】\01.第一章 往期直播分享回放\1.品牌设计师的作品集要怎么做更有竞争力？ .sz<br>E:\学习数据\01_设计系统\文档资料\卢帅-2025年品牌全案·AI设计实战班【已完结】\01.第一章 往期直播分享回放\2.品牌设计，如何进行商业变现？ .sz<br>E:\学习数据\01_设计系统\文档资料\卢帅-2025年品牌全案·AI设计实战班【已完结】\01.第一章 往期直播分享回放\3.燃计划宣讲：如何设计一份吸金的品牌策划案？ .sz<br>E:\学习数据\01_设计系统\文档资料\卢帅-2025年品牌全案·AI设计实战班【已完结】\01.第一章 往期直播分享回放\4.央美品牌课宣讲 .sz | .sz 已识别为视频容器；重跑品牌课 sz ASR/关键帧；zip/rar 只列素材清单 |
| 大脑训练 | raw_text_not_cross_confirmed | 0 | 5 | .doc:2 | E:\学习数据\04_心理记忆学习力\文档资料\大脑训练\全脑开发巨人\赠送\《超级记忆法》教材(完整版).doc<br>E:\学习数据\04_心理记忆学习力\文档资料\大脑训练\全脑开发巨人\赠送\本站资源免费下载指导教程.doc | 重跑 sidecar：doc/docx 文本 + sz 视频尝试；归档只列清单 |
| 敏感与待确认 | raw_text_not_cross_confirmed、missing_visual_evidence | 0 | 1 | - | - | 分类页拆分；不按单一课程正文关闭 |
| 新媒体运营与增长 | raw_text_not_cross_confirmed | 2 | 4369 | .docx:42, .xlsx:7 | E:\学习数据\03_新媒体运营与增长\音频课程\KEKE-李兴兴：剪辑实战训练营【已完结】\素材\12、10W元商单如何诞生：《无名之背》\03、分镜表\分镜头脚本《无名之“背”》剪辑版.xlsx<br>E:\学习数据\03_新媒体运营与增长\音频课程\KEKE-李兴兴：剪辑实战训练营【已完结】\素材\20、职业规划剪辑师面试应聘和接单技巧\【不知疲倦】应届生毕业求职个人简历.docx<br>E:\学习数据\03_新媒体运营与增长\音频课程\KEKE-李兴兴：剪辑实战训练营【已完结】\素材\20、职业规划剪辑师面试应聘和接单技巧\【冰花错落】热销个人总结.docx<br>E:\学习数据\03_新媒体运营与增长\音频课程\KEKE-李兴兴：剪辑实战训练营【已完结】\素材\20、职业规划剪辑师面试应聘和接单技巧\【姹紫嫣红敌不过你一回眸】个人应届生求职简历.docx | 分类页拆分；不按单一课程正文关闭 |
| 有趣有料心理学 | raw_text_not_cross_confirmed | 1 | 3 | - | - | 重跑 sidecar：doc/docx 文本 + sz 视频尝试；归档只列清单 |
| 牛客算法直通套餐 | raw_text_not_cross_confirmed | 2 | 164 | - | - | 重跑 sidecar：doc/docx 文本 + sz 视频尝试；归档只列清单 |
| 设计师职业加速营 | raw_text_not_cross_confirmed | 0 | 74 | - | - | 重跑 sidecar：doc/docx 文本 + sz 视频尝试；归档只列清单 |
| 设计转岗运营加速版 | raw_text_not_cross_confirmed | 0 | 44 | - | - | 重跑 sidecar：doc/docx 文本 + sz 视频尝试；归档只列清单 |

## 处理规则
- `.doc`: antiword 抽文本后可进入 text sidecar。
- `.docx`: 通过 OOXML `word/document.xml` 直接抽文本。
- `.sz`: 作为视频容器尝试 ffmpeg/ASR；如转写失败，标记 `audio_video_asr_unusable`。
- `.rar/.zip`: 只用 7z 列清单/素材存在，不全量解压到仓库。
- `.ape`: 作为音频存在证据；是否转写需单独小样本抽取。
