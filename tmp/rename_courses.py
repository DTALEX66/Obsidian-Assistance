import re
from pathlib import Path

v=Path('E:/BaiduSyncdisk/Obsidian知识库/10_课程库')
renamed=0

for cat in sorted(v.iterdir()):
    if not cat.is_dir(): continue
    for cd in sorted(cat.iterdir()):
        if not cd.is_dir(): continue
        # Skip if already has descriptive name
        parts=cd.name.split('_',1)
        if len(parts)>1 and len(parts[1])>2 and not parts[1].startswith('C'):
            continue
        
        m=cd/'00_课程主页.md'
        if not m.exists(): continue
        t=m.read_text(encoding='utf-8',errors='ignore')
        title_line=[l for l in t.split('\n') if l.startswith('title:')]
        if not title_line: continue
        title=title_line[0].replace('title:','').strip().strip('"').strip()
        if not title: continue
        
        safe=title.replace('/','_').replace('\\','_').replace(':','_')
        safe=safe.replace('*','').replace('?','').replace('"','')
        safe=safe.replace('<','').replace('>','').replace('|','')[:50]
        
        new_name=f'{cd.name}_{safe}'
        new_path=cd.parent/new_name
        if new_path.exists(): continue
        
        try:
            cd.rename(new_path)
            print(f'  {cd.name} -> {new_name}')
            renamed+=1
        except Exception as e:
            print(f'  FAIL: {cd.name} - {e}')

print(f'Renamed: {renamed}')
