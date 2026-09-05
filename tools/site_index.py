#!/usr/bin/env python3
"""Write book/sitemap.xml and book/llms.txt from src/SUMMARY.md. Run after
`mdbook build`; tools/deploy.sh runs it beside llms_full.py.

sitemap.xml — every page of the book at its published URL, with the date of
the last commit that touched its source, so a search engine crawls the
150-odd pages without discovering them one link at a time (mdBook writes no
sitemap; src/robots.txt points here).

llms.txt — the index form of https://llmstxt.org: the book on one screen,
one line per page carrying the scenario from the page's verified line, for
an agent deciding what to fetch. book/llms-full.txt (tools/llms_full.py) is
the whole corpus in one file.
"""
import os
import re
import subprocess
import sys
from datetime import date

HERE = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SRC, BOOK = os.path.join(HERE, "src"), os.path.join(HERE, "book")
SITE = "https://minecraftdocs.dev"

if not os.path.isdir(BOOK):
    sys.exit("run mdbook build first")


def html_url(md: str) -> str:
    """The page's canonical live URL. mdBook publishes README.md as index.html
    and every other page as .html, but Cloudflare Pages serves clean URLs and
    answers the .html form with a 308 to the extension-less one, so an index
    that listed .html addresses would be an index of redirects."""
    if os.path.basename(md) == "README.md":
        return f"{SITE}/{md[:-len('README.md')]}"
    return f"{SITE}/{md[:-3]}"


def lastmod(md: str) -> str:
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", os.path.join("src", md)],
            cwd=HERE, capture_output=True, text=True, check=True).stdout.strip()
        return out or date.today().isoformat()
    except (OSError, subprocess.CalledProcessError):
        return date.today().isoformat()


MARKUP = re.compile(r"\*\*|`|\[([^\]]*)\]\([^)]*\)")


def scenario(md: str) -> str:
    """The last ' · ' segment of the page's verified line (the scenario), plain text."""
    lines: list[str] = []
    with open(os.path.join(SRC, md), encoding="utf-8") as fh:
        for line in fh:
            if lines:
                if line.startswith(">"):
                    lines.append(line[1:].strip())
                    continue
                break
            if line.startswith("> Verified against"):
                lines.append(line[1:].strip())
    if not lines:
        return ""
    text = " ".join(lines)
    text = MARKUP.sub(lambda m: m.group(1) or "", text)
    parts = [p.strip() for p in text.split(" · ")]
    return parts[-1].rstrip(".") if len(parts) > 1 else ""


# --- SUMMARY.md: sections (H1 lines) and pages, with their nesting ------------
with open(os.path.join(SRC, "SUMMARY.md"), encoding="utf-8") as fh:
    summary = fh.read().splitlines()

LINK = re.compile(r"^(\s*)- \[([^\]]+)\]\(([^)]+\.md)\)")
PREFIX = re.compile(r"^\[([^\]]+)\]\(([^)]+\.md)\)")
entries: list[tuple[str, int, str, str]] = []  # (section, depth, title, md)
section = "Introduction"
for line in summary:
    if line.startswith("# "):
        # The file's own title ("# Summary") is not a section; the H1s below it are.
        section = line[2:].strip() if line.strip() != "# Summary" else section
        continue
    m = PREFIX.match(line)
    if m:
        entries.append((section, 0, m.group(1), m.group(2)))
        continue
    m = LINK.match(line)
    if m:
        entries.append((section, len(m.group(1)) // 2, m.group(2), m.group(3)))

# --- sitemap.xml --------------------------------------------------------------
rows = [f"  <url><loc>{SITE}/</loc><lastmod>{lastmod('introduction.md')}</lastmod></url>"]
for _, _, _, md in entries:
    rows.append(f"  <url><loc>{html_url(md)}</loc><lastmod>{lastmod(md)}</lastmod></url>")
sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(rows) + "\n</urlset>\n")
with open(os.path.join(BOOK, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write(sitemap)

# --- llms.txt -----------------------------------------------------------------
out = ["# How Java Minecraft Works", "",
       "> System-level documentation of the current Java Minecraft codebase, 26.2, "
       "written as the notes for a video lecture series: names, never code. One page "
       "per lecture, each following one scenario through the system, with a diagram "
       "whose lanes are class names.", "",
       "Every backticked identifier on every page exists in the 26.2 decompile (checked "
       "before the site publishes), and every claim has been fact-checked against the "
       "decompile twice. The writing is CC BY-SA 4.0; it describes the game and contains "
       f"none of it. The whole book in one file: {SITE}/llms-full.txt", ""]
current = None
part = None
for sec, depth, title, md in entries:
    # Under Systems, each part (a depth-0 entry, its landing page) is its own
    # section and its pages list under it; every other section lists as it is.
    if sec == "Systems" and depth == 0:
        part = title
    heading = f"Systems — {part}" if sec == "Systems" else sec
    if heading != current:
        out += ([""] if out and out[-1] != "" else []) + [f"## {heading}", ""]
        current = heading
    desc = scenario(md)
    out.append(f"- [{title}]({html_url(md)})" + (f": {desc}" if desc else ""))
text = "\n".join(out) + "\n"
with open(os.path.join(BOOK, "llms.txt"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write(text)

print(f"wrote book/sitemap.xml ({len(rows)} urls) and book/llms.txt ({len(entries)} pages)")
