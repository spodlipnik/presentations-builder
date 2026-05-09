---
description: cairosvg + libcairo gotcha on macOS — always prepend DYLD_FALLBACK_LIBRARY_PATH
paths:
  - "hooks/**"
  - "skills/talk-assets/**"
  - "assets/scripts/requirements.txt"
---

# cairosvg / libcairo gotcha on macOS

`cairosvg` (the Python lib used by `talk-assets` for SVG → PNG) is a wrapper around the system `libcairo`. On macOS:

1. The system lib must be installed: `brew install cairo`. The SessionStart hook checks for it and warns if missing.
2. macOS Python (CommandLineTools) does NOT search `/opt/homebrew/lib` by default. Even with libcairo installed, `import cairosvg` raises:

   ```
   OSError: no library called "cairo-2" was found
   ```

   Skills that invoke cairosvg MUST prepend:

   ```bash
   DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib:/usr/local/lib:/opt/local/lib
   ```

   to the Python command. See `skills/talk-assets/SKILL.md` (CHART section) for the canonical incantation.

## Why three paths?

- `/opt/homebrew/lib` — Apple Silicon Homebrew (default for M1/M2/M3 Macs)
- `/usr/local/lib` — Intel Mac Homebrew (still used by some users)
- `/opt/local/lib` — MacPorts (less common but still in use)

Listing all three makes the prepend portable across macOS install variants.

## Why not set it globally?

We could put it in the user's shell profile, but the plugin can't assume that. Making each cairosvg call self-contained is the robust choice.
