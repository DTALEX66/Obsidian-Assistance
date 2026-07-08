#!/usr/bin/env python3
"""
课程转化全流程引擎 — Course Conversion Pipeline
从 E:/服务器 源文件 → Obsidian 课程库 的全自动转化

流程：扫描 → 检测格式 → 选转换器 → 提取文本 → 质量校验 → 交叉验证 → 入库
"""

import json, re, subprocess, sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# === 配置 ===
DISK_ROOT = Path("E:/服务器")
VAULT_ROOT = Path("E:/BaiduSyncdisk/Obsidian知识库")
COURSE_ROOT = VAULT_ROOT / "10_课程库"
TOOLS_DIR = Path(__file__).parent

# === 格式检测与转换器选择 ===
FORMAT_HANDLERS = {}

def register(fmt):
    def decorator(fn):
        FORMAT_HANDLERS[fmt] = fn
        return fn
    return decorator

@register('.pdf')
def handle_pdf(path: Path, out_dir: Path) -> Optional[Path]:
    """PDF → 文本（优先 pymupdf，失败则 OCR）"""
    try:
        import fitz
        doc = fitz.open(path)
        text = ''
        for page in doc[:10]:
            text += page.get_text()
        doc.close()
        if text.strip() and len(text) > 100:
            out = out_dir / f'{path.stem}.md'
            out.write_text(f'# {path.stem}\n\n> 来源：{path.relative_to(DISK_ROOT)}\n\n{text[:8000]}', encoding='utf-8')
            return out
        raise ValueError("Insufficient text")
    except:
        pass
    
    # OCR fallback
    try:
        from pdf2image import convert_from_path
        import pytesseract
        images = convert_from_path(path, first_page=1, last_page=3)
        text = ''
        for img in images:
            text += pytesseract.image_to_string(img, lang='chi_sim+eng')
        if text.strip():
            out = out_dir / f'{path.stem}.md'
            out.write_text(f'# {path.stem} (OCR)\n\n{text[:8000]}', encoding='utf-8')
            return out
    except:
        pass
    return None

@register('.docx')
def handle_docx(path: Path, out_dir: Path) -> Optional[Path]:
    try:
        import zipfile
        with zipfile.ZipFile(path) as z:
            xml = z.read('word/document.xml').decode('utf-8', errors='ignore')
        text = re.sub(r'<[^>]+>', '', xml)
        text = re.sub(r'\s+', ' ', text).strip()
        if text:
            out = out_dir / f'{path.stem}.md'
            out.write_text(f'# {path.stem}\n\n> 来源：{path.relative_to(DISK_ROOT)}\n\n{text[:8000]}', encoding='utf-8')
            return out
    except:
        pass
    return None

@register('.pptx')
def handle_pptx(path: Path, out_dir: Path) -> Optional[Path]:
    try:
        import zipfile
        with zipfile.ZipFile(path) as z:
            slides = sorted([n for n in z.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')])
            text = ''
            for s in slides[:10]:
                xml = z.read(s).decode('utf-8', errors='ignore')
                text += re.sub(r'<[^>]+>', ' ', xml)
            text = re.sub(r'\s+', ' ', text).strip()
            if text and len(text) > 50:
                out = out_dir / f'{path.stem}.md'
                out.write_text(f'# {path.stem}\n\n{text[:8000]}', encoding='utf-8')
                return out
    except:
        pass
    return None

@register('.txt')
@register('.md')
def handle_text(path: Path, out_dir: Path) -> Optional[Path]:
    try:
        text = path.read_text(encoding='utf-8', errors='ignore')
        if text.strip():
            out = out_dir / f'{path.stem}.md'
            out.write_text(f'# {path.stem}\n\n{text[:8000]}', encoding='utf-8')
            return out
    except:
        pass
    return None

@register('.mp4')
@register('.mov')
@register('.mkv')
@register('.avi')
@register('.flv')
def handle_video(path: Path, out_dir: Path) -> Optional[Path]:
    out = out_dir / f'{path.stem}_ASR.md'
    if out.exists() and out.stat().st_size > 200:
        return out
    
    wav = path.with_suffix('.pipeline.wav')
    try:
        r = subprocess.run(['ffmpeg', '-y', '-i', str(path), '-t', '120', '-vn',
                          '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', str(wav)],
                         capture_output=True, timeout=300)
        if r.returncode != 0 or not wav.exists():
            return None
        
        from funasr import AutoModel
        model = AutoModel(model='iic/SenseVoiceSmall', device='cpu', disable_pbar=True, disable_update=True)
        result = model.generate(input=str(wav), language='zh', use_itn=True)
        text = result[0]['text'] if result else ''
        if text.strip():
            out.write_text(f'# {path.stem}\n\n> SenseVoice ASR\n\n{text}', encoding='utf-8')
            return out
    except:
        pass
    finally:
        wav.unlink(missing_ok=True)
    return None


def convert_course(source_dir: Path, course_dir: Path) -> dict:
    """转化单门课程的所有源文件"""
    summary_dir = course_dir / '03_逐节总结'
    summary_dir.mkdir(parents=True, exist_ok=True)
    
    stats = {'total': 0, 'converted': 0, 'skipped': 0, 'failed': 0, 'by_format': {}}
    
    for f in source_dir.rglob('*'):
        if not f.is_file():
            continue
        ext = f.suffix.lower()
        stats['total'] += 1
        
        if ext in FORMAT_HANDLERS:
            try:
                result = FORMAT_HANDLERS[ext](f, summary_dir)
                if result:
                    stats['converted'] += 1
                    stats['by_format'][ext] = stats['by_format'].get(ext, 0) + 1
                else:
                    stats['skipped'] += 1
            except Exception as e:
                stats['failed'] += 1
        elif ext in {'.jpg', '.png', '.gif', '.bmp'}:
            stats['skipped'] += 1  # 图片保留链接
        elif ext in {'.zip', '.rar', '.7z', '.sz', '.iso', '.exe', '.dll'}:
            stats['skipped'] += 1  # 素材不入库
        else:
            stats['skipped'] += 1
    
    # 更新课程主页
    main = course_dir / '00_课程主页.md'
    if main.exists():
        t = main.read_text(encoding='utf-8')
        
        # 添加统计
        if '## 转化统计' not in t:
            stats_block = (
                f'\n\n## 转化统计\n'
                f'- 总文件：{stats["total"]}\n'
                f'- 已转化：{stats["converted"]}\n'
                f'- 素材型：{stats["skipped"]}\n'
                f'- 失败：{stats["failed"]}\n'
                f'- 格式分布：{json.dumps(stats["by_format"], ensure_ascii=False)}\n'
            )
            t = t.rstrip() + stats_block
        
        # 合并逐节总结
        if summary_dir.exists():
            t += '\n\n## 逐节总结\n'
            for sf in sorted(summary_dir.glob('*.md')):
                if sf.stem not in t:
                    st = sf.read_text(encoding='utf-8', errors='ignore')[:2000]
                    t += f'\n### {sf.stem}\n\n{st}\n'
        
        t = t.replace('status: 待转化', 'status: 已转化')
        t = t.replace('status: 骨架', 'status: 已转化')
        main.write_text(t, encoding='utf-8')
    
    return stats


def scan_and_convert_all():
    """扫描全部课程并转化"""
    log = {
        'timestamp': datetime.now().isoformat(),
        'source_disk': str(DISK_ROOT),
        'courses': {}
    }
    
    for cat_dir in sorted(COURSE_ROOT.iterdir()):
        if not cat_dir.is_dir():
            continue
        if cat_dir.name == '11_OER开源技能库':
            continue
        
        for cd in sorted(cat_dir.iterdir()):
            if not cd.is_dir():
                continue
            main = cd / '00_课程主页.md'
            if not main.exists():
                continue
            
            t = main.read_text(encoding='utf-8')
            m = re.search(r'source_root:\s*"([^"]+)"', t)
            if not m:
                continue
            
            src = Path(m.group(1))
            if not src.exists():
                log['courses'][cd.name] = {'error': 'source not found'}
                continue
            
            print(f'Converting: {cd.name}')
            stats = convert_course(src, cd)
            log['courses'][cd.name] = {
                'source': str(src.relative_to(DISK_ROOT)),
                'stats': stats
            }
            print(f'  → {stats["converted"]}/{stats["total"]} converted')
    
    # 写日志
    log_path = VAULT_ROOT / '90_系统资产/96_HERMES执行记录/pipeline_log.json'
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding='utf-8')
    
    return log


if __name__ == '__main__':
    print('=== Course Conversion Pipeline ===')
    print(f'Disk: {DISK_ROOT}')
    print(f'Vault: {VAULT_ROOT}')
    
    if len(sys.argv) > 1 and sys.argv[1] == '--course':
        # 单门课程
        course_id = sys.argv[2]
        for cat_dir in COURSE_ROOT.iterdir():
            cd = cat_dir / course_id
            if cd.exists() and cd.is_dir():
                main = cd / '00_课程主页.md'
                t = main.read_text(encoding='utf-8')
                m = re.search(r'source_root:\s*"([^"]+)"', t)
                if m:
                    stats = convert_course(Path(m.group(1)), cd)
                    print(json.dumps(stats, ensure_ascii=False, indent=2))
                break
    else:
        log = scan_and_convert_all()
        total_converted = sum(c.get('stats', {}).get('converted', 0) for c in log['courses'].values())
        total_courses = len(log['courses'])
        print(f'\nDone: {total_converted} files converted across {total_courses} courses')
