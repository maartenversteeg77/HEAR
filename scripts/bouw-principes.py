"""Bouwt site/principes.html uit content/principes.json: één pagina met de jogwheel.
Elk principe: titel (op het display), statement (regel onder de titel), intro, en de uitleg onder
"Waar merk je dit aan?". Geen subpagina's, geen doorklik. Een anker (#slug) opent dat principe.
Kop, menu en voet komen uit site/index.html. Draaien na elke wijziging: python3 scripts/bouw-principes.py"""
import json, html, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
site = root / "site"
data = json.loads((root / "content" / "principes.json").read_text())
idx = (site / "index.html").read_text()
kop = idx[idx.index('<header class="top">'):idx.index('</script>') + 9]
kop = kop.replace('href="principes.html">', 'href="principes.html" aria-current="page">', 1)
voet = idx[idx.index('<footer class="voet">'):idx.index('</footer>') + 9]
e = lambda t: html.escape(t, quote=True)

items = []
for p in data["paginas"]:
    st = p.get("statement") or (p["kernzin"].split(":", 1)[1].strip() if ":" in p["kernzin"] else p["kernzin"])
    st = st[0].upper() + st[1:]
    waar = p.get("waar")
    if waar is None and "blokken" in p:  # oude structuur
        bl = p["blokken"]
        waar = [t for b in bl if b["label"] == "Wat je ervan merkt" for t in b["tekst"]] + \
               [t for b in bl if b["label"] != "Wat je ervan merkt" for t in b["tekst"]]
    items.append({"slug": p.get("slug") or p.get("bestand", "").replace(".html", ""), "titel": p["titel"],
                  "statement": st, "intro": p["intro"], "principes": p.get("principes", []), "waar": waar})

kernzin = data.get("kernzin", "Principes en way of working")
intro = data.get("intro", "")
beschrijving = intro or " · ".join(i["titel"] for i in items)
pagina = f'''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(beschrijving[:155])}"><title>Principes en way of working · HEAR</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Advent+Pro:wght@300;400;500&display=swap" rel="stylesheet"><link rel="stylesheet" href="home.css"><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="jog.css"></head><body class="pagina">
{kop}
<main class="wrap">
<section class="casehead"><a class="crumb" href="index.html"><span class="sectie">HEAR</span></a><h1 class="kernzin">{e(kernzin)}</h1></section>
{f'<section class="quick quick-breed"><p>{e(intro)}</p></section>' if intro else ''}
<section class="jogmidden">
  <button class="jog" id="jog" type="button" aria-label="Volgend principe">
    <div class="rand"></div><div class="kuiltjes" id="kuiltjes"></div><div class="chroom"></div>
    <div class="ringdonker"></div><div class="zij"></div>
    <div class="wit"></div><div class="wijzer" id="wijzer"><i></i></div><div class="koraal"></div>
    <div class="scherm" id="scherm"><strong id="titel"></strong></div>
  </button>
  <div class="jogtekst" id="tekst" aria-live="polite"></div>
</section>
</main>
{voet}
<script>window.JOG={{midden:true,items:{json.dumps(items, ensure_ascii=False)}}};</script><script src="jog.js"></script>
</body></html>'''
(site / "principes.html").write_text(pagina)
print("ok principes.html")
