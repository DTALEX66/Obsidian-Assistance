import re
from pathlib import Path
from collections import Counter

vault=Path('E:/BaiduSyncdisk/Obsidian知识库/10_课程库')
stop_words=['可以','需要','一个','什么','进行','使用','没有','就是','不是','我们','因为','所以','如果','知道','然后','自己','其实','比较','而且','但是','可能','通过','应该','问题','那么','对于','方面','来说','非常','很多']

total=0
compared=0

for cat in sorted(vault.iterdir()):
    if not cat.is_dir() or cat.name=='11_OER开源技能库':
        continue
    for cd in sorted(cat.iterdir()):
        if not cd.is_dir():
            continue
        sd=cd/'03_逐节总结'
        if not sd.exists():
            continue
        total+=1
        
        all_files=[f for f in sd.glob('*.md') if f.stat().st_size>200]
        if len(all_files)<2:
            continue
        
        pdf_files=[f for f in all_files if 'ASR' not in f.name]
        asr_files=[f for f in all_files if 'ASR' in f.name]
        
        comp='\n\n## 多源交叉对比\n\n'
        
        n_pdf=len(pdf_files)
        n_asr=len(asr_files)
        if n_pdf:
            comp+=f'| PDF/文档 | {n_pdf} |\n'
        if n_asr:
            comp+=f'| ASR/音频 | {n_asr} |\n'
        comp+='\n'
        
        # PDF vs ASR
        if pdf_files and asr_files:
            try:
                pdf_all=pdf_files[0].read_text(encoding='utf-8',errors='ignore')[:3000]
                asr_all=asr_files[0].read_text(encoding='utf-8',errors='ignore')[:3000]
                pdf_terms=Counter(t for t in re.findall(r'[\u4e00-\u9fff]{2,6}',pdf_all) if t not in stop_words)
                asr_terms=Counter(t for t in re.findall(r'[\u4e00-\u9fff]{2,6}',asr_all) if t not in stop_words)
                shared=set(pdf_terms) & set(asr_terms)
                comp+=f'### PDF vs ASR\n- 共享概念: {len(shared)}个\n'
                if shared:
                    top=[t for t,_ in pdf_terms.most_common(20) if t in shared][:5]
                    comp+=f'- {" | ".join(top)}\n'
                comp+='- 结论: 互补关系\n\n'
            except:
                pass
        
        # PDF vs PDF
        if len(pdf_files)>=2:
            try:
                t1=pdf_files[0].read_text(encoding='utf-8',errors='ignore')[:2000]
                t2=pdf_files[1].read_text(encoding='utf-8',errors='ignore')[:2000]
                s1=set(re.findall(r'[\u4e00-\u9fff]{2,6}',t1))
                s2=set(re.findall(r'[\u4e00-\u9fff]{2,6}',t2))
                comp+=f'### PDF vs PDF ({n_pdf} docs)\n- 术语重叠: {len(s1&s2)}个\n\n'
            except:
                pass
        
        # ASR vs ASR
        if n_asr>=2:
            comp+=f'### ASR vs ASR ({n_asr} videos)\n\n'
        
        # Missing sources
        if not pdf_files and asr_files:
            comp+='### 仅视频源\n- 无文档交叉验证\n\n'
        elif pdf_files and not asr_files:
            comp+='### 仅文档源\n- 无视频转录交叉验证\n\n'
        
        # Write
        ve=cd/'06_验证与不确定项.md'
        vt=ve.read_text(encoding='utf-8',errors='ignore') if ve.exists() else ''
        if '## 多源交叉对比' in vt:
            vt=vt[:vt.index('## 多源交叉对比')]
        vt=vt.rstrip()+comp
        ve.write_text(vt,encoding='utf-8')
        compared+=1

print(f'Done: {compared}/{total} courses')
