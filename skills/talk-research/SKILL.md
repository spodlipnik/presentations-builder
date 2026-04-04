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

Iterative research phase that builds a comprehensive evidence base for the presentation. Uses PubMed, Consensus, and user-provided PDFs.

## Important

- This phase is iterative — it loops until the user is satisfied.
- The user can add PDFs to `pdfs/` at ANY point during this phase.
- Every claim in `research.md` MUST have a verifiable reference (DOI or PMID).
- NEVER invent or fabricate references. If you cannot find a source, say so.

Read `talk.yaml` and `vision.md` before starting to understand topic, angle, and intent.

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

### Step 1: Initial search

Based on the topic and vision, construct search queries for PubMed and Consensus.

Use the MCP tools:
- `mcp__claude_ai_PubMed__search_articles` for PubMed searches
- `mcp__claude_ai_Consensus__search` for Consensus searches

Search strategy:
- Start broad with the main topic
- Then narrow based on the vision angle
- Look for: key reviews, landmark studies, recent advances, relevant clinical data

### Step 2: Present results interactively

Show the user what you found in a structured list:

```
Found 15 relevant articles. Here are the top results:

1. [Title] — Author et al., Journal (Year)
   Key finding: [one sentence]
   Relevance: [why it matters for this talk]

2. [Title] — Author et al., Journal (Year)
   ...
```

Ask: "Which of these do you want to include? Any specific angles to explore further?"

### Step 3: Read user PDFs

Check `pdfs/` for any files. If present:
- Read each PDF
- Extract key findings, methodology, conclusions
- Integrate into the research base

Tell the user: "I've read [N] PDFs from your pdfs/ folder. Here's what I found relevant..."

### Step 4: Consolidate research.md

Write `research.md` with this structure:

```markdown
# Research — [Talk Topic]

## Key Findings

### [Finding Category 1]
- [Finding with source] (Author et al., Year; DOI: xxx)
- [Finding with source] ...

### [Finding Category 2]
- ...

## Key Statistics
- [Statistic] (Source)
- ...

## Potential STAR Moment Data
- [Surprising or impactful data points that could serve as STAR moments]

## Gaps Identified
- [Areas where more evidence is needed]

## References
1. Author et al. "Title." Journal, Year. DOI: xxx / PMID: xxx
2. ...
```

### Step 5: Review together

Present the consolidated research to the user. Ask:
- "Are there gaps you'd like to fill?"
- "Any specific aspect you want to dig deeper into?"
- "Should we search for more papers on [identified gap]?"

### Step 6: Iterate

If the user wants more:
- Run additional searches
- Read new PDFs they add to `pdfs/`
- Update `research.md`

Continue until the user confirms: "The research base is solid."

### Step 7: Reference verification

Before finalizing, verify:
- Every claim has a source
- DOIs/PMIDs are present for all references
- No fabricated citations
- Key statistics are accurately transcribed from sources

## After completion

Tell the user: "Research complete! Next phase: Assets — extracting and preparing visual materials. Continue with /talk or /talk-assets."
