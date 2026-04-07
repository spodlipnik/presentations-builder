"""Extract PDFs to structured markdown + images using IBM Docling with multiprocessing."""

import os
import re
import sys

import multiprocessing
from datetime import datetime, timezone
from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sanitize_filename(pdf_path: str) -> str:
    """Convert PDF filename to a safe identifier.

    Removes extension, path components, and problematic characters.
    Collapses runs of underscores/hyphens and strips leading/trailing ones.
    """
    name = Path(pdf_path).stem
    # Replace spaces and problematic chars with underscores
    name = re.sub(r"[^\w\-]", "_", name)
    # Collapse repeated underscores/hyphens
    name = re.sub(r"[_\-]{2,}", "_", name)
    # Strip leading/trailing underscores/hyphens
    name = name.strip("_-")
    # Lowercase for consistency
    return name.lower()


def calculate_workers() -> int:
    """Return worker count: cpu_count() - 4, clamped to [2, 8]."""
    cpus = os.cpu_count() or 4
    return max(2, min(8, cpus - 4))


def needs_extraction(pdf_path: str, extracted_dir: str) -> bool:
    """Return True if the PDF needs (re-)extraction.

    Compares the mtime of the source PDF against its extracted markdown.
    If the markdown doesn't exist or is older than the PDF, extraction is needed.
    """
    md_path = Path(extracted_dir) / f"{sanitize_filename(pdf_path)}.md"
    if not md_path.exists():
        return True
    pdf_mtime = os.path.getmtime(pdf_path)
    md_mtime = os.path.getmtime(md_path)
    return pdf_mtime > md_mtime


def extract_single_pdf(args: tuple) -> dict:
    """Extract one PDF using Docling. Designed to run in a worker process.

    Args:
        args: (pdf_path, extracted_dir) tuple

    Returns:
        dict with keys: filename, title, pages, sections, tables, figures,
        images_extracted, md_path, extracted_at, status, error (if any)
    """
    pdf_path, extracted_dir = args
    pdf_path = str(pdf_path)
    extracted_dir = Path(extracted_dir)
    safe_name = sanitize_filename(pdf_path)
    md_path = extracted_dir / f"{safe_name}.md"
    images_dir = extracted_dir / safe_name

    result = {
        "filename": Path(pdf_path).name,
        "title": Path(pdf_path).stem,
        "pages": 0,
        "sections": 0,
        "tables": 0,
        "figures": 0,
        "images_extracted": 0,
        "md_path": str(md_path),
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "status": "error",
        "error": None,
    }

    try:
        # Import Docling inside worker to avoid pickling issues
        from docling.document_converter import DocumentConverter

        # Try the richer API first; fall back to bare converter
        try:
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
                    InputFormat.PDF: PdfFormatOption(
                        pipeline_options=pipeline_options
                    )
                }
            )
        except (ImportError, AttributeError, TypeError):
            converter = DocumentConverter()

        conv_result = converter.convert(pdf_path)
        doc = conv_result.document

        # Export markdown
        markdown = doc.export_to_markdown()
        extracted_dir.mkdir(parents=True, exist_ok=True)
        md_path.write_text(markdown, encoding="utf-8")

        # Count structural elements from the markdown
        lines = markdown.split("\n")
        result["sections"] = [l.lstrip("#").strip() for l in lines if l.startswith("## ") and not l.startswith("### ")]
        result["tables"] = markdown.count("|---")  # rough heuristic

        # Extract images if the document exposes them
        images_dir.mkdir(parents=True, exist_ok=True)
        img_count = 0
        try:
            if hasattr(doc, "pictures") and doc.pictures:
                for idx, pic in enumerate(doc.pictures, 1):
                    if hasattr(pic, "image") and pic.image and hasattr(pic.image, "pil_image"):
                        img = pic.image.pil_image
                        img_file = images_dir / f"fig-{idx:03d}.png"
                        img.save(str(img_file))
                        img_count += 1
        except Exception:
            pass  # Image extraction is best-effort

        result["images_extracted"] = img_count
        result["figures"] = img_count

        # Try to get page count
        try:
            if hasattr(doc, "pages"):
                result["pages"] = len(doc.pages)
        except Exception:
            # Fallback: count page breaks in markdown
            result["pages"] = markdown.count("<!-- page-break -->") + 1

        result["status"] = "ok"

    except Exception as exc:
        result["error"] = str(exc)
        # Log error to file alongside extracted dir
        error_log = extracted_dir / "_extraction_errors.log"
        extracted_dir.mkdir(parents=True, exist_ok=True)
        with open(error_log, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now(timezone.utc).isoformat()}] {Path(pdf_path).name}: {exc}\n")

    return result


def write_index(entries: list, extracted_dir: str) -> None:
    """Write _index.yaml manifest from a list of result dicts."""
    extracted_dir = Path(extracted_dir)
    extracted_dir.mkdir(parents=True, exist_ok=True)

    # Strip internal-only fields before writing
    clean = []
    for entry in entries:
        e = dict(entry)
        e.pop("error", None)
        clean.append(e)

    index_path = extracted_dir / "_index.yaml"
    with open(index_path, "w", encoding="utf-8") as f:
        yaml.dump(clean, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: extract_pdfs.py <pdfs_directory>", file=sys.stderr)
        return 1

    pdfs_dir = Path(sys.argv[1]).resolve()
    if not pdfs_dir.is_dir():
        print(f"Error: {pdfs_dir} is not a directory", file=sys.stderr)
        return 1

    extracted_dir = pdfs_dir / "extracted"
    extracted_dir.mkdir(parents=True, exist_ok=True)

    # Collect PDFs needing extraction (non-recursive)
    all_pdfs = sorted(pdfs_dir.glob("*.pdf"))
    if not all_pdfs:
        print("No PDF files found.", file=sys.stderr)
        return 1

    to_extract = [
        (str(p), str(extracted_dir))
        for p in all_pdfs
        if needs_extraction(str(p), str(extracted_dir))
    ]

    if not to_extract:
        print("All PDFs already extracted (up to date).")
        # Rebuild index from existing markdowns
        existing = []
        for p in all_pdfs:
            safe = sanitize_filename(str(p))
            md = extracted_dir / f"{safe}.md"
            if md.exists():
                md_content = md.read_text(encoding="utf-8")
                sections = [l.lstrip("#").strip() for l in md_content.split("\n") if l.startswith("## ") and not l.startswith("### ")]
                existing.append({
                    "filename": p.name,
                    "title": p.stem,
                    "pages": 0,
                    "sections": sections,
                    "tables": 0,
                    "figures": 0,
                    "images_extracted": 0,
                    "md_path": str(md),
                    "extracted_at": datetime.fromtimestamp(
                        md.stat().st_mtime, tz=timezone.utc
                    ).isoformat(),
                    "status": "ok",
                })
        if existing:
            write_index(existing, str(extracted_dir))
        return 0

    workers = calculate_workers()
    print(f"Extracting {len(to_extract)}/{len(all_pdfs)} PDFs with {workers} workers...")

    # Use multiprocessing to extract in parallel
    results = []
    with multiprocessing.Pool(processes=workers) as pool:
        for result in pool.imap_unordered(extract_single_pdf, to_extract):
            status_icon = "ok" if result["status"] == "ok" else "FAIL"
            print(f"  [{status_icon}] {result['filename']}")
            results.append(result)

    # Include previously-extracted PDFs in the index
    extracted_names = {r["filename"] for r in results}
    for p in all_pdfs:
        if p.name not in extracted_names:
            safe = sanitize_filename(str(p))
            md = extracted_dir / f"{safe}.md"
            if md.exists():
                md_content = md.read_text(encoding="utf-8")
                sections = [l.lstrip("#").strip() for l in md_content.split("\n") if l.startswith("## ") and not l.startswith("### ")]
                results.append({
                    "filename": p.name,
                    "title": p.stem,
                    "pages": 0,
                    "sections": sections,
                    "tables": 0,
                    "figures": 0,
                    "images_extracted": 0,
                    "md_path": str(md),
                    "extracted_at": datetime.fromtimestamp(
                        md.stat().st_mtime, tz=timezone.utc
                    ).isoformat(),
                    "status": "ok",
                })

    write_index(results, str(extracted_dir))

    succeeded = sum(1 for r in results if r["status"] == "ok")
    failed = sum(1 for r in results if r["status"] != "ok")
    print(f"\nDone: {succeeded} succeeded, {failed} failed.")

    return 0 if succeeded > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
