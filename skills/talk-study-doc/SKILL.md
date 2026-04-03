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

## Generation Method

**Requires:** The official `docx` skill from `claude-plugins-official` must be installed.

Use the **docx-js approach** described in the official `docx` skill to create both documents programmatically. Refer to the `docx` skill's `docx-js.md` reference for the full API.

Key generation instructions:
- Install docx if not available: `npm install -g docx`
- Write a Node.js script that creates each document using the docx library
- Use the `docx` skill's guidance for document structure, tables, formatting, and page setup
- After creation, validate with the `docx` skill's validation tools if available

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
