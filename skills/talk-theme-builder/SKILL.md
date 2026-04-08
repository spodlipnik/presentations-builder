---
name: talk-theme-builder
description: Use when user wants to create, edit, or manage presentation themes for the Talk Builder system. Triggers when user says "crear tema", "create theme", "nuevo tema", "edit theme", "talk-theme-builder", or similar. Walks user through co-creation of themes from their reference PPTX slides.
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
- Python deps in plugin venv: always use `${CLAUDE_PLUGIN_DATA}/venv/bin/python3` (auto-created by SessionStart hook, includes python-pptx, PyYAML, lxml). Fall back to `python3` only if venv is unavailable.

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

## Phase 0: Input + Extracción

**Goal:** Get the user's reference PPTX, extract its layout catalog, render thumbnails.

### Steps

**1. Confirm assets_path is configured**

Check `${user_config.assets_path}`. If not set, tell the user to configure it via plugin settings or run `/talk-builder:talk-setup`.

**2. Ask for reference PPTX**

> "Para crear un tema, necesito un PPTX tuyo con 15-30 slides que representen tu estilo. ¿Cuál quieres usar?"

If the user gives a path, verify it exists. If they don't have one ready:
> "Necesitas al menos un PPTX para extraer tu estilo. Cuando lo tengas, vuelve a ejecutar `/talk-theme-builder create`."

Exit gracefully.

**3. Ask for theme ID (working name)**

> "¿Qué nombre quieres darle a este tema? Usa kebab-case (ej: `derma-congresos-2026`, `teaching-residentes`). Puedes cambiarlo al final."

Validate: `[a-z0-9-]+`. Save as `THEME_ID`.

**4. Create theme directory**

```bash
THEME_DIR="${user_config.assets_path}/themes/${THEME_ID}"
mkdir -p "${THEME_DIR}/assets" "${THEME_DIR}/_dev" "${THEME_DIR}/_reference/thumbnails"
```

Theme directory structure:
```
{THEME_ID}/
├── theme.yaml              ← the theme catalog (only thing that matters long-term)
├── assets/                 ← personal assets: presenter photo, QR, logos
├── .backups/               ← automatic backups
├── _dev/                   ← generated scripts + outputs (gitignore-friendly)
│   ├── generate_sampler.js
│   ├── sampler.pptx
│   └── sampler_thumbs/
└── _reference/             ← extraction data (do not modify)
    ├── reference-slides.pptx
    ├── reference-catalog.yaml
    ├── clusters.yaml
    └── thumbnails/
```

**5. Copy reference PPTX and extract catalog**

```bash
cp "<user-pptx-path>" "${THEME_DIR}/_reference/reference-slides.pptx"
python3 "${CLAUDE_PLUGIN_ROOT}/assets/scripts/extract_references.py" \
  --input "${THEME_DIR}/_reference/reference-slides.pptx" \
  --output "${THEME_DIR}/_reference/reference-catalog.yaml" \
  --theme-name "${THEME_ID}"
```

**6. Render thumbnails**

Check if LibreOffice is available:
```bash
which soffice
```

If YES:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/assets/scripts/render_thumbnails.sh" \
  "${THEME_DIR}/_reference/reference-slides.pptx" \
  "${THEME_DIR}/_reference/thumbnails" \
  100
```

If NO:
> "⚠️ LibreOffice no está instalado. No podré mostrarte thumbnails visuales de tus slides. Puedo seguir con descripciones de texto de cada slide, pero recomiendo instalar LibreOffice para mejor experiencia: `brew install --cask libreoffice`. ¿Continuamos sin thumbnails?"

Wait for user confirmation. If they accept, proceed without thumbnails (set `HAS_THUMBNAILS=false`). If they want to install first, exit gracefully.

**7. Report what was extracted**

Read the catalog and summarize:

> "✅ Listo. Extraje:
> - **N slides** de `reference-slides.pptx`
> - **X fuentes** dominantes detectadas: {list top 3}
> - **Y colores** dominantes detectados: {list top 3}
> - **Tema del archivo**: major={major_latin}, minor={minor_latin}
> - **Aspect ratio**: {16:9 | 4:3 | custom}
>
> Siguiente fase: agrupar slides similares en patrones."

Then proceed to Phase 1.

---

## Phase 1: Clustering + Mapping

**Goal:** Group similar slides into variant candidates and map each group to a canonical role.

### Steps

**1. Run clustering**

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/assets/scripts/cluster_slides.py" \
  --input "${THEME_DIR}/_reference/reference-catalog.yaml" \
  --output "${THEME_DIR}/_reference/clusters.yaml" \
  --bucket 0.05
```

**2. Load clusters and role-taxonomy**

Read `${THEME_DIR}/_reference/clusters.yaml` → list of clusters (each has: role, count, slide_numbers, signature).

Read `${CLAUDE_PLUGIN_ROOT}/references/role-taxonomy.md` to know the 18 canonical roles.

**3. Group clusters by inferred role**

Build a map `{role_id: [cluster1, cluster2, ...]}`.

Example result:
```
title: [cluster_A (1 slide)]
assertion-evidence: [cluster_B (12 slides), cluster_C (8 slides)]
image-gallery: [cluster_D (5 slides), cluster_E (3 slides)]
quote-pullout: [cluster_F (2 slides)]
unknown: [cluster_G (4 slides)]
```

**4. Report to user**

> "🔍 Encontré **N variantes** cubriendo **M roles**:
>
> | Rol | Variantes | Slides |
> |---|---|---|
> | title | 1 | #1 |
> | assertion-evidence | 2 | 12 + 8 |
> | image-gallery | 2 | 5 + 3 |
> | quote-pullout | 1 | 2 |
> | unknown | 1 | 4 |
>
> **Roles sin cobertura** (faltan): disclosure, agenda, section-divider, patient-case, methodology, data-chart, data-table, comparison, image-fullbleed, timeline-process, key-takeaway, poll-question, contact, closing.
>
> En Fase 2 vamos a revisar cada rol juntos y decidir qué variantes conservar. Los roles sin cobertura se **omitirán** en esta versión (podrás añadirlos más tarde con `talk-theme-builder edit`).
>
> ¿Continuamos con la revisión rol-por-rol?"

Wait for confirmation. If user says "no" or "stop", save current state to `${THEME_DIR}/state.yaml` and exit.

**5. Handle clusters with role="unknown"**

For each cluster with `role="unknown"`, show the representative slide and ask:
> "Este cluster ({count} slides) no se pudo clasificar automáticamente. ¿Qué rol asignarle? Opciones: title, disclosure, agenda, section-divider, assertion-evidence, patient-case, methodology, data-chart, data-table, comparison, quote-pullout, image-fullbleed, image-gallery, timeline-process, key-takeaway, poll-question, contact, closing, SKIP."

If user says SKIP, remove the cluster. Otherwise, update the cluster's role.

---

## Phase 2: Review rol-por-rol

**Goal:** Walk through each role's variant candidates with the user, validating or rejecting each, refining specs, naming final variants.

**This is the heart of the skill.** It's conversational and takes time. Save state after every role.

### Global flow

Iterate through roles in this order (following narrative importance):

1. `title`
2. `disclosure`
3. `agenda`
4. `section-divider`
5. `assertion-evidence`
6. `patient-case`
7. `methodology`
8. `data-chart`
9. `data-table`
10. `comparison`
11. `quote-pullout`
12. `image-fullbleed`
13. `image-gallery`
14. `timeline-process`
15. `key-takeaway`
16. `poll-question`
17. `contact`
18. `closing`

For each role:
- If the role has clusters → review each cluster as a variant candidate
- If no clusters (role not detected) → skip (Plan 2A scope), note in summary

### Per-role review loop

For role `R` with clusters `[C1, C2, ...]`:

**1. Introduce the role to user**

> "### Rol: `R`
>
> {Brief description from role-taxonomy.md}
>
> Detecté **{len(clusters)} variantes** para este rol:"

**2. For each cluster, present the representative slide**

If `HAS_THUMBNAILS=true`:
> "**Variante candidata 1**: slide #{representative_slide_number} (aparece {count} veces)
>
> Mírala aquí: `{THEME_DIR}/_reference/thumbnails/slide-{NN}.jpg`
>
> Layout: {N shapes}
> {For each shape: type, position, font (if text)}"

If `HAS_THUMBNAILS=false`:
> "**Variante candidata 1**: slide #{representative_slide_number} (aparece {count} veces)
>
> {Describe the layout textually: shape types, rough positions, font info}"

**3. Ask user to decide**

> "Para esta variante:
> - **(a) ACEPTAR** — la conservamos como variante del rol `R`
> - **(r) REFINAR** — conservarla pero ajustar algo (font size, position, color)
> - **(x) RECHAZAR** — descartarla
> - **(s) SKIP** — dejar de revisar este rol"

**4. Handle user choice**

**If ACEPTAR:**
- Ask for variant ID: "¿Nombre de la variante? Sugerencia: `{role-short}.{descriptor}` (ej: `ae.image-right`, `title.centered`)"
- Validate ID format: `[a-z0-9-]+\.[a-z0-9-]+`
- Build the variant entry with: id, description (ask user), slots (infer from shapes), layout (from signature boxes), thumbnail path.
- Append to the theme's `roles.{R}.variants[]` list.
- **Save state immediately** to `${THEME_DIR}/theme.yaml.wip`.

**If REFINAR:**
- Ask: "¿Qué quieres ajustar? Opciones: font size, position, color, alignment, padding, o describe el cambio en palabras."
- Apply the change to the variant's layout.
- Show the updated spec and ask "¿Así está bien? (yes/no)"
- Loop until user approves. Then save as in ACEPTAR.

**If RECHAZAR:**
- Skip this cluster, move to next.

**If SKIP:**
- Stop reviewing this role, move to next role.

**5. After all clusters for role reviewed**

Report:
> "Rol `R` completado: {N} variantes aprobadas — {list of variant IDs}. Siguiente rol: `{next_role}`."

**6. State persistence**

After every variant approval or refinement, write current state to `${THEME_DIR}/theme.yaml.wip`. This allows resumption if the session is interrupted.

### Slot defaults (assets/)

Slots in variant definitions can have a `default:` field that points to a file in `assets/` or a text string. This allows recurring content (presenter photo, QR, logos, contact info) to be pre-filled automatically in every presentation without requiring narrative specification.

**When building variant entries**, for slots that typically have recurring content, ask the user:

> "Este slot (`photo`) se repite en varias variantes. ¿Tienes una imagen que quieras usar siempre? Si es así, colócala en `assets/` y la configuro como default."

**Slot default examples in theme.yaml:**

```yaml
contact.card-centered:
  slots:
    photo:
      type: image
      position: { x: 0.05, y: 0.15, w: 0.25, h: 0.7 }
      fit: cover
      default: "assets/presenter-photo.png"    # auto-filled
    qr:
      type: image
      position: { x: 0.75, y: 0.3, w: 0.2, h: 0.35 }
      fit: contain
      default: "assets/qr-code.png"
    name:
      type: text
      default: "Dr. Sebastian Podlipnik"
    email:
      type: text
      default: "s.podlipnik@example.com"
```

**Roles that benefit most from defaults:** `title`, `contact`, `disclosure`, `closing`.

**Rule:** Defaults are overridden if the narrative specifies a value for that slot. If no value in narrative AND no default → slot is left empty (placeholder).

### Token extraction from first few variants

**During review of the first 2-3 variants**, also capture the theme's tokens. Ask user:

> "Antes de seguir, confirmemos los tokens del tema (los colores y fuentes que usarás en TODAS las variantes).
>
> Detecté estas fuentes en tus slides:
> - {font1} ({count1} usos)
> - {font2} ({count2} usos)
> ...
>
> ¿Cuál quieres como fuente principal para TÍTULOS? ¿Y para CUERPO DE TEXTO?"

Save user's choices as `tokens.typography.heading` and `tokens.typography.body`.

> "Para los colores, detecté:
> - {color1} ({count1} usos) — {hex}
> - {color2} ({count2} usos) — {hex}
> ...
>
> ¿Cuál es tu color primario (el de la marca)? ¿Y el de acento? ¿Y el texto base?"

Save as `tokens.color.primary`, `tokens.color.accent`, `tokens.color.text`.

**Auto-detect background**: usually white (#FFFFFF). If detected otherwise, confirm with user.

### Completion check

When done with all roles:

> "🎉 Fase 2 completada. Resumen:
> - **Tokens**: {heading font}, {body font}, {primary color}, {accent color}
> - **Roles con variantes**: {count}
> - **Variantes totales**: {sum}
>
> Roles sin variantes (omitidos en esta versión): {list}.
>
> Podrás añadir esos roles con `talk-theme-builder edit` más adelante.
>
> Siguiente: guardar el tema (Fase 5)."

---

## Phase 4: Real-Asset Preview (optional)

**Goal:** Generate a PPTX with real images (not colored rectangles) for visual QA of key variants.

**When to trigger:** After Phase 2 completion, if the user has placed assets in `assets/` (photo, QR, logos), offer:

> "¿Quieres ver una preview con los assets reales (foto, QR, logos) para las slides de título y contacto? Esto te dará una idea más fiel del resultado final."

If user accepts:

**1. Create preview script per variant:**

Write `_dev/preview_{variant_id}.js` for each requested variant. The script:
- Reads `../theme.yaml` (from `_dev/` parent)
- Resolves `default:` values for each slot (images → `../assets/...`, text → hardcoded defaults)
- Generates PPTX with real images at exact normalized coordinates
- Uses `imgCover()` / `imgContain()` helpers (NOT pptxgenjs `sizing` — it's broken)
- Outputs to `_dev/preview_{variant_id}.pptx`

**2. Image placement rules:**

DO NOT use `sizing: { type: "cover" }` or `sizing: { type: "contain" }` — they are broken in pptxgenjs. Use the helper functions from talk-slides instead:

```javascript
// fit: cover → pre-crop with smart_crop.py, then insert flat
imgCover(slide, imgPath, slot.position.x, slot.position.y, slot.position.w, slot.position.h);

// fit: contain → calculate dimensions manually, center in box
imgContain(slide, imgPath, slot.position.x, slot.position.y, slot.position.w, slot.position.h);
```

See `skills/talk-slides/SKILL.md` → "Image placement" section for full implementation of these helpers.

**3. Convert to PNG for review:**

```bash
soffice --headless --convert-to png --outdir "${THEME_DIR}/_dev" "${THEME_DIR}/_dev/preview_{variant_id}.pptx"
```

Then show the PNG to the user with Read tool for visual feedback.

**Variants that benefit most:** `title.*` (photo + QR + logos), `contact.*` (photo + QR + logos), any variant with `default:` image assets.

**4. Iterate:** If user wants adjustments, modify the variant in `theme.yaml.wip` and regenerate preview.

---

## Phase 5: Save + Naming

**Goal:** Confirm theme name and write the final theme.yaml.

### Steps

**1. Confirm theme name**

> "Ya tienes el tema listo. ¿Confirmas el nombre `{THEME_ID}` o quieres cambiarlo?"

If changes, validate format ([a-z0-9-]+) and rename directory:
```bash
mv "${user_config.assets_path}/themes/${OLD_ID}" "${user_config.assets_path}/themes/${NEW_ID}"
```

**2. Ask for description**

> "Dame una descripción breve (1-2 frases) del propósito de este tema:"

Save as `theme.description`.

**3. Finalize theme.yaml**

Read the WIP file `${THEME_DIR}/theme.yaml.wip`, add:
- `theme.id`: confirmed ID
- `theme.name`: human-friendly version of ID
- `theme.version`: "1.0"
- `theme.description`: from step 2
- `theme.created`: today's ISO date
- `theme.updated`: today's ISO date

Write to `${THEME_DIR}/theme.yaml` (final, without `.wip`).

Validate it's parseable YAML:
```bash
python3 -c "import yaml; yaml.safe_load(open('${THEME_DIR}/theme.yaml'))" && echo "Valid"
```

**4. Remove WIP file**

```bash
rm "${THEME_DIR}/theme.yaml.wip"
```

**5. Create initial backup**

```bash
bash "${CLAUDE_PLUGIN_ROOT}/assets/scripts/backup_theme.sh" "${THEME_DIR}/theme.yaml"
```

**6. Final report**

> "🎉 Tema `{THEME_ID}` guardado en `${THEME_DIR}`.
>
> **Archivos generados:**
> - `theme.yaml` — el catálogo del tema
> - `assets/` — tus assets personales (foto, QR, logos)
> - `_reference/reference-slides.pptx` — fuente original
> - `_reference/reference-catalog.yaml` — datos crudos de extracción
> - `_reference/thumbnails/` — {N} JPGs de tus slides
> - `_reference/clusters.yaml` — agrupación de slides
> - `_dev/` — scripts y outputs generados
> - `.backups/` — backup inicial
>
> **Para usarlo en una presentación**: en tu `docs/talk.yaml`, añade `theme: {THEME_ID}` y corre `/talk-slides`.
>
> **Para refinar este tema más adelante**: `/talk-theme-builder edit {THEME_ID}` (disponible en Plan 2B).
>
> ¿Quieres crear otro tema ahora o terminamos?"
