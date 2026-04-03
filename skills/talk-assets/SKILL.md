---
name: talk-assets
description: Use when extracting and preparing visual assets for a presentation. Extracts images from PDFs, proposes generative image prompts, and creates an image map. Triggers when /talk detects research.md exists but images/ is empty.
---

# Talk Builder — Visual Assets

Extract figures from papers, propose high-impact images for generation, and create a visual asset library for the presentation.

## Important

- Always maintain aspect ratio when processing images. NEVER distort by adjusting width and height independently.
- For each extracted figure, generate TWO files: the extracted image (.png) AND the full PDF page as reference.
- Naming convention: `author-year-figN-description` (e.g., `smith2024-fig3-survival-curve`)

Read `research.md` to know which papers and findings are relevant.

## Dependencies

Requires `poppler-utils` installed (`pdfimages`, `pdftoppm`). If not available, warn the user and suggest: `brew install poppler`

## Workflow

### Step 1: Scan PDFs

List all PDFs in `pdfs/`. For each, identify figures that are relevant to the research findings.

### Step 2: Extract images — Hybrid approach

**Method A — Embedded images (try first):**
```bash
pdfimages -png <paper.pdf> images/<prefix>
```
This extracts images at their original quality without page capture.

**Method B — Page conversion (fallback for vector/composite figures):**
```bash
pdftoppm -png -r 300 -f <page> -l <page> <paper.pdf> images/<prefix>
```
This converts specific pages to high-resolution PNGs (300 DPI).

For Method B, ask the user which region to crop. Always maintain aspect ratio.

### Step 3: Generate dual files per figure

For each figure the user selects:
1. `author-year-figN-description.png` — the extracted figure for use in slides
2. `author-year-figN-description-page.pdf` — the full page from the paper as reference

Extract the specific page as PDF:
```bash
pdfseparate -f <page> -l <page> <paper.pdf> images/<name>-page.pdf
```

### Step 4: Present to user

Show all extracted figures to the user. Ask which ones to keep, which to discard, and if any are missing.

### Step 5: Propose generative images

Based on `research.md` and `vision.md`, propose high-impact images that could be generated with AI tools (Midjourney, Gemini, DALL-E):

- "For the STAR moment about [topic], a dramatic visualization of [concept] would be powerful"
- "The opening could use a compelling image of [scene]"
- "This comparison could work as an infographic"

For each proposal, generate a ready-to-use prompt file:
`[GENERATE]-description.txt` containing:
- The detailed prompt for the AI image generator
- Suggested style and dimensions
- Which slide it would be used in

### Step 6: Create image-map.md

Generate `images/image-map.md`:

```markdown
# Image Map — [Talk Topic]

| Slide | Description | File | Status |
|---|---|---|---|
| 3 | Survival curve comparison | smith2024-fig3-survival-curve.png | Ready |
| 7 | Molecular pathway | jones2023-fig1-pathway.png | Ready |
| 9 | Impact visualization | [GENERATE]-star-moment.txt | To generate |
| 12 | Before/after comparison | [MISSING] | Need to find |
```

## After completion

Tell the user: "Assets prepared! Review the images/ folder and generate any AI images from the prompt files. Next phase: Narrative — building the slide structure with storytelling. Continue with /talk or /talk-narrative."
