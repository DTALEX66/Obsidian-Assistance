# Pixel Tuning Pass

## Reference Used

- `01_Dashboard_紫色霓虹工作台.png`
- `02_Reading_紫色钻石笔记工作区.png`

Primary target for this pass: `02_Reading_紫色钻石笔记工作区.png`.

## Layout Changes

The preview page was changed from a presentation-style page into an Obsidian-like desktop workspace:

- fixed left vault rail
- top tab/search toolbar
- central editor + live preview split pane
- right rail with Outline, Properties, and Linked Mentions
- bottom status bar

## Visual Matching Decisions

- Dark navy/purple base canvas
- thin translucent borders
- low-contrast panel layering
- purple active tabs and selected file rows
- compact 12-14px interface typography
- high-density desktop layout
- crystal accent in the sidebar
- Markdown note content mirroring the reference structure

## Important Fixes

- Replaced landing-page structure with Obsidian workspace structure.
- Added realistic Vault tree proportions.
- Added top Obsidian tab strip and search field.
- Added editor/live-preview split with scrollable note panels.
- Added right inspector rail with Outline, Properties, Linked Mentions.
- Added bottom status strip.
- Added desktop and narrow viewport fallbacks.
- Added package-local SVG illustrations for crystal branding, graph texture, reading flow, and empty state.

## Verification

Static structure check passed:

- one `<body>`
- one `</body>`
- one `</html>`
- left rail exists
- topbar exists
- note workspace exists
- right rail exists
- bottom status exists
- matching CSS classes exist

Rendered screenshot check was attempted but could not run because the local Playwright browser executable is not installed. No dependency was installed.

## Remaining Pixel Work

Needs one real rendered pass to tune:

- exact left rail width against Obsidian theme chrome
- center split ratio at the user's normal window size
- right rail density
- purple glow intensity
- line-height and Markdown paragraph rhythm
- bottom status bar alignment
