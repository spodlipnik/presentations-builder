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
