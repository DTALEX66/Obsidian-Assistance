# 课程完整性补全计划（2026-07-08）

## 当前状态

| 维度 | 覆盖率 |
|---|---|
| Markdown 文件 | 39/39 ✅ |
| Frontmatter | 39/39 ✅ |
| 双链 (wikilinks) | 39/39 ✅ |
| 图片嵌入 | 29/39 ⚠️ |
| 附件目录 | 23/39 ⚠️ |
| OER/交叉比对 | 30/39 ⚠️ |
| 外部链接 | 12/39 ❌ |
| Dataview 查询 | 29/39 |

## 分类处理

### A. 分类索引页（8 门）— 无需补全图片/交叉比对

这些是领域导航页，不是单一课程：

```
传统文化与术数、心理记忆学习力、新媒体运营与增长、
生活策略与沟通、编程系统与AI开发、考试数学与学习方法、
设计系统、阅读资料库
```

→ 保持现状；它们的功能是 dataview 聚合和索引。

### B. 敏感内容（1 门）

```
敏感与待确认
```

→ 不补任何内容。

### C. 真实课程缺外部链接（19 门）— 需要补 OER/网络交叉引用

| 课程 | 已有 OER sidecar | 网络来源 |
|---|---|---|
| 30天考霸训练营 | ✅ | 学习科学/spaced repetition 文献 |
| Photoshop AIGC商业设计 | ✅ | Adobe Firefly 官方文档 |
| UI系统全能班 | ✅ | Apple HIG / Material Design 3 |
| 中央美院美术基础教学 | ✅ | Smarthistory / CAFA 官网 |
| 全栈新媒体运营 | ✅ | HubSpot Academy / Content Marketing Institute |
| 品牌全案AI设计实战班 | ✅ | AIGC 品牌设计学术论文 |
| 大模型应用开发介绍 | ✅ | OpenAI / LangChain 文档 |
| 大脑训练 | ✅ | Art of Memory / 间隔重复研究 |
| 思维导图与记忆宫殿教程 | ✅ | Tony Buzan 官方 / 认知科学 |
| 新媒体高阶运营增长实战训练 | ✅ | Smart Insights / GrowthHackers |
| 有趣有料心理学 | ✅ | Yale PSYC 110 / Coursera |
| 海马记忆法与记忆宫殿 | ✅ | Memory Palace 研究 |
| 清华视觉传达设计思维与方法 | ✅ | 清华美院课程页 |
| 版式设计 | ✅ | Typography 教材 |
| 牛客算法直通套餐 | ✅ | LeetCode / cp-algorithms |
| 网易视觉设计师养成计划 | ✅ | 网易 UEDC 设计规范 |
| 设计师职业加速营 | ✅ | Stanford Designing Your Career |
| 设计转岗运营加速版 | ✅ | Marketing KPI 行业标准 |

### D. 缺图片/附件（非分类页，9 门中的 1 门）

```
敏感与待确认 — 保持隔离
```

其余 8 门都是 A 类分类页。

## 处理建议

对于 19 门缺外部链接的真实课程：**直接从已有 OER sidecar 中提取链接，添加到课程页面的交叉比对区块。** 这是非正文补充，不涉及课程内容改写。

**操作边界：只添加 `## 外部交叉参考` 区块到课程页末尾，不改写正文。**
