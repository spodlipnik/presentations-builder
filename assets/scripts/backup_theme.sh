#!/bin/bash
# backup_theme.sh — Create dated backup of a theme.yaml file.
#
# Usage: backup_theme.sh <theme-yaml-path>
#
# Creates .backups/theme.YYYY-MM-DD-HHMM.yaml in the theme directory.
# Keeps only the last 5 backups (deletes oldest).
#
set -euo pipefail

THEME_YAML="${1:?Missing theme.yaml path}"

if [ ! -f "$THEME_YAML" ]; then
    echo "Error: theme.yaml not found: $THEME_YAML" >&2
    exit 1
fi

THEME_DIR=$(dirname "$THEME_YAML")
BACKUP_DIR="$THEME_DIR/.backups"
TIMESTAMP=$(date +%Y-%m-%d-%H%M)
BACKUP_FILE="$BACKUP_DIR/theme.$TIMESTAMP.yaml"

mkdir -p "$BACKUP_DIR"
cp "$THEME_YAML" "$BACKUP_FILE"
echo "Backup created: $BACKUP_FILE"

# Keep only last 5 backups (delete oldest)
BACKUP_COUNT=$(find "$BACKUP_DIR" -name "theme.*.yaml" -type f | wc -l | tr -d ' ')
if [ "$BACKUP_COUNT" -gt 5 ]; then
    TO_DELETE=$((BACKUP_COUNT - 5))
    find "$BACKUP_DIR" -name "theme.*.yaml" -type f | sort | head -n "$TO_DELETE" | while read -r old; do
        rm "$old"
        echo "Removed old backup: $(basename "$old")"
    done
fi
