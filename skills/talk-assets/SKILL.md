---
name: talk-assets
description: Use when creating and preparing visual assets for a presentation. Collaborative visual creation — extracts figures from PDFs, generates data charts (SVG), creates diagrams, and proposes AI illustration prompts. Triggers when /talk detects docs/narrative.md exists but images/ is empty.
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
---

# Talk Builder — Visual Creation Studio

Create the visual assets for each slide in the presentation. This is a collaborative process — for each visual need, we discuss the best approach with the speaker and create it together.

The goal is NOT to extract every figure from every PDF. It's to create a focused set of high-quality visuals where every image earns its place and helps the audience understand something they couldn't grasp from words alone.

## Important

- Read `docs/narrative.md` first — it defines what each slide needs
- Read `docs/research.md` for the Visual Elements Catalog (what figures exist in papers)
- Read `${user_config.assets_path}/config.yaml` for colors, fonts, and style
- Read `docs/talk.yaml` and `docs/vision.md` for topic and intent context
- **Language priority:** Use the language the user writes in. Fall back to config.language for ambiguous messages.
- **Every visual must be didactic** — it must teach, explain, or make data tangible. No decorative images.
- **Quality over quantity** — a 20-minute talk needs ~10-15 visuals max. 100 images is failure, not thoroughness.

## Dependencies

- `poppler-utils` for PDF extraction (`pdftoppm`, `pdfseparate`). Install: `brew install poppler`
- `sharp` (Node.js, globally installed) for SVG → PNG conversion
- Python with Pillow for raster compositing (if needed)

Check dependencies at start. Warn about missing ones but don't block — some visual types don't need all tools.

## The Four Generators

This skill has four ways to create visuals, each for a different need:

### EXTRACT — Figures from published papers
**When:** The paper has a published figure that's better than anything we could recreate (original data, clinical photos, histology, complex charts from the study itself)
**How (prefer pre-extracted):** Check `pdfs/extracted/<paper_name>/` first — Docling may have already extracted figure images as `fig-*.png` during the research phase. If suitable images exist there, copy them to `images/` with proper naming. Only fall back to `pdftoppm` + `pdfseparate` if pre-extracted images are missing or insufficient quality.
**How (fallback):** `pdftoppm` for PNG (300dpi) + `pdfseparate` for PDF vector
**Naming:** `author-year-pN-description.png` (e.g., `gopalakrishnan2018-p4-survival.png`)
**Always:** PNG + PDF pair per figure when using pdftoppm. Pre-extracted images are PNG only.

### CHART — Data visualizations with SVG
**When:** You need a clean chart with specific data from the research (bar chart, comparison, simplified forest plot, timeline, trend line). Better than using a cluttered paper figure when you only need 3 data points from a table of 20.
**How:** Claude writes inline SVG code with config.yaml colors → convert to PNG via sharp:
```bash
node -e "const sharp = require('/opt/homebrew/lib/node_modules/sharp'); sharp('images/chart.svg').png({density: 300}).toFile('images/chart.png')"
```
**Style rules:**
- Use primary color for main data, accent for highlights
- Background: transparent or config background color
- 16:9 aspect ratio (1920x1080 viewBox)
- Large text (min 24pt equivalent) — readable from back of auditorium
- Annotated: labels, arrows, key numbers highlighted
- Minimal: only the data that supports the slide's message

### DIAGRAM — Conceptual visualizations
**When:** You need to explain a mechanism, pathway, process, flowchart, timeline, or comparison that doesn't exist as a published figure. These are the most valuable original visuals — they're what makes YOUR talk unique.
**How — Simple (SVG):** For clean diagrams with boxes, arrows, text, connections. Claude writes SVG directly.
**How — Complex (HTML artifact):** For multi-layered diagrams, interactive elements, or designs that benefit from CSS layout. Claude creates an HTML file, user opens in browser, screenshots to PNG.
**Style rules:**
- Same color palette as CHART (config.yaml)
- Self-explanatory — the diagram should make sense without the speaker
- Labeled clearly — no ambiguous arrows
- Clean, minimal — avoid visual clutter

### ILLUSTRATE — Prompts for AI image generation
**When:** You need something Claude cannot draw — photorealistic images, artistic illustrations, complex biological mechanisms with 3D depth, medical illustrations. These require Gemini, DALL-E, or similar tools.
**How:** Generate a detailed prompt file `[GENERATE]-description.txt` with style context from config.yaml. The user generates the image externally and places it in `images/`.
**Important:** This is the LAST resort. Before proposing ILLUSTRATE, ask: "Can I create this as a DIAGRAM instead?" Most conceptual visuals work better as clean diagrams than as AI-generated illustrations.

## Workflow

### Step 1: Visual needs analysis

Read `docs/narrative.md` slide by slide. For each slide, determine:
- Does it need a visual? (divider slides, text-only emotional slides, and big-number slides usually don't)
- What type of visual? (EXTRACT / CHART / DIAGRAM / ILLUSTRATE / SPEAKER ADDS)
- What source? (which paper, which data, what concept)

Cross-reference with `docs/research.md`'s Visual Elements Catalog to match paper figures to slide needs.

### Step 2: Present visual plan and discuss

This is the collaborative heart of the skill. Present the complete visual plan organized by type:

```
VISUAL PLAN — [Talk Topic] ([N] visuals for [M] slides)

📄 EXTRACT from papers ([N]):
  S[N]: [description] — [Author Year] p.[N], [figure type]
  S[N]: [description] — [Author Year] p.[N], [figure type]
  ...

📊 CREATE charts ([N]):
  S[N]: [description]
    Data: [specific numbers from docs/research.md]
    Proposed: [chart type — bar, comparison, trend]
    Why not EXTRACT: [reason — e.g., "paper figure has 20 rows, we need 3"]
  
  S[N]: [description]
    ...

🔬 CREATE diagrams ([N]):
  S[N]: [description]
    Concept: [what it explains]
    Proposed: [SVG / HTML artifact]
    Key elements: [boxes, arrows, labels needed]
    Your idea? [ask user how they envision this]
  
  S[N]: [description]
    ...

🎨 GENERATE with AI ([N]):
  S[N]: [description]
    Why not DIAGRAM: [reason — e.g., "needs photorealistic tissue rendering"]
    Proposed prompt direction: [brief]
  
❌ No visual needed ([N] slides):
  S[N] (title), S[N] (COI), S[N] (divider), ...

📷 SPEAKER ADDS in Keynote ([N]):
  S[N]: [description — clinical photos only speaker has]
```

Then ask:
"This is my proposal. Let's discuss:
- Any extractions you'd skip or add?
- For the charts and diagrams — how do you envision them? Do my proposals make sense?
- For the AI illustrations — do you agree these can't be done as diagrams?
- Which visual should we start with?"

**Wait for the user's input before creating anything.** This discussion saves hours of wasted work.

### Step 3: Create visuals iteratively

Work through the approved plan one visual at a time. For each:

1. **Create** the visual (extract, generate SVG, write HTML, or write prompt)
2. **Show** it to the user (describe what was created, where it's saved)
3. **Get feedback** ("looks good" / "change X" / "start over")
4. **Iterate** until the user approves
5. **Move to the next** visual

For CHART and DIAGRAM visuals, save both source (SVG/HTML) and output (PNG):
```
images/
├── gut-skin-axis.svg          # Source — editable
├── gut-skin-axis.png          # Output — for slides (300dpi)
├── tmb-comparison-chart.svg   # Source
├── tmb-comparison-chart.png   # Output
└── ...
```

For EXTRACT visuals:
```
images/
├── gopalakrishnan2018-p4-survival.png   # Raster 300dpi
├── gopalakrishnan2018-p4-survival.pdf   # Vector for Keynote
└── ...
```

### Step 4: Update image-map.md

After creating all visuals, generate `images/image-map.md`:

```markdown
# Image Map — [Talk Topic]

## Summary
- Extracted from papers: [N]
- Charts created: [N]
- Diagrams created: [N]  
- AI illustrations: [N] pending / [N] done
- Speaker adds: [N]
- Total visuals: [N] ready / [N] pending

## Visual Map

### EXTRACTED
| Slide | Description | File | Source | Notes |
|---|---|---|---|---|
| S6 | Forest plot acné | lin2025-p7-forest.png | Lin 2025, Fig 3 | — |

### CREATED (Charts)
| Slide | Description | File | Data Source | Notes |
|---|---|---|---|---|
| S18 | ATB pre-ICI comparison | atb-ici-comparison.png | Pinato 2019 + Wilson 2020 | SVG source: atb-ici-comparison.svg |

### CREATED (Diagrams)
| Slide | Description | File | Concept | Notes |
|---|---|---|---|---|
| S4 | Gut-skin axis | gut-skin-axis.png | Bidirectional pathway | SVG source: gut-skin-axis.svg |

### AI ILLUSTRATIONS
| Slide | Description | Prompt File | Status | Final File |
|---|---|---|---|---|
| S22 | L. reuteri in tumor | [GENERATE]-lreuteri-tumor.txt | Pending | — |

### SPEAKER ADDS
| Slide | Description | Notes |
|---|---|---|
| S3 | Clinical photo melanoma | Speaker adds in Keynote |
```

## Quality Principles

Every visual created by this skill must pass these checks:

- **Didactic:** Does it teach something? Would the audience understand the concept better WITH this visual than without it?
- **Self-explanatory:** Can someone understand the main point without the speaker talking? (Labels, annotations, clear structure)
- **Consistent:** Same color palette (config.yaml), same style across all created visuals
- **Readable:** Large enough text to read from the back of the auditorium (think billboard test)
- **Minimal:** No unnecessary elements. If removing something doesn't weaken understanding, remove it.
- **16:9:** Correct aspect ratio for slide insertion
- **High resolution:** 300dpi PNG minimum for print/projection quality

## After completion

Tell the user: "Visual assets complete! You have [N] visuals ready and [N] AI illustrations pending. Generate those with Gemini using the prompt files in `images/`, then continue with /talk or /talk-builder:talk-study-doc."
