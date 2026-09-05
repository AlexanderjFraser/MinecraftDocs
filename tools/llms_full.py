#!/usr/bin/env python3
"""Concatenate every page of the book into book/llms-full.txt, in SUMMARY order,
for agents that would rather fetch the corpus once. Run after `mdbook build`.

mdBook's `{{#include path}}` directives are expanded here too: an included
markdown fragment (the atlas's generated tables) is pasted in, and an included
SVG figure is replaced by a one-line note naming it, since the table beside
it carries the same data."""
import os, re, sys
here = os.path.join(os.path.dirname(__file__), "..")
src, book = os.path.join(here, "src"), os.path.join(here, "book")
if not os.path.isdir(book):
    sys.exit("run mdbook build first")
INCLUDE = re.compile(r"\{\{#include ([^}]+)\}\}")


def expand(text: str, page_dir: str) -> str:
    def sub(m):
        target = m.group(1).strip()
        path = os.path.normpath(os.path.join(page_dir, target))
        if target.endswith(".svg"):
            # The claim used to be unconditional, and two pages carry no such table
            # (the treemap on the introduction, the EntityRenderState tree). Where a
            # sibling table exists, inline it; otherwise say the figure is only on the site.
            sibling = path[:-4] + ".md"
            if os.path.exists(sibling):
                with open(sibling, encoding="utf-8") as fh:
                    return (f"*(figure: {os.path.basename(target)} — a generated SVG on the site; its data follows)*"
                            + "\n\n" + fh.read().rstrip("\n"))
            return f"*(figure: {os.path.basename(target)} — a generated SVG, not reproduced here)*"
        with open(path, encoding="utf-8") as fh:
            return fh.read().rstrip("\n")
    return INCLUDE.sub(sub, text)


with open(os.path.join(src, "SUMMARY.md"), encoding="utf-8") as fh:
    pages = re.findall(r"\]\(([^)]+\.md)\)", fh.read())
parts = ["# MinecraftDocs — how Java Minecraft works\n\nOne file, every page, in reading order. Source: https://minecraftdocs.dev\n"]
for p in pages:
    with open(os.path.join(src, p), encoding="utf-8") as fh:
        parts.append(f"\n\n---\n<!-- page: {p} -->\n\n" + expand(fh.read(), os.path.dirname(os.path.join(src, p))))
out = os.path.join(book, "llms-full.txt")
with open(out, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("".join(parts))
print(f"wrote {out}: {len(pages)} pages, {os.path.getsize(out)//1024} KB")
