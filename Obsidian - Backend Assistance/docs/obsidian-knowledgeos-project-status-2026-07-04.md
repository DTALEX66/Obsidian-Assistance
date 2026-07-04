# Obsidian KnowledgeOS Project Status (2026-07-04)

This is a sanitized public status snapshot for the helper repository. It summarizes architecture, toolchain, and progress **without uploading the private Obsidian vault or course materials**.

## Boundary

The formal Obsidian vault remains local-only. This repository contains reusable tools, standards, process notes, templates, and sanitized design/project documentation.

## Current High-Level Metrics

| Metric | Count |
|---|---:|
| Formal course portals in private vault | 30 |
| Courses with visual index pages | 29 |
| Courses with verified screenshots/keyframes/PDF page samples | 16 |
| Courses with project-conversion pages | 30 |
| Courses with OER crosswalk pages | 4 |

## Completed Capability Layers

| Layer | Status | Public Repo Scope |
|---|---|---|
| V4 course pack generator | Implemented | Scripts, tests, templates, demo-safe examples. |
| V5 course diversity and visual standards | Implemented | Audit/generator standards and documentation. |
| V6 evidence/keyframe system | Implemented | Evidence toolchain documentation and reusable scripts. |
| V7 course-to-project conversion | Implemented | Generator scripts and public-safe workflow notes. |
| V8 active training / daily mission loop | Implemented | Daily mission, streak, retro tooling. |
| V9 OER crosswalk generator | Implemented | OER comparison generator and tests. |
| TALOS Purple Gemstone UI handoff | Added | Public/sanitized UI/UX design handoff document. |

## Recent Private-Vault Work Summarized Publicly

- Formal course pages were upgraded away from pure text toward visual/evidence-aware pages.
- Visual coverage counting was corrected: only actual image embeds count as visuals; path mentions are candidate references only.
- Reference images are explicitly separated from verified evidence.
- Verified evidence pages record source type, page/time metadata, and visual-check status.
- TALOS Home Console, course reader, evidence matrix, project Kanban, review center, plugin component QA, and pixel-parity QA were expanded.
- UI/UX handoff was extracted for a designer as a standalone brief.

## Latest Private Vault Commit References

These hashes are only local-vault references and do not expose private file contents.

```text
8e78927 docs: 提取TALOS UI交互设计交接包
c84f47e auto: 2026-07-04 07:56:37
472b14c feat: 睡觉模式升级PDF源页图
b8f8a29 feat: 睡觉模式升级学习运营真实关键帧
db0186d feat: 睡觉模式升级设计课程真实关键帧
f6e0592 feat: 睡觉模式升级更多真实关键帧
ba79f57 feat: 睡觉模式强化紫晶像素一致性
6418197 feat: 睡觉模式补充GitHub源截图
```

## What Is Intentionally Not Uploaded

- Private vault notes.
- `.obsidian/` runtime configuration.
- Course videos, PDFs, audio, screenshots, and generated attachments.
- Full derived text outputs and private course summaries.
- Personal paths, credentials, API keys, tokens, cookies, local sync state.

## Next Public-Repo Candidates

1. Add a reusable TALOS UI implementation checklist from the design handoff.
2. Add CSS-token documentation separate from private vault snippets.
3. Add demo-only mock pages that do not contain real course content.
4. Add CI checks for forbidden path/media/secret patterns in future documentation uploads.
