"""Tests for guard_paths.py. Run: python3 .github/scripts/test_guard_paths.py"""
import pathlib, sys, unittest
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from guard_paths import infra_changes, offending, parse_log

TOM = "10145413+tomvonheill@users.noreply.github.com"
KENNEN = "kennen@example.com"
OWNERS = {TOM}


class Guard(unittest.TestCase):
    def test_content_and_pages_are_allowed(self):
        self.assertEqual(infra_changes([
            "src/pages/index.astro", "src/content/insights/a/index.md", "src/styles/global.css",
            "public/images/x.jpg", "CLAUDE.md", "README.md",
        ]), [])

    def test_infra_paths_are_flagged(self):
        files = [".github/workflows/check.yml", "package.json", "package-lock.json",
                 "astro.config.mjs", "tsconfig.json", ".nvmrc", "public/admin/config.yml"]
        self.assertEqual(infra_changes(files), files)

    def test_lookalikes_are_not_flagged(self):
        self.assertEqual(infra_changes(["src/package.json.md", "public/administration.html"]), [])


class PerCommit(unittest.TestCase):
    def test_tom_infra_commit_allowed(self):
        self.assertEqual(offending([("a1", TOM, ["package.json", ".nvmrc"])], OWNERS), [])

    def test_kennen_content_commit_allowed(self):
        self.assertEqual(offending([("b2", KENNEN, ["src/pages/index.astro"])], OWNERS), [])

    def test_kennen_infra_commit_flagged_with_only_infra_paths(self):
        commits = [
            ("a1", TOM, ["package.json"]),
            ("b2", KENNEN, ["src/pages/index.astro", "public/admin/config.yml", ".github/x.yml"]),
        ]
        self.assertEqual(offending(commits, OWNERS),
                         [("b2", KENNEN, ["public/admin/config.yml", ".github/x.yml"])])

    def test_empty(self):
        self.assertEqual(offending([], OWNERS), [])

    def test_parse_log(self):
        text = ("\x00aaa111\t" + TOM + "\n\npackage.json\nsrc/a.astro\n"
                "\x00bbb222\t" + KENNEN + "\n\npublic/admin/config.yml\n"
                "\x00ccc333\t" + KENNEN + "\n")
        self.assertEqual(parse_log(text), [
            ("aaa111", TOM, ["package.json", "src/a.astro"]),
            ("bbb222", KENNEN, ["public/admin/config.yml"]),
            ("ccc333", KENNEN, []),
        ])


if __name__ == "__main__":
    unittest.main()
