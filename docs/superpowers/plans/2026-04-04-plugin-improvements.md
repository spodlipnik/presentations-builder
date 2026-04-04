# Talk Builder Plugin Improvements — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Talk Builder plugin marketplace-ready with correct structure, robust frontmatter, path resolution, dependency validation, and documentation.

**Architecture:** Fix plugin manifest location, enhance all 10 skill frontmatters, replace relative paths with `${CLAUDE_PLUGIN_ROOT}`, add SessionStart hooks, use `${CLAUDE_PLUGIN_DATA}` for persistent deps, and create distribution docs.

**Tech Stack:** Claude Code plugin system, Markdown/YAML, JSON, shell scripts

---

## File Structure

| Action | File |
|---|---|
| DELETE | `plugin.json` (root) |
| CREATE | `.claude-plugin/plugin.json` (moved + enhanced) |
| EDIT | `.claude-plugin/marketplace.json` |
| EDIT | `skills/talk/SKILL.md` |
| EDIT | `skills/talk-setup/SKILL.md` |
| EDIT | `skills/talk-briefing/SKILL.md` |
| EDIT | `skills/talk-vision/SKILL.md` |
| EDIT | `skills/talk-research/SKILL.md` |
| EDIT | `skills/talk-assets/SKILL.md` |
| EDIT | `skills/talk-narrative/SKILL.md` |
| EDIT | `skills/talk-slides/SKILL.md` |
| EDIT | `skills/talk-study-doc/SKILL.md` |
| EDIT | `skills/talk-script/SKILL.md` |
| CREATE | `hooks/hooks.json` |
| CREATE | `assets/package.json` |
| CREATE | `README.md` |
| CREATE | `LICENSE` |
| CREATE | `CHANGELOG.md` |
| EDIT | `.gitignore` |

---

### Task 1: Move plugin.json and fix manifest

**Files:**
- Delete: `plugin.json` (root)
- Create: `.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Create new `.claude-plugin/plugin.json`**

Write this file:

```json
{
  "name": "talk-builder",
  "version": "1.0.0",
  "description": "Multi-skill plugin for building academic and medical presentations with storytelling, from research to PPTX and speaker scripts",
  "author": {
    "name": "Sebastian Podlipnik"
  },
  "homepage": "https://github.com/sebastianpodlipnik/talk-builder",
  "repository": "https://github.com/sebastianpodlipnik/talk-builder",
  "license": "MIT",
  "keywords": ["presentations", "academic", "medical", "storytelling", "slides", "pptx", "speaker-script"]
}
```

- [ ] **Step 2: Remove `version` from marketplace.json**

Edit `.claude-plugin/marketplace.json` — remove the `"version": "1.0.0",` line. Result:

```json
{
  "name": "talk-builder",
  "description": "Multi-skill plugin for building academic and medical presentations with storytelling, from research to PPTX and speaker scripts",
  "owner": {
    "name": "Sebastian Podlipnik"
  },
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

- [ ] **Step 3: Delete root `plugin.json`**

```bash
rm plugin.json
```

- [ ] **Step 4: Verify structure**

```bash
ls .claude-plugin/
```

Expected: `marketplace.json  plugin.json`

- [ ] **Step 5: Commit**

```bash
git add .claude-plugin/plugin.json .claude-plugin/marketplace.json
git rm plugin.json
git commit -m "fix: move plugin.json to .claude-plugin/, unify version to 1.0.0"
```

---

### Task 2: Update orchestrator `/talk` frontmatter

**Files:**
- Modify: `skills/talk/SKILL.md`

- [ ] **Step 1: Update frontmatter**

Replace the frontmatter block (lines 1-4) with:

```yaml
---
name: talk
description: Use when building academic or medical presentations. Main entry point for Talk Builder — orchestrates the full workflow from briefing to final outputs. Triggers when user says "create a presentation", "build a talk", "prepare slides", "presentation about", or invokes /talk.
argument-hint: "[topic or phase]"
allowed-tools:
  - Read
  - Glob
  - Bash
  - Skill
---
```

Note: `disable-model-invocation` is NOT set (defaults to `false`) — this is the only skill Claude can auto-invoke.

- [ ] **Step 2: Remove _build/node_modules cleanup section**

In the "### 5. Detect _build/ directory" section (lines 79-83), replace:

```markdown
### 5. Detect _build/ directory

If a `_build/` directory exists in the project:
- If `_build/node_modules/` exists, offer to clean it up: "Found leftover node_modules in _build/. Want me to delete it to save space? (You can regenerate it anytime with `npm install` inside `_build/`)"
- If `_build/` contains generation scripts (`.js` files), mention: "Previous generation scripts are available in `_build/` — these can be used to regenerate or modify the presentation."
```

With:

```markdown
### 5. Detect _build/ directory

If a `_build/` directory exists in the project and contains generation scripts (`.js` files), mention: "Previous generation scripts are available in `_build/` — these can be used to regenerate or modify the presentation."
```

- [ ] **Step 3: Commit**

```bash
git add skills/talk/SKILL.md
git commit -m "feat(talk): add allowed-tools and argument-hint, remove node_modules cleanup"
```

---

### Task 3: Update talk-setup frontmatter

**Files:**
- Modify: `skills/talk-setup/SKILL.md`

- [ ] **Step 1: Update frontmatter**

Replace lines 1-4 with:

```yaml
---
name: talk-setup
description: Use when setting up Talk Builder for the first time or reconfiguring personal style preferences. Triggers on first /talk invocation if no config exists, or when user says "configure talk builder", "setup talk builder", "change my presentation style".
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
---
```

- [ ] **Step 2: Commit**

```bash
git add skills/talk-setup/SKILL.md
git commit -m "feat(talk-setup): add disable-model-invocation and allowed-tools"
```

---

### Task 4: Update talk-briefing frontmatter

**Files:**
- Modify: `skills/talk-briefing/SKILL.md`

- [ ] **Step 1: Update frontmatter**

Replace lines 1-4 with:

```yaml
---
name: talk-briefing
description: Use when starting a new presentation project. Interactive wizard that collects topic, duration, audience, and preferences. Triggers on "new talk", "new presentation", or when /talk detects no talk.yaml exists.
disable-model-invocation: true
argument-hint: "[topic]"
allowed-tools:
  - Read
  - Write
  - Bash
---
```

- [ ] **Step 2: Commit**

```bash
git add skills/talk-briefing/SKILL.md
git commit -m "feat(talk-briefing): add disable-model-invocation, argument-hint, allowed-tools"
```

---

### Task 5: Update talk-vision frontmatter

**Files:**
- Modify: `skills/talk-vision/SKILL.md`

- [ ] **Step 1: Update frontmatter**

Replace lines 1-4 with:

```yaml
---
name: talk-vision
description: Use when defining the personal angle, message, and emotional intent for a presentation. Interactive conversation to capture the speaker's vision. Triggers when /talk detects talk.yaml exists but no vision.md.
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
---
```

- [ ] **Step 2: Commit**

```bash
git add skills/talk-vision/SKILL.md
git commit -m "feat(talk-vision): add disable-model-invocation and allowed-tools"
```

---

### Task 6: Update talk-research — frontmatter + MCP check

**Files:**
- Modify: `skills/talk-research/SKILL.md`

- [ ] **Step 1: Update frontmatter**

Replace lines 1-4 with:

```yaml
---
name: talk-research
description: Use when researching evidence for a presentation. Iterative phase that searches PubMed, Consensus, reads PDFs, and builds a consolidated research document. Triggers when /talk detects vision.md exists but no research.md.
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - WebSearch
  - WebFetch
  - mcp__claude_ai_PubMed__search_articles
  - mcp__claude_ai_PubMed__get_article_metadata
  - mcp__claude_ai_PubMed__get_full_text_article
  - mcp__claude_ai_Consensus__search
---
```

- [ ] **Step 2: Add MCP tool availability check**

After line 17 (`Read `talk.yaml` and `vision.md` before starting to understand topic, angle, and intent.`), insert:

```markdown

## Tool Availability Check

Before starting any search, check if these MCP tools are available:
- `mcp__claude_ai_PubMed__search_articles`
- `mcp__claude_ai_Consensus__search`

If ANY of them is NOT available, STOP and tell the user:

"The following recommended tools are not available in this session:
- [list missing tools]

These tools provide structured medical literature search with verified references (DOI/PMID). Without them, I'll use general web search which produces less precise and less structured results.

To connect them: go to claude.ai > Settings > MCP Servers and activate PubMed and/or Consensus.

Would you like to connect them before we continue, or proceed with web search only?"

Wait for the user's explicit response before proceeding. If they choose to continue without the MCP tools, use WebSearch and WebFetch as fallback for all literature searches. Always inform the user which tools you are using at the start of each search round.
```

- [ ] **Step 3: Commit**

```bash
git add skills/talk-research/SKILL.md
git commit -m "feat(talk-research): add allowed-tools, disable-model-invocation, MCP availability check"
```

---

### Task 7: Update talk-assets frontmatter

**Files:**
- Modify: `skills/talk-assets/SKILL.md`

- [ ] **Step 1: Update frontmatter**

Replace lines 1-4 with:

```yaml
---
name: talk-assets
description: Use when extracting and preparing visual assets for a presentation. Extracts full pages from PDFs as PNG+PDF, proposes didactic image prompts for Gemini, and creates an image map. Triggers when /talk detects research.md exists but images/ is empty.
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
---
```

- [ ] **Step 2: Commit**

```bash
git add skills/talk-assets/SKILL.md
git commit -m "feat(talk-assets): add disable-model-invocation and allowed-tools"
```

---

### Task 8: Update talk-narrative — frontmatter + plugin root paths

**Files:**
- Modify: `skills/talk-narrative/SKILL.md`

- [ ] **Step 1: Update frontmatter**

Replace lines 1-4 with:

```yaml
---
name: talk-narrative
description: Use when building the slide structure and storytelling arc for a presentation. Creates narrative.md with slide-by-slide plan including timing, connectors, and storytelling elements. Triggers when /talk detects assets ready but no narrative.md.
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Glob
---
```

- [ ] **Step 2: Update references paths**

Replace line 12:
```
- MUST read `references/storytelling-guide.md` before starting
```
With:
```
- MUST read `${CLAUDE_PLUGIN_ROOT}/references/storytelling-guide.md` before starting
```

Replace line 13:
```
- MUST read `references/slide-design-guide.md` for slide design principles
```
With:
```
- MUST read `${CLAUDE_PLUGIN_ROOT}/references/slide-design-guide.md` for slide design principles
```

Replace line 14:
```
- MUST read `references/pacing-guide.md` to select the timing template
```
With:
```
- MUST read `${CLAUDE_PLUGIN_ROOT}/references/pacing-guide.md` to select the timing template
```

Replace on line 23:
```
Based on `talk.yaml` duration, select the appropriate template from `references/pacing-guide.md`. Show it to the user as the structural skeleton.
```
With:
```
Based on `talk.yaml` duration, select the appropriate template from `${CLAUDE_PLUGIN_ROOT}/references/pacing-guide.md`. Show it to the user as the structural skeleton.
```

Replace on line 38:
```
Based on the user's vision, propose 2-3 opening options from `references/storytelling-guide.md`:
```
With:
```
Based on the user's vision, propose 2-3 opening options from `${CLAUDE_PLUGIN_ROOT}/references/storytelling-guide.md`:
```

- [ ] **Step 3: Commit**

```bash
git add skills/talk-narrative/SKILL.md
git commit -m "feat(talk-narrative): add frontmatter, use CLAUDE_PLUGIN_ROOT for reference paths"
```

---

### Task 9: Update talk-slides — frontmatter + plugin root + PLUGIN_DATA

**Files:**
- Modify: `skills/talk-slides/SKILL.md`

- [ ] **Step 1: Update frontmatter**

Replace lines 1-4 with:

```yaml
---
name: talk-slides
description: Use when generating the PPTX presentation file from an approved narrative structure. Applies the user's personal style and design principles. Triggers when /talk detects speaker-script.md exists but no presentation.pptx.
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Skill
---
```

- [ ] **Step 2: Update references path**

Replace line 12:
```
- Read `references/slide-design-guide.md` before generating
```
With:
```
- Read `${CLAUDE_PLUGIN_ROOT}/references/slide-design-guide.md` before generating
```

- [ ] **Step 3: Replace node_modules workflow with CLAUDE_PLUGIN_DATA**

Replace lines 41-49:
```markdown
1. Create `_build/` directory in the project root if it doesn't exist
2. Write the generation script to `_build/generate_presentation.js`
3. Write `_build/package.json` with PptxGenJS dependency
4. Run `npm install` inside `_build/`
5. Run the script — output `presentation.pptx` to the **project root** (not inside `_build/`)
6. After successful generation, delete `_build/node_modules/` to save space

The `_build/` directory with scripts is **permanent** — it allows the user to re-generate or modify the presentation later. Only `node_modules/` is disposable.
```

With:
```markdown
1. Create `_build/` directory in the project root if it doesn't exist
2. Write the generation script to `_build/generate_presentation.js`
3. Run the script with persistent dependencies:
   ```bash
   NODE_PATH=${CLAUDE_PLUGIN_DATA}/node_modules node _build/generate_presentation.js
   ```
4. Output `presentation.pptx` to the **project root** (not inside `_build/`)

If the script fails with a module not found error, reinstall dependencies:
```bash
cd ${CLAUDE_PLUGIN_DATA} && npm install
```

The `_build/` directory with scripts is **permanent** — it allows the user to re-generate or modify the presentation later. Dependencies (PptxGenJS) are managed by the plugin in `${CLAUDE_PLUGIN_DATA}` and shared across all projects.
```

- [ ] **Step 4: Commit**

```bash
git add skills/talk-slides/SKILL.md
git commit -m "feat(talk-slides): add frontmatter, CLAUDE_PLUGIN_ROOT paths, CLAUDE_PLUGIN_DATA for deps"
```

---

### Task 10: Update talk-study-doc frontmatter

**Files:**
- Modify: `skills/talk-study-doc/SKILL.md`

- [ ] **Step 1: Update frontmatter**

Replace lines 1-4 with:

```yaml
---
name: talk-study-doc
description: Use when generating study documents for a presentation — a comprehensive reference document and per-article summaries in Markdown. Triggers when /talk detects narrative.md exists but no study-document.md.
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Glob
---
```

- [ ] **Step 2: Commit**

```bash
git add skills/talk-study-doc/SKILL.md
git commit -m "feat(talk-study-doc): add disable-model-invocation and allowed-tools"
```

---

### Task 11: Update talk-script — frontmatter + SKILL_DIR path

**Files:**
- Modify: `skills/talk-script/SKILL.md`

- [ ] **Step 1: Update frontmatter**

Replace lines 1-4 with:

```yaml
---
name: talk-script
description: Use when generating the speaker script for a presentation — slide-by-slide delivery guide with preparation table and teleprompter format in Markdown. Triggers when /talk detects study-document.md exists but no speaker-script.md.
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Glob
---
```

- [ ] **Step 2: Update teleprompter reference path**

Replace line 12:
```
- Read `references/teleprompter-format.md` in this skill's directory for formatting rules
```
With:
```
- Read `${CLAUDE_SKILL_DIR}/references/teleprompter-format.md` for formatting rules
```

Replace line 47:
```
Full delivery script formatted according to `references/teleprompter-format.md`:
```
With:
```
Full delivery script formatted according to `${CLAUDE_SKILL_DIR}/references/teleprompter-format.md`:
```

- [ ] **Step 3: Commit**

```bash
git add skills/talk-script/SKILL.md
git commit -m "feat(talk-script): add frontmatter, use CLAUDE_SKILL_DIR for teleprompter reference"
```

---

### Task 12: Create SessionStart hooks

**Files:**
- Create: `hooks/hooks.json`
- Create: `assets/package.json`

- [ ] **Step 1: Create `assets/package.json`**

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

- [ ] **Step 2: Create `hooks/hooks.json`**

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "missing=\"\"; which pdftoppm >/dev/null 2>&1 || missing=\"$missing\n  - poppler (brew install poppler) — required for PDF image extraction\"; which node >/dev/null 2>&1 || missing=\"$missing\n  - Node.js (brew install node) — required for PPTX generation\"; if [ -n \"$missing\" ]; then printf '{\"result\": \"warn\", \"message\": \"Talk Builder: missing system dependencies:%s\"}' \"$missing\"; fi"
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

- [ ] **Step 3: Verify hooks directory is at plugin root**

```bash
ls -la hooks/
```

Expected: `hooks.json`

- [ ] **Step 4: Commit**

```bash
git add hooks/hooks.json assets/package.json
git commit -m "feat: add SessionStart hooks for dependency validation and PptxGenJS install"
```

---

### Task 13: Update .gitignore

**Files:**
- Modify: `.gitignore`

- [ ] **Step 1: Replace .gitignore contents**

```gitignore
config.yaml
.DS_Store
docs/superpowers/
```

- [ ] **Step 2: Commit**

```bash
git add .gitignore
git commit -m "chore: update gitignore — exclude dev artifacts, include assets/"
```

---

### Task 14: Create documentation files

**Files:**
- Create: `README.md`
- Create: `LICENSE`
- Create: `CHANGELOG.md`

- [ ] **Step 1: Create README.md**

```markdown
# Talk Builder

A Claude Code plugin for building academic and medical presentations with structured storytelling — from research to final PPTX and speaker scripts.

## Features

- **10-skill orchestrated workflow**: briefing, vision, research, assets, narrative, slides, study documents, speaker script
- **Evidence-based research**: PubMed and Consensus integration with DOI/PMID verification
- **Storytelling frameworks**: ABT, Sparkline, STAR moments, assertion-evidence design
- **Personal style config**: fonts, colors, layout preferences applied consistently
- **PPTX generation**: automated slide creation with PptxGenJS
- **Study documents**: comprehensive review-article-style reference and per-paper summaries
- **Speaker scripts**: preparation table + teleprompter format

## Requirements

- **Claude Code** (latest version)
- **poppler** — PDF image extraction: `brew install poppler`
- **Node.js** — PPTX generation: `brew install node`
- **PPTX plugin** from `claude-plugins-official` marketplace
- **Recommended**: PubMed and Consensus MCP servers (claude.ai > Settings > MCP Servers)

## Installation

Install from the marketplace:

```
/plugin install talk-builder
```

Or load locally for development:

```bash
claude --plugin-dir ./presentations-builder
```

## Quick Start

1. Run `/talk-builder:talk-setup` to configure your personal style
2. Create a new directory for your presentation: `mkdir my-talk && cd my-talk`
3. Run `/talk-builder:talk` to start the guided workflow

## Skills

| Skill | Purpose |
|---|---|
| `/talk` | Main orchestrator — detects phase and guides workflow |
| `/talk-setup` | One-time style and environment configuration |
| `/talk-briefing` | Collect topic, duration, audience, preferences |
| `/talk-vision` | Define personal angle, message, emotional intent |
| `/talk-research` | Search literature, read PDFs, build evidence base |
| `/talk-assets` | Extract figures from PDFs, propose AI image prompts |
| `/talk-narrative` | Build slide structure with storytelling arc and timing |
| `/talk-slides` | Generate PPTX presentation file |
| `/talk-study-doc` | Create study document and article summaries |
| `/talk-script` | Generate speaker script with teleprompter format |

## How It Works

Each presentation is a directory. Talk Builder detects your progress by checking which files exist:

| File | Phase |
|---|---|
| `talk.yaml` | Briefing complete |
| `vision.md` | Vision defined |
| `research.md` | Research complete |
| `images/` (non-empty) | Assets ready |
| `narrative.md` | Narrative approved |
| `study-document.md` | Study docs complete |
| `speaker-script.md` | Script ready |
| `presentation.pptx` | Slides generated |

Run `/talk` at any point to see your status and continue from where you left off.

## Configuration

Personal style is stored in a `config.yaml` at a path you choose during setup. Per-project overrides go in `talk.yaml`.

See `config.example.yaml` for all available options.

## License

MIT — see [LICENSE](LICENSE)
```

- [ ] **Step 2: Create LICENSE**

```
MIT License

Copyright (c) 2026 Sebastian Podlipnik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 3: Create CHANGELOG.md**

```markdown
# Changelog

All notable changes to Talk Builder will be documented in this file.

## [1.0.0] - 2026-04-04

### Added
- Initial marketplace release
- 10 skills: orchestrator + setup + 8 workflow phases
- Reference guides: storytelling, slide design, pacing, data storytelling
- SessionStart hook for system dependency validation
- Persistent PptxGenJS dependencies via `CLAUDE_PLUGIN_DATA`
- MCP tool availability check with fallback to WebSearch
- README, LICENSE, and CHANGELOG

### Fixed
- Plugin manifest moved to `.claude-plugin/plugin.json` (correct location)
- All reference paths use `${CLAUDE_PLUGIN_ROOT}` for marketplace compatibility
- Sub-skills no longer auto-invoked by Claude (only orchestrator is)
```

- [ ] **Step 4: Commit**

```bash
git add README.md LICENSE CHANGELOG.md
git commit -m "docs: add README, LICENSE (MIT), and CHANGELOG for 1.0.0 release"
```

---

### Task 15: Final validation

- [ ] **Step 1: Verify plugin structure**

```bash
echo "=== Plugin structure ===" && \
ls -la .claude-plugin/ && \
echo "=== Skills ===" && \
ls skills/ && \
echo "=== Hooks ===" && \
ls hooks/ && \
echo "=== Assets ===" && \
ls assets/ && \
echo "=== Root docs ===" && \
ls README.md LICENSE CHANGELOG.md && \
echo "=== No root plugin.json ===" && \
test ! -f plugin.json && echo "PASS: no root plugin.json" || echo "FAIL: root plugin.json still exists"
```

- [ ] **Step 2: Verify all skills have disable-model-invocation (except talk)**

```bash
for skill in talk-setup talk-briefing talk-vision talk-research talk-assets talk-narrative talk-slides talk-study-doc talk-script; do
  if grep -q "disable-model-invocation: true" "skills/$skill/SKILL.md"; then
    echo "PASS: $skill has disable-model-invocation"
  else
    echo "FAIL: $skill missing disable-model-invocation"
  fi
done
echo "---"
if ! grep -q "disable-model-invocation" "skills/talk/SKILL.md"; then
  echo "PASS: talk orchestrator does NOT have disable-model-invocation"
else
  echo "FAIL: talk orchestrator should NOT have disable-model-invocation"
fi
```

- [ ] **Step 3: Verify all skills have allowed-tools**

```bash
for skill in talk talk-setup talk-briefing talk-vision talk-research talk-assets talk-narrative talk-slides talk-study-doc talk-script; do
  if grep -q "allowed-tools" "skills/$skill/SKILL.md"; then
    echo "PASS: $skill has allowed-tools"
  else
    echo "FAIL: $skill missing allowed-tools"
  fi
done
```

- [ ] **Step 4: Verify CLAUDE_PLUGIN_ROOT paths**

```bash
echo "=== Should have CLAUDE_PLUGIN_ROOT ===" && \
grep -c "CLAUDE_PLUGIN_ROOT" skills/talk-narrative/SKILL.md && \
grep -c "CLAUDE_PLUGIN_ROOT" skills/talk-slides/SKILL.md && \
echo "=== Should have CLAUDE_SKILL_DIR ===" && \
grep -c "CLAUDE_SKILL_DIR" skills/talk-script/SKILL.md && \
echo "=== Should NOT have bare references/ ===" && \
grep -rn "^- .*\`references/" skills/ || echo "PASS: no bare references/ paths"
```

- [ ] **Step 5: Test plugin loads**

```bash
claude --plugin-dir . --print-skills 2>/dev/null || echo "Manual test needed: run 'claude --plugin-dir .' and check /help for skills"
```

- [ ] **Step 6: Commit any fixes if needed, then final status**

```bash
git log --oneline -10
```

Expected: ~7-8 new commits on top of the bugfixes commit.
