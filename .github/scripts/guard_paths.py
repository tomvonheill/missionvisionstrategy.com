"""Fail if a commit by someone other than Tom touches infrastructure paths.

Usage: python3 .github/scripts/guard_paths.py <git-log-range>   (e.g. origin/main..origin/dev)
Each commit is judged by its author email (merges list only files differing from every parent), so Tom's own infra commits
pass even when they sit in a range that Kennen publishes.
"""
import subprocess
import sys

INFRA_PREFIXES = (".github/", "public/admin/")
INFRA_FILES = {"package.json", "package-lock.json", "astro.config.mjs", "tsconfig.json", ".nvmrc"}
OWNERS = {"10145413+tomvonheill@users.noreply.github.com"}


def infra_changes(paths):
    return [p for p in paths if p in INFRA_FILES or p.startswith(INFRA_PREFIXES)]


def offending(commits, owners):
    """commits: [(sha, author_email, [paths])] -> [(sha, email, infra_paths)] for non-owners."""
    out = []
    for sha, email, paths in commits:
        if email in owners:
            continue
        bad = infra_changes(paths)
        if bad:
            out.append((sha, email, bad))
    return out


def parse_log(text):
    """Parse `git log --format=%x00%H%x09%ae --name-only` output."""
    commits = []
    for chunk in text.split("\x00"):
        if not chunk.strip():
            continue
        head, _, rest = chunk.partition("\n")
        sha, _, email = head.partition("\t")
        commits.append((sha.strip(), email.strip(), [l.strip() for l in rest.splitlines() if l.strip()]))
    return commits


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: guard_paths.py <git-log-range>")
    log = subprocess.run(
        ["git", "log", "--cc", "--format=%x00%H%x09%ae", "--name-only", sys.argv[1]],
        check=True, capture_output=True, text=True).stdout
    bad = offending(parse_log(log), OWNERS)
    for sha, email, paths in bad:
        for p in paths:
            print(f"::error file={p}::{p} is infrastructure that only Tom changes "
                  f"(commit {sha[:7]} by {email}). Undo this change, or ask Tom.")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
