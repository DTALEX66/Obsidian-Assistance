# TALOS Obsidian Frontend Scope

## 1. Project Definition

TALOS is currently defined as an **Obsidian frontend UI kit and plugin-view design system**.

This project is responsible for:

- frontend interface design
- Obsidian view mapping
- page layout, panels, components, and responsive behavior
- visual system, CSS tokens, component states, and mock interactions
- implementation-ready HTML/CSS/JS prototypes inside this workspace

This project is not responsible for:

- real course content ingestion
- reading or rewriting the user's Obsidian vault
- vault-wide indexing
- AI summarization or embedding
- backend services, databases, API servers, or sync workers
- Git automation
- plugin publishing or production packaging

The current HTML files are design prototypes. They should be treated as source material for frontend design decisions, not as final plugin architecture.

## 2. Meaning of "Connect to Obsidian"

In this project, "connect to Obsidian" means:

> A TALOS interface can be rendered inside Obsidian as a plugin-owned frontend surface.

Valid Obsidian frontend surfaces include:

- main workspace views
- right sidebar views
- modal dialogs
- command-triggered panels
- note-adjacent helper panes
- canvas-adjacent or graph-adjacent custom views

It does not mean:

- scanning the whole vault
- replacing Obsidian's file explorer, tab system, backlinks, properties, or status bar
- embedding the entire HTML prototype as a web page without adaptation
- automatically writing notes or metadata into the real vault

## 3. Current Prototype to Obsidian View Mapping

| Prototype file | Intended Obsidian surface | Frontend role | Notes |
|---|---|---|---|
| `index.html` | Main workspace view | TALOS Home Console | Should become a command-center view. It may show mock dashboard modules, but must not imply real indexing unless explicitly added later. |
| `course-reading.html` | Main workspace view | Course Reading Workspace | Keep the central reading/workbench UI. In a real plugin, Obsidian should provide native file tree, tabs, properties, backlinks, and status UI. |
| `evidence-matrix.html` | Main workspace view or right sidebar view | Evidence Matrix | Can remain a standalone frontend surface with mock filters, cards, and matrix states. |
| Review AI module | Right sidebar view or modal | Review assistant surface | Frontend-only mock interaction. No AI call, no vault read, no spaced-repetition write unless scope expands. |
| Project Atlas module | Main workspace view or canvas-adjacent view | Visual project map | Frontend map/canvas surface only. No real graph database or canvas file mutation. |
| Kanban / mission modules | Main view modules or command panels | Workflow UI components | Mock task states only. Do not bind to real Tasks plugin until explicitly requested. |

## 4. Architecture Boundary

The frontend layer may include:

- static mock data
- local in-page interactions
- tabs, drawers, filters, panels, keyboard-friendly controls
- empty states and loading states
- responsive desktop/tablet/narrow layouts
- component-level design tokens
- scoped CSS for Obsidian compatibility

The frontend layer must avoid:

- direct filesystem access
- direct vault writes
- plugin configuration edits
- `.obsidian` folder mutation
- `.git` operations
- BaiduSyncdisk sync manipulation
- background workers that index or transform files
- hidden network calls

## 5. Obsidian Shell Rule

The TALOS UI should not recreate Obsidian's native shell in production.

Use Obsidian native UI for:

- file explorer
- tabs
- panes
- command palette
- properties
- backlinks
- outgoing links
- status bar
- theme chrome

Use TALOS custom UI for:

- course reading workbench
- evidence cards
- evidence matrix
- review panel
- project atlas
- mission/kanban modules
- TALOS-specific action bars and state panels

The current full-shell prototype is still useful for visual review, but the production-facing plugin design should extract the TALOS workspace area and let Obsidian provide the surrounding frame.

## 6. Performance Policy

Frontend-only TALOS views should not make Obsidian noticeably slower if these constraints are followed:

- lazy-render hidden tabs and panels
- avoid rendering large lists all at once
- avoid all-vault query assumptions in UI copy
- keep animations restrained and transform/opacity based
- scope CSS under TALOS-specific root classes
- avoid global selectors that affect Obsidian themes
- avoid embedding large images unless they are part of the active screen
- use mock data caps for prototypes

Potential performance risks are out of scope unless the project later adds backend behavior:

- Dataview all-vault queries
- Smart Connections indexing
- Copilot whole-vault summaries
- Text Extractor batch OCR
- Obsidian Git sync
- large Excalidraw or Canvas files

## 7. Conflict Policy

Frontend-only TALOS does not conflict with opening Obsidian when:

- it renders inside plugin-owned containers
- it does not write to notes
- it does not modify `.obsidian`
- it does not run background indexing
- it does not trigger Git, sync, OCR, or AI processes

Conflict risk appears only if the scope expands into:

- writing real notes
- modifying plugin settings
- scanning the vault
- syncing files
- running scripts
- mutating canvas or attachment files

Those capabilities require a separate approval and implementation plan.

## 8. Design Deliverables

The project should now focus on these deliverables:

1. Obsidian-compatible visual system
2. TALOS component inventory
3. view-by-view frontend screen files
4. scoped CSS token strategy
5. mock interaction behavior
6. responsive layout rules
7. plugin-view mapping notes
8. frontend acceptance checklist

Recommended screen files:

- `index.html` for the TALOS Home Console prototype
- `course-reading.html` for the core reading workspace prototype
- `evidence-matrix.html` for the evidence matrix prototype
- optional future `review-center.html`
- optional future `project-atlas.html`
- optional future `component-system.html`

Each screen should remain a frontend artifact unless the user explicitly expands the project into plugin engineering.

## 9. Acceptance Checklist

A TALOS frontend screen is acceptable when:

- it can be understood as an Obsidian plugin view
- it does not depend on real vault data
- all visible copy is interface-facing, not backend-facing
- it avoids fake claims about indexing, sync, or AI completion
- it has scoped selectors and implementation-ready component structure
- it supports realistic desktop workspace density
- it has a narrow-screen fallback
- it does not duplicate Obsidian native shell elements unless the file is explicitly a visual mockup
- interactive controls have local mock behavior where useful

## 10. Working Rule Going Forward

Unless the user explicitly expands scope, future TALOS work should use this rule:

> Design the Obsidian frontend surface. Do not design, read, write, index, or automate the user's real knowledge base.
