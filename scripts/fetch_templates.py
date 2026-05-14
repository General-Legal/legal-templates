"""
Fetch all .docx templates from https://general.legal/resources/library.

Scrapes the library index, follows each detail page to find its .docx
asset on the Webflow CDN, and downloads it into docx-originals/ named
after the library slug (e.g. business-associate-agreement-baa.docx).

Usage:
    python3 scripts/fetch_templates.py

Uses only the Python standard library, no external dependencies.
"""

import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

LIBRARY_URL = "https://general.legal/resources/library"
USER_AGENT = "legal-templates-fetcher/1.0 (+https://general.legal)"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def find_detail_paths(html):
    """Return ordered, deduplicated list of /library/<slug> paths."""
    paths = re.findall(r'href="(/library/[^"#?]+)"', html)
    seen = []
    for p in paths:
        if p not in seen:
            seen.append(p)
    return seen


def find_docx_url(html):
    """Return the first .docx URL on the page, or None."""
    m = re.search(r'https://[^"\']+\.docx', html)
    return m.group(0) if m else None


def slug_from_path(path):
    """`/library/foo-bar` -> `foo-bar`."""
    return path.rsplit("/", 1)[-1]


def main():
    root = Path(__file__).resolve().parent.parent
    dest_dir = root / "docx-originals"
    dest_dir.mkdir(parents=True, exist_ok=True)

    print(f"Fetching library index: {LIBRARY_URL}")
    index_html = fetch(LIBRARY_URL).decode("utf-8", errors="replace")
    paths = find_detail_paths(index_html)
    if not paths:
        print("No /library/<slug> links found on the index page.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(paths)} templates.\n")

    downloaded = 0
    failed = []
    for path in paths:
        slug = slug_from_path(path)
        detail_url = urljoin(LIBRARY_URL, path)
        print(f"- {slug}")
        try:
            detail_html = fetch(detail_url).decode("utf-8", errors="replace")
        except Exception as e:
            print(f"    detail page failed: {e}")
            failed.append(slug)
            continue

        docx_url = find_docx_url(detail_html)
        if not docx_url:
            print("    no .docx link on detail page")
            failed.append(slug)
            continue

        try:
            data = fetch(docx_url)
        except Exception as e:
            print(f"    download failed: {e}")
            failed.append(slug)
            continue

        out = dest_dir / f"{slug}.docx"
        out.write_bytes(data)
        print(f"    -> {out.relative_to(root)} ({len(data):,} bytes)")
        downloaded += 1

    print(f"\nDownloaded {downloaded}/{len(paths)} templates.")
    if failed:
        print(f"Failed: {', '.join(failed)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
