"""Validate this repository as a Claude skill plugin and marketplace before publishing.

Checks the documented rules that can be verified offline:
- every skills/<name>/SKILL.md has YAML frontmatter with `name` and `description`;
- `name`: at most 64 characters, lowercase letters/digits/hyphens, matches the
  folder, no reserved words ("anthropic", "claude"), no XML tags;
- `description`: non-empty, at most 1024 characters, no XML tags, third person
  (does not start with "I " or "You ");
- the SKILL.md body stays under 500 lines and every relative link resolves and
  stays one level deep (links only from SKILL.md, not between reference files);
- .claude-plugin/plugin.json has a kebab-case `name` and the recommended fields;
- .claude-plugin/marketplace.json has `name`, `owner.name` and plugin entries whose
  names match plugin.json and whose relative sources exist without "..".

Usage: python tools/validate_skill.py [REPO_ROOT]   (exit 0 = valid, 1 = problems)
"""
import json
import re
import sys
from pathlib import Path

NAME = re.compile(r'[a-z0-9]+(?:-[a-z0-9]+)*\Z')
RESERVED = ('anthropic', 'claude')
XML = re.compile(r'<[A-Za-z/][^>]*>')
LINK = re.compile(r'\]\(([^)#\s]+)(?:#[^)]*)?\)')
FENCE = re.compile(r'^(```|~~~).*?^\1', re.MULTILINE | re.DOTALL)


def prose(text):
    """Markdown without fenced code blocks, whose example links are not references."""
    return FENCE.sub('', text)
MAX_BODY_LINES = 500


def frontmatter(text):
    """Return ({key: value}, body) for simple `key: value` YAML frontmatter."""
    if not text.startswith('---\n'):
        raise ValueError('SKILL.md must start with YAML frontmatter (---)')
    end = text.find('\n---\n', 4)
    if end < 0:
        raise ValueError('frontmatter is not closed with ---')
    fields = {}
    for line in text[4:end].splitlines():
        if line.strip() and not line.startswith(' '):
            key, _, value = line.partition(':')
            fields[key.strip()] = value.strip().strip('"\'')
    return fields, text[end + 5:]


def check_skill(folder, problems):
    path = folder / 'SKILL.md'
    try:
        fields, body = frontmatter(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as error:
        problems.append(f'{path}: {error}')
        return
    name, description = fields.get('name', ''), fields.get('description', '')
    if not NAME.match(name) or len(name) > 64:
        problems.append(f'{path}: name must be 1-64 lowercase letters, digits and hyphens')
    if name != folder.name:
        problems.append(f'{path}: name "{name}" must match its folder "{folder.name}"')
    if any(word in name for word in RESERVED):
        problems.append(f'{path}: name must not contain reserved words {RESERVED}')
    if not description or len(description) > 1024:
        problems.append(f'{path}: description must be 1-1024 characters (has {len(description)})')
    if XML.search(name + description):
        problems.append(f'{path}: name and description must not contain XML tags')
    if re.match(r'(I|You)\b', description):
        problems.append(f'{path}: write the description in third person')
    if 'use when' not in description.lower():
        problems.append(f'{path}: description should say when to use the skill ("Use when ...")')
    if len(body.splitlines()) >= MAX_BODY_LINES:
        problems.append(f'{path}: body has {len(body.splitlines())} lines; keep it under {MAX_BODY_LINES}')
    for target in LINK.findall(prose(body)):
        if re.match(r'[a-z]+:', target):
            continue
        if '\\' in target or target.startswith('/'):
            problems.append(f'{path}: use relative forward-slash links: {target}')
        elif not (folder / target).exists():
            problems.append(f'{path}: linked file does not exist: {target}')
    for reference in folder.rglob('*.md'):
        if reference.name == 'SKILL.md':
            continue
        text = reference.read_text(encoding='utf-8')
        if any(not re.match(r'[a-z]+:', target) and target.endswith('.md') for target in LINK.findall(prose(text))):
            problems.append(f'{reference}: keep references one level deep; link files only from SKILL.md')
        if len(text.splitlines()) > 100 and '## Contents' not in text:
            problems.append(f'{reference}: files over 100 lines need a "## Contents" section')


def check_plugin(root, problems):
    manifest_path = root / '.claude-plugin/plugin.json'
    try:
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as error:
        problems.append(f'{manifest_path}: {error}')
        return None
    name = manifest.get('name', '')
    if not NAME.match(name):
        problems.append(f'{manifest_path}: name must be kebab-case')
    if name.startswith(tuple(word + '-' for word in RESERVED)) or name in RESERVED:
        problems.append(f'{manifest_path}: name is reserved for official plugins')
    for field in ('version', 'description', 'author', 'license'):
        if not manifest.get(field):
            problems.append(f'{manifest_path}: add "{field}"')
    if not (manifest.get('author') or {}).get('name'):
        problems.append(f'{manifest_path}: author.name is required')
    return name


def check_marketplace(root, plugin_name, problems):
    path = root / '.claude-plugin/marketplace.json'
    if not path.exists():
        return
    try:
        market = json.loads(path.read_text(encoding='utf-8'))
    except ValueError as error:
        problems.append(f'{path}: {error}')
        return
    if not NAME.match(market.get('name', '')):
        problems.append(f'{path}: marketplace name must be kebab-case')
    if not (market.get('owner') or {}).get('name'):
        problems.append(f'{path}: owner.name is required')
    entries = market.get('plugins') or []
    if not entries:
        problems.append(f'{path}: list at least one plugin')
    for entry in entries:
        source = entry.get('source')
        if entry.get('name') != plugin_name:
            problems.append(f'{path}: entry name "{entry.get("name")}" must equal plugin.json name "{plugin_name}"')
        if isinstance(source, str):
            if '..' in source or not source.startswith('./'):
                problems.append(f'{path}: relative source must start with ./ and not contain ..')
            elif not (root / source).exists():
                problems.append(f'{path}: source path does not exist: {source}')


def main(argv=None):
    root = Path((argv or sys.argv[1:] or ['.'])[0]).resolve()
    problems = []
    skills = sorted(path.parent for path in (root / 'skills').glob('*/SKILL.md'))
    if not skills:
        problems.append(f'{root}: no skills/<name>/SKILL.md found')
    for folder in skills:
        check_skill(folder, problems)
    plugin_name = check_plugin(root, problems)
    check_marketplace(root, plugin_name, problems)
    for problem in problems:
        print(problem)
    print('valid' if not problems else f'{len(problems)} problem(s)')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
