# Cloud Upload Safety Report (2026-07-04)

## Decision

The project was prepared for upload through the auxiliary repository, not by uploading the private Obsidian vault.

## Target Repository

```text
git@github.com:DTALEX66/Obsidian-Assistance.git
```

## Uploaded Scope

Only public-safe helper-repository documentation is intended for this upload:

- `docs/talos-ui-ux-design-handoff-2026-07-04.md`
- `docs/obsidian-knowledgeos-project-status-2026-07-04.md`
- `docs/cloud-upload-safety-report-2026-07-04.md`
- README links to the new docs

## Explicitly Excluded

- Private Obsidian vault content.
- `.obsidian/` configs, plugins, workspace, runtime state.
- Source course files and derived media.
- Audio/video/PDF/PPT/images from private materials.
- ASR/OCR/transcript/full-note outputs.
- Secrets, tokens, cookies, credentials, connection strings.
- Local sync/cache/runtime files.

## Required Pre-Push Checks

Before push, run a staged-file scan for:

- Forbidden paths: `.obsidian/`, `work/`, `outputs/`, `transcripts/`, `ocr/`, `asr/`, private vault paths.
- Forbidden media/extensions: `.mp3`, `.mp4`, `.wav`, `.m4a`, `.pdf`, `.ppt`, `.pptx`, `.zip`, `.rar`, `.7z`, `.sqlite`.
- Secret-like strings: API keys, tokens, passwords, cookies, private keys, connection strings.
- Large files.

## Result

The concrete scan result is recorded in the terminal output for the upload commit/push session.
