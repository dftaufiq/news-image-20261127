#!/usr/bin/env python3
"""Draw the 27 November 2026 front page (1024x1024) with PIL.

All artwork is drawn in code: no photos, no network, no randomness.
Run: python3 generate_image.py  ->  writes entry.png next to this file.
Deterministic: identical input, identical bytes (fixed content, no time).
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# --- palette ---------------------------------------------------------------
CREAM   = (251, 246, 233)   # page background
PAPER   = (255, 253, 245)   # story panels
INK     = (20, 20, 20)
NAVY    = (27, 42, 74)
NAVY2   = (31, 78, 121)
RED     = (180, 35, 24)
RED_LT  = (214, 48, 49)
GOLD    = (201, 162, 39)
TEAL    = (14, 124, 107)
AMBER   = (217, 119, 6)
PURPLE  = (107, 63, 160)
GREY    = (110, 110, 105)
LINE    = (27, 42, 74)
SEA     = (214, 228, 240)   # map sea
LAND    = (227, 211, 168)   # map land
SKY_D   = (23, 36, 66)      # dark sky (lead 1)
SKY_L   = (245, 222, 179)   # warm sky (lead 2)

FD = "/usr/share/fonts/truetype/dejavu/"
FN = "/usr/share/fonts/truetype/noto/"


def F(path, size):
    return ImageFont.truetype(path, size)


def serif_b(s):
    return F(FD + "DejaVuSerif-Bold.ttf", s)


def serif_i(s):
    return F(FN + "NotoSerif-Italic.ttf", s)


def sans(s):
    return F(FD + "DejaVuSans.ttf", s)


def sans_b(s):
    return F(FD + "DejaVuSans-Bold.ttf", s)


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_font(draw, text, path, size, max_w):
    """Largest size <= `size` whose text fits max_w."""
    while size > 8:
        f = F(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return F(path, 8)


def text(draw, xy, s, font, fill=INK, anchor="la"):
    draw.text(xy, s, font=font, fill=fill, anchor=anchor)


def centre(draw, y, s, font, fill=INK, cx=W // 2):
    draw.text((cx, y), s, font=font, fill=fill, anchor="ma")


def badge(draw, x, y, label, fill=RED):
    """Small HOW SURE badge; returns width used."""
    f = sans_b(10)
    w = int(draw.textlength(label, font=f)) + 12
    draw.rounded_rectangle([x, y, x + w, y + 15], radius=3, fill=fill)
    draw.text((x + 6, y + 2), label, font=f, fill=(255, 255, 255))
    return w


def hline(draw, x0, x1, y, fill=NAVY, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# --- illustration helpers --------------------------------------------------
def eu_stars(draw, cx, cy, r, n=12, dot=4):
    import math
    for i in range(n):
        a = -math.pi / 2 + 2 * math.pi * i / n
        x = cx + r * math.cos(a)
        y = cy + r * math.sin(a)
        draw.ellipse([x - dot, y - dot, x + dot, y + dot], fill=GOLD)


def mini_flag(draw, x, y, w, h, stripes):
    """Vertical tricolour / stripes flag; stripes = list of colours."""
    n = len(stripes)
    for i, c in enumerate(stripes):
        draw.rectangle([x, y + i * h // n, x + w, y + (i + 1) * h // n], fill=c)

# --- lead illustrations ----------------------------------------------------
def ill_eu(draw, x, y, w, h):
    """Brussels: EU quarter at dusk, circle of gold stars over the Berlaymont."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY_D)
    # distant skyline
    for bx, bw, bh in [(6, 34, 46), (48, 26, 62), (82, 40, 38), (130, 30, 55),
                       (168, 36, 42), (212, 28, 58), (248, 34, 36), (288, 26, 50)]:
        draw.rectangle([x + bx, y + h - bh - 18, x + bx + bw, y + h - 18],
                       fill=(52, 66, 102))
        for wy in range(y + h - bh - 12, y + h - 22, 10):
            for wx in range(x + bx + 5, x + bx + bw - 4, 9):
                draw.rectangle([wx, wy, wx + 3, wy + 4], fill=(250, 214, 120))
    # Berlaymont: curved slab with window grid
    draw.rounded_rectangle([x + 96, y + 34, x + w - 96, y + h - 18], radius=18,
                           fill=(88, 104, 138))
    for r in range(5):
        for c in range(7):
            wx = x + 112 + c * 16
            wy = y + 46 + r * 13
            draw.rectangle([wx, wy, wx + 9, wy + 7], fill=(190, 205, 225))
    eu_stars(draw, x + w // 2, y + 66, 52, dot=4)
    draw.rectangle([x, y + h - 18, x + w, y + h], fill=(16, 24, 46))


def ill_black_friday(draw, x, y, w, h):
    """Black Friday: shopfront with striped awning, gift boxes, SALE tag."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY_L)
    # sky sun + clouds
    draw.ellipse([x + w - 52, y + 10, x + w - 18, y + 44], fill=(250, 200, 80))
    # building
    draw.rectangle([x, y + 34, x + w, y + h], fill=(122, 62, 48))
    # awning stripes
    for i in range(8):
        c = RED if i % 2 == 0 else (255, 253, 245)
        draw.polygon([(x + i * w // 8, y + 34), (x + (i + 1) * w // 8, y + 34),
                      (x + (i + 1) * w // 8 - 6, y + 62), (x + i * w // 8 + 6, y + 62)],
                     fill=c)
    # windows with gifts
    for wx in (x + 14, x + 118, x + 222):
        draw.rectangle([wx, y + 74, wx + 88, y + h - 26], fill=(70, 130, 160))
        draw.rectangle([wx + 8, y + 82, wx + 38, y + 112], fill=(250, 200, 80))
        draw.rectangle([wx + 8, y + 96, wx + 38, y + 100], fill=RED)
        draw.rectangle([wx + 48, y + 88, wx + 80, y + 112], fill=(120, 200, 120))
        draw.rectangle([wx + 62, y + 88, wx + 66, y + 112], fill=(255, 255, 255))
    # SALE tag
    draw.polygon([(x + w - 78, y + h - 52), (x + w - 8, y + h - 52),
                  (x + w - 8, y + h - 14), (x + w - 78, y + h - 14)], fill=RED)
    draw.text((x + w - 70, y + h - 46), "SALE", font=sans_b(20), fill=(255, 255, 255))
    # shopping bags
    for bx, bc in [(x + 18, (30, 90, 160)), (x + 52, (14, 124, 107))]:
        draw.polygon([(bx, y + h - 22), (bx + 8, y + h - 44), (bx + 30, y + h - 44),
                      (bx + 38, y + h - 22)], fill=bc)


def ill_gas(draw, x, y, w, h):
    """Australia gas: LNG plant, storage spheres, flare stack."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 238, 244))
    draw.ellipse([x + 24, y + 12, x + 58, y + 46], fill=(250, 200, 80))
    # ground
    draw.rectangle([x, y + h - 30, x + w, y + h], fill=(196, 178, 140))
    # storage tanks
    for tx in (x + 20, x + 100, x + 180):
        draw.rectangle([tx, y + 62, tx + 62, y + h - 30], fill=(235, 238, 242),
                       outline=NAVY, width=2)
        draw.rectangle([tx, y + 78, tx + 62, y + 86], fill=NAVY2)
        draw.rectangle([tx, y + 96, tx + 62, y + 100], fill=NAVY2)
    # flare stack with flame
    draw.polygon([(x + 268, y + 26), (x + 276, y + 26), (x + 282, y + h - 30),
                  (x + 262, y + h - 30)], fill=(90, 100, 110))
    draw.polygon([(x + 264, y + 26), (x + 272, y + 4), (x + 280, y + 26)],
                 fill=(240, 120, 30))
    draw.polygon([(x + 267, y + 26), (x + 272, y + 12), (x + 277, y + 26)],
                 fill=(250, 200, 80))
    # pipeline
    draw.rectangle([x, y + h - 44, x + w, y + h - 36], fill=(120, 120, 110))


# --- small icons for secondaries -------------------------------------------
def icon_tobacco(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(250, 240, 210))
    draw.rectangle([x + 6, y + 8, x + s - 6, y + s - 8], fill=(255, 255, 255),
                   outline=NAVY, width=2)
    draw.rectangle([x + 6, y + 8, x + s - 6, y + 18], fill=RED)
    draw.rectangle([x + 12, y + 24, x + s - 12, y + 28], fill=(60, 60, 60))
    draw.rectangle([x + 12, y + 32, x + s - 16, y + 36], fill=(140, 140, 140))


def icon_tube(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(250, 240, 210))
    draw.ellipse([x + 6, y + 6, x + s - 6, y + s - 6], outline=RED, width=5)
    draw.rectangle([x + 2, y + s // 2 - 5, x + s - 2, y + s // 2 + 5], fill=NAVY2)


def icon_chess(draw, x, y, s):
    sq = s // 4
    for r in range(4):
        for c in range(4):
            if (r + c) % 2 == 0:
                draw.rectangle([x + c * sq, y + r * sq,
                                x + (c + 1) * sq, y + (r + 1) * sq], fill=INK)
    draw.ellipse([x + sq, y + sq, x + 2 * sq, y + 2 * sq], fill=GOLD)


def icon_cricket(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(120, 190, 90))
    draw.rectangle([x + 6, y + s // 2 - 3, x + s - 6, y + s // 2 + 3],
                   fill=(240, 230, 200))
    draw.ellipse([x + s - 16, y + 8, x + s - 4, y + 20], fill=(255, 255, 255),
                 outline=RED, width=1)
    draw.polygon([(x + 10, y + 10), (x + 18, y + 8), (x + 26, y + 26),
                  (x + 18, y + 28)], fill=(150, 100, 50))


def icon_gold(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(250, 240, 210))
    for i, (bx, by) in enumerate([(8, 26), (22, 26), (15, 12)]):
        draw.polygon([(x + bx, y + by), (x + bx + 4, y + by - 8),
                      (x + bx + 20, y + by - 8), (x + bx + 24, y + by)],
                     fill=GOLD, outline=(150, 110, 20))


def icon_flag_us(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(250, 240, 210))
    for i in range(7):
        draw.rectangle([x + 6, y + 6 + i * 5, x + s - 6, y + 6 + (i + 1) * 5],
                       fill=RED if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([x + 6, y + 6, x + 6 + s // 2, y + 6 + 20], fill=NAVY2)


def icon_files(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(250, 240, 210))
    draw.rectangle([x + 12, y + 6, x + s - 6, y + s - 8], fill=(255, 255, 255),
                   outline=NAVY, width=2)
    for i in range(4):
        draw.line([(x + 16, y + 14 + i * 7), (x + s - 10, y + 14 + i * 7)],
                  fill=GREY, width=2)
    draw.rectangle([x + 4, y + s - 16, x + 26, y + s - 4], fill=RED)
    draw.text((x + 7, y + s - 15), "!", font=sans_b(10), fill=(255, 255, 255))


def icon_pact(draw, x, y, s):
    draw.rectangle([x, y, x + s, y + s], fill=(250, 240, 210))
    for i, c in enumerate([(14, 124, 107), RED, (30, 90, 160)]):
        fx = x + 6 + i * 12
        draw.rectangle([fx, y + 8, fx + 10, y + s - 10], fill=c)
        draw.ellipse([fx + 2, y + 12, fx + 8, y + 18], fill=(255, 255, 255))

# --- page ------------------------------------------------------------------
def draw_page():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    # outer frame
    d.rectangle([0, 0, W - 1, H - 1], outline=NAVY, width=4)
    d.rectangle([6, 6, W - 7, H - 7], outline=NAVY, width=1)

    # ---- top bar ------------------------------------------------------
    d.rectangle([8, 8, W - 8, 34], fill=NAVY)
    text(d, (18, 13), "THE WORLD IN ONE DAY", sans_b(13), fill=(255, 255, 255))
    centre(d, 13, "15 STORIES  •  5 REGIONS  •  6 SOURCES  •  11 FIELDS",
           sans_b(12), fill=(250, 214, 120))

    # ---- masthead -----------------------------------------------------
    f_date = fit_font(d, "Friday 27 November 2026",
                      FD + "DejaVuSerif-Bold.ttf", 62, 990)
    centre(d, 38, "Friday 27 November 2026", f_date, fill=INK)
    sub = ("EU leaders leave the budget summit empty-handed, Black Friday opens "
           "with $1tn in holiday sales, and Australia reserves a fifth of its gas for home.")
    for i, ln in enumerate(wrap(d, sub, serif_i(17), 960)):
        centre(d, 106 + i * 22, ln, serif_i(17), fill=RED)

    # ---- later-today strip --------------------------------------------
    y = 154
    hline(d, 14, W - 14, y)
    centre(d, y + 5, "LATER TODAY (UTC)  •  14:30  Wall Street half-day Black Friday session"
                     "     •     EU Council presents summit conclusions"
                     "     •     20:00  Broncos – Steelers kick off",
           sans(12), fill=NAVY)
    hline(d, 14, W - 14, y + 24)

    # ---- big numbers --------------------------------------------------
    y0, y1 = 182, 240
    nums = [("€1.78tn", "EU BUDGET STALLED"),
            ("€45bn", "UKRAINE LOAN BLOCKED"),
            ("$1tn", "HOLIDAY SALES FORECAST"),
            ("+4.2%", "SALES GROWTH"),
            ("20%", "GAS KEPT AT HOME"),
            ("$3,550", "GOLD PER OUNCE")]
    bw = (W - 28) // 6
    for i, (num, lab) in enumerate(nums):
        x0 = 14 + i * bw
        if i:
            d.line([(x0, y0 + 4), (x0, y1 - 4)], fill=GREY, width=1)
        f_num = fit_font(d, num, FD + "DejaVuSans-Bold.ttf", 30, bw - 12)
        centre(d, y0 + 4, num, f_num, fill=NAVY, cx=x0 + bw // 2)
        f_lab = fit_font(d, lab, FD + "DejaVuSans-Bold.ttf", 10, bw - 10)
        centre(d, y0 + 38, lab, f_lab, fill=INK, cx=x0 + bw // 2)
    hline(d, 14, W - 14, y1)

    # ---- region tabs --------------------------------------------------
    y = 246
    chips = [("N AMERICA 3", NAVY2), ("EUROPE 7", RED), ("OCEANIA 2", TEAL),
             ("E ASIA 2", AMBER), ("M EAST / S ASIA 1", PURPLE)]
    cx = 14
    for label, col in chips:
        f = sans_b(11)
        wch = int(d.textlength(label, font=f)) + 16
        d.rounded_rectangle([cx, y, cx + wch, y + 20], radius=4, fill=col)
        d.text((cx + 8, y + 4), label, font=f, fill=(255, 255, 255))
        cx += wch + 6
    fields = "FIELDS: POLITICS · ECONOMY · ENERGY · MARKETS · TRANSPORT · SPORT · SCIENCE · DIPLOMACY · MEDIA · DEFENCE · CULTURE"
    f_f = fit_font(d, fields, FD + "DejaVuSans.ttf", 10, W - 14 - cx - 4)
    text(d, (cx + 4, y + 4), fields, f_f, fill=GREY, anchor="la")

    # ---- leads --------------------------------------------------------
    leads = [
        dict(num=1, place="BRUSSELS", beat="POLITICS",
             head="EU summit stalls: no budget, no Ukraine loan",
             body=("No deal on the €1.78tn budget or a €45bn Ukraine loan. "
                   "Next try: 17 December."),
             src="GUARDIAN • REUTERS", sure="CONFIRMED", ill=ill_eu),
        dict(num=2, place="USA", beat="SHOPPING",
             head="Black Friday opens: $1tn season ahead",
             body=("Holiday sales forecast up 4.2% to just over $1tn; "
                   "$82.5bn spent online so far."),
             src="REUTERS", sure="CONFIRMED", ill=ill_black_friday),
        dict(num=3, place="CANBERRA", beat="ENERGY",
             head="Australia reserves a fifth of its gas for home",
             body=("A 20% domestic gas reservation from 2028; "
                   "export tax fails, WA carved out."),
             src="REUTERS", sure="CONFIRMED", ill=ill_gas),
    ]
    ly0, ly1 = 274, 566
    lw = (W - 28 - 16) // 3
    for i, L in enumerate(leads):
        x0 = 14 + i * (lw + 8)
        x1 = x0 + lw
        d.rectangle([x0, ly0, x1, ly1], fill=PAPER, outline=NAVY, width=2)
        L["ill"](d, x0 + 2, ly0 + 2, lw - 4, 146)
        ky = ly0 + 154
        text(d, (x0 + 10, ky), f"{L['num']}  •  {L['place']}  •  {L['beat']}",
             sans_b(11), fill=RED)
        hy = ky + 18
        hlines = wrap(d, L["head"], serif_b(22), lw - 20)
        hf = serif_b(22)
        if len(hlines) > 2:
            hlines = wrap(d, L["head"], serif_b(20), lw - 20)
            hf = serif_b(20)
        for j, ln in enumerate(hlines[:2]):
            text(d, (x0 + 10, hy + j * 26), ln, hf)
        by = hy + 2 * 26 + 4
        for j, ln in enumerate(wrap(d, L["body"], sans(13), lw - 20)):
            text(d, (x0 + 10, by + j * 17), ln, sans(13))
        sy = ly1 - 24
        text(d, (x0 + 10, sy), L["src"], sans_b(10), fill=GREY)
        badge(d, x1 - 96, sy - 1, L["sure"])

    # ---- secondaries --------------------------------------------------
    secs = [
        dict(num=4, place="TOKYO", beat="MARKETS",
             head="Tobacco shares jump on takeover talk",
             body="Altria weighs an Imperial Brands bid.",
             src="REUTERS", sure="CONFIRMED", icon=icon_tobacco),
        dict(num=5, place="LONDON", beat="TRANSPORT",
             head="Tube strike hits London",
             body="Three lines suspended; back by 6pm.",
             src="REUTERS", sure="CONFIRMED", icon=icon_tube),
        dict(num=6, place="GENEVA", beat="CHESS",
             head="Gukesh–Sindarov: rest day at 1½–1½",
             body="Three draws in a row; Game 4 is Saturday.",
             src="FIDE", sure="CONFIRMED", icon=icon_chess),
        dict(num=7, place="AUSTRALIA", beat="SPORT",
             head="Cricket forum: no blame over sandpapergate",
             body="No blame, no adverse findings on anyone.",
             src="REUTERS", sure="CONFIRMED", icon=icon_cricket),
        dict(num=8, place="CHINA", beat="SCIENCE",
             head="China maps a $300bn gold belt",
             body="2,000+ tonnes mapped; biggest since 1949.",
             src="SCIENCEALERT", sure="REPORTED", icon=icon_gold),
        dict(num=9, place="WASHINGTON", beat="DIPLOMACY",
             head="Trump: Ukraine deal 'can be made swiftly'",
             body="He hopes a deal can be reached swiftly.",
             src="GUARDIAN", sure="CONFIRMED", icon=icon_flag_us),
        dict(num=10, place="LONDON", beat="POLITICS",
             head="Mandelson files: 'under the radar' meeting",
             body="Papers show a discreet meeting was sought.",
             src="GUARDIAN", sure="REPORTED", icon=icon_files),
        dict(num=11, place="ISLAMABAD", beat="DEFENCE",
             head="Mecca pact meets in Islamabad",
             body="First meeting of the new defence pact.",
             src="REUTERS", sure="CONFIRMED", icon=icon_pact),
    ]
    sy0 = 568
    sh, sw = 116, (W - 28 - 24) // 4
    for i, S in enumerate(secs):
        r, c = divmod(i, 4)
        x0 = 14 + c * (sw + 8)
        y0 = sy0 + r * (sh + 8)
        x1, y1 = x0 + sw, y0 + sh
        d.rectangle([x0, y0, x1, y1], fill=PAPER, outline=NAVY, width=1)
        S["icon"](d, x0 + 8, y0 + 8, 40)
        text(d, (x0 + 54, y0 + 10),
             f"{S['num']} • {S['place']}", sans_b(10), fill=RED)
        text(d, (x0 + 54, y0 + 24), S["beat"], sans_b(10), fill=GREY)
        hy = y0 + 50
        for j, ln in enumerate(wrap(d, S["head"], serif_b(14), sw - 16)[:2]):
            text(d, (x0 + 8, hy + j * 17), ln, serif_b(14))
        by = hy + 2 * 17 + 2
        for j, ln in enumerate(wrap(d, S["body"], sans(10), sw - 16)[:1]):
            text(d, (x0 + 8, by + j * 13), ln, sans(10))
        fy = y1 - 13
        text(d, (x0 + 8, fy), S["src"], sans_b(9), fill=GREY)
        badge(d, x1 - 78, fy - 2, S["sure"])
    return img, d

# --- map -------------------------------------------------------------------
MAP_CONTINENTS = [
    [(18, 8), (70, 4), (88, 12), (80, 26), (60, 34), (44, 30), (30, 22), (16, 16)],
    [(78, 2), (92, 2), (94, 8), (82, 8)],
    [(72, 38), (92, 36), (100, 46), (92, 62), (80, 58), (70, 46)],
    [(160, 8), (186, 6), (196, 12), (188, 20), (170, 20), (158, 14)],
    [(162, 24), (190, 22), (202, 32), (196, 50), (180, 58), (166, 44), (158, 32)],
    [(196, 6), (280, 4), (320, 10), (330, 22), (300, 30), (270, 26),
     (240, 28), (220, 20), (200, 14)],
    [(280, 34), (300, 32), (306, 40), (288, 42)],
    [(282, 48), (318, 46), (326, 54), (310, 62), (288, 58)],
]
# (number, x, y) in the 336x66 map space — spread to avoid overlaps
MAP_PINS = [(1, 182, 8), (2, 52, 12), (3, 300, 58), (4, 308, 18),
            (5, 160, 4), (6, 174, 20), (7, 322, 48), (8, 282, 22),
            (9, 40, 28), (10, 152, 12), (11, 238, 22)]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=NAVY, width=1)
    sx, sy = w / 336.0, h / 66.0
    for poly in MAP_CONTINENTS:
        d.polygon([(x + px * sx, y + py * sy) for px, py in poly], fill=LAND)
    for num, px, py in MAP_PINS:
        cx, cy = x + px * sx, y + py * sy
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        d.text((cx, cy - 1), str(num), font=sans_b(9), fill=(255, 255, 255),
               anchor="mm")


def draw_bottom(d):
    # ---- map + also ---------------------------------------------------
    by0, by1 = 814, 918
    # map panel
    mx0, mx1 = 14, 358
    text(d, (mx0, by0 + 4), "WHERE IT HAPPENED — PINS MATCH STORY NUMBERS",
         sans_b(11), fill=NAVY)
    draw_map(d, mx0, by0 + 24, mx1 - mx0, by1 - by0 - 24)
    # also-list panel
    ax0, ax1 = 366, 1010
    text(d, (ax0, by0 + 4), "ALSO ON FRIDAY 27 NOVEMBER — 4 MORE STORIES",
         sans_b(12), fill=RED)
    also = [
        (12, "SPAIN", "Doctored PM video in Yamal shirt",
         "People's Party AI clip stirs election race.", "GUARDIAN"),
        (13, "CALIFORNIA", "Father dies saving son on hike",
         "A father dies rescuing his teen son on a trail.", "GUARDIAN"),
        (14, "UK", "Lift-mechanic shortage strands towers",
         "High-rise residents wait for engineers.", "BBC"),
        (15, "MUSIC", "a-ha's Harket releases solo album",
         "Morten Harket's 'Human Grace' is out today.", "GUARDIAN"),
    ]
    cw = (ax1 - ax0 - 16) // 2
    for i, (num, place, head, det, src) in enumerate(also):
        r, c = divmod(i, 2)
        ex = ax0 + c * (cw + 16)
        ey = by0 + 26 + r * 36
        d.rectangle([ex, ey, ex + 22, ey + 22], fill=RED)
        d.text((ex + 11, ey + 11), str(num), font=sans_b(11),
               fill=(255, 255, 255), anchor="mm")
        text(d, (ex + 28, ey - 1), f"{place} — {head}", serif_b(11))
        text(d, (ex + 28, ey + 15), f"{det}  ", sans(10), fill=INK)
        # source appended right after detail on the same line
        dw = d.textlength(det + "  ", font=sans(10))
        text(d, (ex + 28 + dw, ey + 15), src, sans_b(9), fill=GREY)

    # ---- DATE CHECK ---------------------------------------------------
    dy0, dy1 = 922, 990
    d.rectangle([14, dy0, W - 14, dy1], fill=(253, 238, 238),
                outline=RED, width=2)
    text(d, (24, dy0 + 5),
         "DATE CHECK — EVERY STORY HERE IS DATED FRIDAY 27 NOVEMBER 2026. "
         "LEFT OUT (OTHER DAYS):", sans_b(11), fill=RED)
    ex1 = ("Macy's parade postponed (25 Nov)  •  Kuwait drone attack, 2 Italians "
           "killed (26 Nov)  •  Kim nuclear tour (26 Nov)  •  Hong Kong fire "
           "anniversary (26 Nov)  •  Bangkok refinery blast (26 Nov)")
    ex2 = ("COP31 ends without pact (22 Nov)  •  Shenzhou-24 docking (25 Nov)  •  "
           "BOK rate hike (26 Nov)  •  Katz Gaza threat (26 Nov)  •  Iraq sentences "
           "8 French IS members (26 Nov)")
    text(d, (24, dy0 + 24), ex1, sans(10))
    text(d, (24, dy0 + 40), ex2, sans(10))
    text(d, (24, dy0 + 54),
         "No story was carried over from another day; no story here is a forecast.",
         sans_b(10), fill=NAVY)

    # ---- footer -------------------------------------------------------
    text(d, (14, 996),
         "HOW SURE:   OFFICIAL = on the record   •   CONFIRMED = 2+ outlets   •   "
         "REPORTED = one outlet   •   CLAIM = one side's account",
         sans_b(10), fill=NAVY)
    text(d, (14, 1010),
         "Pictures and map: original, drawn in code.   •   Sources: Reuters · Guardian "
         "· FIDE · ScienceAlert · BBC · Time Out.   •   Built 08:50 WIB, Friday 27 November 2026.",
         sans(9), fill=GREY)


def main():
    img, d = draw_page()
    draw_bottom(d)
    out = __file__.rsplit("/", 1)[0] + "/entry.png"
    img.save(out, "PNG", optimize=True)
    import os
    print(f"wrote {out} ({os.path.getsize(out)} bytes, {img.size[0]}x{img.size[1]})")


if __name__ == "__main__":
    main()
