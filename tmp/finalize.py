#!/usr/bin/env python3
"""Finalize: update all nav pages, create indexes"""
from pathlib import Path

vault=Path('E:/BaiduSyncdisk/Obsidian知识库')

# 1. Update 01_课程总览.md with all courses
courses_root=vault/'10_课程库'
cats=sorted([d for d in courses_root.iterdir() if d.is_dir()])

lines=['---','type: index','title: 课程总览','status: active','updated: 2026-07-08','---','','# 课程总览','']

for cat_dir in cats:
    cat_name=cat_dir.name
    course_dirs=sorted([d for d in cat_dir.iterdir() if d.is_dir()])
    if not course_dirs: continue
    
    lines.append(f'## {cat_name}')
    for cd in course_dirs:
        main=cd/'00_课程主页.md'
        if main.exists():
            lines.append(f'- [[../10_课程库/{cat_name}/{cd.name}/00_课程主页|{cd.name}]]')
    lines.append('')

nav=vault/'00_总控台/01_课程总览.md'
nav.write_text('\n'.join(lines)+'\n', encoding='utf-8')
print('Updated 01_课程总览.md')

# 2. Create 20_知识原子库 homepage
kc=vault/'20_知识原子库'
(kc/'00_知识原子库首页.md').write_text('''---
type: index
title: 知识原子库首页
status: active
---

# 知识原子库

跨课程复用的知识卡，按类型分类。

## 卡类型

| 类型 | 目录 | 来源 |
|---|---|---|
| 概念卡 | [[../20_知识原子库/21_概念卡\|21_概念卡]] | 旧知识卡片已迁移 |
| 方法卡 | 22_方法卡 | |
| 案例卡 | 23_案例卡 | |
| 流程卡 | 24_流程卡 | |
| 工具卡 | 25_工具卡 | |
| 术语卡 | [[../20_知识原子库/26_术语卡\|26_术语卡]] | 旧术语索引已迁移 |
| 问题卡 | 27_问题卡 | |
| 模型卡 | 28_模型卡 | |
| 金句观点卡 | 29_金句观点卡 | |
''', encoding='utf-8')
print('Created 00_知识原子库首页.md')

# 3. Create other section homepages
sections={
    '30_复习系统': ('00_复习系统首页.md', '# 复习系统\n\n主动回忆、间隔复习、错题薄弱点。\n\n- [[../30_复习系统/31_主动回忆|31_主动回忆]]\n- [[../30_复习系统/32_间隔复习|32_间隔复习]]\n'),
    '40_项目行动库': ('00_项目行动库首页.md', '# 项目行动库\n\n可执行任务、项目方案、提示词资产。\n'),
    '50_知识宫殿': ('00_知识宫殿首页.md', '# 知识宫殿\n\n空间记忆、视觉路线。\n'),
    '60_外部资料链接索引': ('00_外部资料链接首页.md', '# 外部资料链接索引\n\n原始盘链接，素材不入库。\n- [[../60_外部资料链接索引/67_原始盘总索引|67_原始盘总索引]]\n'),
}
for sec_dir, (fname, content) in sections.items():
    p=vault/sec_dir/fname
    if not p.exists():
        p.write_text(f'---\ntype: index\ntitle: {sec_dir}\n---\n\n{content}', encoding='utf-8')
        print(f'Created {fname}')

# 4. Update knowledge base homepage
home=vault/'00_总控台/00_知识库首页.md'
home.write_text('''---
type: dashboard
title: 知识库首页
status: active
updated: 2026-07-08
---

# 知识库首页

## 快速入口

- [[01_课程总览|课程总览（67门）]]
- [[05_外部资料盘索引|外部资料盘索引]]

## 核心模块

- [[../10_课程库|10_课程库]] — 57门本地课程 + 10门OER
- [[../20_知识原子库/00_知识原子库首页|20_知识原子库]] — 概念卡/方法卡/术语卡
- [[../30_复习系统/00_复习系统首页|30_复习系统]] — 主动回忆/间隔复习
- [[../40_项目行动库/00_项目行动库首页|40_项目行动库]] — 任务/项目/提示词
- [[../50_知识宫殿/00_知识宫殿首页|50_知识宫殿]] — 空间记忆
- [[../60_外部资料链接索引/00_外部资料链接首页|60_外部资料链接索引]] — 原始盘链接
- [[../70_模板系统|70_模板系统]] — 课程/知识卡/复习卡模板
- [[../80_审核与质检|80_审核与质检]] — AI转化待核验
- [[../90_系统资产|90_系统资产]] — 日志/报告/Dataview
''', encoding='utf-8')
print('Updated 00_知识库首页.md')

print('\nAll done!')
