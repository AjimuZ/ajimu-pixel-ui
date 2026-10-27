---
name: ajimu-pixel-ui
description: Applies the Minimal Pixel JRPG design system - a modern, readable interface with a subtle 16-bit role-playing-game menu identity, built only from the project's existing color tokens. Use when designing, building, restyling or reviewing a web or app interface in a pixel, retro, 8/16-bit or JRPG style, or when a product (tools, dashboards, editors, admin panels) should feel like a refined RPG menu without becoming a game.
---

# Ajimu Pixel UI: Minimal Pixel JRPG

**Principle: 80% modern minimal application, 20% pixel JRPG identity.** The
result must stay a professional, usable product. Readability always wins over
retro fidelity. If the project already has an owner-approved visual reference, it
takes precedence over this guide.

## Workflow

Copy this checklist and work through it:

```
Pixel UI progress:
- [ ] 1. Find the existing color system and map its roles
- [ ] 2. Add non-color tokens (frame, pixel unit, radius, fonts, timing)
- [ ] 3. Build the shared primitives (window, button, field, tab, gauge, pill)
- [ ] 4. Apply them to layout and navigation
- [ ] 5. Add pixel icons and, optionally, a pixel title font
- [ ] 6. Verify colors, contrast, keyboard, motion and narrow widths
```

**1. Colors: use only the project's color system.** Locate the tokens: CSS custom
properties, a theme file, Tailwind configuration or design tokens. Map these roles:
background, raised surface, panel, inset/deep surface, text, muted, subtle,
primary/brand, accent, success, warning, danger, info and border.

- Never add hardcoded colors and never change the palette.
- Derive any extra shade from existing tokens, for example
  `color-mix(in srgb, var(--muted) 28%, transparent)`.
- Only when the project has no color system, start from
  [reference/fallback-palette.md](reference/fallback-palette.md) and record it as
  the project's tokens.

**2. Non-color tokens.** Add these alongside the color tokens:
- a pixel unit (`--px: 2px`);
- a radius of 0–2px;
- a frame color derived from the tokens;
- `--font-ui`, `--font-mono` and an optional `--font-pixel`;
- a quick transition time of about 100–150 ms.

**3–4. Components and layout.** Use the recipes in
[reference/components.md](reference/components.md):
- windows with stepped corner marks;
- a stepped menu cursor;
- framed buttons, fields and tabs;
- segmented HP/MP gauges and status pills.

Layout guidance:
- modular, clearly bounded panels;
- a vertical menu sidebar like an inventory or status screen;
- compact headers;
- thin separators;
- dense but legible information;
- responsive down to mobile with no horizontal page scroll.

**5. Icons and type.** Follow [reference/icons-and-type.md](reference/icons-and-type.md).
- Draw icons on a 16×16 or 24×24 grid.
- Generate an SVG sprite from ASCII grids:
  `python scripts/pixel_icons.py icons/ --out sprite.svg`.
- Use a pixel font only for short titles of about 15px and up.

**6. Verify, then fix and repeat.**
- Run `python scripts/check_colors.py <css-or-src-dir> --tokens <token-file>`.
  It lists every color literal outside the token file; resolve each one.
- Check contrast: at least 4.5:1 for text, 3:1 for large text, focus rings and
  control borders.
- Check visible keyboard focus and logical tab order.
- Check that `prefers-reduced-motion` removes nonessential motion.
- Check layouts at narrow width and at 200% zoom.

## Core rules

- **Identity:**
  - flat surfaces, rectangular windows and thin 1px frames;
  - depth comes from frames, layers and contrast, never from shadows or glow;
  - small geometric pixel ornaments only; no sprites or characters unless requested.
- **Selection:**
  - the selected item is unmistakable through fill, contrast and a small pixel cursor;
  - hover and focus use the same language, with immediate feedback.
- **Motion:**
  - brief and discreet: a fade or 2–8px slide in a few steps;
  - no continuous animation except a minimal loading or progress indicator;
  - honor reduced motion.
- **Data:**
  - gauges and progress show real values only;
  - unknown values show a neutral striped track, never an invented number;
  - status always uses words as well as color.
- **Typography:**
  - modern readable fonts for content and monospace for code and IDs;
  - pixel fonts never in paragraphs or small labels.
- **Consistency:**
  - reuse existing components and architecture;
  - centralize frames, spacing, type and interactive states;
  - apply the style everywhere instead of to isolated components.

## Avoid

- pixel art on every component, and large decorative sprites;
- interfaces that look only like a game menu;
- neon, heavy glow, glassmorphism, heavy shadows or noisy textures;
- thick borders, bulky buttons and hard-to-read pixel fonts;
- piles of fantasy ornaments;
- fictional data in real screens;
- any change to the existing palette.
