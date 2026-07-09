from pathlib import Path
import re
from collections import Counter

v=Path('E:/BaiduSyncdisk/Obsidian知识库')

print('='*60)
print('OBSIDIAN 知识库全量审计')
print('='*60)

# 1. Structure
print('\n--- 1. 目录结构 ---')
for d in sorted(v.iterdir()):
    if d.is_dir() and not d.name.startswith('.'):
        items=sum(1 for _ in d.rglob('*'))
        files=sum(1 for _ in d.rglob('*') if _.is_file())
        print(f'  {d.name}/  ({items} items, {files} files)')

# 2. Course audit
courses=v/'10_课程库'
print(f'\n--- 2. 课程库 ({len(list(courses.iterdir()))} 分类) ---')
total=0; rich=0; thin=0; broken_source=0
empty_verify=0; no_screenshots=0; no_extlink=0

for cat in sorted(courses.iterdir()):
    if not cat.is_dir(): continue
    c_count=0
    for cd in sorted(cat.iterdir()):
        if not cd.is_dir(): continue
        m=cd/'00_课程主页.md'
        if not m.exists(): continue
        total+=1; c_count+=1
        t=m.read_text(encoding='utf-8',errors='ignore')
        s=m.stat().st_size
        
        if s>5000: rich+=1
        elif s<3000: thin+=1
        
        # Check source_root exists
        src=re.search(r'source_root:\s*"([^"]+)"',t)
        if src and not Path(src.group(1)).exists():
            broken_source+=1
        
        # Verify page
        ve=cd/'06_验证与不确定项.md'
        if not ve.exists() or ve.stat().st_size<100: empty_verify+=1
        
        # Screenshots
        if 'http' not in t: no_extlink+=1
    
    bar='x'*c_count
    print(f'  {cat.name}: {bar} ({c_count})')

print(f'\n  总课程: {total}')
print(f'  丰富(>5K): {rich} | 薄弱(<3K): {thin}')
print(f'  断裂source_path: {broken_source}')
print(f'  空验证页: {empty_verify}')
print(f'  无外链: {no_extlink}')

# 3. Attachments
print(f'\n--- 3. 附件 ---')
att=v/'99_附件_重组'
if att.exists():
    pngs=list(att.rglob('*.png'))
    print(f'  截图: {len(pngs)} 张')
    course_imgs=Counter()
    for p in pngs:
        parts=p.relative_to(att).parts
        if parts: course_imgs[parts[0]]+=1
    top10=course_imgs.most_common(10)
    for cid,cnt in top10:
        print(f'    {cid}: {cnt} 张')

# 4. Broken wikilinks (exclude archive)
print(f'\n--- 4. Wikilink 审计 ---')
all_wikilinks=set()
all_pages=set()
for m in v.rglob('*.md'):
    if '.obsidian' in str(m) or '99_旧库' in str(m): continue
    rel=str(m.relative_to(v)).replace('\\','/').replace('.md','')
    all_pages.add(rel)
    t=m.read_text(encoding='utf-8',errors='ignore')
    for link in re.findall(r'\[\[([^\]|#]+)',t):
        link=link.strip()
        # Skip code artifacts
        if link.startswith('[') or ',' in link or link.startswith("'"): continue
        if len(link)<2: continue
        all_wikilinks.add(link)

broken_links=all_wikilinks-all_pages
real_broken=[l for l in broken_links if not l.startswith('http') and not l.startswith('../')]
if real_broken:
    print(f'  断裂wikilink: {len(real_broken)}')
    for l in sorted(real_broken)[:10]:
        print(f'    [[{l}]]')
else:
    print(f'  无断裂wikilink')

# 5. Score
print(f'\n--- 5. 总体评分 ---')
issues=broken_source+empty_verify+len(real_broken)
score=100-(issues*2+no_extlink*1+thin*1)
print(f'  评分: {max(0,min(100,score))}/100')
print(f'  问题明细:')
print(f'    断裂路径: {broken_source}')
print(f'    空验证页: {empty_verify}')
print(f'    断裂wikilink: {len(real_broken)}')
print(f'    无外链: {no_extlink}')
print(f'    薄弱课程: {thin}')
