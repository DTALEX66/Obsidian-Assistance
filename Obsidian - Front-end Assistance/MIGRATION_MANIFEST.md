# TALOS Obsidian Frontend Migration Manifest

## Source

`D:\All projects\35d917c5-aef6-4c4f-b0d4-8d36c07dcc28`

## Target

`D:\All projects\Obsidian-Assistance\Obsidian - Front-end Assistance`

## Scope

This migration moves the current workspace project into the Obsidian front-end assistance workspace.

Included:

- `talos-frontend-ui/`
- preview HTML, plugin scaffold, styles, SVG assets, and audit notes
- TALOS reference extraction folders and visual reference images
- Obsidian frontend scope and compatibility notes
- existing prototype HTML files

Excluded:

- real Obsidian Vault writes
- `.obsidian` plugin installation
- course content ingestion
- backend services
- AI indexing
- Git commits or pushes

## Safety Rule

The migration should copy files into the target workspace only. It should not overwrite target files, modify the real vault, or touch `E:\`.

## Verification

After migration, confirm that the target contains:

- `talos-frontend-ui/preview.html`
- `talos-frontend-ui/styles.css`
- `talos-frontend-ui/assets/crystal-logo.svg`
- `OBSIDIAN_FRONTEND_SCOPE.md`
- `MIGRATION_MANIFEST.md`
