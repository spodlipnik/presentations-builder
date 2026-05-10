#!/bin/sh
# SessionStart hook — ensure the talk-builder Python venv exists and has all required packages.
# Provisions ${CLAUDE_PLUGIN_DATA}/venv from assets/scripts/requirements.txt if needed.
# Silent on success; emits a Claude Code-format JSON warning on failure.

VENV="${CLAUDE_PLUGIN_DATA}/venv"
REQUIRED_IMPORTS='import pptx, yaml, lxml, docling, cairosvg'

# Make libcairo discoverable on macOS Homebrew layouts so cairosvg can load.
export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib:/usr/local/lib:/opt/local/lib:${DYLD_FALLBACK_LIBRARY_PATH}"

# Fast path: venv already provisioned with everything we need.
if [ -d "$VENV" ] && "$VENV/bin/python3" -c "$REQUIRED_IMPORTS" 2>/dev/null; then
    exit 0
fi

# Slow path: try to create + populate the venv.
if python3 -m venv "$VENV" 2>/dev/null \
    && "$VENV/bin/pip" install --quiet -r "${CLAUDE_PLUGIN_ROOT}/assets/scripts/requirements.txt" 2>/dev/null \
    && "$VENV/bin/python3" -c "$REQUIRED_IMPORTS" 2>/dev/null; then
    exit 0
fi

printf '{"result": "warn", "message": "Talk Builder: Python deps unavailable. If error mentions libcairo, run: brew install cairo. If cairo IS installed but cairosvg fails, set DYLD_FALLBACK_LIBRARY_PATH to include /opt/homebrew/lib (skills already do this when invoking cairosvg)."}'
