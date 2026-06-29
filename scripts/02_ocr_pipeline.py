#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
课程 OCR 流水线 v1.0
功能：PDF -> 图片 -> OCR -> JSON 输出
前置：poppler (pdftoppm), tesseract, pytesseract
用法：
  python 02_ocr_pipeline.py --source-dir "课程目录" --output-dir "outputs"
"""

import os, sys, json, hashlib, subprocess, argparse, time
from pathlib import Path

try:
    from PIL import Image
    import pytesseract
except ImportError:
    print("请先安装依赖: pip install Pillow pytesseract")
    sys.exit(1)

PDFTOPPM_CANDIDATES = [
    r"C:UsersALEX.cachecodex-runtimescodex-primary-runtimedependencies
ativepopplerLibraryinpdftoppm.exe",
    "pdftoppm", "pdftoppm.exe"
]

def find_pdftoppm():
    for c in PDFTOPPM_CANDIDATES:
        try:
            subprocess.run([c, "--version"], capture_output=True, timeout=5)
            return c
        except Exception:
            pass
    return None

def pdf_to_images(pdf_path, output_dir, dpi=300):
    exe = find_pdftoppm()
    if not exe:
        return {"status": "ERROR", "error": "pdftoppm not found"}
    stem = Path(pdf_path).stem
    page_dir = Path(output_dir) / "pdf_pages" / stem
    page_dir.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run([exe, "-png", "-r", str(dpi), str(pdf_path),
                        str(page_dir / stem)], check=True, capture_output=True, timeout=300)
        images = sorted(page_dir.glob(f"{stem}-*.png"))
        return {"status": "OK", "pages": len(images), "images": [str(p) for p in images]}
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode("utf-8", errors="ignore")[:200]
        return {"status": "ERROR", "error": f"pdftoppm failed: {err}"}
    except subprocess.TimeoutExpired:
        return {"status": "ERROR", "error": "pdftoppm timeout (>300s)"}

def ocr_image(img_path, lang="chi_sim+eng"):
    try:
        img = Image.open(img_path)
        w, h = img.size
        if h > w * 8:
            chunk_h = h // 8
            texts = []
            for i in range(8):
                box = (0, i * chunk_h, w, min((i+1) * chunk_h, h))
                texts.append(pytesseract.image_to_string(img.crop(box), lang=lang))
            return {"status": "OK", "text": "\n".join(texts), "method": "split8"}
        else:
            text = pytesseract.image_to_string(img, lang=lang)
            return {"status": "OK", "text": text, "method": "direct"}
    except Exception as e:
        return {"status": "ERROR", "error": str(e)[:200]}

def main():
    parser = argparse.ArgumentParser(description="课程 OCR 流水线")
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--output-dir", default="outputs")
    parser.add_argument("--lang", default="chi_sim+eng")
    parser.add_argument("--dpi", type=int, default=300)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    src = Path(args.source_dir)
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    pdfs = list(src.rglob("*.pdf"))
    print(f"找到 {len(pdfs)} 个 PDF 文件")

    result_file = out / "ocr_results.json"
    results = {}
    if args.resume and result_file.exists():
        with open(result_file, "r", encoding="utf-8") as f:
            results = json.load(f)
        print(f"已加载 {len(results)} 个已有结果")

    for pdf in pdfs:
        rel = pdf.relative_to(src)
        key = str(rel)
        if key in results:
            print(f"  [SKIP] {rel}")
            continue

        print(f"  [OCR]  {rel} ...", end=" ", flush=True)
        t0 = time.time()

        sha = hashlib.sha256()
        with open(pdf, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                sha.update(chunk)
        sha256 = sha.hexdigest()

        pages = pdf_to_images(pdf, out, dpi=args.dpi)
        if pages["status"] != "OK":
            results[key] = {
                "file": str(pdf), "sha256": sha256, "size_bytes": pdf.stat().st_size,
                "pdf_to_images": pages, "ocr_pages": [], "status": "PDF_CONVERT_FAILED"
            }
            print("PDF 转换失败")
            continue

        ocr_pages = []
        full_text = []
        for i, img_path in enumerate(pages["images"]):
            ocr = ocr_image(img_path, lang=args.lang)
            ocr_pages.append({
                "page": i + 1, "image": img_path,
                "status": ocr["status"],
                "method": ocr.get("method", "direct"),
                "char_count": len(ocr.get("text", "")),
                "error": ocr.get("error", "")
            })
            if ocr["status"] == "OK":
                full_text.append(ocr["text"])

        elapsed = time.time() - t0
        results[key] = {
            "file": str(pdf), "sha256": sha256, "size_bytes": pdf.stat().st_size,
            "pdf_to_images": pages, "ocr_pages": ocr_pages,
            "total_chars": sum(len(t) for t in full_text),
            "status": "OK" if len(full_text) > 0 else "ALL_OCR_FAILED",
            "elapsed_seconds": round(elapsed, 1)
        }
        print(f"OK ({results[key]['total_chars']} chars, {elapsed:.1f}s)")

        if len(results) % 3 == 0:
            with open(result_file, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    ok = sum(1 for v in results.values() if v["status"] == "OK")
    failed = sum(1 for v in results.values() if v["status"] != "OK")
    total_chars = sum(v.get("total_chars", 0) for v in results.values())
    print(f"\n完成: OK={ok}, 失败={failed}, 总字符={total_chars}")

if __name__ == "__main__":
    main()
