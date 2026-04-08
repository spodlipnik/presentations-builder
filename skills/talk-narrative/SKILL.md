---
name: talk-narrative
description: Use when building the slide structure and storytelling arc for a presentation. Creates docs/narrative.md with slide-by-slide plan including timing, connectors, and storytelling elements. Triggers when /talk detects docs/research.md exists but no docs/narrative.md.
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
- Read `docs/talk.yaml`, `docs/vision.md`, and `docs/research.md` (including the Visual Elements Catalog and comprehensive paper summaries)
- Read `${user_config.assets_path}/config.yaml` for style preferences (colors, fonts, language)
- **Language priority:** Use the language the user writes in. Fall back to config.language for ambiguous messages.
- The narrative must serve the user's vision and emotional intent, not just present facts
- This is ITERATIVE — present the structure and refine until the user approves

## Workflow

### Step 1: Select pacing template

Based on `docs/talk.yaml` duration, select the appropriate template from `${CLAUDE_PLUGIN_ROOT}/references/pacing-guide.md`. Show it to the user as the structural skeleton.

### Step 2: Design macro structure

Apply the ABT framework to the entire talk:
- AND: establish context (what we know)
- BUT: introduce tension (the problem, gap, contradiction)
- THEREFORE: deliver resolution (findings, implications, call to action)

Map the Sparkline rhythm:
- Plan at least 3-4 oscillations between "what is" and "what could be"
- Place the STAR moment at approximately 2/3 of the talk

Look for a **narrative thread** — a repeating pattern, a recurring character, a question that evolves. The strongest talks have a thread that the audience tracks unconsciously. Examples from the storytelling guide: patient story bookend, progressive revelation, the "rule of three" with a twist.

### Step 2b: Discuss organizational structure

Propose 2-3 organizational structures that fit the specific talk's content and vision. Don't present a generic menu — think about what would work best for THIS talk and explain why. Some patterns that work well:

- **By questions** — Each section answers one question. Works for educational/review talks.
- **By themes/topics** — Classic sections. Works for talks covering multiple subtopics.
- **By chronology** — Time periods mark sections. Works for field evolution talks.
- **By hypothesis** — "What we believed / What we found / What it means". Works for surprising findings.
- **By progressive revelation** — Repeating pattern that builds, then breaks. Very powerful.
- **Something completely different** — The best talks sometimes invent their own structure.

Discuss with the user and decide together. The structure should serve the story, not constrain it. Be creative.

Based on the chosen structure, consider:

1. **Roadmap slide** — Propose one if it fits (e.g., "5 questions" works, but a cold-open mystery talk would be ruined by showing the roadmap upfront). Let the user decide.

2. **Section divider slides** between major sections:
   - Dark background, large text
   - Section label in accent color (e.g., "QUESTION 3" in red)
   - The section title/question in large white text
   - Optionally a teaser subtitle in smaller gray italic
   - These slides are 5-10 seconds each — they're breaths, not content
   - Not every talk needs dividers — some flow better without them

3. **Section labels on content slides** within a section:
   - Small text in the upper-left corner
   - Keeps the audience oriented ("where am I in this talk?")
   - Use accent color from config.yaml
   - Discuss with user — some talks benefit from this, others don't

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

This is the most detailed step. For EACH slide, specify these fields:

- **Type line** — combines slide type, section label, timing, and sparkline in one line: `evidence | SECTION · SUBTOPIC | 60s | CB`. Types: `divider`, `evidence`, `emotional`, `data`, `content`, `opening`, `closing`. The `/talk-slides` skill uses the type to decide visual design (dark/light, layout, typography). Narrative does NOT specify visual design — that's the slides skill's job.
- **Content** — what appears on the slide: the visible text, data, visual description. Reference specific files from `docs/research.md`'s Visual Elements Catalog when available.
- **Image** — reference to specific file from Visual Elements Catalog, or `[GENERATE]` for assets to create, or `[SPEAKER ADDS IN KEYNOTE]` for clinical photos only the speaker has.
- **Speaker** — actual draft dialogue. Write it as the speaker would say it on stage: conversational, with emotional cues (pause), (slow down), (eye contact), (dramatic). Include exact data points with numbers. This becomes the raw material for the speaker script phase.
- **Context** — the comprehensive backstory for this slide. Study design, N patients, exact results with p-values, mechanism, why it matters for the narrative, limitations, connections to other slides. The speaker should be able to read ONLY this field and fully understand everything behind the slide — without opening `docs/research.md` or any paper. Write 3-6 sentences minimum for evidence slides. This is what the speaker reads on the plane before the conference to refresh their knowledge.
- **Ref** — author, journal, year, DOI if available. For the speaker to cite on stage.
- **Bridge** — the exact transition sentence or question to the next slide. Must feel natural, not mechanical. Vary bridge types (narrative, rhetorical question, contrast, callback, dramatic pause).

**Design principles for each slide:**
- One message per slide — if you need two messages, make two slides
- Assertion-evidence titles on all content slides (exception: dramatic/emotional slides)
- Dark backgrounds for emotional/dramatic moments, light for evidence/data
- Big numbers deserve their own slide — don't bury "65% ORR" in a bullet list
- Empty or near-empty slides are powerful for pauses and transitions
- Split layouts work well for image + text combinations
- **Every word on the slide must earn its place.** Text is not decoration — it must reinforce the speaker's message or anchor a key concept for the audience. If removing a word doesn't weaken understanding, remove it. The slide supports the speaker, not the other way around. Test: "Would the audience understand the slide's message in 3 seconds?" If not, simplify.

### Slide Type (obligatorio) — 18 roles canónicos

Cada slide debe tener un `Type:` que corresponde a uno de los 18 roles:

`title`, `disclosure`, `agenda`, `section-divider`, `assertion-evidence`, `patient-case`, `methodology`, `data-chart`, `data-table`, `comparison`, `quote-pullout`, `image-fullbleed`, `image-gallery`, `timeline-process`, `key-takeaway`, `poll-question`, `contact`, `closing`.

Ver `${CLAUDE_PLUGIN_ROOT}/references/role-taxonomy.md` para descripción de cada rol.

### Slide Variant (opcional) — elección específica de layout

Si quieres controlar qué variante usar, añade `Variant:` con el ID de la variante definida en tu tema:

```
## Slide 5
Type: assertion-evidence
Variant: ae.image-right       ← elección explícita
Content: ...
```

Si omites `Variant:`, `talk-slides` lo elige automáticamente usando la rúbrica del tema y escribe la elección de vuelta como `Variant: X # auto`. Puedes cambiarla editando el archivo.

Para LOCKEAR una variante (para que auto no la sobrescriba), simplemente quita el sufijo ` # auto`.

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
- [ ] Context field is comprehensive for every evidence slide (no need to check other docs)
- [ ] All image references point to real files from `docs/research.md` catalog or are marked [GENERATE]
- [ ] Section divider slides between major sections (where appropriate)
- [ ] Section labels defined for content slides
- [ ] Every word on every slide earns its place — text supports the message, doesn't decorate
- [ ] Slide types correctly assigned (divider/evidence/emotional/data/content)

### Step 8: Present and save for review

Save `docs/narrative.md` to the working directory. Then show the user a **compact index** for quick scanning:

```
NARRATIVE INDEX — [Talk Topic] ([X] min, [N] slides)

OPENING
  1. Title
  2. COI
  3. [Opening hook — description]
--- SECTION: [Name/Question] ---
  4. [Divider: section title]
  5. [Assertion-evidence title]
  6. [Assertion-evidence title]
--- SECTION: [Name/Question] ---
  7. [Divider: section title]
  ...
CLOSING
  N. [Thank you / contact]
```

Tell the user:

"I've saved `docs/narrative.md`. You can review and edit it in two ways:

**Option A: Quick feedback here** — Tell me what to change: 'move slide 5 after 8', 'add a divider before 12', 'remove slide 6', 'I want a new slide about X between 7 and 8'.

**Option B: Annotate the document directly** — Open `docs/narrative.md` in your editor, add annotations where you want changes. Use any format you like:
- `[MOVE AFTER SLIDE 8]` next to a slide
- `[REMOVE]` on slides you don't want
- `[NEW SLIDE: about topic X]` where you want to insert
- `[CHANGE: I want this to be more about Y]` on any field
- Any free-text notes — I'll interpret them

When you're done annotating, just tell me 'I've edited docs/narrative.md' and I'll re-read the file, apply your changes, and generate a clean updated version."

Both options work. Option B is better for big structural changes because the user can see the full document and make multiple edits at once without chatting back and forth.

After each round of edits, show the updated compact index. Iterate until the user says the structure is approved.

## Output

Generate `docs/narrative.md`:

```markdown
# Narrative — [Talk Topic]

## Meta
- Duration: [X] minutes
- Total slides: [N]
- Key messages: [1, 2, 3]
- Organizational structure: [by questions / by themes / by chronology / by hypothesis / by progressive revelation]
- Opening technique: [type]
- Closing technique: [type]
- STAR moment: Slide [N] — [description]
- Attention reset: ~min [X], [description]
- Narrative thread: [description of the repeating pattern/story]

## Narrative Thread
[2-3 sentences describing the thread that runs through the talk — the repeating pattern, the evolving question, the character arc]

## Quick-Edit Index
[Compact numbered list of all slides — titles only, grouped by section, with dividers marked. This is the reference for fast editing.]

## [SECTION NAME] (slides N-M, ~X:XX)

### Slide N: [DIVIDER — Section title/question]
- **Type:** divider | [SECTION LABEL] | 5-10s
- **Content:** "[Section title or question]" large text. Optional teaser subtitle.

### Slide N+1: [Assertion-evidence title]
- **Type:** [evidence/emotional/data/content] | [SECTION · SUBTOPIC] | [seconds] | [IS/CB/STAR]
- **Content:** [what appears on screen — text, data, visual description]
- **Image:** [images/filename.png or [GENERATE]-description or [SPEAKER ADDS]]
- **Speaker:** "[Full draft dialogue with (emotional cues). Include exact 
  numbers and data points. Write as natural speech, not notes. This is 
  what you say on stage.]"
- **Context:** [Comprehensive context for this slide. Include: study design, 
  N patients, center(s), key results with exact numbers and p-values, 
  mechanism/rationale, why this matters for the narrative, limitations, 
  connections to other slides. The speaker should be able to read this 
  and fully understand the slide without opening any other document. 
  2-4 sentences minimum, more if the evidence is complex.]
- **Ref:** [Author et al., Journal Year; DOI if available]
- **Bridge:** "[exact transition sentence/question to next slide]"

### Slide N+2: ...

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
