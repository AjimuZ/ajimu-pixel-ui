"""Report color literals used outside the project's token definitions.

The Minimal Pixel JRPG style allows colors only through the project's existing
tokens. This check scans style and component sources for hex, rgb()/rgba(),
hsl()/hsla() and named-color literals and prints each occurrence that is not in an
allowed token file, so every one can be replaced by a token reference.

Usage:
    python check_colors.py PATH [PATH ...] [--tokens FILE ...]

PATH may be a file or a directory (scanned recursively for .css .scss .less .sass
.html .vue .svelte .jsx .tsx .js .ts). Files named with --tokens are where
literals are expected and are skipped. Exit status: 0 when clean, 1 when literals
were found, 2 for usage errors.
"""
import argparse
import re
import sys
from pathlib import Path

EXTENSIONS = {'.css', '.scss', '.less', '.sass', '.html', '.vue', '.svelte', '.jsx', '.tsx', '.js', '.ts'}
SKIP_DIRS = {'node_modules', '.git', 'dist', 'build', '.next', 'coverage', 'vendor'}
# Hex colors must not be part of identifiers or URLs; functions are matched by name.
LITERAL = re.compile(r'(?<![\w&/-])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b|\b(?:rgba?|hsla?)\(')
# A deliberately short list of named colors that appear in real styling mistakes.
NAMED = re.compile(r':\s*(?:white|black|red|green|blue|gray|grey|orange|yellow|purple|pink)\b\s*[;!}]', re.I)
# Declarations that define custom properties are token definitions, not usages.
TOKEN_DEFINITION = re.compile(r'^\s*--[\w-]+\s*:')


def candidates(paths, tokens):
    for path in paths:
        if path.is_file():
            if path.resolve() not in tokens:
                yield path
            continue
        for child in sorted(path.rglob('*')):
            if (child.is_file() and child.suffix in EXTENSIONS and child.resolve() not in tokens
                    and not any(part in SKIP_DIRS for part in child.parts)):
                yield child


def scan(file):
    findings = []
    try:
        lines = file.read_text(encoding='utf-8').splitlines()
    except (OSError, UnicodeDecodeError):
        return [(0, 'file could not be read as UTF-8 text; check it manually')]
    for number, line in enumerate(lines, 1):
        if TOKEN_DEFINITION.match(line):
            continue
        for match in list(LITERAL.finditer(line)) + list(NAMED.finditer(line)):
            findings.append((number, match.group(0).strip(': ;!}')))
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('paths', nargs='+', type=Path)
    parser.add_argument('--tokens', nargs='*', type=Path, default=[], help='files that define the color tokens')
    args = parser.parse_args(argv)
    missing = [str(path) for path in args.paths + args.tokens if not path.exists()]
    if missing:
        print('error: not found: ' + ', '.join(missing), file=sys.stderr)
        return 2
    tokens = {path.resolve() for path in args.tokens}
    total = 0
    for file in candidates(args.paths, tokens):
        for number, literal in scan(file):
            total += 1
            print(f'{file}:{number}: color literal {literal!r} - replace it with a token')
    print('clean: no color literals outside token definitions' if not total else f'{total} literal(s) found')
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main())
