from pathlib import Path

from scripts.v8.retro_summary_generator import audit, collect_outputs, markdown_report, write_reports


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def mission(date='2026-07-02', course='知识内化训练营'):
    return f'''---
type: talos-daily-mission
mission_date: {date}
course: {course}
---
# TALOS Daily Mission — {date}

## 1. Evidence / 证据
- [x] evidence
- 选择的证据/原文链接：[[02_课程库/{course}/11_证据索引|证据]]
## 2. Recall / 主动回忆
- [x] recall
## 3. Project / 项目动作
- [x] project
- 产出链接/截图/文件：[[00_主页/12_TALOS_Daily_Missions/outputs/{date}_产出|产出]]
## 4. Log / 复盘
- 做了什么：完成任务
- 卡住点：未声称已导入客户端
- 明天下一步：继续验证产出
## 5. Done Criteria
- [x] done 1
- [x] done 2
- [x] done 3
'''


def output_note(date='2026-07-02', course='知识内化训练营'):
    return f'''---
type: talos-mission-output
mission_date: {date}
course: {course}
status: draft
---
# {date}｜{course} 产出
'''


def test_audit_collects_missions_and_outputs(tmp_path):
    vault = tmp_path / 'vault'
    write(vault / '00_主页/12_TALOS_Daily_Missions/2026-07-02.md', mission())
    write(vault / '00_主页/12_TALOS_Daily_Missions/outputs/2026-07-02_产出.md', output_note())
    data = audit(vault)
    assert data['missions'] == 1
    assert data['outputs'] == 1
    assert data['tasks_done'] == 6
    assert data['tasks_total'] == 6
    assert data['completion_rate'] == 1.0
    assert data['course_counts']['知识内化训练营'] == 1


def test_audit_ignores_non_mission_top_level_outputs(tmp_path):
    vault = tmp_path / 'vault'
    write(vault / '00_主页/12_TALOS_Daily_Missions/2026-07-02.md', mission())
    write(vault / '00_主页/12_TALOS_Daily_Missions/2026-07-02_output.md', output_note())
    data = audit(vault)
    assert data['missions'] == 1
    assert data['tasks_total'] == 6


def test_collect_outputs_extracts_frontmatter(tmp_path):
    vault = tmp_path / 'vault'
    write(vault / '00_主页/12_TALOS_Daily_Missions/outputs/2026-07-02_产出.md', output_note())
    items = collect_outputs(vault)
    assert len(items) == 1
    assert items[0].mission_date == '2026-07-02'
    assert items[0].course == '知识内化训练营'
    assert items[0].status == 'draft'


def test_markdown_report_links_outputs_and_boundary(tmp_path):
    vault = tmp_path / 'vault'
    write(vault / '00_主页/12_TALOS_Daily_Missions/2026-07-02.md', mission())
    write(vault / '00_主页/12_TALOS_Daily_Missions/outputs/2026-07-02_产出.md', output_note())
    text = markdown_report(audit(vault))
    assert 'TALOS V8 自动复盘汇总' in text
    assert '[[00_主页/12_TALOS_Daily_Missions/outputs/2026-07-02_产出|' in text
    assert '不得由复盘报告生成' in text
    assert text.count('```') % 2 == 0


def test_write_reports(tmp_path):
    vault = tmp_path / 'vault'
    write(vault / '00_主页/12_TALOS_Daily_Missions/2026-07-02.md', mission())
    out = tmp_path / 'out'
    paths = write_reports(audit(vault), out)
    assert Path(paths['json']).exists()
    assert Path(paths['markdown']).exists()
