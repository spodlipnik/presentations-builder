---
name: talk-briefing
description: Use when starting a new presentation project. Interactive wizard that collects topic, duration, audience, and preferences. Triggers on "new talk", "new presentation", or when /talk detects no docs/talk.yaml exists.
disable-model-invocation: true
argument-hint: "[topic]"
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
---

# Talk Builder — Briefing Wizard

Interactive wizard that collects essential information about a new presentation and generates `docs/talk.yaml`. This should feel like a quick, focused conversation — not a bureaucratic form.

## Important

- Read `${user_config.assets_path}/config.yaml` first to know the user's defaults (language, complexity).
- Use the user's language (from config or from how they write) for all questions.
- If the user already provided information in their message or in the `/talk` invocation (topic, duration, audience), acknowledge it and skip those questions. Don't re-ask what you already know.
- Ask ONE question per message. Use multiple choice when possible.

## Before asking questions

1. Read config.yaml for defaults
2. Check if there's already a .pptx or .key file in the working directory — if so, this is likely an improvement of an existing talk, not a new one
3. Check what's available in `${user_config.assets_path}/fixed-slides/` — only ask about fixed slides if the folder has files
4. Parse the user's initial message for any info already provided

## Questions (sequential, one per message — skip any already answered)

### 1. Topic
"What is the topic of your talk?"
(Open-ended — skip if already provided)

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
- e) Other (specify)

### 4. Language and complexity (confirm defaults)

If config has defaults for language and complexity, just confirm:
"Your default settings are [language] and [complexity] complexity. Should I use these, or do you want different settings for this talk?"

If no config defaults, ask separately:
- Language: "What language will you present in?" (en/es/other)
- Complexity: "What level of scientific depth?" (basic/moderate/advanced)

### 5. Existing materials and literature search

Combine these into one question to save turns:
"Do you have research papers to include?"
- a) Yes — I'll put PDFs in the `pdfs/` folder, and also search for more
- b) Yes — I'll provide everything, no need to search
- c) No — please search for literature automatically
- d) Not yet — I'll add papers later

### 6. Fixed slides (only if fixed-slides/ has files)

Check `${user_config.assets_path}/fixed-slides/`. If files exist, list what's available:
"I found these standard slides in your collection: [list]. Which do you want to include?"
- a) All of them
- b) None
- c) Let me pick: [show checkboxes]

If the folder is empty or doesn't exist, skip this question entirely.

### 7. Pregunta sobre tema visual

Antes de crear talk.yaml, pregunta:

> "¿Qué tema visual usarás para esta presentación? (Si ya creaste uno con `talk-theme-builder`, usa su ID). Si no tienes ninguno, puedo dejar este campo vacío y créalo después."

Lista los temas disponibles en `${user_config.assets_path}/themes/` si existe. Presenta las opciones.

Guarda la elección en `docs/talk.yaml` bajo el campo `theme:`. Si el usuario no elige, deja el campo vacío (talk-slides pedirá el tema después).

## Output

Generate `docs/talk.yaml` in the current working directory:

```yaml
topic: "<user answer>"
duration_minutes: <number>
audience: "<type>"
language: "<code>"
complexity: "<level>"
has_existing_pdfs: <true/false>
literature_search: "<yes/no/review>"
is_new: <true/false>
theme: ""                      # ID del tema visual (de talk-theme-builder), empty if none yet
fixed_slides:
  disclosures: <true/false>
  contact: <true/false>
  acknowledgments: <true/false>
created: "<ISO date>"
```

Also create `docs/`, `pdfs/`, and `images/` directories if they don't exist.

## After completion

Tell the user: "Briefing complete! Next phase: Vision — defining your personal angle and message. Continue with /talk or /talk-builder:talk-vision."
