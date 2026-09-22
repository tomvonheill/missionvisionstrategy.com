"""Fail if any internal href/src in the site points at a file that doesn't exist.

Usage: python3 .github/scripts/check_links.py site
External URLs, mailto:, tel:, and same-page #anchors are skipped.
"""
import html.parser
import pathlib
import sys
import urllib.parse

SKIP_PREFIXES = ("http://", "https://", "//", "mailto:", "tel:", "#", "data:")


class Refs(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("href", "src") and value:
                self.refs.append(value.strip())


def broken_refs(root):
    root = root.resolve()
    for page in sorted(root.rglob("*.html")):
        parser = Refs()
        parser.feed(page.read_text(encoding="utf-8"))
        for ref in parser.refs:
            if ref.startswith(SKIP_PREFIXES):
                continue
            path = urllib.parse.unquote(urllib.parse.urlsplit(ref).path)
            target = (root / path.lstrip("/")) if path.startswith("/") else (page.parent / path)
            if ref.endswith("/") or path in ("", ".", "./"):
                target = target / "index.html"
            target = target.resolve()
            if not target.is_relative_to(root) or not target.is_file():
                yield page.relative_to(root), ref


def main():
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "site")
    broken = list(broken_refs(root))
    for page, ref in broken:
        print(f"{root / page}: broken link -> {ref}")
    if broken:
        print(f"\n{len(broken)} broken link(s). Fix the path or add the missing file.")
        sys.exit(1)
    print("All internal links resolve.")


if __name__ == "__main__":
    main()
