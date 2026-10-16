"""Bouwt de acht dienstenpagina's (site/*.html) uit content/diensten.json.
Kop, menu en voet komen uit site/index.html, zodat ze overal gelijk blijven.
Draaien na elke tekstwijziging: python3 scripts/bouw-diensten.py"""
import json, html, re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
site = root / "site"
data = json.loads((root / "content" / "diensten.json").read_text())
idx = (site / "index.html").read_text()
kop = idx[idx.index('<header class="top">'):idx.index('</script>') + 9]
kop = kop.replace('href="diensten.html">', 'href="diensten.html" aria-current="page">', 1)
voet = idx[idx.index('<footer class="voet">'):idx.index('</footer>') + 9]
e = lambda t: html.escape(t, quote=True)
def heel(t):  # koppeltekenwoorden niet afbreken
    return re.sub(r"(?<![\w-])([\wéÉ]+-[\wé]+)(?![\w-])", r'<span class="heel">\1</span>', e(t))

def blok(b):
    if "producten" in b:
        items = "".join(
            f'<figure><img src="{e(p["beeld"])}" alt="{e(p["naam"])}" loading="lazy">'
            f'<figcaption><strong>{e(p["naam"])}</strong>{e(p["regel"])}</figcaption></figure>'
            for p in b["producten"])
        return f'<section class="producten" aria-label="Producten">{items}</section>'
    ps = "".join(f"<p>{e(t)}</p>" for t in b["tekst"]) + b.get("html_na", "")
    return f'<article class="case-section"><h2>{e(b["label"]).upper()}</h2><div>{ps}</div></article>'

for pg in data["paginas"]:
    pos = f' style="object-position:{e(pg["beeld_positie"])}"' if pg.get("beeld_positie") else ""
    # productrij naar voren: direct onder de kop, vóór de intro
    prod = [b for b in pg["blokken"] if "producten" in b]
    rest = [b for b in pg["blokken"] if "producten" not in b]
    producten = "".join(blok(b) for b in prod)
    blokken = "".join(blok(b) for b in rest)
    # opeenvolgende case-sections samen in één case-sections-wrapper
    blokken = re.sub(r'((?:<article class="case-section">.*?</article>)+)', r'<section class="case-sections">\1</section>', blokken, flags=re.S)
    links = "".join(f'<a href="{e(l["href"])}">{e(l["tekst"])} →</a>' for l in pg.get("links", []))
    main = f'''<main class="wrap">
<section class="casehead"><a class="crumb" href="diensten.html">← Producten en diensten</a><h1 class="kernzin">{heel(pg["kernzin"])}</h1></section>
{producten}
<section class="quick quick-breed"><p>{e(pg["intro"])}</p></section>
{blokken}
<nav class="verwijzingen" aria-label="Verder lezen">{links}</nav>
</main>'''
    doc = f'''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(pg["intro"][:155])}"><title>{e(pg["titel"])} · HEAR</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Advent+Pro:wght@300;400;500&display=swap" rel="stylesheet"><link rel="stylesheet" href="home.css"><link rel="stylesheet" href="styles.css"></head><body class="pagina">
{kop}
{main}
{voet}
</body></html>'''
    (site / pg["bestand"]).write_text(doc)
    print("ok", pg["bestand"])
