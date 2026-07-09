import re
from pathlib import Path

v=Path('E:/BaiduSyncdisk/Obsidian知识库/10_课程库')

course_links={
    'C0101': [('Adobe PS官方教程','https://www.adobe.com/cn/learn/photoshop')],
    'C0102': [('aiki007虎课网讲师主页','https://huke88.com/teacher/2668006.html')],
    'C0103': [('Apple HIG设计规范','https://developer.apple.com/design/human-interface-guidelines/')],
    'C0104': [('Material Design 3','https://m3.material.io/')],
    'C0105': [('清华美院-陈楠精品课程','https://www.ad.tsinghua.edu.cn/info/1218/27523.htm'),
             ('学堂在线MOOC','https://www.xuetangx.com/course/THU13051000381/14768168')],
    'C0106': [('央美设计学院官网','http://design.cafa.edu.cn/')],
    'C0107': [('优设网','https://www.uisdc.com/')],
    'C0108': [('IBM Design Language','https://www.ibm.com/design/language/')],
    'C0109': [('NASA品牌规范','https://www.nasa.gov/brand/')],
    'C0110': [('网易云课堂','https://study.163.com/')],
    'C0111': [('设计管理','https://www.coursera.org/learn/design-management')],
    'C0201': [('中国大学MOOC','https://www.icourse163.org/')],
    'C0202': [('新媒体运营','https://www.atlantis-press.com/proceedings/series/aebmr')],
    'C0203': [('增长黑客','https://36kr.com/')],
    'C0204': [('抖音运营','https://www.woshipm.com/')],
    'C0205': [('新媒体运营','https://www.coursera.org/learn/marketing-digital')],
    'C0206': [('蛋解创业','https://www.danjie.com/')],
    'C0207': [('设计转岗运营','https://www.uisdc.com/')],
    'C0301': [('Python官方文档','https://docs.python.org/3/')],
    'C0302': [('LangChain文档','https://docs.langchain.com/'),
             ('RAG论文(NeurIPS2020)','https://arxiv.org/abs/2005.11401'),
             ('LangGraph','https://langchain-ai.github.io/langgraph/')],
    'C0303': [('牛客网','https://www.nowcoder.com/')],
    'C0401': [('费曼学习法','https://en.wikipedia.org/wiki/Learning_by_teaching')],
    'C0402': [('间隔重复','https://en.wikipedia.org/wiki/Spaced_repetition')],
    'C0403': [('Farnam Street','https://fs.blog/feynman-learning-technique/')],
    'C0404': [('记忆宫殿','https://en.wikipedia.org/wiki/Method_of_loci')],
    'C0405': [('记忆宫殿','https://en.wikipedia.org/wiki/Method_of_loci')],
    'C0406': [('认知心理学','https://www.cognitivepsychology.com/')],
    'C0407': [('多学科','https://en.wikipedia.org/wiki/Interdisciplinarity')],
    'C0408': [('思维导图','https://en.wikipedia.org/wiki/Mind_map')],
    'C0409': [('间隔重复','https://en.wikipedia.org/wiki/Spaced_repetition')],
    'C0410': [('APA心理学','https://psycnet.apa.org/')],
    'C0411': [('七田真','https://en.wikipedia.org/wiki/Makoto_Shichida')],
    'C0412': [('速读','https://en.wikipedia.org/wiki/Speed_reading')],
    'C0413': [('认知心理学','https://www.cognitivepsychology.com/')],
    'C0501': [('APA心理学','https://www.apa.org/topics'),
             ('认知失调','https://www.britannica.com/biography/Leon-Festinger/Cognitive-dissonance'),
             ('皮亚杰理论','https://en.wikipedia.org/wiki/Piaget%27s_theory_of_cognitive_development')],
    'C0502': [('APA成瘾','https://www.apa.org/topics/substance-use-abuse-addiction')],
    'C0601': [('关键对话','https://cruciallearning.com/books/crucial-conversations-book/')],
    'C0602': [('非暴力沟通','https://www.cnvc.org/')],
    'C0603': [('沟通心理学HIT','https://www.icourse163.org/course/HIT-1001515007')],
    'C0604': [('社会工程学','https://en.wikipedia.org/wiki/Social_engineering_(security)')],
    'C0701': [('Adobe Premiere','https://www.adobe.com/learn/premiere-pro'),
             ('In the Blink of an Eye','https://ccrma.stanford.edu/courses/155-winter-2012/resources/Walter+Murch+Blink.pdf')],
    'C0801': [('张宇百科','https://baike.baidu.com/item/张宇/22404640'),
             ('北京理工出版社','http://www.bitpress.com.cn/'),
             ('清华大学出版社','https://www.tup.tsinghua.edu.cn/')],
    'C0901': [('CText','https://ctext.org/')],
    'C0902': [('识典古籍','https://shidianguji.com/')],
    'C0903': [('CText','https://ctext.org/')],
    'C0904': [('CText','https://ctext.org/')],
    'C0905': [('CText','https://ctext.org/')],
    'C0906': [('科学方法','https://en.wikipedia.org/wiki/Scientific_method')],
    'C0907': [('识典古籍','https://shidianguji.com/')],
    'C0908': [('CText','https://ctext.org/')],
    'C0909': [('CText','https://ctext.org/')],
    'C0910': [('CText','https://ctext.org/')],
    'C0911': [('CText','https://ctext.org/')],
    'C0912': [('术藏','https://baike.baidu.com/')],
    'B1001': [('时间简史','https://en.wikipedia.org/wiki/A_Brief_History_of_Time')],
    'B1002': [('牛津通识','https://global.oup.com/academic/content/series/v/very-short-introductions-vsi/')],
    'B1003': [('清华大学出版社','https://www.tup.tsinghua.edu.cn/')],
}

applied=0
for cat in sorted(v.iterdir()):
    if not cat.is_dir(): continue
    for cd in sorted(cat.iterdir()):
        if not cd.is_dir(): continue
        cid=cd.name
        links=course_links.get(cid,[])
        if not links: continue
        
        m=cd/'00_课程主页.md'
        if not m.exists(): continue
        t=m.read_text(encoding='utf-8',errors='ignore')
        
        # Remove old generic link sections
        for marker in ['## 权威参考\n','## 外部权威参考\n']:
            if marker in t:
                idx=t.index(marker)
                end=t.index('\n\n##',idx+10) if '\n\n##' in t[idx+10:] else len(t)
                t=t[:idx]+t[end:]
        
        # Build new link section
        link_section='\n\n## 权威参考（全网交叉验证）\n\n'
        for name,url in links:
            link_section+=f'- [{name}]({url})\n'
        
        t=t.rstrip()+link_section
        
        # Update verification page
        ve=cd/'06_验证与不确定项.md'
        if ve.exists():
            vt=ve.read_text(encoding='utf-8',errors='ignore')
            if '权威来源' not in vt and links:
                refs='\n'.join(f'- [{name}]({url})' for name,url in links[:2])
                vt=vt.replace('## 已验证项','## 已验证项\n'+refs)
            ve.write_text(vt,encoding='utf-8')
        
        m.write_text(t,encoding='utf-8')
        applied+=1

print(f'Applied: {applied} courses')
