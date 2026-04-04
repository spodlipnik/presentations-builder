---
name: talk-narrative
description: Use when building the slide structure and storytelling arc for a presentation. Creates narrative.md with slide-by-slide plan including timing, connectors, and storytelling elements. Triggers when /talk detects research.md exists but no narrative.md.
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Glob
---

# Talk Builder — Narrative Structure & Storytelling

Build the complete slide-by-slide structure with storytelling arc, visual design, speaker text, and timing. This is the heart of Talk Builder — where evidence becomes a story that moves people.

The goal is NOT to organize information into slides. It's to design an emotional journey that happens to use slides as a medium. Every slide is a beat in a story — it should make the audience feel something, not just know something.

## Important

- MUST read `${CLAUDE_PLUGIN_ROOT}/references/storytelling-guide.md` before starting
- MUST read `${CLAUDE_PLUGIN_ROOT}/references/slide-design-guide.md` for slide design principles
- MUST read `${CLAUDE_PLUGIN_ROOT}/references/pacing-guide.md` to select the timing template
- Read `talk.yaml`, `vision.md`, and `research.md` (including the Visual Elements Catalog and comprehensive paper summaries)
- Read `${user_config.assets_path}/config.yaml` for style preferences (colors, fonts, language)
- **Language priority:** Use the language the user writes in. Fall back to config.language for ambiguous messages.
- The narrative must serve the user's vision and emotional intent, not just present facts
- This is ITERATIVE — present the structure and refine until the user approves

## Workflow

### Step 1: Select pacing template

Based on `talk.yaml` duration, select the appropriate template from `${CLAUDE_PLUGIN_ROOT}/references/pacing-guide.md`. Show it to the user as the structural skeleton.

### Step 2: Design macro structure

Apply the ABT framework to the entire talk:
- AND: establish context (what we know)
- BUT: introduce tension (the problem, gap, contradiction)
- THEREFORE: deliver resolution (findings, implications, call to action)

Map the Sparkline rhythm:
- Plan at least 3-4 oscillations between "what is" and "what could be"
- Place the STAR moment at approximately 2/3 of the talk

Look for a **narrative thread** — a repeating pattern, a recurring character, a question that evolves. The strongest talks have a thread that the audience tracks unconsciously. Examples from the storytelling guide: patient story bookend, progressive revelation, the "rule of three" with a twist.

### Step 3: Design opening

Based on the user's vision, propose 2-3 opening options from `${CLAUDE_PLUGIN_ROOT}/references/storytelling-guide.md`:
- Cold open with patient case (if story thread exists)
- Startling statistic from research
- Provocative question
- Contrarian statement

Let the user choose. The opening sets everything — it defines the emotional contract with the audience.

### Step 4: Design closing

Propose 2-3 closing options that match the opening:
- Callback close (return to opening story/number)
- Vision of the future
- Call to action
- Patient quote

The closing MUST connect to the opening for narrative completeness. The audience should feel the circle close.

### Step 5: Build slide-by-slide structure

This is the most detailed step. For EACH slide, specify:

- **Number and title** — assertion-evidence format (full sentence, not topic phrase). The title IS the takeaway.
- **Visual design** — background (dark/light), layout (full, split, two-column), label/section marker, typography size/weight for key elements
- **Content** — what appears on the slide: text, data, image reference. Reference specific files from research.md's Visual Elements Catalog when available.
- **Speaker text** — NOT just "what to convey" but actual draft dialogue. Write it as the speaker would say it on stage: conversational, with emotional cues (pause), (slow down), (eye contact), (dramatic). Include exact data points with numbers. This becomes the raw material for the speaker script phase.
- **Image** — reference to specific file from Visual Elements Catalog, or `[GENERATE]` for assets to create, or `[SPEAKER ADDS IN KEYNOTE]` for clinical photos only the speaker has
- **Timing** — estimated seconds for this slide
- **Sparkline position** — "what is" (IS) or "what could be" (CB) or STAR
- **Bridge to next** — the exact transition sentence or question. Must feel natural, not mechanical. Vary bridge types throughout (narrative, rhetorical question, contrast, callback, dramatic pause).

**Design principles for each slide:**
- One message per slide — if you need two messages, make two slides
- Assertion-evidence titles on all content slides (exception: dramatic/emotional slides)
- Dark backgrounds for emotional/dramatic moments, light for evidence/data
- Big numbers deserve their own slide — don't bury "65% ORR" in a bullet list
- Empty or near-empty slides are powerful for pauses and transitions
- Split layouts work well for image + text combinations

### Step 6: Plan attention reset (for talks > 10 min)

At approximately the 10-minute mark, plan a deliberate attention reset — a moment that breaks the pattern and re-engages the audience. This could be:
- A surprising connection between two seemingly unrelated topics
- A shift in tone (from data to personal, from clinical to philosophical)
- A visual surprise (blank slide, dramatic image, huge number)

### Step 7: Apply quality checks

Before presenting to user, verify:
- [ ] Rule of Three: no more than 3 key messages for the entire talk
- [ ] One message per slide
- [ ] Assertion-evidence titles on all content slides
- [ ] Attention reset planned every 10 minutes (for talks > 10 min)
- [ ] STAR moment placed at ~2/3
- [ ] Opening and closing are connected (callback)
- [ ] Every bridge connector is specific and varied (not all "Next, we'll discuss...")
- [ ] Total timing fits within duration (with 1-2 min buffer)
- [ ] Sparkline has at least 3 oscillations
- [ ] Speaker text includes emotional cues, not just content
- [ ] Visual design specified for every slide (dark/light, layout)
- [ ] All image references point to real files from research.md catalog or are marked [GENERATE]

### Step 8: Present and iterate

Show the complete narrative structure to the user. Ask:
- "Does this flow feel right?"
- "Is the emotional arc what you envisioned?"
- "Any slides to add, remove, or reorder?"
- "Are the transitions natural?"
- "Do the speaker texts capture how you'd actually talk?"

Iterate until the user approves.

## Output

Generate `narrative.md`:

```markdown
# Narrative — [Talk Topic]

## Meta
- Duration: [X] minutes
- Total slides: [N]
- Key messages: [1, 2, 3]
- Opening technique: [type]
- Closing technique: [type]
- STAR moment: Slide [N] — [description]
- Attention reset: ~min [X], [description]
- Narrative thread: [description of the repeating pattern/story]

## Narrative Thread
[2-3 sentences describing the thread that runs through the talk — the repeating pattern, the evolving question, the character arc]

## [SECTION NAME] (slides N-M, ~X:XX)

### Slide N: [Assertion-evidence title]
- **Background:** [dark/light]
- **Layout:** [full / split / two-column]
- **Label:** [section marker if any]
- **Content:** [what appears on screen — text, data, visual description]
- **Image:** [images/filename.png or [GENERATE]-description or [SPEAKER ADDS]]
- **Speaker:** "[Full draft dialogue with (emotional cues). Include exact numbers and data points. Write as natural speech, not notes.]"
- **Ref:** [Author Year — for the speaker to cite on stage]
- **Timing:** [seconds]
- **Sparkline:** [IS / CB / STAR]
- **Bridge:** "[exact transition sentence/question to next slide]"

### Slide N+1: ...

---

## Timing Summary

| Section | Slides | Time |
|---------|--------|------|
| [Section 1] | 1-4 | ~X:XX |
| [Section 2] | 5-10 | ~X:XX |
| ... | ... | ... |
| **TOTAL** | **N slides** | **~XX:XX** |

## Sparkline Map

[Visual representation of the emotional rhythm across all slides, showing IS/CB oscillations and STAR moment position]
```

## After completion

Tell the user: "Narrative approved! Next phase: Assets — creating and extracting the visual elements for each slide. Continue with /talk or /talk-builder:talk-assets."
