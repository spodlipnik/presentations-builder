---
name: talk
description: Use when building academic or medical presentations. Main entry point for Talk Builder — orchestrates the full workflow from briefing to final outputs. Triggers when user says "create a presentation", "build a talk", "prepare slides", "presentation about", or invokes /talk.
argument-hint: "[topic or phase]"
allowed-tools:
  - Read
  - Glob
  - Bash
  - Skill
---

# Talk Builder — Orchestrator

Single entry point for the Talk Builder workflow. Detects the current project state and guides the user through the next phase.

## Important

Always read the user's `config.yaml` first. If it does not exist, redirect to `/talk-setup` before anything else.

The config location is stored at a user-chosen path. Check for a `talk-builder-config-path` file in `~/.claude/` that stores the assets path. If neither exists, ask the user for the path or redirect to `/talk-setup`.

## Phase Detection

Scan the current working directory for these files to determine project state:

| File | Phase Completed |
|---|---|
| `talk.yaml` | Briefing |
| `vision.md` | Vision |
| `research.md` | Research |
| `images/` (non-empty) | Assets |
| `narrative.md` | Narrative |
| `study-document.md` + `article-summaries.md` | Study Docs |
| `speaker-script.md` | Script |
| `presentation.pptx` | Slides |

## Behavior

### 1. Show project status

Display a visual checklist of all phases:

```
Talk Builder — Project Status:

  [done] Briefing (talk.yaml)
  [done] Vision (vision.md)
  [done] Research (research.md)
  [open] Assets (images/)
  [open] Narrative (narrative.md)
  [open] Study Documents (study-document.md)
  [open] Speaker Script (speaker-script.md)
  [open] Slides (presentation.pptx)

  -> Next step: Assets
  Continue, or jump to another phase?
```

Use checkmarks and clear indicators for completed vs pending phases.

### 2. Propose next phase

Suggest the next uncompleted phase. The user can:
- Continue with the suggested phase
- Jump to any other phase
- Redo a completed phase

### 3. Invoke the corresponding skill

Based on the user's choice, invoke the appropriate skill:
- No config found -> `talk-setup`
- No `talk.yaml` -> `talk-briefing`
- No `vision.md` -> `talk-vision`
- No `research.md` -> `talk-research`
- No images -> `talk-assets`
- No `narrative.md` -> `talk-narrative`
- No `study-document.md` -> `talk-study-doc`
- No `speaker-script.md` -> `talk-script`
- No `presentation.pptx` -> `talk-slides`

### 4. Handle empty directory

If the working directory is empty (new project), start from `talk-briefing` and create the `pdfs/` and `images/` subdirectories.

### 5. Detect _build/ directory

If a `_build/` directory exists in the project and contains generation scripts (`.js` files), mention: "Previous generation scripts are available in `_build/` — these can be used to regenerate or modify the presentation."

## Config Path Resolution

On first run after setup, the `/talk-setup` skill saves the config path. The orchestrator needs to find it. Strategy:

1. Check `~/.claude/talk-builder-config-path` (a single-line file with the path)
2. If not found, ask the user: "Where is your Talk Builder config? (run /talk-setup if you haven't set it up yet)"
