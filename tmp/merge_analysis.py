import re
from pathlib import Path
from collections import Counter, defaultdict

vault=Path('E:/BaiduSyncdisk/Obsidian知识库/10_课程库')
stop={'可以','需要','一个','什么','进行','使用','没有','就是','不是','我们','因为','所以','如果','知道','然后','自己','其实','比较','而且','但是','可能','通过','应该','问题','那么','对于','方面','来说','非常','很多'}

# Content fingerprints
fingerprints={}
for cat in sorted(vault.iterdir()):
    if not cat.is_dir(): continue
    for cd in sorted(cat.iterdir()):
        if not cd.is_dir(): continue
        m=cd/'00_课程主页.md'
        if not m.exists() or m.stat().st_size<2000: continue
        sd=cd/'03_逐节总结'
        text=''
        if sd.exists():
            for f in sorted(sd.glob('*.md'))[:10]:
                try: text+=f.read_text(encoding='utf-8',errors='ignore')[:2000]
                except: pass
        terms=Counter(t for t in re.findall(r'[\u4e00-\u9fff]{2,6}',text) if t not in stop)
        fingerprints[cd.name]=set(t for t,_ in terms.most_common(15))

# Find similar
print('=== 内容相似度 (>15%) ===')
pairs=[]
for n1,f1 in fingerprints.items():
    for n2,f2 in fingerprints.items():
        if n1>=n2: continue
        shared=len(f1 & f2)
        total=len(f1 | f2)
        if total==0: continue
        sim=shared*100//total
        if sim>=15:
            pairs.append((sim,n1,n2,shared))

for sim,n1,n2,shared in sorted(pairs, reverse=True):
    print(f'  {sim}% {n1} <-> {n2} ({shared} shared)')

# Complementary in same category
print('\n=== 互补课程对 ===')
for cat in sorted(vault.iterdir()):
    if not cat.is_dir() or cat.name=='11_OER开源技能库': continue
    courses=list(cat.iterdir())
    for i in range(len(courses)):
        for j in range(i+1,len(courses)):
            c1=courses[i]; c2=courses[j]
            if not c1.is_dir() or not c2.is_dir(): continue
            n1=c1.name; n2=c2.name
            w1=set(re.findall(r'[\u4e00-\u9fff]{2,4}',n1))
            w2=set(re.findall(r'[\u4e00-\u9fff]{2,4}',n2))
            shared=w1 & w2
            if len(shared)>=2 and len(shared)/max(len(w1),len(w2))>0.3:
                print(f'  {cat.name}: {n1[:35]} <-> {n2[:35]}')

# Source path overlap
print('\n=== 源路径共享 ===')
src_map=defaultdict(list)
for cat in sorted(vault.iterdir()):
    if not cat.is_dir() or cat.name=='11_OER开源技能库': continue
    for cd in sorted(cat.iterdir()):
        if not cd.is_dir(): continue
        m=cd/'00_课程主页.md'
        if not m.exists(): continue
        t=m.read_text(encoding='utf-8',errors='ignore')
        src=re.search(r'source_root:\s*"([^"]+)"',t)
        if src:
            parent=str(Path(src.group(1)).parent)
            src_map[parent].append(cd.name)

for src_parent,courses in src_map.items():
    if len(courses)>=2:
        pname=Path(src_parent).name
        print(f'  {pname}: {", ".join(courses[:5])}')
