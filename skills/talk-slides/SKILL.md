---
name: talk-slides
description: Use when generating the PPTX presentation file from an approved narrative structure. Applies the user's personal style and design principles. Triggers when /talk detects narrative.md exists but no presentation.pptx.
---

# Talk Builder — PPTX Generation

Generate the presentation file from the approved narrative structure, applying the user's personal style configuration and slide design principles.

## Important

- Read `references/slide-design-guide.md` before generating
- Read the user's `config.yaml` for fonts, colors, and style analysis
- Read `talk.yaml` for any local style overrides
- Read `narrative.md` for the complete slide structure
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

Create `presentation.pptx` following `narrative.md` slide by slide:

For each slide:
- Apply assertion-evidence title format
- Use configured fonts (title font for headers, body font for content)
- Use configured colors (primary, accent, background)
- Insert images from `images/` where referenced in narrative
- Follow one-slide-one-message principle
- Apply slide-design-guide principles (glance test, minimal text, visual evidence)

### Step 3: Insert fixed slides

If `talk.yaml` specifies fixed slides (disclosures, contact, acknowledgments):
- Read corresponding files from the user's `fixed-slides/` directory
- Insert at appropriate positions (disclosures near start, contact at end)

### Step 4: Present for review

Tell the user:
"PPTX generated at `presentation.pptx`. This is a first draft — open it in Keynote to:
- Adjust image positions and sizes
- Fine-tune layouts
- Replace any placeholder images
- Check the `images/image-map.md` for reference on which images go where"

## After completion

Tell the user: "Slides generated! Open in Keynote for visual fine-tuning. When ready, continue with /talk or /talk-study-doc for the study documents."
