"""Bouwt het casesoverzicht (site/cases.html) uit site/cases.json.
Eén bron: titels, doelgroepen, teksten en beelden pas je aan in cases.json; daarna dit script draaien.
Alleen cases met status 'af' komen in het overzicht, in de volgorde van cases.json.
Labels = doelgroepen, elk met een link naar de Voor wie-pagina van die doelgroep."""
import json, html, re, pathlib
site = pathlib.Path(__file__).resolve().parent.parent / "site"
data = json.loads((site / "cases.json").read_text())
dg = data["doelgroepen"]
e = lambda t: html.escape(t, quote=True)
def tegel(c):
    pos = f' style="object-position:{e(c["positie"])}"' if c.get("positie") else ""
    labels = "".join(f'<a href="{e(dg[k]["link"])}">{e(dg[k]["naam"])}</a>' for k in c["doelgroepen"])
    return (f'<article class="case-tegel"><img src="{e(c["beeld"])}" alt="{e(c["alt"])}" loading="lazy"{pos}>'
            f'<div class="case-tekst"><p class="labels">{labels}</p>'
            f'<h2><a class="tegel-link" href="{e(c["link"])}">{e(c["titel"])}</a></h2>'
            f'<p>{e(c["tekst"])}</p><span class="pijl" aria-hidden="true">→</span></div></article>')
tegels = "".join(tegel(c) for c in data["cases"] if c.get("status") == "af")
p = site / "cases.html"
s = p.read_text()
s, n = re.subn(r'<section class="[^"]*(?:case-index-grid|case-overzicht)[^"]*">.*?</section>',
               lambda m: f'<section class="case-overzicht"><!-- gegenereerd uit cases.json door scripts/bouw-cases.py -->{tegels}</section>',
               s, count=1, flags=re.S)
p.write_text(s)
print("tegels:", tegels.count("case-tegel"), "vervangen:", n)
