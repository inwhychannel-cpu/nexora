"""
Generate the 4 Nexora v5 header tiles with PIL (original drawn art).

Output: ~/workspace/nexora-voice-assistant/assets/tile_*.png (560x340)
Style: Nexora dark navy with blue/cyan/purple gradients, a large
simple drawn motif, and a short white label at the bottom.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = os.path.expanduser("~/workspace/nexora-voice-assistant/assets")
W, H = 560, 340

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def vgrad(size, top, bottom):
    """Vertical gradient image."""
    w, h = size
    base = Image.new("RGB", size, top)
    px = base.load()
    for y in range(h):
        t = y / max(1, h - 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        for x in range(w):
            px[x, y] = c
    return base


def add_glow(img, cx, cy, radius, color, strength=70):
    """Soft radial glow spot."""
    glow = Image.new("RGB", img.size, (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    steps = 24
    for i in range(steps, 0, -1):
        r = radius * i / steps
        f = (1 - i / steps)
        col = tuple(int(color[c] * strength / 100 * f) for c in range(3))
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    glow = glow.filter(ImageFilter.GaussianBlur(30))
    from PIL import ImageChops
    return ImageChops.add(img, glow)


def frame_and_label(img, label, sub):
    d = ImageDraw.Draw(img, "RGBA")
    # rounded border
    d.rounded_rectangle([6, 6, W - 7, H - 7], radius=28,
                        outline=(90, 150, 255, 160), width=3)
    # bottom band for the label
    d.rounded_rectangle([6, H - 78, W - 7, H - 7], radius=28,
                        fill=(5, 8, 20, 190))
    d.rectangle([6, H - 78, W - 7, H - 40], fill=(5, 8, 20, 190))
    f_big = ImageFont.truetype(BOLD, 34)
    f_small = ImageFont.truetype(REG, 19)
    # label with a soft cyan shadow
    d.text((30, H - 66), label, font=f_big, fill=(56, 225, 255))
    d.text((28, H - 68), label, font=f_big, fill=(255, 255, 255))
    d.text((29, H - 30), sub, font=f_small, fill=(170, 185, 235))
    return img


def rr(d, box, rad, **kw):
    d.rounded_rectangle(box, radius=rad, **kw)


# ---------------------------------------------------------------- voice
def tile_voice():
    img = vgrad((W, H), (10, 14, 42), (24, 18, 74))
    img = add_glow(img, 215, 140, 150, (56, 225, 255), 55)
    d = ImageDraw.Draw(img, "RGBA")
    cyan = (56, 225, 255)
    blue = (91, 140, 255)
    # microphone body
    rr(d, [185, 45, 245, 165], 30, fill=(30, 60, 160), outline=cyan, width=4)
    rr(d, [198, 62, 232, 100], 16, fill=cyan)
    # mic stand (cradle arc + stem + base)
    d.arc([160, 90, 270, 200], start=0, end=180, fill=blue, width=7)
    d.line([215, 198, 215, 228], fill=blue, width=7)
    d.line([178, 230, 252, 230], fill=blue, width=7)
    # sound waves
    for r, col in ((45, cyan), (78, (120, 200, 255)), (112, (150, 120, 255))):
        d.arc([215 - r, 140 - r, 215 + r, 140 + r], start=-55, end=55,
              fill=col, width=6)
    # a few music-note-like dots
    for (x, y, r) in ((360, 70, 7), (405, 110, 5), (375, 165, 6), (430, 60, 4)):
        d.ellipse([x - r, y - r, x + r, y + r], fill=(150, 120, 255, 200))
    return frame_and_label(img, "Speak & Done", "Boliye — kaam ho jayega")


# ---------------------------------------------------------------- apps
def tile_apps():
    img = vgrad((W, H), (8, 20, 48), (14, 40, 92))
    img = add_glow(img, 280, 130, 170, (91, 140, 255), 50)
    d = ImageDraw.Draw(img, "RGBA")
    # laptop: screen + base
    rr(d, [130, 40, 430, 215], 14, fill=(10, 16, 38), outline=(120, 170, 255), width=4)
    d.polygon([(112, 232), (448, 232), (472, 252), (88, 252)],
              fill=(22, 34, 74), outline=(120, 170, 255))
    # app squares inside the screen
    cols = [(56, 225, 255), (150, 120, 255), (91, 140, 255), (80, 230, 170)]
    pos = [(160, 65), (245, 65), (330, 65 - 0), (160, 140)]
    pos = [(160, 65), (245, 65), (330, 65), (245, 140)]
    labels = ["W", "▶", "N", "▦"]
    for (x, y), col, lab in zip(pos, cols, labels):
        rr(d, [x, y, x + 62, y + 62], 12, fill=col)
        f = ImageFont.truetype(BOLD, 30)
        d.text((x + 31, y + 30), lab, font=f, fill=(8, 10, 26), anchor="mm")
    # small squares row under screen = dock
    for i, col in enumerate(cols):
        x = 205 + i * 42
        rr(d, [x, 222, x + 26, 240], 6, fill=col)
    return frame_and_label(img, "Open Any App", "Word • Chrome • Desktop • PC")


# ---------------------------------------------------------------- search
def tile_search():
    img = vgrad((W, H), (16, 10, 46), (40, 16, 84))
    img = add_glow(img, 245, 130, 150, (150, 120, 255), 55)
    d = ImageDraw.Draw(img, "RGBA")
    # magnifier lens
    d.ellipse([140, 30, 350, 240], outline=(56, 225, 255), width=10,
              fill=(18, 26, 66))
    # play triangle inside the lens
    d.polygon([(225, 85), (225, 185), (295, 135)],
              fill=(255, 92, 120), outline=(255, 255, 255))
    # handle
    d.line([325, 215, 415, 268], fill=(91, 140, 255), width=20)
    d.line([325, 215, 415, 268], fill=(56, 225, 255), width=8)
    # sparkle stars
    for (x, y, s) in ((430, 60, 9), (465, 120, 6), (95, 90, 6), (445, 180, 5)):
        d.line([x - s, y, x + s, y], fill=(255, 255, 255), width=3)
        d.line([x, y - s, x, y + s], fill=(255, 255, 255), width=3)
    return frame_and_label(img, "Search the Web", "Google • YouTube • anything")


# ---------------------------------------------------------------- languages
def tile_languages():
    img = vgrad((W, H), (8, 26, 44), (12, 54, 84))
    img = add_glow(img, 250, 135, 160, (64, 200, 190), 50)
    d = ImageDraw.Draw(img, "RGBA")
    cx, cy, R = 250, 135, 100
    teal = (64, 220, 200)
    blue = (91, 140, 255)
    # orbit rings (wide flat ellipses) behind the globe
    d.ellipse([cx - 165, cy - 42, cx + 165, cy + 42], outline=(150, 120, 255), width=4)
    # globe
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(14, 34, 66),
              outline=teal, width=5)
    # meridians
    for fx in (0.45, 0.8):
        w2 = int(R * fx)
        d.ellipse([cx - w2, cy - R, cx + w2, cy + R], outline=blue, width=3)
    d.line([cx, cy - R, cx, cy + R], fill=blue, width=3)
    # parallels
    for fy in (-0.5, 0.0, 0.5):
        yy = cy + int(R * fy)
        half = int(R * math.sqrt(max(0.0, 1 - fy * fy)))
        d.line([cx - half, yy, cx + half, yy], fill=blue, width=3)
    d.line([cx - R, cy, cx + R, cy], fill=blue, width=3)
    # small speech dots around
    for (x, y, r, col) in ((420, 70, 10, (56, 225, 255)),
                           (95, 80, 8, (150, 120, 255)),
                           (430, 165, 7, (80, 230, 170)),
                           (105, 185, 6, (56, 225, 255))):
        d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    return frame_and_label(img, "62 Languages", "Sunein aur jawab — apni zuban mein")


def make_background():
    """
    v6: full-window background photo - the 4 tiles arranged 2x2 on a
    1280x800 dark-navy canvas, darkened to ~40% brightness so the
    foreground panels and text stay easy to read on top of it.
    Output: assets/bg_main.png (1280x800).
    """
    from PIL import ImageEnhance
    canvas = vgrad((1280, 800), (6, 8, 22), (10, 12, 30))
    tiles = [tile_voice(), tile_apps(), tile_search(), tile_languages()]
    tw, th = 616, 374
    positions = [(16, 16), (648, 16), (16, 410), (648, 410)]
    for img, (x, y) in zip(tiles, positions):
        canvas.paste(img.resize((tw, th)), (x, y))
    canvas = ImageEnhance.Brightness(canvas).enhance(0.40)
    return canvas


def main():
    os.makedirs(OUT, exist_ok=True)
    tiles = {
        "tile_voice.png": tile_voice(),
        "tile_apps.png": tile_apps(),
        "tile_search.png": tile_search(),
        "tile_languages.png": tile_languages(),
    }
    for name, img in tiles.items():
        path = os.path.join(OUT, name)
        img.save(path)
        print("wrote", path, img.size, os.path.getsize(path), "bytes")
    bg = make_background()
    bg_path = os.path.join(OUT, "bg_main.png")
    bg.save(bg_path)
    print("wrote", bg_path, bg.size, os.path.getsize(bg_path), "bytes")


if __name__ == "__main__":
    main()
