"""Tests for guard_paths.py. Run: python3 .github/scripts/test_guard_paths.py"""
import pathlib, sys, unittest
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from guard_paths import infra_changes, offending

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
                 "astro.config.mjs", "tsconfig.json", ".nvmrc", "public/admin/config.yml", "scripts/check-dist.ts"]
        self.assertEqual(infra_changes(files), files)

    def test_lookalikes_are_not_flagged(self):
        self.assertEqual(infra_changes(["src/package.json.md", "public/administration.html"]), [])


class NetChange(unittest.TestCase):
    """offending(net_paths, last_author, owners): net_paths come from the net diff of the range."""

    def test_kennen_changes_package_json_flagged(self):
        self.assertEqual(offending(["package.json"], {"package.json": KENNEN}, OWNERS),
                         [("package.json", KENNEN)])

    def test_changed_then_reverted_is_not_in_net_diff_so_passes(self):
        net = infra_changes([])  # revert: git diff A...B lists nothing
        self.assertEqual(offending(net, {}, OWNERS), [])

    def test_tom_edits_after_kennen_passes(self):
        self.assertEqual(offending(["package.json"], {"package.json": TOM}, OWNERS), [])

    def test_tom_change_passes(self):
        self.assertEqual(offending([".nvmrc"], {".nvmrc": TOM}, OWNERS), [])

    def test_content_only_passes(self):
        net = infra_changes(["src/pages/index.astro"])
        self.assertEqual(offending(net, {}, OWNERS), [])

    def test_only_nonowner_paths_reported(self):
        got = offending(["package.json", "scripts/x.ts"], {"package.json": TOM, "scripts/x.ts": KENNEN}, OWNERS)
        self.assertEqual(got, [("scripts/x.ts", KENNEN)])

    def test_scripts_dir_is_infra(self):
        self.assertEqual(infra_changes(["scripts/check-dist.ts"]), ["scripts/check-dist.ts"])


if __name__ == "__main__":
    unittest.main()
