#!/usr/bin/env python3
"""Compose the 19 November 2026 front page: 4 illustrated panels + ticker.

Every fact in the image was checked against news first reported on
Thursday 19 November 2026 (Reuters, AP, IMD, ICJ, Pew, NASA). The four
panels are artist's impressions drawn with Pillow shapes, not photos.
Output: 1024x1024 entry.png (PNG if it fits the 1 MiB cap, else JPEG).
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (179, 32, 44)
NAVY = (31, 56, 100)
TEAL = (14, 107, 107)
RULE = (26, 26, 26)

FD = "/usr/share/fonts/truetype/dejavu"
SERIF_B = ImageFont.truetype(f"{FD}/DejaVuSerif-Bold.ttf", 27)
SERIF = ImageFont.truetype(f"{FD}/DejaVuSerif.ttf", 17)
SANS = ImageFont.truetype(f"{FD}/DejaVuSans.ttf", 15)
SANS_B = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 13)
SANS_SM = ImageFont.truetype(f"{FD}/DejaVuSans.ttf", 12)
MAST = ImageFont.truetype(f"{FD}/DejaVuSerif-Bold.ttf", 58)
DATE_F = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 20)
KICK_F = ImageFont.truetype(f"{FD}/DejaVuSans-Bold.ttf", 13)


def wrap(draw, text, font, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def skyline(draw, x, y, w, h):
    """Dusk sky, tower silhouettes, three flags, Shenzhen panel."""
    for i in range(h):
        t = i / h
        draw.line([(x, y + i), (x + w, y + i)],
                  fill=(int(31 + 90 * t), int(56 + 60 * t), int(100 + 60 * t)))
    sun_x, sun_y, sun_r = x + w - 70, y + 42, 26
    draw.ellipse([sun_x - sun_r, sun_y - sun_r, sun_x + sun_r, sun_y + sun_r],
                 fill=(255, 176, 92))
    towers = [(0, 88, 34, 62), (40, 64, 30, 86), (76, 96, 36, 54),
              (118, 58, 28, 92), (152, 84, 34, 66), (192, 70, 30, 80),
              (228, 98, 32, 52), (266, 60, 30, 90), (302, 86, 34, 64),
              (342, 72, 30, 78), (378, 96, 34, 54), (418, 66, 30, 84)]
    for bx, by, bw, bh in towers:
        draw.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(16, 24, 46))
        for wy in range(y + h - bh + 8, y + h - 6, 12):
            for wx in range(x + bx + 5, x + bx + bw - 4, 10):
                if (wx + wy) % 3 == 0:
                    draw.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 120))
    # three flags on poles: US, China, Russia
    flags = [((214, 48, 48), (255, 255, 255), (214, 48, 48)),
             ((222, 41, 16), None, None),
             ((255, 255, 255), (0, 57, 166), (214, 48, 48))]
    for i, stripes in enumerate(flags):
        px = x + 60 + i * 170
        draw.line([(px, y + h - 118), (px, y + h - 52)], fill=(220, 220, 220), width=3)
        for j, col in enumerate(stripes):
            if col is None:
                draw.rectangle([px, y + h - 118, px + 46, y + h - 96],
                               fill=(222, 41, 16))
                for sx, sy in [(8, 6), (16, 10), (20, 4)]:
                    draw.ellipse([px + sx, y + h - 118 + sy, px + sx + 4,
                                  y + h - 118 + sy + 4], fill=(255, 222, 0))
                break
            draw.rectangle([px, y + h - 118 + j * 7, px + 46, y + h - 111 + j * 7],
                           fill=col)
        if i == 0:
            draw.rectangle([px, y + h - 118, px + 20, y + h - 107], fill=(31, 56, 100))


def vice_city(draw, x, y, w, h):
    """Neon dusk over Vice City: sun, palms, boulevard, sign."""
    for i in range(h):
        t = i / h
        draw.line([(x, y + i), (x + w, y + i)],
                  fill=(int(24 + 120 * t), int(10 + 30 * t), int(60 + 40 * t)))
    cx, cy, r = x + w // 2, y + 78, 52
    for rr in range(r, 0, -2):
        t = rr / r
        draw.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                     fill=(int(255 * (1 - t) + 255 * t), int(80 + 120 * t),
                           int(120 + 80 * t)))
    draw.rectangle([x, y + h - 34, x + w, y + h], fill=(12, 8, 24))
    draw.rectangle([x, y + h - 36, x + w, y + h - 34], fill=(255, 64, 180))
    for px, flip in [(x + 36, 1), (x + w - 52, -1)]:
        draw.line([(px, y + h - 34), (px + 8 * flip, y + 44)], fill=(8, 40, 20),
                  width=5)
        for a in range(-70, 71, 28):
            rad = math.radians(a)
            ex = px + 8 * flip + int(math.cos(rad) * 34 * flip)
            ey = y + 48 + int(math.sin(rad) * 16)
            draw.line([(px + 8 * flip, y + 46), (ex, ey)], fill=(8, 40, 20),
                      width=4)
    # car silhouette on the boulevard
    car_y = y + h - 30
    draw.rounded_rectangle([x + w // 2 - 78, car_y - 14, x + w // 2 + 78,
                            car_y + 2], radius=8, fill=(10, 10, 18))
    draw.polygon([(x + w // 2 - 44, car_y - 14), (x + w // 2 - 28, car_y - 30),
                  (x + w // 2 + 30, car_y - 30), (x + w // 2 + 46, car_y - 14)],
                 fill=(10, 10, 18))
    for wx in (x + w // 2 - 52, x + w // 2 + 36):
        draw.ellipse([wx, car_y - 2, wx + 16, car_y + 12], fill=(5, 5, 8))
    txt = "VICE CITY"
    tw = draw.textlength(txt, font=SERIF_B)
    for ox, oy, col in [(2, 2, (255, 64, 180)), (0, 0, (120, 240, 255))]:
        draw.text((x + (w - tw) / 2 + ox, y + 8 + oy), txt, font=SERIF_B,
                  fill=col)


def peace_palace(draw, x, y, w, h):
    """Peace Palace facade and scales of justice, The Hague panel."""
    draw.rectangle([x, y, x + w, y + h], fill=(233, 226, 208))
    draw.rectangle([x, y, x + w, y + 26], fill=(168, 196, 222))
    draw.ellipse([x + w - 66, y + 8, x + w - 34, y + 40], fill=(250, 244, 214))
    base = y + h - 22
    draw.rectangle([x + 52, base, x + w - 52, base + 22], fill=(120, 104, 84))
    draw.rectangle([x + 64, y + 66, x + w - 64, base], fill=(214, 200, 168))
    draw.polygon([(x + 52, y + 66), (x + w // 2, y + 30), (x + w - 52, y + 66)],
                 fill=(178, 160, 124))
    draw.ellipse([x + w // 2 - 10, y + 42, x + w // 2 + 10, y + 62],
                 fill=(179, 32, 44))
    for i in range(5):
        cx = x + 92 + i * 68
        draw.rectangle([cx, y + 78, cx + 18, base], fill=(240, 232, 210))
        draw.rectangle([cx - 3, y + 72, cx + 21, y + 78], fill=(178, 160, 124))
    # scales of justice, left
    sx, sy = x + 34, y + 96
    draw.line([(sx, sy), (sx, sy - 34)], fill=INK, width=3)
    draw.line([(sx - 26, sy - 34), (sx + 26, sy - 34)], fill=INK, width=3)
    for dx in (-26, 26):
        draw.line([(sx + dx, sy - 34), (sx + dx, sy - 18)], fill=INK, width=2)
        draw.polygon([(sx + dx - 12, sy - 18), (sx + dx + 12, sy - 18),
                      (sx + dx, sy - 4)], outline=INK, width=2)
    draw.ellipse([sx - 5, sy - 44, sx + 5, sy - 34], fill=INK)


def cyclone(draw, x, y, w, h):
    """Spiral storm over the Bay of Bengal, coastline at right."""
    draw.rectangle([x, y, x + w, y + h], fill=(58, 116, 158))
    cx, cy = x + w // 2 - 40, y + h // 2 + 6
    for k in range(1, 7):
        r = k * 15
        a0 = k * 55
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=a0, end=a0 + 250,
                 fill=(240, 244, 248), width=7)
    draw.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(240, 244, 248))
    # coastline: land mass bottom-right
    draw.polygon([(x + w - 150, y + h), (x + w, y + h - 150), (x + w, y + h)],
                 fill=(196, 178, 128))
    draw.polygon([(x + w - 150, y + h), (x + w, y + h - 150),
                  (x + w - 40, y + h - 118), (x + w - 118, y + h - 40)],
                 fill=(150, 168, 96))
    draw.line([(x + w - 150, y + h), (x + w, y + h - 150)], fill=(255, 255, 255),
              width=3)
    # rain streaks
    for rx in range(x + 16, x + w - 160, 26):
        draw.line([(rx, y + 12), (rx - 8, y + 34)], fill=(220, 235, 245), width=2)
    # storm label
    tag = "AKVAN"
    tw = draw.textlength(tag, font=SANS_B)
    draw.rectangle([x + 10, y + h - 30, x + 18 + tw, y + h - 10], fill=RED)
    draw.text((x + 14, y + h - 29), tag, font=SANS_B, fill=(255, 255, 255))


PANELS = [
    ("SHENZHEN  •  APEC", "Three leaders, one table",
     "Trump, Xi and Putin meet today in a first-ever trilateral — Iran and "
     "nuclear arms cuts on the agenda; Ukraine is not. A Trump–Xi lunch comes first.",
     skyline),
    ("GAMING  •  WORLDWIDE", "Welcome back to Vice City",
     "Grand Theft Auto VI launches today, rolling out at midnight from New "
     "Zealand — the first new title in 13 years, on PS5 and Xbox Series X|S, "
     "from $79.99. Lucia and Jason lead.",
     vice_city),
    ("THE HAGUE  •  10:00", "World court rules on Rohingya genocide",
     "The ICJ delivers its judgment today in The Gambia v. Myanmar — seven "
     "years after the case was filed; 730,000 Rohingya were driven out in "
     "2017. The ruling is final.",
     peace_palace),
    ("BAY OF BENGAL", "Cyclone Akvan closes in",
     "The severe storm sits about 480 km off Narsapur, moving north; landfall "
     "is due by noon Friday between Narsapur and Puri, winds 90–100 km/h. "
     "Schools shut in six Odisha districts.",
     cyclone),
]

TICKER = [
    "PEW: Islam to pass Christianity as the world's largest religion by 2035 — 2.57bn v 2.52bn",
    "NASA briefs today on Voyager 1, now a full light-day from Earth — 16bn miles",
    "SAUDI ARABIA: danger has passed in three southern cities after alerts",
    "AUSTRALIA sanctions Israeli settlers over West Bank expansion",
    "DELHI: Modi meets the Prince and Princess of Wales",
    "CANADA: Carney retools China ties, chasing the right US deal",
]


def panel(draw, x, y, w, h, kicker, headline, body, art):
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    art_h = 150
    art(draw, x + 1, y + 1, w - 2, art_h)
    draw.line([(x, y + art_h + 1), (x + w, y + art_h + 1)], fill=INK, width=2)
    ty = y + art_h + 10
    draw.text((x + 12, ty), kicker, font=KICK_F, fill=RED)
    ty += 20
    for line in wrap(draw, headline, SERIF_B, w - 24):
        draw.text((x + 12, ty), line, font=SERIF_B, fill=INK)
        ty += 32
    ty += 2
    for line in wrap(draw, body, SANS, w - 24):
        draw.text((x + 12, ty), line, font=SANS, fill=(40, 40, 40))
        ty += 19


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=MAST)
    d.text(((W - tw) / 2, 14), title, font=MAST, fill=INK)
    d.line([(28, 84), (W - 28, 84)], fill=RULE, width=3)
    date = "THURSDAY, 19 NOVEMBER 2026"
    dw = d.textlength(date, font=DATE_F)
    d.text(((W - dw) / 2, 94), date, font=DATE_F, fill=RED)
    d.line([(28, 122), (W - 28, 122)], fill=RULE, width=2)
    sub = "One day  •  One page  •  The world's news, first reported today"
    sw = d.textlength(sub, font=SERIF)
    d.text(((W - sw) / 2, 130), sub, font=SERIF, fill=(70, 70, 70))
    # panels 2x2
    gx, gy, pw, ph, gap = 28, 162, 474, 330, 20
    for i, (kicker, head, body, art) in enumerate(PANELS):
        px = gx + (i % 2) * (pw + gap)
        py = gy + (i // 2) * (ph + gap)
        panel(d, px, py, pw, ph, kicker, head, body, art)
    # ticker
    ty = gy + 2 * ph + gap + 8
    d.rectangle([28, ty, W - 28, ty + 140], fill=NAVY)
    d.text((44, ty + 10), "ALSO TODAY", font=SANS_B, fill=(255, 214, 120))
    ly = ty + 32
    for item in TICKER:
        d.text((44, ly), "•  " + item, font=SANS_SM, fill=(255, 255, 255))
        ly += 17
    # footer
    fy = ty + 150
    foot = ("All stories first reported 19 November 2026. Sources: Reuters, AP, IMD, "
            "ICJ, Pew Research Center, NASA. Panels are artist's impressions.")
    fw = d.textlength(foot, font=SANS_SM)
    d.text(((W - fw) / 2, fy), foot, font=SANS_SM, fill=(90, 90, 90))
    img.save("/tmp/entry-20261119.png")
    import os
    size = os.path.getsize("/tmp/entry-20261119.png")
    print(f"PNG bytes: {size}")
    if size <= 1048576:
        img.save("entry.png")
        print("saved entry.png as PNG")
    else:
        img.save("entry.png", "JPEG", quality=88)
        print(f"saved entry.png as JPEG: {os.path.getsize('entry.png')} bytes")


if __name__ == "__main__":
    main()
