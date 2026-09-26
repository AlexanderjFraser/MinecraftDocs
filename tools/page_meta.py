#!/usr/bin/env python3
"""Rewrite the <head> of every built page so search engines, link unfurlers and
agents each get what they read. Run after `mdbook build`; tools/deploy.sh runs
it beside llms_full.py and md_twins.py.

mdBook gives every page the same description (book.toml's) and a title of the
form "page - book". Per page this tool sets:

  <title>            the page's own title and its part ("Entity lifecycle · Entities")
  description        the scenario from the page's verified line, else its first paragraph
  canonical          the clean URL Cloudflare Pages serves (no .html), one host
  alternate          the page's markdown twin (tools/md_twins.py), type text/markdown
  og:* / twitter:*   title, description, url and the site's image
  JSON-LD            TechArticle + BreadcrumbList; WebSite on the home page

`--check` fails if any built page lacks a canonical or shares its description
with another page (the state of the site before 2026-09-26). `--probe` proves
the check fails on a page that has neither.
"""
import html
import json
import os
import re
import subprocess
import sys
from datetime import date

HERE = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SRC, BOOK = os.path.join(HERE, "src"), os.path.join(HERE, "book")
SITE = "https://minecraftdocs.dev"
SITE_NAME = "How Java Minecraft Works"
AUTHOR = "Alexander Fraser"
IMAGE = f"{SITE}/og.png"
MAX_DESC = 170

# --- SUMMARY.md: every page with its section (part) --------------------------
LINK = re.compile(r"^(\s*)- \[([^\]]+)\]\(([^)]+\.md)\)")
PREFIX = re.compile(r"^\[([^\]]+)\]\(([^)]+\.md)\)")
PART = re.compile(r"^[IVX]+ · (.+)$")


def pages():
    """(md, title, part) for every page in SUMMARY order; part is the sidebar
    section a page sits under ("Entities" for a Part VI page, "Maps", "Reference")."""
    out, section, part = [], "", None
    with open(os.path.join(SRC, "SUMMARY.md"), encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("# ") and line.strip() != "# Summary":
                section, part = line[2:].strip(), None
                continue
            m = PREFIX.match(line)
            if m:
                out.append((m.group(2), m.group(1), ""))
                continue
            m = LINK.match(line)
            if not m:
                continue
            depth, title, md = len(m.group(1)) // 2, m.group(2), m.group(3)
            if section == "Systems" and depth == 0:
                pm = PART.match(title)
                part = pm.group(1) if pm else title
                out.append((md, part, SITE_NAME))
            else:
                out.append((md, title, part or section))
    return out


def url(md: str) -> str:
    if os.path.basename(md) == "README.md":
        return f"{SITE}/{md[:-len('README.md')]}"
    return f"{SITE}/{md[:-3]}"


def md_url(md: str) -> str:
    if os.path.basename(md) == "README.md":
        return f"{SITE}/{md[:-len('README.md')]}index.md"
    return f"{SITE}/{md}"


def html_path(md: str) -> str:
    if os.path.basename(md) == "README.md":
        return os.path.join(BOOK, os.path.dirname(md), "index.html")
    return os.path.join(BOOK, md[:-3] + ".html")


MARKUP = re.compile(r"\*\*|\*|`|<[^>]+>|\[([^\]]*)\]\([^)]*\)|\{\{#include [^}]*\}\}")


def plain(text: str) -> str:
    return re.sub(r"\s+", " ", MARKUP.sub(lambda m: m.group(1) or "", text)).strip()


def description(md: str) -> str:
    """The scenario segment of the verified line, else the first prose paragraph."""
    with open(os.path.join(SRC, md), encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    quote, i = [], 0
    while i < len(lines):
        if lines[i].startswith("> Verified against"):
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i][1:].strip())
                i += 1
            break
        i += 1
    if quote:
        parts = [p.strip() for p in plain(" ".join(quote)).split(" · ")]
        if len(parts) > 1 and parts[-1]:
            return clip(parts[-1])
    para, i = [], 0
    while i < len(lines):
        line = lines[i]
        if line.startswith(("#", ">", "|", "```", "<", "{{", "- ", "* ", "1. ")) or not line.strip():
            if para:
                break
            i += 1
            continue
        para.append(line.strip())
        i += 1
    return clip(plain(" ".join(para)))


def clip(text: str) -> str:
    text = text.rstrip(".") + "."
    if len(text) <= MAX_DESC:
        return text
    cut = text[:MAX_DESC].rsplit(" ", 1)[0].rstrip(",;:")
    return cut + "…"


def lastmod(md: str) -> str:
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", os.path.join("src", md)],
                             cwd=HERE, capture_output=True, text=True, check=True).stdout.strip()
        return out or date.today().isoformat()
    except (OSError, subprocess.CalledProcessError):
        return date.today().isoformat()


def a(s: str) -> str:
    return html.escape(s, quote=True)


TITLE = re.compile(r"<title>.*?</title>", re.S)
META_DESC = re.compile(r'\s*<meta name="description" content="[^"]*">')
OG_BLOCK = re.compile(r'\s*<meta (?:property="(?:og|twitter):[^"]*"|name="twitter:[^"]*") content="[^"]*">')
HEAD_END = re.compile(r"\n\s*</head>")


def rewrite(md: str, title: str, part: str, dry: bool = False, path: str = None, page_url: str = None) -> bool:
    path = path or html_path(md)
    if not os.path.exists(path):
        return False
    with open(path, encoding="utf-8") as fh:
        doc = fh.read()
    desc = description(md)
    page_url, twin = page_url or url(md), md_url(md)
    full_title = f"{title} · {part}" if part else title  # a part's landing page: "Entities · How Java Minecraft Works"
    if md == "introduction.md":
        full_title = f"{title} · {SITE_NAME}"
    crumbs = [{"@type": "ListItem", "position": 1, "name": SITE_NAME, "item": f"{SITE}/"}]
    if part and part != SITE_NAME:
        crumbs.append({"@type": "ListItem", "position": 2, "name": part})
    crumbs.append({"@type": "ListItem", "position": len(crumbs) + 1, "name": title, "item": page_url})
    ld = [{"@context": "https://schema.org", "@type": "TechArticle", "headline": title,
           "description": desc, "url": page_url, "dateModified": lastmod(md),
           "author": {"@type": "Person", "name": AUTHOR},
           "isPartOf": {"@type": "Book", "name": SITE_NAME, "url": f"{SITE}/"},
           "license": "https://creativecommons.org/licenses/by-sa/4.0/"},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": crumbs}]
    if md == "introduction.md":
        ld.append({"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME,
                   "alternateName": "MinecraftDocs", "url": f"{SITE}/"})
    block = "\n".join([
        f'        <meta name="description" content="{a(desc)}">',
        f'        <link rel="canonical" href="{page_url}">',
        f'        <link rel="alternate" type="text/markdown" href="{twin}" title="This page as markdown">',
        '        <meta property="og:type" content="article">',
        f'        <meta property="og:site_name" content="{SITE_NAME}">',
        f'        <meta property="og:title" content="{a(full_title)}">',
        f'        <meta property="og:description" content="{a(desc)}">',
        f'        <meta property="og:url" content="{page_url}">',
        f'        <meta property="og:image" content="{IMAGE}">',
        '        <meta property="og:image:width" content="1200">',
        '        <meta property="og:image:height" content="630">',
        '        <meta name="twitter:card" content="summary_large_image">',
        f'        <meta name="twitter:title" content="{a(full_title)}">',
        f'        <meta name="twitter:description" content="{a(desc)}">',
        f'        <meta name="twitter:image" content="{IMAGE}">',
        '        <script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>",
    ])
    new = TITLE.sub(f"<title>{a(full_title)}</title>", doc, count=1)
    new = META_DESC.sub("", new)
    new = OG_BLOCK.sub("", new)
    new = re.sub(r'\s*<link rel="canonical"[^>]*>|\s*<link rel="alternate" type="text/markdown"[^>]*>|\s*<script type="application/ld\+json">.*?</script>', "", new, flags=re.S)
    new, n = HEAD_END.subn("\n" + block + "\n    </head>", new, count=1)
    if n != 1:
        sys.exit(f"{path}: no </head>")
    if not dry and new != doc:
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(new)
    return True


def check(root: str = BOOK) -> list[str]:
    """Every built page has a canonical and a description no other page shares."""
    faults, seen = [], {}
    for dp, _, fn in os.walk(root):
        for f in fn:
            if not f.endswith(".html") or f in ("404.html", "print.html", "toc.html"):
                continue
            p = os.path.join(dp, f)
            with open(p, encoding="utf-8") as fh:
                head = fh.read().split("</head>", 1)[0]
            if 'http-equiv="refresh"' in head:
                continue  # a redirect stub from book.toml's [output.html.redirect]
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            if 'rel="canonical"' not in head:
                faults.append(f"{rel}: no canonical")
            m = re.search(r'<meta name="description" content="([^"]*)">', head)
            d = m.group(1) if m else ""
            if not d:
                faults.append(f"{rel}: no description")
            elif d in seen and {rel, seen[d]} != {"index.html", "introduction.html"}:
                faults.append(f"{rel}: description shared with {seen[d]}")
            else:
                seen[d] = rel
    return faults


def probe() -> None:
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        for name in ("a.html", "b.html"):
            with open(os.path.join(tmp, name), "w", encoding="utf-8") as fh:
                fh.write('<html><head><title>x</title><meta name="description" content="same"></head><body></body></html>')
        faults = check(tmp)
    want = {"a.html: no canonical", "b.html: no canonical", "b.html: description shared with a.html"}
    if set(faults) != want:
        sys.exit(f"probe FAILED: got {faults}")
    print("probe ok: the check fails on a page with no canonical and on a shared description")


if __name__ == "__main__":
    if "--probe" in sys.argv:
        probe()
        sys.exit()
    if "--check" in sys.argv:
        faults = check()
        for f in faults:
            print(f)
        sys.exit(1 if faults else 0)
    if not os.path.isdir(BOOK):
        sys.exit("run mdbook build first")
    n = 0
    for md, title, part in pages():
        # The introduction is also the home page (mdBook copies it to index.html),
        # so both copies carry the site root as their canonical URL.
        n += rewrite(md, title, part, dry="--dry" in sys.argv,
                     page_url=f"{SITE}/" if md == "introduction.md" else None)
    # mdBook copies the first chapter to book/index.html; it is the home page,
    # so it gets the introduction's metadata with the site root as its URL.
    rewrite("introduction.md", "Introduction", "", dry="--dry" in sys.argv,
            path=os.path.join(BOOK, "index.html"), page_url=f"{SITE}/")
    faults = check()
    for f in faults:
        print(f)
    print(f"rewrote the head of {n} pages" + (f"; {len(faults)} faults" if faults else "; every page has a canonical and its own description"))
    sys.exit(1 if faults else 0)
