---
name: talk-narrative
description: Use when building the slide structure and storytelling arc for a presentation. Creates narrative.md with slide-by-slide plan including timing, connectors, and storytelling elements. Triggers when /talk detects assets ready but no narrative.md.
---

# Talk Builder — Narrative Structure & Storytelling

Build the complete slide-by-slide structure with storytelling arc, connectors, and timing. This is the heart of Talk Builder — where evidence becomes narrative.

## Important

- MUST read `references/storytelling-guide.md` before starting
- MUST read `references/slide-design-guide.md` for slide design principles
- MUST read `references/pacing-guide.md` to select the timing template
- Read `talk.yaml`, `vision.md`, `research.md`, and `images/image-map.md`
- The narrative must serve the user's vision and emotional intent, not just present facts
- This is ITERATIVE — present the structure and refine until the user approves

## Workflow

### Step 1: Select pacing template

Based on `talk.yaml` duration, select the appropriate template from `references/pacing-guide.md`. Show it to the user as the structural skeleton.

### Step 2: Design macro structure

Apply the ABT framework to the entire talk:
- AND: establish context (what we know)
- BUT: introduce tension (the problem, gap, contradiction)
- THEREFORE: deliver resolution (findings, implications, call to action)

Map the Sparkline rhythm:
- Plan at least 3-4 oscillations between "what is" and "what could be"
- Place the STAR moment at approximately 2/3 of the talk

### Step 3: Design opening

Based on the user's vision, propose 2-3 opening options from `references/storytelling-guide.md`:
- Cold open with patient case (if story thread exists)
- Startling statistic from research
- Provocative question
- Contrarian statement

Let the user choose.

### Step 4: Design closing

Propose 2-3 closing options that match the opening:
- Callback close (return to opening story)
- Vision of the future
- Call to action
- Patient quote

The closing MUST connect to the opening for narrative completeness.

### Step 5: Build slide-by-slide structure

Create each slide with:
- **Number and title** (assertion-evidence format — full sentence, not topic phrase)
- **Content** — what appears on the slide (visual, data, image reference)
- **Speaker intent** — what the speaker aims to convey
- **Image** — reference to file in `images/` or `[GENERATE]` or `[SPEAKER ADDS IN KEYNOTE]`
- **Bridge** — the narrative connector to the next slide (from storytelling-guide.md connector types)
- **Timing** — estimated seconds for this slide
- **Sparkline position** — is this a "what is" or "what could be" moment?

### Step 6: Generate data visualizations

For any slide that would benefit from a data visualization (bar chart, survival curve, forest plot, comparison chart, clinical algorithm flowchart, etc.):

1. Identify the data from `research.md` that needs visual representation
2. Generate an SVG file with **transparent background**
3. Write the SVG directly — no external libraries needed for most charts. For complex visualizations, use a Node.js script with d3.
4. Save to `images/[VIZ]-description.svg`
5. Add to `images/image-map.md` with status "Generated"

The user can convert SVG to PNG for Keynote if needed, or use SVG directly.

Only generate visualizations that the narrative identifies as necessary — do not create them speculatively.

### Step 7: Apply quality checks

Before presenting to user, verify:
- [ ] Rule of Three: no more than 3 key messages
- [ ] One message per slide
- [ ] Assertion-evidence titles on all content slides
- [ ] Attention reset planned every 10 minutes (for talks > 10 min)
- [ ] STAR moment placed at ~2/3
- [ ] Opening and closing are connected
- [ ] Every Bridge connector is specific (not "Next, we'll discuss...")
- [ ] Total timing fits within duration (with buffer)
- [ ] Sparkline has at least 3 oscillations

### Step 8: Present and iterate

Show the complete narrative structure to the user. Ask:
- "Does this flow feel right?"
- "Is the emotional arc what you envisioned?"
- "Any slides to add, remove, or reorder?"
- "Are the connectors natural?"

Iterate until the user approves.

## Output

Generate `narrative.md`:

```markdown
# Narrative — [Talk Topic]

## Meta
- Duration: [X] minutes
- Key messages: [1, 2, 3]
- Opening technique: [type]
- Closing technique: [type]
- STAR moment: Slide [N] — [description]

## Slide Structure

### Slide 1: [Title — Opening]
- **Type:** Opening
- **Content:** [what appears on screen]
- **Speaker intent:** [what to convey]
- **Image:** [reference or none]
- **Timing:** [seconds]
- **Sparkline:** [what is / what could be]
- **Bridge to next:** "[connector text]"

### Slide 2: [Assertion-evidence title]
- **Type:** Context
- **Content:** [visual/data description]
- **Speaker intent:** [what to convey]
- **Image:** [images/file.png]
- **Timing:** [seconds]
- **Sparkline:** [what is]
- **Bridge to next:** "[connector text]"

...

### Slide N: [Title — Closing]
- **Type:** Closing
- **Content:** [what appears on screen]
- **Speaker intent:** [callback to opening / call to action]
- **Image:** [reference or none]
- **Timing:** [seconds]
- **Sparkline:** [new bliss]
```

## After completion

Tell the user: "Narrative approved! Next phase: Study Document — building the comprehensive reference document. Continue with /talk or /talk-study-doc."
