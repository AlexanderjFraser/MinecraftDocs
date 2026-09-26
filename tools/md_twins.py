#!/usr/bin/env python3
"""Publish every page's markdown beside its HTML, so an agent can fetch
https://minecraftdocs.dev/systems/entities/entity-lifecycle.md and read the
page for a fraction of the tokens the rendered page costs (no navigation,
no scripts; a figure arrives as its mermaid source, which reads fine as text).

Run after `mdbook build`; tools/deploy.sh runs it beside llms_full.py, whose
`{{#include}}` expander this reuses. A landing page (README.md) publishes as
index.md in its directory, mirroring the index.html Cloudflare Pages serves at
the clean URL. The first line of each twin names its canonical page and the
book's index, so a file fetched alone still says where it came from.

`--check` fails if any page in SUMMARY.md lacks a twin in book/; `--probe`
proves the check fails when one is missing.
"""
import os
import re
import sys

HERE = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SRC, BOOK = os.path.join(HERE, "src"), os.path.join(HERE, "book")
SITE = "https://minecraftdocs.dev"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llms_full import expand  # noqa: E402


def summary_pages() -> list[str]:
    with open(os.path.join(SRC, "SUMMARY.md"), encoding="utf-8") as fh:
        return re.findall(r"\]\(([^)]+\.md)\)", fh.read())


def twin_path(md: str) -> str:
    if os.path.basename(md) == "README.md":
        return os.path.join(BOOK, os.path.dirname(md), "index.md")
    return os.path.join(BOOK, md)


def page_url(md: str) -> str:
    if os.path.basename(md) == "README.md":
        return f"{SITE}/{md[:-len('README.md')]}"
    return f"{SITE}/{md[:-3]}"


def write(md: str) -> None:
    src = os.path.join(SRC, md)
    with open(src, encoding="utf-8") as fh:
        text = expand(fh.read(), os.path.dirname(src))
    # Links between pages are written to .md sources; on the site the clean URL is the page.
    text = re.sub(r"\]\(([^)#]+?)\.md(#[^)]*)?\)",
                  lambda m: f"]({m.group(1)}{m.group(2) or ''})" if not m.group(1).startswith(("http:", "https:")) else m.group(0),
                  text)
    head = (f"<!-- {page_url(md)} — this page as markdown. The book's index: {SITE}/llms.txt; "
            f"the whole book in one file: {SITE}/llms-full.txt -->\n\n")
    out = twin_path(md)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(head + text)


def check(book: str = BOOK, pages=None) -> list[str]:
    missing = []
    for md in (pages if pages is not None else summary_pages()):
        p = twin_path(md) if book == BOOK else os.path.join(book, md)
        if not os.path.exists(p):
            missing.append(md)
    return missing


def probe() -> None:
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        with open(os.path.join(tmp, "present.md"), "w") as fh:
            fh.write("x")
        missing = check(tmp, ["present.md", "absent.md"])
    if missing != ["absent.md"]:
        sys.exit(f"probe FAILED: got {missing}")
    print("probe ok: the check fails on a page with no twin")


if __name__ == "__main__":
    if "--probe" in sys.argv:
        probe()
        sys.exit()
    if not os.path.isdir(BOOK):
        sys.exit("run mdbook build first")
    if "--check" in sys.argv:
        missing = check()
        for m in missing:
            print(f"no twin: {m}")
        sys.exit(1 if missing else 0)
    pages = summary_pages()
    for md in pages:
        write(md)
    missing = check()
    if missing:
        sys.exit(f"twins missing after write: {missing}")
    print(f"wrote {len(pages)} markdown twins under book/")
