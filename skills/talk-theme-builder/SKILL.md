---
name: talk-theme-builder
description: Use when user wants to create, edit, or manage presentation themes for the Talk Builder system. Triggers when user says "crear tema", "create theme", "nuevo tema", "edit theme", "talk-theme-builder", or similar. Walks user through co-creation of themes from their reference PPTX slides.
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Skill
---

# Talk Theme Builder

Interactive skill to create and manage presentation themes. A theme is a reusable collection of layouts (tokens + roles × variants) that `talk-slides` uses to generate presentations.

## Commands

- `create` — build a new theme from reference PPTX (5-phase co-creation workflow)
- `edit` — refine an existing theme (deferred to Plan 2B)
- `list` — list all themes (deferred to Plan 2B)

## Prerequisites

Before running `create`:
- User must have a reference PPTX with 15-30 slides representing their style
- LibreOffice must be installed (`which soffice`) for thumbnail generation
- Python deps installed (python-pptx, PyYAML, lxml) — auto-installed by hooks

## Workflow: `create`

Takes the user through 5 phases to build a complete theme.

### Fase 0: Input + Extracción

(see phase-0 section below)

### Fase 1: Clustering + Mapping

(see phase-1 section below)

### Fase 2: Review rol-por-rol

(see phase-2 section below)

### Fase 3: Fill gaps

(DEFERRED to Plan 2B — for MVP, skip roles not detected in reference)

### Fase 4: Sampler deck

(DEFERRED to Plan 2B)

### Fase 5: Save + naming

(see phase-5 section below)

---

<!-- Phase implementations will be added in subsequent tasks -->
