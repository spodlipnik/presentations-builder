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
