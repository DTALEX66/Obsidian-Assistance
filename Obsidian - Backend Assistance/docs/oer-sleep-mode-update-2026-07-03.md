# OER Sleep Mode Update — 2026-07-03

> Sanitized helper-repo update. This document records reusable workflow changes and aggregate metrics only. It does **not** copy the formal Obsidian vault, private notes, course source material, screenshots, transcripts, OCR output, plugin configs, or synced-drive internals.

## Summary

This update captures a bounded autonomous OER/open-knowledge loop for an Obsidian KnowledgeOS/TALOS-style course library.

The loop moved from manual page authoring to a reusable helper-repo generator:

```text
scripts/v9/oer_crosswalk_generator.py
```

The generator remains safe by default:

- dry-run unless `--apply` is explicitly provided;
- blocks path traversal;
- writes only course-level OER/FAQ pages and optional sample pages;
- supports backup directories;
- preserves the evidence boundary: OER/FAQ structure is not V6 verified evidence.

## Aggregate Result from the Local Vault Run

The formal vault run stayed local-only. Aggregate metrics after the final stopped round:

| Metric | Count | Coverage |
|---|---:|---:|
| Formal courses scanned | 20 | 100% |
| OER crosswalk pages | 4 | 20% |
| FAQ / question-driven hubs | 3 | 15% |
| V7 project pages | 20 | 100% |
| Term indexes | 20 | 100% |
| Review-practice pages | 20 | 100% |
| V6 verified evidence courses | 1 | 5% |
| V8 Daily Mission courses | 1 | 5% |

Only aggregate counts and reusable workflow lessons are uploaded here. Formal course notes and generated vault dashboards remain local.

## Profiles Covered

The local run validated the generator against several course profiles:

| Profile | OER structure emphasis |
|---|---|
| learning / memory | open textbook structure, active recall, spaced repetition, Q&A prompts |
| technical documentation | MDN-style docs, Stack Exchange-style troubleshooting, terminology graph |
| design / media | open-media licensing, critique rubrics, design Q&A, asset provenance |
| exam / performance training | course-package structure, progress logs, error reproduction, learning-method FAQ |

The generator intentionally does not claim factual verification when no V6 verified source exists.

## Reusable Command Pattern

Preview without writing:

```bash
python scripts/v9/oer_crosswalk_generator.py \
  --vault "<formal-vault-path>" \
  --course "<course-name>" \
  --sample
```

Apply with explicit write permission and backups:

```bash
python scripts/v9/oer_crosswalk_generator.py \
  --vault "<formal-vault-path>" \
  --course "<course-name>" \
  --sample \
  --apply \
  --backup-dir "<external-backup-dir>"
```

## Validation Checklist Used Locally

Each applied round used this checklist before local commit:

1. JSON parse checks for generated machine-readable summaries.
2. Markdown fence-balance checks.
3. HTML `href` target checks for generated dashboard cards.
4. Mojibake marker scan.
5. Evidence-boundary review: OER/FAQ must not become a V6 verified claim.
6. Local git commit only for the formal vault.
7. Helper repo tests before upload.

## Stop Protocol

The user requested: finish the current round, then stop.

The loop honored that by:

- completing the active round to a validation + commit point;
- not enqueueing a new course round;
- recording the stopped state in local execution notes;
- leaving the helper repo update as this sanitized upload only.

## Helper-Repo Scope

Uploaded helper-repo changes should remain limited to:

- docs;
- reusable scripts;
- tests;
- templates;
- demo-only examples.

The following stay out of the repository:

- formal vault note bodies;
- private Obsidian configuration;
- raw course materials;
- media files;
- transcripts or OCR full text;
- local synced-drive state;
- secrets or API keys.
