# Role Taxonomy — Canonical Slide Roles for Academic/Medical Presentations

This document defines the **18 canonical slide roles** used across all themes in the Talk Builder system. Each role represents a distinct communicative purpose. Themes implement subsets of these roles with 2-4 **variants** each (different visual arrangements serving the same role).

Based on: Assertion-Evidence methodology (Michael Alley, Penn State), Presentation Zen (Garr Reynolds), IMRAD structure, PPTAgent research (arxiv 2501.03936).

## How to Use This Taxonomy

- **In `narrative.md`**: Set `Type:` to one of the 18 role IDs below
- **In `theme.yaml`**: Define `roles.<role-id>.variants[]` with concrete layouts
- **Custom roles**: Add to `theme.yaml` `custom_roles:` for theme-specific needs (e.g., `dermoscopy-findings`)

## The 18 Canonical Roles

### 1. `title`
**Purpose:** Opening slide of the presentation.
**Content:** Presentation title, author name, affiliation, date, optional branding.
**Variants:** `title.centered`, `title.image-left`, `title.fullbleed-overlay`

### 2. `disclosure`
**Purpose:** Conflicts of interest, funding sources, ethics statements.
**Content:** Bulleted or tabular listing of disclosures.
**Variants:** `disclosure.minimal`, `disclosure.table`

### 3. `agenda`
**Purpose:** Roadmap of the talk — what will be covered.
**Content:** Numbered list or icon grid of sections.
**Variants:** `agenda.numbered`, `agenda.icons-grid`

### 4. `section-divider`
**Purpose:** Visual transition between major sections (e.g., IMRAD phases).
**Content:** Large section heading, optional number/icon.
**Variants:** `divider.number-large`, `divider.fullbleed-quote`

### 5. `assertion-evidence` ⭐ DEFAULT
**Purpose:** Single assertion (sentence headline) supported by one visual evidence. Based on Michael Alley's methodology (p<.01 learning gains).
**Content:** Headline sentence (20-140 chars) + image/chart/diagram.
**Variants:** `ae.image-right`, `ae.image-left`, `ae.chart-center`, `ae.diagram-fullwidth`

### 6. `patient-case`
**Purpose:** Clinical vignette or case presentation.
**Content:** Patient photo/imaging + structured text (history, findings).
**Variants:** `case.photo-left`, `case.timeline-right`, `case.before-after`

### 7. `methodology`
**Purpose:** Study design, CONSORT diagram, process flowchart.
**Content:** Flowchart or horizontal step sequence.
**Variants:** `method.flowchart`, `method.steps-horizontal`

### 8. `data-chart`
**Purpose:** Quantitative results presentation.
**Content:** Chart + caption + optional key finding.
**Variants:** `chart.single-key`, `chart.dual-compare`, `chart.callout-stat`

### 9. `data-table`
**Purpose:** Numerical comparison, demographics, study arms.
**Content:** Table with headers + optional highlighted row.
**Variants:** `table.clean`, `table.highlighted-row`

### 10. `comparison`
**Purpose:** A vs B, before/after, arm1 vs arm2.
**Content:** Two-column layout (text or images).
**Variants:** `compare.two-col-text`, `compare.two-col-image`

### 11. `quote-pullout`
**Purpose:** Guideline quote, patient voice, expert testimony.
**Content:** Large attributed quote.
**Variants:** `quote.centered-large`, `quote.with-attribution-image`

### 12. `image-fullbleed`
**Purpose:** Single dominant image for visual impact (anatomy, imaging, emotional anchor).
**Content:** Full-bleed image + optional caption.
**Variants:** `full.caption-bottom`, `full.caption-overlay`

### 13. `image-gallery`
**Purpose:** Multiple images in grid (clinical series, dermoscopic cases).
**Content:** 2-6 images with labels/captions.
**Variants:** `gallery.2-vertical`, `gallery.2x2-grid`, `gallery.3x2-grid`, `gallery.comparative-pair`

### 14. `timeline-process`
**Purpose:** Progression, disease course, treatment pathway.
**Content:** Horizontal or vertical sequence of events.
**Variants:** `timeline.horizontal`, `timeline.vertical`

### 15. `key-takeaway`
**Purpose:** STAR moment, single-sentence summary, emphasis slide.
**Content:** Large statement OR 3 bullets with visual.
**Variants:** `takeaway.large-statement`, `takeaway.3-bullets-visual`

### 16. `poll-question`
**Purpose:** Interactive question to audience (live poll, rhetorical).
**Content:** Question + optional answer choices.
**Variants:** `poll.single-question`, `poll.multiple-choice`

### 17. `contact`
**Purpose:** Presenter contact information at end of talk.
**Content:** Name, email, institution, social handles.
**Variants:** `contact.card-centered`, `contact.minimal-horizontal`

### 18. `closing`
**Purpose:** Closing slide (Q&A prompt, thanks).
**Content:** Short message + optional image.
**Variants:** `closing.qa`, `closing.thanks`

## Complete Variant Vocabulary (43 variants)

```
title.centered · title.image-left · title.fullbleed-overlay
disclosure.minimal · disclosure.table
agenda.numbered · agenda.icons-grid
divider.number-large · divider.fullbleed-quote
ae.image-right · ae.image-left · ae.chart-center · ae.diagram-fullwidth
case.photo-left · case.timeline-right · case.before-after
method.flowchart · method.steps-horizontal
chart.single-key · chart.dual-compare · chart.callout-stat
table.clean · table.highlighted-row
compare.two-col-text · compare.two-col-image
quote.centered-large · quote.with-attribution-image
full.caption-bottom · full.caption-overlay
gallery.2-vertical · gallery.2x2-grid · gallery.3x2-grid · gallery.comparative-pair
timeline.horizontal · timeline.vertical
takeaway.large-statement · takeaway.3-bullets-visual
poll.single-question · poll.multiple-choice
contact.card-centered · contact.minimal-horizontal
closing.qa · closing.thanks
```

## Extending the Vocabulary

**Adding a canonical role** (shared across themes):
1. Edit this file: add role definition with purpose + variants
2. Update `references/variant-selection-rubric.md` with selection signals
3. Commit to plugin repo

**Adding a custom role** (theme-specific):
1. Edit `themes/<theme-id>/theme.yaml` under `custom_roles:`
2. No plugin changes needed
