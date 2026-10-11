"""Write sitemap.xml for the assembled Puzzle Factories site.

Usage: python tools/sitemap.py SITE_DIR BASE_URL

Lists every .html page under SITE_DIR (the combined artifact the deploy
workflow builds: the landing page plus each project's index and puzzle
pages), so the sitemap always matches what is actually published,
including each day's new puzzles. index.html pages are listed by their
directory address, which is the one the site links to.
"""

import sys
from pathlib import Path
from xml.sax.saxutils import escape


def page_urls(site_dir: Path, base_url: str) -> list[str]:
    base = base_url.rstrip("/") + "/"
    paths = []
    for page in site_dir.rglob("*.html"):
        rel = page.relative_to(site_dir).as_posix()
        if rel == "index.html":
            rel = ""
        elif rel.endswith("/index.html"):
            rel = rel[: -len("index.html")]
        paths.append(rel)
    # Landing page first, then each project's index before its puzzles.
    paths.sort(key=lambda p: (p.count("/"), p))
    return [base + p for p in paths]


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__.strip().splitlines()[2])
    site_dir, base_url = Path(sys.argv[1]), sys.argv[2]
    urls = page_urls(site_dir, base_url)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    lines += [f"  <url><loc>{escape(u)}</loc></url>" for u in urls]
    lines.append("</urlset>")
    (site_dir / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote sitemap.xml ({len(urls)} pages)")


if __name__ == "__main__":
    main()
