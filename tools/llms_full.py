#!/usr/bin/env python3
"""Concatenate every page of the book into book/llms-full.txt, in SUMMARY order,
for agents that would rather fetch the corpus once. Run after `mdbook build`."""
import os, re, sys
here = os.path.join(os.path.dirname(__file__), "..")
src, book = os.path.join(here, "src"), os.path.join(here, "book")
if not os.path.isdir(book):
    sys.exit("run mdbook build first")
with open(os.path.join(src, "SUMMARY.md"), encoding="utf-8") as fh:
    pages = re.findall(r"\]\(([^)]+\.md)\)", fh.read())
parts = ["# MinecraftDocs — how Java Minecraft works\n\nOne file, every page, in reading order. Source: https://minecraftdocs.dev\n"]
for p in pages:
    with open(os.path.join(src, p), encoding="utf-8") as fh:
        parts.append(f"\n\n---\n<!-- page: {p} -->\n\n" + fh.read())
out = os.path.join(book, "llms-full.txt")
with open(out, "w", encoding="utf-8", newline="\n") as fh:
    fh.write("".join(parts))
print(f"wrote {out}: {len(pages)} pages, {os.path.getsize(out)//1024} KB")
