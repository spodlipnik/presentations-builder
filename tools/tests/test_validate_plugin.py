"""Tests for tools/validate_plugin.py.

Each test builds a minimal-but-realistic fake plugin tree in tmp_path, points
the module's REPO_ROOT at it, and asserts main() returns the expected exit
code while emitting the expected stderr.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Import after path manipulation so `tools` is importable regardless of CWD.
TOOLS_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT_REAL = TOOLS_DIR.parent
if str(REPO_ROOT_REAL) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_REAL))

import tools.validate_plugin as vp  # noqa: E402, I001


# ---------------------------------------------------------------------------
# Helpers — build a valid baseline fake plugin tree
# ---------------------------------------------------------------------------

def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _make_valid_plugin(root: Path, name: str = "test-plugin", version: str = "1.0.0") -> None:
    _write(
        root / ".claude-plugin" / "plugin.json",
        json.dumps({"name": name, "version": version}),
    )
    _write(
        root / ".claude-plugin" / "marketplace.json",
        json.dumps({"plugins": [{"name": name}]}),
    )
    _write(root / "hooks" / "hooks.json", json.dumps({"hooks": {}}))
    _write(
        root / "skills" / "alpha" / "SKILL.md",
        "---\nname: alpha\ndescription: Use when alpha\nallowed-tools:\n  - Read\n---\n\n# Alpha\n",
    )
    _write(
        root / ".claude" / "rules" / "rule-a.md",
        "---\ndescription: rule A description\npaths:\n  - skills/**\n---\n\n# Rule A\n",
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_valid_plugin_passes(tmp_path: Path, monkeypatch, capsys):
    _make_valid_plugin(tmp_path)
    monkeypatch.setattr(vp, "REPO_ROOT", tmp_path)
    assert vp.main() == 0
    out = capsys.readouterr().out
    assert "Plugin valid: 1 skills, 1 rules" in out


def test_missing_plugin_json_fails(tmp_path: Path, monkeypatch, capsys):
    _make_valid_plugin(tmp_path)
    (tmp_path / ".claude-plugin" / "plugin.json").unlink()
    monkeypatch.setattr(vp, "REPO_ROOT", tmp_path)
    assert vp.main() == 1
    err = capsys.readouterr().err
    assert "plugin.json: missing" in err


def test_bad_semver_fails(tmp_path: Path, monkeypatch, capsys):
    _make_valid_plugin(tmp_path, version="not-semver")
    monkeypatch.setattr(vp, "REPO_ROOT", tmp_path)
    assert vp.main() == 1
    err = capsys.readouterr().err
    assert "not semver" in err


def test_invalid_json_in_plugin_json_fails(tmp_path: Path, monkeypatch, capsys):
    _make_valid_plugin(tmp_path)
    (tmp_path / ".claude-plugin" / "plugin.json").write_text("{ not-valid-json }", encoding="utf-8")
    monkeypatch.setattr(vp, "REPO_ROOT", tmp_path)
    assert vp.main() == 1
    err = capsys.readouterr().err
    assert "invalid JSON" in err


def test_plugin_name_missing_from_marketplace_fails(tmp_path: Path, monkeypatch, capsys):
    _make_valid_plugin(tmp_path, name="real-name")
    _write(
        tmp_path / ".claude-plugin" / "marketplace.json",
        json.dumps({"plugins": [{"name": "different-name"}]}),
    )
    monkeypatch.setattr(vp, "REPO_ROOT", tmp_path)
    assert vp.main() == 1
    err = capsys.readouterr().err
    assert "not in marketplace" in err


def test_skill_missing_skill_md_fails(tmp_path: Path, monkeypatch, capsys):
    _make_valid_plugin(tmp_path)
    (tmp_path / "skills" / "alpha" / "SKILL.md").unlink()
    monkeypatch.setattr(vp, "REPO_ROOT", tmp_path)
    assert vp.main() == 1
    err = capsys.readouterr().err
    assert "missing SKILL.md" in err


def test_skill_name_directory_mismatch_fails(tmp_path: Path, monkeypatch, capsys):
    _make_valid_plugin(tmp_path)
    _write(
        tmp_path / "skills" / "alpha" / "SKILL.md",
        "---\nname: WRONG\ndescription: x\nallowed-tools:\n  - Read\n---\n",
    )
    monkeypatch.setattr(vp, "REPO_ROOT", tmp_path)
    assert vp.main() == 1
    err = capsys.readouterr().err
    assert "!= directory 'alpha'" in err


def test_skill_empty_description_fails(tmp_path: Path, monkeypatch, capsys):
    _make_valid_plugin(tmp_path)
    _write(
        tmp_path / "skills" / "alpha" / "SKILL.md",
        "---\nname: alpha\ndescription:\nallowed-tools:\n  - Read\n---\n",
    )
    monkeypatch.setattr(vp, "REPO_ROOT", tmp_path)
    assert vp.main() == 1
    err = capsys.readouterr().err
    assert "empty description" in err


def test_skill_empty_allowed_tools_fails(tmp_path: Path, monkeypatch, capsys):
    _make_valid_plugin(tmp_path)
    _write(
        tmp_path / "skills" / "alpha" / "SKILL.md",
        "---\nname: alpha\ndescription: x\nallowed-tools: []\n---\n",
    )
    monkeypatch.setattr(vp, "REPO_ROOT", tmp_path)
    assert vp.main() == 1
    err = capsys.readouterr().err
    assert "empty allowed-tools" in err


def test_skill_malformed_yaml_fails(tmp_path: Path, monkeypatch, capsys):
    _make_valid_plugin(tmp_path)
    _write(
        tmp_path / "skills" / "alpha" / "SKILL.md",
        "---\nname: alpha\n  description: bad-indent\n---\n",
    )
    monkeypatch.setattr(vp, "REPO_ROOT", tmp_path)
    assert vp.main() == 1
    err = capsys.readouterr().err
    assert "invalid YAML" in err


def test_skill_missing_frontmatter_fails(tmp_path: Path, monkeypatch, capsys):
    _make_valid_plugin(tmp_path)
    _write(tmp_path / "skills" / "alpha" / "SKILL.md", "# No frontmatter here\n")
    monkeypatch.setattr(vp, "REPO_ROOT", tmp_path)
    assert vp.main() == 1
    err = capsys.readouterr().err
    assert "no YAML frontmatter" in err


def test_rule_missing_paths_fails(tmp_path: Path, monkeypatch, capsys):
    _make_valid_plugin(tmp_path)
    _write(
        tmp_path / ".claude" / "rules" / "rule-a.md",
        "---\ndescription: rule A\n---\n",
    )
    monkeypatch.setattr(vp, "REPO_ROOT", tmp_path)
    assert vp.main() == 1
    err = capsys.readouterr().err
    assert "paths must be a non-empty list" in err


def test_rule_paths_not_a_list_fails(tmp_path: Path, monkeypatch, capsys):
    _make_valid_plugin(tmp_path)
    _write(
        tmp_path / ".claude" / "rules" / "rule-a.md",
        "---\ndescription: rule A\npaths: not-a-list\n---\n",
    )
    monkeypatch.setattr(vp, "REPO_ROOT", tmp_path)
    assert vp.main() == 1
    err = capsys.readouterr().err
    assert "paths must be a non-empty list" in err


def test_rule_empty_description_fails(tmp_path: Path, monkeypatch, capsys):
    _make_valid_plugin(tmp_path)
    _write(
        tmp_path / ".claude" / "rules" / "rule-a.md",
        "---\ndescription:\npaths:\n  - skills/**\n---\n",
    )
    monkeypatch.setattr(vp, "REPO_ROOT", tmp_path)
    assert vp.main() == 1
    err = capsys.readouterr().err
    assert "empty description" in err


def test_real_repo_validates(monkeypatch, capsys):
    """Smoke test against the actual repo — guards against the validator going stale."""
    monkeypatch.setattr(vp, "REPO_ROOT", REPO_ROOT_REAL)
    assert vp.main() == 0
