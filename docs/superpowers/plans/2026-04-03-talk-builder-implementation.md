# Talk Builder Plugin — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a multi-skill Claude Code plugin that guides users through creating academic/medical presentations with storytelling, from research to final PPTX and DOCX outputs.

**Architecture:** Plugin with 10 skills (1 orchestrator, 1 setup, 8 phase skills) + 4 shared reference documents + config infrastructure. Skills are markdown-based (SKILL.md). The plugin detects project state via file presence in the working directory.

**Tech Stack:** Claude Code plugin system (SKILL.md files, plugin.json), YAML config, Markdown references. Runtime dependencies: poppler-utils (PDF image extraction), Claude MCPs (PubMed, Consensus).

**Spec:** `docs/superpowers/specs/2026-04-03-talk-builder-design.md`

---

## File Map

### Plugin Infrastructure
- Create: `plugin.json`
- Create: `.gitignore`
- Create: `config.example.yaml`
- Create: `assets/README.md`

### Reference Documents (shared across skills)
- Create: `references/storytelling-guide.md`
- Create: `references/slide-design-guide.md`
- Create: `references/data-storytelling.md`
- Create: `references/pacing-guide.md`

### Skills
- Create: `skills/talk-setup/SKILL.md`
- Create: `skills/talk/SKILL.md`
- Create: `skills/talk-briefing/SKILL.md`
- Create: `skills/talk-vision/SKILL.md`
- Create: `skills/talk-research/SKILL.md`
- Create: `skills/talk-assets/SKILL.md`
- Create: `skills/talk-narrative/SKILL.md`
- Create: `skills/talk-slides/SKILL.md`
- Create: `skills/talk-study-doc/SKILL.md`
- Create: `skills/talk-script/SKILL.md`
- Create: `skills/talk-script/references/teleprompter-format.md`

---

## Task 1: Plugin Scaffolding

**Files:**
- Create: `plugin.json`
- Create: `.gitignore`
- Create: `config.example.yaml`
- Create: `assets/README.md`

- [ ] **Step 1: Create plugin.json**

```json
{
  "name": "talk-builder",
  "description": "Multi-skill plugin for building academic and medical presentations with storytelling, from research to PPTX and speaker scripts",
  "version": "0.1.0",
  "author": {
    "name": "Sebastian Podlipnik"
  },
  "license": "MIT",
  "keywords": ["presentations", "academic", "medical", "storytelling", "slides", "pptx", "speaker-script"]
}
```

- [ ] **Step 2: Create .gitignore**

```
config.yaml
assets/example-slides/*
assets/fixed-slides/*
!assets/README.md
```

- [ ] **Step 3: Create config.example.yaml**

```yaml
# Talk Builder — Personal Configuration
# Copy this file to your assets directory as config.yaml
# Run /talk-setup to generate this interactively

assets_path: "~/Documents/talk-builder"   # Path chosen during /talk-setup

style:
  fonts:
    title: "Montserrat Bold"
    body: "Open Sans"
  colors:
    primary: "#1A365D"
    accent: "#E53E3E"
    background: "#FFFFFF"
  language: "en"
  narrative_style: "conversational"
  complexity_default: "moderate"

style_analysis:
  # Generated automatically by /talk-setup when analyzing example slides
  layout: ""
  title_style: ""
  color_usage: ""
  typography: ""
  visual_density: ""
  notes: ""
```

- [ ] **Step 4: Create assets/README.md**

```markdown
# Talk Builder Assets

This directory is for personal assets that are NOT version-controlled.

## Setup

Run `/talk-setup` to configure your personal assets directory.
Your assets will be stored at the path you choose during setup (e.g. `~/Documents/talk-builder/`).

## Structure of your assets directory

```
<your-chosen-path>/
├── config.yaml          # Your personal style config
├── example-slides/      # Your reference presentations (.pptx/.key)
└── fixed-slides/        # Reusable slides: contact, disclosures, etc.
```
```

- [ ] **Step 5: Initialize git repo and commit**

```bash
cd /Users/sebastianpodlipnik/Personal/ClaudeCode/presentations-builder
git init
git add plugin.json .gitignore config.example.yaml assets/README.md
git commit -m "chore: initialize talk-builder plugin scaffolding"
```

---

## Task 2: Reference — Storytelling Guide

**Files:**
- Create: `references/storytelling-guide.md`

This is the core reference document for narrative construction. It must cover all frameworks from the spec with actionable instructions, not just descriptions.

- [ ] **Step 1: Create references/storytelling-guide.md**

Write a comprehensive guide covering these sections in order. All content in English. Each section must include: what it is (2-3 sentences), when to use it, and a concrete example applied to a medical/academic presentation.

**Required sections:**

1. **Macro Narrative Structure**
   - ABT (And, But, Therefore) — Randy Olson
     - The three-part template with fill-in-the-blank format
     - Contrast with AAA (boring lists) and DHY (overly hedged)
     - Example: "Antibiotic resistance is one of the greatest threats to global health, AND we've relied on the same drug classes for decades, BUT novel discovery pipelines have dried up, THEREFORE we turned to AI-driven molecular screening."
   - SCR (Situation, Complication, Resolution) — Barbara Minto
     - Alternative to ABT for framing research problems
     - Example with medical research context

2. **Emotional Rhythm**
   - Sparkline (what is / what could be) — Nancy Duarte
     - How to alternate between current reality and envisioned future
     - Template: "Today, X happens [what is]. Imagine if Y [what could be]..."
     - Must oscillate at least 3-4 times across the talk
   - STAR Moment (Something They'll Always Remember) — Nancy Duarte
     - Place at approximately 2/3 through the talk
     - Types: shocking statistic, live demo, powerful image, personal revelation
     - Medical examples: patient on stage, before/after reveal, audio recording

3. **Structural Constraints**
   - Rule of Three — maximum 3 key messages per talk
   - One Slide One Message — each slide communicates exactly one idea
   - Bookend Heavy — most important content in first 20% and last 20%
   - Attention Reset — plan a reset every 10 minutes (story, question, modality change)

4. **Opening Techniques** (with examples for academic/medical talks)
   - Cold Open / In Medias Res — start in the middle of action
   - Provocative Question — ask something the audience genuinely wants answered
   - Startling Statistic — one carefully chosen, context-rich number
   - Personal Story — brief authentic connection to topic
   - Contrarian Statement — challenge a belief the audience holds

5. **Closing Techniques** (with examples)
   - Callback Close — return to opening story and resolve it
   - Challenge / Call to Action — specific next step for the audience
   - Vision of the Future — paint the world your research enables
   - Patient Quote — end with the human voice
   - NEVER end with: "Any questions?", acknowledgments slide, "That's all I have"

6. **Connectors / Bridges Between Slides** (with examples for each)
   - Narrative Bridge — link conclusion of one section to question opening next
   - Callback Connector — reference something from earlier
   - Rhetorical Question Bridge — end section with question leading to next
   - Contrast Bridge — use "but/however" to pivot with tension
   - Signpost — explicitly tell audience where they are in the structure
   - Physical/Vocal Transitions — pause 2-3 seconds, change position, shift energy

7. **Advanced Patterns**
   - Patient Story Bookend — open with patient case, close by returning to them
   - Nested Loops — open multiple narrative threads, close in reverse order
   - The Vulnerability Move — appropriate admission of uncertainty builds trust
   - Analogy/Metaphor Bridge — make complex concepts accessible
   - SUCCESs test (Chip & Dan Heath) — test each slide: Simple, Unexpected, Concrete, Credible, Emotional, Story

- [ ] **Step 2: Commit**

```bash
git add references/storytelling-guide.md
git commit -m "docs: add storytelling guide reference document"
```

---

## Task 3: Reference — Slide Design Guide

**Files:**
- Create: `references/slide-design-guide.md`

- [ ] **Step 1: Create references/slide-design-guide.md**

Write a comprehensive guide in English covering these sections. Each section must include the principle, why it matters, and a concrete do/don't example.

**Required sections:**

1. **Assertion-Evidence Method** — Michael Alley
   - Replace topic-phrase headlines with full-sentence assertions
   - Support with visual evidence (graph, image, diagram), never bullet points
   - Do: "Patients receiving combination therapy had 40% fewer readmissions at 90 days"
   - Don't: "Patient Outcomes"

2. **One Slide, One Message** — Garr Reynolds / Jean-Luc Doumont
   - Each slide communicates exactly one idea
   - If you say "and this slide also shows..." — split into two slides

3. **The Glance Test**
   - Audience must grasp main point within 3 seconds
   - Show slides to a colleague for 3 seconds — if they can't tell the point, simplify

4. **The Billboard Test**
   - Readable and comprehensible at highway speed
   - Forces radical simplification

5. **Data-Ink Ratio** — Edward Tufte
   - Maximize proportion of ink devoted to data
   - Remove: gridlines, unnecessary borders, 3D effects, decorative elements
   - Never use: 3D bar charts, pie charts with >3 segments

6. **Visual Hierarchy and Contrast** — Nancy Duarte / Slide:ology
   - Direct attention with contrast (color, size, position)
   - Use consistent visual language (same color = same concept throughout)
   - Diagram relationships instead of listing them

7. **Full-Bleed Images** — Garr Reynolds / Presentation Zen
   - High-quality photographs filling entire slide as emotional anchors
   - The slide is not your teleprompter — it's a visual aid

8. **Progressive Disclosure**
   - Build complex diagrams element by element
   - Narrate each addition
   - Never show full complex figure at once

9. **Typography Rules**
   - 30-point minimum font (Guy Kawasaki)
   - Sans-serif for slides
   - Maximum 2 font families per presentation
   - Title font vs body font distinction

10. **Color Usage**
    - Maximum 3-4 colors per presentation
    - Use accent color only for emphasis
    - Ensure sufficient contrast for readability
    - Consider color blindness (avoid red/green as sole differentiator)

- [ ] **Step 2: Commit**

```bash
git add references/slide-design-guide.md
git commit -m "docs: add slide design guide reference document"
```

---

## Task 4: Reference — Data Storytelling Guide

**Files:**
- Create: `references/data-storytelling.md`

- [ ] **Step 1: Create references/data-storytelling.md**

Write a guide in English covering these sections with concrete examples for medical/scientific data:

**Required sections:**

1. **Core Principle** — Cole Nussbaumer Knaflic
   - Data doesn't speak for itself — provide context, highlight what matters, tell the audience what it means
   - The Big Idea worksheet: one sentence with (1) your unique point of view and (2) what's at stake

2. **Choosing the Right Visual**
   - Comparison: bar chart (vertical or horizontal)
   - Trend over time: line chart
   - Part-to-whole: stacked bar or simple pie (max 3 segments)
   - Correlation: scatter plot
   - Distribution: histogram or box plot
   - Survival data: Kaplan-Meier curve (annotated)

3. **Annotating Charts**
   - Never show a raw figure and say "as you can see"
   - Annotate: circle the key point, arrow to the separation, label directly
   - Include a "so what" in the chart title (assertion-evidence)
   - Example: Kaplan-Meier curve with annotation at exact separation point + clinical meaning in title

4. **Humanizing Numbers**
   - Identifiable Victim Effect (Paul Slovic) — one person > statistics
   - Number Needed to Treat (NNT) framing vs relative risk reduction
   - Absolute risk alongside relative risk
   - Icon arrays (pictographs) instead of percentages
   - Hans Rosling technique: animate data, narrate live, challenge assumptions

5. **Removing Chart Junk** — Tufte
   - Remove: gridlines, borders, legends (label directly), background fills
   - Keep: data points, axis labels (minimal), direct labels, annotations
   - Before/after example of cleaning up a chart

6. **Small Multiples**
   - Repeat same chart structure across conditions for comparison
   - More effective than overlaying multiple series on one chart
   - Each panel should be independently readable

- [ ] **Step 2: Commit**

```bash
git add references/data-storytelling.md
git commit -m "docs: add data storytelling reference document"
```

---

## Task 5: Reference — Pacing Guide

**Files:**
- Create: `references/pacing-guide.md`

- [ ] **Step 1: Create references/pacing-guide.md**

Write a guide in English with concrete templates for each duration. Include slide count, section timing, and structural notes.

**Required sections:**

1. **General Pacing Principles**
   - Attention drops after 10 minutes — plan attention resets
   - Bookend Heavy: most important content in first 20% and last 20%
   - Slow down for: key findings, emotional moments, complex concepts
   - Speed up for: background info, obvious context, energetic passages
   - Pause for: after key point (let it land), before transitions, after rhetorical questions
   - Most common mistake: uniform pacing (same speed, energy, volume throughout)

2. **10-Minute Talk Template**
   ```
   Opening hook:           0:00-0:45    (1 slide)
   Context / Problem:      0:45-2:30    (2-3 slides)
   Key Method (brief):     2:30-4:00    (2 slides)
   Core Results:           4:00-7:30    (3-4 slides)
   Significance:           7:30-9:00    (1-2 slides)
   Close:                  9:00-9:30    (1 slide)
   Buffer:                 9:30-10:00
   Total: 8-10 slides. ONE main finding only.
   ```
   Rules: cut all non-essential methods, no literature review, no limitations slide, rehearse to 9 minutes.

3. **15-Minute Talk Template**
   ```
   Hook + Context:         0:00-2:30    (2-3 slides)
   Problem / Gap:          2:30-4:00    (1-2 slides)
   Methods (selective):    4:00-6:30    (2-3 slides)
   Results:                6:30-11:00   (4-5 slides)
   Discussion:             11:00-13:30  (1-2 slides)
   Close:                  13:30-14:30  (1 slide)
   Buffer:                 14:30-15:00
   Total: 12-15 slides. 2-3 key messages. One STAR moment.
   ```

4. **20-Minute Talk Template**
   ```
   Opening story/hook:     0:00-2:30    (2 slides)
   Context + Problem:      2:30-5:00    (2-3 slides)
   Methods:                5:00-8:00    (3 slides)
   Results Section 1:      8:00-11:00   (3-4 slides)
   STAR Moment:            ~13:00       (1 slide)
   Results Section 2:      11:00-15:00  (3-4 slides)
   Implications:           15:00-17:30  (2 slides)
   Close:                  17:30-19:00  (1 slide)
   Buffer:                 19:00-20:00
   Total: 15-20 slides. Attention reset at 10 min mark.
   ```

5. **30-Minute Talk Template**
   ```
   Opening story/hook:     0:00-3:00    (2 slides)
   Roadmap:                3:00-4:00    (1 slide, "Three things today")
   Section 1:              4:00-12:00   (5-6 slides, own mini-arc)
   Transition:             12:00-12:30
   Attention Reset:        ~10:00       (story, question, modality change)
   Section 2:              12:30-20:00  (5-6 slides)
   STAR Moment:            ~20:00       (1 slide)
   Transition:             20:00-20:30
   Section 3:              20:30-25:00  (4-5 slides)
   Synthesis + Close:      25:00-28:00  (2 slides)
   Buffer:                 28:00-30:00
   Total: 20-25 slides. 3 sections, each with own narrative arc.
   Attention resets at ~10 and ~20 minutes.
   ```

6. **Slide Density Guidelines**
   - Minimum time per slide: 45 seconds (less = audience can't process)
   - Average time per slide: 60-90 seconds
   - Data-heavy slide: 90-120 seconds
   - Emotional/image slide: 30-45 seconds
   - Title/transition slide: 10-15 seconds

- [ ] **Step 2: Commit**

```bash
git add references/pacing-guide.md
git commit -m "docs: add pacing guide reference document"
```

---

## Task 6: Skill — talk-setup

**Files:**
- Create: `skills/talk-setup/SKILL.md`

- [ ] **Step 1: Create skills/talk-setup/SKILL.md**

```markdown
---
name: talk-setup
description: Use when setting up Talk Builder for the first time or reconfiguring personal style preferences. Triggers on first /talk invocation if no config exists, or when user says "configure talk builder", "setup talk builder", "change my presentation style".
---

# Talk Builder — Initial Setup

Guide the user through configuring their personal Talk Builder environment. This runs once and creates persistent configuration that all other talk-builder skills reference.

## Important

This skill creates the user's personal assets directory and config file. It MUST ask the user for their preferred path — never assume a default.

## Steps

### 1. Ask for assets directory path

Ask the user where they want to store their personal Talk Builder assets (config, example slides, fixed slides). Suggest examples like `~/Documents/talk-builder/` or `~/talks-config/` but let them choose any path.

### 2. Create directory structure

Create the chosen directory with subdirectories:
```
<chosen-path>/
├── config.yaml
├── example-slides/
└── fixed-slides/
```

### 3. Collect style preferences (one question at a time)

Ask these questions sequentially, one per message:

1. "What is your default presentation language?" (en/es/other)
2. "What font do you use for slide titles?" (e.g., Montserrat Bold, Arial Black)
3. "What font do you use for body text?" (e.g., Open Sans, Calibri)
4. "What is your primary color? (hex code, e.g., #1A365D)"
5. "What is your accent color? (hex code, e.g., #E53E3E)"
6. "What is your default complexity level?" (basic / moderate / advanced)

### 4. Ask about example slides

"Do you have existing presentations that represent your style? If so, place your .pptx or .key files in: `<chosen-path>/example-slides/`"

If the user confirms they have placed files there, read and analyze them to generate the `style_analysis` section of the config:
- `layout`: overall layout approach (e.g., "minimal, full-bleed images, one message per slide")
- `title_style`: how titles are written (e.g., "assertion-evidence, sentence case")
- `color_usage`: how colors are applied (e.g., "dark backgrounds, high contrast accent")
- `typography`: font patterns observed (e.g., "sans-serif, large titles, minimal body text")
- `visual_density`: content density (e.g., "low — lots of whitespace")
- `notes`: any other style patterns (e.g., "uses clinical photos, avoids clip art")

### 5. Ask about fixed slides

"Do you have slides you reuse in every presentation (contact info, disclosures, acknowledgments)? If so, place them in: `<chosen-path>/fixed-slides/`"

### 6. Check dependencies

Verify `poppler-utils` is installed by running:
```bash
which pdfimages && which pdftoppm
```

If not found, tell the user:
"Talk Builder needs poppler-utils for extracting images from PDFs. Install with: `brew install poppler`"

### 7. Generate config.yaml

Write the config file at `<chosen-path>/config.yaml` with all collected information:

```yaml
assets_path: "<chosen-path>"

style:
  fonts:
    title: "<user-answer>"
    body: "<user-answer>"
  colors:
    primary: "<user-answer>"
    accent: "<user-answer>"
    background: "#FFFFFF"
  language: "<user-answer>"
  narrative_style: "conversational"
  complexity_default: "<user-answer>"

style_analysis:
  layout: "<analyzed or empty>"
  title_style: "<analyzed or empty>"
  color_usage: "<analyzed or empty>"
  typography: "<analyzed or empty>"
  visual_density: "<analyzed or empty>"
  notes: "<analyzed or empty>"
```

### 8. Confirm completion

Show the user a summary of their configuration and confirm everything is set up correctly.

## Reconfiguration

If the user already has a config and runs `/talk-setup` again, read the existing config first and ask which sections they want to update. Do not overwrite unchanged sections.
```

- [ ] **Step 2: Commit**

```bash
git add skills/talk-setup/SKILL.md
git commit -m "feat: add talk-setup skill for initial configuration"
```

---

## Task 7: Skill — talk (Orchestrator)

**Files:**
- Create: `skills/talk/SKILL.md`

- [ ] **Step 1: Create skills/talk/SKILL.md**

```markdown
---
name: talk
description: Use when building academic or medical presentations. Main entry point for Talk Builder — orchestrates the full workflow from briefing to final outputs. Triggers when user says "create a presentation", "build a talk", "prepare slides", "presentation about", or invokes /talk.
---

# Talk Builder — Orchestrator

Single entry point for the Talk Builder workflow. Detects the current project state and guides the user through the next phase.

## Important

Always read the user's `config.yaml` first. If it does not exist, redirect to `/talk-setup` before anything else.

The config location is stored at a user-chosen path. Check for a `.talk-builder-config-path` file in `~/.claude/` that stores the assets path. If neither exists, ask the user for the path or redirect to `/talk-setup`.

## Phase Detection

Scan the current working directory for these files to determine project state:

| File | Phase Completed |
|---|---|
| `talk.yaml` | Briefing |
| `vision.md` | Vision |
| `research.md` | Research |
| `images/` (non-empty) | Assets |
| `narrative.md` | Narrative |
| `presentation.pptx` | Slides |
| `study-document.docx` + `article-summaries.docx` | Study Docs |
| `speaker-script.docx` | Script |

## Behavior

### 1. Show project status

Display a visual checklist of all phases:

```
Talk Builder — Project Status:

  [done] Briefing (talk.yaml)
  [done] Vision (vision.md)
  [done] Research (research.md)
  [open] Assets (images/)
  [open] Narrative (narrative.md)
  [open] Slides (presentation.pptx)
  [open] Study Documents
  [open] Speaker Script

  -> Next step: Assets
  Continue, or jump to another phase?
```

Use checkmarks and clear indicators for completed vs pending phases.

### 2. Propose next phase

Suggest the next uncompleted phase. The user can:
- Continue with the suggested phase
- Jump to any other phase
- Redo a completed phase

### 3. Invoke the corresponding skill

Based on the user's choice, invoke the appropriate skill:
- No config → `talk-setup`
- No `talk.yaml` → `talk-briefing`
- No `vision.md` → `talk-vision`
- No `research.md` → `talk-research`
- No images → `talk-assets`
- No `narrative.md` → `talk-narrative`
- No `presentation.pptx` → `talk-slides`
- No study docs → `talk-study-doc`
- No script → `talk-script`

### 4. Handle empty directory

If the working directory is empty (new project), start from `talk-briefing` and create the `pdfs/` and `images/` subdirectories.

## Config Path Resolution

On first run after setup, the `/talk-setup` skill saves the config path. The orchestrator needs to find it. Strategy:

1. Check `~/.claude/talk-builder-config-path` (a single-line file with the path)
2. If not found, ask the user: "Where is your Talk Builder config? (run /talk-setup if you haven't set it up yet)"
```

- [ ] **Step 2: Commit**

```bash
git add skills/talk/SKILL.md
git commit -m "feat: add talk orchestrator skill"
```

---

## Task 8: Skill — talk-briefing

**Files:**
- Create: `skills/talk-briefing/SKILL.md`

- [ ] **Step 1: Create skills/talk-briefing/SKILL.md**

```markdown
---
name: talk-briefing
description: Use when starting a new presentation project. Interactive wizard that collects topic, duration, audience, and preferences. Triggers on "new talk", "new presentation", or when /talk detects no talk.yaml exists.
---

# Talk Builder — Briefing Wizard

Interactive wizard that collects all essential information about a new presentation. Asks questions one at a time and generates `talk.yaml`.

## Important

Ask ONE question per message. Use multiple choice when possible. Do not overwhelm the user with multiple questions at once.

## Questions (sequential, one per message)

### 1. Topic
"What is the topic of your talk?"
(Open-ended)

### 2. Duration
"How long is your time slot?"
- a) 10 minutes
- b) 15 minutes
- c) 20 minutes
- d) 30 minutes
- e) Other (specify)

### 3. Audience
"Who is your audience?"
- a) Specialists in the field
- b) General practitioners / non-specialists
- c) International congress (mixed expertise)
- d) Internal training / department meeting
- e) Mixed / other (specify)

### 4. Language
"What language will you present in?"
- a) English
- b) Spanish
- c) Other (specify)

(Default from config if set)

### 5. Complexity
"What level of scientific complexity?"
- a) Basic — fundamentals, minimal jargon
- b) Moderate — some technical depth, common terminology
- c) Advanced — cutting-edge, specialist vocabulary

(Default from config if set)

### 6. Existing materials
"Do you have papers or specific bibliography to include?"
- a) Yes — I'll put PDFs in the `pdfs/` folder
- b) No, not yet
- c) I have some, will add more later

If yes or partially: create `pdfs/` directory and tell the user to place files there.

### 7. Literature search
"Do you want to search for literature using PubMed and Consensus?"
- a) Yes, search automatically based on topic
- b) No, I'll provide everything myself
- c) Yes, but I want to review results before including

### 8. New or existing
"Is this a new talk or improving an existing one?"
- a) New talk from scratch
- b) Improving an existing presentation

If improving: ask the user to place their existing .pptx/.key in the working directory. Read and analyze it as baseline.

### 9. Fixed slides
"Which standard slides do you want to include?"
- a) Disclosures / Conflicts of interest
- b) Contact information
- c) Acknowledgments
- d) All of the above
- e) None
- f) Custom selection

Check `fixed-slides/` in the user's assets directory to see what's available.

## Output

Generate `talk.yaml` in the current working directory:

```yaml
topic: "<user answer>"
duration_minutes: <number>
audience: "<type>"
language: "<code>"
complexity: "<level>"
has_existing_pdfs: <true/false>
literature_search: "<yes/no/review>"
is_new: <true/false>
fixed_slides:
  disclosures: <true/false>
  contact: <true/false>
  acknowledgments: <true/false>
created: "<ISO date>"
```

Also create `pdfs/` and `images/` directories if they don't exist.

## After completion

Tell the user: "Briefing complete! Next phase: Vision — defining your personal angle and message. Continue with /talk or /talk-vision."
```

- [ ] **Step 2: Commit**

```bash
git add skills/talk-briefing/SKILL.md
git commit -m "feat: add talk-briefing skill for wizard phase"
```

---

## Task 9: Skill — talk-vision

**Files:**
- Create: `skills/talk-vision/SKILL.md`

- [ ] **Step 1: Create skills/talk-vision/SKILL.md**

```markdown
---
name: talk-vision
description: Use when defining the personal angle, message, and emotional intent for a presentation. Interactive conversation to capture the speaker's vision. Triggers when /talk detects talk.yaml exists but no vision.md.
---

# Talk Builder — Vision & Personal Angle

Interactive conversation to capture the speaker's personal vision for the presentation. This is NOT about content — it's about intent, emotion, and differentiation.

## Important

This phase is conversational and open-ended. Ask one question at a time. Listen actively and probe deeper when the user shares something interesting. The goal is to uncover what makes THIS talk unique — not just another review of the topic.

Read `talk.yaml` first to understand the topic, audience, and duration.

## Questions (one at a time, conversational)

### 1. Core message
"If the audience remembers only ONE thing from your talk, what should it be?"

Probe deeper if the answer is too generic: "That's a good start, but every talk on this topic could say that. What is YOUR unique angle?"

### 2. Approach / angle
"What angle do you want to take?"
- Clinical focus — practical, applicable tomorrow
- Research-driven — new data, cutting edge
- Provocative — challenge conventional thinking
- Inspirational — motivate change
- Educational — build understanding step by step
- Other

### 3. Story thread
"Is there a personal story, patient case, or anecdote you want to use as the narrative thread?"

If yes: ask for details. This will become the backbone of the presentation (Patient Story Bookend or Nested Loop pattern).

If no: suggest options based on the topic — "Sometimes a compelling case from the literature can serve the same purpose. We can find one during the research phase."

### 4. Emotional intent
"What emotions do you want to generate in the audience?"
- Curiosity — "I need to learn more about this"
- Urgency — "We need to act now"
- Hope — "This can get better"
- Surprise — "I didn't expect that"
- Empathy — "I feel connected to this"
- Confidence — "I can do this"
- Other (specify)

### 5. Specific ideas
"Do you already have ideas for specific slides, moments, or visuals you want to include?"

Capture everything — even rough ideas. These become seeds for the narrative phase.

### 6. Anti-goals
"What do you NOT want this talk to be?"

Examples: "Not another guidelines review", "Not death by bullet points", "Not purely academic with no clinical relevance"

### 7. Differentiation
"What will make your talk different from every other talk on this topic?"

This is the most important question. Push the user to be specific.

## Output

Generate `vision.md` in the current working directory. Structure:

```markdown
# Vision — [Talk Topic]

## Core Message
[The one thing the audience must remember]

## Angle
[The approach/perspective]

## Story Thread
[The narrative backbone — patient case, personal story, or research journey]

## Emotional Arc
[What emotions to generate and when]

## Specific Ideas
[Any slides, moments, visuals the speaker already envisions]

## Anti-Goals
[What this talk must NOT be]

## Differentiation
[What makes this talk unique]
```

## After completion

Tell the user: "Vision captured! Next phase: Research — finding the evidence to support your narrative. Continue with /talk or /talk-research."
```

- [ ] **Step 2: Commit**

```bash
git add skills/talk-vision/SKILL.md
git commit -m "feat: add talk-vision skill for personal angle definition"
```

---

## Task 10: Skill — talk-research

**Files:**
- Create: `skills/talk-research/SKILL.md`

- [ ] **Step 1: Create skills/talk-research/SKILL.md**

```markdown
---
name: talk-research
description: Use when researching evidence for a presentation. Iterative phase that searches PubMed, Consensus, reads PDFs, and builds a consolidated research document. Triggers when /talk detects vision.md exists but no research.md.
---

# Talk Builder — Research Phase

Iterative research phase that builds a comprehensive evidence base for the presentation. Uses PubMed, Consensus, and user-provided PDFs.

## Important

- This phase is iterative — it loops until the user is satisfied.
- The user can add PDFs to `pdfs/` at ANY point during this phase.
- Every claim in `research.md` MUST have a verifiable reference (DOI or PMID).
- NEVER invent or fabricate references. If you cannot find a source, say so.

Read `talk.yaml` and `vision.md` before starting to understand topic, angle, and intent.

## Workflow

### Step 1: Initial search

Based on the topic and vision, construct search queries for PubMed and Consensus.

Use the MCP tools:
- `mcp__claude_ai_PubMed__search_articles` for PubMed searches
- `mcp__claude_ai_Consensus__search` for Consensus searches

Search strategy:
- Start broad with the main topic
- Then narrow based on the vision angle
- Look for: key reviews, landmark studies, recent advances, relevant clinical data

### Step 2: Present results interactively

Show the user what you found in a structured list:
```
Found 15 relevant articles. Here are the top results:

1. [Title] — Author et al., Journal (Year)
   Key finding: [one sentence]
   Relevance: [why it matters for this talk]

2. [Title] — Author et al., Journal (Year)
   ...
```

Ask: "Which of these do you want to include? Any specific angles to explore further?"

### Step 3: Read user PDFs

Check `pdfs/` for any files. If present:
- Read each PDF
- Extract key findings, methodology, conclusions
- Integrate into the research base

Tell the user: "I've read [N] PDFs from your pdfs/ folder. Here's what I found relevant..."

### Step 4: Consolidate research.md

Write `research.md` with this structure:

```markdown
# Research — [Talk Topic]

## Key Findings

### [Finding Category 1]
- [Finding with source] (Author et al., Year; DOI: xxx)
- [Finding with source] ...

### [Finding Category 2]
- ...

## Key Statistics
- [Statistic] (Source)
- ...

## Potential STAR Moment Data
- [Surprising or impactful data points that could serve as STAR moments]

## Gaps Identified
- [Areas where more evidence is needed]

## References
1. Author et al. "Title." Journal, Year. DOI: xxx / PMID: xxx
2. ...
```

### Step 5: Review together

Present the consolidated research to the user. Ask:
- "Are there gaps you'd like to fill?"
- "Any specific aspect you want to dig deeper into?"
- "Should we search for more papers on [identified gap]?"

### Step 6: Iterate

If the user wants more:
- Run additional searches
- Read new PDFs they add to `pdfs/`
- Update `research.md`

Continue until the user confirms: "The research base is solid."

### Step 7: Reference verification

Before finalizing, verify:
- Every claim has a source
- DOIs/PMIDs are present for all references
- No fabricated citations
- Key statistics are accurately transcribed from sources

## After completion

Tell the user: "Research complete! Next phase: Assets — extracting and preparing visual materials. Continue with /talk or /talk-assets."
```

- [ ] **Step 2: Commit**

```bash
git add skills/talk-research/SKILL.md
git commit -m "feat: add talk-research skill for iterative research phase"
```

---

## Task 11: Skill — talk-assets

**Files:**
- Create: `skills/talk-assets/SKILL.md`

- [ ] **Step 1: Create skills/talk-assets/SKILL.md**

```markdown
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
pdftk <paper.pdf> cat <page-number> output images/<name>-page.pdf
```
Or with poppler:
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
```

- [ ] **Step 2: Commit**

```bash
git add skills/talk-assets/SKILL.md
git commit -m "feat: add talk-assets skill for visual asset extraction"
```

---

## Task 12: Skill — talk-narrative

**Files:**
- Create: `skills/talk-narrative/SKILL.md`

- [ ] **Step 1: Create skills/talk-narrative/SKILL.md**

```markdown
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

### Step 6: Apply quality checks

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

### Step 7: Present and iterate

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

Tell the user: "Narrative approved! Next phase: Slides — generating the PPTX. Continue with /talk or /talk-slides. Remember: you'll fine-tune in Keynote after generation."
```

- [ ] **Step 2: Commit**

```bash
git add skills/talk-narrative/SKILL.md
git commit -m "feat: add talk-narrative skill for storytelling structure"
```

---

## Task 13: Skill — talk-slides

**Files:**
- Create: `skills/talk-slides/SKILL.md`

- [ ] **Step 1: Create skills/talk-slides/SKILL.md**

```markdown
---
name: talk-slides
description: Use when generating the PPTX presentation file from an approved narrative structure. Applies the user's personal style and design principles. Triggers when /talk detects narrative.md exists but no presentation.pptx.
---

# Talk Builder — PPTX Generation

Generate the presentation file from the approved narrative structure, applying the user's personal style configuration and slide design principles.

## Important

- Read `references/slide-design-guide.md` before generating
- Read the user's `config.yaml` for fonts, colors, and style analysis
- Read `talk.yaml` for any local style overrides
- Read `narrative.md` for the complete slide structure
- Check `images/` for available visual assets
- Check the user's `fixed-slides/` directory for reusable slides

The PPTX is a FIRST DRAFT. The user will fine-tune in Keynote. Focus on:
- Correct structure and content placement
- Proper fonts and colors from config
- Image insertion where available
- Clean, minimal design following slide-design-guide principles

## Workflow

### Step 1: Load configuration

1. Read `config.yaml` from the user's assets path
2. Read `talk.yaml` for local overrides
3. Merge: talk.yaml overrides config.yaml for any shared fields
4. Note the style_analysis for design decisions

### Step 2: Generate PPTX

Create `presentation.pptx` following `narrative.md` slide by slide:

For each slide:
- Apply assertion-evidence title format
- Use configured fonts (title font for headers, body font for content)
- Use configured colors (primary, accent, background)
- Insert images from `images/` where referenced in narrative
- Follow one-slide-one-message principle
- Apply slide-design-guide principles (glance test, minimal text, visual evidence)

### Step 3: Insert fixed slides

If `talk.yaml` specifies fixed slides (disclosures, contact, acknowledgments):
- Read corresponding files from the user's `fixed-slides/` directory
- Insert at appropriate positions (disclosures near start, contact at end)

### Step 4: Present for review

Tell the user:
"PPTX generated at `presentation.pptx`. This is a first draft — open it in Keynote to:
- Adjust image positions and sizes
- Fine-tune layouts
- Replace any placeholder images
- Check the `images/image-map.md` for reference on which images go where"

## After completion

Tell the user: "Slides generated! Open in Keynote for visual fine-tuning. When ready, continue with /talk or /talk-study-doc for the study documents."
```

- [ ] **Step 2: Commit**

```bash
git add skills/talk-slides/SKILL.md
git commit -m "feat: add talk-slides skill for PPTX generation"
```

---

## Task 14: Skill — talk-study-doc

**Files:**
- Create: `skills/talk-study-doc/SKILL.md`

- [ ] **Step 1: Create skills/talk-study-doc/SKILL.md**

```markdown
---
name: talk-study-doc
description: Use when generating study documents for a presentation — an exhaustive study document and per-article summaries. Triggers when /talk detects presentation.pptx exists but no study-document.docx.
---

# Talk Builder — Study Documents

Generate two DOCX documents for the speaker to study and review the topic in depth.

## Important

- Read `research.md` for all evidence and references
- Read `narrative.md` for the presentation structure
- Read `talk.yaml` for language preference
- ALL content must be in the language specified in config/talk.yaml
- Every claim must include its reference — do not invent citations

## Output 1: study-document.docx

An exhaustive document covering the topic in depth. Structure:

### Document Structure

1. **Title page** — Talk topic, date, speaker name (from config if available)

2. **Executive Summary** — 500-word overview of the entire topic

3. **Sections matching the talk structure** — For each major section of the narrative:
   - Deep explanation of the topic (beyond what's in the slides)
   - All relevant data with full context
   - Background information the speaker should know
   - Potential Q&A questions and answers
   - Key references for that section

4. **Extended Q&A Preparation** — Anticipated questions with detailed answers, organized by difficulty:
   - Basic questions (from non-specialists)
   - Technical questions (from experts)
   - Challenging questions (controversial aspects)

5. **Complete Reference List** — All references in a consistent format with DOI/PMID

### Writing Style
- Comprehensive but readable
- Include context that helps the speaker understand WHY, not just WHAT
- Highlight controversial areas or areas of active debate
- Note where evidence is strong vs. weak

## Output 2: article-summaries.docx

A document with a 200-300 word summary for each paper used in the presentation.

### Per-Article Structure

For each paper:

```
## [Author et al. — "Title" (Year)]
**Journal:** [Name], [Volume], [Pages]
**DOI:** [doi] / **PMID:** [pmid]

**Summary:** [200-300 words covering:]
- Study objective and design
- Key methodology
- Main findings (with numbers)
- Clinical significance
- Relevance to this presentation

**Key quote:** "[Most relevant sentence from the paper]"

**Relevance to your talk:** [How this paper supports your narrative]
```

## After completion

Tell the user: "Study documents generated! Review them to prepare for your presentation. Next phase: Speaker Script — your slide-by-slide delivery guide. Continue with /talk or /talk-script."
```

- [ ] **Step 2: Commit**

```bash
git add skills/talk-study-doc/SKILL.md
git commit -m "feat: add talk-study-doc skill for study document generation"
```

---

## Task 15: Skill — talk-script

**Files:**
- Create: `skills/talk-script/SKILL.md`
- Create: `skills/talk-script/references/teleprompter-format.md`

- [ ] **Step 1: Create skills/talk-script/references/teleprompter-format.md**

```markdown
# Teleprompter Format Reference

## Principles

The teleprompter section is formatted for reading on-screen during live delivery. It must be immediately readable at a glance — no cognitive effort needed to parse the text.

## Formatting Rules

### Line Length
- Maximum 5-7 words per line
- Break at natural speech pauses
- Never break in the middle of a phrase

### Pauses
- Mark with `[PAUSE]` on its own line
- Use after: key points, rhetorical questions, emotional moments, slide transitions
- Use `[LONG PAUSE]` for dramatic effect (3+ seconds)

### Emphasis
- CAPITALIZE key words for vocal emphasis (1-2 per paragraph maximum)
- Do not capitalize entire sentences — only the word(s) to stress

### Slide Transitions
- Mark with `--- SLIDE [N]: [Title] ---` on its own line
- Add `[ADVANCE SLIDE]` where the speaker should click

### Timing Markers
- Add `[TIME: X:XX]` at section starts
- Helps speaker track pacing during delivery

### Breathing
- Line breaks naturally create breathing points
- Extra blank lines indicate longer pauses

## Example

```
--- SLIDE 3: Cancer mortality dropped 40% in treated patients ---

[TIME: 2:30]

Let me show you
what happened next.

[PAUSE]

When we analyzed
the SURVIVAL data,
something REMARKABLE emerged.

[ADVANCE SLIDE]

--- SLIDE 4: The unexpected finding changed our protocol ---

Patients who received
the combination therapy
lived SIGNIFICANTLY longer.

[PAUSE]

Not just weeks.

Not just months.

YEARS.

[LONG PAUSE]

And that changed everything.
```

## Connector Formatting

When transitioning between slides, the connector (Bridge) should feel natural:

```
[Bridge to next slide]
So we knew the treatment worked.
But would it work
in the REAL world?

[ADVANCE SLIDE]
```

## Do NOT

- Do not write full paragraphs
- Do not use complex sentence structures
- Do not include parenthetical asides
- Do not use abbreviations the speaker might stumble on
- Do not use em dashes — break into separate lines instead
```

- [ ] **Step 2: Create skills/talk-script/SKILL.md**

```markdown
---
name: talk-script
description: Use when generating the speaker script for a presentation — slide-by-slide delivery guide with preparation table and teleprompter format. Triggers when /talk detects study documents exist but no speaker-script.docx.
---

# Talk Builder — Speaker Script

Generate a comprehensive speaker script with two sections: a preparation table and a teleprompter-formatted delivery script.

## Important

- Read `references/teleprompter-format.md` in this skill's directory for formatting rules
- Read `narrative.md` for slide structure, content, and connectors
- Read `vision.md` for emotional intent
- Read `talk.yaml` for language preference
- Write in the language specified in config/talk.yaml
- Use conversational, natural language — short sentences, no jargon unless necessary
- The script must feel like natural speech, not written text

## Output: speaker-script.docx

### Section 1: Preparation Table

A table with one row per slide:

| Slide | Title | What to Say | Bridge to Next | Timing |
|---|---|---|---|---|
| 1 | [Title] | [Natural prose — what to communicate, key phrases to use, emotional tone] | [The connector sentence/question leading to the next slide] | [seconds] |
| 2 | [Title] | ... | ... | ... |

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

Tell the user: "Speaker script generated! Your Talk Builder project is complete. All outputs:
- presentation.pptx — open in Keynote for visual fine-tuning
- study-document.docx — deep review of the topic
- article-summaries.docx — quick reference for each paper
- speaker-script.docx — your delivery guide with teleprompter

Run /talk to see the full project status."
```

- [ ] **Step 3: Commit**

```bash
git add skills/talk-script/SKILL.md skills/talk-script/references/teleprompter-format.md
git commit -m "feat: add talk-script skill with teleprompter format reference"
```

---

## Task 16: Config Path Resolution

**Files:**
- Modify: `skills/talk-setup/SKILL.md`
- Modify: `skills/talk/SKILL.md`

- [ ] **Step 1: Add config path persistence to talk-setup**

Add the following to the end of Step 7 in `skills/talk-setup/SKILL.md`, after generating `config.yaml`:

```markdown
### 8. Save config path for discovery

Write the chosen assets path to `~/.claude/talk-builder-config-path` so the orchestrator can find it:

```bash
echo "<chosen-path>" > ~/.claude/talk-builder-config-path
```

This single-line file is how `/talk` locates the user's config without asking every time.
```

Renumber the existing Step 8 ("Confirm completion") to Step 9.

- [ ] **Step 2: Commit**

```bash
git add skills/talk-setup/SKILL.md skills/talk/SKILL.md
git commit -m "feat: add config path persistence between setup and orchestrator"
```

---

## Task 17: Final Review & Integration Test

- [ ] **Step 1: Verify all files exist**

```bash
ls -la plugin.json .gitignore config.example.yaml
ls -la assets/README.md
ls -la references/storytelling-guide.md references/slide-design-guide.md references/data-storytelling.md references/pacing-guide.md
ls -la skills/talk/SKILL.md skills/talk-setup/SKILL.md skills/talk-briefing/SKILL.md skills/talk-vision/SKILL.md skills/talk-research/SKILL.md skills/talk-assets/SKILL.md skills/talk-narrative/SKILL.md skills/talk-slides/SKILL.md skills/talk-study-doc/SKILL.md skills/talk-script/SKILL.md
ls -la skills/talk-script/references/teleprompter-format.md
```

All files must exist.

- [ ] **Step 2: Verify all SKILL.md files have valid frontmatter**

For each SKILL.md, check that:
- Frontmatter starts with `---` on line 1
- Contains `name:` field in kebab-case
- Contains `description:` field under 1024 characters
- Description includes triggering conditions (not workflow summary)
- Frontmatter closes with `---`
- No XML angle brackets (`<` or `>`) in frontmatter

```bash
for f in skills/*/SKILL.md; do
  echo "=== $f ==="
  head -5 "$f"
  echo ""
done
```

- [ ] **Step 3: Verify plugin.json is valid JSON**

```bash
python3 -c "import json; json.load(open('plugin.json'))"
```

- [ ] **Step 4: Verify .gitignore excludes personal files**

```bash
cat .gitignore
```

Must contain: `config.yaml`, `assets/example-slides/*`, `assets/fixed-slides/*`, `!assets/README.md`

- [ ] **Step 5: Final commit**

```bash
git add -A
git status
git commit -m "chore: complete talk-builder plugin v0.1.0"
```
