#!/usr/bin/env python3
"""Add external cross-reference links to courses missing them."""
import json, re, sys
from pathlib import Path

vault=Path('E:/BaiduSyncdisk/Obsidian知识库/02_课程库')
oer_dir=Path('Obsidian - Backend Assistance/docs/course-oer-sidecars')

# OER links from existing sidecars
oer_links={}
for f in sorted(oer_dir.glob('*.md')):
    text=f.read_text(encoding='utf-8')[:3000]
    urls=re.findall(r'(https?://[^\s)\]]+)', text)
    oer_links[f.stem]=urls

oer_to_course={
    '30天考霸训练营':'30天考霸训练营', 'Photoshop_AIGC商业设计':'Photoshop AIGC商业设计',
    'UI_UX_Agent设计系统实战':'UI系统全能班', '中央美院美术基础教学':'中央美院美术基础教学',
    '全栈新媒体运营':'全栈新媒体运营', '品牌全案AI设计实战班':'品牌全案AI设计实战班',
    '大模型应用开发介绍':'大模型应用开发介绍', '大脑训练':'大脑训练',
    '思维导图与记忆宫殿教程':'思维导图与记忆宫殿教程',
    '新媒体运营与增长':'新媒体高阶运营增长实战训练','新媒体高阶运营增长实战训练':'新媒体高阶运营增长实战训练',
    '有趣有料心理学':'有趣有料心理学', '海马记忆法与记忆宫殿':'海马记忆法与记忆宫殿',
    '清华视觉传达设计思维与方法':'清华视觉传达设计思维与方法', '版式设计':'版式设计',
    '牛客算法直通套餐':'牛客算法直通套餐', '网易视觉设计师养成计划':'网易视觉设计师养成计划',
    '设计师职业加速营':'设计师职业加速营', '设计转岗运营加速版':'设计转岗运营加速版',
}

web_extra={
    '30天考霸训练营': ['- [Spaced Repetition Research](https://www.gwern.net/Spaced-repetition) — 间隔重复学术研究'],
    'Photoshop AIGC商业设计': ['- [Adobe Firefly](https://experienceleague.adobe.com/en/docs/creative-cloud-enterprise-learn/cce-learning-hub/fireflyoverview/overview-firefly) — 官方 AI 工具文档','- [Photoshop Generative Fill](https://www.adobe.com/learn/photoshop/web/discover-generative-fill) — 官方教程'],
    'UI系统全能班': ['- [Apple HIG](https://developer.apple.com/design/human-interface-guidelines/)','- [Material Design 3](https://m3.material.io/)'],
    '全栈新媒体运营': ['- [HubSpot Academy](https://academy.hubspot.com/)','- [Content Marketing Institute](https://contentmarketinginstitute.com/)'],
    '品牌全案AI设计实战班': ['- [AIGC Brand Visual Communication](https://www.sciencedirect.com/science/article/pii/S187705092402862X)','- [The Brand Identity](https://the-brandidentity.com/features)'],
    '大脑训练': ['- [Art of Memory](https://artofmemory.com/blog/how-to-build-a-memory-palace/)','- [Coursera: Memory Palace](https://www.coursera.org/articles/memory-palace)'],
    '海马记忆法与记忆宫殿': ['- [Art of Memory](https://artofmemory.com/)','- [Memory Palace Research](https://files.eric.ed.gov/fulltext/ED626951.pdf)'],
    '版式设计': ['- [Thinking with Type](http://thinkingwithtype.com/)','- [Google Fonts Knowledge](https://fonts.google.com/knowledge)'],
    '牛客算法直通套餐': ['- [cp-algorithms](https://cp-algorithms.com/)','- [LeetCode](https://leetcode.com/problemset/)'],
    '有趣有料心理学': ['- [Yale PSYC 110](https://oyc.yale.edu/introduction-psychology/psyc-110)','- [Coursera Psychology](https://www.coursera.org/learn/introduction-psychology)'],
    '设计师职业加速营': ['- [Stanford Designing Your Career](https://online.stanford.edu/courses/tds-y0003-designing-your-career)','- [Harvard Resume Guide](https://careerservices.fas.harvard.edu/resources/create-a-strong-resume/)'],
    '设计转岗运营加速版': ['- [Smart Insights KPIs](https://www.smartinsights.com/goal-setting-evaluation/goals-kpis/choosing-effective-digital-marketing-kpis/)','- [Marketing Metrics](https://www.indeed.com/career-advice/career-development/marketing-metrics-and-kpis)'],
    '新媒体高阶运营增长实战训练': ['- [GrowthHackers](https://growthhackers.com/)','- [Smart Insights](https://www.smartinsights.com/)'],
    '清华视觉传达设计思维与方法': ['- [清华美院](https://www.ad.tsinghua.edu.cn/)'],
    '网易视觉设计师养成计划': ['- [网易 UEDC](https://uedc.netease.com/)'],
    '中央美院美术基础教学': ['- [Smarthistory](https://smarthistory.org/)','- [CAFA](https://www.cafa.edu.cn/)'],
    '大模型应用开发介绍': ['- [LangChain](https://python.langchain.com/)','- [OpenAI API](https://platform.openai.com/docs)'],
}

category_pages={'传统文化与术数','心理记忆学习力','新媒体运营与增长','生活策略与沟通',
                '编程系统与AI开发','考试数学与学习方法','设计系统','阅读资料库','敏感与待确认'}

modified=0
for course_dir in sorted(vault.iterdir()):
    if not course_dir.is_dir(): continue
    course=course_dir.name
    if course in category_pages: continue
    
    main=course_dir/'00_课程总览.md'
    if not main.exists():
        mains=sorted(course_dir.glob('*.md'))
        if not mains: continue
        main=mains[0]
    
    text=main.read_text(encoding='utf-8')
    if re.search(r'(#+\s*(外部|交叉|比对|参考|来源|O[Ee][Rr]))', text): continue
    
    lines=['','---','','## 外部交叉参考','','> 以下为公开网络权威来源，用于课程公共知识的交叉验证。','']
    for oer_name, cname in oer_to_course.items():
        if cname==course and oer_name in oer_links:
            for u in oer_links[oer_name][:3]:
                lines.append(f'- <{u}>')
            break
    for e in web_extra.get(course,[]): lines.append(e)
    if len(lines)<=7: continue
    
    main.write_text(text.rstrip()+'\n'+'\n'.join(lines)+'\n', encoding='utf-8')
    modified+=1
    print(f'  [OK] {course}')

print(f'\nDone: {modified} courses updated')
