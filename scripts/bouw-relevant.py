"""Zet het blok 'Relevante producten en diensten' op doelgroep- en casepagina's (site/*.html),
uit content/relevant.json. Vóór <section class="cta-brug">; bestaand blok wordt vervangen.
Draaien: python3 scripts/bouw-relevant.py  (daarna bouw-en.py voor de Engelse pagina's)"""
import json, html, re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
site = root / "site"
d = json.loads((root / "content" / "relevant.json").read_text())
e = lambda t: html.escape(t, quote=True)
cat = d["catalogus"]
LEES_OOK = set(d.get("lees_ook", []))
def links_html(naam):
    links = [("diensten.html", "Alle producten en diensten")]
    if naam in LEES_OOK: links.append(("prijs.html", "Wat kost audiovisuele ondersteuning van een evenement eigenlijk?"))
    if len(links) == 1:
        h, t = links[0]; return f'<p class="inline-link"><a href="{h}">{e(t)} →</a></p>'
    return ('<div class="relevante-links"><p class="relevante-links-kop">Relevante links</p><ul>'
            + "".join(f'<li class="inline-link"><a href="{h}">{e(t)} →</a></li>' for h, t in links) + '</ul></div>')
for naam, items in d["paginas"].items():
    tegels = ""
    for it in items:
        slug, tekst = (it, None) if isinstance(it, str) else (it["slug"], it.get("tekst"))
        c = cat[slug]
        tegels += (f'<a class="visual-card" href="{slug}.html"><img src="{e(c["beeld"])}" alt="{e(c["naam"])}" loading="lazy">'
                   f'<span class="visual-card-shade"></span><span class="tegel-bekijk">Bekijk →</span><h2>{e(c["naam"])}</h2><p>{e(tekst or c["tekst"])}</p></a>')
    blok = (f'<section class="relevant" aria-label="Relevante producten en diensten"><h2 class="relevant-kop">Relevante producten en diensten</h2>'
            f'<div class="relevant-grid n{len(items)}">{tegels}</div>'
            + links_html(naam) + '</section>')
    p = site / naam
    s = p.read_text()
    s = re.sub(r'<section class="relevant".*?</section>', '', s, count=1, flags=re.S)
    assert '<section class="cta-brug">' in s, naam
    s = s.replace('<section class="cta-brug">', blok + '<section class="cta-brug">', 1)
    p.write_text(s)
    print("ok", naam, len(items))
