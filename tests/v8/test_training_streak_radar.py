from pathlib import Path

from scripts.v8.training_streak_radar import audit, markdown_report, streak_days, write_reports


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')


def mission(date: str, course: str, done: bool = False) -> str:
    mark = 'x' if done else ' '
    return f'''---
type: talos-daily-mission
mission_date: {date}
course: {course}
---
# TALOS Daily Mission — {date}

## 1. Evidence / 证据
- [{mark}] evidence task
## 2. Recall / 主动回忆
- [ ] recall task
## 3. Project / 项目动作
- [ ] project task
## 4. Log / 复盘
- [ ] log task
'''


def test_streak_days_counts_back_from_today():
    assert streak_days(['2026-07-01', '2026-07-02'], today='2026-07-02') == 2
    assert streak_days(['2026-06-30', '2026-07-02'], today='2026-07-02') == 1
    assert streak_days([], today='2026-07-02') == 0


def test_audit_reads_missions_and_completion(tmp_path):
    vault = tmp_path / 'vault'
    write(vault / '00_主页/12_TALOS_Daily_Missions/2026-07-01.md', mission('2026-07-01', '课程A', done=True))
    write(vault / '00_主页/12_TALOS_Daily_Missions/2026-07-02.md', mission('2026-07-02', '课程A', done=False))
    data = audit(vault, today='2026-07-02')
    assert data['missions'] == 2
    assert data['tasks_total'] == 8
    assert data['tasks_done'] == 1
    assert data['streak_days'] == 2
    assert data['course_counts']['课程A'] == 2


def test_audit_detects_missing_sections(tmp_path):
    vault = tmp_path / 'vault'
    write(vault / '00_主页/12_TALOS_Daily_Missions/2026-07-02.md', '---\nmission_date: 2026-07-02\ncourse: 课程B\n---\n- [ ] task')
    data = audit(vault, today='2026-07-02')
    assert data['missing_sections']
    assert 'Evidence' in data['missing_sections'][0]['missing']


def test_markdown_report_has_links_and_boundary(tmp_path):
    vault = tmp_path / 'vault'
    write(vault / '00_主页/12_TALOS_Daily_Missions/2026-07-02.md', mission('2026-07-02', '课程A', done=True))
    text = markdown_report(audit(vault, today='2026-07-02'))
    assert '连续打卡' in text
    assert '[[00_主页/12_TALOS_Daily_Missions/2026-07-02|2026-07-02]]' in text
    assert '不得伪造成 verified' in text
    assert text.count('```') % 2 == 0


def test_write_reports_writes_json_and_markdown(tmp_path):
    vault = tmp_path / 'vault'
    write(vault / '00_主页/12_TALOS_Daily_Missions/2026-07-02.md', mission('2026-07-02', '课程A', done=True))
    out = tmp_path / 'out'
    paths = write_reports(audit(vault, today='2026-07-02'), out)
    assert Path(paths['json']).exists()
    assert Path(paths['markdown']).exists()
