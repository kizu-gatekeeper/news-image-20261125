#!/usr/bin/env python3
"""Draw the front page of THE WORLD TODAY for Wednesday, 25 November 2026.

A 1024x1024 newspaper front page summing up the day's world news.
All art is drawn in code with Pillow: no external images, no network.
Run:  python3 draw_poster.py   -> writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (178, 34, 34)
NAVY = (24, 52, 96)
TEAL = (18, 90, 92)
GOLD = (184, 134, 11)
GREY = (90, 88, 82)
LIGHT = (233, 226, 210)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, fill, max_w, leading):
    """Draw wrapped paragraph, return y after the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, x1, y, fill=INK, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def paste_art(img, box, func):
    """Draw art into a temp layer clipped to the box, then paste it in."""
    x0, y0, x1, y1 = box
    layer = Image.new("RGB", (x1 - x0, y1 - y0), (255, 255, 255))
    ld = ImageDraw.Draw(layer)
    func(ld, (0, 0, x1 - x0, y1 - y0))
    img.paste(layer, (x0, y0))


def gradient(draw, box, top, bottom):
    """Vertical gradient inside box."""
    x0, y0, x1, y1 = box
    steps = max(1, y1 - y0)
    for i in range(steps):
        t = i / steps
        col = tuple(int(top[c] + (bottom[c] - top[c]) * t) for c in range(3))
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=col)


# ---------------------------------------------------------------- lead art
def draw_hormuz(draw, box):
    """Strait of Hormuz: tanker at sea, a mine, smoke from a struck ship."""
    import math
    x0, y0, x1, y1 = box
    h = y1 - y0
    w = x1 - x0
    gradient(draw, (x0, y0, x1, y0 + int(h * 0.55)),
             (255, 214, 140), (240, 150, 90))
    # sun
    sr = int(h * 0.16)
    draw.ellipse([x1 - int(w * 0.12) - sr, y0 + int(h * 0.08),
                  x1 - int(w * 0.12) + sr, y0 + int(h * 0.08) + 2 * sr],
                 fill=(255, 236, 170))
    # sea
    sea_y = y0 + int(h * 0.55)
    gradient(draw, (x0, sea_y, x1, y1), (16, 68, 110), (8, 40, 70))
    # distant tanker silhouette
    dy = sea_y + int(h * 0.06)
    draw.rectangle([x0 + int(w * 0.06), dy + int(h * 0.10),
                    x0 + int(w * 0.30), dy + int(h * 0.24)], fill=(30, 30, 34))
    draw.rectangle([x0 + int(w * 0.20), dy, x0 + int(w * 0.24),
                    dy + int(h * 0.10)], fill=(30, 30, 34))
    # main tanker, foreground: long hull, white bridge, funnel
    hx0 = x0 + int(w * 0.34)
    hx1 = x1 - int(w * 0.06)
    hy = sea_y + int(h * 0.08)
    hh = int(h * 0.20)
    draw.rectangle([hx0, hy, hx1, hy + hh], fill=(122, 20, 20))
    draw.polygon([(hx1, hy), (hx1 + int(w * 0.03), hy + hh // 2),
                  (hx1, hy + hh)], fill=(122, 20, 20))
    draw.rectangle([hx0 + int(w * 0.42), hy - int(h * 0.18),
                    hx0 + int(w * 0.52), hy], fill=(240, 240, 235))
    draw.rectangle([hx0 + int(w * 0.44), hy - int(h * 0.26),
                    hx0 + int(w * 0.47), hy - int(h * 0.18)], fill=(240, 240, 235))
    draw.rectangle([hx0 + int(w * 0.55), hy - int(h * 0.12),
                    hx0 + int(w * 0.58), hy], fill=(40, 38, 36))
    # flame where the mine struck, mid-hull
    fx = hx0 + int(w * 0.16)
    draw.polygon([(fx, hy), (fx + int(w * 0.025), hy - int(h * 0.30)),
                  (fx + int(w * 0.05), hy)], fill=(255, 150, 30))
    draw.polygon([(fx + int(w * 0.01), hy),
                  (fx + int(w * 0.025), hy - int(h * 0.16)),
                  (fx + int(w * 0.04), hy)], fill=(255, 220, 80))
    # smoke plume above the flame, small puffs
    for fx2, fy2, fr in [(0.17, 0.30, 0.11), (0.20, 0.44, 0.13),
                         (0.23, 0.56, 0.14)]:
        cx = hx0 + int(w * fx2)
        cy = hy - int(h * fy2)
        r = int(h * fr)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(88, 84, 78))
    # naval mine in the water, foreground left
    mx, my = x0 + int(w * 0.15), y1 - int(h * 0.14)
    mr = int(h * 0.10)
    for ang in range(0, 360, 45):
        dx = int(mr * 1.9 * math.cos(math.radians(ang)))
        dy = int(mr * 1.9 * math.sin(math.radians(ang)))
        draw.line([(mx + dx // 2, my + dy // 2), (mx + dx, my + dy)],
                  fill=(20, 20, 22), width=4)
    draw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(25, 25, 28))
    draw.ellipse([mx - mr // 2, my - mr // 2, mx + mr // 2, my + mr // 2],
                 fill=(70, 70, 76))
    # waves
    for wy in (sea_y + int(h * 0.30), y1 - int(h * 0.06)):
        for wx in range(x0 + 10, x1 - 40, 90):
            draw.arc([wx, wy, wx + 70, wy + 18], 200, 340,
                     fill=(140, 190, 220), width=3)


# ------------------------------------------------------------- support art
def draw_rocket(draw, box):
    """Shenzhou-24: rocket climbing past the stars, Earth below."""
    import random
    x0, y0, x1, y1 = box
    h = y1 - y0
    w = x1 - x0
    gradient(draw, box, (10, 16, 44), (36, 68, 120))
    rnd = random.Random(11)
    for _ in range(40):
        sx = rnd.randint(x0 + 6, x1 - 6)
        sy = rnd.randint(y0 + 6, y1 - int(h * 0.25))
        r = rnd.choice([1, 1, 2])
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
    cx = (x0 + x1) // 2
    bw = max(8, int(w * 0.05))  # half body width
    top = y0 + int(h * 0.06)
    bot = y0 + int(h * 0.62)
    # flame
    draw.polygon([(cx - bw, bot), (cx, bot + int(h * 0.30)), (cx + bw, bot)],
                 fill=(255, 140, 20))
    draw.polygon([(cx - bw // 2, bot), (cx, bot + int(h * 0.18)),
                  (cx + bw // 2, bot)], fill=(255, 220, 90))
    # body
    draw.rounded_rectangle([cx - bw, top + int(h * 0.10), cx + bw, bot],
                           radius=8, fill=(240, 240, 238))
    draw.polygon([(cx - bw, top + int(h * 0.16)), (cx, top),
                  (cx + bw, top + int(h * 0.16))], fill=(178, 34, 34))
    wr = max(4, bw // 2)
    draw.ellipse([cx - wr, top + int(h * 0.28), cx + wr, top + int(h * 0.44)],
                 outline=(24, 52, 96), width=2)
    draw.polygon([(cx - bw, bot - int(h * 0.10)), (cx - bw - int(w * 0.05), bot),
                  (cx - bw, bot)], fill=(178, 34, 34))
    draw.polygon([(cx + bw, bot - int(h * 0.10)), (cx + bw + int(w * 0.05), bot),
                  (cx + bw, bot)], fill=(178, 34, 34))
    # Earth arc
    ey = y1 - int(h * 0.16)
    draw.ellipse([x0 - int(w * 0.25), ey, x1 + int(w * 0.25), y1 + int(h * 0.22)],
                 fill=(34, 110, 160))
    draw.ellipse([x0 + int(w * 0.08), ey + int(h * 0.04),
                  x0 + int(w * 0.32), ey + int(h * 0.14)], fill=(46, 140, 90))
    draw.ellipse([x1 - int(w * 0.34), ey + int(h * 0.06),
                  x1 - int(w * 0.10), ey + int(h * 0.16)], fill=(46, 140, 90))


def draw_treaty(draw, box):
    """Australia-Solomon Islands treaty: Pacific map, islands, signed pact."""
    import random
    x0, y0, x1, y1 = box
    h = y1 - y0
    w = x1 - x0
    gradient(draw, box, (120, 190, 220), (30, 100, 160))
    rnd = random.Random(7)
    # islands
    for _ in range(8):
        ix = rnd.randint(x0 + 8, x1 - int(w * 0.30))
        iy = rnd.randint(y0 + 6, y1 - int(h * 0.45))
        rx = rnd.randint(8, 20)
        ry = rnd.randint(5, 11)
        draw.ellipse([ix, iy, ix + rx, iy + ry], fill=(58, 140, 84))
    # dotted route from the lower-left corner toward the islands
    pts = []
    for t in range(0, 11):
        px = x0 + int(w * 0.06) + (x1 - x0 - int(w * 0.45)) * t / 10
        py = y1 - int(h * 0.10) - (y1 - y0 - int(h * 0.55)) * t / 10
        pts.append((px, py))
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=(255, 255, 255), width=2)
    # signed document, bottom right
    dx0, dy0 = x1 - int(w * 0.42), y1 - int(h * 0.62)
    dx1, dy1 = x1 - int(w * 0.05), y1 - int(h * 0.08)
    draw.rounded_rectangle([dx0, dy0, dx1, dy1], radius=5, fill=(250, 248, 240))
    draw.rectangle([dx0, dy0, dx1, dy0 + int(h * 0.10)], fill=(178, 34, 34))
    for ly in range(dy0 + int(h * 0.22), dy1 - int(h * 0.18), max(6, int(h * 0.09))):
        draw.line([(dx0 + 8, ly), (dx1 - 20, ly)], fill=(120, 116, 108), width=2)
    # signature squiggle + seal
    draw.arc([dx0 + 10, dy1 - int(h * 0.22), dx0 + int(w * 0.18), dy1 - int(h * 0.06)],
             200, 340, fill=INK, width=2)
    sr = max(4, int(h * 0.08))
    draw.ellipse([dx1 - 8 - 2 * sr, dy1 - 8 - 2 * sr, dx1 - 8, dy1 - 8],
                 fill=(178, 34, 34))
    # star marker at the route's end
    sx, sy = pts[-1]
    r = max(4, int(h * 0.07))
    draw.polygon([(sx, sy - 2 * r), (sx + r // 2, sy - r // 2), (sx + 2 * r, sy - r // 2),
                  (sx + r, sy + r // 2), (sx + int(1.5 * r), sy + 2 * r),
                  (sx, sy + r), (sx - int(1.5 * r), sy + 2 * r),
                  (sx - r, sy + r // 2), (sx - 2 * r, sy - r // 2),
                  (sx - r // 2, sy - r // 2)], fill=(255, 215, 60))


def draw_refinery(draw, box):
    """Ukraine strikes Russian refineries: plant silhouette, flames, smoke."""
    x0, y0, x1, y1 = box
    h = y1 - y0
    w = x1 - x0
    gradient(draw, box, (250, 200, 120), (210, 120, 70))
    # smoke
    for fx, fy, fr in [(0.22, 0.16, 0.16), (0.38, 0.08, 0.20), (0.78, 0.14, 0.18)]:
        cx, cy = x0 + int(w * fx), y0 + int(h * fy)
        r = int(h * fr)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 88, 80))
    # towers and tanks
    base = y1 - int(h * 0.08)
    draw.rectangle([x0 + int(w * 0.08), base - int(h * 0.55),
                    x0 + int(w * 0.18), base], fill=(40, 38, 36))
    draw.rectangle([x0 + int(w * 0.22), base - int(h * 0.72),
                    x0 + int(w * 0.30), base], fill=(40, 38, 36))
    draw.rectangle([x0 + int(w * 0.34), base - int(h * 0.42),
                    x0 + int(w * 0.52), base], fill=(52, 48, 44))
    draw.ellipse([x0 + int(w * 0.56), base - int(h * 0.38),
                  x0 + int(w * 0.76), base], fill=(52, 48, 44))
    draw.rectangle([x0 + int(w * 0.80), base - int(h * 0.62),
                    x0 + int(w * 0.88), base], fill=(40, 38, 36))
    # flame on the middle tower
    fx = x0 + int(w * 0.26)
    draw.polygon([(fx - int(w * 0.02), base - int(h * 0.72)),
                  (fx, base - int(h * 0.88)),
                  (fx + int(w * 0.02), base - int(h * 0.72))],
                 fill=(255, 150, 30))
    draw.polygon([(fx - int(w * 0.01), base - int(h * 0.72)),
                  (fx, base - int(h * 0.80)),
                  (fx + int(w * 0.01), base - int(h * 0.72))],
                 fill=(255, 220, 90))
    draw.line([(x0 + int(w * 0.04), base), (x1 - int(w * 0.04), base)],
              fill=(40, 38, 36), width=3)


def draw_court(draw, box):
    """Huawei convicted: courthouse columns and scales of justice."""
    x0, y0, x1, y1 = box
    h = y1 - y0
    w = x1 - x0
    gradient(draw, box, (228, 228, 222), (190, 188, 178))
    # pediment
    draw.polygon([(x0 + int(w * 0.06), y0 + int(h * 0.30)),
                  ((x0 + x1) // 2, y0 + int(h * 0.06)),
                  (x1 - int(w * 0.06), y0 + int(h * 0.30))], fill=(70, 70, 74))
    draw.rectangle([x0 + int(w * 0.06), y0 + int(h * 0.30),
                    x1 - int(w * 0.06), y0 + int(h * 0.38)], fill=(70, 70, 74))
    # columns
    n = 4
    gap = w / (n + 1)
    cw = max(6, int(w * 0.06))
    for i in range(1, n + 1):
        cx = int(x0 + gap * i - cw // 2)
        draw.rectangle([cx, y0 + int(h * 0.38), cx + cw, y1 - int(h * 0.14)],
                       fill=(245, 245, 240))
    draw.rectangle([x0 + int(w * 0.06), y1 - int(h * 0.14),
                    x1 - int(w * 0.06), y1 - int(h * 0.06)], fill=(70, 70, 74))
    # scales, centre
    cx = (x0 + x1) // 2
    top = y0 + int(h * 0.44)
    bot = y1 - int(h * 0.20)
    draw.line([(cx, top), (cx, bot)], fill=(178, 134, 11), width=3)
    arm = int(w * 0.16)
    draw.line([(cx - arm, top + int(h * 0.06)), (cx + arm, top + int(h * 0.06))],
              fill=(178, 134, 11), width=3)
    for s in (-1, 1):
        ex = cx + s * arm
        draw.line([(ex, top + int(h * 0.06)), (ex, top + int(h * 0.26))],
                  fill=(178, 134, 11), width=2)
        draw.arc([ex - int(w * 0.06), top + int(h * 0.20),
                  ex + int(w * 0.06), top + int(h * 0.42)], 0, 180,
                 fill=(178, 134, 11), width=2)
    draw.ellipse([cx - 3, top - 4, cx + 3, top + 2], fill=(178, 134, 11))


def draw_storm(draw, box):
    """Nor'easter: storm cloud, rain, lightning over a parade balloon."""
    x0, y0, x1, y1 = box
    h = y1 - y0
    w = x1 - x0
    gradient(draw, box, (70, 84, 110), (150, 160, 180))
    # cloud puffs only, no hard rectangle
    for fx, fy, fr in [(0.18, 0.28, 0.20), (0.38, 0.16, 0.26),
                       (0.60, 0.28, 0.22), (0.80, 0.24, 0.16)]:
        cx, cy = x0 + int(w * fx), y0 + int(h * fy)
        r = int(h * fr)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 56, 66))
    # lightning
    lx = x0 + int(w * 0.44)
    draw.polygon([(lx, y0 + int(h * 0.48)), (lx - int(w * 0.06), y0 + int(h * 0.72)),
                  (lx, y0 + int(h * 0.72)), (lx - int(w * 0.05), y0 + int(h * 0.94)),
                  (lx + int(w * 0.06), y0 + int(h * 0.66)),
                  (lx + int(w * 0.01), y0 + int(h * 0.66))],
                 fill=(255, 220, 60))
    # rain
    for rx in range(x0 + int(w * 0.06), x1 - int(w * 0.05), max(10, int(w * 0.09))):
        draw.line([(rx, y0 + int(h * 0.56)), (rx - 4, y0 + int(h * 0.76))],
                  fill=(210, 225, 240), width=2)
    # parade balloon, low right
    bx, by = x1 - int(w * 0.16), y1 - int(h * 0.22)
    br = max(6, int(h * 0.16))
    draw.ellipse([bx - 2 * br, by - br, bx + 2 * br, by + br], fill=(178, 34, 34))
    draw.ellipse([bx - br, by - br, bx + br, by - br // 3], fill=(220, 90, 90))
    draw.line([(bx, by + br), (bx, y1 - int(h * 0.04))], fill=(120, 116, 108), width=2)


# ------------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin
    X1 = W - M

    # masthead
    title_f = font(SERIF_B, 72)
    d.text((W // 2, 30), "THE WORLD TODAY", font=title_f, fill=INK, anchor="ma")
    rule(d, M, X1, 118, width=3)
    date_f = font(SANS_B, 26)
    d.text((W // 2, 130), "WEDNESDAY, 25 NOVEMBER 2026",
           font=date_f, fill=RED, anchor="ma")
    tag_f = font(SANS, 18)
    d.text((W // 2, 164), "THE DAY'S WORLD NEWS IN ONE PAGE",
           font=tag_f, fill=GREY, anchor="ma")
    rule(d, M, X1, 192, width=2)

    # ---- lead story: Hormuz
    y = 192
    kick_f = font(SANS_B, 20)
    d.text((M, y), "MIDDLE EAST  •  LEAD STORY", font=kick_f, fill=RED)
    y += 28
    head_f = font(SERIF_B, 40)
    y = para(d, M, y, "TANKERS HIT BY MINES IN THE STRAIT OF HORMUZ",
             head_f, INK, X1 - M, 48)
    y += 4
    art_box = (M, y, X1, y + 136)
    d.rectangle(art_box, outline=INK, width=2)
    paste_art(img, (art_box[0] + 2, art_box[1] + 2, art_box[2] - 2, art_box[3] - 2),
              draw_hormuz)
    y = art_box[3] + 8
    body_f = font(SANS, 19)
    y = para(d, M, y,
             "Three oil tankers under US air escort struck naval mines in the "
             "Strait of Hormuz, Iran's Revolutionary Guards said, as the "
             "conflict widens toward the Red Sea.",
             body_f, INK, X1 - M, 24)
    rule(d, M, X1, y + 4, width=2)

    # ---- middle row: two stories
    y += 14
    mid_top = y
    col_w = (X1 - M - 24) // 2
    mid = [
        ("SPACE", "PAKISTAN'S FIRST ASTRONAUT REACHES ORBIT",
         "Shenzhou-24 took Pakistan's Zeeshan Ali to Tiangong — the "
         "first foreign astronaut aboard it.",
         draw_rocket, TEAL),
        ("INDO-PACIFIC", "SOLOMONS SIGN HISTORIC PACT WITH AUSTRALIA",
         "Canberra becomes the islands' security partner of choice as "
         "Honiara drops its China deal.",
         draw_treaty, NAVY),
    ]
    mid_end = mid_top
    for i, (kick, head, body, art, col) in enumerate(mid):
        cx0 = M + i * (col_w + 24)
        cx1 = cx0 + col_w
        d.text((cx0, mid_top), kick, font=kick_f, fill=col)
        hy = mid_top + 28
        hy = para(d, cx0, hy, head, font(SERIF_B, 24), INK, col_w, 28)
        ay0 = hy + 6
        d.rectangle([cx0, ay0, cx1, ay0 + 88], outline=INK, width=2)
        paste_art(img, (cx0 + 2, ay0 + 2, cx1 - 2, ay0 + 86), art)
        by = ay0 + 98
        end = para(d, cx0, by, body, font(SANS, 18), INK, col_w, 23)
        mid_end = max(mid_end, end)
    rule(d, M, X1, mid_end + 4, width=2)

    # ---- bottom row: three stories
    y = mid_end + 14
    bot_top = y
    bcol_w = (X1 - M - 32) // 3
    bottom = [
        ("EUROPE", "PUTIN VOWS REVENGE FOR REFINERY STRIKES",
         "Ukraine keeps hitting Russian refineries despite a US request "
         "to stop.",
         draw_refinery, RED),
        ("TECH", "HUAWEI CONVICTED IN US SANCTIONS CASE",
         "A US court convicts Huawei in a sanctions and trade-secret case.",
         draw_court, NAVY),
        ("WEATHER", "NOR'EASTER THREATENS THANKSGIVING",
         "Heavy rain and winds threaten the Macy's parade and holiday "
         "travel.",
         draw_storm, TEAL),
    ]
    bot_end = bot_top
    for i, (kick, head, body, art, col) in enumerate(bottom):
        cx0 = M + i * (bcol_w + 16)
        cx1 = cx0 + bcol_w
        d.text((cx0, bot_top), kick, font=kick_f, fill=col)
        hy = bot_top + 26
        hy = para(d, cx0, hy, head, font(SERIF_B, 19), INK, bcol_w, 23)
        ay0 = hy + 4
        d.rectangle([cx0, ay0, cx1, ay0 + 54], outline=INK, width=2)
        paste_art(img, (cx0 + 2, ay0 + 2, cx1 - 2, ay0 + 52), art)
        by = ay0 + 62
        end = para(d, cx0, by, body, font(SANS, 16), INK, bcol_w, 20)
        bot_end = max(bot_end, end)
    print("layout: mid_end", mid_end, "bot_end", bot_end)

    # footer
    fy = H - 34
    rule(d, M, X1, fy - 8, width=2)
    d.text((W // 2, fy), "All events reported on Wednesday, 25 November 2026  •  "
           "Sources: Reuters, AP, CNN, The New York Times",
           font=font(SANS, 15), fill=GREY, anchor="ma")

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
