# Docling PDF Extraction — Design Spec

**Date:** 2026-04-06
**Problem:** talk-research reads PDFs directly via Claude's Read tool, consuming ~1M+ tokens for 35 papers and spawning fragile parallel agents that fail silently. This is expensive, slow, and unreliable.

**Solution:** Pre-extract all PDFs with Docling (IBM, MIT license) into structured markdown before Claude touches them. Claude reads only the extracted output (~52k tokens instead of ~1M+).

## Architecture

```
pdfs/*.pdf
    │
    ▼
extract_pdfs.py (Docling + multiprocessing)
    │
    ├── pdfs/extracted/<filename>.md     ← structured markdown per paper
    ├── pdfs/extracted/<filename>/       ← extracted images per paper
    │   ├── fig-001.png
    │   └── fig-002.png
    └── pdfs/extracted/_index.yaml       ← manifest: filename, pages, title, sections, image count
    │
    ▼
talk-research reads _index.yaml + individual .md files
    │
    ▼
Claude writes docs/research.md (synthesis, no raw PDF reading)
```

## Component 1: `extract_pdfs.py`

**Location:** `assets/scripts/extract_pdfs.py`

**Usage:**
```bash
${CLAUDE_PLUGIN_DATA}/venv/bin/python3 ${CLAUDE_PLUGIN_ROOT}/assets/scripts/extract_pdfs.py <pdfs_directory>
```

**Behavior:**
1. Scan `<pdfs_directory>` for `*.pdf` files (non-recursive)
2. Check if `<pdfs_directory>/extracted/` exists with up-to-date extractions (compare mtime of each PDF vs its `.md` — skip already-extracted)
3. Detect CPU cores: `os.cpu_count() - 4` workers (minimum 2, maximum 8)
4. Use `multiprocessing.Pool` — each worker creates its own `DocumentConverter` and runs `convert()`
5. Per PDF, write:
   - `extracted/<filename>.md` — full structured markdown (headings, tables, text)
   - `extracted/<filename>/` — directory with extracted images (if any)
6. After all PDFs processed, write `extracted/_index.yaml` — manifest with:
   ```yaml
   - filename: "Podwojniak_2024.pdf"
     title: "Acne and the cutaneous microbiome..."
     pages: 13
     sections: [Introduction, Methods, Results, Discussion, Conclusions]
     tables: 4
     figures: 3
     images_extracted: 3
     extracted_at: "2026-04-06T14:30:00"
     md_path: "extracted/Podwojniak_2024.md"
   ```

**Error handling:**
- If a single PDF fails, log the error and continue with the rest
- Write `_extraction_errors.log` with failed filenames and reasons
- Exit code 0 if at least 1 PDF succeeded, exit code 1 if all failed

**Dependencies:** `docling` (includes PyTorch). Added to `requirements.txt`.

**Incremental extraction:** If a PDF was already extracted (`.md` exists and PDF mtime <= `.md` mtime), skip it. This makes re-runs fast when the user adds a few new PDFs.

## Component 2: Docling installation in plugin venv

**Hook change in `hooks/hooks.json`:**

Add Docling to the existing Python venv hook. Since Docling is heavy (~1.5GB with PyTorch), the install should:
1. Check if Docling is already installed in the venv: `python3 -c "import docling"` 
2. Only install if missing
3. Show a warning if install fails (don't block the plugin — Docling is only needed for talk-research)

**requirements.txt change:**
```
python-pptx>=1.0.2
PyYAML>=6.0
lxml>=4.9.0
docling>=2.80.0
```

**First-run experience:** The first time a user runs `/talk-research` with PDFs, the venv may need to install Docling. The script should detect this and tell the user: "Installing Docling (one-time, ~1.5GB download)... This takes 2-3 minutes."


**DECISION:** Eager install via requirements.txt. Docling installs once into the persistent venv (`${CLAUDE_PLUGIN_DATA}/venv`) and stays across sessions. The SessionStart hook already handles venv creation and dependency installation — Docling is just another dependency. This way any install issues surface at setup time, not mid-workflow.

## Component 3: talk-research SKILL.md changes

### CRITICAL CONSTRAINT — NO DIRECT PDF READING

```
┌─────────────────────────────────────────────────────────┐
│ talk-research MUST NEVER read PDF files directly.       │
│                                                         │
│ It MUST use the pre-extracted markdown from Docling.    │
│ If extraction hasn't been run, it MUST run the script   │
│ first and wait for it to complete.                      │
│                                                         │
│ The ONLY exception: using Read tool to visually inspect │
│ a specific figure on a specific page (with the pages    │
│ parameter) AFTER reading the extracted markdown.        │
└─────────────────────────────────────────────────────────┘
```

### Changes to Step 6 (Deep-read all PDFs)

**Current Step 6:** "Read EVERY PDF in `pdfs/`" — this is what causes the token explosion.

**New Step 6:**

```markdown
### Step 6: Extract and read PDFs

**6a. Run Docling extraction**

Check if `pdfs/extracted/_index.yaml` exists and is up to date:

If missing or stale, run the extraction script:
\```bash
${CLAUDE_PLUGIN_DATA}/venv/bin/python3 \
  ${CLAUDE_PLUGIN_ROOT}/assets/scripts/extract_pdfs.py \
  pdfs/
\```

This processes all PDFs in parallel (~2-3 minutes for 35 papers).
Wait for it to complete. Report results to user:

> "Extracted [N] papers ([M] pages total) in [X] seconds.
>  [E] errors (see pdfs/extracted/_extraction_errors.log)"

**6b. Read the extraction index**

Read `pdfs/extracted/_index.yaml` to see what's available.
List all papers with their title, pages, sections, tables, figures.

**6c. Read extracted markdown files**

Read each `pdfs/extracted/<filename>.md` using the Read tool.
These are structured markdown with headings, tables (as markdown tables),
and figure captions. Much smaller than raw PDFs.

DO NOT read the original PDF files. ONLY read the extracted .md files.

**6d. Visual figure inspection (selective)**

After reading all extracted markdown, identify figures that need
visual inspection (e.g., Kaplan-Meier curves, forest plots, clinical photos).
For ONLY those specific figures, use the Read tool with the `pages` parameter
to view the specific page in the original PDF:

\```
Read(file_path="pdfs/paper.pdf", pages="9")
\```

This should be rare — only for figures where the caption alone
doesn't provide enough information for the visual elements catalog.
Limit to maximum 10-15 page reads across all papers.
```

### Changes to allowed-tools

Add `Bash` to the allowed-tools list (needed to run `extract_pdfs.py`):

```yaml
allowed-tools:
  - Read
  - Write
  - Bash           # NEW — needed for extract_pdfs.py
  - Glob
  - Grep
  - WebSearch
  - WebFetch
  - mcp__claude_ai_PubMed__search_articles
  - mcp__claude_ai_PubMed__get_article_metadata
  - mcp__claude_ai_PubMed__get_full_text_article
  - mcp__claude_ai_Consensus__search
```

### Explicit prohibition

Add to the "## Important" section at the top of the skill:

```markdown
- **NEVER read PDF files directly with the Read tool.** Always use the 
  pre-extracted markdown from `pdfs/extracted/`. If the extraction hasn't 
  been run, run `extract_pdfs.py` first. The ONLY exception is viewing 
  a specific page for visual figure inspection (using the `pages` parameter).
  Reading full PDFs directly wastes tokens and risks context overflow.
```

## Component 4: talk-assets integration

`talk-assets` also benefits from Docling extraction. The extracted images
in `pdfs/extracted/<filename>/` can be used directly instead of running
`pdfimages` separately. Update talk-assets to check for pre-extracted
images before running its own extraction.

This is a MINOR change — just add a check at the beginning of talk-assets.

## What this does NOT change

- Steps 0-5 of talk-research (search strategy, PubMed/Consensus, PDF acquisition) — unchanged
- Steps 7-11 (consolidation, calibration, review, iteration, verification) — unchanged
- The format and content of `docs/research.md` — unchanged
- Other skills (talk-briefing, talk-vision, talk-narrative, etc.) — unchanged
- The plugin hook for Python venv — Docling added to requirements.txt, installed automatically

## Token budget comparison

| Approach | Tokens for 35 papers | Agents needed | Failure rate |
|---|---|---|---|
| Current (Read PDFs) | ~1M+ | 4-10 | High (context overflow) |
| New (Docling → markdown) | ~52k + ~15 page reads (~30k) = ~82k | 0 | Near zero |

**12x reduction in token usage. Zero agents. Zero context overflows.**

## Risks

1. **Docling install size** (1.5GB) — one-time cost, persists in venv across sessions
2. **Docling extraction quality** — tested on real paper (Podwojniak 2024), quality is excellent for text and tables
3. **First-run latency** — Docling install (2-3 min) + model download (~500MB) + extraction (~2-3 min). Subsequent runs: only extraction of new PDFs (~seconds)
4. **Docling bugs** — pin version to avoid regressions: `docling>=2.80.0,<3.0.0`
