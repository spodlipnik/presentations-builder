---
description: Runtime substrate paths for talk-builder (CLAUDE_PLUGIN_ROOT, CLAUDE_PLUGIN_DATA, venv)
paths:
  - "skills/**"
  - "hooks/**"
  - "assets/**"
---

# Runtime environment

Two substrate paths govern where things live:

- `${CLAUDE_PLUGIN_ROOT}` — read-only path to the installed plugin repo. Use for shipped scripts and references:
  - `${CLAUDE_PLUGIN_ROOT}/assets/scripts/extract_pdfs.py`
  - `${CLAUDE_PLUGIN_ROOT}/references/<guide>.md`
- `${CLAUDE_PLUGIN_DATA}` — writable per-user data dir (`~/.claude/plugins/data/talk-builder/`). Houses the persistent venv at `${CLAUDE_PLUGIN_DATA}/venv/bin/python3`. Provisioned by the SessionStart hook from `assets/scripts/requirements.txt` (python-pptx, PyYAML, lxml, docling, cairosvg, Pillow).

## Python invocation

Skills that shell out to Python MUST prefer `${CLAUDE_PLUGIN_DATA}/venv/bin/python3` and only fall back to system `python3` when the venv is unavailable. The venv is what guarantees the dependency set; the system Python is uncontrolled.

## No Node deps

Talk Builder does not own any Node.js dependencies as of v2.0. The official `document-skills:pptx` skill manages its own pptxgenjs install (`npm install -g pptxgenjs`).

## Skill orchestration

`/talk` is the only user-invoked skill. It detects project phase by sentinel-file presence and dispatches via the `Skill` tool to the right phase skill:

| Sentinel file | Phase | Dispatch target |
|---|---|---|
| `docs/talk.yaml` | Briefing | `talk-briefing` |
| `docs/vision.md` | Vision | `talk-vision` |
| `docs/research.md` | Research | `talk-research` |
| `docs/narrative.md` | Narrative | `talk-narrative` |
| `images/` non-empty | Assets | `talk-assets` |
| `docs/study-document.md` | Study docs | `talk-study-doc` |
| `docs/speaker-script.md` | Script | `talk-script` |
| `presentation.pptx` | Slides | `talk-slides` |

Phase order: briefing → vision → research → narrative → assets → study-doc → script → slides.
