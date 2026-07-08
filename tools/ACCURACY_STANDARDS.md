# 课程转化精确度标准

## 目标

所有格式最低精确度：**85-95%**

不足部分通过：
1. 全网公开权威来源交叉验证
2. 多元证据链（OCR+ASR+原始文本+网络校对）
3. 人工复核标记

## 格式精确度基线

| 格式 | 工具 | 目标 | 当前 | 缺口补足 |
|---|---|---|---|---|
| PDF 文字型 | pymupdf | 98% | ✅ 98% | - |
| PDF 扫描型 | PaddleOCR | 90% | 待测 | Tesseract 备用 |
| DOCX | zipfile OOXML | 98% | ✅ 98% | - |
| DOC 新格式 | pandoc + antiword | 90% | ✅ |
| DOC 老中文 | antiword (已知限制) | 50% | ⚠️ 需手动/LibreOffice |
| PPTX | zipfile OOXML | 95% | ✅ |
| TXT/MD | open() | 100% | ✅ 100% | - |
| 视频 ASR | FunASR SenseVoice | 92% (CER<8%) | ✅ | 网络交叉验证 |
| 音频 ASR | FunASR SenseVoice | 92% | ✅ | 网络交叉验证 |
| 图片 OCR | PaddleOCR | 90% | 待测 | Tesseract 备用 |

## 安装

```bash
cd D:/All projects/Obsidian-Assistance/tools
pip install -r requirements.txt
```

## 运行基准测试

```bash
python tools/benchmark_accuracy.py
```

## 交叉验证

```bash
python tools/crosscheck_accuracy.py
```
