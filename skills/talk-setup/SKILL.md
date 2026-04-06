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

### 4. Collect style preferences (one question at a time)

Ask these questions sequentially, one per message. Adapt your language to match the user's — if they write in Spanish, ask in Spanish.

**Question 1 — Language (ask this first, it determines the language for remaining questions):**
"What language do you usually present in?"
- English
- Spanish
- Other (specify)

**Question 2 — Title font:**
"What font do you use for slide titles? Some popular choices for presentations:"
- **Montserrat Bold** — modern, clean
- **Helvetica Neue Bold** — classic, professional
- **Playfair Display** — elegant, editorial
- **Arial Black** — safe, universal
- Or type any font name you prefer

**Question 3 — Body font:**
"What font for body text? It should pair well with [their title font choice]:"
- **Open Sans** — pairs well with most title fonts
- **Lato** — friendly, readable
- **Source Sans Pro** — clean, technical
- **Calibri** — safe default
- Or type any font name

**Question 4 — Colors:**
"What are your brand/presentation colors? You can:"
- a) Give me hex codes if you know them (e.g., #1A365D)
- b) Describe them ("dark navy blue and a warm red")
- c) Choose a preset:
  - **Classic** — navy #1A365D + red #E53E3E
  - **Medical** — teal #0D9488 + orange #F97316
  - **Modern** — dark gray #1F2937 + blue #3B82F6
  - **Elegant** — black #111827 + gold #D97706

If the user describes colors in words, convert to the closest hex values. Also ask: "Do you prefer light backgrounds (white/cream) or dark backgrounds?"

**Question 5 — Complexity default:**
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

Write the config file at `<chosen-path>/config.yaml` with all collected information:

```yaml
assets_path: "<chosen-path>"

style:
  fonts:
    title: "<user-answer>"
    body: "<user-answer>"
  colors:
    primary: "<user-answer>"
    accent: "<user-answer>"
    background: "<user-answer — #FFFFFF or dark>"
  language: "<user-answer>"
  narrative_style: "conversational"
  complexity_default: "<user-answer>"

style_analysis:
  layout: "<analyzed or empty>"
  title_style: "<analyzed or empty>"
  color_usage: "<analyzed or empty>"
  typography: "<analyzed or empty>"
  visual_density: "<analyzed or empty>"
  notes: "<analyzed or empty>"
```

### 8. Confirm completion

Show the user a visual summary of their configuration — display the colors as hex codes with their names, the fonts, and the language. End with: "You're all set! Start a new presentation anytime with `/talk-builder:talk`."

## Reconfiguration

If the user already has a config and runs `/talk-setup` again, read the existing config first and show them their current settings. Ask which sections they want to update. Do not overwrite unchanged sections.
