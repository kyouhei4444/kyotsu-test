"""icons.py  アプリのアイコンを作る（紺地に白で「共テ」）"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

OUT = pathlib.Path(__file__).resolve().parent.parent / 'icons'
FONT = 'C:/Windows/Fonts/YuGothB.ttc'
NAVY, WHITE, GOLD = (36, 70, 126), (255, 255, 255), (232, 184, 76)


def draw(size, safe):
    s = size * 4
    im = Image.new('RGB', (s, s), NAVY)
    d = ImageDraw.Draw(im)
    pad = s * (0.5 - safe / 2)
    f = ImageFont.truetype(FONT, int(s * safe * 0.42))
    d.text((s / 2, s / 2 - s * safe * 0.06), '共テ', font=f, fill=WHITE, anchor='mm')
    y = s / 2 + s * safe * 0.27
    d.rounded_rectangle([pad + s * safe * 0.22, y, s - pad - s * safe * 0.22, y + s * safe * 0.05], radius=s * 0.01, fill=GOLD)
    return im.resize((size, size), Image.LANCZOS)


for name, size, safe in [('icon-192.png', 192, 0.9), ('icon-512.png', 512, 0.9),
                         ('icon-maskable-512.png', 512, 0.66), ('apple-touch-icon.png', 180, 0.86),
                         ('favicon-32.png', 32, 1.0)]:
    draw(size, safe).save(OUT / name)
print('ok')
