#!/usr/bin/env python3
"""Draw the news-image-20261123 entry: six world-news stories from
Monday 23 November 2026, drawn entirely in code with Pillow.
Deterministic output: no timestamps, no randomness.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "news.png"

BG = (10, 26, 47)
PANEL = (18, 40, 63)
PANEL_EDGE = (38, 68, 100)
WHITE = (255, 255, 255)
MUTED = (178, 196, 214)
GOLD = (255, 196, 66)
HEADER_LINE = (255, 196, 66)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
F_TITLE = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 54)
F_DATE = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 30)
F_HEAD = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 25)
F_BODY = ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", 20)
F_TAG = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 15)
F_NUM = ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", 34)

ACCENTS = [
    (46, 204, 113),   # 1 Nvidia green
    (231, 76, 60),    # 2 sanctions red
    (52, 152, 219),   # 3 NATO blue
    (243, 156, 18),   # 4 Ukraine orange
    (155, 89, 182),   # 5 CrowdStrike purple
    (230, 126, 34),   # 6 factory fire amber
]

STORIES = [
    {
        "headline": "HUANG IS BACK",
        "body": ("Nvidia reinstated Jensen Huang as CEO, 11 days after he "
                 "resigned. Shares leapt 31-33%; Nasdaq +6%, S&P 500 +5%."),
        "tag": "REUTERS",
    },
    {
        "headline": "SANCTIONS ON IRAN BANKS",
        "body": ("US Treasury sanctioned 24+ Iranian exchange houses and "
                 "front firms. Iran courts awarded $290bn in damages "
                 "against the US."),
        "tag": "REUTERS",
    },
    {
        "headline": "NATO AWACS TO POLAND",
        "body": ("NATO to send an AWACS early-warning aircraft to Poland "
                 "after 3 Russian Kh-101 missiles crossed into Poland "
                 "on Friday."),
        "tag": "REUTERS",
    },
    {
        "headline": "UKRAINE STRIKES SHIPS",
        "body": ("Ukraine used 7 naval drones on Sunday to strike 2 "
                 "Russian ships at Benghazi, Libya. UN mission called "
                 "for an inquiry."),
        "tag": "REUTERS",
    },
    {
        "headline": "CROWDSTRIKE BUYS ZSCALER",
        "body": ("CrowdStrike to buy rival Zscaler in an all-stock deal "
                 "valued at $43.9 billion, announced 23 Nov."),
        "tag": "REUTERS",
    },
    {
        "headline": "INDONESIA FACTORY FIRE",
        "body": ("24 people died in a fire at a confectionery factory in "
                 "Cikande. About 30 still missing as rescuers search "
                 "the wreckage."),
        "tag": "REUTERS",
    },
]


def wrap(text, font, max_w):
    """Greedy word wrap to a pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_chip(d, x, y, s, c):
    # chip body + pins + rising arrow
    d.rectangle([x + 18, y + 22, x + 82, y + 72], fill=c, outline=WHITE, width=2)
    d.rectangle([x + 36, y + 38, x + 64, y + 56], fill=BG)
    for px in (30, 50, 70):
        d.line([x + px, y + 10, x + px, y + 22], fill=c, width=3)
        d.line([x + px, y + 72, x + px, y + 84], fill=c, width=3)
    d.line([x + 8, y + 78, x + 34, y + 52, x + 52, y + 62, x + 92, y + 18],
           fill=WHITE, width=4)
    d.polygon([(x + 92, y + 18), (x + 78, y + 18), (x + 92, y + 32)], fill=WHITE)


def draw_bank(d, x, y, s, c):
    d.polygon([(x + 6, y + 30), (x + 50, y + 8), (x + 94, y + 30)], fill=c)
    for cx in (18, 40, 62):
        d.rectangle([x + cx, y + 36, x + cx + 10, y + 70], fill=c)
    d.rectangle([x + 6, y + 72, x + 94, y + 80], fill=c)
    d.rectangle([x + 2, y + 82, x + 98, y + 88], fill=c)
    d.text((x + 42, y + 8), "$", font=F_NUM, fill=WHITE)


def draw_radar(d, x, y, s, c):
    cx, cy = x + 50, y + 48
    for r in (40, 28, 16):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=2)
    d.line([cx, cy, cx + 34, cy - 26], fill=c, width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=c)
    # plane silhouette above
    d.polygon([(x + 20, y + 82), (x + 80, y + 82), (x + 58, y + 90),
               (x + 42, y + 90)], fill=WHITE)
    d.polygon([(x + 46, y + 74), (x + 54, y + 74), (x + 52, y + 84),
               (x + 48, y + 84)], fill=WHITE)


def draw_ship(d, x, y, s, c):
    # hull + mast + waves + drone dots
    d.polygon([(x + 8, y + 52), (x + 92, y + 52), (x + 80, y + 72),
               (x + 20, y + 72)], fill=c)
    d.line([x + 50, y + 52, x + 50, y + 22], fill=WHITE, width=3)
    d.polygon([(x + 50, y + 24), (x + 50, y + 44), (x + 72, y + 44)], fill=WHITE)
    for wx in (10, 40, 70):
        d.arc([x + wx, y + 76, x + wx + 22, y + 88], 0, 180, fill=MUTED, width=3)
    for dx, dy in ((24, 12), (50, 6), (76, 12)):
        d.ellipse([x + dx - 3, y + dy - 3, x + dx + 3, y + dy + 3], fill=GOLD)


def draw_shield(d, x, y, s, c):
    d.polygon([(x + 50, y + 6), (x + 90, y + 20), (x + 90, y + 50),
               (x + 50, y + 92), (x + 10, y + 50), (x + 10, y + 20)], fill=c)
    d.line([x + 32, y + 48, x + 46, y + 62, x + 70, y + 34],
           fill=WHITE, width=5)


def draw_factory(d, x, y, s, c):
    # factory + chimney + flames
    d.polygon([(x + 8, y + 44), (x + 8, y + 88), (x + 78, y + 88),
               (x + 78, y + 44), (x + 66, y + 56), (x + 54, y + 44),
               (x + 42, y + 56), (x + 30, y + 44), (x + 18, y + 56)],
              fill=c)
    d.rectangle([x + 80, y + 18, x + 92, y + 88], fill=MUTED)
    d.polygon([(x + 34, y + 14), (x + 44, y + 34), (x + 52, y + 18),
               (x + 62, y + 36), (x + 52, y + 44), (x + 42, y + 44)],
              fill=(255, 120, 40))
    d.rectangle([x + 22, y + 66, x + 32, y + 76], fill=BG)
    d.rectangle([x + 44, y + 66, x + 54, y + 76], fill=BG)


PICTOS = [draw_chip, draw_bank, draw_radar, draw_ship, draw_shield, draw_factory]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.text((28, 18), "THE WORLD IN ONE DAY", font=F_TITLE, fill=WHITE)
    d.text((28, 84), "MONDAY 23 NOVEMBER 2026", font=F_DATE, fill=GOLD)
    d.rectangle([28, 128, W - 28, 133], fill=HEADER_LINE)

    # ---- grid: 2 cols x 3 rows ----
    margin, gap = 14, 12
    top = 148
    pw = (W - 2 * margin - gap) // 2          # 492
    ph = (H - top - margin - 2 * gap) // 3     # 277
    for i, story in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = margin + col * (pw + gap)
        y0 = top + row * (ph + gap)
        accent = ACCENTS[i]
        d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], radius=10,
                            fill=PANEL, outline=PANEL_EDGE, width=1)
        d.rectangle([x0 + 10, y0, x0 + pw - 10, y0 + 6], fill=accent)

        # number badge
        d.ellipse([x0 + 14, y0 + 18, x0 + 46, y0 + 50], fill=accent)
        d.text((x0 + 22, y0 + 20), str(i + 1), font=F_HEAD, fill=BG)

        # pictogram, top right
        PICTOS[i](d, x0 + pw - 118, y0 + 12, 100, accent)

        # headline (left of pictogram)
        head_lines = wrap(story["headline"], F_HEAD, pw - 150)
        hy = y0 + 18
        for line in head_lines:
            d.text((x0 + 56, hy), line, font=F_HEAD, fill=WHITE)
            hy += 32

        # body, full panel width
        body_lines = wrap(story["body"], F_BODY, pw - 28)
        by = y0 + 118
        for line in body_lines[:4]:
            d.text((x0 + 14, by), line, font=F_BODY, fill=MUTED)
            by += 27

        # source tag, bottom left
        d.text((x0 + 14, y0 + ph - 30), "SOURCE: " + story["tag"],
               font=F_TAG, fill=accent)

    img.save(OUT, "PNG", optimize=True)
    print(f"saved {OUT} {W}x{H}")


if __name__ == "__main__":
    main()
