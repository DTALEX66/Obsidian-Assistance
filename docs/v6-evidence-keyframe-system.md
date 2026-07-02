# V6 Evidence & Keyframe System

> Goal: turn the Obsidian course vault from a text/usage-layer KnowledgeOS into a source-backed, multimodal evidence system. This design is intentionally conservative: candidates are not evidence, screenshots/keyframes must come from real local source files, and the formal vault remains local-only.

## Scope

V6 focuses on verifiable media evidence for existing courses:

- PDF page snapshots
- video keyframe extraction plans
- evidence metadata sidecars
- course-level evidence index notes
- visual-index back-links
- Talos dashboard metrics

It does **not** upload the formal vault, copy source course files into the helper repo, or fabricate images.

## Safety boundary

| Rule | Requirement |
|---|---|
| Real source only | A snapshot/keyframe must come from a local PDF/video/image/courseware file. |
| Candidate != evidence | Path/name matches from `source_candidate_audit.py` stay unverified until the file is opened and page/time is recorded. |
| Dry-run first | Tools default to dry-run and only write with `--apply`. |
| No source copying | Never copy original PDFs/videos into the helper repo. |
| Vault-local media | Extracted images go into the formal vault attachment area, e.g. `99_附件/images/<course>/`. |
| Metadata required | Every image needs a JSON sidecar or Markdown row with source path, source type, page/time, extractor, and confidence. |
| Confidence visible | Uncertain items stay `pending-verification`, not silently promoted. |
| No destructive operations | No deleting, moving, or overwriting course source/body notes. |

## Evidence metadata schema

Each extracted evidence item should follow this conceptual schema:

```yaml
evidence_id: course-slug-pdf-p001-001
course: 课程名
source_type: pdf|video|image|web|note
source_path: E:/...
source_ref:
  page: 1
  timestamp: null
  frame_index: null
output_path: 99_附件/images/<course>/course-slug-p001.png
caption: 待填写的图片说明
confidence: A|B|C|D
status: verified|pending-verification|candidate-only
created: YYYY-MM-DD
extractor: scripts/v6/pdf_page_snapshot.py
notes: []
```

Confidence levels:

| Level | Meaning |
|---|---|
| A | Local source opened; page/time recorded; image extracted; course relation verified. |
| B | Local source opened and likely related, but content/page requires later human review. |
| C | Filename/path candidate only; no page/time content verification. |
| D | Ambiguous or low-quality source; keep as pending. |

## Course-level files

For a fully upgraded course, V6 can add:

```text
11_证据索引.md
12_真实截图与关键帧.md
```

`11_证据索引.md` records evidence rows.  
`12_真实截图与关键帧.md` embeds real images with metadata and links back to source refs.

## Tool roadmap

| Tool | Purpose | Default |
|---|---|---|
| `scripts/v6/pdf_page_snapshot.py` | Render selected PDF pages into image files and metadata sidecars. | dry-run |
| `scripts/v6/video_keyframe_plan.py` | Generate timestamp extraction plans without copying videos. | dry-run |
| `scripts/v6/evidence_index_builder.py` | Build `11_证据索引.md` and `12_真实截图与关键帧.md` from metadata sidecars. | dry-run |
| `scripts/v6/visual_index_updater.py` | Link verified evidence images into `04_关键图表与课件索引.md`. | dry-run |
| `scripts/v6/vault_health_radar.py` | Track multimodal evidence health by course. | read-only |

## Minimal V6 pilot

1. Pick one existing course with a real local PDF/video candidate.
2. Open/verify the source locally.
3. Extract one PDF page snapshot or one video keyframe.
4. Save under `99_附件/images/<course>/`.
5. Write metadata sidecar.
6. Generate or update `11_证据索引.md` and `12_真实截图与关键帧.md`.
7. Re-run image evidence audit.
8. Commit formal vault locally only.

## Anti-goals

- No internet images as fake course screenshots.
- No copying real vault notes/media into the helper repo.
- No treating OCR snippets or filename matches as verified evidence.
- No mass rewriting course body notes.

## Verification gates

Helper repo gates:

```bash
python -m py_compile scripts/*.py scripts/v4/*.py scripts/v5/*.py scripts/v6/*.py pytest.py
python -m pytest tests -q
python scripts/v4/obsidian_v4_audit.py .
```

Formal vault gates are local-only:

- Markdown fences balanced
- evidence metadata JSON parses
- image paths exist
- course links resolve
- Git status clean after local commit
