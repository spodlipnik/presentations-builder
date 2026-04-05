---
name: talk-slides
description: Use when generating the PPTX presentation file from an approved narrative structure and a theme. Reads docs/talk.yaml (theme reference), docs/narrative.md (structured slides), and the theme catalog from assets_path/themes/. Applies rubric-based variant selection, generates the PPTX via PptxGenJS, and writes layout decisions back to narrative.md with `# auto` markers.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Skill
---

# Talk Slides — Generate PPTX from Theme + Narrative

Consumes a theme (from `talk-theme-builder`) and a narrative (from `talk-narrative`) to generate a professional PPTX presentation.

## When this runs

- After `talk-narrative` has produced `docs/narrative.md`
- When user wants to generate or regenerate `presentation.pptx`
- Triggers: "generar slides", "crear pptx", "generate the presentation", "hacer el pptx"

## Prerequisites

- `docs/talk.yaml` exists with `theme:` field pointing to an existing theme
- `docs/narrative.md` exists with slides using the 18 canonical roles
- Theme exists at `${ASSETS_PATH}/themes/<theme-id>/theme.yaml`
- Python 3 + Node.js + PptxGenJS installed (auto by hooks)

## Workflow

The skill proceeds through these phases:

1. **Load** — read talk.yaml, narrative.md, theme.yaml; validate
2. **Migrate** (if needed) — detect legacy narrative format and offer to update
3. **Select** — apply rubric to pick a variant per slide, write back with `# auto`
4. **Quality check** — LLM review of variant choices
5. **Generate** — invoke PptxGenJS script to produce presentation.pptx
6. **Protect** — detect Keynote edits, offer backup before overwrite
7. **Report** — write layout-decisions.md with reasoning

---

## Phase 1: Load

**Step 1:** Read `docs/talk.yaml`. Check for `theme:` field.
- If missing or empty → ask user:
  > "`docs/talk.yaml` no tiene un `theme:` definido. ¿Cuál quieres usar? Temas disponibles en `${ASSETS_PATH}/themes/`:"
  List available themes.

**Step 2:** Load and validate theme:
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/assets/scripts/load_theme.py" \
  "${ASSETS_PATH}/themes/${THEME_ID}/theme.yaml"
```
If validation fails → report error and exit.

**Step 3:** Parse narrative.md:
```bash
python3 -c "
import sys, json
sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT}/assets/scripts')
from parse_narrative import parse_narrative
slides = parse_narrative('docs/narrative.md')
json.dump(slides, open('/tmp/parsed_slides.json', 'w'), indent=2)
print(f'Parsed {len(slides)} slides')
"
```

**Step 4:** Summary to user:
> "✅ Cargado:
> - Tema: `${THEME_ID}` con X roles + Y variantes
> - Narrativa: N slides parseados
>
> Siguiente: {Migrate if legacy | Select variants}"
