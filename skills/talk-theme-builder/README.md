# talk-theme-builder

Skill to create and manage presentation themes for the Talk Builder system.

## What is a theme?

A theme is a reusable collection of visual layouts — tokens (colors, fonts, spacing) + roles × variants. Themes are consumed by `talk-slides` when generating presentations.

Users can have multiple themes (one per presentation context: congresses, teaching, patient talks, etc.).

## Prerequisites

- Python 3.9+ with python-pptx, PyYAML, lxml (auto-installed)
- **LibreOffice** (recommended for thumbnail generation): `brew install --cask libreoffice`
- **poppler** (pdftoppm): `brew install poppler`
- A reference PPTX with 15-30 slides representing user's style

## Commands (MVP — Plan 2A)

- `create` — interactive 5-phase workflow to build a new theme

Additional commands (Plan 2B):
- `edit` — refine existing theme
- `list` — list all themes
- `clone`, `delete`

## Workflow

Invoke with: "crear tema", "nuevo tema", or `/talk-theme-builder create`.

### Fase 0: Input + Extraction
User provides reference PPTX. Skill runs `extract_references.py` to produce a structured catalog, and `render_thumbnails.sh` to generate JPGs.

### Fase 1: Clustering + Mapping
Slides grouped by geometric similarity into variants. Each group mapped to one of the 18 canonical roles.

### Fase 2: Review rol-por-rol
User walks through each role's variant candidates. For each: approve, refine, or reject. User names approved variants. Tokens (colors, fonts) are confirmed early.

### Fase 3: Fill gaps (deferred to Plan 2B)
### Fase 4: Sampler deck (deferred to Plan 2B)

### Fase 5: Save + naming
Final theme.yaml written to `${ASSETS_PATH}/themes/<theme-id>/`. Initial backup created.

## Output structure

```
${ASSETS_PATH}/themes/<theme-id>/
├── theme.yaml                  # the final catalog
├── reference-slides.pptx       # user's source file
├── reference-catalog.yaml      # extractor output
├── clusters.yaml               # grouped variants
├── thumbnails/                 # JPG per slide
│   ├── slide-01.jpg
│   └── ...
└── .backups/                   # dated backups (5 max)
```

## Known limitations (MVP)

- Only `create` command implemented
- No gap-filling (roles not in reference are skipped)
- No sampler deck for holistic validation
- No edit/list/clone/delete
- Single paragraph-level font detection (run-level + lstStyle fallback)

See Plan 2B for these features.
