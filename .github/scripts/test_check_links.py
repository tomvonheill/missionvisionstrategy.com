"""Tests for check_links.py. Run: python3 .github/scripts/test_check_links.py"""
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).with_name("check_links.py")


def run(files):
    with tempfile.TemporaryDirectory() as d:
        root = pathlib.Path(d)
        for name, body in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body)
        return subprocess.run([sys.executable, SCRIPT, root], capture_output=True, text=True)


class CheckLinks(unittest.TestCase):
    def test_valid_internal_links_pass(self):
        r = run({
            "index.html": '<a href="about.html#team">x</a><link href="styles.css"><img src="images/a.svg">'
                          '<a href="./">home</a><a href="sub/">sub</a>',
            "about.html": "", "styles.css": "", "images/a.svg": "", "sub/index.html": "",
        })
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_external_and_special_links_ignored(self):
        r = run({"index.html": '<a href="https://example.com/x">x</a><a href="mailto:a@b.c">m</a>'
                               '<a href="tel:123">t</a><a href="#top">t</a><a href="//cdn.x/y.js">y</a>'})
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_missing_file_fails_and_names_it(self):
        r = run({"index.html": '<a href="servces.html">typo</a>'})
        self.assertEqual(r.returncode, 1)
        self.assertIn("index.html", r.stdout)
        self.assertIn("servces.html", r.stdout)

    def test_link_escaping_site_root_fails(self):
        r = run({"index.html": '<img src="../secret.png">'})
        self.assertEqual(r.returncode, 1)


if __name__ == "__main__":
    unittest.main()
