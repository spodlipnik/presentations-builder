"""Tests for load_theme.py — validates theme.yaml structure."""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from load_theme import load_theme, ThemeValidationError


def _write_yaml(path, content):
    path.write_text(content, encoding="utf-8")


def test_load_theme_valid_minimal(tmp_path):
    theme_yaml = tmp_path / "theme.yaml"
    _write_yaml(theme_yaml, """
theme:
  id: test-theme
  name: Test
  version: "1.0"
  tokens:
    color:
      primary: "#000000"
      text: "#1A1A1A"
      background: "#FFFFFF"
    typography:
      heading: {family: Arial, weight: 700, size_pt: 54}
      body: {family: Arial, weight: 400, size_pt: 24}
    aspect_ratio: "16:9"
    slide: {width_in: 13.333, height_in: 7.5}
  roles:
    title:
      variants:
        - id: title.centered
          layout:
            title: {box: [0.1, 0.3, 0.8, 0.3]}
""")
    theme = load_theme(theme_yaml)
    assert theme["id"] == "test-theme"
    assert theme["tokens"]["color"]["primary"] == "#000000"
    assert "title" in theme["roles"]


def test_load_theme_missing_required_color_fails(tmp_path):
    theme_yaml = tmp_path / "theme.yaml"
    _write_yaml(theme_yaml, """
theme:
  id: bad
  version: "1.0"
  tokens:
    color:
      primary: "#000000"
      # missing text and background
    typography:
      heading: {family: Arial}
      body: {family: Arial}
  roles: {}
""")
    with pytest.raises(ThemeValidationError, match="text"):
        load_theme(theme_yaml)


def test_load_theme_invalid_id_format_fails(tmp_path):
    theme_yaml = tmp_path / "theme.yaml"
    _write_yaml(theme_yaml, """
theme:
  id: "Invalid ID!"
  version: "1.0"
  tokens:
    color: {primary: "#000", text: "#000", background: "#FFF"}
    typography: {heading: {family: A}, body: {family: A}}
  roles: {}
""")
    with pytest.raises(ThemeValidationError, match="id"):
        load_theme(theme_yaml)


def test_load_theme_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_theme("/tmp/does_not_exist.yaml")
