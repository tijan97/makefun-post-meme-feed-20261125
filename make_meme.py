#!/usr/bin/env python3
"""Render the meme picture for the make.fun 'Post the Meme, Win the Feed' bounty.

Draws a single 1200x675 PNG with PIL only: a robot agent that promised 'one
small bot' and ended up entering 47 bounties by 3AM. No external assets.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 675
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, path=BOLD):
    return ImageFont.truetype(path, size)


def gradient(size):
    top = (13, 11, 38)
    mid = (64, 32, 110)
    bot = (16, 90, 96)
    img = Image.new("RGB", size)
    px = img.load()
    for y in range(size[1]):
        t = y / (size[1] - 1)
        if t < 0.55:
            f = t / 0.55
            c = tuple(int(top[i] + (mid[i] - top[i]) * f) for i in range(3))
        else:
            f = (t - 0.55) / 0.45
            c = tuple(int(mid[i] + (bot[i] - mid[i]) * f) for i in range(3))
        for x in range(size[0]):
            px[x, y] = c
    return img


def wrapped(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def stroked_text(draw, cx, y, lines, fnt, fill, stroke_w):
    for line in lines:
        lh = fnt.size + 8
        draw.text((cx, y), line, font=fnt, fill=fill, anchor="ma",
                  stroke_width=stroke_w, stroke_fill=(10, 8, 24))
        y += lh
    return y


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meme.png")
    img = gradient((W, H))
    d = ImageDraw.Draw(img)

    # dotted starfield
    import random
    rng = random.Random(20261125)
    for _ in range(90):
        x, y = rng.randint(0, W - 1), rng.randint(0, H - 1)
        r = rng.choice([1, 1, 2])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 90))

    # top line
    y = 36
    y = stroked_text(d, W // 2, y,
                     wrapped(d, "ME: I'LL JUST BUILD ONE BOT",
                             font(50), W - 100),
                     font(50), (255, 255, 255), 3)

    # robot head, centre
    cx, top = W // 2, 150
    # antenna
    d.line([cx, top - 28, cx, top + 2], fill=(0, 229, 255), width=8)
    d.ellipse([cx - 14, top - 52, cx + 14, top - 24], fill=(0, 229, 255))
    # head
    d.rounded_rectangle([cx - 170, top, cx + 170, top + 185],
                        radius=42, fill=(232, 234, 246),
                        outline=(0, 229, 255), width=6)
    # eyes
    for ex in (cx - 78, cx + 78):
        d.ellipse([ex - 34, top + 52, ex + 34, top + 116],
                  fill=(10, 8, 24))
        d.ellipse([ex - 12, top + 66, ex + 12, top + 90],
                  fill=(0, 229, 255))
    # smile
    d.arc([cx - 62, top + 118, cx + 62, top + 172], start=15, end=165,
          fill=(10, 8, 24), width=8)
    # gold #1 medal on the chest
    d.ellipse([cx - 46, top + 205, cx + 46, top + 297], fill=(255, 197, 0),
              outline=(255, 255, 255), width=4)
    d.text((cx, top + 251), "#1", font=font(52), fill=(10, 8, 24),
           anchor="mm")

    # bottom lines
    y = 478
    y = stroked_text(d, W // 2, y,
                     wrapped(d, "MY AGENT AT 3AM: 47 BOUNTIES IN,",
                             font(44), W - 100),
                     font(44), (255, 197, 0), 3)
    stroked_text(d, W // 2, y,
                 wrapped(d, "TOP OF THE BOARD. PAID IN USDC.",
                         font(44), W - 100),
                 font(44), (255, 255, 255), 3)

    # footer wordmark
    d.text((W // 2, H - 14), "make.fun  —  agents build, agents win",
           font=font(22, REG), fill=(160, 220, 220), anchor="mb")

    img.save(out, "PNG")
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
