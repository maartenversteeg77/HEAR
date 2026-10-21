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
BASIS = data.get("basis", "https://hear.nl").rstrip("/")
idx = (site / "index.html").read_text()
e = lambda t: html.escape(t, quote=True)

# kop en voet uit index.html, met absolute paden (deze pagina's staan in een submap)
def absoluut(s):
    s = re.sub(r'href="(?!http|mailto:|#|/)([^"]+)"', r'href="/\1"', s)
    s = re.sub(r'src="(?!http|/)([^"]+)"', r'src="/\1"', s)
    return s
kop = absoluut(idx[idx.index('<header class="top">'):idx.index('</script>') + 9])
kop = kop.replace('<a href="/nieuws/">Nieuws</a>', '<a href="/nieuws/" aria-current="page">Nieuws</a>', 1)  # geen EN-nieuws; de EN-knop (uit index.html, al /en/index.html) leidt naar de Engelse homepage
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

def head(titel, omschrijving, pad, beeld_abs=None, artikel=False, taal="nl", alt_pad=None):
    og = (f'<meta property="og:title" content="{e(titel)}"><meta property="og:description" content="{e(omschrijving)}">'
          f'<meta property="og:url" content="{BASIS}{pad}"><meta property="og:site_name" content="HEAR">'
          f'<meta property="og:type" content="{"article" if artikel else "website"}"><meta property="og:locale" content="{"en_GB" if taal == "en" else "nl_NL"}">')
    if beeld_abs:
        og += (f'<meta property="og:image" content="{beeld_abs}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
               f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{beeld_abs}">')
    alt = ""
    if alt_pad:
        nl, en_ = (pad, alt_pad) if taal == "nl" else (alt_pad, pad)
        alt = f'<link rel="alternate" hreflang="nl" href="{nl}"><link rel="alternate" hreflang="en" href="{en_}">'
    return (f'<!doctype html><html lang="{taal}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta name="description" content="{e(omschrijving[:155])}"><title>{e(titel)} · HEAR</title>{og}{alt}'
            f'<link rel="canonical" href="{BASIS}{pad}">'
            f'<link rel="stylesheet" href="/home.css"><link rel="stylesheet" href="/styles.css"></head><body class="pagina">')

MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"]
def datum(iso, taal):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {(MONTHS if taal == 'en' else MAANDEN)[d.month-1]} {d.year}"
def v(b, veld, taal):
    return b.get(veld + "_en", b.get(veld)) if taal == "en" else b.get(veld)

# Engelse kop en voet uit site/en/index.html (gebouwd door bouw-en.py)
en_idx = (site / "en" / "index.html")
if en_idx.exists():
    ei = en_idx.read_text()
    kop_en = ei[ei.index('<header class="top">'):ei.index('</script>') + 9].replace('href="/nieuws/"', 'href="/en/nieuws/"')
    kop_en = kop_en.replace('<a href="/en/nieuws/">News</a>', '<a href="/en/nieuws/" aria-current="page">News</a>', 1)
    voet_en = ei[ei.index('<footer class="voet">'):ei.index('</footer>') + 9].replace('href="/nieuws/"', 'href="/en/nieuws/"')
else:
    kop_en, voet_en = kop, voet
def taalknop(k, taal, doel):
    if taal == "nl":
        return re.sub(r'<a class="taal" href="[^"]*"', f'<a class="taal" href="/en{doel}"', k, count=1)
    return re.sub(r'<a class="taal" href="[^"]*"', f'<a class="taal" href="{doel}"', k, count=1)

berichten = sorted([b for b in data["berichten"] if b.get("status") == "af"], key=lambda b: b["datum"], reverse=True)
(site / "en" / "nieuws").mkdir(parents=True, exist_ok=True)
L = {"nl": {"nieuws": "Nieuws", "overzicht_titel": "Nieuws en achtergronden", "laatste": "Laatste nieuws", "overzicht": "Naar het nieuwsoverzicht →", "lees": "Lees het bericht", "alle": "Alle berichten →", "home": "Naar de homepage →", "omschr": "Nieuwe producten, events en berichten van HEAR.", "home_href": "/index.html"},
     "en": {"nieuws": "News", "overzicht_titel": "News and background", "laatste": "Latest news", "overzicht": "To the news overview →", "lees": "Read the post", "alle": "All posts →", "home": "To the homepage →", "omschr": "New products, events and news from HEAR.", "home_href": "/en/index.html"}}

for taal in ("nl", "en"):
    pre = "/en" if taal == "en" else ""
    doelmap = site / "en" / "nieuws" if taal == "en" else uit
    K = kop_en if taal == "en" else kop; V = voet_en if taal == "en" else voet; T = L[taal]
    lijst = [b for b in berichten if not (taal == "en" and b.get("alleen_nl"))]
    for b in [b for b in lijst if not b.get("pad")]:
        pad = f"{pre}/nieuws/{b['slug']}.html"; nl_pad = f"/nieuws/{b['slug']}.html"
        social = imgdir / f"{b['slug']}-social.jpg"
        if taal == "nl": deelbeeld(b["beeld"], social)
        social_abs = f"{BASIS}/img/nieuws/{b['slug']}-social.jpg"
        def alinea_html(t):
            if t.startswith("## "): return f'<h2 class="kopje">{e(t[3:])}</h2>'
            return f"<p>{e(t)}</p>"
        lopend = "".join(alinea_html(t) for t in v(b, "tekst", taal)) + (v(b, "html_na", taal) or "")
        lead = v(b, "lead", taal) or v(b, "intro", taal)
        knop = ""
        if b.get("knop"):
            k = b["knop"]; ext = k["href"].startswith("http")
            href = k["href"] if ext or taal == "nl" else "/en" + k["href"]
            ktekst = b.get("knop_tekst_en", k["tekst"]) if taal == "en" else k["tekst"]
            knop = f'<p class="knoprij"><a class="link" href="{e(href)}"{" target=\"_blank\" rel=\"noopener\"" if ext else ""}>{e(ktekst)}<i aria-hidden="true">→</i></a></p>'
        pos = f' style="object-position:{e(b["beeld_positie"])}"' if b.get("beeld_positie") else ""
        passend = " passend" if b.get("beeld_passend") else ""
        kopregel = f'<section class="quick quick-breed kopregel"><p>{e(v(b, "kop", taal))}</p></section>' if b.get("kop") else ""
        main = f'''<main class="wrap">
<section class="casehead"><a class="crumb" href="{pre}/nieuws/"><span class="sectie">{T["nieuws"]}</span></a><p class="label nieuws-datum"><time datetime="{b["datum"]}">{datum(b["datum"], taal)}</time></p><h1 class="kernzin">{e(v(b, "titel", taal))}</h1></section>
<figure class="casehero{passend}"><img src="/{e(b["beeld"])}" alt="{e(v(b, "beeld_alt", taal) or "")}"{pos}></figure>
{kopregel}
<article class="artikel"><p class="lead">{e(lead)}</p>{lopend}{knop}</article>
<nav class="verwijzingen" aria-label="Verder"><a href="{pre}/nieuws/">{T["alle"]}</a><a href="{T["home_href"]}">{T["home"]}</a></nav>
</main>'''
        alt_pad = f"/en/nieuws/{b['slug']}.html" if taal == "nl" else nl_pad
        (doelmap / f"{b['slug']}.html").write_text(head(v(b, "titel", taal), v(b, "intro", taal), pad, social_abs, artikel=True, taal=taal, alt_pad=alt_pad)
            + taalknop(K, taal, nl_pad) + main + V + "</body></html>")
        print(f"ok {taal} nieuws/{b['slug']}.html")
    tegels = "".join(
        f'<article class="case-tegel"><img src="/{e(b["beeld"])}" alt="{e(v(b, "beeld_alt", taal) or "")}" loading="lazy"{(" style=\"object-position:" + e(b["beeld_positie"]) + "\"") if b.get("beeld_positie") else ""}>'
        f'<div class="case-tekst"><p class="labels"><time datetime="{b["datum"]}">{datum(b["datum"], taal)}</time></p>'
        f'<h2><a class="tegel-link" href="{(b.get("pad_en") if taal == "en" else b.get("pad")) or (pre + "/nieuws/" + b["slug"] + ".html")}">{e(v(b, "titel", taal))}</a></h2><p>{e(v(b, "intro", taal))}</p><span class="pijl" aria-hidden="true">→</span></div></article>'
        for b in lijst)
    artikelen = [b for b in lijst if not b.get("pad")]
    eerste = f"{BASIS}/img/nieuws/{artikelen[0]['slug']}-social.jpg" if artikelen else None
    main = f'''<main class="wrap">
<section class="casehead"><a class="crumb" href="{T["home_href"]}"><span class="sectie">HEAR</span></a><h1>{T["overzicht_titel"]}</h1></section>
<section class="case-overzicht">{tegels}</section>
</main>'''
    (doelmap / "index.html").write_text(head(T["overzicht_titel"], T["omschr"], f"{pre}/nieuws/", eerste, taal=taal, alt_pad=("/en/nieuws/" if taal == "nl" else "/nieuws/"))
        + taalknop(K, taal, "/nieuws/") + main + V + "</body></html>")
    print(f"ok {taal} nieuws/index.html")

    heel = lambda t: re.sub(r'(\S*\w-\w\S*)', r'<span class="heel">\1</span>', t)  # modelnamen niet afbreken op het koppelteken
    # homepage: twee laatste berichten tussen Over HEAR en de afsluiter (markers <!--nieuws-home-->)
    home = site / "en" / "index.html" if taal == "en" else site / "index.html"
    if home.exists() and "<!--nieuws-home-->" in home.read_text():
        rel = "/" if taal == "en" else ""
        kaarten = "".join(
            f'<a class="werk-kaart" href="{(b.get("pad_en") if taal == "en" else b.get("pad")) or (pre + "/nieuws/" + b["slug"] + ".html")}"><span class="werk-beeld"><img src="{rel}{e(b["beeld"])}" alt="{e(v(b, "beeld_alt", taal) or "")}" loading="lazy"'
            f'{(" style=\"object-position:" + e(b["beeld_positie"]) + "\"") if b.get("beeld_positie") else ""}><span class="bekijk-case">{T["lees"]}<i aria-hidden="true">→</i></span></span>'
            f'<time datetime="{b["datum"]}">{datum(b["datum"], taal)}</time><h3>{heel(e(v(b, "titel", taal)))}</h3></a>'
            for b in ([b for b in lijst if not b.get("niet_op_home") and not b.get("op_home_derde")][:2] + [b for b in lijst if b.get("op_home_derde")][:1]))
        blok = (f'<!--nieuws-home--><section class="nieuws-home" aria-labelledby="nieuws-kop"><div class="werk-kop"><h2 id="nieuws-kop">{T["laatste"]}</h2>'
                f'<a class="tekstlink" href="{pre}/nieuws/">{T["overzicht"]}</a></div><div class="nieuws-home-rij">{kaarten}</div>'
                f'<a class="tekstlink onder" href="{pre}/nieuws/">{T["overzicht"]}</a></section><!--/nieuws-home-->')
        h = home.read_text()
        h = re.sub(r"<!--nieuws-home-->.*?<!--/nieuws-home-->", lambda m: blok, h, flags=re.S)
        home.write_text(h)
        print(f"ok {taal} index.html (laatste nieuws)")
