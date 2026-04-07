# Docling PDF Extraction — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace direct PDF reading in talk-research with Docling pre-extraction, reducing token usage ~12x and eliminating fragile parallel agents.

**Architecture:** Python script (`extract_pdfs.py`) uses Docling + multiprocessing to extract all PDFs into structured markdown + images. talk-research reads only the extracted output. Claude never touches raw PDFs except for selective figure inspection.

**Tech Stack:** Docling (IBM, MIT), Python multiprocessing, PyYAML, pdfplumber (fallback)

**Spec:** `docs/superpowers/specs/2026-04-06-docling-pdf-extraction-design.md`

---

### Task 1: Add Docling to requirements and verify installation

**Files:**
- Modify: `assets/scripts/requirements.txt`

- [ ] **Step 1: Add docling to requirements.txt**

```
python-pptx>=1.0.2
PyYAML>=6.0
lxml>=4.9.0
docling>=2.80.0,<3.0.0
```

- [ ] **Step 2: Install in the plugin venv and verify**

Run:
```bash
${CLAUDE_PLUGIN_DATA}/venv/bin/pip install -r ${CLAUDE_PLUGIN_ROOT}/assets/scripts/requirements.txt
```

Expected: Docling + PyTorch install successfully (~1.5GB, takes 2-3 minutes).

- [ ] **Step 3: Verify Docling works**

Run:
```bash
${CLAUDE_PLUGIN_DATA}/venv/bin/python3 -c "
from docling.document_converter import DocumentConverter
print('Docling OK:', DocumentConverter)
"
```

Expected: prints `Docling OK: <class 'docling.document_converter.DocumentConverter'>`

- [ ] **Step 4: Verify Docling on a real PDF**

Run:
```bash
${CLAUDE_PLUGIN_DATA}/venv/bin/python3 -c "
from docling.document_converter import DocumentConverter
converter = DocumentConverter()
result = converter.convert('/Users/sebastianpodlipnik/Personal/Presentaciones - keynote/congresos/Microbiota y dermatología/2026-04_microbiota_dermatologia/pdfs/toda la bibliografía/Acad Dermatol Venereol - 2024 - Podwojniak - Acne and the cutaneous microbiome  A systematic review of mechanisms and.pdf')
md = result.document.export_to_markdown()
print(f'Extracted {len(md)} chars')
print(md[:500])
"
```

Expected: Markdown output with structured headings, tables, and clean text. Should show the abstract and first section with proper formatting.

- [ ] **Step 5: Commit**

```bash
git add assets/scripts/requirements.txt
git commit -m "feat: add docling to requirements for PDF pre-extraction"
```

---

### Task 2: Write `extract_pdfs.py` — core extraction logic

**Files:**
- Create: `assets/scripts/extract_pdfs.py`
- Test: `assets/scripts/tests/test_extract_pdfs.py`

- [ ] **Step 1: Write the failing test**

Create `assets/scripts/tests/test_extract_pdfs.py`:

```python
import os
import tempfile
import pytest
import yaml

# We test the helper functions, not the full Docling pipeline
# (which requires real PDFs and models)


def test_sanitize_filename():
    from extract_pdfs import sanitize_filename

    assert sanitize_filename("Hello World (2024).pdf") == "Hello_World_2024"
    assert sanitize_filename("Acad Dermatol Venereol - 2024 - Podwojniak.pdf") == "Acad_Dermatol_Venereol_-_2024_-_Podwojniak"
    assert sanitize_filename("file.pdf") == "file"
    assert sanitize_filename("a/b/c.pdf") == "c"


def test_calculate_workers():
    from extract_pdfs import calculate_workers

    # Should be cpu_count - 4, min 2, max 8
    workers = calculate_workers()
    assert 2 <= workers <= 8


def test_needs_extraction_missing_md(tmp_path):
    from extract_pdfs import needs_extraction

    pdf_path = tmp_path / "test.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 fake")
    extracted_dir = tmp_path / "extracted"
    extracted_dir.mkdir()

    assert needs_extraction(str(pdf_path), str(extracted_dir)) is True


def test_needs_extraction_stale_md(tmp_path):
    from extract_pdfs import needs_extraction

    pdf_path = tmp_path / "test.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 fake")

    extracted_dir = tmp_path / "extracted"
    extracted_dir.mkdir()
    md_path = extracted_dir / "test.md"
    md_path.write_text("old extraction")

    # Make PDF newer than md
    import time
    time.sleep(0.1)
    pdf_path.write_bytes(b"%PDF-1.4 updated")

    assert needs_extraction(str(pdf_path), str(extracted_dir)) is True


def test_needs_extraction_up_to_date(tmp_path):
    from extract_pdfs import needs_extraction

    extracted_dir = tmp_path / "extracted"
    extracted_dir.mkdir()
    md_path = extracted_dir / "test.md"
    md_path.write_text("current extraction")

    pdf_path = tmp_path / "test.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 fake")

    # md is newer (created after pdf)
    import time
    time.sleep(0.1)
    md_path.write_text("current extraction updated")

    assert needs_extraction(str(pdf_path), str(extracted_dir)) is False


def test_write_index(tmp_path):
    from extract_pdfs import write_index

    entries = [
        {
            "filename": "test.pdf",
            "title": "Test Paper",
            "pages": 10,
            "sections": ["Introduction", "Methods"],
            "tables": 2,
            "figures": 1,
            "images_extracted": 1,
            "md_path": "extracted/test.md",
        }
    ]

    write_index(entries, str(tmp_path / "extracted"))
    index_path = tmp_path / "extracted" / "_index.yaml"
    assert index_path.exists()

    data = yaml.safe_load(index_path.read_text())
    assert len(data) == 1
    assert data[0]["filename"] == "test.pdf"
    assert data[0]["pages"] == 10
```

- [ ] **Step 2: Run test to verify it fails**

Run:
```bash
cd ${CLAUDE_PLUGIN_ROOT} && ${CLAUDE_PLUGIN_DATA}/venv/bin/python3 -m pytest assets/scripts/tests/test_extract_pdfs.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'extract_pdfs'`

- [ ] **Step 3: Write the implementation**

Create `assets/scripts/extract_pdfs.py`:

```python
#!/usr/bin/env python3
"""Extract PDFs into structured markdown using Docling.

Usage:
    python extract_pdfs.py <pdfs_directory>

Output:
    <pdfs_directory>/extracted/<filename>.md      — structured markdown
    <pdfs_directory>/extracted/<filename>/         — extracted images
    <pdfs_directory>/extracted/_index.yaml         — manifest
    <pdfs_directory>/extracted/_extraction_errors.log  — errors (if any)
"""

import os
import sys
import time
import re
import yaml
from datetime import datetime, timezone
from multiprocessing import Pool
from pathlib import Path


def sanitize_filename(pdf_path: str) -> str:
    """Convert PDF filename to a safe identifier (no extension, no path)."""
    name = Path(pdf_path).stem
    # Replace problematic chars with underscore, collapse multiples
    name = re.sub(r"[()&,;:'\"\[\]]+", "", name)
    name = re.sub(r"\s+", "_", name.strip())
    name = re.sub(r"_+", "_", name)
    return name.rstrip("_")


def calculate_workers() -> int:
    """Calculate optimal worker count: cpu_count - 4, clamped to [2, 8]."""
    cpu = os.cpu_count() or 4
    return max(2, min(8, cpu - 4))


def needs_extraction(pdf_path: str, extracted_dir: str) -> bool:
    """Check if a PDF needs (re-)extraction based on file modification times."""
    sanitized = sanitize_filename(pdf_path)
    md_path = os.path.join(extracted_dir, f"{sanitized}.md")

    if not os.path.exists(md_path):
        return True

    pdf_mtime = os.path.getmtime(pdf_path)
    md_mtime = os.path.getmtime(md_path)
    return pdf_mtime > md_mtime


def extract_single_pdf(args: tuple) -> dict:
    """Extract a single PDF using Docling. Runs in a worker process.

    Args:
        args: tuple of (pdf_path, extracted_dir)

    Returns:
        dict with extraction results or error info
    """
    pdf_path, extracted_dir = args
    sanitized = sanitize_filename(pdf_path)
    md_path = os.path.join(extracted_dir, f"{sanitized}.md")
    images_dir = os.path.join(extracted_dir, sanitized)

    try:
        from docling.document_converter import DocumentConverter
        from docling.datamodel.base_models import InputFormat
        from docling.document_converter import PdfFormatOption
        from docling.datamodel.pipeline_options import PdfPipelineOptions

        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_table_structure = True
        pipeline_options.images_scale = 2.0
        pipeline_options.generate_page_images = False
        pipeline_options.generate_picture_images = True

        converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

        result = converter.convert(pdf_path)
        doc = result.document

        # Export markdown
        markdown = doc.export_to_markdown()
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(markdown)

        # Export images
        os.makedirs(images_dir, exist_ok=True)
        image_count = 0
        for element, _level in doc.iterate_items():
            if hasattr(element, "image") and element.image is not None:
                image_count += 1
                img_path = os.path.join(images_dir, f"fig-{image_count:03d}.png")
                try:
                    element.image.pil_image.save(img_path)
                except Exception:
                    pass  # Image export is best-effort

        # Detect sections from markdown headings
        sections = []
        for line in markdown.split("\n"):
            if line.startswith("## ") and not line.startswith("### "):
                sections.append(line.lstrip("# ").strip())

        # Count tables (markdown tables have |---|)
        table_count = markdown.count("|---|")

        # Extract title (first # heading)
        title = ""
        for line in markdown.split("\n"):
            if line.startswith("# ") and not line.startswith("## "):
                title = line.lstrip("# ").strip()
                break

        return {
            "filename": os.path.basename(pdf_path),
            "title": title or sanitized,
            "pages": getattr(result.document, "num_pages", 0) or len(result.pages),
            "sections": sections,
            "tables": table_count,
            "figures": image_count,
            "images_extracted": image_count,
            "md_path": f"extracted/{sanitized}.md",
            "extracted_at": datetime.now(timezone.utc).isoformat(),
            "error": None,
        }

    except Exception as e:
        return {
            "filename": os.path.basename(pdf_path),
            "title": sanitized,
            "pages": 0,
            "sections": [],
            "tables": 0,
            "figures": 0,
            "images_extracted": 0,
            "md_path": "",
            "extracted_at": datetime.now(timezone.utc).isoformat(),
            "error": str(e),
        }


def write_index(entries: list, extracted_dir: str) -> None:
    """Write _index.yaml manifest."""
    os.makedirs(extracted_dir, exist_ok=True)
    index_path = os.path.join(extracted_dir, "_index.yaml")
    # Filter out error field for clean index, but keep errored entries marked
    clean_entries = []
    for e in entries:
        entry = {k: v for k, v in e.items() if k != "error"}
        if e.get("error"):
            entry["status"] = "error"
            entry["error_message"] = e["error"]
        else:
            entry["status"] = "ok"
        clean_entries.append(entry)

    with open(index_path, "w", encoding="utf-8") as f:
        yaml.dump(clean_entries, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


def main():
    if len(sys.argv) < 2:
        print("Usage: extract_pdfs.py <pdfs_directory>")
        sys.exit(1)

    pdfs_dir = sys.argv[1]
    if not os.path.isdir(pdfs_dir):
        print(f"Error: {pdfs_dir} is not a directory")
        sys.exit(1)

    extracted_dir = os.path.join(pdfs_dir, "extracted")
    os.makedirs(extracted_dir, exist_ok=True)

    # Find all PDFs
    pdf_files = sorted(
        [os.path.join(pdfs_dir, f) for f in os.listdir(pdfs_dir) if f.lower().endswith(".pdf")]
    )

    if not pdf_files:
        print(f"No PDF files found in {pdfs_dir}")
        sys.exit(0)

    # Filter to only those needing extraction
    to_extract = [(p, extracted_dir) for p in pdf_files if needs_extraction(p, extracted_dir)]
    already_done = len(pdf_files) - len(to_extract)

    if not to_extract:
        print(f"All {len(pdf_files)} PDFs already extracted. Nothing to do.")
        # Still regenerate index from existing .md files
        entries = []
        for pdf_path in pdf_files:
            sanitized = sanitize_filename(pdf_path)
            md_path = os.path.join(extracted_dir, f"{sanitized}.md")
            if os.path.exists(md_path):
                md_content = open(md_path, "r", encoding="utf-8").read()
                sections = [l.lstrip("# ").strip() for l in md_content.split("\n") if l.startswith("## ") and not l.startswith("### ")]
                title = ""
                for line in md_content.split("\n"):
                    if line.startswith("# ") and not line.startswith("## "):
                        title = line.lstrip("# ").strip()
                        break
                entries.append({
                    "filename": os.path.basename(pdf_path),
                    "title": title or sanitized,
                    "pages": 0,
                    "sections": sections,
                    "tables": md_content.count("|---|"),
                    "figures": 0,
                    "images_extracted": len(list(Path(os.path.join(extracted_dir, sanitized)).glob("*.png"))) if os.path.isdir(os.path.join(extracted_dir, sanitized)) else 0,
                    "md_path": f"extracted/{sanitized}.md",
                    "extracted_at": datetime.fromtimestamp(os.path.getmtime(md_path), tz=timezone.utc).isoformat(),
                    "error": None,
                })
        write_index(entries, extracted_dir)
        sys.exit(0)

    workers = calculate_workers()
    print(f"Extracting {len(to_extract)} PDFs ({already_done} already up-to-date)")
    print(f"Using {workers} parallel workers")

    start_time = time.time()

    with Pool(workers) as pool:
        results = pool.map(extract_single_pdf, to_extract)

    elapsed = time.time() - start_time

    # Collect results
    successes = [r for r in results if r["error"] is None]
    failures = [r for r in results if r["error"] is not None]

    # Also include previously extracted files in index
    all_entries = list(results)
    for pdf_path in pdf_files:
        sanitized = sanitize_filename(pdf_path)
        if not any(r["filename"] == os.path.basename(pdf_path) for r in results):
            md_path = os.path.join(extracted_dir, f"{sanitized}.md")
            if os.path.exists(md_path):
                md_content = open(md_path, "r", encoding="utf-8").read()
                sections = [l.lstrip("# ").strip() for l in md_content.split("\n") if l.startswith("## ") and not l.startswith("### ")]
                title = ""
                for line in md_content.split("\n"):
                    if line.startswith("# ") and not line.startswith("## "):
                        title = line.lstrip("# ").strip()
                        break
                all_entries.append({
                    "filename": os.path.basename(pdf_path),
                    "title": title or sanitized,
                    "pages": 0,
                    "sections": sections,
                    "tables": md_content.count("|---|"),
                    "figures": 0,
                    "images_extracted": len(list(Path(os.path.join(extracted_dir, sanitized)).glob("*.png"))) if os.path.isdir(os.path.join(extracted_dir, sanitized)) else 0,
                    "md_path": f"extracted/{sanitized}.md",
                    "extracted_at": datetime.fromtimestamp(os.path.getmtime(md_path), tz=timezone.utc).isoformat(),
                    "error": None,
                })

    # Write index
    write_index(all_entries, extracted_dir)

    # Write errors log
    if failures:
        errors_log = os.path.join(extracted_dir, "_extraction_errors.log")
        with open(errors_log, "w") as f:
            for r in failures:
                f.write(f"{r['filename']}: {r['error']}\n")

    # Summary
    print(f"\nDone in {elapsed:.1f}s")
    print(f"  Extracted: {len(successes)}")
    print(f"  Skipped (up-to-date): {already_done}")
    if failures:
        print(f"  Failed: {len(failures)}")
        for r in failures:
            print(f"    - {r['filename']}: {r['error']}")
    print(f"  Index: {os.path.join(extracted_dir, '_index.yaml')}")

    sys.exit(0 if successes or already_done > 0 else 1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run:
```bash
cd ${CLAUDE_PLUGIN_ROOT} && PYTHONPATH=assets/scripts ${CLAUDE_PLUGIN_DATA}/venv/bin/python3 -m pytest assets/scripts/tests/test_extract_pdfs.py -v
```

Expected: All 6 tests PASS.

- [ ] **Step 5: Run integration test with real PDF**

Run:
```bash
mkdir -p /tmp/docling-test && cp "/Users/sebastianpodlipnik/Personal/Presentaciones - keynote/congresos/Microbiota y dermatología/2026-04_microbiota_dermatologia/pdfs/toda la bibliografía/Acad Dermatol Venereol - 2024 - Podwojniak - Acne and the cutaneous microbiome  A systematic review of mechanisms and.pdf" /tmp/docling-test/

${CLAUDE_PLUGIN_DATA}/venv/bin/python3 ${CLAUDE_PLUGIN_ROOT}/assets/scripts/extract_pdfs.py /tmp/docling-test/
```

Expected:
- `/tmp/docling-test/extracted/*.md` created with structured markdown
- `/tmp/docling-test/extracted/_index.yaml` created with paper metadata
- Tables rendered as markdown tables
- Two-column layout handled correctly
- Output under ~5k tokens for this paper

- [ ] **Step 6: Verify incremental extraction (re-run skips)**

Run:
```bash
${CLAUDE_PLUGIN_DATA}/venv/bin/python3 ${CLAUDE_PLUGIN_ROOT}/assets/scripts/extract_pdfs.py /tmp/docling-test/
```

Expected: "All 1 PDFs already extracted. Nothing to do."

- [ ] **Step 7: Commit**

```bash
git add assets/scripts/extract_pdfs.py assets/scripts/tests/test_extract_pdfs.py
git commit -m "feat: add extract_pdfs.py with Docling + multiprocessing"
```

---

### Task 3: Update talk-research SKILL.md

**Files:**
- Modify: `skills/talk-research/SKILL.md`

- [ ] **Step 1: Add Bash to allowed-tools**

In the frontmatter, add `Bash` to the allowed-tools list:

```yaml
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - WebSearch
  - WebFetch
  - mcp__claude_ai_PubMed__search_articles
  - mcp__claude_ai_PubMed__get_article_metadata
  - mcp__claude_ai_PubMed__get_full_text_article
  - mcp__claude_ai_Consensus__search
```

- [ ] **Step 2: Add PDF prohibition to Important section**

After the existing bullet about NEVER inventing references, add:

```markdown
- **NEVER read PDF files directly with the Read tool.** Always use the pre-extracted markdown from `pdfs/extracted/`. If the extraction hasn't been run, run `extract_pdfs.py` first. The ONLY exception is viewing a specific page for visual figure inspection (using the `pages` parameter). Reading full PDFs directly wastes tokens and risks context overflow.
```

- [ ] **Step 3: Replace Step 6 entirely**

Replace the entire "### Step 6: Deep-read all PDFs" section with the new Step 6 from the spec. The new step has 4 sub-steps:

- **6a**: Run Docling extraction via Bash:
  ```bash
  ${CLAUDE_PLUGIN_DATA}/venv/bin/python3 ${CLAUDE_PLUGIN_ROOT}/assets/scripts/extract_pdfs.py pdfs/
  ```
- **6b**: Read `pdfs/extracted/_index.yaml`
- **6c**: Read each `pdfs/extracted/<filename>.md` (NOT the original PDFs)
- **6d**: Selective figure inspection (max 10-15 page reads total)

Full replacement text is in the spec, section "Component 3 → Changes to Step 6".

- [ ] **Step 4: Verify the skill file is valid YAML frontmatter + markdown**

Run:
```bash
head -20 ${CLAUDE_PLUGIN_ROOT}/skills/talk-research/SKILL.md
```

Expected: Valid YAML frontmatter with all allowed-tools including Bash.

- [ ] **Step 5: Commit**

```bash
git add skills/talk-research/SKILL.md
git commit -m "feat(talk-research): use Docling pre-extraction instead of direct PDF reading

BREAKING: talk-research no longer reads PDF files directly.
Requires extract_pdfs.py to be run first (automatic in Step 6).
Reduces token usage ~12x for 35 papers."
```

---

### Task 4: Update talk-assets to use pre-extracted images

**Files:**
- Modify: `skills/talk-assets/SKILL.md`

- [ ] **Step 1: Read current talk-assets SKILL.md**

Read `skills/talk-assets/SKILL.md` to find where image extraction is described.

- [ ] **Step 2: Add pre-extracted images check**

At the beginning of the image extraction section, add a check:

```markdown
Before extracting images from PDFs, check if Docling has already extracted them:

1. Check `pdfs/extracted/` for image directories (created by `extract_pdfs.py` in the research phase)
2. If images exist in `pdfs/extracted/<paper>/fig-*.png`, use those directly
3. Only run `pdfimages` for papers that don't have pre-extracted images
```

- [ ] **Step 3: Commit**

```bash
git add skills/talk-assets/SKILL.md
git commit -m "feat(talk-assets): use Docling pre-extracted images when available"
```

---

### Task 5: End-to-end test on real PDF collection

**Files:** None (validation only)

- [ ] **Step 1: Run extraction on full PDF collection**

Run:
```bash
${CLAUDE_PLUGIN_DATA}/venv/bin/python3 ${CLAUDE_PLUGIN_ROOT}/assets/scripts/extract_pdfs.py \
  "/Users/sebastianpodlipnik/Personal/Presentaciones - keynote/congresos/Microbiota y dermatología/2026-04_microbiota_dermatologia/pdfs/toda la bibliografía/"
```

Expected:
- ~35 PDFs extracted in ~2-3 minutes
- `_index.yaml` lists all papers
- Each `.md` file has structured content
- Errors (if any) logged in `_extraction_errors.log`

- [ ] **Step 2: Verify extraction quality**

Read 3 sample extracted markdown files and verify:
- Two-column text is correctly ordered
- Tables are structured as markdown tables
- Section headings detected (Introduction, Methods, Results, etc.)
- Figure captions preserved

- [ ] **Step 3: Check token count**

Run:
```bash
wc -w /path/to/extracted/*.md | tail -1
```

Expected: Total word count ~40k-60k words = ~52k-80k tokens (vs ~400k+ for raw PDFs).

- [ ] **Step 4: Verify images extracted**

Run:
```bash
find /path/to/extracted/ -name "*.png" | wc -l
```

Expected: Images extracted from papers that contain figures.

- [ ] **Step 5: Push all changes**

```bash
git push
```

Then in the other window: `/reload-plugins` and test `/talk-builder:talk-research`.
