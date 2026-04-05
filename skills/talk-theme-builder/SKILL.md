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

## Phase 0: Input + Extracción

**Goal:** Get the user's reference PPTX, extract its layout catalog, render thumbnails.

### Steps

**1. Confirm assets_path is configured**

Read `~/.claude/config/talk-builder.yaml` or check userConfig. If not set, ask:

> "No tengo configurado el directorio de tus presentaciones. ¿Dónde quieres guardar tus temas?
> (ej: `~/Presentaciones/talk-themes/`)"

Save the path as `ASSETS_PATH`.

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
THEME_DIR="${ASSETS_PATH}/themes/${THEME_ID}"
mkdir -p "${THEME_DIR}/thumbnails"
```

**5. Copy reference PPTX and extract catalog**

```bash
cp "<user-pptx-path>" "${THEME_DIR}/reference-slides.pptx"
python3 "${CLAUDE_PLUGIN_ROOT}/assets/scripts/extract_references.py" \
  --input "${THEME_DIR}/reference-slides.pptx" \
  --output "${THEME_DIR}/reference-catalog.yaml" \
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
  "${THEME_DIR}/reference-slides.pptx" \
  "${THEME_DIR}/thumbnails" \
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
  --input "${THEME_DIR}/reference-catalog.yaml" \
  --output "${THEME_DIR}/clusters.yaml" \
  --bucket 0.05
```

**2. Load clusters and role-taxonomy**

Read `${THEME_DIR}/clusters.yaml` → list of clusters (each has: role, count, slide_numbers, signature).

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
