#!/bin/bash
# render_thumbnails.sh — Convert a PPTX file to per-slide JPG thumbnails.
#
# Usage: render_thumbnails.sh <input.pptx> <output-dir> [dpi]
#
# Requires: soffice (LibreOffice), pdftoppm (poppler)
# Output: <output-dir>/slide-NN.jpg for each slide
#
set -euo pipefail

INPUT_PPTX="${1:?Missing input PPTX path}"
OUTPUT_DIR="${2:?Missing output directory}"
DPI="${3:-100}"

if [ ! -f "$INPUT_PPTX" ]; then
    echo "Error: PPTX file not found: $INPUT_PPTX" >&2
    exit 1
fi

if ! command -v soffice >/dev/null 2>&1; then
    echo "Error: soffice (LibreOffice) not found. Install with: brew install --cask libreoffice" >&2
    exit 2
fi

if ! command -v pdftoppm >/dev/null 2>&1; then
    echo "Error: pdftoppm not found. Install with: brew install poppler" >&2
    exit 3
fi

mkdir -p "$OUTPUT_DIR"

# Use a temp dir for the intermediate PDF
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

echo "Converting PPTX to PDF..."
soffice --headless --convert-to pdf --outdir "$TMPDIR" "$INPUT_PPTX" >/dev/null 2>&1

# Find the generated PDF (soffice names it based on input file)
PDF_FILE=$(find "$TMPDIR" -name "*.pdf" -type f | head -1)
if [ -z "$PDF_FILE" ]; then
    echo "Error: PDF conversion failed" >&2
    exit 4
fi

echo "Converting PDF to JPGs (DPI=$DPI)..."
# pdftoppm outputs as <prefix>-NN.jpg
pdftoppm -jpeg -r "$DPI" "$PDF_FILE" "$OUTPUT_DIR/slide"

# pdftoppm uses NN format (no leading zeros up to 9, then 10, 11...)
# Rename to always use 2-digit leading zeros for consistent sorting
for f in "$OUTPUT_DIR"/slide-?.jpg; do
    [ -f "$f" ] || continue
    base=$(basename "$f" .jpg)
    num=${base#slide-}
    new_name=$(printf "slide-%02d.jpg" "$num")
    mv "$f" "$OUTPUT_DIR/$new_name"
done

COUNT=$(find "$OUTPUT_DIR" -name "slide-*.jpg" -type f | wc -l | tr -d ' ')
echo "Generated $COUNT thumbnails in $OUTPUT_DIR"
