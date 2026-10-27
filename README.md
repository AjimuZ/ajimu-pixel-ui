# Ajimu Pixel UI

A Claude skill for the **Minimal Pixel JRPG** design system. It produces modern,
readable interfaces with a subtle 16-bit role-playing-game menu identity:
framed windows, a pixel menu cursor, segmented HP/MP gauges and crisp pixel
icons. It is built only from the colors your project already defines.

> 80% modern minimal application, 20% pixel JRPG identity. Readability always
> wins over retro fidelity.

It is made for products that are not games: developer tools, dashboards,
editors, admin panels and productivity apps.

## What it gives Claude

- **A six-step workflow:**
  1. map the existing color tokens;
  2. add non-color tokens;
  3. build the shared primitives;
  4. lay out pages and navigation;
  5. add icons and type;
  6. verify.
- **Component recipes** in token-only CSS: window with stepped corner marks,
  stepped menu cursor, buttons, fields, tabs, segmented gauges, status pills,
  activity line and reduced motion.
- **Guidance for pixel icons and typography,** including when a pixel font is
  appropriate (short titles of 15px and up only) and how to bundle one legally.
- **Two scripts:**
  - `pixel_icons.py` turns ASCII grids into an SVG sprite;
  - `check_colors.py` lists every color literal outside your token files.
- **A fallback palette,** used only when a project has no color system yet.

## Install

### Claude Code (plugin)

```bash
claude plugin marketplace add AjimuZ/ajimu-pixel-ui
claude plugin install ajimu-pixel-ui@ajimu-pixel-ui
```

Inside a session you can use `/plugin marketplace add AjimuZ/ajimu-pixel-ui`
instead. Claude loads the skill when a task matches its description. You can also
invoke it directly as `/ajimu-pixel-ui:ajimu-pixel-ui`.

### Claude Code (personal or project skill)

Copy the skill folder into your skills directory:

```bash
git clone https://github.com/AjimuZ/ajimu-pixel-ui
cp -r ajimu-pixel-ui/skills/ajimu-pixel-ui ~/.claude/skills/         # personal
cp -r ajimu-pixel-ui/skills/ajimu-pixel-ui .claude/skills/           # one project
```

### Claude apps

Zip the `skills/ajimu-pixel-ui` folder and upload it as a custom skill in your
Claude settings.

## Use

Ask for the style directly, for example "Restyle the settings page in a
minimal pixel JRPG style", or apply it to a new interface. The skill reads your
existing tokens first and never introduces new colors.

The scripts need Python 3.9 or later and no packages:

```bash
python skills/ajimu-pixel-ui/scripts/pixel_icons.py icons/ --out assets/sprite.svg
python skills/ajimu-pixel-ui/scripts/check_colors.py src/ --tokens src/styles/tokens.css
```

## Develop

```bash
python tools/validate_skill.py .        # frontmatter, length, links, plugin and marketplace
python -m unittest discover -s tests    # validator and script tests
```

## License

MIT © Azim Ben Othman. See [LICENSE](LICENSE).
