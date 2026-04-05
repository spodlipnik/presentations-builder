#!/usr/bin/env python3
"""Load and validate theme.yaml files.

Usage:
    from load_theme import load_theme
    theme = load_theme("path/to/theme.yaml")
"""
import re
import yaml
from pathlib import Path


class ThemeValidationError(ValueError):
    """Raised when theme.yaml fails validation."""
    pass


_ID_PATTERN = re.compile(r"^[a-z0-9-]+$")
_REQUIRED_COLORS = ("primary", "text", "background")
_REQUIRED_TYPOGRAPHY = ("heading", "body")


def load_theme(theme_path):
    """Load a theme.yaml file, validate, and return the theme dict.

    Returns the content of the top-level `theme:` key. Raises ThemeValidationError
    if validation fails, or FileNotFoundError if the file does not exist.
    """
    theme_path = Path(theme_path)
    if not theme_path.exists():
        raise FileNotFoundError(f"Theme file not found: {theme_path}")

    with open(theme_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data or "theme" not in data:
        raise ThemeValidationError("theme.yaml must have top-level 'theme:' key")

    theme = data["theme"]

    # Validate ID
    theme_id = theme.get("id", "")
    if not theme_id or not _ID_PATTERN.match(theme_id):
        raise ThemeValidationError(
            f"theme.id must match pattern [a-z0-9-]+, got: {theme_id!r}"
        )

    # Validate tokens
    tokens = theme.get("tokens", {})
    colors = tokens.get("color", {}) if isinstance(tokens, dict) else {}
    for required in _REQUIRED_COLORS:
        if required not in colors:
            raise ThemeValidationError(
                f"tokens.color.{required} is required"
            )

    typography = tokens.get("typography", {})
    for required in _REQUIRED_TYPOGRAPHY:
        if required not in typography:
            raise ThemeValidationError(
                f"tokens.typography.{required} is required"
            )

    # Validate roles is a dict
    if not isinstance(theme.get("roles"), dict):
        raise ThemeValidationError("theme.roles must be a dict")

    return theme
