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

---

## Phase 2: Migrate (only if legacy format detected)

**Detection:** A narrative is legacy if any slide has a `Type:` value NOT in the 18 canonical roles (see `references/role-taxonomy.md`).

**Step 1:** Check all slides' types:
```bash
python3 -c "
import sys
sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT}/assets/scripts')
from parse_narrative import parse_narrative
slides = parse_narrative('docs/narrative.md')
canonical = {'title','disclosure','agenda','section-divider','assertion-evidence',
             'patient-case','methodology','data-chart','data-table','comparison',
             'quote-pullout','image-fullbleed','image-gallery','timeline-process',
             'key-takeaway','poll-question','contact','closing'}
unknowns = [(s['slide_number'], s.get('type','')) for s in slides if s.get('type') not in canonical]
if unknowns:
    for sn, t in unknowns:
        print(f'Slide {sn}: {t!r}')
"
```

**Step 2:** If unknowns exist, ask user:

> "Esta presentación usa formato anterior. Detecté Types no canónicos:
> {list}
>
> ¿Migrar al sistema nuevo? Esto:
> - Mapea Types viejos a los 18 roles canónicos
> - Crea backup en `docs/narrative.legacy-backup.md`
> - Te muestra cambios propuestos antes de aplicar
>
> (yes/no/cancel)"

**Step 3:** If yes:
- Create backup: `cp docs/narrative.md docs/narrative.legacy-backup.md`
- For each unknown Type, propose mapping based on semantic similarity:
  - "bullets", "list" → `agenda` or `key-takeaway`
  - "intro" → `title`
  - "divider", "section" → `section-divider`
  - "conclusion", "summary" → `key-takeaway`
  - (catch-all) → ask user per slide
- Show proposed changes as a table, ask for confirmation
- Apply changes via Edit tool, line by line

**Step 4:** If no → proceed with warning that some slides may fail variant selection.

---

## Phase 3: Select Variants

**Step 1:** Run selection logic:

```bash
python3 -c "
import sys, json, yaml
sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT}/assets/scripts')
from select_variant import select_variant

slides = json.load(open('/tmp/parsed_slides.json'))
theme = yaml.safe_load(open('${THEME_PATH}'))['theme']
total = len(slides)
decisions = {}
reasons = {}
previous = None
for s in slides:
    # Respect user-locked variants (has Variant: but not # auto)
    if s.get('variant') and not s.get('variant_is_auto'):
        decisions[s['slide_number']] = s['variant']
        reasons[s['slide_number']] = 'user-locked (manual override)'
    else:
        chosen, reason = select_variant(s, theme, previous, total)
        decisions[s['slide_number']] = chosen
        reasons[s['slide_number']] = reason
    previous = decisions[s['slide_number']]

json.dump({'decisions': decisions, 'reasons': reasons}, open('/tmp/variant_decisions.json', 'w'), indent=2)
print(f'Selected {len(decisions)} variants')
" 2>&1
```

**Step 2:** Show user a summary:

> "🎯 Variantes seleccionadas para {N} slides:
>
> | # | Type | Variant | Reason |
> |---|---|---|---|
> | 1 | title | title.centered | auto: first slide, no image |
> | 2 | ae | ae.image-right | auto: image + short text |
> | 5 | ae | ae.image-left | auto: pacing alternation |
> | 8 | compare | compare.two-col-image | user-locked |
>
> ¿Aplicar estas decisiones al narrative.md? (yes/no/preview)"

**Step 3:** If user approves, write back:

```bash
python3 -c "
import sys, json
sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT}/assets/scripts')
from update_narrative import update_narrative_variants
data = json.load(open('/tmp/variant_decisions.json'))
decisions = {int(k): v for k, v in data['decisions'].items() if v}
update_narrative_variants('docs/narrative.md', decisions)
print('narrative.md updated')
"
```

---

## Phase 4: Quality Check (LLM review)

**Goal:** Review the full mapping for issues the rubric may have missed.

Read `/tmp/variant_decisions.json` and `/tmp/parsed_slides.json`. Look for:

1. **Consecutive same variants**: 3+ slides in a row with identical variant → suggest breaking up
2. **Content-variant mismatch**: e.g., `ae.image-right` but slide has no image; `chart.single-key` but no chart mentioned
3. **Missing required fields**: variant requires `image` slot but slide has no `Image:`
4. **Variety**: if only 1-2 variants used across all AE slides, suggest alternatives

Report findings:

> "🔍 Quality check:
> - {count} issues found
> - {details}
>
> Sugerencias:
> - Slide 7-9 usan todos `ae.image-right`. Considera alternar con `ae.image-left` para variedad visual.
> - Slide 12 usa `chart.single-key` pero no hay imagen. Verifica que el slide tenga una imagen de chart.
>
> ¿Aplicar sugerencias, ignorar, o dejar al usuario decidir? (apply/ignore/review)"

If apply → update decisions and re-run write-back.
If ignore → continue.
If review → pause for user input per-issue.

---

## Phase 5-preamble: Keynote Edit Protection

**Before running the generator**, check if an existing `presentation.pptx` was edited in Keynote (modified after last generation).

**Step 1:** Check file timestamps:

```bash
if [ -f presentation.pptx ] && [ -f _build/generate_presentation.js ]; then
    PPTX_MTIME=$(stat -f %m presentation.pptx)
    SCRIPT_MTIME=$(stat -f %m _build/generate_presentation.js)
    if [ "$PPTX_MTIME" -gt "$SCRIPT_MTIME" ]; then
        echo "WARNING: presentation.pptx modified after last generation"
    fi
fi
```

**Step 2:** If warning triggers, ask user:

> "⚠️ `presentation.pptx` fue editado después de la última generación (probablemente en Keynote).
>
> Regenerar lo va a sobrescribir. Opciones:
> - **(a) Continuar** — regenerar (perdería ediciones Keynote)
> - **(b) Backup primero** — copiar a `presentation.backup-YYYY-MM-DD-HHMM.pptx` y regenerar
> - **(c) Cancelar** — no regenerar"

**Step 3:** If backup:
```bash
TIMESTAMP=$(date +%Y-%m-%d-%H%M)
cp presentation.pptx "presentation.backup-${TIMESTAMP}.pptx"
echo "Backup: presentation.backup-${TIMESTAMP}.pptx"
```

Then proceed to generation.

---

## Phase 5: Generate PPTX

**Step 1:** Copy the generator template to `_build/`:

```bash
mkdir -p _build
cp "${CLAUDE_PLUGIN_ROOT}/assets/scripts/generate_presentation_template.js" _build/generate_presentation.js
```

**Step 2:** Fill in the template variables. Use sed or manual Edit:

```bash
THEME_PATH="${ASSETS_PATH}/themes/${THEME_ID}/theme.yaml"
SLIDES_JSON="/tmp/parsed_slides.json"
IMAGES_DIR="$(pwd)/images"
OUTPUT="$(pwd)/presentation.pptx"

# Use sed to substitute (backup first)
sed -i.bak \
  -e "s|\${THEME_PATH}|${THEME_PATH}|g" \
  -e "s|\${SLIDES_JSON_PATH}|${SLIDES_JSON}|g" \
  -e "s|\${IMAGES_DIR}|${IMAGES_DIR}|g" \
  -e "s|\${OUTPUT_PATH}|${OUTPUT}|g" \
  _build/generate_presentation.js
rm _build/generate_presentation.js.bak
```

**Step 3:** Run the generator:

```bash
NODE_PATH="${CLAUDE_PLUGIN_DATA}/node_modules" node _build/generate_presentation.js
```

Expected output: `Generated: /path/to/presentation.pptx`

If fails with module error → reinstall dependencies:
```bash
cd "${CLAUDE_PLUGIN_DATA}" && npm install
```

**Step 4:** Verify file exists:
```bash
ls -la presentation.pptx
```

---

## Phase 6: Final Report + layout-decisions.md

**Step 1:** Write `docs/layout-decisions.md` with per-slide reasoning:

```bash
python3 -c "
import json
decisions = json.load(open('/tmp/variant_decisions.json'))
lines = ['# Layout Decisions', '', 'Auto-generated by talk-slides.', '']
lines.append('| Slide | Variant | Reason |')
lines.append('|---|---|---|')
for sn in sorted(int(k) for k in decisions['decisions']):
    v = decisions['decisions'][str(sn)]
    r = decisions['reasons'][str(sn)]
    lines.append(f'| {sn} | {v or \"—\"} | {r} |')
open('docs/layout-decisions.md', 'w').write(chr(10).join(lines))
print('Wrote docs/layout-decisions.md')
"
```

**Step 2:** Final summary to user:

> "🎉 Presentación generada:
>
> **Archivos:**
> - `presentation.pptx` — deck generado
> - `docs/layout-decisions.md` — razonamiento de cada slide
> - `_build/generate_presentation.js` — script de generación (regenerable)
>
> **Variantes usadas:** {count distinct} de {count total} slides
> **Roles cubiertos:** {list}
>
> **Siguiente:** Abre `presentation.pptx` en Keynote para ajustes finales de:
> - Posición/tamaño de imágenes
> - Tipografía fina
> - Reemplazo de placeholders
>
> Si quieres regenerar con cambios de variantes, edita `docs/narrative.md` (quita `# auto` de variantes que quieres lockear, cambia las que quieres override), y corre `/talk-slides` de nuevo."
