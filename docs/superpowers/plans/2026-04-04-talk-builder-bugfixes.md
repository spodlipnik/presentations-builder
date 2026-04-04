# Talk Builder Bugfixes & Improvements — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix workflow order, migrate docs to Markdown, overhaul assets extraction, and clean up build artifacts across 7 skill files.

**Architecture:** Each task modifies one skill file (SKILL.md). Changes are content edits to Markdown — no code compilation or tests. Verification is manual review of the diff.

**Tech Stack:** Markdown skill files in a Claude Code plugin.

**Spec:** `docs/superpowers/specs/2026-04-04-talk-builder-bugfixes-design.md`

---

### Task 1: Update orchestrator — reorder phases and add `_build/` detection

**Files:**
- Modify: `skills/talk/SKILL.md`

**Covers spec sections:** 1 (Workflow Reorder), 6c (Orchestrator cleanup), Issues D, E, G

- [ ] **Step 1: Update Phase Detection table**

Replace the current Phase Detection table with:

```markdown
## Phase Detection

Scan the current working directory for these files to determine project state:

| File | Phase Completed |
|---|---|
| `talk.yaml` | Briefing |
| `vision.md` | Vision |
| `research.md` | Research |
| `images/` (non-empty) | Assets |
| `narrative.md` | Narrative |
| `study-document.md` + `article-summaries.md` | Study Docs |
| `speaker-script.md` | Script |
| `presentation.pptx` | Slides |
```

- [ ] **Step 2: Update the visual checklist example**

Replace the status display example with:

```
Talk Builder — Project Status:

  [done] Briefing (talk.yaml)
  [done] Vision (vision.md)
  [done] Research (research.md)
  [open] Assets (images/)
  [open] Narrative (narrative.md)
  [open] Study Documents (study-document.md)
  [open] Speaker Script (speaker-script.md)
  [open] Slides (presentation.pptx)

  -> Next step: Assets
  Continue, or jump to another phase?
```

- [ ] **Step 3: Update trigger chain in section 3**

Replace the trigger list under "### 3. Invoke the corresponding skill" with:

```markdown
Based on the user's choice, invoke the appropriate skill:
- No config found -> `talk-setup`
- No `talk.yaml` -> `talk-briefing`
- No `vision.md` -> `talk-vision`
- No `research.md` -> `talk-research`
- No images -> `talk-assets`
- No `narrative.md` -> `talk-narrative`
- No `study-document.md` -> `talk-study-doc`
- No `speaker-script.md` -> `talk-script`
- No `presentation.pptx` -> `talk-slides`
```

- [ ] **Step 4: Add `_build/` detection section**

Add after the "### 4. Handle empty directory" section:

```markdown
### 5. Detect _build/ directory

If a `_build/` directory exists in the project:
- If `_build/node_modules/` exists, offer to clean it up: "Found leftover node_modules in _build/. Want me to delete it to save space? (You can regenerate it anytime with `npm install` inside `_build/`)"
- If `_build/` contains generation scripts (`.js` files), mention: "Previous generation scripts are available in `_build/` — these can be used to regenerate or modify the presentation."
```

- [ ] **Step 5: Commit**

```bash
git add skills/talk/SKILL.md
git commit -m "fix(talk): reorder phases and add _build/ detection"
```

---

### Task 2: Overhaul talk-assets — page extraction, Gemini prompts, didactic focus

**Files:**
- Modify: `skills/talk-assets/SKILL.md`

**Covers spec sections:** 2a, 2b, 2c, 2d, Issue I

- [ ] **Step 1: Update skill description and intro**

Replace the opening paragraphs (lines 1-8) with:

```markdown
---
name: talk-assets
description: Use when extracting and preparing visual assets for a presentation. Extracts full pages from PDFs as PNG+PDF, proposes didactic image prompts for Gemini, and creates an image map. Triggers when /talk detects research.md exists but images/ is empty.
---

# Talk Builder — Visual Assets

Extract relevant pages from research papers, propose didactic images for generation with Gemini, and create a visual asset library for the presentation.
```

- [ ] **Step 2: Update Important section**

Replace the Important section with:

```markdown
## Important

- Always maintain aspect ratio when processing images. NEVER distort by adjusting width and height independently.
- For each extracted page, generate TWO files: the page as PNG (.png) AND the page as PDF (.pdf) for vector quality in Keynote.
- Naming convention: `author-year-pN-description` (e.g., `smith2024-p4-survival-curve`)
- Images must be **didactic and self-explanatory** — they should help the audience understand complex concepts, not just decorate slides.

Read `research.md` to know which papers and findings are relevant.
Read `config.yaml` for the presentation's color palette and style (used for generative image prompts).
```

- [ ] **Step 3: Update Dependencies section**

Replace the Dependencies section with:

```markdown
## Dependencies

Requires `poppler-utils` installed (`pdftoppm`, `pdfseparate`). If not available, warn the user and suggest: `brew install poppler`
```

- [ ] **Step 4: Replace Step 2 (extraction method)**

Replace the entire "### Step 2: Extract images — Hybrid approach" section with:

```markdown
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
```

- [ ] **Step 5: Remove Step 3 (dual files) — now redundant**

Delete the entire "### Step 3: Generate dual files per figure" section. Dual file generation is now part of Step 2.

Renumber remaining steps: Step 4 → Step 3, Step 5 → Step 4, Step 6 → Step 5.

- [ ] **Step 6: Replace generative images section (was Step 5, now Step 4)**

Replace with:

```markdown
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
```

- [ ] **Step 7: Update image-map section (was Step 6, now Step 5)**

Replace the image-map example with:

```markdown
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
```

- [ ] **Step 8: Update After completion message**

Replace with:

```markdown
## After completion

Tell the user: "Assets prepared! Review the images/ folder and generate any AI images from the prompt files using Gemini. Next phase: Narrative — building the slide structure with storytelling. Continue with /talk or /talk-narrative."
```

- [ ] **Step 9: Commit**

```bash
git add skills/talk-assets/SKILL.md
git commit -m "fix(talk-assets): page extraction only, Gemini prompts, didactic focus"
```

---

### Task 3: Add data visualization step to talk-narrative

**Files:**
- Modify: `skills/talk-narrative/SKILL.md`

**Covers spec sections:** 3 (Data Visualizations), Issues D, H

- [ ] **Step 1: Add visualization step after Step 5 (build slide-by-slide)**

Insert after "### Step 5: Build slide-by-slide structure" and before "### Step 6: Apply quality checks":

```markdown
### Step 6: Generate data visualizations

For any slide that would benefit from a data visualization (bar chart, survival curve, forest plot, comparison chart, clinical algorithm flowchart, etc.):

1. Identify the data from `research.md` that needs visual representation
2. Generate an SVG file with **transparent background**
3. Write the SVG directly — no external libraries needed for most charts. For complex visualizations, use a Node.js script with d3.
4. Save to `images/[VIZ]-description.svg`
5. Add to `images/image-map.md` with status "Generated"

The user can convert SVG to PNG for Keynote if needed, or use SVG directly.

Only generate visualizations that the narrative identifies as necessary — do not create them speculatively.
```

- [ ] **Step 2: Renumber subsequent steps**

- Step 6 (Apply quality checks) → Step 7
- Step 7 (Present and iterate) → Step 8

- [ ] **Step 3: Update After completion message**

Replace with:

```markdown
## After completion

Tell the user: "Narrative approved! Next phase: Study Document — building the comprehensive reference document. Continue with /talk or /talk-study-doc."
```

- [ ] **Step 4: Commit**

```bash
git add skills/talk-narrative/SKILL.md
git commit -m "feat(talk-narrative): add data visualization step, update next phase"
```

---

### Task 4: Rewrite talk-study-doc — Markdown, review article format

**Files:**
- Modify: `skills/talk-study-doc/SKILL.md`

**Covers spec sections:** 4a, 4b, 4c

- [ ] **Step 1: Replace the entire SKILL.md**

Write the complete new content:

```markdown
---
name: talk-study-doc
description: Use when generating study documents for a presentation — a comprehensive reference document and per-article summaries in Markdown. Triggers when /talk detects narrative.md exists but no study-document.md.
---

# Talk Builder — Study Documents

Generate two Markdown documents: a comprehensive reference document following the talk structure, and per-article summaries.

## Important

- Read `research.md` for all evidence and references
- Read `narrative.md` for the presentation structure — the study document follows this order
- Read `talk.yaml` for language preference
- ALL content must be in the language specified in config/talk.yaml
- Every claim must include its reference (DOI/PMID) — NEVER invent citations
- Write in **review article style** — continuous prose, NO bullet points
- This document serves as a **permanent reference**: the speaker should be able to re-open it a year later and refresh all knowledge needed to re-present the talk

## Output 1: study-document.md

A comprehensive reference document that follows the talk's narrative structure. The speaker should be able to read this cover-to-cover and fully understand every aspect of the presentation topic.

### Document Structure

```markdown
# [Talk Title]
Date: YYYY-MM-DD | Author: [name from config]

## Executive Summary
[~500 words of narrative prose providing a global vision of the topic — what it is,
why it matters, where the field stands, and what this talk contributes]

## 1. [First section title from narrative.md]

[Continuous prose — review article style. Cover:]
[- Full context of the topic, beyond what appears on slides]
[- All relevant evidence with exact data and inline references (Author et al., Year; DOI)]
[- Why this matters for the audience]
[- Areas of active debate or controversy]
[- Where evidence is strong vs. weak or emerging]
[- Background the speaker should know but won't say on stage]

### Frequently Asked Questions
[Q: [Question a listener might ask about this section]
A: [Developed answer in prose, with references]]

## 2. [Next section from narrative.md]
[Same structure as above]

...

## Extended Q&A Preparation

### Basic Questions (non-specialists)
[Q&A pairs in prose — questions a general audience might ask]

### Technical Questions (experts)
[Q&A pairs — questions from specialists in the field]

### Challenging Questions (controversial topics)
[Q&A pairs — difficult questions about limitations, contradictions, or ethical aspects]

## Complete References
[Full reference list in consistent format with DOI/PMID for every entry]
```

### Writing Style

- Review article prose: paragraphs with transitions, not bullet lists
- Include context that helps the speaker understand WHY, not just WHAT
- Highlight controversial areas and areas of active debate
- Note where evidence is strong vs. weak
- Be comprehensive: the speaker should not need to re-read the original papers to refresh their knowledge
- Write as if for a medical journal review, but accessible to the speaker's level

## Output 2: article-summaries.md

A document with a 200-300 word summary for each paper used in the presentation.

### Per-Article Structure

```markdown
# Article Summaries — [Talk Title]

## [Author et al. — "Title" (Year)]
**Journal:** [Name], [Volume], [Pages]
**DOI:** [doi] | **PMID:** [pmid]

**Summary:** [200-300 words covering study objective and design, key methodology,
main findings with numbers, clinical significance, and relevance to this presentation.
Written as continuous prose, not bullets.]

**Key quote:** "[Most relevant sentence from the paper]"

**Relevance to your talk:** [How this paper supports the narrative — which section
it feeds into and why it matters for the argument]
```

## After completion

Tell the user: "Study documents generated! Review them to prepare for your presentation. Next phase: Speaker Script — your slide-by-slide delivery guide. Continue with /talk or /talk-script."
```

- [ ] **Step 2: Commit**

```bash
git add skills/talk-study-doc/SKILL.md
git commit -m "fix(talk-study-doc): markdown output, review article format, new trigger"
```

---

### Task 5: Rewrite talk-script — Markdown output

**Files:**
- Modify: `skills/talk-script/SKILL.md`

**Covers spec sections:** 5a, 5b, 5c, Issue C

- [ ] **Step 1: Replace the entire SKILL.md**

Write the complete new content:

```markdown
---
name: talk-script
description: Use when generating the speaker script for a presentation — slide-by-slide delivery guide with preparation table and teleprompter format in Markdown. Triggers when /talk detects study-document.md exists but no speaker-script.md.
---

# Talk Builder — Speaker Script

Generate a comprehensive speaker script in Markdown with two sections: a preparation table and a teleprompter-formatted delivery script.

## Important

- Read `references/teleprompter-format.md` in this skill's directory for formatting rules
- Read `narrative.md` for slide structure, content, and connectors
- Read `vision.md` for emotional intent
- Read `talk.yaml` for language preference
- Write in the language specified in config/talk.yaml
- Use conversational, natural language — short sentences, no jargon unless necessary
- The script must feel like natural speech, not written text

## Output: speaker-script.md

### Section 1: Preparation Table

A Markdown table with one row per slide:

```markdown
| Slide | Title | What to Say | Bridge to Next | Timing |
|---|---|---|---|---|
| 1 | [Title] | [Natural prose — what to communicate, key phrases to use, emotional tone] | [The connector sentence/question leading to the next slide] | 45s |
| 2 | [Title] | ... | ... | ... |
```

**Writing style for "What to Say" column:**
- Conversational prose, as if explaining to a colleague
- Include specific phrases the speaker might use
- Note where to pause, where to speed up, where to make eye contact
- Reference data points with exact numbers
- Note emotional moments: "(slow down here)", "(make eye contact)", "(pause for effect)"

**Writing style for "Bridge to Next" column:**
- The exact transition sentence or question
- Must feel natural, not mechanical
- Use connector types from storytelling-guide.md (narrative bridge, callback, rhetorical question, contrast)

### Section 2: Teleprompter

Full delivery script formatted according to `references/teleprompter-format.md`:

- Short lines (5-7 words)
- `[PAUSE]` markers
- KEY words in CAPS
- `--- SLIDE [N]: [Title] ---` markers
- `[ADVANCE SLIDE]` cues
- `[TIME: X:XX]` markers at section starts
- Bridges between slides formatted naturally

The teleprompter script must cover EVERY slide including:
- Opening hook
- All content slides
- Transitions
- STAR moment (mark with `[STAR MOMENT]`)
- Closing

### Quality Checks

Before generating, verify:
- [ ] Every slide has a bridge to the next (except the last)
- [ ] Bridges are varied — not all the same type
- [ ] Language matches config setting
- [ ] Timing adds up to within the duration (with buffer)
- [ ] Emotional beats from vision.md are reflected in the script
- [ ] STAR moment is clearly marked and impactful
- [ ] Opening and closing are connected (callback pattern)

## After completion

Tell the user: "Speaker script generated! Next phase: Slides — generating the PPTX presentation. Continue with /talk or /talk-slides."
```

- [ ] **Step 2: Commit**

```bash
git add skills/talk-script/SKILL.md
git commit -m "fix(talk-script): markdown output, updated trigger and completion message"
```

---

### Task 6: Update talk-slides — `_build/` directory, last phase

**Files:**
- Modify: `skills/talk-slides/SKILL.md`

**Covers spec sections:** 6a, 6b, Issues E, F

- [ ] **Step 1: Update skill description**

Replace the description in frontmatter:

```markdown
---
name: talk-slides
description: Use when generating the PPTX presentation file from an approved narrative structure. Applies the user's personal style and design principles. Triggers when /talk detects speaker-script.md exists but no presentation.pptx.
---
```

- [ ] **Step 2: Add `_build/` instructions to Step 2 (Generate PPTX)**

Replace the current Step 2 content with:

```markdown
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
```

- [ ] **Step 3: Update Important section — add speaker-script.md reference**

Add to the Important section's reading list:

```markdown
- Read `speaker-script.md` to understand the full delivery context
```

- [ ] **Step 4: Update After completion message**

Replace with:

```markdown
## After completion

Tell the user: "Slides generated! Your Talk Builder project is complete. All outputs:
- study-document.md — comprehensive reference document
- article-summaries.md — quick reference per paper
- speaker-script.md — delivery guide with teleprompter
- presentation.pptx — open in Keynote for visual fine-tuning
- _build/ — generation scripts (reusable for modifications)

Run /talk to see the full project status."
```

- [ ] **Step 5: Commit**

```bash
git add skills/talk-slides/SKILL.md
git commit -m "fix(talk-slides): add _build/ directory, update as last phase"
```

---

### Task 7: Update talk-setup — remove DOCX dependency, fix poppler check

**Files:**
- Modify: `skills/talk-setup/SKILL.md`

**Covers spec sections:** 7, Issues A, B

- [ ] **Step 1: Remove DOCX skill from section 6a**

Replace the "#### 6a. Required Claude Code plugins" section with:

```markdown
#### 6a. Required Claude Code plugins

Talk Builder depends on the official Anthropic PPTX skill for presentation generation. Check if it is installed and guide the user if not:

**PPTX skill** (for presentation generation):
- Required for `/talk-slides`
- Install via: `/plugin` → select `claude-plugins-official` marketplace → install `pptx`

Tell the user:
"Talk Builder needs the official PPTX skill from Anthropic to generate presentation files. Please install it from the `claude-plugins-official` marketplace using `/plugin` if you haven't already."
```

- [ ] **Step 2: Update poppler check in section 6b**

Replace the poppler-utils verification with:

```markdown
**poppler-utils** (for page extraction from PDFs):
Verify installed by running:

```bash
which pdftoppm && which pdfseparate
```

If not found, tell the user:
"Talk Builder needs poppler-utils for extracting pages from PDFs. Install with: `brew install poppler`"
```

- [ ] **Step 3: Commit**

```bash
git add skills/talk-setup/SKILL.md
git commit -m "fix(talk-setup): remove DOCX dependency, update poppler check"
```

---

### Task 8: Final verification — cross-check all changes

- [ ] **Step 1: Verify trigger chain consistency**

Read all 7 modified files and confirm:
- `talk/SKILL.md` phase order matches all individual skill triggers
- Every "After completion" message points to the correct next skill
- All file references use `.md` (not `.docx`)
- No remaining references to `pdfimages`
- No remaining references to DOCX skill or `npm install docx`

- [ ] **Step 2: Verify against spec issues checklist**

Check every item from the spec:
- [ ] A — DOCX removed from talk-setup ✓
- [ ] B — pdfimages removed from talk-setup ✓
- [ ] C — talk-script completion message uses .md ✓
- [ ] D — talk-narrative points to Study Document ✓
- [ ] E — talk-slides says "Project complete!" ✓
- [ ] F — _build/ instructions in talk-slides ✓
- [ ] G — _build/ detection in orchestrator ✓
- [ ] H — Data visualization step in talk-narrative ✓
- [ ] I — Gemini prompts + didactic focus in talk-assets ✓

- [ ] **Step 3: Commit verification notes (if any fixes needed)**

```bash
git add -A
git commit -m "fix: address remaining inconsistencies from cross-check"
```
