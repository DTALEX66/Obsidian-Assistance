---
name: course-verifier
description: Local-first course evidence retrieval, comparison, and verification for Obsidian knowledge-base ingestion. Use when processing courses, validating uncertain course terms, comparing OCR/ASR/text/web evidence, deciding whether online search is needed, or preparing final Obsidian-ready course summaries without hallucinated details.
---

# Course Verifier

Use this skill before finalizing course summaries, term indexes, workflows, knowledge cards, or review cards.

## Rules

1. Prefer local evidence before web evidence.
2. Treat extracted course materials as primary sources: ASR transcripts, OCR text, PDFs converted to text, screenshots, Markdown notes, and cached source pages.
3. Use online search only when local evidence is missing or contradictory.
4. Never invent exact formulas, workflows, names, awards, rankings, UI button positions, or diagram details from filenames.
5. Exclude non-course-mainline content such as prizes, award lists, activity decoration, marketing copy, and ceremonial display unless the user explicitly asks to preserve it.
6. Write formal Obsidian notes only after evidence status is clear.

## Workflow

Build or refresh a local evidence index:

```powershell
python scripts/course_verify.py --root "path/to/project" build
```

Query uncertain terms:

```powershell
python scripts/course_verify.py --root "path/to/project" query --q "121工作流"
```

Verify multiple terms and generate a report:

```powershell
python scripts/course_verify.py --root "path/to/project" verify --terms "121工作流,卡片指数,个人成长速度"
```

## Decisions

- `confirmed`: enough local or cached source evidence.
- `single_source`: usable, but write conservatively.
- `needs_web`: local evidence is insufficient; search online or ask for source material.
- `exclude`: irrelevant to the course knowledge system.

When online sources are used, save only source metadata, URLs, and short evidence snippets into project outputs. Do not mirror whole copyrighted pages into the vault or this repository.

