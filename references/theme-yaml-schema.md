# theme.yaml Schema

Defines the structure of a theme file used by `talk-slides` to generate presentations. Each theme lives in `assets_path/themes/<theme-id>/theme.yaml`.

## Top-level structure

```yaml
theme:
  id: string               # unique identifier (kebab-case)
  name: string             # human-readable name
  version: string          # semver
  description: string      # brief purpose
  created: date            # ISO date
  updated: date            # ISO date

  tokens:                  # see Tokens section
    color: {...}
    typography: {...}
    spacing: {...}
    aspect_ratio: string
    slide: {...}

  roles:                   # see Roles section
    <role-id>:
      variants: [...]

  custom_roles:            # optional, theme-specific roles
    <custom-role-id>:
      variants: [...]
```

## Tokens

Tokens are the "brand" of the theme — shared across all variants.

```yaml
tokens:
  color:
    primary: "#0B3D91"
    accent: "#E63946"
    text: "#1A1A1A"
    background: "#FFFFFF"
    muted: "#6C757D"
    # additional named colors allowed
  typography:
    heading:
      family: "Avenir Heavy"
      weight: 700
      size_pt: 54
    body:
      family: "Avenir Book"
      weight: 400
      size_pt: 24
    caption:
      family: "Avenir Book"
      weight: 400
      size_pt: 12
    # additional roles allowed
  spacing:
    margin_in: 0.5
    gutter_in: 0.25
  aspect_ratio: "16:9"  # or "4:3"
  slide:
    width_in: 13.333
    height_in: 7.5
```

## Roles and Variants

Each role implements a subset of the 18 canonical roles (see role-taxonomy.md). Each variant describes a concrete layout with positions as fractions of slide dimensions.

```yaml
roles:
  title:
    variants:
      - id: title.centered
        description: "Classic academic title, centered"
        slots: [eyebrow, title, author, affiliation, date]
        layout:
          title:
            box: [0.10, 0.35, 0.80, 0.20]   # [x, y, w, h] fractions
            font: {size: 54, weight: bold, color: text, align: center}
          author:
            box: [0.10, 0.58, 0.80, 0.08]
            font: {size: 22, color: muted, align: center}
        thumbnail: thumbnails/title.centered.jpg

  assertion-evidence:
    variants:
      - id: ae.image-right
        description: "Headline top, image 60% right"
        slots: [headline, image, caption]
        layout:
          headline:
            box: [0.05, 0.08, 0.90, 0.15]
            font: {size: 32, weight: bold, color: text, align: left}
          image:
            box: [0.55, 0.28, 0.40, 0.60]
            fit: contain
          caption:
            box: [0.55, 0.90, 0.40, 0.06]
            font: {size: 12, color: muted, align: left}
        rules:
          min_chars_headline: 20
          max_chars_headline: 140
        thumbnail: thumbnails/ae.image-right.jpg
```

## Field Reference

### `layout.<slot>.box`
Array of 4 floats `[x, y, w, h]` as fractions (0-1) of slide dimensions.

### `layout.<slot>.font`
Font specification:
- `size`: point size (integer)
- `weight`: `bold`, `regular`, or OpenType number (400, 700)
- `color`: token name from `tokens.color` (e.g., "text", "accent") OR direct hex "#RRGGBB"
- `align`: `left`, `center`, `right`, `justify`

### `layout.<slot>.fit` (images only)
- `contain`: scale to fit, preserve aspect
- `cover`: fill box, crop excess
- `fill`: stretch to fill

### `variant.rules` (optional)
Content constraints:
- `min_chars_headline`, `max_chars_headline`: content length limits
- `required_slots`: list of slots that must have content

### `variant.thumbnail`
Relative path to JPG thumbnail (generated from reference slide or preview).

## Custom Roles

Theme-specific roles not in the canonical 18:

```yaml
custom_roles:
  dermoscopy-findings:
    variants:
      - id: dermo.4-panel-grid
        slots: [title, image1, image2, image3, image4, labels]
        layout: ...
```

## Validation

A theme.yaml is valid when:
- `theme.id` matches `[a-z0-9-]+`
- `tokens.color` has at minimum: primary, text, background
- `tokens.typography` has at minimum: heading, body
- Each variant's `id` matches canonical pattern: `<role-short>.<variant-short>` (e.g., `ae.image-right`)
- All box arrays have 4 values in range [0, 1]
- `layout.<slot>.font.color` references a defined token or is valid hex
