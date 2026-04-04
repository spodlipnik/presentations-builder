# Talk Builder

A Claude Code plugin for building academic and medical presentations with structured storytelling — from research to final PPTX and speaker scripts.

## Features

- **10-skill orchestrated workflow**: briefing, vision, research, assets, narrative, slides, study documents, speaker script
- **Evidence-based research**: PubMed and Consensus integration with DOI/PMID verification
- **Storytelling frameworks**: ABT, Sparkline, STAR moments, assertion-evidence design
- **Personal style config**: fonts, colors, layout preferences applied consistently
- **PPTX generation**: automated slide creation with PptxGenJS
- **Study documents**: comprehensive review-article-style reference and per-paper summaries
- **Speaker scripts**: preparation table + teleprompter format

## Requirements

- **Claude Code** (latest version)
- **poppler** — PDF image extraction: `brew install poppler`
- **Node.js** — PPTX generation: `brew install node`
- **PPTX plugin** from `claude-plugins-official` marketplace
- **Recommended**: PubMed and Consensus MCP servers (claude.ai > Settings > MCP Servers)

## Installation

Install from the marketplace:

```
/plugin install talk-builder
```

Or load locally for development:

```bash
claude --plugin-dir ./presentations-builder
```

## Quick Start

1. Run `/talk-builder:talk-setup` to configure your personal style
2. Create a new directory for your presentation: `mkdir my-talk && cd my-talk`
3. Run `/talk-builder:talk` to start the guided workflow

## Skills

| Skill | Purpose |
|---|---|
| `/talk` | Main orchestrator — detects phase and guides workflow |
| `/talk-setup` | One-time style and environment configuration |
| `/talk-briefing` | Collect topic, duration, audience, preferences |
| `/talk-vision` | Define personal angle, message, emotional intent |
| `/talk-research` | Search literature, read PDFs, build evidence base |
| `/talk-assets` | Extract figures from PDFs, propose AI image prompts |
| `/talk-narrative` | Build slide structure with storytelling arc and timing |
| `/talk-slides` | Generate PPTX presentation file |
| `/talk-study-doc` | Create study document and article summaries |
| `/talk-script` | Generate speaker script with teleprompter format |

## How It Works

Each presentation is a directory. Talk Builder detects your progress by checking which files exist:

| File | Phase |
|---|---|
| `talk.yaml` | Briefing complete |
| `vision.md` | Vision defined |
| `research.md` | Research complete |
| `images/` (non-empty) | Assets ready |
| `narrative.md` | Narrative approved |
| `study-document.md` | Study docs complete |
| `speaker-script.md` | Script ready |
| `presentation.pptx` | Slides generated |

Run `/talk` at any point to see your status and continue from where you left off.

## Configuration

Personal style is stored in a `config.yaml` at a path you choose during setup. Per-project overrides go in `talk.yaml`.

See `config.example.yaml` for all available options.

## License

MIT — see [LICENSE](LICENSE)
