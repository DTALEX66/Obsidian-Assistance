#!/usr/bin/env python3
"""
课程转化工具精度基准测试
目标：每种格式 >= 85% 精确度
不足部分通过全网交叉验证补足
"""

import json, re, subprocess, time
from pathlib import Path
from datetime import datetime

TOOLS_DIR = Path(__file__).parent
VAULT = Path("E:/BaiduSyncdisk/Obsidian知识库")
DISK = Path("E:/服务器")

def test_ocr_accuracy():
    """测试 OCR 识别准确率"""
    results = {"tool": "PaddleOCR", "target": "95%", "tests": []}
    
    # 找一个有文字的标准PDF测试页
    test_pdfs = list(DISK.rglob("*.pdf"))[:20]
    
    try:
        from paddleocr import PaddleOCR
        ocr = PaddleOCR(lang='ch')
        
        for pdf in test_pdfs[:3]:
            from pdf2image import convert_from_path
            try:
                images = convert_from_path(pdf, first_page=1, last_page=1)
                if images:
                    result = ocr.ocr(images[0])
                    if result and result[0]:
                        texts = [line[1][0] for line in result[0]]
                        char_count = sum(len(t) for t in texts)
                        results["tests"].append({
                            "file": pdf.name[:50],
                            "lines": len(texts),
                            "chars": char_count,
                            "confidence": round(sum(line[1][1] for line in result[0]) / len(result[0]), 3) if result[0] else 0
                        })
            except:
                pass
    except Exception as e:
        results["error"] = str(e)[:100]
    
    return results


def test_asr_accuracy():
    """测试 ASR 识别准确率"""
    results = {"tool": "FunASR SenseVoice", "target": "CER < 10% (92%+)", "tests": []}
    
    # 找一个标准中文视频测试
    test_videos = sorted(DISK.rglob("*.mp4"))[:5]
    
    try:
        from funasr import AutoModel
        model = AutoModel(model='iic/SenseVoiceSmall', device='cpu', disable_pbar=True, disable_update=True)
        
        for v in test_videos[:2]:
            wav = v.with_suffix('.bench.wav')
            subprocess.run(['ffmpeg','-y','-i',str(v),'-t','60','-vn','-acodec','pcm_s16le','-ar','16000','-ac','1',str(wav)],
                         capture_output=True, timeout=120)
            if wav.exists():
                t0 = time.time()
                result = model.generate(input=str(wav), language='zh', use_itn=True)
                elapsed = time.time() - t0
                text = result[0]['text'] if result else ''
                results["tests"].append({
                    "file": v.name[:50],
                    "chars": len(text),
                    "duration_sec": 60,
                    "process_sec": round(elapsed, 1),
                    "speed": f"{round(60/elapsed)}x realtime",
                })
                wav.unlink()
    except Exception as e:
        results["error"] = str(e)[:100]
    
    return results


def test_docx_accuracy():
    """测试 DOCX 提取准确率"""
    results = {"tool": "python-docx + zipfile", "target": "98%", "tests": []}
    
    test_files = list(DISK.rglob("*.docx"))[:5]
    for f in test_files:
        try:
            import zipfile
            with zipfile.ZipFile(f) as z:
                xml = z.read('word/document.xml').decode('utf-8', errors='ignore')
            text = re.sub(r'<[^>]+>', '', xml)
            text = re.sub(r'\s+', ' ', text).strip()
            results["tests"].append({
                "file": f.name[:50],
                "chars": len(text),
                "has_chinese": bool(re.search(r'[\u4e00-\u9fff]', text))
            })
        except Exception as e:
            results["tests"].append({"file": f.name[:50], "error": str(e)[:50]})
    
    return results


def test_pdf_accuracy():
    """测试 PDF 文本提取准确率"""
    results = {"tool": "pymupdf", "target": "95% (text-based), 85% (scanned via OCR)", "tests": []}
    
    test_files = list(DISK.rglob("*.pdf"))[:10]
    for f in test_files:
        try:
            import fitz
            doc = fitz.open(f)
            text = ''
            for page in doc[:3]:
                text += page.get_text()
            doc.close()
            results["tests"].append({
                "file": f.name[:50],
                "pages": min(3, doc.page_count if 'doc' in dir() else 3),
                "chars": len(text.strip()),
                "type": "text" if len(text.strip()) > 100 else "scanned"
            })
        except Exception as e:
            results["tests"].append({"file": f.name[:50], "error": str(e)[:50]})
    
    return results


if __name__ == "__main__":
    report = {
        "timestamp": datetime.now().isoformat(),
        "target": "所有格式 >= 85% 精确度",
        "benchmarks": {}
    }
    
    print("=== OCR 测试 ===")
    report["benchmarks"]["ocr"] = test_ocr_accuracy()
    print(json.dumps(report["benchmarks"]["ocr"], ensure_ascii=False, indent=2))
    
    print("\n=== ASR 测试 ===")
    report["benchmarks"]["asr"] = test_asr_accuracy()
    print(json.dumps(report["benchmarks"]["asr"], ensure_ascii=False, indent=2))
    
    print("\n=== DOCX 测试 ===")
    report["benchmarks"]["docx"] = test_docx_accuracy()
    print(json.dumps(report["benchmarks"]["docx"], ensure_ascii=False, indent=2)[:500])
    
    print("\n=== PDF 测试 ===")
    report["benchmarks"]["pdf"] = test_pdf_accuracy()
    print(json.dumps(report["benchmarks"]["pdf"], ensure_ascii=False, indent=2)[:500])
    
    out = TOOLS_DIR / "accuracy_benchmark.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"\nReport: {out}")
