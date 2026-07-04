# V5 20-Round Course Repair Loop Summary

> Sanitized helper-repo summary. This document records reusable process, scripts, and safety rules only. It does **not** copy formal vault notes, source materials, transcripts, screenshots, OCR text, media, or private Obsidian configs.

## Goal

Upgrade an existing Obsidian course library that had become too text-heavy. The loop repaired the **usage layer** of the first 20 formal courses without starting new courses or rewriting the original course bodies.

## Safety boundary

- Do not create new courses.
- Do not delete or move course source/body notes.
- Do not upload the real vault to GitHub.
- Do not fabricate screenshots, images, keyframes, or evidence.
- Treat filename/path matches as **unverified candidates**, not evidence.
- Formal vault changes are local-only commits.
- Helper repo changes go through branch → tests/audit → PR → CI → squash merge.

## Final coverage achieved in the formal vault

The formal vault run reached these measurable outcomes:

| Area | Result |
|---|---:|
| Formal courses in scope | 20 |
| V5 learning-layer coverage | 20/20 |
| Independent review cards | 60 |
| Review-card course coverage | 20/20 |
| Keyframe collection task notes | 20/20 |
| Final structural issues | 0 |
| Remaining hard gap | real images/keyframes |

The remaining real gap is intentional: real screenshots/keyframes require opening local source videos/PDF/courseware, recording page/time evidence, then extracting images. The loop explicitly avoided placeholder or fake image embeds.

## Reusable loop sequence

1. Audit the course library with `scripts/v5/course_diversity_audit.py`.
2. If courses are thin/text-heavy, generate V5 usage-layer supplements:
   - `02_课程地图.canvas`
   - `04_关键图表与课件索引.md`
   - `05_复习与检索练习.md`
   - `06_验证与不确定项.md`
3. Add links from each course overview into those usage-layer pages.
4. Generate independent active-recall review cards with `scripts/v5/generate_course_review_cards.py`.
5. Generate keyframe collection task notes with `scripts/v5/generate_keyframe_tasks.py`.
6. Audit real image evidence with `scripts/v5/course_image_evidence_audit.py`.
7. Scan local source-file candidates with `scripts/v5/source_candidate_audit.py`.
8. Backfill only **unverified candidate** source links into task notes; never treat them as evidence.
9. Re-run structural checks:
   - Markdown fences balanced
   - Canvas JSON valid
   - review cards have frontmatter, review tasks, and evidence boundary text
   - every in-scope course has the required V5 usage-layer files
10. Commit the formal vault locally; PR helper-repo scripts/tests separately.

## Helper scripts added during the loop

| Script | Purpose |
|---|---|
| `scripts/v5/generate_course_review_cards.py` | Dry-run/apply generator for independent active-recall course cards. |
| `scripts/v5/generate_keyframe_tasks.py` | Dry-run/apply generator for course keyframe collection task notes. |
| `scripts/v5/source_candidate_audit.py` | Conservative local filename/path scanner for unverified source candidates. |

Existing scripts used heavily:

| Script | Purpose |
|---|---|
| `scripts/v5/course_diversity_audit.py` | Measures course modality diversity: tables, Mermaid, Dataview, tasks, callouts, Canvas, review questions, source/evidence, action items. |
| `scripts/v5/course_image_evidence_audit.py` | Counts only real vault images or existing image embeds; does not fabricate missing images. |
| `scripts/v4/obsidian_v4_audit.py` | Helper-repo safety audit. |

## Quality lesson: candidate cards need quality checks

A first review-card batch accidentally used frontmatter-like strings as card questions. The repair rule is now:

- Reject card titles that start with `type:`, `status:`, `course:`, or contain generated filename fragments like `type_` / `status_`.
- Every card must include:
  - YAML frontmatter
  - `## 正面`
  - `## 背面`
  - `## 来源与边界`
  - at least three review checklist items
  - boundary text: the card is an active-recall candidate and does not add course facts.

## Evidence boundary for source candidates

`source_candidate_audit.py` can find likely files by matching course names against local paths, but the output is only a triage list. A candidate becomes evidence only after a later step opens the file and records one of:

- PDF page number
- video timestamp
- slide/page identifier
- screenshot/keyframe filename under the vault attachment directory

## Verification commands

Helper repo:

```bash
cd "D:/All projects/Obsidian-Assistance/github/Obsidian-Assistance"
python -m py_compile scripts/*.py scripts/v4/*.py scripts/v5/*.py pytest.py
python -m pytest tests -q
python scripts/v4/obsidian_v4_audit.py .
```

Formal vault structural checks are intentionally local-only and should not upload vault content.

## What not to do next

- Do not push the real Obsidian vault to GitHub.
- Do not add placeholder `![[fake.png]]` links to improve scores.
- Do not copy local videos/PDFs/courseware into the helper repo.
- Do not treat source-file candidates as verified evidence.

## Next real upgrade

The only valuable next step is source-backed media enrichment:

1. Open local course videos/PDF/courseware.
2. Record page/time evidence.
3. Extract a real keyframe or page screenshot.
4. Save it under the vault attachment area.
5. Link it from the course visual index with source metadata.
6. Re-run image evidence audit.
