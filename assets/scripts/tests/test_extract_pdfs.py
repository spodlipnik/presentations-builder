"""Tests for extract_pdfs.py — helper functions only (no Docling required)."""

import os
import sys
import time
from pathlib import Path
from unittest.mock import patch

import yaml

sys.path.insert(0, str(Path(__file__).parent.parent))

from extract_pdfs import sanitize_filename, calculate_workers, needs_extraction, write_index


# ---------------------------------------------------------------------------
# sanitize_filename
# ---------------------------------------------------------------------------

class TestSanitizeFilename:
    def test_basic_pdf(self):
        assert sanitize_filename("my_paper.pdf") == "my_paper"

    def test_removes_path_components(self):
        result = sanitize_filename("/home/user/docs/paper.pdf")
        assert "/" not in result
        assert result == "paper"

    def test_replaces_spaces_and_special_chars(self):
        result = sanitize_filename("My Paper (2024) — v2.pdf")
        # Spaces, parens, em-dash become underscores; collapses runs
        assert " " not in result
        assert "(" not in result
        assert result == "my_paper_2024_v2"

    def test_collapses_repeated_underscores(self):
        result = sanitize_filename("foo___bar--baz.pdf")
        assert "__" not in result
        assert "--" not in result

    def test_strips_leading_trailing_underscores(self):
        result = sanitize_filename("_leading_and_trailing_.pdf")
        assert not result.startswith("_")
        assert not result.endswith("_")

    def test_lowercase(self):
        assert sanitize_filename("UPPERCASE.PDF") == "uppercase"

    def test_dots_in_name(self):
        result = sanitize_filename("file.name.with.dots.pdf")
        assert "." not in result  # dots replaced


# ---------------------------------------------------------------------------
# calculate_workers
# ---------------------------------------------------------------------------

class TestCalculateWorkers:
    def test_returns_int(self):
        assert isinstance(calculate_workers(), int)

    def test_minimum_is_2(self):
        with patch("extract_pdfs.os.cpu_count", return_value=2):
            assert calculate_workers() == 2

    def test_maximum_is_8(self):
        with patch("extract_pdfs.os.cpu_count", return_value=20):
            assert calculate_workers() == 8

    def test_formula(self):
        with patch("extract_pdfs.os.cpu_count", return_value=10):
            assert calculate_workers() == 6

    def test_none_cpu_count(self):
        with patch("extract_pdfs.os.cpu_count", return_value=None):
            # Falls back to 4, 4-4=0, clamped to 2
            assert calculate_workers() == 2

    def test_exact_boundary_low(self):
        with patch("extract_pdfs.os.cpu_count", return_value=6):
            assert calculate_workers() == 2

    def test_exact_boundary_high(self):
        with patch("extract_pdfs.os.cpu_count", return_value=12):
            assert calculate_workers() == 8


# ---------------------------------------------------------------------------
# needs_extraction
# ---------------------------------------------------------------------------

class TestNeedsExtraction:
    def test_no_md_exists(self, tmp_path):
        pdf = tmp_path / "paper.pdf"
        pdf.write_text("fake pdf")
        extracted = tmp_path / "extracted"
        extracted.mkdir()
        assert needs_extraction(str(pdf), str(extracted)) is True

    def test_md_exists_and_newer(self, tmp_path):
        pdf = tmp_path / "paper.pdf"
        pdf.write_text("fake pdf")
        extracted = tmp_path / "extracted"
        extracted.mkdir()

        md = extracted / "paper.md"
        # Ensure md is written after pdf
        time.sleep(0.05)
        md.write_text("# Extracted")

        assert needs_extraction(str(pdf), str(extracted)) is False

    def test_pdf_newer_than_md(self, tmp_path):
        pdf = tmp_path / "paper.pdf"
        extracted = tmp_path / "extracted"
        extracted.mkdir()

        md = extracted / "paper.md"
        md.write_text("# Old extraction")

        # Make pdf newer
        time.sleep(0.05)
        pdf.write_text("updated fake pdf")

        assert needs_extraction(str(pdf), str(extracted)) is True

    def test_sanitized_name_used(self, tmp_path):
        """needs_extraction uses sanitize_filename so special chars are handled."""
        pdf = tmp_path / "My Paper (2024).pdf"
        pdf.write_text("fake")
        extracted = tmp_path / "extracted"
        extracted.mkdir()

        # Create md with sanitized name
        safe = sanitize_filename(str(pdf))
        md = extracted / f"{safe}.md"
        time.sleep(0.05)
        md.write_text("# Done")

        assert needs_extraction(str(pdf), str(extracted)) is False


# ---------------------------------------------------------------------------
# write_index
# ---------------------------------------------------------------------------

class TestWriteIndex:
    def test_creates_yaml_file(self, tmp_path):
        entries = [
            {
                "filename": "paper.pdf",
                "title": "paper",
                "pages": 10,
                "sections": ["Introduction", "Methods", "Results", "Discussion", "Conclusion"],
                "tables": 2,
                "figures": 3,
                "images_extracted": 3,
                "md_path": "/tmp/extracted/paper.md",
                "extracted_at": "2024-01-01T00:00:00+00:00",
                "status": "ok",
            }
        ]
        write_index(entries, str(tmp_path))
        index = tmp_path / "_index.yaml"
        assert index.exists()
        data = yaml.safe_load(index.read_text())
        assert len(data) == 1
        assert data[0]["filename"] == "paper.pdf"
        assert data[0]["status"] == "ok"

    def test_strips_error_field(self, tmp_path):
        entries = [
            {
                "filename": "bad.pdf",
                "status": "error",
                "error": "something went wrong",
            }
        ]
        write_index(entries, str(tmp_path))
        data = yaml.safe_load((tmp_path / "_index.yaml").read_text())
        assert "error" not in data[0]

    def test_creates_directory_if_needed(self, tmp_path):
        target = tmp_path / "nested" / "dir"
        write_index([], str(target))
        assert (target / "_index.yaml").exists()

    def test_multiple_entries(self, tmp_path):
        entries = [
            {"filename": f"paper{i}.pdf", "status": "ok"} for i in range(5)
        ]
        write_index(entries, str(tmp_path))
        data = yaml.safe_load((tmp_path / "_index.yaml").read_text())
        assert len(data) == 5
