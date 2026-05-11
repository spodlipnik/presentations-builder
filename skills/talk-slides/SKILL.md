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
- The `document-skills:pptx` skill is available in the session (ships with the `claude-plugins-official` `document-skills` plugin) — it brings its own Node + pptxgenjs requirement; see that skill's setup docs (`npm install -g pptxgenjs`). Talk Builder itself owns no Node dependencies.
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

**Step 1.4:** Validate every slide. Run the executable guard first:

```bash
${CLAUDE_PLUGIN_DATA}/venv/bin/python3 "${CLAUDE_PLUGIN_ROOT}/tools/validate_narrative.py" docs/narrative.md
```

If it exits non-zero, surface its stderr verbatim to the user and abort — do not attempt to fix-forward.

The validator checks:
- `type` must be one of the 12 canonical types (legacy v1 types hard-fail with CHANGELOG pointer)
- All required fields for that type must be present and non-empty
- All `image` / `chart_image` / `image_*` / `image_full` paths must point to existing files (resolved relative to the narrative's project root)

After it passes, convert relative image paths to absolute paths for the brief.

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

**Field-rendering rules per type** — these are codified from a layout eval and represent the canonical render contract. Layout coordinates assume LAYOUT_WIDE (13.333" × 7.5") throughout.

- `title`: `title` (large ~48pt, heading font bold, primary color, left-aligned at y≈2.3); optional `subtitle` between title and author (medium ~22pt italic, muted); `author` (medium ~20pt, text color); `affiliation` (small ~14pt, muted); optional `date` near bottom (small ~11pt, muted).

- `text-list`: anchor (title + items) as a block in the upper third — don't let dead space accumulate between them.
  - Title at y≈1.4 (heading font ~40pt, primary color, left-aligned).
  - Items start at y≈2.7, each row spaced ~0.85"–1.05" apart.
  - **CRITICAL**: render each item as TWO `addText` calls — one for the number, one for the text — in separate boxes so wrapped lines indent correctly under the item start. NEVER use a single rich-text array with embedded numbers; the wrap breaks to the left margin.
  - Number in accent color (heading font, bold, ~22pt) on the left (x≈0.9, w≈0.55).
  - Text in text color (body font, ~22pt) on the right (x≈1.45, w spans remainder).
  - **NEVER use pptxgenjs `bullet: { type: 'number' }`** — it doesn't auto-increment reliably; the items either all show "1" or only the first gets numbered. Bake the numbers into your code (`${i+1}`).

- `divider`: dark background (primary color). `section_label` small at top-third (accent, heading font, uppercase, `charSpacing: 6-8`). `section_title` large centered (heading font white, autosize so two-line titles don't visually outweigh single-line ones — clamp to a max ~48pt for long titles, ~54pt for short). Optional `teaser` smaller below (light gray for legibility on dark, italic body font).

- `assertion-evidence` / `assertion-evidence-left`: workhorse with optional stat callout.
  - **Pre-crop the image to 3:2 with Pillow center-crop** before placing (use the venv: `${CLAUDE_PLUGIN_DATA}/venv/bin/python3`). Save to `images/cropped/`. This keeps visual weight consistent across slides regardless of source aspect.
  - Image at fixed **6.0" × 4.0"** (3:2). On `assertion-evidence`: right side (`x = 13.333 - 0.7 - 6.0 = 6.633`, `y ≈ 2.4`). On `-left`: left side (`x = 0.7`).
  - Headline at top, full-width: `y ≈ 0.55`, `h ≈ 1.2`, ~24pt heading font bold, text color.
  - Optional `caption` below image (10pt italic, muted).
  - **If `stat` AND `stat_label` are both present**: render a callout on the side opposite the image. Big number ~130pt heading font bold in accent color (`y ≈ 2.6`, vertically centered with the image). Below it, `stat_label` in ~16pt body font, muted, single line. This callout pulls the eye and anchors the slide's message.
  - If only one (or neither) of `stat`/`stat_label` is present, omit the callout. Just headline + image, with the free side as intentional whitespace.

- `chart`: `headline` at top (heading font ~28pt, text color, full width at y≈0.6). `chart_image` centered, contained within an area ~11.5" × 4.4" below. Optional `caption` centered below in 10pt italic muted body font.

- `callout`: `big_text` huge centered (~140-200pt depending on length, heading font bold, accent color). `sub_label` below in body font ~18pt, muted, centered, can wrap to a max of two lines. Background light.

- `quote`: `quote_text` large centered italic (~28pt heading font), `attribution` smaller below right-aligned (~14pt body, muted). Optional decorative opening quote-mark glyph in primary color at high transparency (~85%) at top-left as visual texture.

- `comparison`: emphasize the winner — never render two columns identically.
  - `headline` at top (heading font ~30pt, text color, left-aligned).
  - Subtle accent panel behind the winner column (transparency ~92, very low alpha) so the difference is visible without being garish.
  - Vertical separator at x = slide_width/2 in muted, thin (0.75pt).
  - Both labels in heading font ~13pt bold uppercase with `charSpacing: 6` — loser in muted gray, winner in accent.
  - Render each row as a triplet: small label (body 13pt) + big value (heading 30-32pt) + delta indicator. On the loser side: muted color for both label and value, no delta. On the winner side: text color + bold for the value, accent color for the delta indicator (`▲ +13 pp`). If a "delta" represents a cost not a win (e.g., `+7s` more time), keep that one in muted to honestly signal the tradeoff.
  - Today the canonical schema gives this content as flat `left_content` / `right_content` strings. If they contain newline-separated `label: value` pairs, split them into rows; otherwise render as-is.

- `gallery`: 2×2 grid with UNIFORM cells — never let mixed source aspect ratios break the grid.
  - **Pre-crop all 4 images to a single aspect ratio** (default 4:3) via Pillow center-crop. Save to `images/cropped/`. This is non-negotiable; without uniform crops the grid reads as four random photos.
  - Cells at fixed size (e.g., `cellH = 2.35`, `cellW = cellH × 4/3 = 3.13`, `gap = 0.25`). Grid centered horizontally on the slide.
  - Place each cropped image at the exact cell rectangle — `w` and `h` equal cell size — so the image fills the cell with no padding and no distortion (aspect already matches).
  - **Caption position is computed from the grid bottom**, NOT a fixed slide-bottom Y — otherwise it overlaps images when the grid is sized differently. Use `captionY = gridY + 2*cellH + gap + 0.2`.
  - `headline` at top (heading font ~24pt, text color), `caption` below grid (10pt italic muted, centered).

- `fullbleed`: `image_full` covers the entire slide (`x:0, y:0, w:13.333, h:7.5`). If aspect doesn't match 16:9 exactly, accept letterboxing rather than distorting. If `overlay_text` present: render a semi-transparent dark rectangle (rgba ≈ 0,0,0,0.55 via `transparency: 45`) across the bottom ~1.5" of the slide, then `overlay_text` over it in white (~28pt heading font bold, left-aligned with 0.8" margin).

- `closing`: `main_text` centered large (heading font ~80pt bold, primary color, at y≈2.4). `contact_info` smaller centered below (~18pt body, muted) using `breakLine` between fields.

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

### Numbered lists are unreliable in pptxgenjs — bake the numbers manually

PptxGenJS `bullet: { type: 'number' }` does NOT auto-increment correctly across multiple items in a rich-text array. Behavior observed:
- Per-item `options: { bullet: { type: 'number' } }` → every item renders as "1." (each starts a new list).
- Top-level `bullet: { type: 'number' }` on the `addText` call → only the FIRST item gets numbered; rest have no number at all.

For any numbered list (text-list slides, comparison row labels, etc.), bake the numbers into the code: `s.addText(\`\${i+1}\`, {...})` in a separate addText call per row. Don't rely on the bullet system for numbering.

### Text-list wraps lose their hanging indent in rich-text arrays

When using `addText([{...}, {...}])` with embedded "1.   ", "2.   " number prefixes in the same text run, wrapped lines reset to the leftmost text-box x (`x=0.9`), NOT under the start of the item text. This looks broken on items longer than one line.

Fix: render each list item as TWO separate `addText` calls — one for the number (small left-side box), one for the text (wider right-side box that wraps within itself). Each item sits on its own row computed by `y = baseY + i * rowSpacing`.

### Gallery requires pre-cropped images — there is no good in-place workaround

PptxGenJS `sizing: { type: 'cover' | 'contain' }` produces broken XML and is forbidden (see gotcha above). Centering a contain-fit image inside a cell with mixed source aspect ratios produces a chaotic grid where each image floats at a different visible size — even with identical cell rectangles.

The only path that yields a clean 2×2 gallery is **pre-cropping all 4 images to the same aspect ratio** via Pillow center-crop, then placing them at the exact cell rectangle (image fills cell, no distortion because aspect already matches). Default cell aspect: 4:3. Output to `images/cropped/` (gitignore-able). The venv has Pillow.

### Caption Y on gallery must be computed from the grid bottom

A fixed `captionY = 7.05` was the original (broken) approach — it overlapped the bottom row of images whenever the grid extended past that Y. Compute it from the actual grid layout: `captionY = gridY0 + 2*cellH + gap + 0.2`. This makes the caption follow wherever the grid actually ends.

### Pre-crop assertion-evidence images to 3:2 — visual weight must be uniform

Assertion-evidence is the workhorse type and gets used 5-15 times per deck. If the images have varying aspect ratios, the rendered image area varies too (slide N shows a 5.5×3.7 image, slide N+1 shows a 4×4 image), and the hierarchy reads inconsistently. Same fix as gallery: Pillow center-crop to 3:2 before placing, then use a FIXED 6.0"×4.0" rectangle on every assertion-evidence slide.

### `stat` callout is opt-in via narrative.md fields

The big-number callout on the side opposite the image is rendered ONLY when both `stat:` and `stat_label:` are present in the slide's narrative.md entry. If only one is present, ignore both (fall back to plain headline+image). This keeps the rule explicit and gives the narrative writer control over when the callout fires — for slides whose headline doesn't pivot on a single number, the callout would be artificial.

### Comparison MUST differentiate the winner

Two identical-looking columns defeat the purpose of `comparison`. Always render three layers of differentiation: (1) subtle accent panel behind the winner column, (2) winner values in bold + text color (loser values in muted), (3) per-row delta indicator in accent for wins, muted for cost-tradeoffs. A "+7s more time" delta should not visually celebrate itself the way a "+13 pp accuracy" delta does.
