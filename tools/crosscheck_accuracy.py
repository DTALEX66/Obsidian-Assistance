#!/usr/bin/env python3
"""
全网交叉验证补足精度缺口
对于 OCR/ASR 精度不足 85% 的内容，
通过公开网络权威来源进行交叉校对
"""

import re, json
from pathlib import Path
from datetime import datetime

TOOLS_DIR = Path(__file__).parent
VAULT = Path("E:/BaiduSyncdisk/Obsidian知识库")

# 公开网络权威来源注册表
AUTHORITY_SOURCES = {
    "心理学": [
        ("Yale PSYC 110", "https://oyc.yale.edu/introduction-psychology/psyc-110"),
        ("APA Dictionary", "https://dictionary.apa.org/"),
    ],
    "记忆术": [
        ("Art of Memory", "https://artofmemory.com/"),
        ("SuperMemo", "https://www.supermemo.com/"),
    ],
    "设计": [
        ("Apple HIG", "https://developer.apple.com/design/human-interface-guidelines/"),
        ("Material Design 3", "https://m3.material.io/"),
        ("Adobe Firefly", "https://experienceleague.adobe.com/en/docs/creative-cloud-enterprise-learn/cce-learning-hub/fireflyoverview/overview-firefly"),
    ],
    "编程": [
        ("Python Docs", "https://docs.python.org/3/"),
        ("MDN Web Docs", "https://developer.mozilla.org/"),
        ("GitHub Docs", "https://docs.github.com/"),
    ],
    "新媒体": [
        ("HubSpot Academy", "https://academy.hubspot.com/"),
        ("Smart Insights", "https://www.smartinsights.com/"),
    ],
    "数学": [
        ("Khan Academy", "https://www.khanacademy.org/"),
        ("MIT OCW Math", "https://ocw.mit.edu/search/?d=Mathematics"),
    ],
    "传统文化": [
        ("ctext.org", "https://ctext.org/"),
        ("Wikisource", "https://wikisource.org/"),
    ],
}

def get_crosscheck_sources(course_name: str, domain: str) -> list:
    """根据课程名和领域返回可用的权威来源"""
    sources = []
    for key, urls in AUTHORITY_SOURCES.items():
        if key in course_name or key in domain:
            sources.extend(urls)
    return sources[:5]


def generate_crosscheck_report(course_path: Path) -> dict:
    """为单门课程生成交叉验证建议"""
    main = course_path / "00_课程主页.md"
    if not main.exists():
        return {}
    
    text = main.read_text(encoding='utf-8')
    
    # 提取课程信息
    domain_match = re.search(r'domain:\s*(.+)', text)
    domain = domain_match.group(1).strip() if domain_match else ""
    
    # 提取已转化内容的关键术语
    terms = set()
    summaries_dir = course_path / "03_逐节总结"
    if summaries_dir.exists():
        for sf in summaries_dir.glob("*.md"):
            st = sf.read_text(encoding='utf-8')[:2000]
            # 提取中文术语 (2-8字)
            found = re.findall(r'[\u4e00-\u9fff]{2,8}', st)
            terms.update(found[:20])
    
    # 获取权威来源
    sources = get_crosscheck_sources(course_path.name, domain)
    
    return {
        "course": course_path.name,
        "domain": domain,
        "key_terms": list(terms)[:15],
        "authority_sources": sources,
        "crosscheck_needed": len(terms) > 0 and len(sources) > 0,
    }


if __name__ == "__main__":
    course_lib = VAULT / "10_课程库"
    reports = []
    
    for cat_dir in sorted(course_lib.iterdir()):
        if not cat_dir.is_dir(): continue
        for cd in sorted(cat_dir.iterdir()):
            if not cd.is_dir(): continue
            report = generate_crosscheck_report(cd)
            if report.get("crosscheck_needed"):
                reports.append(report)
    
    out = TOOLS_DIR / "crosscheck_sources.json"
    out.write_text(json.dumps({
        "timestamp": datetime.now().isoformat(),
        "courses": reports,
        "authority_registry": {k: [v[0] for v in vals] for k, vals in AUTHORITY_SOURCES.items()}
    }, ensure_ascii=False, indent=2), encoding='utf-8')
    
    print(f"Crosscheck report: {out}")
    print(f"Courses needing crosscheck: {len(reports)}")
