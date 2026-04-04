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
- **NEVER invent or fabricate references.** If you cannot find a source, say so explicitly. If a DOI cannot be confirmed, mark it as "[DOI: UNVERIFIED — check manually]". A missing reference is always better than a fake one. This is a medical presentation — incorrect citations damage the speaker's credibility with specialists who know the literature.
- **Reference quality matters.** Prioritize high-impact journals and high-evidence-level studies. A meta-analysis in Lancet carries more weight than a case series in a low-tier journal. Note the journal and evidence level for each reference.

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

### Step 0: Ask research preferences

Before searching, ask the user ONE question that sets scope:

"Before I start searching, a few quick preferences:
- **How many key references** do you want in the final research doc? (I'd suggest [N] for a [X]-minute talk, but you decide)
- **Any specific journals or databases you trust most?** (e.g., 'prioritize NEJM, Lancet, JAAD' or 'anything peer-reviewed is fine')
- **Any papers you already know should be included?** (landmark studies, your own publications, etc.)

This helps me search smarter and not overwhelm you with 50 papers when you need 8."

Use their answers to calibrate search depth and filtering.

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
1. [Title] — Author et al., Journal (Year) [IF: X.X]
   Evidence: [meta-analysis / RCT / cohort / case series / review]
   Key finding: [one sentence]
   Relevance: [how it connects to the vision]
   Priority: [ESSENTIAL / SUPPORTING / OPTIONAL]
   Full-text: [Open Access / Requires download]

2. [Title] — Author et al., Journal (Year) [IF: X.X]
   ...
```

**Prioritization criteria:**
- **ESSENTIAL:** Directly supports core message, high evidence level, high-impact journal. These MUST be in the talk.
- **SUPPORTING:** Adds depth or context, good evidence. Include if there's room.
- **OPTIONAL:** Interesting but not critical. Keep as backup for Q&A.

Prioritize by evidence quality (meta-analyses > RCTs > cohort > case series) AND by journal quality. But a compelling case report that fits the narrative can be more valuable than a weak meta-analysis that doesn't.

Ask: "Which of these do you want to include? I've marked my recommendations — the ESSENTIAL ones I'd keep no matter what."

### Step 4: Obtain full-text PDFs

After the user selects papers, try to obtain full-text for each:

1. **Try PubMed full-text** — use `mcp__claude_ai_PubMed__get_full_text_article` for open access papers
2. **Check for PDFs already in `pdfs/`** — the user may have pre-loaded some
3. **List papers still missing** — provide a clear download checklist:

```
Papers obtained (full-text available):
  ✓ Gopalakrishnan 2018 — via PubMed Central
  ✓ Smith 2023 — already in pdfs/

Papers you need to download:
  ✗ Routy 2023 (Nature Medicine) — DOI: 10.1038/xxx
  ✗ Davar 2021 (Science) — DOI: 10.1126/xxx
  
  Download these and place them in: [working directory]/pdfs/
```

### Step 5: Manual search pause (Scopus / Google Scholar)

After the automated search, explicitly offer the user time to complement:

"I've found [N] papers via PubMed/Consensus. Before I deep-read everything, this is a good moment to:

- **Search Scopus or Google Scholar** for papers I might have missed (especially recent publications, conference abstracts, or papers in journals not fully indexed in PubMed)
- **Add your own publications** if relevant
- **Add papers from colleagues** or recommendations you've received

Take your time — when you've added any extra PDFs to `pdfs/`, just tell me 'ready' and I'll read everything together."

**Wait for the user to come back.** Do not proceed until they confirm. They might need minutes or hours to search Scopus — that's fine.

### Step 6: Deep-read all PDFs

Once the user confirms all PDFs are in place, read EVERY PDF in `pdfs/`:

For each paper, extract:
- **Exact numbers** — sample sizes, effect sizes, p-values, confidence intervals, hazard ratios
- **Methodology** — study design, population, follow-up duration
- **Key conclusions** — in the authors' own words
- **Relevant figures** — identify figures that could be used in the presentation (mark page numbers and describe content for the assets phase)
- **Limitations** — what the authors themselves acknowledge

This deep reading is critical — abstracts alone lead to imprecise claims. The full text gives you the exact data the speaker needs to be credible in front of specialists.

Present a summary per paper: "I've read [N] papers. Here's what I found in each..."

### Step 7: Consolidate research.md

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

## Key Statistics (ready for slides)
| Statistic | Source | Priority |
|---|---|---|
| [number + context] | [Author Year] | [ESSENTIAL / SUPPORTING] |

## STAR Moment Candidates
- [Surprising or impactful data points that could serve as STAR moments]
- [Include the numbers — specific, visceralized, comparable]

## Counter-Arguments & Limitations
- [What skeptics would say, with sources]
- [Known limitations of the evidence]

## Figures for Slides (from PDFs)
| Paper | Page | Description | Relevance |
|---|---|---|---|
| [Author Year] | p.4 | [Kaplan-Meier survival curve] | [STAR moment slide] |
| [Author Year] | p.7 | [Forest plot of meta-analysis] | [Evidence summary slide] |

This table feeds into the `/talk-assets` phase for extraction.

## Gaps Identified
- [Areas where more evidence is needed or could strengthen the talk]

## References
1. Author et al. "Title." Journal, Year;Vol(Issue):Pages. DOI: xxx / PMID: xxx
2. ...
```

### Step 8: Calibrate scope

Guide the user on how much evidence is enough:
- **10-min talk:** 3-5 key references are plenty
- **15-min talk:** 5-8 key references
- **20-min talk:** 8-12 key references
- **30-min talk:** 10-15 key references

These are references that directly appear in or support the narrative — not every paper you read. More is not better. Say: "You have [N] references for a [X]-minute talk. That's [sufficient / a bit light / more than enough]. Want to search for more or are we solid?"

### Step 9: Review together

Present the consolidated research. Ask:
- "Does this evidence support your core message?"
- "Are there gaps that weaken your argument?"
- "Any specific aspect you want to dig deeper into?"
- "Are there enough figures identified for the slides?"

### Step 10: Iterate

If the user wants more:
- Run additional targeted searches
- Read new PDFs they add to `pdfs/`
- Update `research.md`

Continue until the user confirms the evidence base is solid.

### Step 11: Reference verification

Before finalizing, verify:
- Every claim has a source with DOI or PMID
- No fabricated citations — if in doubt, flag it as `[UNVERIFIED]`
- Key statistics are accurately transcribed from full-text sources (not abstracts)
- References section is complete with journal, volume, issue, pages
- Figures table is complete for the assets phase

## After completion

Tell the user: "Research complete! Next phase: Assets — extracting and preparing visual materials. Continue with /talk or /talk-builder:talk-assets."
