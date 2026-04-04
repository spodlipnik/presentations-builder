# Talk Builder — Bugfixes & Improvements Design Spec

**Date:** 2026-04-04
**Scope:** 6 areas of improvement (PPT visual quality deferred to separate session)
**Source:** `/Users/sebastianpodlipnik/Personal/Presentaciones - keynote/corrections.txt`

---

## 1. Workflow Reorder

### Problem
The PPT is generated before the speaker script exists. It's hard to evaluate content without seeing the full script first.

### Solution
Change the phase order from:
```
briefing → vision → research → assets → narrative → slides → study-doc → script
```
To:
```
briefing → vision → research → assets → narrative → study-doc → script → slides
```

### Changes Required

**`talk/SKILL.md` (orchestrator):**
- Phase Detection table: update file markers and order
  - `study-document.md` + `article-summaries.md` detected after `narrative.md`
  - `speaker-script.md` detected after `study-document.md`
  - `presentation.pptx` detected after `speaker-script.md`
- Trigger chain updated:
  - No `study-document.md` but has `narrative.md` → `talk-study-doc`
  - No `speaker-script.md` but has `study-document.md` → `talk-script`
  - No `presentation.pptx` but has `speaker-script.md` → `talk-slides`

**"After completion" messages updated in each skill:**
- `talk-narrative` → "Next: Study Document"
- `talk-study-doc` → "Next: Speaker Script"
- `talk-script` → "Next: Slides (PPTX generation)"
- `talk-slides` → "Project complete!"

---

## 2. Assets Overhaul (talk-assets)

### Problem
- `pdfimages` extracts junk (icons, logos, backgrounds)
- Missing PDF page extraction alongside PNG
- Generative image prompts are generic, not optimized for Gemini
- Images proposed are decorative, not didactic
- No style coherence with presentation

### Solution

#### 2a. Page extraction only — eliminate `pdfimages`

Replace the hybrid approach (Method A + Method B) with a single method:

```bash
# PNG of full page at 300 DPI
pdftoppm -png -r 300 -f <page> -l <page> <paper.pdf> images/<prefix>

# PDF of the individual page (vector quality for Keynote)
pdfseparate -f <page> -l <page> <paper.pdf> images/<prefix>-page.pdf
```

- Remove ALL references to `pdfimages`
- Naming convention changes from `author-year-figN-description` to `author-year-pN-description` (pages, not figures)
- Always generate both PNG + PDF per page

#### 2b. Gemini-optimized prompts

Step 5 (propose generative images) changes:
- Prompts written for **Gemini** (descriptive natural language, no Midjourney syntax)
- Replace "Midjourney, Gemini, DALL-E" references with "Gemini" as primary model
- Each `[GENERATE]-description.txt` includes:
  - Detailed descriptive prompt (Gemini-optimized)
  - `style_context` section reading colors/fonts from `config.yaml` for coherence
  - Target slide reference
  - **Purpose statement**: how this image helps the audience understand a concept (not just decorate)

#### 2c. Didactic focus

Change the skill's framing from "high-impact images" to "self-explanatory, didactic images that help the audience understand complex concepts." The instruction must emphasize:
- Images must help understand context, not just decorate
- Propose illustrations that explain mechanisms, comparisons, processes
- If a concept is complex, propose a visual explanation

#### 2d. Dependencies update

- Remove `pdfimages` from dependency checks
- Only require `pdftoppm` and `pdfseparate` from poppler-utils

---

## 3. Data Visualizations in Narrative Phase

### Problem
No capability to generate charts, infographics, or data visualizations from study statistics.

### Solution

Add a step to `talk-narrative/SKILL.md`:

When designing a slide that would benefit from a data visualization (bar chart, survival curve, comparison, flowchart, etc.):
1. Claude generates it as SVG with **transparent background**
2. Writes the SVG directly (no external libraries needed for most charts) — for complex interactive visualizations, uses a Node.js script with d3
3. Saves to `images/[VIZ]-description.svg`
4. Adds to `image-map.md` with status "Generated"
5. The user converts SVG to PNG if needed for Keynote (or uses SVG directly)

This only happens when the narrative design identifies the need — not speculatively.

---

## 4. Study Document Redesign (talk-study-doc)

### Problem
- Output is too basic, too many bullets
- Doesn't review literature in depth
- Format doesn't allow re-reading a year later to refresh knowledge
- Uses DOCX which requires external skill dependency

### Solution

#### 4a. Markdown output
- `study-document.docx` → `study-document.md`
- `article-summaries.docx` → `article-summaries.md`
- Remove ALL references to DOCX skill, `npm install docx`, Node.js scripts
- Claude writes Markdown directly

#### 4b. Review article format following talk flow

Purpose: **permanent reference document** that follows the talk structure and allows the speaker to re-present months/years later with fresh knowledge.

Structure:
```markdown
# [Talk Title]
Date: YYYY-MM-DD | Author: [name]

## Executive Summary
[~500 words, narrative prose, global vision of the topic]

## 1. [First section from narrative.md]
[Continuous prose — review article style, NO bullets]
- Full context of the topic (beyond what's on slides)
- Evidence with exact data and inline references (DOI/PMID)
- Why it matters for the audience
- Areas of debate or controversy
- What the speaker should know beyond the slide content

### Frequently Asked Questions
[Prose format: question → developed answer]

## 2. [Next section from narrative.md]
...

## Extended Q&A Preparation
### Basic (non-specialists)
### Technical (experts)
### Challenging (controversial topics)

## Complete References
[Full list with DOI/PMID]
```

#### 4c. Trigger update
- Activates when `narrative.md` exists but `study-document.md` does not
- Remove dependency on `presentation.pptx` existing first

---

## 5. Speaker Script to Markdown (talk-script)

### Problem
- Uses DOCX requiring external dependency
- Trigger references `.docx` files

### Solution

#### 5a. Markdown output
- `speaker-script.docx` → `speaker-script.md`
- Remove ALL references to DOCX skill, `npm install docx`, Node.js scripts, `WidthType.DXA`
- Claude writes Markdown directly

#### 5b. Structure preserved in Markdown

**Section 1: Preparation Table** as Markdown table:
```markdown
| Slide | Title | What to Say | Bridge to Next | Timing |
|---|---|---|---|---|
| 1 | [Title] | [Natural prose, emotional notes] | [Transition phrase] | 45s |
```

**Section 2: Teleprompter** as plain Markdown following `teleprompter-format.md` rules.

#### 5c. Trigger update
- Activates when `study-document.md` exists but `speaker-script.md` does not
- "After completion" message lists all outputs with `.md` extensions
- Points to slides as next phase

---

## 6. Build Directory & Cleanup (talk-slides)

### Problem
PPTX/DOCX skills generate `generate_*.js`, `package.json`, `node_modules/`, etc. in the project root.

### Solution

#### 6a. `_build/` directory
- All generation scripts (`generate_presentation.js`, `package.json`, etc.) go in `_build/`
- `_build/` is **permanent** — scripts are reusable for future modifications
- `node_modules/` inside `_build/` is the only disposable part (regenerated with `npm install`)

#### 6b. talk-slides instructions
Add to `talk-slides/SKILL.md`:
- Create `_build/` directory before generating scripts
- Run `npm install` inside `_build/`
- Output `presentation.pptx` to project root (not inside `_build/`)
- After successful generation: delete `_build/node_modules/` to save space

#### 6c. Orchestrator cleanup detection
Add to `talk/SKILL.md`:
- On startup, if `_build/node_modules/` exists, offer to clean it up
- If `_build/` exists with scripts, mention it's available for re-generation

---

## 7. Setup Dependency Updates (talk-setup)

### Changes
- **Remove DOCX skill** from required dependencies (no longer needed)
- **Remove `pdfimages`** from poppler-utils check
- Update check to verify only `pdftoppm` and `pdfseparate`
- Keep PPTX skill as required (still needed for slides)
- Keep Node.js as required (still needed for slides)
- Keep LibreOffice as optional

---

## 8. Deferred: PPT Visual Quality

The following issues are **deferred to a dedicated session**:
- PPTX output not faithful to user's style
- Poor chapter/section separation
- No reproducible visual templates/layouts
- Overall design quality

These require deep design work on a template system, layout definitions, and visual guides.

---

## Summary of Files Modified

| File | Type of Change |
|---|---|
| `skills/talk/SKILL.md` | Reorder phases, update triggers, add `_build/` detection |
| `skills/talk-assets/SKILL.md` | Remove `pdfimages`, page-only extraction, Gemini prompts, didactic focus |
| `skills/talk-narrative/SKILL.md` | Add data visualization generation step |
| `skills/talk-study-doc/SKILL.md` | Markdown output, review article format, new trigger |
| `skills/talk-script/SKILL.md` | Markdown output, new trigger, updated completion message |
| `skills/talk-slides/SKILL.md` | `_build/` directory, updated trigger (last phase) |
| `skills/talk-setup/SKILL.md` | Remove DOCX dependency, update poppler check |

## Issues Checklist (from debugging)

- [ ] **A** — Remove DOCX skill from `talk-setup` dependencies
- [ ] **B** — Remove `pdfimages` from `talk-setup` poppler check
- [ ] **C** — Update `talk-script` completion message to `.md` outputs
- [ ] **D** — Update `talk-narrative` "After completion" → "Next: Study Document"
- [ ] **E** — Update `talk-slides` "After completion" → "Project complete!"
- [ ] **F** — Add `_build/` instructions to `talk-slides`
- [ ] **G** — Add `_build/` cleanup detection to orchestrator
- [ ] **H** — Add data visualization step to `talk-narrative`
- [ ] **I** — Change `talk-assets` to Gemini-focused, didactic prompts with style context
