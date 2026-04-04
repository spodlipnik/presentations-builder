---
name: talk-study-doc
description: Use when generating study documents for a presentation — a comprehensive reference document and per-article summaries in Markdown. Triggers when /talk detects narrative.md exists but no study-document.md.
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Glob
---

# Talk Builder — Study Documents

Generate two Markdown documents: a comprehensive reference document following the talk structure, and per-article summaries.

## Important

- Read `research.md` for all evidence and references
- Read `narrative.md` for the presentation structure — the study document follows this order
- Read `talk.yaml` for language preference
- ALL content must be in the language specified in config/talk.yaml
- Every claim must include its reference (DOI/PMID) — NEVER invent citations
- Write in **review article style** — continuous prose, NO bullet points
- This document serves as a **permanent reference**: the speaker should be able to re-open it a year later and refresh all knowledge needed to re-present the talk

## Output 1: study-document.md

A comprehensive reference document that follows the talk's narrative structure. The speaker should be able to read this cover-to-cover and fully understand every aspect of the presentation topic.

### Document Structure

```markdown
# [Talk Title]
Date: YYYY-MM-DD | Author: [name from config]

## Executive Summary
[~500 words of narrative prose providing a global vision of the topic — what it is,
why it matters, where the field stands, and what this talk contributes]

## 1. [First section title from narrative.md]

[Continuous prose — review article style. Cover:]
[- Full context of the topic, beyond what appears on slides]
[- All relevant evidence with exact data and inline references (Author et al., Year; DOI)]
[- Why this matters for the audience]
[- Areas of active debate or controversy]
[- Where evidence is strong vs. weak or emerging]
[- Background the speaker should know but won't say on stage]

### Frequently Asked Questions
[Q: [Question a listener might ask about this section]
A: [Developed answer in prose, with references]]

## 2. [Next section from narrative.md]
[Same structure as above]

...

## Extended Q&A Preparation

### Basic Questions (non-specialists)
[Q&A pairs in prose — questions a general audience might ask]

### Technical Questions (experts)
[Q&A pairs — questions from specialists in the field]

### Challenging Questions (controversial topics)
[Q&A pairs — difficult questions about limitations, contradictions, or ethical aspects]

## Complete References
[Full reference list in consistent format with DOI/PMID for every entry]
```

### Writing Style

- Review article prose: paragraphs with transitions, not bullet lists
- Include context that helps the speaker understand WHY, not just WHAT
- Highlight controversial areas and areas of active debate
- Note where evidence is strong vs. weak
- Be comprehensive: the speaker should not need to re-read the original papers to refresh their knowledge
- Write as if for a medical journal review, but accessible to the speaker's level

## Output 2: article-summaries.md

A document with a 200-300 word summary for each paper used in the presentation.

### Per-Article Structure

```markdown
# Article Summaries — [Talk Title]

## [Author et al. — "Title" (Year)]
**Journal:** [Name], [Volume], [Pages]
**DOI:** [doi] | **PMID:** [pmid]

**Summary:** [200-300 words covering study objective and design, key methodology,
main findings with numbers, clinical significance, and relevance to this presentation.
Written as continuous prose, not bullets.]

**Key quote:** "[Most relevant sentence from the paper]"

**Relevance to your talk:** [How this paper supports the narrative — which section
it feeds into and why it matters for the argument]
```

## After completion

Tell the user: "Study documents generated! Review them to prepare for your presentation. Next phase: Speaker Script — your slide-by-slide delivery guide. Continue with /talk or /talk-script."
