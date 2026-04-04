---
name: talk-assets
description: Use when extracting and preparing visual assets for a presentation. Extracts specific figures from PDFs as PNG+PDF, proposes didactic image prompts, and creates an image map. Triggers when /talk detects research.md exists but images/ is empty.
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
---

# Talk Builder — Visual Assets

Extract SPECIFIC relevant figures from research papers and prepare visual assets for the presentation. The goal is quality over quantity — only extract what serves the narrative.

## Important

- Read `talk.yaml`, `vision.md`, `research.md`, and `${user_config.assets_path}/config.yaml` before starting.
- **Language priority:** Use the language the user writes in. Fall back to config.language for ambiguous messages.
- **Start from research.md's "Figures for Slides" table** (if it exists). That table already identifies which figures from which papers are relevant to which slides. Don't re-scan from scratch.
- Only extract figures that serve the narrative. A 20-minute talk needs ~15-20 images max. Extracting 100 images from every PDF creates clutter, not value.
- Always maintain aspect ratio when processing images. NEVER distort.
- For each extracted page, generate TWO files: PNG (.png) for preview AND PDF (.pdf) for vector quality in Keynote.
- Naming convention: `author-year-pN-description` (e.g., `smith2024-p4-survival-curve`)

## Dependencies

Requires `poppler-utils` installed (`pdftoppm`, `pdfseparate`). If not available, warn the user and suggest: `brew install poppler`

## Workflow

### Step 1: Build extraction plan from research.md

Read the "Figures for Slides" table in `research.md` (if present). This gives you a pre-identified list of:
- Which paper has the figure
- Which page
- What it shows
- Which slide it's intended for

If the table doesn't exist, read `research.md` and `narrative.md` (if available) to identify which data points need visual support, then scan the PDFs for matching figures.

Present the extraction plan to the user:

"Based on the research, I plan to extract these figures:
1. [Author Year] p.[N] — [description] → for slide about [topic]
2. ...
[Total: N figures from M papers]

Does this look right? Any others you want, or any to skip?"

### Step 2: Extract targeted figures

For each approved figure, extract ONLY that page in both formats:

**PNG** (300dpi for slides):
```bash
pdftoppm -png -r 300 -f <page> -l <page> <paper.pdf> images/<author-year-pN-description>
```

**PDF** (vector quality for Keynote):
```bash
pdfseparate -f <page> -l <page> <paper.pdf> images/<author-year-pN-description>-page.pdf
```

**Do NOT extract every image from every PDF.** Only extract what was planned in Step 1. If a page has multiple figures, extract the whole page — the user can crop in Keynote.

### Step 3: Present extracted figures

Show the user what was extracted with a brief description of each:

```
Extracted 12 figures:

From Gopalakrishnan 2018:
  ✓ gopalakrishnan2018-p2-diversity.png — Alpha diversity comparison
  ✓ gopalakrishnan2018-p4-survival.png — PFS Kaplan-Meier curve

From Routy 2023:
  ✓ routy2023-p3-clinical-response.png — ORR waterfall plot
  ...
```

Ask: "Review these in the `images/` folder. Which to keep, which to discard? Any figures missing?"

### Step 4: Propose didactic images

Based on `research.md` and `vision.md`, identify gaps where a custom illustration would help the audience understand a concept better than a paper figure. Focus on:

- **Mechanisms or pathways** that don't have a good published figure
- **Comparisons or timelines** that synthesize data from multiple papers
- **Conceptual diagrams** that simplify complex ideas for the audience level

Do NOT propose purely decorative images. Every proposed image must have a clear didactic purpose. Limit to 3-5 proposals max — quality over quantity.

For each proposal, generate a ready-to-use prompt file in `images/`:
`[GENERATE]-description.txt` containing:

```
## Prompt (for image generation — Gemini, DALL-E, or Midjourney)
[Detailed descriptive prompt in natural language]

## Purpose
[How this image helps the audience understand a specific concept]

## Style Context
Colors: [primary and accent from config.yaml]
Tone: [matching the presentation style]
Background: transparent or clean white, suitable for slide insertion
Aspect ratio: 16:9 (slide format)

## Target Slide
[Which slide in the narrative this is intended for]
```

### Step 5: Create image-map.md

Generate `images/image-map.md` — this is the master reference that connects images to slides:

```markdown
# Image Map — [Talk Topic]

## Summary
- Total figures extracted: [N]
- Figures to generate: [N]
- Figures missing: [N]

## Map

| Slide | Description | File | Source | Status |
|---|---|---|---|---|
| 3 | Survival curve | gopalakrishnan2018-p4-survival.png | Gopalakrishnan 2018, Fig 3 | Ready |
| 7 | Gut-skin axis diagram | [GENERATE]-gut-skin-axis.txt | AI-generated | To generate |
| 9 | Forest plot PASI-75 | li2024-p9-forest.png | Li 2024, Fig 1 | Ready |
| 12 | Treatment mechanism | [MISSING] | — | Need to find/create |
```

**This file is critical** — it's the bridge between research and narrative. The narrative phase uses it to know what visuals are available per slide.

## After completion

Tell the user: "Assets prepared! You have [N] figures ready and [N] to generate. Review the `images/` folder and create any AI images from the prompt files. Next phase: Narrative — building the slide structure with storytelling. Continue with /talk or /talk-builder:talk-narrative."
