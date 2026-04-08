---
name: talk-study-doc
description: Use when generating the study document for a presentation — a comprehensive reference document for the speaker to study and refresh their knowledge. Triggers when /talk detects docs/narrative.md exists but no docs/study-document.md.
allowed-tools:
  - Read
  - Write
  - Glob
---

# Talk Builder — Study Document

Generate a single comprehensive study document that the speaker can use to master the topic and prepare for any question. This document is designed for long-term use — the speaker should be able to re-open it a year later and refresh everything they need to re-present the talk.

## Important

- Read `docs/narrative.md` for the presentation structure — the study document follows this order
- Read `docs/research.md` for all evidence, paper summaries, and visual elements catalog
- Read `${user_config.assets_path}/config.yaml` for language and speaker info
- Read `docs/talk.yaml` and `docs/vision.md` for topic and intent context
- **Language priority:** Use the language the user writes in. Fall back to config.language for ambiguous messages.
- Every claim must include its reference with DOI/PMID — NEVER invent citations
- Write in **review article style** — continuous narrative prose. No bullet lists except for key data points that must be memorized.
- This is NOT a transcript of the talk. It's deeper — it covers what the speaker needs to KNOW, not just what they'll SAY.

## Design Principles (evidence-based)

This document is designed around three cognitive science principles:

1. **Pyramid structure** — each section starts with the conclusion, then adds evidence. The reader grasps the key point immediately and reads deeper only if needed.
2. **Active recall** — each section ends with self-test questions. Struggling to recall is what builds retention, not passive re-reading.
3. **Modular sections** — each section is self-contained. The speaker can review one section independently (e.g., on the train to the conference) without reading the whole document.

## Output: docs/study-document.md

Target length: **2,500-4,000 words** for a 20-minute talk. Scale proportionally for shorter/longer talks. This is enough to be comprehensive without becoming a textbook.

```markdown
# [Talk Title] — Study Document
Date: YYYY-MM-DD | Speaker: [name] | Duration: [X] min | Audience: [type]

---

## Quick Refresh

[300-500 words maximum. One page. The last thing you read before going on stage.

Structure:
- Core message in one sentence
- The 3 key messages of the talk
- The 5 most important numbers you must know (with sources)
- The STAR moment in one sentence
- The opening and closing in one sentence each

Write as dense, scannable prose — not an essay. This section trades elegance for speed.]

---

## [Section 1: name — corresponds to slides N-M]

> **In brief:** [50-100 word mini-abstract. Conclusion first, then evidence summary. The reader decides if they need to read further or already remember enough.]

[200-400 words of continuous narrative prose. Write like a review article — connect ideas, explain mechanisms, discuss controversies. Each paragraph = one concept. Integrate references naturally: "Gopalakrishnan et al. demonstrated in 112 melanoma patients that gut diversity predicted response to anti-PD-1 (Science 2018; DOI: 10.1126/science.aan4236)."

Include:
- Full context beyond what's on the slides
- The WHY behind the data, not just the WHAT
- How this section connects to the previous and next
- Where evidence is strong vs weak
- What the speaker should know but won't say on stage
- Transition to next section: "Having established that... the natural question becomes..."]

**Key data (know these cold):**
- 66.7% vs 41.9% PASI-75 (Navarro-López 2019; p=0.03)
- Recaídas: 20% vs 42% a 6 meses (p=0.027)
- OR 4.80 para PASI-75 (Li 2024)

**Self-test:**
1. ¿Cuál es el OR para PASI-75 con probióticos?
2. ¿Qué distingue a Probiasor de otros estudios de probióticos en psoriasis?
3. Si te preguntan la limitación principal, ¿qué dices?

[Answers at end of document]

---

## [Section 2: name — slides N-M]

> **In brief:** [...]

[Transition from previous section...]

[Narrative prose...]

**Key data:**
- ...

**Self-test:**
1. ...

---

[...continue for each section of the talk...]

---

## Q&A Preparation

### Basic questions (non-specialists)
**Q:** [Question a general audience member might ask]
**A:** [Answer in conversational prose, with reference. 2-3 sentences. The speaker should be able to say this naturally, not read it.]

### Technical questions (specialists)
**Q:** [Question an expert might ask]
**A:** [More detailed answer with specific data and references.]

### Difficult questions (the ones that scare you)
**Q:** [The hardest question someone could ask — about limitations, contradictions, ethical issues]
**A:** [Honest answer. Acknowledge the limitation. Explain why it doesn't invalidate the message. Cite the specific data. Never bluff.]

## Evidence Weak Points

[Where you are vulnerable. Be explicit:
- "[Study X] is monocentric with N=90 — if challenged, acknowledge but note it's the best available RCT"
- "[The antibiotics-ICI association] may be confounded — Poizeau 2022 (n=2,605) found no effect after adjustment. Present this honestly."
- "[Probiros] has no independent publication — 'data on file' is the weakest evidence in the talk. Be transparent."

For each weak point: what to say if challenged, and what NOT to say.]

## Self-Test Answers

[All answers from the self-test sections, grouped by section number]

### Section 1
1. OR 4.80 (Li 2024)
2. ...
3. ...

### Section 2
...

## Complete References

[Full reference list in consistent format, numbered, with DOI/PMID for every entry. Organized by order of appearance in the document.]

1. Author et al. "Title." Journal, Year;Vol(Issue):Pages. DOI: xxx
2. ...
```

## Writing Style Guide

- **Narrative prose always.** Write as you would for a medical journal review — paragraphs with transitions, context, and interpretation. Not bullet lists, not slide notes.
- **References inline.** "(Gopalakrishnan et al., Science 2018; DOI: xxx)" — so the reader can look up any claim instantly.
- **One paragraph = one concept.** Never mix two ideas in one paragraph.
- **Transitions between sections.** "Having established X, the natural question is Y..." — the document should read cover-to-cover as a coherent narrative, not as disconnected blocks.
- **Bullet lists ONLY for "Key data" sections** — the numbers the speaker must memorize. Everything else is prose.
- **Honest about limitations.** If a study is weak, say so. The speaker's credibility depends on knowing their own weak points.

## After completion

Tell the user: "Study document generated! Use it to prepare — review one section per day starting 4 weeks before the talk, and do the self-tests without looking at the answers. Next phase: Speaker Script. Continue with /talk or /talk-builder:talk-script."
