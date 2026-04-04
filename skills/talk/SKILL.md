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

Always read the user's `config.yaml` first. The config lives at `${user_config.assets_path}/config.yaml`.

Before doing anything else, check the config path:

1. **If `${user_config.assets_path}` is empty or not set**: Tell the user: "No assets path configured. Run `/talk-builder:talk-setup` to set up your personal style and preferences." Then stop.
2. **If the path is set but the directory doesn't exist**: Tell the user: "Your assets folder `[path]` doesn't exist. Run `/talk-builder:talk-setup` to set it up again, or update the path in your plugin settings." Then stop.
3. **If the directory exists but `config.yaml` is missing**: Tell the user: "Your assets folder exists but has no `config.yaml`. Run `/talk-builder:talk-setup` to complete the configuration." Then stop.
4. **If `config.yaml` exists**: Read it and continue with phase detection.

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

The assets path is configured via the plugin's `userConfig` system. When the user enables the plugin, Claude Code prompts for `assets_path`. This value is available as `${user_config.assets_path}` and persists across plugin updates.

If the user needs to change the path later, they can update it in their plugin settings or run `/talk-builder:talk-setup` again.
