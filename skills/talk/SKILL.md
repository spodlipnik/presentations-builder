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
4. **If `config.yaml` exists**: Read it and confirm to the user: "Config loaded from `[path]` (language: [lang], complexity: [level], design_tokens: [primary color] / [heading font])." Then continue with phase detection.

## Environment Check

After loading config successfully, run a quick environment verification **before** showing project status. Run all checks silently via Bash and present a single summary table.

### Checks to run

```bash
# 1. Python venv (with cairosvg added in v2.0)
VENV="${CLAUDE_PLUGIN_DATA}/venv/bin/python3"
if [ -x "$VENV" ] && "$VENV" -c 'import pptx, yaml, lxml, cairosvg' 2>/dev/null; then
  echo "PYTHON_OK"
else
  echo "PYTHON_FAIL"
fi

# 2. System deps
which pdftoppm >/dev/null 2>&1 && echo "POPPLER_OK" || echo "POPPLER_FAIL"

# 3. document-skills:pptx availability (best-effort — the Skill tool will fail gracefully if missing)
# No reliable shell check exists; talk-slides handles this at delegation time.
```

### Display format

Present results as a compact status block before the project status. Use checkmarks for passing, warnings for non-critical missing items, and errors for blockers:

```
Talk Builder — Environment:
  ✓ Config: en, moderate, design_tokens: #0B3D91 / Avenir Heavy
  ✓ Python venv (python-pptx, PyYAML, lxml, cairosvg)
  ✓ System: poppler ✓

```

Rules:
- **Python venv missing** → error, suggest: `python3 -m venv ~/.claude/plugins/data/talk-builder/venv && ~/.claude/plugins/data/talk-builder/venv/bin/pip install -r <plugin>/assets/scripts/requirements.txt`
- **poppler missing** → error, suggest `brew install poppler`
- Do NOT block the workflow for warnings, only for errors.

## Phase Detection

Scan the current working directory for these files to determine project state:

| File | Phase Completed |
|---|---|
| `docs/talk.yaml` | Briefing |
| `docs/vision.md` | Vision |
| `docs/research.md` | Research |
| `docs/narrative.md` | Narrative |
| `images/` (non-empty) | Assets |
| `docs/study-document.md` | Study Docs |
| `docs/speaker-script.md` | Script |
| `presentation.pptx` | Slides |

## Behavior

### 1. Show project status

Display a visual checklist of all phases:

```
Talk Builder — Project Status:

  [done] Briefing (docs/talk.yaml)
  [done] Vision (docs/vision.md)
  [done] Research (docs/research.md)
  [open] Narrative (docs/narrative.md)
  [open] Assets (images/)
  [open] Study Documents (docs/study-document.md)
  [open] Speaker Script (docs/speaker-script.md)
  [open] Slides (presentation.pptx)

  -> Next step: Narrative
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
- No `docs/talk.yaml` -> `talk-briefing`
- No `docs/vision.md` -> `talk-vision`
- No `docs/research.md` -> `talk-research`
- No `docs/narrative.md` -> `talk-narrative`
- No images -> `talk-assets`
- No `docs/study-document.md` -> `talk-study-doc`
- No `docs/speaker-script.md` -> `talk-script`
- No `presentation.pptx` -> `talk-slides`

### 4. Handle empty directory

If the working directory is empty (new project), start from `talk-briefing` and create the `docs/`, `pdfs/`, and `images/` subdirectories.

If the user already provided useful information in their message (topic, duration, audience, occasion), acknowledge it and note that it will be carried into the briefing phase so they don't have to repeat themselves.


## Config Path Resolution

The assets path is configured via the plugin's `userConfig` system. When the user enables the plugin, Claude Code prompts for `assets_path`. This value is available as `${user_config.assets_path}` and persists across plugin updates.

If the user needs to change the path later, they can update it in their plugin settings or run `/talk-builder:talk-setup` again.

## Gotchas

### `libcairo` is a library, not a binary — don't use `which`

The environment check tests for libcairo with `[ -f /opt/homebrew/lib/libcairo.2.dylib ]` (and fallback paths), not `which libcairo`. Files like `.dylib` aren't on PATH; `which` always returns missing. The actual install: `brew install cairo`.

### Phase detection is purely file-based — empty `images/` does NOT mark Assets done

Phase Detection checks `images/` non-empty (via `ls`). If the user creates `images/` but adds files later, the phase only flips when at least one file appears. Watch for this when guiding the user — the orchestrator's "Next step" remains "Assets" until something is in `images/`.

### Legacy `Type:` values from v1 will hard-fail in `talk-slides`

If `docs/narrative.md` was authored with v1 (18-role taxonomy), `talk-slides` aborts with a list of legacy types and points at the CHANGELOG migration table. Don't try to "fix forward" silently — the failure is intentional. The user should manually map per the CHANGELOG.
