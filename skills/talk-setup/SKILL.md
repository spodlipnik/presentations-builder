---
name: talk-setup
description: Use when setting up Talk Builder for the first time or reconfiguring personal style preferences. Triggers on first /talk invocation if no config exists, or when user says "configure talk builder", "setup talk builder", "change my presentation style".
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
---

# Talk Builder — Initial Setup

Guide the user through configuring their personal Talk Builder environment. This runs once and creates persistent configuration that all other talk-builder skills reference.

The goal is to capture the user's personal presentation style so that every future talk feels like *theirs*, not like a generic template. Ask questions conversationally — this should feel like a brief creative consultation, not a form.

## Important

The assets path comes from the plugin's `userConfig` system — it's stored in `${user_config.assets_path}`. If the user hasn't configured it yet, Claude Code will have prompted them when they enabled the plugin. If the value is empty, ask them to set it via plugin settings or provide a path now.

## Steps

### 1. Verify assets directory path

Check `${user_config.assets_path}`. If it's set, confirm with the user: "Your assets folder is set to `[path]`. Is this correct, or would you like to change it?"

If not set, ask the user where they want to store their Talk Builder assets (config, example slides, fixed slides). Suggest examples like `~/Documents/talk-builder/` but let them choose any path. Then tell them to update the plugin setting with the chosen path.

### 2. Check dependencies first

Check system dependencies before investing time in style questions. Run these checks silently and only report problems:

**poppler-utils** (for PDF image extraction):
```bash
which pdftoppm && which pdfseparate
```

**Node.js** (for PPTX generation):
```bash
which node && node --version
```

If anything is missing, tell the user what to install and why:
- poppler: `brew install poppler` — needed to extract figures from research papers
- Node.js: `brew install node` — needed to generate PPTX files

**LibreOffice** (optional, for thumbnail generation in `talk-theme-builder`): only mention if the user asks about visual QA.

Do not block setup if dependencies are missing — the user can install them later before they need those specific features.

### 3. Create directory structure

Create the chosen directory with subdirectories:

```
<chosen-path>/
├── config.yaml
├── example-slides/
├── fixed-slides/
└── themes/
```

### 4. Collect user preferences (one question at a time)

Ask these questions sequentially, one per message. Adapt your language to match the user's — if they write in Spanish, ask in Spanish.

**Note:** Fonts and colors are NOT configured here. They live exclusively in the theme (`theme.yaml`), created via `/talk-theme-builder create`. This avoids duplication.

**Question 1 — Language (ask this first, it determines the language for remaining questions):**
"What language do you usually present in?"
- English
- Spanish
- Other (specify)

**Question 2 — Complexity default:**
"When you give talks, what's your typical audience level? This helps calibrate how much jargon and technical depth to use by default:"
- **Basic** — general audience, minimal jargon, focus on concepts
- **Moderate** — professionals in related fields, some technical terms okay
- **Advanced** — specialists, cutting-edge terminology expected

### 5. Ask about example slides

"Do you have existing presentations that represent your style? If so, place your .pptx or .key files in: `<chosen-path>/example-slides/`"

If the user confirms they have placed files there, read and analyze them to generate the `style_analysis` section of the config:
- `layout`: overall layout approach (e.g., "minimal, full-bleed images, one message per slide")
- `title_style`: how titles are written (e.g., "assertion-evidence, sentence case")
- `color_usage`: how colors are applied (e.g., "dark backgrounds, high contrast accent")
- `typography`: font patterns observed (e.g., "sans-serif, large titles, minimal body text")
- `visual_density`: content density (e.g., "low — lots of whitespace")
- `notes`: any other style patterns (e.g., "uses clinical photos, avoids clip art")

### 6. Ask about fixed slides

"Do you have slides you reuse in every presentation (contact info, disclosures, acknowledgments)? If so, place them in: `<chosen-path>/fixed-slides/`"

### 7. Generate config.yaml

Write the config file at `<chosen-path>/config.yaml` with user preferences only (NO fonts/colors — those live in theme.yaml):

```yaml
language: "<user-answer>"
narrative_style: "conversational"
complexity_default: "<user-answer>"
default_theme: ""

style_analysis:
  layout: "<analyzed or empty>"
  title_style: "<analyzed or empty>"
  color_usage: "<analyzed or empty>"
  typography: "<analyzed or empty>"
  visual_density: "<analyzed or empty>"
  notes: "<analyzed or empty>"
```

**Important:** `config.yaml` stores WHO the user is (language, complexity, narrative style). All visual tokens (fonts, colors, layouts) live exclusively in `theme.yaml`. This prevents duplication — there is one single source of truth for visual style.

### 8. Confirm completion

Show the user a summary of their configuration — the language, complexity level, and narrative style. Then suggest: "Next step: create a theme with `/talk-builder:talk-theme-builder create` to define your visual style (fonts, colors, layouts). Start a new presentation anytime with `/talk-builder:talk`."

## Reconfiguration

If the user already has a config and runs `/talk-setup` again, read the existing config first and show them their current settings. Ask which sections they want to update. Do not overwrite unchanged sections.
