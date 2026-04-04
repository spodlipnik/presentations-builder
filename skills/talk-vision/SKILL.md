---
name: talk-vision
description: Use when defining the personal angle, message, and emotional intent for a presentation. Interactive conversation to capture the speaker's vision. Triggers when /talk detects talk.yaml exists but no vision.md.
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
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
