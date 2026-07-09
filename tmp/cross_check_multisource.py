import re
from pathlib import Path
from collections import Counter

vault=Path('E:/BaiduSyncdisk/Obsidian知识库/10_课程库')
stop={'可以','需要','一个','什么','进行','使用','没有','就是','不是','我们','因为','所以','如果','知道','然后','自己','其实','比较','而且','但是','可能','通过','应该','问题','那么','对于','方面','来说','非常','很多'}

report=[]
for cat in sorted(vault.iterdir()):
    if not cat.is_dir() or cat.name=='11_OER开源技能库': continue
    for cd in sorted(cat.iterdir()):
        if not cd.is_dir(): continue
        sd=cd/'03_逐节总结'
        if not sd.exists(): continue
        
        pdf_files=[f for f in sd.glob('*.md') if 'ASR' not in f.name]
        asr_files=list(sd.glob('*ASR*.md'))
        
        if not pdf_files or not asr_files: continue
        
        pdf_text=''
        for f in pdf_files[:10]:
            try: pdf_text+=f.read_text(encoding='utf-8',errors='ignore')[:3000]
            except: pass
        asr_text=''
        for f in asr_files[:10]:
            try: asr_text+=f.read_text(encoding='utf-8',errors='ignore')[:3000]
            except: pass
        
        if len(pdf_text)<500 or len(asr_text)<500: continue
        
        pdf_terms=Counter(t for t in re.findall(r'[\u4e00-\u9fff]{2,6}',pdf_text) if t not in stop)
        asr_terms=Counter(t for t in re.findall(r'[\u4e00-\u9fff]{2,6}',asr_text) if t not in stop)
        
        common=set(pdf_terms) & set(asr_terms)
        all_terms=set(pdf_terms) | set(asr_terms)
        overlap=len(common)/len(all_terms)*100 if all_terms else 0
        
        top_shared=[t for t,_ in pdf_terms.most_common(30) if t in common][:5]
        
        if overlap>8:
            report.append(('✅',cd.name,int(overlap),' | '.join(top_shared)))
        else:
            report.append(('⚠️',cd.name,int(overlap),'PDF/ASR diverges'))

print(f'{"":6} {"课程":30} {"重叠":>5} {"共享术语"}')
for icon,name,ov,terms in sorted(report,key=lambda x:-x[2]):
    print(f'{icon} {name:36} {ov:>3}%  {terms[:60]}')

good=sum(1 for r in report if r[0]=='✅')
print(f'\n总计: {len(report)} 门多源课程, 匹配: {good}, 低重叠: {len(report)-good}')
