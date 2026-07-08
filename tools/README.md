# Obsidian-Assistance 转化工具集

## 工具清单

| 工具 | 文件 | 用途 | 精确度 | 状态 |
|---|---|---|---|---|
| **FunASR SenseVoice** | pip install | 中文视频/音频 ASR | 92%+ (CER 8%) | ✅ |
| **PaddleOCR** | pip install | 中文扫描PDF/图片 OCR | 90-95% | ✅ |
| **pymupdf** | pip install | PDF 文字提取 | 98% | ✅ |
| **Tesseract** | scoop install | 备用 OCR | 70-80% | ✅ |
| **LibreOffice Portable** | LibreOfficePortable.paf.exe | DOC/DOCX/PPT 全格式 | 85-95% | ⏳ 下载中 |
| **faster-whisper** | pip install | 备用 ASR | 80% | ✅ |

## 安装

```bash
cd tools
pip install -r requirements.txt
```

LibreOffice Portable 双击 `LibreOfficePortable.paf.exe` 解压到当前目录即可，无需安装。

## 精确度标准

见 `ACCURACY_STANDARDS.md`

## 运行

```bash
# 基准测试
python benchmark_accuracy.py

# 交叉验证
python crosscheck_accuracy.py
```
