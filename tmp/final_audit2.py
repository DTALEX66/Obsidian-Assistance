import re
from pathlib import Path
from collections import defaultdict

vault=Path('E:/BaiduSyncdisk/Obsidian知识库/10_课程库')
disk=Path('E:/服务器')

print('='*60)
print('全 面 审 计')
print('='*60)

# === 1. Content coverage ===
print('\n--- 1. 内容覆盖 ---')
issues_found=0
for cat in sorted(vault.iterdir()):
    if not cat.is_dir(): continue
    for cd in sorted(cat.iterdir()):
        if not cd.is_dir(): continue
        m=cd/'00_课程主页.md'
        if not m.exists(): continue
        t=m.read_text(encoding='utf-8',errors='ignore')
        sd=cd/'03_逐节总结'
        
        n_pdf=sum(1 for f in sd.glob('*[!ASR]*.md')) if sd.exists() else 0
        n_asr=sum(1 for f in sd.glob('*ASR*.md')) if sd.exists() else 0
        has_map=(cd/'02_课程地图.md').exists()
        ve=cd/'06_验证与不确定项.md'
        has_verify=ve.exists() and ve.stat().st_size>300
        size=m.stat().st_size
        
        src_m=re.search(r'source_root:\s*"([^"]+)"',t)
        src_exists=Path(src_m.group(1)).exists() if src_m else False
        
        issues=[]
        if not src_exists: issues.append('源不存在')
        if size<3000: issues.append('内容少')
        if n_pdf==0 and n_asr==0: issues.append('无总结')
        if not has_map: issues.append('无地图')
        if not has_verify: issues.append('无验证')
        
        icon='OK' if not issues else '!!'
        issue_str='; '.join(issues) if issues else '-'
        print(f'{icon} {cd.name}: {size//1000}K PDF={n_pdf} ASR={n_asr} [{issue_str}]')
        if issues: issues_found+=1

print(f'\n问题课程: {issues_found}')

# === 2. Requirements check ===
print('\n--- 2. 需求覆盖 ---')
checks=[
    ('课程主页', sum(1 for _ in vault.rglob('00_课程主页.md'))),
    ('原始索引', sum(1 for _ in vault.rglob('01_原始资料链接索引.md'))),
    ('课程地图', sum(1 for _ in vault.rglob('02_课程地图.md'))),
    ('逐节总结', sum(1 for _ in vault.rglob('03_逐节总结/*.md'))),
    ('验证页', sum(1 for _ in vault.rglob('06_验证与不确定项.md'))),
    ('视觉索引', sum(1 for _ in vault.rglob('12_视觉索引与配图.md'))),
    ('内容截图', sum(1 for _ in Path('E:/BaiduSyncdisk/Obsidian知识库/99_附件_重组/内容匹配截图').rglob('*.png'))),
    ('权威外链', sum(1 for m in vault.rglob('00_课程主页.md') if 'http' in m.read_text(encoding='utf-8',errors='ignore'))),
    ('Wikilink', sum(1 for m in vault.rglob('00_课程主页.md') if '[[' in m.read_text(encoding='utf-8',errors='ignore'))),
    ('Dataview', sum(1 for m in vault.rglob('00_课程主页.md') if 'dataview' in m.read_text(encoding='utf-8',errors='ignore').lower())),
]
for item,count in checks:
    print(f'  {item}: {count}')

# === 3. Merge candidates ===
print('\n--- 3. 可合并课程 ---')
# Find tiny courses in same category
merges=[]
for cat in sorted(vault.iterdir()):
    if not cat.is_dir() or cat.name=='11_OER开源技能库': continue
    tiny=[]
    normal=[]
    for cd in sorted(cat.iterdir()):
        if not cd.is_dir(): continue
        m=cd/'00_课程主页.md'
        if not m.exists(): continue
        if m.stat().st_size<3000:
            tiny.append(cd.name)
        else:
            normal.append(cd.name)
    if len(tiny)>=2 and len(normal)>=1:
        merges.append((cat.name, tiny))

for cat_name, courses in merges:
    print(f'  {cat_name}: 可合并 {len(courses)} 门小课 -> {", ".join(courses[:5])}')

# Special: 术数资料 12 sub-courses
shu=vault/'术数资料'
if shu.exists():
    tiny_shu=[cd.name for cd in shu.iterdir() if cd.is_dir() and (cd/'00_课程主页.md').exists() and (cd/'00_课程主页.md').stat().st_size<3000]
    if tiny_shu:
        print(f'  术数资料: {len(tiny_shu)}门可合并子课程')

print('\n=== 审计完成 ===')
