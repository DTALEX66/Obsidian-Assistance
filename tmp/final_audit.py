from pathlib import Path
v=Path('E:/BaiduSyncdisk/Obsidian知识库/10_课程库')
updated=0; scores=[]

for cat in sorted(v.iterdir()):
    if not cat.is_dir(): continue
    if cat.name=='11_OER开源技能库': continue
    for cd in sorted(cat.iterdir()):
        if not cd.is_dir(): continue
        m=cd/'00_课程主页.md'
        if not m.exists(): continue
        t=m.read_text(encoding='utf-8',errors='ignore')
        changed=False
        
        sd=cd/'03_逐节总结'
        vp=cd/'12_视觉索引与配图.md'
        ve=cd/'06_验证与不确定项.md'
        
        ok='Y'; na='NA'; no='N'
        has_pdf=sd.exists() and len(list(sd.glob('*[!ASR]*.md')))>0
        has_asr=sd.exists() and len(list(sd.glob('*ASR*.md')))>0
        has_visual=vp.exists() and vp.stat().st_size>500
        has_ext='http' in t
        has_wiki='[[' in t
        has_dv='dataview' in t.lower()
        has_ver=ve.exists() and ve.stat().st_size>300
        
        items=[has_pdf,has_asr,has_visual,has_ext,has_wiki,has_dv,has_ver]
        score=sum(1 for i in items if i)*100//len(items)
        scores.append(score)
        
        audit=f'''## 完整性审计

| 维度 | 状态 |
|---|---|
| PDF文本 | {ok if has_pdf else na} |
| ASR转写 | {ok if has_asr else na} |
| 视觉索引 | {ok if has_visual else no} |
| 外部链接 | {ok if has_ext else no} |
| 内部导航 | {ok if has_wiki else no} |
| Dataview | {ok if has_dv else no} |
| 验证页 | {ok if has_ver else no} |

**完整度: {score}%**
'''
        if '## 完整性审计' not in t:
            t=t.rstrip()+'\n\n'+audit
            changed=True
        
        if changed:
            m.write_text(t,encoding='utf-8')
            updated+=1

print(f'Updated: {updated}')
print(f'Avg: {sum(scores)//len(scores)}%')
print(f'Range: {min(scores)}-{max(scores)}%')
