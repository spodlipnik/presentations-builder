# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Source for the **Talk Builder** Claude Code plugin (`.claude-plugin/plugin.json`, name `talk-builder`). It ships an orchestrator + 9 phase skills (`/talk`, `/talk-setup`, `/talk-briefing`, `/talk-vision`, `/talk-research`, `/talk-assets`, `/talk-narrative`, `/talk-slides`, `/talk-study-doc`, `/talk-script`) plus reference guides and one Python helper script.

The plugin is loaded into a user's Claude Code session; its skills act on the user's *current working directory* (their presentation project), not on this repo.

**As of v2.0** (May 2026), `talk-slides` no longer generates PPTX itself — it delegates to the official `document-skills:pptx` skill (Anthropic's marketplace plugin). All theme/role/variant complexity has been removed.

## Repo layout

```
.claude-plugin/         Plugin manifest
.claude/rules/          Lazy-loaded context-specific rules (paths: frontmatter)
.claude/settings.json   Project-level settings (attribution, permissions)
hooks/hooks.json        SessionStart hook: poppler/cairo check + Python venv install
skills/<name>/SKILL.md  Each skill's instructions + frontmatter + Gotchas
references/             Long-form guides (storytelling, slide-design, pacing, data-storytelling)
assets/scripts/         extract_pdfs.py only (Docling-based PDF extraction) + tests
tools/                  Plugin validators (CI utilities)
```

## Where to find more guidance

The most important conventions live in `.claude/rules/*.md` and load automatically when you touch matching paths:

- **Editing any `skills/**`** → `.claude/rules/skills-authoring.md` (frontmatter, language, allowed-tools)
- **Editing skill internals or hooks** → `.claude/rules/runtime-environment.md` (CLAUDE_PLUGIN_ROOT/DATA, venv, orchestration model)
- **Touching cairosvg paths** → `.claude/rules/cairosvg-macos.md` (the libcairo + DYLD gotcha)
- **Editing talk-narrative or talk-slides** → `.claude/rules/canonical-types.md` (12-type schema)

Each `skills/<name>/SKILL.md` also has a `## Gotchas` section documenting that skill's known failure modes.

## Commands

### Tests

```bash
cd assets/scripts && ${CLAUDE_PLUGIN_DATA}/venv/bin/python3 -m pytest tests/ -v
```

### Local plugin loading for development

```bash
claude --plugin-dir ./presentations-builder
```

Bumping `version` in `.claude-plugin/plugin.json` is the canonical release step.

### CI

`.github/workflows/ci.yml` runs ruff + pytest + plugin structural validation on push and PR.

## Things that look like local data but are not committed

`.gitignore` keeps these out of git: `config.yaml` (per-user), `docs/superpowers/`, `evals/`, `talk-*-workspace/`, `.claude/settings.local.json` (per-user overrides). When a skill writes user content, it goes to the user's CWD or `${user_config.assets_path}`, never into this repo.

## Migration from v1.x

v2.0 is a breaking change. v1.x narrative.md files using the 18-role taxonomy will be rejected by `talk-slides`. See `CHANGELOG.md` 2.0.0 entry for the legacy → new type mapping. There is no auto-migration — legacy projects are disposable.
