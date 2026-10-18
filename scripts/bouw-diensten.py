"""Bouwt de acht dienstenpagina's (site/*.html) uit content/diensten.json.
Kop, menu en voet komen uit site/index.html, zodat ze overal gelijk blijven.
Draaien na elke tekstwijziging: python3 scripts/bouw-diensten.py"""
import json, html, re, pathlib, urllib.parse
root = pathlib.Path(__file__).resolve().parent.parent
site = root / "site"
data = json.loads((root / "content" / "diensten.json").read_text())
idx = (site / "index.html").read_text()
kop = idx[idx.index('<header class="top">'):idx.index('</script>') + 9]
kop = kop.replace('href="diensten.html">', 'href="diensten.html" aria-current="page">', 1)
voet = idx[idx.index('<footer class="voet">'):idx.index('</footer>') + 9]
e = lambda t: html.escape(t, quote=True)
AAN = ' class="aan" aria-current="page"'
def heel(t):  # koppeltekenwoorden niet afbreken
    return re.sub(r"(?<![\w-])([\wéÉ]+-[\wé]+)(?![\w-])", r'<span class="heel">\1</span>', e(t))

SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2c0 1.3.9 2.5 1.1 2.7.1.2 1.8 2.8 4.4 3.9 1.7.7 2.3.8 3.1.7.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2l-.8-.3Z"/></svg>'
def waknop(tekst, bericht):
    return f'<a class="wa" href="https://wa.me/?text={urllib.parse.quote(bericht)}" data-whatsapp>{SVG}<span>{e(tekst)}</span><i aria-hidden="true">→</i></a>'

def blok(b):
    if "producten" in b:
        def fig(p):
            beelden = p.get("beelden") or [p["beeld"]]
            imgs = "".join(f'<img src="{e(bl)}" alt="{e(p["naam"])}" loading="lazy">' for bl in beelden)
            if len(beelden) > 1: imgs = f'<div class="duo">{imgs}</div>'
            link = f'<a class="bekijk" href="{e(p["link"]["href"])}" target="_blank" rel="noopener">{e(p["link"]["tekst"])} ↗</a>' if p.get("link") else ""
            breed = ' class="breed"' if len(beelden) > 1 else ""
            return f'<figure{breed}>{imgs}<figcaption><strong>{e(p["naam"])}</strong><span class="regel">{e(p["regel"]).replace(chr(10), "<br>")}</span>{link}</figcaption></figure>'
        rijen = b.get("rijen")  # bv. [3,2,2]: tegels per rij op desktop; daarna rijen zo breed als de laatste
        if rijen:
            spans = []
            for n in rijen: spans += [12 // n] * n
            while len(spans) < len(b["producten"]): spans.append(12 // rijen[-1])
            items = "".join(fig(p).replace("<figure", f'<figure style="--s:{sp}"', 1) for p, sp in zip(b["producten"], spans))
            return f'<section class="producten rijen" aria-label="Producten">{items}</section>'
        items = "".join(fig(p) for p in b["producten"])
        return f'<section class="producten" aria-label="Producten">{items}</section>'
    ps = "".join(f"<p>{e(t)}</p>" for t in b["tekst"]) + b.get("html_na", "")
    kop = f'<h3 class="blok-kop">{e(b["kop"]).replace(chr(10), "<br>")}</h3>' if b.get("kop") else ""
    cls = "case-section donker" if b.get("donker") else "case-section"
    return f'<article class="{cls}"><h2>{e(b["label"]).upper()}</h2><div>{kop}{ps}</div></article>'

volgorde = data["paginas"]
def zijnav(i):
    v, n = volgorde[i - 1], volgorde[(i + 1) % len(volgorde)]
    bollen = "".join(f'<a href="{e(it["bestand"])}" title="{e(it["titel"])}"{AAN if k == i else ""}></a>' for k, it in enumerate(volgorde))
    return (f'<nav class="zijnav" aria-label="Andere categorieën"><a class="pijl" href="{e(v["bestand"])}" title="{e(v["titel"])}" aria-label="Vorige: {e(v["titel"])}">←</a>'
            f'<span class="bollen">{bollen}</span><a class="pijl" href="{e(n["bestand"])}" title="{e(n["titel"])}" aria-label="Volgende: {e(n["titel"])}">→</a></nav>')

for i, pg in enumerate(data["paginas"]):
    pos = f' style="object-position:{e(pg["beeld_positie"])}"' if pg.get("beeld_positie") else ""
    # intro direct onder de kop, dan de productrij
    prod = [b for b in pg["blokken"] if "producten" in b]
    rest = [b for b in pg["blokken"] if "producten" not in b]
    producten = "".join(blok(b) for b in prod)
    blokken = "".join(blok(b) for b in rest)
    # opeenvolgende case-sections samen in één case-sections-wrapper
    blokken = re.sub(r'((?:<article class="case-section">.*?</article>)+)', r'<section class="case-sections">\1</section>', blokken, flags=re.S)
    links = "".join(f'<a href="{e(l["href"])}">{e(l["tekst"])} →</a>' for l in pg.get("links", []))
    cta = ""
    if pg.get("cta", True):
        knop = pg.get("cta_tekst", "Vraag een voorstel aan")
        bericht = pg.get("cta_bericht", f"Hoi Maarten, ik wil graag een voorstel voor {pg['titel'].lower()} voor mijn event.")
        cta = f'<p class="knoprij cta-intro">{waknop(knop, bericht)}</p>'
    intro = (f'<section class="quick quick-breed"><p>{e(pg["intro"])}</p>{cta}</section>' if pg.get("intro") else (f'<section class="quick quick-breed">{cta}</section>' if cta else ""))
    beschrijving = pg.get("intro") or next((t for b in pg["blokken"] for t in b.get("tekst", [])), pg["kernzin"])
    main = f'''<main class="wrap">
<section class="casehead"><a class="crumb" href="diensten.html"><span class="sectie">Producten</span><span class="scheiding" aria-hidden="true">|</span><span class="huidig">{e(pg["titel"])}</span></a>{zijnav(i)}<h1 class="kernzin">{heel(pg["kernzin"])}</h1>{('<p class="kop-knop">'+pg["kop_knop"]+'</p>') if pg.get("kop_knop") else ''}</section>
{intro}
{producten}
{blokken}
<nav class="verwijzingen" aria-label="Verder lezen">{links}</nav>
</main>'''
    doc = f'''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(beschrijving[:155])}"><title>{e(pg["titel"])} · HEAR</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Advent+Pro:wght@300;400;500&display=swap" rel="stylesheet"><link rel="stylesheet" href="home.css"><link rel="stylesheet" href="styles.css"></head><body class="pagina">
{kop}
{main}
{voet}
</body></html>'''
    (site / pg["bestand"]).write_text(doc)
    print("ok", pg["bestand"])
