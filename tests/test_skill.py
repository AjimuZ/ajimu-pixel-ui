"""Offline checks for the skill package and its utility scripts."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills/ajimu-pixel-ui/scripts'


def run(*args):
    return subprocess.run([sys.executable, *map(str, args)], capture_output=True, text=True)


class PackageTests(unittest.TestCase):
    def test_repository_is_a_valid_skill_plugin(self):
        result = run(ROOT / 'tools/validate_skill.py', ROOT)
        self.assertEqual(0, result.returncode, result.stdout)


class PixelIconTests(unittest.TestCase):
    def test_grids_become_a_sprite_of_exact_runs(self):
        with tempfile.TemporaryDirectory() as folder:
            Path(folder, 'dot.txt').write_text('..\n.#\n', encoding='utf-8')
            result = run(SCRIPTS / 'pixel_icons.py', folder)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn('<symbol id="i-dot" viewBox="0 0 2 2"><path d="M1 1h1v1h-1z"/></symbol>', result.stdout)

    def test_ragged_grids_are_rejected_with_their_line(self):
        with tempfile.TemporaryDirectory() as folder:
            Path(folder, 'bad.txt').write_text('##\n#\n', encoding='utf-8')
            result = run(SCRIPTS / 'pixel_icons.py', folder)
            self.assertEqual(1, result.returncode)
            self.assertIn('bad.txt:2', result.stderr)


class ColorCheckTests(unittest.TestCase):
    def test_literals_outside_tokens_are_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            tokens = Path(folder, 'tokens.css')
            tokens.write_text(':root { --brand: #d46c7f; }\n', encoding='utf-8')
            styles = Path(folder, 'app.css')
            styles.write_text('.a { color: var(--brand); }\n.b { color: #fff; }\n.c { background: rgba(0,0,0,.4); }\n', encoding='utf-8')
            result = run(SCRIPTS / 'check_colors.py', folder, '--tokens', tokens)
            self.assertEqual(1, result.returncode)
            self.assertIn('app.css:2', result.stdout)
            self.assertIn('app.css:3', result.stdout)
            self.assertNotIn('tokens.css', result.stdout)

    def test_clean_sources_pass(self):
        with tempfile.TemporaryDirectory() as folder:
            Path(folder, 'app.css').write_text(':root {\n  --text: #f7e6ea;\n}\n.a { color: var(--text); }\n', encoding='utf-8')
            result = run(SCRIPTS / 'check_colors.py', folder)
            self.assertEqual(0, result.returncode, result.stdout)


if __name__ == '__main__':
    unittest.main()
