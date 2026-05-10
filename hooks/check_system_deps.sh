#!/bin/sh
# SessionStart hook — warn on missing system deps (poppler, Python 3, libcairo).
# Emits a Claude Code-format JSON result only when something is missing; silent on success.

missing=""

which pdftoppm >/dev/null 2>&1 || missing="${missing:+$missing, }poppler (brew install poppler)"
which python3 >/dev/null 2>&1 || missing="${missing:+$missing, }Python 3 (brew install python)"

if ! { [ -f /opt/homebrew/lib/libcairo.2.dylib ] \
    || [ -f /usr/local/lib/libcairo.2.dylib ] \
    || [ -f /opt/local/lib/libcairo.2.dylib ]; }; then
    missing="${missing:+$missing, }cairo (brew install cairo) — needed by cairosvg for SVG→PNG"
fi

if [ -n "$missing" ]; then
    printf '{"result": "warn", "message": "Talk Builder: missing system dependencies: %s"}' "$missing"
fi
