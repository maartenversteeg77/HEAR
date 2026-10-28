"""Deelbare links voor alle pagina's: Open Graph- en Twitter-metadata + deelbeeld 1200×630
(foto + zwarte balk met HEAR-logo en turquoise lijn, zoals bij nieuws).
Beeld = eerste foto in <main> (of de hero op de homepage); titel en omschrijving uit <title> en meta description.
Draait als LAATSTE stap, over site/*.html en site/en/*.html (nieuws heeft eigen metadata via bouw-nieuws.py).
Draaien: python3 scripts/bouw-og.py"""
import json, re, html, pathlib
from PIL import Image, ImageDraw
root = pathlib.Path(__file__).resolve().parent.parent
site = root / "site"; ogdir = site / "img" / "og"; ogdir.mkdir(parents=True, exist_ok=True)
BASIS = json.loads((root / "content" / "nieuws.json").read_text()).get("basis", "https://hear.nl").rstrip("/")
OVERSLAAN = {"merken.html", "projectbrief.html", "coffeecuts.html"}  # coffeecuts: eigen deelpagina met vaste metadata
# eigen deelbeeld per pagina waar de eerste foto niet de beste is
BEELD = {"high-end-audio": "img/dance-events-zaal.jpg", "aankoopadvies": "img/diensten/gala.jpg", "custom-dj-mix": "img/diensten/coffee-cuts.jpg"}
# uitsnede per pagina (0 = bovenkant, 1 = onderkant); custom-dj-mix: Coffee cuts-logo volledig in beeld
FOCUS = {"over-hear": 0.42, "custom-dj-mix": 0.15}
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
pagina_s = [p for p in site.glob("*.html") if p.name not in OVERSLAAN] + [p for p in (site / "en").glob("*.html") if p.name not in OVERSLAAN]
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
        deelbeeld(site / bron, ogdir / naam, focus=FOCUS.get(p.stem, 0.4))
        gemaakt[naam] = True
    import hashlib
    beeld_abs = f"{BASIS}/img/og/{naam}?v=" + hashlib.md5((ogdir / naam).read_bytes()).hexdigest()[:8]  # versie, zodat Facebook/LinkedIn een nieuw beeld ophalen
    tags = (f'<!--og--><meta property="og:title" content="{e(titel)}"><meta property="og:description" content="{e(omschr)}">'
            f'<meta property="og:url" content="{BASIS}{pad}"><meta property="og:site_name" content="HEAR"><meta property="og:type" content="website">'
            f'<meta property="og:locale" content="{"en_GB" if taal == "en" else "nl_NL"}">'
            f'<meta property="og:image" content="{beeld_abs}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{beeld_abs}"><!--/og-->')
    alt_pad = pad.replace("/en/", "/", 1) if taal == "en" else "/en" + pad
    alt_bestaat = (site / "en" / p.name).exists() if taal == "nl" else True
    tags += f'<link rel="canonical" href="{BASIS}{pad}">'
    if alt_bestaat:
        nl_pad, en_pad = (pad, alt_pad) if taal == "nl" else (alt_pad, pad)
        tags += f'<link rel="alternate" hreflang="nl" href="{BASIS}{nl_pad}"><link rel="alternate" hreflang="en" href="{BASIS}{en_pad}"><link rel="alternate" hreflang="x-default" href="{BASIS}{nl_pad}">'
    tags = tags.replace("<!--/og-->", "") + "<!--/og-->"
    s = re.sub(r'<link rel="canonical"[^>]*>|<link rel="alternate" hreflang[^>]*>', '', s)
    s = re.sub(r'<!--og-->.*?<!--/og-->', '', s, flags=re.S)
    s = re.sub(r'<meta property="og:[^>]*>|<meta name="twitter:[^>]*>', '', s)
    s = s.replace("</title>", "</title>" + tags, 1)
    p.write_text(s)
print(f"ok: {len(pagina_s)} pagina's, {len(gemaakt)} deelbeelden in img/og/")

# Deelpagina hear.nl/coffeecuts (en /en/coffeecuts): wordt hier elke keer opnieuw gemaakt uit de bron,
# zodat titel, omschrijving en deelbeeld nooit achterlopen op de pagina custom-dj-mix.html.
# Bron: het blok "Coffee cuts" in content/diensten.json (NL) en het deelbeeld van custom-dj-mix.
def coffeecuts():
    import hashlib
    dj = json.loads((root / "content" / "diensten.json").read_text())
    pg = next(x for x in dj["paginas"] if x["bestand"] == "custom-dj-mix.html")
    blok = next(b for b in pg["blokken"] if b.get("label") == "Coffee cuts")
    tekst_nl = blok["tekst"][0]
    en_paren = json.loads((root / "content" / "en.json").read_text())["paginas"].get("custom-dj-mix.html", [])
    tekst_en = next((x[1].strip("<>") for x in en_paren if x[0].strip("<>") == html.escape(tekst_nl, quote=True).replace("&#x27;", "&#x27;")), None) \
        or next((x[1].strip("<>") for x in en_paren if html.unescape(x[0].strip("<>")) == tekst_nl), tekst_nl)
    beeld = f"{BASIS}/img/og/custom-dj-mix.jpg?v=" + hashlib.md5((ogdir / "custom-dj-mix.jpg").read_bytes()).hexdigest()[:8]
    for taal, map_, tekst, verder, loc in (("nl", site, tekst_nl, "Door naar Coffee cuts", "nl_NL"), ("en", site / "en", html.unescape(tekst_en), "Continue to Coffee cuts", "en_GB")):
        pre = "/en" if taal == "en" else ""
        doel = f"{pre}/custom-dj-mix.html"
        d = e(tekst)
        s = (f'<!doctype html><html lang="{taal}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
             f'<title>Coffee cuts · HEAR</title><meta name="description" content="{d}">'
             f'<!-- Gegenereerd door scripts/bouw-og.py: deelpagina voor social posts; stuurt door naar het Coffee cuts-blok. Niet met de hand aanpassen. -->'
             f'<meta property="og:title" content="Coffee cuts · HEAR"><meta property="og:description" content="{d}"><meta property="og:url" content="{BASIS}{pre}/coffeecuts">'
             f'<meta property="og:site_name" content="HEAR"><meta property="og:type" content="website"><meta property="og:locale" content="{loc}">'
             f'<meta property="og:image" content="{beeld}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
             f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{beeld}">'
             f'<link rel="canonical" href="{BASIS}{doel}"><meta http-equiv="refresh" content="0; url={doel}#coffee-cuts">'
             f'<script>location.replace("{doel}"+location.search+"#coffee-cuts")</script>'
             '<style>body{margin:0;background:#191A19;color:#F6F5F1;font:16px/1.5 system-ui,sans-serif;display:grid;place-items:center;min-height:100vh}a{color:#D47763}</style>'
             f'</head><body><p><a href="{doel}#coffee-cuts">{verder} →</a></p></body></html>\n')
        (map_ / "coffeecuts.html").write_text(s)
coffeecuts()
print("ok: coffeecuts-deelpagina's opnieuw gemaakt")
