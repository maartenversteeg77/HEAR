"""Maakt een kopbeeld breder door de foto in het midden te zetten en de zijkanten
aan te vullen met een sterk vervaagde, donkere versie van dezelfde foto.
Gebruik: python3 scripts/verbreed.py bron.jpg doel.jpg [verhouding] [donker]"""
import sys, numpy as np
from PIL import Image, ImageFilter
bron, doel = sys.argv[1], sys.argv[2]
ratio = float(sys.argv[3]) if len(sys.argv) > 3 else 2.35
donker = float(sys.argv[4]) if len(sys.argv) > 4 else 0.7
src = Image.open(bron).convert('RGB'); w, h = src.size
W = int(h * ratio)
bg = src.resize((W, int(h * W / w)), Image.BICUBIC); top = (bg.height - h) // 2
bg = np.asarray(bg.crop((0, top, W, top + h)).filter(ImageFilter.GaussianBlur(70))).astype(float)
x = np.arange(W); ox = (W - w) // 2
bg *= (1 - np.clip(np.abs(x - W / 2) - w / 2, 0, None) / ((W - w) / 2) * donker)[None, :, None]
fg = np.zeros_like(bg); fg[:, ox:ox + w] = np.asarray(src).astype(float)
f = max(60, w // 8); a = np.zeros(W); a[ox:ox + w] = 1
r = np.linspace(0, 1, f) ** 1.5; a[ox:ox + f] = r; a[ox + w - f:ox + w] = r[::-1]
out = fg * a[None, :, None] + bg * (1 - a[None, :, None])
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(doel, quality=88)
print(doel, out.shape[1], 'x', out.shape[0])
