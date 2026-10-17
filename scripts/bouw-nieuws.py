"""Bouwt de nieuwspagina's uit content/nieuws.json:
  site/nieuws/index.html          overzicht: [datum] titel, met beeldtegel
  site/nieuws/<slug>.html         het bericht zelf, met Open Graph-metadata voor socials
  site/img/nieuws/<slug>-social.jpg  deelbeeld 1200×630: foto + zwarte balk met HEAR-logo
Nieuws staat niet in de hoofdnavigatie; de pagina's zijn alleen via de link te bereiken.
Draaien na elke wijziging: python3 scripts/bouw-nieuws.py"""
import json, html, re, pathlib, datetime
from PIL import Image, ImageDraw

root = pathlib.Path(__file__).resolve().parent.parent
site = root / "site"; uit = site / "nieuws"; uit.mkdir(exist_ok=True)
imgdir = site / "img" / "nieuws"; imgdir.mkdir(parents=True, exist_ok=True)
data = json.loads((root / "content" / "nieuws.json").read_text())
BASIS = data.get("basis", "https://hear.maartenversteeg.workers.dev").rstrip("/")
idx = (site / "index.html").read_text()
e = lambda t: html.escape(t, quote=True)

# kop en voet uit index.html, met absolute paden (deze pagina's staan in een submap)
def absoluut(s):
    s = re.sub(r'href="(?!http|mailto:|#|/)([^"]+)"', r'href="/\1"', s)
    s = re.sub(r'src="(?!http|/)([^"]+)"', r'src="/\1"', s)
    return s
kop = absoluut(idx[idx.index('<header class="top">'):idx.index('</script>') + 9])
kop = kop.replace('href="/en/index.html"', 'href="/index.html"').replace('<a href="/nieuws/">Nieuws</a>', '<a href="/nieuws/" aria-current="page">Nieuws</a>', 1)  # geen EN-nieuws; knop leidt naar home
voet = absoluut(idx[idx.index('<footer class="voet">'):idx.index('</footer>') + 9])

MAANDEN = ["januari","februari","maart","april","mei","juni","juli","augustus","september","oktober","november","december"]
def datum_nl(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {MAANDEN[d.month-1]} {d.year}"

def deelbeeld(bron, doel):
    """1200×630: foto als cover in het bovenste deel, zwarte balk met logo en turquoise lijn onderaan."""
    W, H, BALK = 1200, 630, 110
    im = Image.open(site / bron).convert("RGB")
    bw, bh = im.size; doelr = W / (H - BALK)
    if bw / bh > doelr: nw = int(bh * doelr); im = im.crop(((bw - nw) // 2, 0, (bw - nw) // 2 + nw, bh))
    else: nh = int(bw / doelr); im = im.crop((0, (bh - nh) // 2, bw, (bh - nh) // 2 + nh))
    im = im.resize((W, H - BALK), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), (25, 26, 25)); canvas.paste(im, (0, 0))
    ImageDraw.Draw(canvas).rectangle([0, H - BALK, W, H - BALK + 4], fill=(122, 195, 201))
    logo = Image.open(site / "img" / "logo-white.png").convert("RGBA")
    lh = 44; lw = int(logo.size[0] * lh / logo.size[1]); logo = logo.resize((lw, lh), Image.LANCZOS)
    canvas.paste(logo, (56, H - BALK + (BALK - lh) // 2 + 2), logo)
    canvas.save(doel, quality=88)

def head(titel, omschrijving, pad, beeld_abs=None, artikel=False):
    og = (f'<meta property="og:title" content="{e(titel)}"><meta property="og:description" content="{e(omschrijving)}">'
          f'<meta property="og:url" content="{BASIS}{pad}"><meta property="og:site_name" content="HEAR">'
          f'<meta property="og:type" content="{"article" if artikel else "website"}"><meta property="og:locale" content="nl_NL">')
    if beeld_abs:
        og += (f'<meta property="og:image" content="{beeld_abs}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
               f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{beeld_abs}">')
    return (f'<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="description" content="{e(omschrijving[:155])}"><title>{e(titel)} · HEAR</title>{og}'
            f'<link rel="canonical" href="{BASIS}{pad}">'
            f'<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            f'<link href="https://fonts.googleapis.com/css2?family=Advent+Pro:wght@300;400;500&display=swap" rel="stylesheet">'
            f'<link rel="stylesheet" href="/home.css"><link rel="stylesheet" href="/styles.css"></head><body class="pagina">')

berichten = sorted([b for b in data["berichten"] if b.get("status") == "af"], key=lambda b: b["datum"], reverse=True)

# --- berichten ---
for b in berichten:
    pad = f"/nieuws/{b['slug']}.html"
    social = imgdir / f"{b['slug']}-social.jpg"; deelbeeld(b["beeld"], social)
    social_abs = f"{BASIS}/img/nieuws/{b['slug']}-social.jpg"
    alinea = "".join(f"<p>{e(t)}</p>" for t in b["tekst"]) + b.get("html_na", "")
    knop = ""
    if b.get("knop"):
        k = b["knop"]; ext = k["href"].startswith("http")
        knop = f'<p class="knoprij"><a class="wa sc" href="{e(k["href"])}"{" target=\"_blank\" rel=\"noopener\"" if ext else ""}>{e(k["tekst"])}<i aria-hidden="true">→</i></a></p>'
    pos = f' style="object-position:{e(b["beeld_positie"])}"' if b.get("beeld_positie") else ""
    passend = " passend" if b.get("beeld_passend") else ""
    main = f'''<main class="wrap">
<section class="casehead"><a class="crumb" href="/nieuws/">← Nieuws</a><p class="label nieuws-datum"><time datetime="{b["datum"]}">{datum_nl(b["datum"])}</time></p><h1 class="kernzin">{e(b["titel"])}</h1></section>
<figure class="casehero{passend}"><img src="/{e(b["beeld"])}" alt="{e(b.get("beeld_alt",""))}"{pos}></figure>
<section class="quick quick-breed"><p>{e(b["kop"]) if b.get("kop") else e(b["intro"])}</p></section>
<section class="case-sections"><article class="case-section nieuws-tekst"><h2>{e(b.get("label","Bericht")).upper()}</h2><div>{alinea}{knop}</div></article></section>
<nav class="verwijzingen" aria-label="Verder"><a href="/nieuws/">Alle berichten →</a><a href="/index.html">Naar de homepage →</a></nav>
</main>'''
    (uit / f"{b['slug']}.html").write_text(head(b["titel"], b["intro"], pad, social_abs, artikel=True) + kop + main + voet + "</body></html>")
    print("ok nieuws/" + b["slug"] + ".html")

# --- overzicht ---
tegels = "".join(
    f'<article class="case-tegel"><img src="/{e(b["beeld"])}" alt="{e(b.get("beeld_alt",""))}" loading="lazy"{(" style=\"object-position:" + e(b["beeld_positie"]) + "\"") if b.get("beeld_positie") else ""}>'
    f'<div class="case-tekst"><p class="labels"><time datetime="{b["datum"]}">{datum_nl(b["datum"])}</time></p>'
    f'<h2><a class="tegel-link" href="/nieuws/{b["slug"]}.html">{e(b["titel"])}</a></h2><p>{e(b["intro"])}</p><span class="pijl" aria-hidden="true">→</span></div></article>'
    for b in berichten)
eerste = f"{BASIS}/img/nieuws/{berichten[0]['slug']}-social.jpg" if berichten else None
main = f'''<main class="wrap">
<section class="casehead"><a class="crumb" href="/index.html">← HEAR</a><h1>Nieuws</h1></section>
<section class="case-overzicht">{tegels}</section>
</main>'''
(uit / "index.html").write_text(head("Nieuws", "Nieuwe producten, events en berichten van HEAR.", "/nieuws/", eerste) + kop + main + voet + "</body></html>")
print("ok nieuws/index.html")
