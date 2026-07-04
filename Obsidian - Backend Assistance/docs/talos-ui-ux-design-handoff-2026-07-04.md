# TALOS UI/UX Design Handoff (2026-07-04)

This is a **public/sanitized design handoff** for the TALOS / Obsidian KnowledgeOS usage layer. It intentionally excludes the private vault, course notes, media files, transcripts, OCR text, `.obsidian/` runtime config, personal paths, and secrets.

## Product Direction

TALOS is an Obsidian-based KnowledgeOS usage layer: a dark Purple Gemstone system console for course reading, evidence review, active recall, project conversion, OER cross-checking, and autonomous loop monitoring.

## Design Principles

| Principle | Requirement |
|---|---|
| Purple Gemstone shell | Deep navy/black background, purple glow, glass panels, rounded cards, thin borders. |
| Evidence-first UX | Separate verified source screenshots/keyframes/PDF pages from reference images, OER, and AI summaries. |
| Obsidian-native implementation | Prefer Markdown, callouts, tables, Dataview, Canvas/Kanban, and CSS snippets over raw HTML. |
| Usage layer over storage layer | Do not require moving private course files; design curated navigation and dashboards. |
| Responsive safety | No vertical squashing, overlapping cards, or unreadable long paths on narrow screens. |
| Performance restraint | Use subtle motion and controlled blur so Obsidian remains smooth. |

## UI Surfaces to Design

### 1. Obsidian Global Shell

- Left Ribbon icon rail.
- Bookmarks/navigation sidebar.
- File tree visual treatment.
- Top title/tabs/search area.
- Command palette and quick switcher.
- Right inspector for properties, backlinks, graph, evidence metadata, and AI suggestions.
- Status bar and sync/validation indicators.
- Context menus, modals, prompts, suggestion lists, and toasts.

### 2. TALOS Home Console

- Hero command bar.
- Global search / shortcut entry area.
- Command Center metrics for Review, OER, Projects, and Evidence.
- Three-column workspace navigation.
- Current focus / next action panel.
- Guardrail status strip.

### 3. Course System

- Course library overview.
- Course card wall.
- Domain dashboard.
- Single-course portal.
- Course reader: left outline, main reading, right inspector.
- Visual index: reference images vs generated diagrams vs verified evidence.
- Real screenshot/keyframe/PDF page viewer.

### 4. Evidence System

- Evidence matrix.
- Evidence heatmap.
- Visual coverage dashboard.
- Media/evidence gallery.
- Pending/rejected evidence queue.
- Verified, pending, rejected, missing, and reference-only status chips.

### 5. Review + AI Center

- Review overview.
- Today's question card.
- Show Answer interaction.
- Again / Hard / Good / Easy rating controls.
- AI companion actions: chat, summarize, connect, plan.
- Daily Mission and retro log.

### 6. Project Atlas + Kanban

- Canvas-style project map.
- Project Kanban columns and cards.
- Project detail drawer.
- Evidence-linked project actions.
- Drag/selection/hover states.

### 7. OER Crosswalk

- OER coverage dashboard.
- Local course vs open-source/open-education structure comparison.
- FAQ-driven learning entry.
- Source confidence and license/status indicators.

### 8. Sleep Mode / Autonomous Loop Console

- Current round.
- Queue and boundary display.
- Recent commit/log timeline.
- Stop/pause/resume states.
- Blocker and validation report surface.

### 9. Native Plugin Components

- Dataview table states.
- Tasks checkbox/due/priority states.
- Kanban board and card states.
- Calendar selection states.
- Canvas/Excalidraw canvas states.
- Properties editor states.
- Graph/backlinks states.
- Image/PDF/video-keyframe embed states.

## Component Library Checklist

| Family | Components |
|---|---|
| Navigation | Sidebar item, bookmark group, tab, breadcrumb, search item, command item. |
| Data display | Stat card, metric strip, badge, tag, progress bar, heatmap cell, status chip. |
| Content | Hero callout, panel, warning, course card, evidence card, project card, review card. |
| Inputs | Search, filter chip, segmented control, checkbox, rating button, toggle, date selector. |
| Overlays | Modal, drawer, tooltip, context menu, toast, image lightbox. |
| Tables | Dashboard table, Dataview table, evidence table, responsive overflow table. |
| Media | Thumbnail grid, image preview, PDF page preview, video keyframe card, rejected frame card. |
| AI/review | AI message bubble, suggestion card, show-answer panel, spaced-repetition buttons. |

## Required Interaction States

Default, hover, active, selected, focus-visible, loading, empty, error, warning, verified, rejected, disabled, narrow-screen, and long-title overflow states.

## Figma Structure Recommendation

```text
TALOS Purple Gemstone UI
├── 00 Cover & Product Principles
├── 01 IA / User Flows
├── 02 Foundations / Tokens
├── 03 Obsidian Shell
├── 04 Home Console
├── 05 Course Library + Reader
├── 06 Evidence Matrix + Media Viewer
├── 07 Review + AI Center
├── 08 Project Atlas + Kanban
├── 09 OER + Sleep Mode Console
├── 10 Native Plugin Components
├── 11 Responsive Frames
└── 12 Dev Notes / Obsidian Mapping
```

## Responsive Frames

Design at 1680, 1440, 1280, 1040, 760, and 520px. Three-column layouts should degrade to two-column and single-column layouts without vertical text or overlapping panels.

## Acceptance Criteria

- Purple Gemstone visual consistency across shell, home, course, evidence, review, project, and OER pages.
- Clear distinction between verified evidence and non-evidence materials.
- Obsidian-native implementation path for every component.
- Full interaction states for navigation, cards, tables, media, modals, and AI/review controls.
- Responsive layouts remain readable and clickable.
- No raw HTML requirement for core reading pages.
