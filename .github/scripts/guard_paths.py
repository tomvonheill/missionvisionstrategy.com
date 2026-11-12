"""Fail if the net change in a range touches infrastructure paths last changed by someone other than Tom.

Usage: python3 .github/scripts/guard_paths.py <A..B>   (e.g. origin/main..origin/dev)
Judges the NET change (git diff A...B), so a revert clears the guard. For each infrastructure path in
that diff, the responsible author is the author of the most recent commit in the range touching it
(--cc, so edits made inside merge commits count). Paths whose responsible author is not an owner fail.
This is a guardrail (author emails are self-declared), not a security boundary.
"""
import subprocess
import sys

INFRA_PREFIXES = (".github/", "public/admin/", "scripts/")
INFRA_FILES = {"package.json", "package-lock.json", "astro.config.mjs", "tsconfig.json", ".nvmrc"}
OWNERS = {"10145413+tomvonheill@users.noreply.github.com"}


def infra_changes(paths):
    return [p for p in paths if p in INFRA_FILES or p.startswith(INFRA_PREFIXES)]


def offending(net_paths, last_author, owners):
    """net_paths: infra paths in the net diff; last_author: path -> email -> [(path, email)] for non-owners."""
    return [(p, last_author.get(p, "unknown")) for p in net_paths if last_author.get(p) not in owners]


def git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def main():
    if len(sys.argv) != 2 or ".." not in sys.argv[1]:
        sys.exit("usage: guard_paths.py <A..B>")
    rng = sys.argv[1]
    base, _, head = rng.partition("..")
    net = infra_changes(git("diff", "--name-only", f"{base}...{head}").splitlines())
    last = {p: git("log", "-1", "-s", "--cc", "--format=%ae", rng, "--", p).strip() for p in net}
    bad = offending(net, last, OWNERS)
    for path, email in bad:
        print(f"::error file={path}::{path} is infrastructure that only Tom changes "
              f"(last changed by {email}). Revert that change on dev, or ask Tom.")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
