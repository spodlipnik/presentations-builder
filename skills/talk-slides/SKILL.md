---
name: talk-slides
description: Use when generating the PPTX presentation file from an approved narrative structure. Applies the user's personal style and design principles. Triggers when /talk detects speaker-script.md exists but no presentation.pptx.
---

# Talk Builder — PPTX Generation

Generate the presentation file from the approved narrative structure, applying the user's personal style configuration and slide design principles.

## Important

- Read `references/slide-design-guide.md` before generating
- Read the user's `config.yaml` for fonts, colors, and style analysis
- Read `talk.yaml` for any local style overrides
- Read `narrative.md` for the complete slide structure
- Read `speaker-script.md` to understand the full delivery context
- Check `images/` for available visual assets
- Check the user's `fixed-slides/` directory for reusable slides

The PPTX is a FIRST DRAFT. The user will fine-tune in Keynote. Focus on:
- Correct structure and content placement
- Proper fonts and colors from config
- Image insertion where available
- Clean, minimal design following slide-design-guide principles

## Workflow

### Step 1: Load configuration

1. Read `config.yaml` from the user's assets path
2. Read `talk.yaml` for local overrides
3. Merge: talk.yaml overrides config.yaml for any shared fields
4. Note the style_analysis for design decisions

### Step 2: Generate PPTX

**Requires:** The official `pptx` skill from `claude-plugins-official` must be installed.

Use the **PptxGenJS approach** described in the official `pptx` skill to create the presentation from scratch. Refer to the `pptx` skill's `pptxgenjs.md` reference for the full API.

**All generation files go in `_build/`:**

1. Create `_build/` directory in the project root if it doesn't exist
2. Write the generation script to `_build/generate_presentation.js`
3. Write `_build/package.json` with PptxGenJS dependency
4. Run `npm install` inside `_build/`
5. Run the script — output `presentation.pptx` to the **project root** (not inside `_build/`)
6. After successful generation, delete `_build/node_modules/` to save space

The `_build/` directory with scripts is **permanent** — it allows the user to re-generate or modify the presentation later. Only `node_modules/` is disposable.

Key generation instructions:
- Apply the user's fonts, colors, and background from `config.yaml` / `talk.yaml`
- Use the `pptx` skill's design guidance for layout, spacing, and visual hierarchy

### Step 3: Visual QA (optional but recommended)

If LibreOffice is available, follow the `pptx` skill's QA workflow:
1. Convert PPTX to PDF via `soffice`
2. Convert PDF to per-slide JPGs via `pdftoppm`
3. Visually inspect each slide
4. Fix any issues found

### Step 4: Insert fixed slides

If `talk.yaml` specifies fixed slides (disclosures, contact, acknowledgments):
- Read corresponding files from the user's `fixed-slides/` directory
- Insert at appropriate positions (disclosures near start, contact at end)

### Step 5: Present for review

Tell the user:
"PPTX generated at `presentation.pptx`. This is a first draft — open it in Keynote to:
- Adjust image positions and sizes
- Fine-tune layouts
- Replace any placeholder images
- Check the `images/image-map.md` for reference on which images go where"

## After completion

Tell the user: "Slides generated! Your Talk Builder project is complete. All outputs:
- study-document.md — comprehensive reference document
- article-summaries.md — quick reference per paper
- speaker-script.md — delivery guide with teleprompter
- presentation.pptx — open in Keynote for visual fine-tuning
- _build/ — generation scripts (reusable for modifications)

Run /talk to see the full project status."
