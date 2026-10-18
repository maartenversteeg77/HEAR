"""Deelbare links voor alle pagina's: Open Graph- en Twitter-metadata + deelbeeld 1200×630
(foto + zwarte balk met HEAR-logo en turquoise lijn, zoals bij nieuws).
Beeld = eerste foto in <main> (of de hero op de homepage); titel en omschrijving uit <title> en meta description.
Draait als LAATSTE stap, over site/*.html en site/en/*.html (nieuws heeft eigen metadata via bouw-nieuws.py).
Draaien: python3 scripts/bouw-og.py"""
import json, re, html, pathlib
from PIL import Image, ImageDraw
root = pathlib.Path(__file__).resolve().parent.parent
site = root / "site"; ogdir = site / "img" / "og"; ogdir.mkdir(parents=True, exist_ok=True)
BASIS = json.loads((root / "content" / "nieuws.json").read_text()).get("basis", "https://hear.maartenversteeg.workers.dev").rstrip("/")
OVERSLAAN = {"merken.html", "projectbrief.html"}
# eigen deelbeeld per pagina waar de eerste foto niet de beste is
BEELD = {"high-end-audio": "img/dance-events-zaal.jpg", "av-as-a-service": "img/diensten/gala.jpg"}
e = lambda t: html.escape(t, quote=True)

def deelbeeld(bron, doel, focus=0.4):
    W, H, BALK = 1200, 630, 110
    im = Image.open(bron).convert("RGB")
    bw, bh = im.size; r = W / (H - BALK)
    if bw / bh > r:
        nw = int(bh * r); x = (bw - nw) // 2; im = im.crop((x, 0, x + nw, bh))
    else:
        nh = int(bw / r); y = int((bh - nh) * focus); im = im.crop((0, y, bw, y + nh))
    im = im.resize((W, H - BALK), Image.LANCZOS)
    c = Image.new("RGB", (W, H), (25, 26, 25)); c.paste(im, (0, 0))
    ImageDraw.Draw(c).rectangle([0, H - BALK, W, H - BALK + 4], fill=(122, 195, 201))
    logo = Image.open(site / "img" / "logo-white.png").convert("RGBA")
    lh = 44; lw = int(logo.size[0] * lh / logo.size[1]); logo = logo.resize((lw, lh), Image.LANCZOS)
    c.paste(logo, (56, H - BALK + (BALK - lh) // 2 + 2), logo)
    c.save(doel, quality=86, optimize=True)

def beeld_van(s):
    m = re.search(r'<img class="hero-bg" src="/?([^"]+)"', s)
    if m: return m.group(1)
    main = re.search(r'<main.*?</main>', s, re.S)
    for m in re.finditer(r'<img[^>]+src="/?([^"]+)"', main.group(0) if main else ""):
        if "logo" not in m.group(1): return m.group(1)
    return "img/hero-dansvloer-blauw.jpg"

gemaakt = {}
pagina_s = [p for p in site.glob("*.html") if p.name not in OVERSLAAN] + list((site / "en").glob("*.html"))
for p in pagina_s:
    s = p.read_text()
    taal = "en" if p.parent.name == "en" else "nl"
    pad = ("/en/" if taal == "en" else "/") + p.name
    if p.name == "index.html": pad = pad[:-len("index.html")]
    titel = html.unescape(re.search(r"<title>(.*?)</title>", s, re.S).group(1))
    m = re.search(r'<meta name="description" content="([^"]*)"', s)
    omschr = html.unescape(m.group(1)) if m else ""
    bron = BEELD.get(p.stem) or beeld_van(s)
    naam = p.stem + ".jpg"
    if naam not in gemaakt:
        deelbeeld(site / bron, ogdir / naam, focus=0.42 if p.stem == "over-hear" else 0.4)
        gemaakt[naam] = True
    beeld_abs = f"{BASIS}/img/og/{naam}"
    tags = (f'<!--og--><meta property="og:title" content="{e(titel)}"><meta property="og:description" content="{e(omschr)}">'
            f'<meta property="og:url" content="{BASIS}{pad}"><meta property="og:site_name" content="HEAR"><meta property="og:type" content="website">'
            f'<meta property="og:locale" content="{"en_GB" if taal == "en" else "nl_NL"}">'
            f'<meta property="og:image" content="{beeld_abs}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{beeld_abs}"><!--/og-->')
    s = re.sub(r'<!--og-->.*?<!--/og-->', '', s, flags=re.S)
    s = re.sub(r'<meta property="og:[^>]*>|<meta name="twitter:[^>]*>', '', s)
    s = s.replace("</title>", "</title>" + tags, 1)
    p.write_text(s)
print(f"ok: {len(pagina_s)} pagina's, {len(gemaakt)} deelbeelden in img/og/")
