#!/usr/bin/env python3
"""Structural validator for the talk-builder plugin.

Checks:
  1. Every JSON file in the plugin (.claude-plugin/plugin.json,
     .claude-plugin/marketplace.json, hooks/hooks.json, evals/*.json)
     parses as valid JSON.
  2. plugin.json and marketplace.json reference the same plugin name.
  3. Every skills/<name>/SKILL.md has a YAML frontmatter with required
     fields (name == directory, description, allowed-tools).
  4. Every .claude/rules/*.md has a YAML frontmatter with required
     fields (description, paths).
  5. .claude-plugin/plugin.json version matches semver pattern.

Exits with status 0 on success, 1 on any failure. Failures are listed.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?$")


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


def check_json(errors: list[str], path: Path) -> dict | list | None:
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as e:
        fail(errors, f"{path}: invalid JSON — {e}")
        return None
    except FileNotFoundError:
        fail(errors, f"{path}: missing")
        return None


def check_yaml_frontmatter(errors: list[str], path: Path) -> dict | None:
    try:
        content = path.read_text()
    except FileNotFoundError:
        fail(errors, f"{path}: missing")
        return None
    m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not m:
        fail(errors, f"{path}: no YAML frontmatter")
        return None
    try:
        return yaml.safe_load(m.group(1))
    except yaml.YAMLError as e:
        fail(errors, f"{path}: invalid YAML frontmatter — {e}")
        return None


def main() -> int:
    errors: list[str] = []

    # 1. Plugin manifests
    plugin_path = REPO_ROOT / ".claude-plugin" / "plugin.json"
    plugin = check_json(errors, plugin_path)
    if plugin is not None and not SEMVER_RE.match(plugin.get("version", "")):
        fail(errors, f"{plugin_path}: version {plugin.get('version')!r} is not semver")

    marketplace_path = REPO_ROOT / ".claude-plugin" / "marketplace.json"
    marketplace = check_json(errors, marketplace_path)

    if plugin and marketplace:
        plugin_name = plugin.get("name")
        mp_names = [p.get("name") for p in marketplace.get("plugins", [])]
        if plugin_name not in mp_names:
            fail(errors, f"plugin.name {plugin_name!r} not in marketplace.plugins[*].name {mp_names!r}")

    # 2. Hooks
    check_json(errors, REPO_ROOT / "hooks" / "hooks.json")

    # 3. Evals
    evals_dir = REPO_ROOT / "evals"
    if evals_dir.is_dir():
        for f in sorted(evals_dir.glob("*.json")):
            check_json(errors, f)

    # 4. Skills
    skills_dir = REPO_ROOT / "skills"
    skill_count = 0
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            fail(errors, f"{skill_dir}: missing SKILL.md")
            continue
        skill_count += 1
        fm = check_yaml_frontmatter(errors, skill_md)
        if fm is None:
            continue
        if fm.get("name") != skill_dir.name:
            fail(errors, f"{skill_md}: name {fm.get('name')!r} != directory {skill_dir.name!r}")
        if not fm.get("description"):
            fail(errors, f"{skill_md}: empty description")
        if not fm.get("allowed-tools"):
            fail(errors, f"{skill_md}: empty allowed-tools")

    # 5. Rules
    rules_dir = REPO_ROOT / ".claude" / "rules"
    rule_count = 0
    if rules_dir.is_dir():
        for rule_md in sorted(rules_dir.glob("*.md")):
            rule_count += 1
            fm = check_yaml_frontmatter(errors, rule_md)
            if fm is None:
                continue
            if not fm.get("description"):
                fail(errors, f"{rule_md}: empty description")
            paths = fm.get("paths")
            if not paths or not isinstance(paths, list):
                fail(errors, f"{rule_md}: paths must be a non-empty list")

    # Report
    if errors:
        print(f"❌ {len(errors)} validation error(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(f"✅ Plugin valid: {skill_count} skills, {rule_count} rules")
    return 0


if __name__ == "__main__":
    sys.exit(main())
