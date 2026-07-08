from pathlib import Path

# Fix C0207
for d in Path('E:/BaiduSyncdisk/Obsidian知识库/10_课程库/02_新媒体运营与增长').iterdir():
    if d.is_dir() and d.name.startswith('C0207'):
        main=d/'00_课程主页.md'
        t=main.read_text(encoding='utf-8')
        old='E:/服务器/设计课程/邢开捷'
        new='E:/服务器/新媒体运营与增长/邢开捷'
        t=t.replace(old, new)
        main.write_text(t, encoding='utf-8')
        print('Fixed C0207')
        break

# Fix C0401 add version B
for d in Path('E:/BaiduSyncdisk/Obsidian知识库/10_课程库/04_记忆力与学习力').iterdir():
    if d.is_dir() and d.name.startswith('C0401'):
        main=d/'00_课程主页.md'
        t=main.read_text(encoding='utf-8')
        if '版本B' not in t:
            t=t.replace('## 4. 后续转化入口',
                '## 3.5 第二版本\n- 版本B：`E:\\服务器\\记忆力与学习力\\30天考霸训练营，北大博士后教你通关任何考试，助你高分拿下证书、岗位、考试(2)`\n\n## 4. 后续转化入口')
            main.write_text(t, encoding='utf-8')
            print('Added C0401 version B')
        break

print('Done!')
