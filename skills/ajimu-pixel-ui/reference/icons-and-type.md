# Pixel icons and typography

## Icons

- **Grid:** use 16×16 for interface icons and 24×24 only for larger empty states.
  Do not mix sizes in one toolbar.
- **Shapes:** simple, recognizable silhouettes with 1–2px strokes, no anti-aliasing
  and no gradients.
- **Color:** monochrome with `fill="currentColor"`, so icons inherit token colors.
  Render with `shape-rendering: crispEdges` and `image-rendering: pixelated` for
  bitmaps.
- **Style:** never mix pixel icons with smooth line or filled modern icon sets.
- **Accessibility:** add `aria-hidden="true"` to decorative icons and an
  accessible name to icon-only buttons.

### Generate a sprite from ASCII grids

Write each icon as a text file of `#` (filled) and `.` (empty), one row per line,
for example `icons/play.txt`:

```
................
....#...........
....##..........
....###.........
....####........
....#####.......
....####........
....###.........
....##..........
....#...........
................
```

Then run:

```bash
python scripts/pixel_icons.py icons/ --out assets/sprite.svg
```

The script writes one `<symbol id="i-<file name>">` per file. Use an icon with:

```html
<svg class="icon" aria-hidden="true"><use href="#i-play"/></svg>
```

```css
.icon { width: 16px; height: 16px; fill: currentColor; shape-rendering: crispEdges; }
```

Inline the sprite once in the page, or serve it from the same origin. The script
rejects ragged grids and unknown characters with the offending file and line.

## Typography

- Main content uses a modern, readable font: the system sans-serif stack or the
  project's font. Code, identifiers and logs use monospace.
- A pixel font is optional and only for short titles, brand marks and large numbers,
  normally 15px and up. Never use it for paragraphs, form labels, tabs or small
  badges: small pixel glyphs become ambiguous, for example "C" can read as "O".
- Bundle fonts locally. Use only an open license such as the SIL Open Font License,
  keep the file unmodified, and record its source revision, file hash and license
  text in the project's third-party notices.
- Keep a simple hierarchy: page title, window title, section title and body text.
  Avoid retro effects such as scanlines, dithering text or blur.

```css
@font-face { font-family: "Pixel Title Font"; src: url("/fonts/PixelTitle.ttf") format("truetype"); font-display: swap; }
h1, h2, .brand { font-family: var(--font-pixel); letter-spacing: .4px; }
```
