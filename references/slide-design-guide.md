# Slide Design Guide for Medical and Academic Presentations

This document is the primary reference for visual design decisions in academic and medical slides. Every principle here is grounded in research or established expert practice. Every section includes a concrete do/don't example from the medical or academic domain. Read this before designing any slide.

---

## 1. Assertion-Evidence Method — Michael Alley

### The Principle

Replace topic-phrase headlines with full-sentence assertions. Support each assertion with visual evidence — a graph, image, diagram, or data table. Never use bullet points as the primary content below a headline.

### Why It Matters

Topic phrases ("Patient Outcomes", "Study Design", "Key Findings") tell the audience nothing. They force listeners to read the bullets and construct the meaning themselves, which competes with listening to you speak. A full-sentence assertion delivers the conclusion immediately. Paired with a visual, it gives the audience two parallel channels — linguistic and visual — reinforcing the same message. This is the single change with the highest return on investment in scientific presenting.

### Do

**Headline:** "Patients receiving combination therapy had 40% fewer readmissions at 90 days"
**Slide body:** A single bar chart showing readmission rates at 90 days, monotherapy vs. combination therapy, with the 40% difference annotated directly on the chart. No bullets anywhere on the slide.

### Don't

**Headline:** "Patient Outcomes"
**Slide body:**
- Readmission rates evaluated at 30, 60, and 90 days
- Combination therapy compared to monotherapy
- Results significant at p < 0.05
- N = 847 patients across 3 centers

The bullets force the audience to synthesize the conclusion. You have already synthesized it. Give it to them directly.

---

## 2. One Slide, One Message — Garr Reynolds / Jean-Luc Doumont

### The Principle

Each slide communicates exactly one idea. If you find yourself saying "and this slide also shows...", you have two slides on one frame. Split them.

### Why It Matters

Cognitive load theory (Sweller, 1988) and Mayer's Multimedia Learning principles establish that working memory is severely limited. When a slide presents multiple concurrent ideas, the audience allocates attention across all of them simultaneously, reducing retention for each. Doumont's formulation is precise: a slide is a claim. One claim per slide.

There is no penalty for slide count. A 30-minute talk with 40 focused slides outperforms a 30-minute talk with 15 overloaded slides. Audiences do not count slides — they track whether they understand what you are saying.

### Do

A slide that shows only a survival curve comparing two arms of a trial, with the headline "Median overall survival improved by 6.2 months in the immunotherapy arm (HR 0.71, 95% CI 0.58–0.87)." One curve, one message, one annotated hazard ratio.

### Don't

A single slide titled "Results" that contains: a survival curve, a forest plot of subgroup analyses, a toxicity table, and four bullet points summarizing p-values. This is a results section, not a slide. Every element deserves its own frame.

---

## 3. The Glance Test

### The Principle

A well-designed slide communicates its main point within three seconds of a first look. If a colleague glancing at your slide for three seconds cannot identify what it is about, the slide needs redesign.

### Why It Matters

Audiences do not study slides. They glance at them while simultaneously listening to you speak. Your visual must win attention and deliver the main point before the audience returns focus to you. If the visual requires more than three seconds of parsing, the audience has missed both the slide and what you said during that time.

### How to Test It

Print your slide deck or open it on a tablet. Show each slide to a colleague for exactly three seconds, then hide it. Ask them: "What was that slide about?" Their answer should match your intended message. If it does not, the slide is not communicating. This takes ten minutes and transforms a presentation.

### Do

A slide with the headline "Mortality dropped sharply after protocol implementation in March 2022", showing a single time-series line chart with a clear downward inflection point and a vertical reference line at March 2022. A colleague glancing for three seconds sees a line going down after a marker. Message received.

### Don't

A slide with no headline, a table of monthly mortality data with twelve rows and six columns, and a footnote explaining which columns to compare. After three seconds a colleague sees: a table. They cannot identify the direction, the time period, or the clinical significance.

---

## 4. The Billboard Test

### The Principle

Your slide must be readable and comprehensible at the equivalent of highway speed — the pace at which a driver reads a billboard. This forces radical simplification. If it would not fit on a billboard, it does not belong on a single slide in its current form.

### Why It Matters

Billboards work under a constraint you cannot engineer around: the viewer is moving. Medical and academic presenters face a structurally identical constraint — audience attention is moving. They are listening, thinking, taking notes, and checking their phones. The billboard test operationalizes this ruthlessly. Text smaller than a headline, tables with more than four columns, diagrams with more than five labeled nodes: these all fail.

### Do

A slide that reads: headline in 36pt font — "Surgery plus radiation reduced local recurrence by half" — with one clean diagram showing two patient pathways and their recurrence rates. A person seeing this at speed gets the message.

### Don't

A slide with a six-column table of dosing schedules, three footnotes in 10pt font, and a headline that reads "Comparative Analysis of Dosing Regimens Across Patient Stratification Groups in the Intent-to-Treat Population." A person seeing this at speed sees a wall of small text. Nothing is communicated.

---

## 5. Data-Ink Ratio — Edward Tufte

### The Principle

Maximize the proportion of ink (or pixels) on a slide devoted to displaying data. Every element that does not represent data is a candidate for removal. The ratio of data-ink to total ink should approach 1.0.

### Why It Matters

Tufte's formulation from *The Visual Display of Quantitative Information* (1983) remains the most rigorous framework for chart design. Every non-data element competes visually with data. Gridlines, decorative borders, drop shadows, 3D perspective, background images, and logo watermarks all reduce the signal-to-noise ratio of your visualization. In medical data, where the difference between two curves may represent a survival benefit, this noise is not aesthetic — it is clinically significant.

### Remove Without Hesitation

- Background gridlines (use axis ticks and direct data labels instead)
- Unnecessary chart borders and boxes
- 3D effects on any chart type
- Decorative elements and clipart
- Redundant legends when direct labels are possible
- Axis titles that merely repeat the axis values

### Never Use

- 3D bar charts (the perspective distorts apparent magnitude)
- Pie charts with more than three segments (humans cannot accurately judge angles; use a horizontal bar chart instead)
- Exploded pie charts at any segment count

### Before and After

**Before (low data-ink ratio):** A 3D pie chart with twelve segments showing medication adherence by patient subgroup. The 3D perspective distorts front segments. A corner legend requires eye travel. A gray gradient background and thick black border frame the chart. The title sits in a colored text box.

**After (high data-ink ratio):** A horizontal bar chart with twelve bars sorted descending. Each bar is labeled directly with its percentage. Single flat color. No gridlines, no border, no legend. The title is the assertion: "Adherence was lowest among patients aged 65+ without a care coordinator."

---

## 6. Visual Hierarchy and Contrast — Nancy Duarte / Slide:ology

### The Principle

Direct the audience's attention with deliberate contrast — in color, size, and position. Use a consistent visual language throughout the deck: the same color always means the same concept, the same font weight always signals the same level of importance.

### Why It Matters

Every slide is a composition. Without deliberate hierarchy, the eye wanders randomly and lands on whatever has the highest contrast by accident. Duarte's framework from *Slide:ology* (2008) establishes that hierarchy is not decoration — it is navigation. In a medical figure with multiple data series, visual hierarchy determines which series the audience reads first. If you want them to notice the intervention arm before the control arm, make the intervention arm visually dominant.

### Do

In a Kaplan-Meier curve comparing three arms, make the primary arm a solid, high-contrast color (e.g., dark blue), the comparator arm medium-weight gray, and the third arm a light gray dashed line. The audience knows immediately which curve to attend to. The headline confirms it: "The combination arm (blue) demonstrated superior 5-year survival." Use that same blue for the intervention in every chart, diagram, and table. Consistent color assignment reduces cognitive load because the audience does not re-decode the legend each time.

### Don't

Diagram a patient pathway by writing: "Patient → Screening → Enrollment → Randomization → Treatment → Follow-up → Outcome." This is a list dressed as a diagram. Instead, build a proper flowchart with boxes, directional arrows, and conditional branches. Show what happens when a patient fails screening. Show dropout rates as numbers at each node. Relationships must be diagrammed, not listed.

---

## 7. Full-Bleed Images — Garr Reynolds / Presentation Zen

### The Principle

High-quality photographs filling the entire slide serve as emotional anchors for key moments in a talk. The slide is not your teleprompter. Text does not have to appear on every frame.

### Why It Matters

Reynolds' *Presentation Zen* (2008) argues that slides exist to support the spoken message, not to document it. A full-bleed image of a patient consultation room, a laboratory bench, or a clinical setting communicates context and emotional weight in a way that bullet points cannot. The image creates the atmosphere; your voice carries the content.

This technique is most effective at transitions — between sections, at the opening, when introducing a case. It signals to the audience that something is shifting and gives them permission to stop reading and start listening.

### Do

Opening a talk on sepsis care: a full-bleed photograph of an ICU at night, monitors glowing, a nurse adjusting an IV line. No text except your name and the talk title in clean white sans-serif in the lower-left corner. The audience is placed in the world of your talk before you say a word.

### Don't

A slide with a small 400px photograph of a hospital corridor centered on a white background, surrounded by bullet points describing the clinical context. The image adds nothing — it is decoration. Commit fully to the image or remove it.

---

## 8. Progressive Disclosure

### The Principle

Build complex diagrams element by element across multiple slides or slide builds. Never reveal a full complex figure at once. Annotate every figure by circling, arrowing, or highlighting the specific part under discussion.

### Why It Matters

A complex pathway diagram presented all at once forces the audience to explore it freely. They will look at parts you have not reached yet. Progressive disclosure sequences attention to match your narrative — each component appears only when you are ready to discuss it.

The same logic applies to figures borrowed from published papers. Journals design figures for readers who can study them at length. Slides are seen for seconds. When you reproduce a published figure, you must adapt it: crop it, annotate it, simplify it.

### Do

A mechanistic diagram of mTOR signaling built across five slides. Slide 1 shows only the upstream receptor and the first kinase. Slides 2-4 add PI3K, AKT, and mTORC1 sequentially. Slide 5 shows the complete pathway with the drug target highlighted in the intervention color and a red inhibition symbol at the binding site. Each element appears only when you are ready to explain it.

### Don't

A full mTOR signaling pathway diagram from a published review article, shrunk to fit a slide, with a vague headline: "Mechanism of Action." The audience spends the entire slide trying to read labels too small to parse. You point at a region of the diagram and say "so this part here" while gesturing at something nobody can distinguish.

---

## 9. Typography Rules

### The Principle

Minimum 30-point font for any text that audience members must read. Use sans-serif typefaces for slides. Limit the presentation to two font families maximum. Distinguish clearly between title font and body font.

### Why It Matters

Guy Kawasaki's 30-point rule is a heuristic for a real problem: presenters routinely reduce font size to fit more text, which violates the one-slide-one-message principle and makes slides unreadable in large rooms. The rule forces you to cut content rather than shrink it.

Sans-serif fonts (Inter, Helvetica, Roboto, Source Sans) render more cleanly on projected screens than serif fonts at small sizes. Serif fonts work for body text in documents, not on slides. Two font families is a hard upper limit. One for titles (slightly larger, possibly a display weight), one for body text (regular or medium weight). Using more than two creates visual noise without adding communicative value.

### Do

Title typeface: Inter Bold, 36pt. Body typeface: Inter Regular, 28pt. Data labels on charts: Inter Medium, 22pt. Caption text (axis labels, footnotes): Inter Light, 18pt. No font below 18pt appears on any slide.

### Don't

A slide with a 14pt font table to fit twelve rows of demographic data, a 12pt footnote citing five references, a 10pt disclaimer in the corner, and a title in a decorative serif font at 28pt. Four different effective font weights with no systematic hierarchy.

---

## 10. Color Usage

### The Principle

Use a maximum of three to four colors per presentation. Reserve one accent color for emphasis only. Ensure sufficient contrast for all text and data. Never use red and green as the sole differentiator between two data categories.

### Why It Matters

Color is the most powerful channel for directing attention, and it is the easiest to overuse. More than four colors in a palette creates visual competition — every element is emphasizing something, so nothing is emphasized. The accent color must be used sparingly so that its appearance is a signal, not background noise.

Contrast is a readability requirement, not an aesthetic preference. Projected environments with ambient light degrade perceived contrast. The WCAG AA standard (4.5:1 for normal text, 3:1 for large text) is a conservative floor for slides.

Approximately 8% of men and 0.5% of women have red-green color vision deficiency. If your forest plot uses red for harmful subgroups and green for beneficial ones, a significant portion of your audience cannot distinguish them. Use blue and orange, or differentiate with line style and shape in addition to color.

### Do

A three-color palette for a clinical trial presentation: dark navy (primary text, control arm), institutional blue (intervention arm, primary emphasis), light gray (supporting elements, background data series). One accent: orange, used only for statistically significant findings. Color-blind safe throughout. Every use of orange in the deck means the same thing: this result is significant.

### Don't

A presentation using seven colors — red, orange, yellow, green, blue, purple, and pink — across various charts and diagrams with no consistent assignment. Red means "bad outcome" on one slide, "intervention arm" on another, and "statistically significant" on a third. The audience must re-decode color meaning every time, which exhausts working memory.

---

## Summary: The Hierarchy of Decisions

Apply these tests in order before finalizing any slide:

1. **Assertion first.** Does the headline state a complete conclusion? (Assertion-Evidence)
2. **One message.** Could this slide be split? If yes, split it. (One Slide, One Message)
3. **Three-second test.** Would a colleague understand the main point in three seconds? (Glance Test)
4. **Data clarity.** Is every non-data element removable? Remove it. (Data-Ink Ratio)
5. **Hierarchy.** Does the most important element have the highest visual weight? (Visual Hierarchy)
6. **Typography.** Is all text 30pt or above? Is the font sans-serif? (Typography Rules)
7. **Color.** Are you within four colors? Is color-blind safety maintained? (Color Usage)

A slide that passes all seven tests is ready to present.
