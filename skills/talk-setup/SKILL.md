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

## Important

This skill creates the user's personal assets directory and config file.

The assets path comes from the plugin's `userConfig` system — it's stored in `${user_config.assets_path}`. If the user hasn't configured it yet, Claude Code will have prompted them when they enabled the plugin. If the value is empty, ask them to set it via plugin settings or provide a path now.

## Steps

### 1. Verify assets directory path

Check `${user_config.assets_path}`. If it's set, confirm with the user: "Your assets folder is set to `[path]`. Is this correct, or would you like to change it?"

If not set, ask the user where they want to store their Talk Builder assets (config, example slides, fixed slides). Suggest examples like `~/Documents/talk-builder/` but let them choose any path. Then tell them to update the plugin setting with the chosen path.

### 2. Create directory structure

Create the chosen directory with subdirectories:

```
<chosen-path>/
├── config.yaml
├── example-slides/
└── fixed-slides/
```

### 3. Collect style preferences (one question at a time)

Ask these questions sequentially, one per message:

1. "What is your default presentation language?" (en/es/other)
2. "What font do you use for slide titles?" (e.g., Montserrat Bold, Arial Black)
3. "What font do you use for body text?" (e.g., Open Sans, Calibri)
4. "What is your primary color? (hex code, e.g., #1A365D)"
5. "What is your accent color? (hex code, e.g., #E53E3E)"
6. "What is your default complexity level?" (basic / moderate / advanced)

### 4. Ask about example slides

"Do you have existing presentations that represent your style? If so, place your .pptx or .key files in: `<chosen-path>/example-slides/`"

If the user confirms they have placed files there, read and analyze them to generate the `style_analysis` section of the config:
- `layout`: overall layout approach (e.g., "minimal, full-bleed images, one message per slide")
- `title_style`: how titles are written (e.g., "assertion-evidence, sentence case")
- `color_usage`: how colors are applied (e.g., "dark backgrounds, high contrast accent")
- `typography`: font patterns observed (e.g., "sans-serif, large titles, minimal body text")
- `visual_density`: content density (e.g., "low — lots of whitespace")
- `notes`: any other style patterns (e.g., "uses clinical photos, avoids clip art")

### 5. Ask about fixed slides

"Do you have slides you reuse in every presentation (contact info, disclosures, acknowledgments)? If so, place them in: `<chosen-path>/fixed-slides/`"

### 6. Check dependencies

#### 6a. Required Claude Code plugins

Talk Builder depends on the official Anthropic PPTX skill for presentation generation. Check if it is installed and guide the user if not:

**PPTX skill** (for presentation generation):
- Required for `/talk-slides`
- Install via: `/plugin` → select `claude-plugins-official` marketplace → install `pptx`

Tell the user:
"Talk Builder needs the official PPTX skill from Anthropic to generate presentation files. Please install it from the `claude-plugins-official` marketplace using `/plugin` if you haven't already."

#### 6b. System dependencies

**poppler-utils** (for page extraction from PDFs):
Verify installed by running:

```bash
which pdftoppm && which pdfseparate
```

If not found, tell the user:
"Talk Builder needs poppler-utils for extracting pages from PDFs. Install with: `brew install poppler`"

**Node.js** (required by PPTX skill):
Verify installed by running:

```bash
which node && node --version
```

If not found, tell the user:
"The PPTX skill requires Node.js. Install with: `brew install node`"

**LibreOffice** (optional, for visual QA of generated presentations):
Verify installed by running:

```bash
which soffice
```

If not found, tell the user:
"LibreOffice is optional but recommended for visual QA of generated presentations. Install with: `brew install --cask libreoffice`"

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
    background: "#FFFFFF"
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

Show the user a summary of their configuration and confirm everything is set up correctly.

## Reconfiguration

If the user already has a config and runs `/talk-setup` again, read the existing config first and ask which sections they want to update. Do not overwrite unchanged sections.
