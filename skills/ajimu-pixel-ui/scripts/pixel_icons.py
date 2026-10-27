"""Build an SVG sprite of pixel icons from ASCII grids.

Each input file is one icon: rows of `#` (filled) and `.` (empty) of equal length,
for example 16x16. The file name without extension becomes the symbol id
`i-<name>`. Filled runs on a row become one rectangle path segment, so the output
stays small and pixel-exact (render it with `shape-rendering: crispEdges`).

Usage:
    python pixel_icons.py ICON_DIR [--out sprite.svg] [--prefix i-]

Exit status is 1 with a precise message when a grid is ragged, empty or contains
characters other than `#` and `.`; no partial sprite is written in that case.
"""
import argparse
import re
import sys
from pathlib import Path

FILLED, EMPTY = '#', '.'
NAME = re.compile(r'[a-z0-9][a-z0-9-]*\Z')


def grid_path(text, source):
    """Return SVG path data and (width, height) for one ASCII grid."""
    rows = [line.rstrip('\r') for line in text.strip('\n').split('\n')]
    if not rows or not rows[0]:
        raise ValueError(f'{source}: the grid is empty')
    width = len(rows[0])
    commands = []
    for number, row in enumerate(rows):
        if len(row) != width:
            raise ValueError(f'{source}:{number + 1}: row has {len(row)} cells, expected {width}')
        unknown = set(row) - {FILLED, EMPTY}
        if unknown:
            raise ValueError(f'{source}:{number + 1}: unexpected characters {sorted(unknown)}; use "#" and "."')
        x = 0
        while x < width:
            if row[x] == FILLED:
                start = x
                while x < width and row[x] == FILLED:
                    x += 1
                commands.append(f'M{start} {number}h{x - start}v1h-{x - start}z')
            else:
                x += 1
    return ''.join(commands), (width, len(rows))


def build_sprite(directory, prefix='i-'):
    """Return the sprite markup for every *.txt grid in `directory`, sorted by name."""
    files = sorted(Path(directory).glob('*.txt'))
    if not files:
        raise ValueError(f'{directory}: no .txt icon grids found')
    symbols = []
    for path in files:
        name = path.stem.lower()
        if not NAME.match(name):
            raise ValueError(f'{path}: use lowercase letters, digits and hyphens in icon file names')
        data, (width, height) = grid_path(path.read_text(encoding='utf-8'), path)
        symbols.append(f'<symbol id="{prefix}{name}" viewBox="0 0 {width} {height}"><path d="{data}"/></symbol>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true">'
            + ''.join(symbols) + '</svg>\n')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('directory', help='folder of .txt icon grids')
    parser.add_argument('--out', help='output file (default: print to stdout)')
    parser.add_argument('--prefix', default='i-', help='symbol id prefix (default: i-)')
    args = parser.parse_args(argv)
    try:
        sprite = build_sprite(args.directory, args.prefix)
    except (OSError, ValueError) as error:
        print(f'error: {error}', file=sys.stderr)
        return 1
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(sprite, encoding='utf-8', newline='\n')
        print(f'wrote {sprite.count("<symbol")} icons to {args.out}')
    else:
        sys.stdout.write(sprite)
    return 0


if __name__ == '__main__':
    sys.exit(main())
