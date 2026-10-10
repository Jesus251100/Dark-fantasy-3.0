from pathlib import Path
from PIL import Image, ImageDraw
import math

SESSION = Path(
    r"C:\Users\sanch\.grok\sessions\C%3A%5CUsers%5Csanch%5CDownloads%5Cclase-sena-piedecuesta-adso-noche-main\01a07198-cffc-7031-8e0b-12bdf3066981\images"
)
OUT = Path(r"C:\Users\sanch\Downloads\Dark-fantasy-3.0\src\assets\img")


def max_channel(px):
    return max(px[0], px[1], px[2])


def find_radii(img: Image.Image):
    gray = img.convert("L")
    w, h = gray.size
    cx, cy = w / 2, h / 2
    inner = None
    outer = None
    max_r = min(cx, cy) - 2
    for i in range(8, int(max_r)):
        # sample 24 points on the circle
        acc = 0
        for k in range(24):
            a = (math.tau * k) / 24
            x = int(cx + math.cos(a) * i)
            y = int(cy + math.sin(a) * i)
            acc += gray.getpixel((x, y))
        mean = acc / 24
        if inner is None and mean > 38:
            inner = i
        if mean > 26:
            outer = i
    return inner or max_r * 0.42, outer or max_r * 0.96, cx, cy


def ring_alpha(src: Path) -> Image.Image:
    img = Image.open(src).convert("RGBA")
    inner, outer, cx, cy = find_radii(img)
    print(f"rim inner={inner:.1f} outer={outer:.1f} size={img.size}")
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((cx - outer, cy - outer, cx + outer, cy + outer), fill=255)
    draw.ellipse((cx - inner, cy - inner, cx + inner, cy + inner), fill=0)
    img.putalpha(mask)
    return img


def key_black(src: Path, thresh: int = 18) -> Image.Image:
    img = Image.open(src).convert("RGBA")
    pix = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pix[x, y]
            m = max(r, g, b)
            if m <= thresh:
                pix[x, y] = (r, g, b, 0)
            elif m < thresh + 16:
                pix[x, y] = (r, g, b, int((m - thresh) * (255 / 16)))
    return img


rim = ring_alpha(SESSION / "1.jpg")
ptr = key_black(SESSION / "2.jpg")
rim.save(OUT / "ruleta-aro.png")
ptr.save(OUT / "ruleta-puntero.png")
print("saved", OUT / "ruleta-aro.png")
print("saved", OUT / "ruleta-puntero.png")
