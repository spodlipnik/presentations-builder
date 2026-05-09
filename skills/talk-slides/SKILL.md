---
name: talk-slides
description: Use when generating the PPTX presentation file from an approved narrative. Reads docs/narrative.md and config.yaml's design_tokens, builds a per-slide brief, and delegates to document-skills:pptx for generation.
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Skill
---

# Talk Slides — Generate PPTX via Official PPTX Skill

Consumes a narrative (from `talk-narrative`) and design tokens (from the user's `config.yaml`) to generate a professional PPTX. **All actual PPTX generation is delegated** to the official `document-skills:pptx` skill — this skill is a thin orchestrator that produces a structured brief and hands off.

The official skill is *guidance-style*: it returns PptxGenJS tutorials. After invoking it, you (Claude) write a per-deck `build.js` script following its patterns, run it via Node, and run the visual QA loop.

## When this runs

- After `talk-narrative` has produced `docs/narrative.md`
- When user wants to generate or regenerate `presentation.pptx`
- Triggers: "generar slides", "crear pptx", "generate the presentation"

## Prerequisites

- `docs/narrative.md` exists with slides using the 12 canonical types (see `talk-narrative` reference)
- `${user_config.assets_path}/config.yaml` exists with a `design_tokens:` section
- The `document-skills:pptx` skill is available in the session (ships with the `claude-plugins-official` `document-skills` plugin)
- Node.js + globally installed `pptxgenjs` (per the official skill's setup: `npm install -g pptxgenjs`)
- `${CLAUDE_PLUGIN_DATA}/venv/bin/python3` available with `python-pptx` (used for output verification)

## Workflow

### Phase 1: Load and validate

**Step 1.1:** Read `docs/talk.yaml` for topic, duration, language.

**Step 1.2:** Read `${user_config.assets_path}/config.yaml`. Extract the `design_tokens:` block. If missing, abort with:

> "❌ Tu `config.yaml` no tiene una sección `design_tokens:`. Corre `/talk-builder:talk-setup` para configurar colores y fuentes, o edita el archivo a mano."

**Step 1.3:** Read `docs/narrative.md`. Parse each slide as a record with:
- `type` (one of the 12 canonical types — see "Valid types" below)
- typed content fields per type (see "Field schema by type")
- speaker-facing fields (`speaker`, `context`, `bridge`, `ref`, `section`, `type_line`) — read but not used in the brief

**Step 1.4:** Validate every slide:
- `type` must be one of the 12 canonical types
- All required fields for that type must be present and non-empty
- All `image` / `chart_image` / `image_*` / `image_full` paths must point to existing files (resolve relative to CWD, then convert to absolute paths for the brief)

**If validation fails**, list every error grouped by slide and abort. Example:

> "❌ Errores en `docs/narrative.md`:
>  - Slide 5 (type=assertion-evidence): falta `image`
>  - Slide 8 (type=patient-case): tipo legacy. Mapea a `assertion-evidence` (ver CHANGELOG 2.0).
>  - Slide 12 (type=chart): `chart_image` apunta a `images/missing.png` (no existe).
>
> Edita docs/narrative.md y volvé a correr /talk-slides."

### Phase 2: Keynote-edit protection

If `presentation.pptx` exists in CWD and was modified after the last generation (compare mtime against `docs/slides-decisions.md` mtime if it exists, otherwise just warn):

> "⚠️ `presentation.pptx` parece editado a mano (probablemente Keynote).
>  Regenerar lo va a sobrescribir. Opciones:
>  - **(a) Continuar** — perdés ediciones manuales
>  - **(b) Backup primero** — copio a `presentation.backup-YYYY-MM-DD-HHMM.pptx`
>  - **(c) Cancelar**"

If (b): `cp presentation.pptx "presentation.backup-$(date +%Y-%m-%d-%H%M).pptx"` then continue.

### Phase 3: Build the brief

For each slide, build a brief entry. The complete brief format is documented inline below.

**Brief structure (passed as prose to the official skill):**

```
Create a PPTX file at <ABSOLUTE_PATH>/presentation.pptx with N slides.

Use these design tokens for ALL slides:
  - primary color: <design_tokens.color.primary>
  - accent color: <design_tokens.color.accent>
  - text color: <design_tokens.color.text>
  - background color: <design_tokens.color.background>
  - muted color: <design_tokens.color.muted>
  - heading font: <design_tokens.typography.heading_font>
  - body font: <design_tokens.typography.body_font>

Use slide layout 'LAYOUT_WIDE' (13.333" × 7.5") for all slides.

General rules:
  - Do not add accent lines under titles (this is a hallmark of AI-generated slides)
  - Do not add decorative elements that weren't requested
  - One message per slide
  - Use the heading font for all titles, headlines, and big numbers
  - Use the body font for all body text, captions, attributions
  - Default text color is the text token; muted color is for secondary text only
  - For images: compute width/height manually from source aspect ratio. Never use pptxgenjs `sizing: { type: 'cover' | 'contain' }` — it produces broken XML.

Slides:

1. <type>:
   <fields rendered as instructions per type — see field-rendering rules>

2. <type>:
   ...
```

**Field-rendering rules per type** (each type expands to instruction prose):

- `title`: instructions for a title slide with `title` (large, heading font, primary color), `author` (medium, text color, body font), `affiliation` (small, muted), optional `subtitle` (between title and author), optional `date` (small, muted, bottom).
- `text-list`: a slide with `title` at top (heading font, primary color) and a numbered list of `items` below (body font, text color).
- `divider`: dark background slide. `section_label` small at top (accent color, heading font, uppercase). `section_title` large centered (heading font, white or background-inverted color). Optional `teaser` smaller below in muted italic.
- `assertion-evidence`: full-sentence `headline` at top (~32pt, heading font, text color), `image` on the right ~40% width (contained, no distortion, no stretching), optional `caption` below image (10pt, muted, body font).
- `assertion-evidence-left`: same as above but image on the left.
- `chart`: `headline` at top, `chart_image` fullwidth below (contained). Optional `caption`.
- `callout`: `big_text` huge centered (60-80pt, heading font, accent or primary color), `sub_label` small below (muted, body font).
- `quote`: `quote_text` large centered italic (~28pt, heading font), `attribution` smaller below right-aligned (muted, body font), optional decorative quote marks in primary color.
- `comparison`: `headline` at top, two columns equal width. Each column has `<side>_label` (small, accent color, heading font) and `<side>_content` below (body font, text color). Vertical separator in muted color.
- `gallery`: `headline` at top, 2×2 grid of `image_1`-`image_4` (each contained, equal box). Optional `caption` at bottom.
- `fullbleed`: `image_full` covers entire slide. If `overlay_text`, overlay it bottom-third in white (or dark if image is light) with a semi-transparent dark band behind for legibility.
- `closing`: `main_text` centered large (heading font, primary color), `contact_info` smaller below (muted, body font).

After validation, ALL image paths in the brief must be absolute paths.

### Phase 4: Delegate to `document-skills:pptx`

Invoke the `Skill` tool with `document-skills:pptx`. Pass the full brief from Phase 3 as the `args` parameter. The skill loads its `pptxgenjs.md` guidance into context.

Following that guidance, write a per-deck build script (e.g., `_build/build.js`) using PptxGenJS. Apply the brief slide-by-slide, honoring design_tokens and the per-type rendering rules. For images, always compute width/height manually from source aspect ratio (use Pillow via the venv if needed) — never use pptxgenjs's broken `sizing` property.

Run the build script:

```bash
cd _build && node build.js
```

Verify `presentation.pptx` exists at the expected absolute path:

```bash
ls -la presentation.pptx
```

### Phase 5: Optional visual QA

Ask the user:

> "✅ `presentation.pptx` generado.
>  ¿Querés que corra una inspección visual ahora? El skill oficial convierte el deck a JPGs y un subagent revisa por overflow, overlap, low contrast, leftover placeholders. Toma 1-2 min adicionales."

If yes, follow the QA loop in the official skill's `SKILL.md` ("QA (Required)" section): convert to PDF/JPG via `soffice` + `pdftoppm`, dispatch a subagent with the standard QA prompt to inspect each slide, report findings, iterate fixes if user requests.

If no, skip.

### Phase 6: Final report

**Step 6.1:** Write `docs/slides-decisions.md`:

```markdown
# Slides Decisions

Generated by `/talk-slides` on YYYY-MM-DD via document-skills:pptx.

| Slide | Type | Key content |
|---|---|---|
| 1 | title | "<title>" |
| 2 | assertion-evidence | "<headline>" + image |
| ... |
```

**Step 6.2:** Tell the user:

> "🎉 Presentación generada:
>  - `presentation.pptx` — deck generado por document-skills:pptx
>  - `docs/slides-decisions.md` — resumen de tipos por slide
>  - `_build/build.js` — script PptxGenJS regenerable (editable para tweaks de bajo nivel)
>
>  Abre `presentation.pptx` en Keynote para pulido final.
>
>  Para regenerar tras cambios en narrative, corre `/talk-slides` de nuevo."

## Valid types (canonical 12)

`title`, `text-list`, `divider`, `assertion-evidence`, `assertion-evidence-left`, `chart`, `callout`, `quote`, `comparison`, `gallery`, `fullbleed`, `closing`.

Any other value in `type:` is a legacy format — see CHANGELOG 2.0 for the mapping.

## Field schema by type

| Type | Required | Optional |
|---|---|---|
| `title` | `title`, `author`, `affiliation` | `subtitle`, `date` |
| `text-list` | `title`, `items` (list) | — |
| `divider` | `section_label`, `section_title` | `teaser` |
| `assertion-evidence` | `headline`, `image` | `caption` |
| `assertion-evidence-left` | `headline`, `image` | `caption` |
| `chart` | `headline`, `chart_image` | `caption` |
| `callout` | `big_text`, `sub_label` | — |
| `quote` | `quote_text`, `attribution` | — |
| `comparison` | `headline`, `left_label`, `left_content`, `right_label`, `right_content` | — |
| `gallery` | `headline`, `image_1`, `image_2`, `image_3`, `image_4` | `caption` |
| `fullbleed` | `image_full` | `overlay_text` |
| `closing` | `main_text`, `contact_info` | — |

## Gotchas

### `document-skills:pptx` is guidance-style, NOT a one-shot generator

Invoking the skill returns its `pptxgenjs.md` tutorial in your context. YOU then write a per-deck `_build/build.js` following that guidance and run it via Node. Don't expect the skill to produce a `.pptx` autonomously from a single Skill call — that's not how it works.

### Never use PptxGenJS `sizing: { type: 'cover' | 'contain' }` for images

These options produce broken XML. Pre-compute width/height manually from the source aspect ratio (use Pillow via the venv: `from PIL import Image; w, h = Image.open(p).size`). Then pass exact `w, h` to `slide.addImage()`. Documented at length in the spike findings.

### Legacy `Type:` values must hard-fail with the migration table

If `narrative.md` contains v1 types like `patient-case`, `data-chart`, `quote-pullout` — list every offending slide and point at CHANGELOG 2.0's mapping table. Don't try to silently translate; the user's intent for borderline cases (e.g., `data-table` → `comparison` vs `chart`) requires their decision.

### `LAYOUT_WIDE` is 13.333"×7.5" — coordinate ALL math to those dimensions

PptxGenJS has multiple 16:9 layouts with different actual sizes. We standardize on `LAYOUT_WIDE` (13.333" × 7.5"). Mixing layouts within a single deck or using LAYOUT_16x9 dimensions inside a LAYOUT_WIDE deck causes off-center clipping with no visible warning.

### The brief's image paths must be ABSOLUTE before delegation

`narrative.md` uses paths relative to the project CWD (e.g., `images/foo.png`). The official skill needs absolute paths to find the files when `_build/build.js` runs. Phase 1.4 of this skill is the place to convert.
