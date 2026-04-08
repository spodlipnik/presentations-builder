---
name: talk-vision
description: Use when defining the personal angle, message, and emotional intent for a presentation. Interactive conversation to capture the speaker's vision. Triggers when /talk detects docs/talk.yaml exists but no docs/vision.md.
allowed-tools:
  - Read
  - Write
---

# Talk Builder — Vision & Personal Angle

This is the most important phase of Talk Builder. Every great talk starts with a clear personal vision — not a list of slides, but a sense of *why this talk matters* and *what makes it yours*. This phase captures that through a brief creative conversation.

This is NOT about content or evidence (that comes in the research phase). It's about intent, emotion, and what makes the speaker's perspective unique.

## Important

- Read `docs/talk.yaml` to understand the topic, audience, and duration.
- Read `${user_config.assets_path}/config.yaml` for the user's default language preference.
- **Language priority:** Use the language the user writes in (primary signal). Only fall back to config.language if the user's message is ambiguous or very short (e.g., "/talk-vision"). Never override the user's own language with the config setting.
- Ask one question at a time. Be conversational — react to what the user says, don't just move to the next question mechanically.
- When the user gives a generic answer, gently push for specificity. The difference between a forgettable talk and a memorable one is in the specifics.
- Adapt your examples to the user's topic. If they're talking about melanoma, don't give examples about cardiology.

## The Conversation (one question at a time)

### 1. Core message — the anchor

"If your audience remembers only ONE thing a week after your talk, what should that be?"

This is the hardest question and the most important. Most speakers answer with something too broad ("AI is useful in dermatology"). Your job is to help them sharpen it into something specific and memorable.

If the answer is generic, probe: "That's true, but any talk on this topic could say that. What's YOUR take? What have you seen or experienced that gives you a different perspective?"

Keep probing until you get something specific and personal. This might take 2-3 exchanges — that's fine.

### 2. Angle — how you'll approach it

"There are many ways to talk about [topic]. Which feels most like you?"
- **Clinical** — "here's what you can use tomorrow in your practice"
- **Research-driven** — "here's what the new data is telling us"
- **Provocative** — "here's why what we've been doing is wrong"
- **Inspirational** — "here's what's possible and why it matters"
- **Educational** — "let me build your understanding step by step"

Contextualize the options with the user's topic. For example, if the topic is AI in dermoscopy: "Clinical would mean showing how to integrate AI tools into your clinic workflow. Provocative might challenge the assumption that dermatologists don't need AI assistance."

### 3. Story thread — the emotional backbone

Every memorable talk has a narrative thread — something human that connects the data to meaning. This is what separates a presentation from a lecture.

"Is there a story you want to weave through the talk? It could be:"
- A patient case that changed how you think about this
- A personal moment of realization or failure
- A journey of discovery (yours or someone else's)
- A before/after transformation

If the user has a story, ask for details — who, what happened, why it matters to them.

If they don't have one: "That's okay — sometimes the research itself tells a compelling story. We can look for one during the research phase. But think about it — the best talks almost always have a human moment."

### 4. Emotional intent — what the audience should feel

This question can feel unusual to academics, so frame it concretely:

"Think about the moment right after your talk ends, before the questions start. What's the feeling in the room?"
- **Curiosity** — they're pulling out their phones to look up what you mentioned
- **Urgency** — they feel they need to change something in their practice
- **Hope** — they see a better future for their patients
- **Surprise** — something you showed them challenged their assumptions
- **Confidence** — they feel equipped to do something they couldn't before

The user can pick one primary emotion and optionally a secondary one.

### 5. The edges — ideas, boundaries, and what makes it yours

Combine the remaining questions into one open exploration. This prevents survey fatigue while capturing important nuance:

"A few final things to shape the vision:"

a) "Do you already have specific ideas for the talk? Slides you've imagined, a moment you want to create, a visual that's in your head?"

b) "What should this talk absolutely NOT be?" (Examples from their context: "not another guidelines review", "not a sales pitch for an AI product", "not boring statistics without clinical meaning")

c) "What will make YOUR talk different from every other talk on [topic]?" Push for specificity — this is where the talk's identity crystallizes.

These can flow naturally in one conversation turn. The user doesn't have to answer all three if something doesn't resonate.

## Output

Generate `docs/vision.md` in the current working directory. Write it as a cohesive document that captures the spirit of the conversation, not just a form with filled blanks:

```markdown
# Vision — [Talk Topic]

## Core Message
[The one thing the audience must remember — sharp, specific, personal]

## Angle
[The approach/perspective and why it fits this speaker]

## Story Thread
[The narrative backbone — patient case, personal story, or research journey. Include enough detail to build on later. If none yet, note that one will be found during research.]

## Emotional Arc
[Primary emotion to generate and why. How it connects to the core message.]

## Specific Ideas
[Any slides, moments, visuals the speaker already envisions. Skip if none.]

## Anti-Goals
[What this talk must NOT be — specific, based on what the user said]

## Differentiation
[What makes this talk unique — the specific perspective, experience, or insight that no other speaker would bring to this topic]
```

## After completion

Tell the user: "Vision captured! This will guide every decision from here — which papers to include, how to structure the narrative, and what emotional arc to build. Next phase: Research. Continue with /talk or /talk-builder:talk-research."
