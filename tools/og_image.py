#!/usr/bin/env python3
"""Draw src/og.png, the 1200×630 image a link to any page unfurls with on
Discord, Reddit, Slack and X (tools/page_meta.py points og:image at it).
mdBook copies src/og.png into the build. Run once and commit the PNG; run
again only when the version or the site's name changes.

Uses the fonts on this machine (Windows: Segoe UI, Consolas); falls back to
Pillow's built-in font so the script never fails, only looks worse.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(HERE, "src", "og.png")
VERSION = "26.2"
W, H = 1200, 630
BG, INK, DIM, ACCENT = (24, 30, 38), (240, 240, 235), (150, 160, 170), (98, 170, 120)


def font(names, size):
    for n in names:
        for d in (r"C:\Windows\Fonts", "/usr/share/fonts", "/System/Library/Fonts"):
            p = os.path.join(d, n)
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    return ImageFont.load_default()


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
d.rectangle([0, 0, 18, H], fill=ACCENT)
title = font(["segoeuib.ttf", "seguisb.ttf", "DejaVuSans-Bold.ttf"], 78)
sub = font(["segoeui.ttf", "DejaVuSans.ttf"], 36)
mono = font(["consola.ttf", "DejaVuSansMono.ttf"], 30)
d.text((80, 150), "How Java", font=title, fill=INK)
d.text((80, 240), "Minecraft Works", font=title, fill=INK)
d.text((84, 370), "A system-level textbook of the current codebase.", font=sub, fill=DIM)
d.text((84, 418), "Names, never code. Every name checked against the decompile.", font=sub, fill=DIM)
d.text((84, 530), f"minecraftdocs.dev   ·   verified against {VERSION}", font=mono, fill=ACCENT)
img.save(OUT, optimize=True)
print(f"wrote {OUT} ({os.path.getsize(OUT)//1024} KB)")
