# Talk Builder — Helper Scripts

Standalone Python scripts shipped with the plugin for non-skill operations.

## Scripts

### `extract_pdfs.py`

Pre-extracts all PDFs in a directory into `pdfs/extracted/<paper_name>.md` (Docling-based markdown) plus extracted figure images.

```bash
${CLAUDE_PLUGIN_DATA}/venv/bin/python3 \
  ${CLAUDE_PLUGIN_ROOT}/assets/scripts/extract_pdfs.py \
  pdfs/
```

Used by `talk-research` and `talk-assets`. See those skills for the full workflow.

## Requirements

Python 3.9+ with the packages listed in `requirements.txt`. The plugin's SessionStart hook auto-installs them into `${CLAUDE_PLUGIN_DATA}/venv`.

## Tests

```bash
cd assets/scripts
${CLAUDE_PLUGIN_DATA}/venv/bin/python3 -m pytest tests/ -v
```

Test file: `tests/test_extract_pdfs.py`.
