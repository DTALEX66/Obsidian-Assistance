import re
from pathlib import Path

vault=Path('E:/BaiduSyncdisk/Obsidian知识库/02_课程库')
new_src=Path('E:/服务器')

# Build index of all course dirs
dir_index={}
for d in new_src.rglob('*'):
    if d.is_dir():
        key=d.name.lower()
        dir_index[key]=str(d)

cnt=0
for cd in sorted(vault.iterdir()):
    if not cd.is_dir(): continue
    main=cd/'00_课程总览.md'
    if not main.exists(): continue
    
    text=main.read_text(encoding='utf-8')
    original=text
    
    # Get source_title
    m=re.search(r'source_title:\s*(.+)', text)
    source_title=m.group(1).strip() if m else None
    
    # Find matching dir
    found_path=None
    for name in ([source_title] if source_title else []) + [cd.name]:
        if not name: continue
        if name.lower() in dir_index:
            found_path=dir_index[name.lower()]
            break
        # Try cleaned match
        clean_course=''.join(c for c in cd.name.lower() if c.isalnum())
        for dname, dpath in dir_index.items():
            clean_dname=''.join(c for c in dname if c.isalnum())
            if len(clean_course)>=4 and clean_course in clean_dname:
                found_path=dpath
                break
        if found_path:
            break
    
    if found_path:
        # Remove old source_path
        lines=text.split('\n')
        new_lines=[]
        replaced=False
        for line in lines:
            if line.strip().startswith('source_path:') and 'E:/' in line:
                new_lines.append(f'source_path: "{found_path}"')
                replaced=True
            elif line.strip().startswith('source:') and 'E:/' in line:
                new_lines.append(f'source: "{found_path}"')
                replaced=True
            elif 'E:/服务器/' in line and 'source_path' not in line:
                # Update body references
                line=line.replace(
                    line[line.index('E:/服务器/'):line.index('`', line.index('E:/服务器/')+10) if '`' in line[line.index('E:/服务器/'):] else len(line)],
                    found_path
                ) if '`E:/服务器/' in line else line
                new_lines.append(line)
            else:
                new_lines.append(line)
        
        new_text='\n'.join(new_lines)
        if new_text!=original:
            main.write_text(new_text, encoding='utf-8')
            cnt+=1
            if cnt<=15:
                print(f'  OK {cd.name}')

print(f'\nUpdated source_path for {cnt} courses')
