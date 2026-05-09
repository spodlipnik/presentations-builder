# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Source for the **Talk Builder** Claude Code plugin (`.claude-plugin/plugin.json`, name `talk-builder`). It is *not* an application — it is a multi-skill plugin that ships an orchestrator + 9 phase skills (`/talk`, `/talk-setup`, `/talk-briefing`, `/talk-vision`, `/talk-research`, `/talk-assets`, `/talk-narrative`, `/talk-slides`, `/talk-study-doc`, `/talk-script`) plus a small set of long-form reference guides and one Python helper script.

The plugin is loaded into a user's Claude Code session; its skills then act on the user's *current working directory* (their presentation project), not on this repo.

**As of v2.0** (May 2026), `talk-slides` no longer generates PPTX itself — it delegates to the official `document-skills:pptx` skill (Anthropic's marketplace plugin). All theme/role/variant complexity has been removed.

## High-level architecture

```
.claude-plugin/         Plugin manifest
hooks/hooks.json        SessionStart hook: poppler check + Python venv install
skills/<name>/SKILL.md  Each skill's instructions + frontmatter
references/             Long-form guides (storytelling, slide-design, pacing, data-storytelling)
assets/scripts/         extract_pdfs.py only (Docling-based PDF extraction) + tests
talk-*-workspace/       Local-only eval/scratch dirs (gitignored)
evals/                  Skill eval JSON files (gitignored)
```

### Two runtime substrate paths

- `${CLAUDE_PLUGIN_ROOT}` — read-only path to *this repo* once installed. Use for reading shipped scripts/refs (`${CLAUDE_PLUGIN_ROOT}/assets/scripts/extract_pdfs.py`, `${CLAUDE_PLUGIN_ROOT}/references/...`).
- `${CLAUDE_PLUGIN_DATA}` — writable per-user data dir (`~/.claude/plugins/data/talk-builder/`). Houses the **persistent venv** (`venv/bin/python3`) populated from `assets/scripts/requirements.txt` (python-pptx, PyYAML, lxml, docling, cairosvg, Pillow). Provisioned by the SessionStart hook.

Skills that shell out to Python **must** prefer `${CLAUDE_PLUGIN_DATA}/venv/bin/python3`, falling back to system `python3` only when the venv is unavailable. There are no Node deps owned by this plugin.

### cairosvg / libcairo gotcha (macOS)

`cairosvg` (the Python lib used by `talk-assets` for SVG→PNG) is a wrapper around the system `libcairo`. On macOS:

1. The system lib must be installed: `brew install cairo`. The SessionStart hook checks for it and warns if missing.
2. macOS Python (CommandLineTools) does NOT search `/opt/homebrew/lib` by default, so even with libcairo present, `import cairosvg` raises `OSError: no library called "cairo-2"`. **Skills that invoke cairosvg MUST prepend `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib:/usr/local/lib:/opt/local/lib`** to the Python command. See `skills/talk-assets/SKILL.md` CHART section for the canonical incantation.

### User config substrate

The plugin's `userConfig.assets_path` (set per user via Claude Code plugin settings) points to the user's external assets dir — this is where `config.yaml`, `example-slides/`, and `fixed-slides/` live. There is no `themes/` directory in v2.0+.

`config.yaml` is the single source of truth for visual style. Its `design_tokens:` section (5 colors + 2 fonts) is read by:
- `talk-assets` for SVG charts/diagrams
- `talk-slides` to pass to `document-skills:pptx` at delegation time

### Skill orchestration model

`/talk` is the only skill the user typically invokes directly. It detects the current project's phase by checking sentinel files and dispatches via `Skill`.

| Sentinel file | Phase complete | Skill that creates it |
|---|---|---|
| `docs/talk.yaml` | Briefing | `talk-briefing` |
| `docs/vision.md` | Vision | `talk-vision` |
| `docs/research.md` | Research | `talk-research` |
| `docs/narrative.md` | Narrative | `talk-narrative` |
| `images/` non-empty | Assets | `talk-assets` |
| `docs/study-document.md` | Study docs | `talk-study-doc` |
| `docs/speaker-script.md` | Script | `talk-script` |
| `presentation.pptx` | Slides | `talk-slides` |

### Slide generation pipeline (v2.0)

`talk-slides` is a thin orchestrator (~150-line SKILL.md). It:

1. Parses `docs/narrative.md` — each slide is a record with `type` (one of 12 canonical types) and typed content fields.
2. Reads `${user_config.assets_path}/config.yaml` for `design_tokens` (colors + fonts).
3. Validates: every `type` is canonical; required fields per type are present; image paths resolve.
4. Builds a structured prose brief listing every slide with explicit visual instructions per type.
5. Invokes `Skill(document-skills:pptx)` with the brief. The official skill provides PptxGenJS guidance, and Claude writes a per-deck `_build/build.js` script following it.
6. Optionally runs the official skill's visual QA loop (subagent inspects rendered JPGs).

**There is no template file**, no `theme.yaml`, no rubric, no variant catalog. The 12 canonical types and their field schemas are documented inline in `skills/talk-slides/SKILL.md` and `skills/talk-narrative/SKILL.md`.

## Commands

### Tests (Python helper)

```bash
cd assets/scripts && ${CLAUDE_PLUGIN_DATA}/venv/bin/python3 -m pytest tests/ -v
```

Test deps: `pip3 install -r assets/scripts/requirements-dev.txt`. The conftest builds real PPTX fixtures with python-pptx (used by `extract_pdfs` tests indirectly).

### Manually exercising the script layer

`extract_pdfs.py` is the only standalone helper now. It runs Docling extraction on a PDF directory:

```bash
${CLAUDE_PLUGIN_DATA}/venv/bin/python3 \
  ${CLAUDE_PLUGIN_ROOT}/assets/scripts/extract_pdfs.py \
  /path/to/pdfs/
```

### Local plugin loading for development

```bash
claude --plugin-dir ./presentations-builder
```

Bumping `version` in `.claude-plugin/plugin.json` is the canonical release step (see git history — `chore: bump version to X.Y.Z`).

## Critical conventions

### Delegation pattern

When a skill needs to invoke another skill (most importantly, when `talk-slides` invokes `document-skills:pptx`), use the `Skill` tool. The invoked skill's instructions become part of the session context — Claude executes them with the data we provide.

For `talk-slides` → `document-skills:pptx`: pass the full structured brief (output path, design_tokens, list of typed slide descriptions with visual instructions) as the prompt. Do not assume any prior shared context.

### `design_tokens` are the only style contract

There is no theme system. The `design_tokens:` block in `config.yaml` is the entire visual contract. Skills that produce visuals (`talk-assets`, `talk-slides`) MUST read it and pass it through. Skills that don't (`talk-vision`, `talk-research`, etc.) ignore it.

### Canonical 12 slide types

The contract between `talk-narrative` (writer) and `talk-slides` (reader) is the 12-type schema. Adding a type means updating both SKILL.md files (and ideally the CHANGELOG migration table). Currently:

`title`, `text-list`, `divider`, `assertion-evidence`, `assertion-evidence-left`, `chart`, `callout`, `quote`, `comparison`, `gallery`, `fullbleed`, `closing`.

### Skill author conventions

- SKILL.md frontmatter `allowed-tools` is enforced — adding a tool the skill doesn't list will fail at runtime. Sub-skills (everything except `talk`) keep `description` worded so the *orchestrator* triggers them, not raw prompts.
- All paths to shared resources in skills must be `${CLAUDE_PLUGIN_ROOT}/...` (marketplace compatibility).
- Skills produce *user-visible* prompts/dialog in **Spanish** by default. Comments in code, internal logs, and reference markdown stay in English.

## Things that look like local data but are not committed

`.gitignore` keeps these out of git: `config.yaml` (per-user), `docs/superpowers/`, `evals/`, and `talk-*-workspace/`. When a skill writes user content, it goes to the user's CWD or `${user_config.assets_path}`, never into this repo.

## Migration from v1.x

This is a breaking change. v1.x narrative.md files using the 18-role taxonomy will be rejected by `talk-slides`. See `CHANGELOG.md` 2.0.0 entry for the legacy → new type mapping.

There is no auto-migration tool — users (per the design discussion) treat legacy projects as disposable.
