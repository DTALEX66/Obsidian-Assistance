from pathlib import Path
vault=Path('E:/BaiduSyncdisk/Obsidian知识库')

bad=[]
for p in vault.rglob('*.md'):
    if '.obsidian' in str(p): continue
    rel=str(p.relative_to(vault))
    sep = '/' if '/' in rel else '\\'
    parts = rel.replace('\\', '/').split('/')
    
    # Files at root level that look like they should be in subdirs
    if len(parts) == 1:
        for pfx in ['00_主页_','02_课程库_','03_知识卡片_','04_复习卡片_','50_领域知识_']:
            if rel.startswith(pfx):
                bad.append(('root_wrong', rel))
                break
    
    # Double underscore in filename
    if '__' in p.name:
        bad.append(('double_underscore', rel))

print(f'Found {len(bad)} bad files:')
for loc, name in sorted(bad):
    full=vault/name
    print(f'  [{loc}] {name} ({full.stat().st_size}B)')
