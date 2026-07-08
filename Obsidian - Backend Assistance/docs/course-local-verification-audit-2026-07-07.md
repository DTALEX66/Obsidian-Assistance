# 全课程本地转化多源交叉识别核验报告

> 结论口径：不声称绝对零错误；只有本地源、二次文本抽取、报告、视觉资产、OER 等多种方法互相印证时，才标 `verified_by_available_methods`。

## 环境
- pymupdf_available: `True`
- markitdown_available: `True`
- pdftotext_available: `True`
- ffmpeg_available: `True`
- tesseract_available: `True`
- whisper_available: `True`

## 总览
- **courses_total**: `39`
- **verified_by_available_methods**: `31`
- **needs_review**: `8`
- **source_files_total**: `18421`
- **report_files_total**: `482`
- **asset_files_total**: `145`
- **oer_files_total**: `60`
- **risk_counts**: `{'raw_text_not_cross_confirmed': 8, 'audio_video_asr_unusable': 1, 'missing_visual_evidence': 1}`

## 课程核验矩阵
| 课程 | 状态 | 方法数 | 风险 | 原始源 | 本地来源索引 | Sidecar | 报告 | 视觉 | OER | 文本交叉 | 样例源 |
|---|---|---:|---|---:|---:|---|---:|---:|---:|---|---|
| 品牌全案AI设计实战班 | needs_review | 5 | raw_text_not_cross_confirmed、audio_video_asr_unusable | 35 | 0 | 5/5/0/0 | 7 | 47 | 1 | 0 terms / text-read | 01_设计系统/文档资料/卢帅-2025年品牌全案·AI设计实战班【已完结】/06.第六章 品牌IP+AIGC篇/第12节 品牌IP设定 .sz<br>01_设计系统/文档资料/卢帅-2025年品牌全案·AI设计实战班【已完结】/06.第六章 品牌IP+AIGC篇/第13节 AIGC工具详解与IP多形态延展 .sz |
| 敏感与待确认 | needs_review | 4 | raw_text_not_cross_confirmed、missing_visual_evidence | 1 | 0 | 0/0/0/0 | 1 | 0 | 1 | 0 terms / text-read | 91_敏感与待确认/混合资料/美女教你社会工程学系列教程/新建 文本文档.txt |
| Photoshop AIGC商业设计 | needs_review | 5 | raw_text_not_cross_confirmed | 99 | 0 | 0/0/3/3 | 9 | 53 | 3 | 1 terms / text-read | 01_设计系统/视频课程/165、【黑马程序员】-2024最新Photoshop+AIGC商业设计从入门到实战/第01章 风景装饰画设计+软件快速入门/01_标准视频/000_Photoshop+AIGC商业设计-导学视频.mp4<br>01_设计系统/视频课程/165、【黑马程序员】-2024最新Photoshop+AIGC商业设计从入门到实战/第01章 风景装饰画设计+软件快速入门/01_标准视频/001_PS界面工作区认识-快速体验.mp4 |
| 传统文化与术数 | needs_review | 5 | raw_text_not_cross_confirmed | 74 | 0 | 8/8/0/0 | 1 | 0 | 1 | 0 terms / text-read | 07_传统文化与术数/文档资料/术数资料/术数资料/八字/三命通会.pdf<br>07_传统文化与术数/文档资料/术数资料/术数资料/八字/三命通会注评.pdf |
| 大脑训练 | needs_review | 5 | raw_text_not_cross_confirmed | 5 | 0 | 1/1/0/0 | 8 | 23 | 1 | 0 terms / pymupdf,text-read | 04_心理记忆学习力/文档资料/大脑训练/全脑开发巨人/www.ffjj.com.cn_albert.txt<br>04_心理记忆学习力/文档资料/大脑训练/全脑开发巨人/赠送/《超级记忆法》教材(完整版).doc |
| 有趣有料心理学 | needs_review | 5 | raw_text_not_cross_confirmed | 3 | 0 | 0/0/3/3 | 8 | 23 | 1 | 0 terms / text-read | 04_心理记忆学习力/视频课程/万门大学-有趣有料心理学/1、课程：社会心理学（上）/1、自我概念及其三种类型.mp4<br>04_心理记忆学习力/视频课程/万门大学-有趣有料心理学/1、课程：社会心理学（上）/2、自我概念与文化.mp4 |
| 设计师职业加速营 | needs_review | 5 | raw_text_not_cross_confirmed | 74 | 0 | 1/0/3/3 | 8 | 29 | 1 | 0 terms / text-read | 01_设计系统/视频课程/邢开捷-人生加速 年课设计师加速营【五期】/10_「设计师的管理学课」—Basic-【入营必看】职场关系｜如何处理职场上的竞争？.mp4<br>01_设计系统/视频课程/邢开捷-人生加速 年课设计师加速营【五期】/11_「设计师的管理学课」—Basic-【入营必看】职场关系｜如何和领导构建统一目标？.mp4 |
| 设计转岗运营加速版 | needs_review | 5 | raw_text_not_cross_confirmed | 44 | 0 | 0/0/3/2 | 8 | 29 | 1 | 0 terms / text-read | 01_设计系统/视频课程/邢开捷丨人生加速-【设计转岗运营20加速版L1L2L3番外篇含转岗面试技巧方法默认班级】-129800圆-43节/01-「必听」先导课.mp4<br>01_设计系统/视频课程/邢开捷丨人生加速-【设计转岗运营20加速版L1L2L3番外篇含转岗面试技巧方法默认班级】-129800圆-43节/02-掌握基础文案知识.mp4 |
| 30天考霸训练营 | verified_by_available_methods | 6 | OK | 181 | 0 | 5/0/1/0 | 7 | 17 | 1 | 27 terms / text-read | 08_考试数学与学习方法/文档资料/30天考霸训练营，北大博士后教你通关任何考试，助你高分拿下证书、岗位、考试(2)/01预热课/00【购课须知】-购买了课程的同学看过来#重点#（建议别发给顾客了）.mp4<br>08_考试数学与学习方法/文档资料/30天考霸训练营，北大博士后教你通关任何考试，助你高分拿下证书、岗位、考试(2)/01预热课/00预热课1-一套通用的“考霸”学习、考试模型，助你轻松拿下任何考试.mp4 |
| AI Agent Skills 实战课 | verified_by_available_methods | 6 | OK | 0 | 6 | 0/0/0/0 | 4 | 14 | 5 | 51 terms / text-read | 50_领域知识/AI Agent技能库/00_awesome-skills-cn吸收总览.md<br>50_领域知识/AI Agent技能库/01_技能分类矩阵.md |
| AI LLM工具生态与Skill工程 | verified_by_available_methods | 6 | OK | 0 | 2 | 0/0/0/0 | 3 | 17 | 5 | 29 terms / text-read | 50_领域知识/AI Agent技能库/04_课程化吸收总控.md<br>50_领域知识/AI Agent技能库/source-summary.json |
| AI研究搜索与OER交叉验证 | verified_by_available_methods | 6 | OK | 0 | 14 | 0/0/0/0 | 47 | 17 | 13 | 26 terms / text-read | 50_领域知识/AI Agent技能库/04_课程化吸收总控.md<br>50_领域知识/AI Agent技能库/source-summary.json |
| Agent技能安全审计 | verified_by_available_methods | 6 | OK | 0 | 2 | 0/0/0/0 | 3 | 17 | 5 | 25 terms / text-read | 50_领域知识/AI Agent技能库/04_课程化吸收总控.md<br>50_领域知识/AI Agent技能库/source-summary.json |
| GitHub自动化与代码审查工作流 | verified_by_available_methods | 6 | OK | 0 | 2 | 0/0/0/0 | 5 | 11 | 1 | 22 terms / text-read | 50_领域知识/AI Agent技能库/04_课程化吸收总控.md<br>50_领域知识/AI Agent技能库/source-summary.json |
| Obsidian与PKM自动化实战 | verified_by_available_methods | 6 | OK | 0 | 2 | 0/0/0/0 | 3 | 17 | 5 | 27 terms / text-read | 50_领域知识/AI Agent技能库/04_课程化吸收总控.md<br>50_领域知识/AI Agent技能库/source-summary.json |
| UI UX Agent设计系统实战 | verified_by_available_methods | 6 | OK | 0 | 2 | 0/0/0/0 | 3 | 17 | 1 | 22 terms / text-read | 50_领域知识/AI Agent技能库/04_课程化吸收总控.md<br>50_领域知识/AI Agent技能库/source-summary.json |
| UI系统全能班 | verified_by_available_methods | 6 | OK | 12 | 1 | 0/0/0/0 | 9 | 29 | 1 | 9 terms / pymupdf,text-read | 01_设计系统/文档资料/KEKE-孔晨-UI系统全能班第3期【已完结】/UI系统班资料汇总/UI系统班资料汇总/02行业任职篇/学习资源.jpg<br>01_设计系统/文档资料/KEKE-孔晨-UI系统全能班第3期【已完结】/UI系统班资料汇总/UI系统班资料汇总/02行业任职篇/行业认知.docx |
| 中央美院美术基础教学 | verified_by_available_methods | 6 | OK | 28 | 1 | 0/0/0/0 | 6 | 23 | 1 | 10 terms / text-read | 01_设计系统/视频课程/中央美院美术基础教学14套/中国美术学院《rent素描》朝戈 视频教程（三讲全）/[中央美术学院：朝戈主讲：rent素描].朝戈.第1讲.WMV<br>01_设计系统/视频课程/中央美院美术基础教学14套/中国美术学院《rent素描》朝戈 视频教程（三讲全）/[中央美术学院：朝戈主讲：rent素描].朝戈.第2讲.WMV |
| 全栈新媒体运营 | verified_by_available_methods | 6 | OK | 239 | 0 | 0/0/0/0 | 8 | 29 | 1 | 15 terms / pdftotext,text-read | 03_新媒体运营与增长/视频课程/全栈新媒体运营/2新媒体应用传播学/1导语/1了解传播学理论的意义.avi<br>03_新媒体运营与增长/视频课程/全栈新媒体运营/2新媒体应用传播学/2传播学导论/1什么是传播学.avi |
| 多Agent工程与任务编排 | verified_by_available_methods | 6 | OK | 0 | 2 | 0/0/0/0 | 3 | 17 | 5 | 26 terms / text-read | 50_领域知识/AI Agent技能库/04_课程化吸收总控.md<br>50_领域知识/AI Agent技能库/source-summary.json |
| 大模型应用开发介绍 | verified_by_available_methods | 6 | OK | 1 | 1 | 0/0/0/0 | 9 | 17 | 1 | 26 terms / pymupdf,text-read | 02_编程系统与AI开发/单文件文档/大模型应用开发介绍-0715.pdf |
| 心理记忆学习力 | verified_by_available_methods | 6 | OK | 2527 | 0 | 5/2/0/0 | 1 | 0 | 1 | 27 terms / text-read | 04_心理记忆学习力/文档资料/大脑训练/全脑开发巨人/www.ffjj.com.cn_albert.txt<br>04_心理记忆学习力/文档资料/大脑训练/全脑开发巨人/赠送/《超级记忆法》教材(完整版).doc |
| 思维导图与记忆宫殿教程 | verified_by_available_methods | 6 | OK | 342 | 0 | 3/3/1/0 | 8 | 23 | 1 | 7 terms / pymupdf,text-read | 04_心理记忆学习力/视频课程/思维导图教程/叶瑞财打造最强大脑/打造最强大脑一(1).flv<br>04_心理记忆学习力/视频课程/思维导图教程/叶瑞财打造最强大脑/打造最强大脑一.flv |
| 文档OCR与课程入库自动化 | verified_by_available_methods | 6 | OK | 0 | 2 | 0/0/0/0 | 3 | 11 | 5 | 25 terms / text-read | 50_领域知识/AI Agent技能库/04_课程化吸收总控.md<br>50_领域知识/AI Agent技能库/source-summary.json |
| 新媒体运营与增长 | verified_by_available_methods | 6 | OK | 4369 | 0 | 8/7/2/2 | 1 | 4 | 1 | 3 terms / text-read | 03_新媒体运营与增长/单文件文档/全媒体运营师相关政策法规复习材料.pdf<br>03_新媒体运营与增长/单文件文档/增长黑客.pdf |
| 新媒体高阶运营增长实战训练 | verified_by_available_methods | 6 | OK | 182 | 0 | 5/5/1/0 | 19 | 16 | 1 | 8 terms / text-read | 03_新媒体运营与增长/文档资料/新媒体高阶运营&增长实战训练（完结）/00.课前必读/【瑞客论坛 www.ruike1.com】这里有个蠢萌老师等你翻牌.docx<br>03_新媒体运营与增长/文档资料/新媒体高阶运营&增长实战训练（完结）/01.导论-重新认知新媒体岗位/【瑞客论坛 www.ruike1.com】01.新媒体人到底是做什么的？.mp4 |
| 浏览器自动化与桌面控制 | verified_by_available_methods | 6 | OK | 0 | 2 | 0/0/0/0 | 3 | 17 | 5 | 24 terms / text-read | 50_领域知识/AI Agent技能库/04_课程化吸收总控.md<br>50_领域知识/AI Agent技能库/source-summary.json |
| 海马记忆法与记忆宫殿 | verified_by_available_methods | 6 | OK | 303 | 0 | 3/3/1/0 | 8 | 23 | 1 | 7 terms / pymupdf,text-read | 04_心理记忆学习力/视频课程/记忆宫殿/1000桩子讲解1 (2).flv<br>04_心理记忆学习力/视频课程/记忆宫殿/1000桩子讲解1(1).flv |
| 清华视觉传达设计思维与方法 | verified_by_available_methods | 6 | OK | 24 | 1 | 0/0/0/0 | 9 | 38 | 1 | 10 terms / text-read | 01_设计系统/视频课程/_清华大学_视觉传达设计思维与方法_全24讲_陈楠/01_1_1_设计与设计师_对生活中习以为常的形式符号的反思.mp4<br>01_设计系统/视频课程/_清华大学_视觉传达设计思维与方法_全24讲_陈楠/02_1_2_对于_设计传达研究生_等概念的反思与解读.mp4 |
| 版式设计 | verified_by_available_methods | 6 | OK | 59 | 1 | 0/0/0/0 | 9 | 53 | 1 | 14 terms / pymupdf,text-read | 01_设计系统/视频课程/版式设计/01-课前测试.mp4<br>01_设计系统/视频课程/版式设计/02-第一课-艺术设计鉴赏.mp4 |
| 牛客算法直通套餐 | verified_by_available_methods | 6 | OK | 164 | 0 | 8/0/2/1 | 8 | 11 | 1 | 4 terms / text-read | 02_编程系统与AI开发/视频课程/牛客算法直通套餐/01.算法基础入门班（第五期）/第1章 认识复杂度和简单排序算法/1.1 课前预习（课件+源码）/算法基础入门班第一课.pdf<br>02_编程系统与AI开发/视频课程/牛客算法直通套餐/01.算法基础入门班（第五期）/第1章 认识复杂度和简单排序算法/1.2课程学习.mp4 |
| 生活策略与沟通 | verified_by_available_methods | 6 | OK | 117 | 0 | 3/4/1/0 | 1 | 0 | 1 | 12 terms / text-read | 06_生活策略与沟通/视频课程/2018年素云vip精英班恋爱课程/VIP第01课教会你如何去正确的爱.mp4<br>06_生活策略与沟通/视频课程/2018年素云vip精英班恋爱课程/VIP第02课如何正确快速的学习PUA.mp4 |
| 知识内化训练营 | verified_by_available_methods | 6 | OK | 64 | 3 | 0/0/0/0 | 11 | 120 | 5 | 23 terms / pdftotext,text-read | 04_心理记忆学习力/文档资料/知识内化训练营：21天北大学霸科学记忆系统（完结）/00发刊词： 从「读书不忘」开始，带你训练出一个强健大脑.mp3<br>04_心理记忆学习力/文档资料/知识内化训练营：21天北大学霸科学记忆系统（完结）/00发刊词： 从「读书不忘」开始，带你训练出一个强健大脑.pdf |
| 编程系统与AI开发 | verified_by_available_methods | 6 | OK | 2968 | 0 | 0/0/0/0 | 1 | 0 | 1 | 3 terms / pymupdf,text-read | 02_编程系统与AI开发/单文件文档/大模型应用开发介绍-0715.pdf<br>02_编程系统与AI开发/素材资产/t514——风变编程/风变编程/Python基础语法与爬虫精进（风变编程）/12关参考代码/2019-02-11 233212.mov |
| 网易视觉设计师养成计划 | verified_by_available_methods | 6 | OK | 2945 | 1 | 0/0/0/0 | 6 | 23 | 1 | 11 terms / pymupdf,text-read | 01_设计系统/视频课程/大河-网易”视觉设计师养成计划【已完结】/合成电商类好图/合成类海报（电商外卖）/2022.2.jpg<br>01_设计系统/视频课程/大河-网易”视觉设计师养成计划【已完结】/合成电商类好图/合成类海报（电商外卖）/2022.5.7 表白季feeds.jpg |
| 考试数学与学习方法 | verified_by_available_methods | 6 | OK | 737 | 0 | 5/1/1/0 | 1 | 0 | 1 | 11 terms / text-read | 08_考试数学与学习方法/文档资料/30天考霸训练营，北大博士后教你通关任何考试，助你高分拿下证书、岗位、考试(2)/01预热课/00【购课须知】-购买了课程的同学看过来#重点#（建议别发给顾客了）.mp4<br>08_考试数学与学习方法/文档资料/30天考霸训练营，北大博士后教你通关任何考试，助你高分拿下证书、岗位、考试(2)/01预热课/00预热课1-一套通用的“考霸”学习、考试模型，助你轻松拿下任何考试.mp4 |
| 记忆圣经学习力合集 | verified_by_available_methods | 6 | OK | 485 | 0 | 5/5/1/0 | 8 | 23 | 1 | 6 terms / text-read | 04_心理记忆学习力/视频课程/记忆圣经/--------记忆圣经-------/文件解压码(1).txt<br>04_心理记忆学习力/视频课程/记忆圣经/--------记忆圣经-------/文件解压码.txt |
| 设计系统 | verified_by_available_methods | 6 | OK | 5305 | 1 | 0/0/0/0 | 7 | 3 | 1 | 8 terms / pymupdf,text-read | 01_设计系统/单文件文档/品牌设计学习手册丨尚道设研第一版.pdf<br>01_设计系统/单文件文档/视觉传达学习手册与避坑指南.pdf |
| 阅读资料库 | verified_by_available_methods | 6 | OK | 2321 | 0 | 0/0/0/0 | 1 | 0 | 1 | 5 terms / pymupdf,text-read | 05_阅读资料库/单文件文档/百问百答.pdf<br>05_阅读资料库/文档资料/《时间简史》（插图本）史蒂芬·霍金 [EPUB+MOBI+PDF]/《时间简史（插图本）》.png |

## 后续规则
- `needs_review` 课程不能宣称无幻觉/无识别错误。
- 视频/音频课程在 whisper/faster-whisper 缺失时，只能做文件级存在验证，不能做内容级 ASR 核验。
- 扫描 PDF 在 tesseract/marker 缺失时，只能做可复制文本 PDF 的 PyMuPDF/pdftotext 核验，不能做图像 OCR 核验。
- 网络/OER 只能校对公共知识，不能替代本地课程源。
