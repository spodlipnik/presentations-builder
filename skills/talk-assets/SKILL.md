---
name: talk-assets
description: Use when extracting and preparing visual assets for a presentation. Extracts full pages from PDFs as PNG+PDF, proposes didactic image prompts for Gemini, and creates an image map. Triggers when /talk detects research.md exists but images/ is empty.
---

# Talk Builder — Visual Assets

Extract relevant pages from research papers, propose didactic images for generation with Gemini, and create a visual asset library for the presentation.

## Important

- Always maintain aspect ratio when processing images. NEVER distort by adjusting width and height independently.
- For each extracted page, generate TWO files: the page as PNG (.png) AND the page as PDF (.pdf) for vector quality in Keynote.
- Naming convention: `author-year-pN-description` (e.g., `smith2024-p4-survival-curve`)
- Images must be **didactic and self-explanatory** — they should help the audience understand complex concepts, not just decorate slides.

Read `research.md` to know which papers and findings are relevant.
Read `config.yaml` for the presentation's color palette and style (used for generative image prompts).

## Dependencies

Requires `poppler-utils` installed (`pdftoppm`, `pdfseparate`). If not available, warn the user and suggest: `brew install poppler`

## Workflow

### Step 1: Scan PDFs

List all PDFs in `pdfs/`. For each, identify figures that are relevant to the research findings.

### Step 2: Extract pages

For each relevant page identified in Step 1, extract both formats:

**PNG** (for preview and slide use):
```bash
pdftoppm -png -r 300 -f <page> -l <page> <paper.pdf> images/<author-year-pN-description>
```

**PDF** (vector quality for Keynote):
```bash
pdfseparate -f <page> -l <page> <paper.pdf> images/<author-year-pN-description>-page.pdf
```

Always generate both files per page. Present the extracted pages to the user and ask which to keep.

### Step 3: Present to user

Show all extracted figures to the user. Ask which ones to keep, which to discard, and if any are missing.

### Step 4: Propose didactic images for Gemini

Based on `research.md` and `vision.md`, propose images that help the audience **understand complex concepts**. Focus on:
- Illustrations that explain mechanisms, pathways, or processes
- Visual comparisons (before/after, treatment A vs B)
- Conceptual diagrams that simplify complex ideas

Do NOT propose purely decorative images. Every proposed image must have a clear didactic purpose.

For each proposal, generate a ready-to-use prompt file:
`[GENERATE]-description.txt` containing:

```
## Prompt (optimized for Gemini)
[Detailed descriptive prompt in natural language — no Midjourney syntax like --ar or --v]

## Purpose
[How this image helps the audience understand a specific concept]

## Style Context
Colors: [primary and accent from config.yaml]
Tone: [matching the presentation style from config.yaml]
Background: transparent or clean, suitable for slide insertion

## Target Slide
[Which slide in the narrative this is intended for]
```

### Step 5: Create image-map.md

Generate `images/image-map.md`:

```markdown
# Image Map — [Talk Topic]

| Slide | Description | File | Status |
|---|---|---|---|
| 3 | Survival curve comparison | smith2024-p4-survival.png | Ready |
| 7 | Molecular pathway diagram | jones2023-p8-pathway.png | Ready |
| 9 | Treatment mechanism | [GENERATE]-mechanism.txt | To generate (Gemini) |
| 12 | Before/after comparison | [MISSING] | Need to find |
```

## After completion

Tell the user: "Assets prepared! Review the images/ folder and generate any AI images from the prompt files using Gemini. Next phase: Narrative — building the slide structure with storytelling. Continue with /talk or /talk-narrative."
