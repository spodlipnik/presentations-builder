---
name: talk-script
description: Use when generating a teleprompter-format speaker script for a presentation. Optional — only needed if the speaker wants a line-by-line reading guide. Triggers when user asks for "teleprompter", "speaker script", or "guión".
allowed-tools:
  - Read
  - Write
  - Glob
---

# Talk Builder — Teleprompter Script (Optional)

Generate a teleprompter-format script from the approved narrative. This is an optional convenience tool — `docs/narrative.md` already contains full speaker text. This skill reformats it for on-screen reading during rehearsal or delivery.

## Important

- Read `docs/narrative.md` — extract the Speaker field from every slide
- Read `${user_config.assets_path}/config.yaml` for language
- **Language priority:** Use the language the user writes in. Fall back to config.language.
- This skill does NOT create new content. It reformats what's already in `docs/narrative.md`.
- If `docs/narrative.md` doesn't exist, tell the user to complete the narrative phase first.

## Teleprompter Format Rules

Read `${CLAUDE_SKILL_DIR}/references/teleprompter-format.md` for the complete formatting specification.

Key rules:
- **5-7 words per line** — natural breath breaks
- **[PAUSE]** markers where the speaker should pause
- **[LONG PAUSE]** for dramatic moments
- **KEY** words in CAPS (1-2 per paragraph) for emphasis
- **`--- SLIDE [N]: [Title] ---`** slide markers
- **[ADVANCE SLIDE]** cues before each new slide
- **[TIME: X:XX]** cumulative timing markers at section starts
- **[STAR MOMENT]** marker at the STAR moment
- Short sentences. Natural speech. Not written text read aloud.

## Output: docs/speaker-script.md

```markdown
# Teleprompter — [Talk Title]
Duration: [X] min | Slides: [N]

--- SLIDE 1: [Title] ---
[TIME: 0:00]

[First line of what to say,
five to seven words per line,
natural breathing rhythm.]

[PAUSE]

[Next thought begins here,
KEY word emphasized,
continue the idea.]

[ADVANCE SLIDE]

--- SLIDE 2: [Title] ---
[TIME: 0:15]

[Speaker text reformatted
from docs/narrative.md,
keeping emotional cues.]

[PAUSE]

[Bridge to next slide
as a natural question
or transition.]

[ADVANCE SLIDE]

...

--- SLIDE [N]: [STAR MOMENT] ---
[TIME: X:XX]
[STAR MOMENT]

(slow, deliberate)
[The key revelation,
one short phrase per line,
let it land.]

[LONG PAUSE]

...
```

## Quality Checks

- [ ] Every slide from `docs/narrative.md` has a corresponding section
- [ ] Cumulative timing adds up correctly
- [ ] STAR moment is marked
- [ ] Bridges between slides are included
- [ ] Language matches `docs/narrative.md`
- [ ] No new content invented — only reformatted from narrative

## After completion

Tell the user: "Teleprompter script ready! Use it for rehearsal — practice reading it aloud at speaking pace. Next: slides generation. Continue with /talk or /talk-builder:talk-slides."
