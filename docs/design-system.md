# Design system

Every asset comes from `scripts/generate_assets.py`. Change the tokens there, then run the script.

## Color

| Token | Dark | Light | Use |
|---|---|---|---|
| bg | `#0d1117` | `#ffffff` | Canvas (matches GitHub) |
| panel / panel2 | `#161b22` / `#1c2230` | `#f6f8fa` / `#eef2f6` | Cards |
| line | `#30363d` | `#d0d7de` | Borders, routes |
| text / muted | `#e6edf3` / `#8b949e` | `#1f2328` / `#59636e` | Copy |
| cyan | `#22d3ee` | `#0891b2` | Primary accent, robotics |
| orange | `#f0883e` | `#bc4c00` | Precision engineering |
| violet | `#a371f7` | `#8250df` | AI and software |
| green | `#3fb950` | `#1a7f37` | Product, healthy status |

- Each domain owns exactly one accent color.
- Accents mark structure, such as rails, dots, and tags. They are never used for large fills.

## Typography

- **Sans:** Segoe UI, Helvetica Neue, Helvetica, Arial. Used for names and descriptions.
- **Mono:** SFMono, Consolas, Menlo. Used for labels, telemetry, and tags, in uppercase with 1–3 px letter spacing.
- **Minimum size:** 10 px in 1200-wide canvases (about 3.3 px at 390 px width). Every graphic therefore has a text equivalent in the README (link table, alt text) so it still works on mobile.

## Layout

- **Canvas:** 1200 px wide, 14 px radius, 1 px border in `line`.
- **Background:** a 20–24 px blueprint grid at low opacity.
- **Cards:** 8–12 px radius, 16–20 px inner padding.

## Motion

- The only animation is SMIL: the AMR driving its route in the banner, the pulsing core in the map, and robots on the contribution floor.
- Loops run 4–13 s and are never flashing. Browsers without SMIL show a correct static frame.

## Icons

- 24 px grid, 1.6 px stroke, round caps, a single domain color, no fills.
- Stored in `assets/icons/`.

## Rules

- No scripts, no external fonts, no external resources inside SVGs.
- Every image has descriptive alt text. Decorative icons use `alt=""`.
- Data graphics use only GitHub API values and print their update date.
