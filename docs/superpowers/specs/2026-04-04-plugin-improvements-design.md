# Talk Builder Plugin — Marketplace & Quality Improvements

**Date:** 2026-04-04
**Status:** Approved
**Approach:** Plugin-Grade (Enfoque B)

## Context

Talk Builder is a 10-skill Claude Code plugin for building academic/medical presentations. Currently works with `--plugin-dir` but has structural issues that prevent correct marketplace installation and lacks features for a professional plugin experience.

Analysis against official Claude Code plugin documentation (https://code.claude.com/docs/en/plugins) revealed critical path issues, missing frontmatter fields, and opportunities for better UX.

## Goals

- Plugin installs and works correctly from a marketplace
- Sub-skills are not auto-invoked by Claude (only orchestrator is)
- Tools are pre-approved per skill for smoother UX
- Dependencies are validated at session start
- node_modules persist across projects via CLAUDE_PLUGIN_DATA
- MCP tools (PubMed/Consensus) degrade gracefully with clear user guidance
- Documentation ready for public distribution

## Non-Goals

- Refactoring skill internals or moving references into skill directories (Enfoque C)
- Making the plugin self-contained without PPTX plugin dependency
- Packaging MCP servers within the plugin

---

## Section 1: Plugin Structure and Manifest

### Move plugin.json

Move `plugin.json` from root to `.claude-plugin/plugin.json` (required location per docs).
Delete the root-level `plugin.json`.

### Unify version

Remove `version` field from `.claude-plugin/marketplace.json`. The `plugin.json` is the single source of truth. Set version to `1.0.0`.

### Add metadata fields

Final `plugin.json`:

```json
{
  "name": "talk-builder",
  "version": "1.0.0",
  "description": "Multi-skill plugin for building academic and medical presentations with storytelling, from research to PPTX and speaker scripts",
  "author": { "name": "Sebastian Podlipnik" },
  "homepage": "https://github.com/sebastianpodlipnik/talk-builder",
  "repository": "https://github.com/sebastianpodlipnik/talk-builder",
  "license": "MIT",
  "keywords": ["presentations", "academic", "medical", "storytelling", "slides", "pptx", "speaker-script"]
}
```

### marketplace.json changes

Remove `version` field. Keep everything else. Result:

```json
{
  "name": "talk-builder",
  "description": "Multi-skill plugin for building academic and medical presentations with storytelling, from research to PPTX and speaker scripts",
  "owner": { "name": "Sebastian Podlipnik" },
  "plugins": [
    {
      "name": "talk-builder",
      "description": "Complete presentation building skills suite — orchestrator, research, narrative, slides, documents, and speaker scripts",
      "source": "./",
      "strict": false,
      "skills": [
        "./skills/talk",
        "./skills/talk-setup",
        "./skills/talk-briefing",
        "./skills/talk-vision",
        "./skills/talk-research",
        "./skills/talk-assets",
        "./skills/talk-narrative",
        "./skills/talk-slides",
        "./skills/talk-study-doc",
        "./skills/talk-script"
      ]
    }
  ]
}
```

---

## Section 2: Skill Frontmatter

### disable-model-invocation

All sub-skills get `disable-model-invocation: true`. Only the orchestrator `/talk` remains auto-invocable by Claude.

### argument-hint

- `talk`: `"[topic or phase]"`
- `talk-briefing`: `"[topic]"`
- All others: no argument-hint (they work with project files)

### allowed-tools per skill

| Skill | allowed-tools |
|---|---|
| `talk` | `Read Glob Bash Skill` |
| `talk-setup` | `Read Write Bash Glob` |
| `talk-briefing` | `Read Write Bash` |
| `talk-vision` | `Read Write` |
| `talk-research` | `Read Write Glob Grep WebSearch WebFetch mcp__claude_ai_PubMed__search_articles mcp__claude_ai_PubMed__get_article_metadata mcp__claude_ai_PubMed__get_full_text_article mcp__claude_ai_Consensus__search` |
| `talk-assets` | `Read Write Bash Glob` |
| `talk-narrative` | `Read Write Glob` |
| `talk-slides` | `Read Write Bash Glob Skill` |
| `talk-study-doc` | `Read Write Glob` |
| `talk-script` | `Read Write Glob` |

---

## Section 3: Plugin Root Paths

All skill references to files bundled with the plugin must use `${CLAUDE_PLUGIN_ROOT}` instead of relative paths. This ensures paths resolve correctly when installed from a marketplace (plugin gets cached at `~/.claude/plugins/cache/`).

### Paths to update

| Skill | Current path | New path |
|---|---|---|
| `talk-narrative` | `references/storytelling-guide.md` | `${CLAUDE_PLUGIN_ROOT}/references/storytelling-guide.md` |
| `talk-narrative` | `references/slide-design-guide.md` | `${CLAUDE_PLUGIN_ROOT}/references/slide-design-guide.md` |
| `talk-narrative` | `references/pacing-guide.md` | `${CLAUDE_PLUGIN_ROOT}/references/pacing-guide.md` |
| `talk-slides` | `references/slide-design-guide.md` | `${CLAUDE_PLUGIN_ROOT}/references/slide-design-guide.md` |
| `talk-slides` | `references/data-storytelling.md` | `${CLAUDE_PLUGIN_ROOT}/references/data-storytelling.md` |
| `talk-assets` | `references/data-storytelling.md` | `${CLAUDE_PLUGIN_ROOT}/references/data-storytelling.md` (if referenced) |
| `talk-script` | `references/teleprompter-format.md` | `${CLAUDE_SKILL_DIR}/references/teleprompter-format.md` (supporting file within skill) |

### Scan requirement

Read every SKILL.md to identify ALL paths to `references/` files. The table above is based on known references but must be verified by reading each file.

---

## Section 4: MCP Tools — Optional with Pause and User Choice

### Change in talk-research SKILL.md

Add a "Tool Availability Check" section before any search logic:

```markdown
## Tool Availability Check

Before starting any search, check if these tools are available:
- mcp__claude_ai_PubMed__search_articles
- mcp__claude_ai_Consensus__search

If ANY of them is NOT available, STOP and tell the user:

"The following recommended tools are not available:
- [list missing tools]

These tools provide structured medical literature search with
verified references. Without them, I'll use general web search
which produces less precise results.

To connect them: claude.ai > Settings > MCP Servers > activate
PubMed and/or Consensus.

Would you like to connect them before we continue, or proceed
with web search only?"

Wait for the user's response. Only proceed after they explicitly
choose to continue or confirm they have connected the tools.
```

---

## Section 5: SessionStart Hook for Dependency Validation

### New file: hooks/hooks.json

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "missing=\"\"; which pdftoppm >/dev/null 2>&1 || missing=\"$missing\n  - poppler (brew install poppler) — required for PDF image extraction\"; which node >/dev/null 2>&1 || missing=\"$missing\n  - Node.js (brew install node) — required for PPTX generation\"; if [ -n \"$missing\" ]; then printf '{\"result\": \"warn\", \"message\": \"Talk Builder: missing dependencies:%s\"}' \"$missing\"; fi"
          },
          {
            "type": "command",
            "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/assets/package.json\" \"${CLAUDE_PLUGIN_DATA}/package.json\" >/dev/null 2>&1 || (cp \"${CLAUDE_PLUGIN_ROOT}/assets/package.json\" \"${CLAUDE_PLUGIN_DATA}/\" && cd \"${CLAUDE_PLUGIN_DATA}\" && npm install --silent) || rm -f \"${CLAUDE_PLUGIN_DATA}/package.json\""
          }
        ]
      }
    ]
  }
}
```

**Behavior:**
- First hook: warns if poppler or Node.js missing. Silent if both present.
- Second hook: installs PptxGenJS to CLAUDE_PLUGIN_DATA if not present or outdated. Pattern from official docs.

---

## Section 6: Persistent node_modules via CLAUDE_PLUGIN_DATA

### New file: assets/package.json

Base package.json with PptxGenJS dependency:

```json
{
  "name": "talk-builder-deps",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "pptxgenjs": "^3.12.0"
  }
}
```

### Change in talk-slides SKILL.md

Update the section about node dependencies:

```markdown
## Node Dependencies

PptxGenJS is pre-installed in the plugin's persistent data directory.
When executing the generation script, set NODE_PATH:

  NODE_PATH=${CLAUDE_PLUGIN_DATA}/node_modules node _build/generate_presentation.js

If the command fails with a module not found error, run:

  cd ${CLAUDE_PLUGIN_DATA} && npm install

Do NOT install node_modules inside _build/. Always use CLAUDE_PLUGIN_DATA.
```

### Remove _build/node_modules cleanup from talk orchestrator

The orchestrator currently offers to clean `_build/node_modules/`. This is no longer needed since node_modules lives in CLAUDE_PLUGIN_DATA. Update the orchestrator to remove this check. Keep the check for `_build/` generation scripts.

---

## Section 7: Documentation

### README.md (root)

Standard plugin documentation with:
- Feature overview
- Requirements (poppler, Node.js, PPTX plugin, PubMed/Consensus recommended)
- Installation instructions (marketplace)
- Quick start (setup → new dir → /talk)
- Skills table (10 skills with purpose)
- License

### LICENSE (root)

MIT license, Sebastian Podlipnik, 2026.

### CHANGELOG.md (root)

Initial entry for 1.0.0 with all features listed.

---

## Section 8: .gitignore Updates

```gitignore
config.yaml
.DS_Store
docs/superpowers/
```

Changes:
- Remove `assets/` exclusion (assets/ now contains package.json for the plugin)
- Add `.DS_Store`
- Add `docs/superpowers/` (development artifacts, not part of distributed plugin)

---

## Files Changed Summary

| Action | File |
|---|---|
| DELETE | `plugin.json` (root) |
| CREATE | `.claude-plugin/plugin.json` (moved + enhanced) |
| EDIT | `.claude-plugin/marketplace.json` (remove version) |
| EDIT | `skills/talk/SKILL.md` (allowed-tools, argument-hint) |
| EDIT | `skills/talk-setup/SKILL.md` (disable-model-invocation, allowed-tools) |
| EDIT | `skills/talk-briefing/SKILL.md` (disable-model-invocation, allowed-tools, argument-hint) |
| EDIT | `skills/talk-vision/SKILL.md` (disable-model-invocation, allowed-tools) |
| EDIT | `skills/talk-research/SKILL.md` (disable-model-invocation, allowed-tools, MCP check) |
| EDIT | `skills/talk-assets/SKILL.md` (disable-model-invocation, allowed-tools, paths) |
| EDIT | `skills/talk-narrative/SKILL.md` (disable-model-invocation, allowed-tools, paths) |
| EDIT | `skills/talk-slides/SKILL.md` (disable-model-invocation, allowed-tools, paths, PLUGIN_DATA) |
| EDIT | `skills/talk-study-doc/SKILL.md` (disable-model-invocation, allowed-tools) |
| EDIT | `skills/talk-script/SKILL.md` (disable-model-invocation, allowed-tools, SKILL_DIR path) |
| CREATE | `hooks/hooks.json` |
| CREATE | `assets/package.json` |
| CREATE | `README.md` |
| CREATE | `LICENSE` |
| CREATE | `CHANGELOG.md` |
| EDIT | `.gitignore` |
