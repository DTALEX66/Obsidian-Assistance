#!/usr/bin/env python3
"""
内容匹配截图引擎 — 非随机关键帧，每张图对应具体课程概念
原理：提取课程关键术语 → 在源文件中定位匹配位置 → 截图/提取对应页面
"""

import re, subprocess
from pathlib import Path
from datetime import datetime

DISK = Path("E:/服务器")
VAULT = Path("E:/BaiduSyncdisk/Obsidian知识库/10_课程库")
ATTACH = Path("E:/BaiduSyncdisk/Obsidian知识库/99_附件_重组")

def extract_key_terms_from_summaries(course_dir: Path, top_n: int = 10) -> list:
    """从逐节总结提取关键术语（比从主页提取更准确）"""
    all_text = ''
    sd = course_dir / '03_逐节总结'
    if sd.exists():
        for f in sorted(sd.glob('*[!ASR]*.md'))[:20]:
            all_text += f.read_text(encoding='utf-8', errors='ignore')[:3000]
    
    # Also get course main page body (skip frontmatter)
    main = course_dir / '00_课程主页.md'
    if main.exists():
        parts = main.read_text(encoding='utf-8').split('---\n', 2)
        if len(parts) >= 3:
            all_text += parts[2][:5000]
    
    terms = re.findall(r'[\u4e00-\u9fff]{2,6}', all_text)
    from collections import Counter
    stop = {'可以','需要','这个','一个','什么','进行','使用','没有','已经',
            '就是','不是','我们','他们','因为','所以','如果','全部','还是',
            '什么','知道','然后','自己','其实','比较','而且','但是','可能',
            '通过','应该','问题','那么','对于','方面','来说','非常','很多'}
    counter = Counter(t for t in terms if t not in stop)
    return [t for t, _ in counter.most_common(top_n)]


def match_pdf_pages_to_terms(source_dir: Path, terms: list) -> list:
    """在 PDF 中搜索包含关键术语的页面"""
    results = []
    import fitz
    for pdf in list(source_dir.rglob('*.pdf'))[:20]:
        try:
            doc = fitz.open(pdf)
            for term in terms[:5]:
                for page_num in range(min(20, len(doc))):
                    page = doc[page_num]
                    text = page.get_text()
                    if term in text:
                        # 找到匹配！提取该页为图片
                        pix = page.get_pixmap(dpi=150)
                        img_dir = ATTACH / '内容匹配截图' / pdf.stem
                        img_dir.mkdir(parents=True, exist_ok=True)
                        img_path = img_dir / f'{term}_p{page_num+1}.png'
                        if not img_path.exists():
                            pix.save(str(img_path))
                        results.append({
                            'term': term,
                            'file': pdf.name,
                            'page': page_num + 1,
                            'image': str(img_path.relative_to(Path("E:/BaiduSyncdisk/Obsidian知识库"))),
                            'context': text[max(0, text.find(term)-50):text.find(term)+50]
                        })
            doc.close()
        except: pass
    return results


def match_video_frames_to_terms(source_dir: Path, terms: list) -> list:
    """在视频 ASR 转写中搜索术语，定位时间戳并截图"""
    results = []
    asr_dir = source_dir.parent / '03_逐节总结'  # Relative to course dir
    
    for asr_file in sorted(Path("E:/BaiduSyncdisk/Obsidian知识库/10_课程库").rglob('*ASR*.md'))[:50]:
        if asr_file.stat().st_size < 200:
            continue
        text = asr_file.read_text(encoding='utf-8')
        
        for term in terms[:5]:
            for line in text.split('\n'):
                if term in line and line.startswith('['):
                    # Parse timestamp: [120s] text...
                    ts_match = re.match(r'\[(\d+)s\]', line)
                    if ts_match:
                        ts = int(ts_match.group(1))
                        # Find the corresponding video file
                        video_stem = asr_file.stem.replace('_ASR转写', '').replace('_ASR', '')
                        for ext in ['.mp4', '.mov', '.mkv']:
                            for v in source_dir.rglob(f'*{video_stem}*{ext}'):
                                if v.exists():
                                    img_dir = ATTACH / '内容匹配截图' / '视频关键帧'
                                    img_dir.mkdir(parents=True, exist_ok=True)
                                    img_name = f'{video_stem}_{term}_{ts}s.png'
                                    img_path = img_dir / img_name
                                    if not img_path.exists():
                                        subprocess.run(['ffmpeg', '-y', '-ss', str(ts), '-i', str(v),
                                                      '-vframes', '1', '-q:v', '2', str(img_path)],
                                                     capture_output=True, timeout=30)
                                    results.append({
                                        'term': term,
                                        'timestamp': ts,
                                        'video': v.name,
                                        'image': str(img_path.relative_to(Path("E:/BaiduSyncdisk/Obsidian知识库")))
                                    })
        if len(results) >= len(terms):
            break
    
    return results


def generate_matched_screenshots(course_dir: Path) -> dict:
    """为单门课程生成内容匹配截图"""
    main = course_dir / '00_课程主页.md'
    if not main.exists():
        return {}
    
    text = main.read_text(encoding='utf-8')
    terms = extract_key_terms_from_summaries(course_dir, 8)
    print(f'  Terms: {", ".join(terms[:5])}')
    
    # Find source dir
    m = re.search(r'source_root:\s*"([^"]+)"', text)
    if not m:
        return {}
    src = Path(m.group(1))
    if not src.exists():
        return {}
    
    # Match PDF pages
    pdf_matches = match_pdf_pages_to_terms(src, terms)
    
    # Match video frames
    video_matches = match_video_frames_to_terms(src, terms)
    
    # Update course visual index
    visual = course_dir / '12_视觉索引与配图.md'
    existing = visual.read_text(encoding='utf-8') if visual.exists() else ''
    
    if pdf_matches or video_matches:
        new_content = '\n\n## 内容匹配截图\n'
        for m in pdf_matches[:5]:
            new_content += f'\n### {m["term"]}\n'
            new_content += f'> {m["file"]} p{m["page"]} — {m["context"][:80]}...\n'
            new_content += f'![[{m["image"]}]]\n'
        for m in video_matches[:5]:
            new_content += f'\n### {m["term"]} ({m["timestamp"]}s)\n'
            new_content += f'> {m["video"]}\n'
            new_content += f'![[{m["image"]}]]\n'
        
        if new_content not in existing:
            visual.write_text(existing.strip() + new_content, encoding='utf-8')
    
    return {
        'course': course_dir.name,
        'terms': terms[:5],
        'pdf_matches': pdf_matches[:5],
        'video_matches': video_matches[:5]
    }


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        # Single course
        course_id = sys.argv[1]
        for cat in VAULT.iterdir():
            cd = cat / course_id
            if cd.exists():
                result = generate_matched_screenshots(cd)
                print(f'Done: {len(result.get("pdf_matches",[]))+len(result.get("video_matches",[]))} matches')
    else:
        print('Usage: python content_keyframes.py C0401')
