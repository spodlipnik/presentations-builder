---
name: talk-research
description: Use when researching evidence for a presentation. Iterative phase that searches PubMed, Consensus, reads PDFs, and builds a consolidated research document. Triggers when /talk detects vision.md exists but no research.md.
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - WebSearch
  - WebFetch
  - mcp__claude_ai_PubMed__search_articles
  - mcp__claude_ai_PubMed__get_article_metadata
  - mcp__claude_ai_PubMed__get_full_text_article
  - mcp__claude_ai_Consensus__search
---

# Talk Builder — Research Phase

Iterative research phase that builds a comprehensive evidence base for the presentation. The goal is not to find every paper on the topic — it's to find the RIGHT papers that support the speaker's vision and narrative.

## Important

- Read `talk.yaml`, `vision.md`, and `${user_config.assets_path}/config.yaml` before starting.
- **Language priority:** Use the language the user writes in. Fall back to config.language for ambiguous messages.
- This phase is iterative — it loops until the user is satisfied.
- The user can add PDFs to `pdfs/` at ANY point during this phase.
- Every claim in `research.md` MUST have a verifiable reference (DOI or PMID).
- NEVER invent or fabricate references. If you cannot find a source, say so explicitly.

## Tool Availability Check

Before starting any search, check if these MCP tools are available:
- `mcp__claude_ai_PubMed__search_articles`
- `mcp__claude_ai_Consensus__search`

If ANY of them is NOT available, STOP and tell the user:

"The following recommended tools are not available in this session:
- [list missing tools]

These tools provide structured medical literature search with verified references (DOI/PMID). Without them, I'll use general web search which produces less precise and less structured results.

To connect them: go to claude.ai > Settings > MCP Servers and activate PubMed and/or Consensus.

Would you like to connect them before we continue, or proceed with web search only?"

Wait for the user's explicit response before proceeding. If they choose to continue without the MCP tools, use WebSearch and WebFetch as fallback for all literature searches. Always inform the user which tools you are using at the start of each search round.

## Workflow

### Step 1: Build search strategy from vision

Read `vision.md` carefully. The vision drives what to search — not the topic alone. Build search queries targeting:

- **Core message support:** Evidence that directly backs the speaker's main thesis
- **Story thread material:** If vision mentions a patient case or narrative, search for published cases or data that support it
- **STAR moment candidates:** Surprising statistics, counterintuitive findings, striking comparisons
- **Counter-arguments:** What the skeptics would cite — knowing this makes the talk stronger
- **Anti-goals filter:** If the speaker said "not a guidelines review", don't fill research.md with guidelines

### Step 2: Propose search queries before executing

Show the user your planned queries before searching:

"Based on your vision, I'm going to search for:
1. [Query 1] — to support [core message aspect]
2. [Query 2] — to find [STAR moment / story data]
3. [Query 3] — to address [counter-argument / gap]

Does this look right, or should I adjust?"

This saves time — the user might redirect you before you burn search tokens on the wrong angle.

### Step 3: Search and present results

Use PubMed and Consensus (or WebSearch as fallback). For each result, show:

```
1. [Title] — Author et al., Journal (Year)
   Key finding: [one sentence]
   Evidence level: [meta-analysis / RCT / cohort / case series / review]
   Relevance to YOUR talk: [how it connects to the vision]

2. [Title] — Author et al., Journal (Year)
   ...
```

Prioritize by evidence quality: meta-analyses and RCTs first, case series and expert opinion last. But a compelling case report that fits the narrative can be more valuable than a weak meta-analysis that doesn't.

Ask: "Which of these do you want to include? Any angles to explore further?"

### Step 4: Read user PDFs

Check `pdfs/` for files. If present:
- Read each PDF
- Extract key findings, methodology, conclusions
- Connect findings to the vision — explain how each paper serves the narrative

Tell the user: "I've read [N] PDFs from your pdfs/ folder. Here's what I found relevant to your vision..."

### Step 5: Consolidate research.md

Write `research.md` organized by narrative role, not by topic taxonomy:

```markdown
# Research — [Talk Topic]

## Evidence Summary

### [Narrative Section 1 — e.g., "The problem: diagnostic gaps"]
- [Finding with source] (Author et al., Year; DOI: xxx)
- [Finding with source] ...
Evidence quality: [meta-analysis / multiple RCTs / emerging]

### [Narrative Section 2 — e.g., "The solution: AI-assisted diagnosis"]
- ...

### [Narrative Section 3 — e.g., "Clinical impact: what changes"]
- ...

## STAR Moment Candidates
- [Surprising or impactful data points that could serve as STAR moments]
- [Include the numbers — specific, visceralized, comparable]

## Counter-Arguments & Limitations
- [What skeptics would say, with sources]
- [Known limitations of the evidence]

## Gaps Identified
- [Areas where more evidence is needed or could strengthen the talk]

## References
1. Author et al. "Title." Journal, Year. DOI: xxx / PMID: xxx
2. ...
```

### Step 6: Calibrate scope

Guide the user on how much evidence is enough:
- **10-min talk:** 3-5 key references are plenty
- **15-min talk:** 5-8 key references
- **20-min talk:** 8-12 key references
- **30-min talk:** 10-15 key references

These are references that directly appear in or support the narrative — not every paper you read. More is not better. Say: "You have [N] references for a [X]-minute talk. That's [sufficient / a bit light / more than enough]. Want to search for more or are we solid?"

### Step 7: Review together

Present the consolidated research. Ask:
- "Does this evidence support your core message?"
- "Are there gaps that weaken your argument?"
- "Any specific aspect you want to dig deeper into?"

### Step 8: Iterate

If the user wants more:
- Run additional targeted searches
- Read new PDFs they add to `pdfs/`
- Update `research.md`

Continue until the user confirms the evidence base is solid.

### Step 9: Reference verification

Before finalizing, verify:
- Every claim has a source with DOI or PMID
- No fabricated citations — if in doubt, flag it
- Key statistics are accurately transcribed from sources
- References section is complete and consistently formatted

## After completion

Tell the user: "Research complete! Next phase: Assets — extracting and preparing visual materials. Continue with /talk or /talk-builder:talk-assets."
