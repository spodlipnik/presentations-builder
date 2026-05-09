---
description: Conventions for authoring SKILL.md files in talk-builder
paths:
  - "skills/**"
---

# Skills authoring conventions

These conventions apply when editing any `skills/<name>/SKILL.md`.

## Frontmatter

- `name` MUST equal the directory name. Mismatch causes runtime failures when the orchestrator dispatches.
- `description` is a *trigger*, not a summary. Write "Use when …" — describe when the skill should fire, not what it does.
- `allowed-tools` is enforced at runtime. Adding a tool the skill doesn't list will fail. Conversely, listing extra tools the skill never uses is dead config.
- Sub-skills (everything except `talk`) keep `description` worded so the orchestrator triggers them, not raw user prompts. The orchestrator is the single user-facing entry point.

## Path references

All paths to shared resources MUST be `${CLAUDE_PLUGIN_ROOT}/...` (marketplace compatibility — relative paths break once installed).

For the plugin's writable data dir, use `${CLAUDE_PLUGIN_DATA}/...` — the SessionStart hook provisions a Python venv there at `${CLAUDE_PLUGIN_DATA}/venv/bin/python3`.

## User-facing language

Skills produce user-visible prompts and dialog in **Spanish** by default (this is a Spanish-speaking medical/academic user base). Comments in code, internal logs, error messages from `Bash`, and reference markdown stay in English.

When the user writes in Spanish but `config.language` is `en` (or vice versa), follow the user's evident language. `config.language` is fallback for ambiguous short messages only.

## Gotchas section

Every SKILL.md should have a `## Gotchas` section near the end documenting failure modes discovered over time. New gotchas are added by the maintainer; do not invent them speculatively.
