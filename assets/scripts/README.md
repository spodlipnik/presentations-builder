# Reference Extractor Script

Standalone Python script to extract structured layout catalogs from PPTX reference files.

## Purpose

Transforms a reference `.pptx` into a YAML catalog of layouts, fonts, colors, and heuristic role guesses. Used by `talk-theme-builder` skill (Plan 2) but can also be run manually.

## Usage

```bash
python3 extract_references.py \
  --input path/to/reference-slides.pptx \
  --output path/to/catalog.yaml \
  --theme-name "my-theme-name"
```

## Requirements

Python 3.9+ with:
- python-pptx >= 1.0.2
- PyYAML
- lxml

Install: `pip3 install -r requirements.txt`

## Output

YAML file containing:
- `meta` — source file info, extraction timestamp, slide count
- `theme_detection` — dominant fonts, colors, slide dimensions, theme XML colors
- `slides` — per-slide shapes with positions (as slide fractions), fonts, text samples, inferred role

## Running Tests

```bash
cd assets/scripts
python3 -m pytest tests/ -v
```

## Notes

- Shape positions are expressed as **fractions** (0-1) of slide dimensions, NOT EMU, for resolution independence.
- Theme colors are extracted directly from `ppt/theme/theme1.xml` (python-pptx does not expose theme->RGB resolution).
- SmartArt is skipped gracefully (not supported by python-pptx).
- Group shapes are flattened recursively into their constituent shapes.
- Inferred roles are heuristic best-guesses — the user validates/corrects them in `talk-theme-builder` Fase 2.

## Additional Scripts (Plan 2A)

### cluster_slides.py
Groups similar slides from a reference catalog into variant patterns.

```bash
python3 cluster_slides.py --input catalog.yaml --output clusters.yaml [--bucket 0.05]
```

### render_thumbnails.sh
Converts a PPTX to per-slide JPGs (requires LibreOffice + poppler).

```bash
bash render_thumbnails.sh input.pptx output-dir [dpi]
```

### backup_theme.sh
Creates dated backup of theme.yaml, keeps last 5.

```bash
bash backup_theme.sh path/to/theme.yaml
```
