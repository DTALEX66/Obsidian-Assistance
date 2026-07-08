import re
from pathlib import Path

vault=Path('E:/BaiduSyncdisk/Obsidian知识库/10_课程库')
disk=Path('E:/服务器')

# 1. Disk categories
print('=== DATA DISK ===')
disk_cats={}
for d in sorted(disk.iterdir()):
    if not d.is_dir(): continue
    pkgs=[p.name for p in d.iterdir() if p.is_dir()]
    disk_cats[d.name]=pkgs
    print(f'\n{d.name}/ ({len(pkgs)} pkgs)')
    for p in pkgs:
        print(f'  {p[:80]}')

# 2. Vault
print('\n\n=== VAULT ===')
vault_cats={}
total_courses=0
for d in sorted(vault.iterdir()):
    if not d.is_dir(): continue
    courses=[c for c in d.iterdir() if c.is_dir() and (c/'00_课程主页.md').exists()]
    vault_cats[d.name]=[c.name for c in courses]
    total_courses+=len(courses)
    rich=sum(1 for c in courses if (c/'00_课程主页.md').stat().st_size>3000)
    print(f'\n{d.name}/ ({len(courses)} courses, {rich} rich)')
    for c in sorted(courses):
        main=c/'00_课程主页.md'
        t=main.read_text(encoding='utf-8')
        size=len(t)
        m=re.search(r'source_root:\s*"([^"]+)"', t)
        status='RICH' if size>3000 else 'thin'
        src_ok='OK' if (m and Path(m.group(1)).exists()) else 'MISSING'
        print(f'  [{status}] {c.name} src={src_ok}')

print(f'\nTotal vault courses: {total_courses}')

# 3. Mismatch check
print('\n\n=== MISMATCHES ===')
for cat_name, pkgs in disk_cats.items():
    vault_cat=None
    for vc in vault_cats:
        vc_clean=vc.replace('_','').replace('0','').replace('1','').replace('2','').replace('3','').replace('4','').replace('5','').replace('6','').replace('7','').replace('8','').replace('9','')
        cn_clean=cat_name
        if vc_clean[:4] in cn_clean or cn_clean[:4] in vc_clean:
            vault_cat=vc
            break
    
    if not vault_cat:
        print(f'MISSING CATEGORY: {cat_name}')
        continue
    
    for pkg in pkgs:
        found=False
        for vc_name in vault_cats.get(vault_cat, []):
            main=vault/vault_cat/vc_name/'00_课程主页.md'
            if main.exists():
                t=main.read_text(encoding='utf-8')
                src=re.search(r'source_root:\s*"([^"]+)"', t)
                if src and pkg in src.group(1):
                    found=True
                    break
        if not found:
            print(f'UNMAPPED: {cat_name}/{pkg[:60]}')

# 4. Source paths check
print('\n\n=== BROKEN SOURCE PATHS ===')
for d in sorted(vault.iterdir()):
    if not d.is_dir(): continue
    for c in d.iterdir():
        if not c.is_dir(): continue
        main=c/'00_课程主页.md'
        if not main.exists(): continue
        t=main.read_text(encoding='utf-8')
        m=re.search(r'source_root:\s*"([^"]+)"', t)
        if m and not Path(m.group(1)).exists():
            print(f'  {d.name}/{c.name}: {m.group(1)[:80]}')
