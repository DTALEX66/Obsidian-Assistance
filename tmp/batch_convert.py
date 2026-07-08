import re, subprocess
from pathlib import Path

vault=Path('E:/BaiduSyncdisk/Obsidian知识库/10_课程库')
disk=Path('E:/服务器')

def extract_text(path, max_chars=3000):
    try:
        import fitz
        doc=fitz.open(path)
        text=''
        for page in doc[:min(3, len(doc))]:
            text+=page.get_text()
            if len(text)>max_chars: break
        doc.close()
        return text[:max_chars] if text.strip() else None
    except:
        return None

def extract_docx(path, max_chars=3000):
    try:
        import zipfile
        with zipfile.ZipFile(path) as z:
            xml=z.read('word/document.xml').decode('utf-8',errors='ignore')
        text=re.sub(r'<[^>]+>','',xml)
        text=re.sub(r'\s+',' ',text).strip()
        return text[:max_chars]
    except:
        return None

extracted_total=0
merged_total=0

for cat_dir in sorted(vault.iterdir()):
    if not cat_dir.is_dir(): continue
    cat=cat_dir.name
    
    # Skip OER (no sources) and already-rich categories
    if cat in ('11_OER开源技能库',): continue
    
    for cd in sorted(cat_dir.iterdir()):
        if not cd.is_dir(): continue
        main=cd/'00_课程主页.md'
        if not main.exists(): continue
        t=main.read_text(encoding='utf-8')
        
        # Already rich?
        if len(t)>3000: continue
        
        # 1. Extract source files
        m=re.search(r'source_root:\s*"([^"]+)"', t)
        if not m: continue
        sp=Path(m.group(1))
        if not sp.exists(): continue
        
        sd=cd/'03_逐节总结'
        sd.mkdir(exist_ok=True)
        
        for pdf in list(sp.rglob('*.pdf'))[:5]:
            if (sd/f'{pdf.stem}.md').exists(): continue
            text=extract_text(pdf)
            if text:
                (sd/f'{pdf.stem}.md').write_text(f'# {pdf.stem}\n\n{text}', encoding='utf-8')
                extracted_total+=1
        
        for doc in list(sp.rglob('*.docx'))[:3]:
            if (sd/f'{doc.stem}.md').exists(): continue
            text=extract_docx(doc)
            if text:
                (sd/f'{doc.stem}.md').write_text(f'# {doc.stem}\n\n{text}', encoding='utf-8')
                extracted_total+=1
        
        # 2. Merge old content if available
        old=cd/'00_课程总览.md'
        if old.exists():
            old_t=old.read_text(encoding='utf-8')
            if len(old_t)>500:
                parts=old_t.split('---\n',2)
                body=parts[2] if len(parts)>=3 else old_t
                if body[:200] not in t:
                    t=t.rstrip()+'\n\n---\n\n## 课程内容\n\n'+body
                    main.write_text(t, encoding='utf-8')
                    merged_total+=1
        
        # 3. Merge sub-page content
        for kp in ['03_模块总结.md','04_关键图表与课件索引.md','08_术语索引.md']:
            fp=cd/kp
            if fp.exists() and fp.stat().st_size>500:
                ct=fp.read_text(encoding='utf-8')
                parts=ct.split('---\n',2)
                body=parts[2] if len(parts)>=3 else ct
                if len(body)>100 and body[:200] not in t:
                    t=t.rstrip()+f'\n\n## {fp.stem}\n\n{body[:1500]}'
                    main.write_text(t, encoding='utf-8')
                    merged_total+=1
        
        # Update status
        t=main.read_text(encoding='utf-8')
        if len(t)>3000:
            t=t.replace('status: 待转化', 'status: 已转化')
            t=t.replace('status: 骨架', 'status: 已转化')
            main.write_text(t, encoding='utf-8')

print(f'Extracted {extracted_total} PDF/DOCX files')
print(f'Merged {merged_total} old content pieces')
print('Done!')
