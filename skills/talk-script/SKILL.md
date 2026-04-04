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
