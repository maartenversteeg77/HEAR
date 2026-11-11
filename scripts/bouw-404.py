"""Bouwt site/404.html en site/en/404.html (11 nov). Cloudflare toont die bij elk onbekend adres (not_found_handling: 404-page),
dus alle links en bronnen zijn absoluut. noindex; niet in sitemap. Draaien na bouw-en, vóór bouw-icoon."""
import pathlib, re
site = pathlib.Path(__file__).resolve().parent.parent / "site"
TEKST = {
    "nl": ("Deze pagina bestaat niet (meer)", "Misschien kwam je via een oude link. Hieronder vind je de weg terug.",
           [("/", "Naar de homepage"), ("/cases.html", "Bekijk de cases"), ("/diensten.html", "Producten en diensten"), ("/aanvraag.html", "Plan een gesprek")]),
    "en": ("This page doesn’t exist (anymore)", "You may have followed an old link. Here’s the way back.",
           [("/en/", "To the homepage"), ("/en/cases.html", "See the cases"), ("/en/diensten.html", "Products and services"), ("/en/aanvraag.html", "Plan a call")]),
}
def absoluut(s, pre):
    s = re.sub(r'(href|src)="(?!https?:|/|#|mailto:|tel:|data:)([^"]*)"', lambda m: f'{m.group(1)}="{pre}{m.group(2)}"', s)
    return s
for taal, (titel, lead, links) in TEKST.items():
    bron = site / ("index.html" if taal == "nl" else "en/index.html")
    pre = "/" if taal == "nl" else "/en/"
    idx = bron.read_text()
    kop = absoluut(idx[idx.index('<header class="top">'):idx.index('</script>') + 9], pre)
    voet = absoluut(idx[idx.index('<footer class="voet">'):idx.index('</footer>') + 9], pre)
    css = "/" if taal == "nl" else "/"
    nav = "".join(f'<a href="{u}">{t} →</a>' for u, t in links)
    doc = f'''<!doctype html><html lang="{taal}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>{titel} · HEAR</title><link rel="stylesheet" href="/home.css"><link rel="stylesheet" href="/styles.css"></head><body class="pagina">
{kop}
<main class="wrap"><section class="casehead"><h1>{titel}</h1></section><article class="artikel"><p class="lead">{lead}</p></article>
<nav class="verwijzingen" aria-label="Verder">{nav}</nav></main>
{voet}
</body></html>'''
    doel = site / ("404.html" if taal == "nl" else "en/404.html")
    doel.write_text(doc); print("ok", doel.name, taal)
