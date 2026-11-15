#!/usr/bin/env python3
"""Proef (15 nov): homepage als vast, beeldvullend vertrekpunt met 'kamers'.
Bouwt site/proef-home.html en per strip van de homepage een eigen pagina (proef-*.html).
De inhoud van de kamers wordt uit site/index.html gehaald, dus de proef volgt de echte homepage.
Niet gelinkt vanaf de site, noindex. De echte homepage blijft ongewijzigd."""
import pathlib, re, sys
site = pathlib.Path(__file__).resolve().parent.parent / "site"
s = (site / "index.html").read_text(encoding="utf-8")

def pak(patroon):
    m = re.search(patroon, s, re.S)
    if not m:
        sys.exit("NIET GEVONDEN op de homepage: " + patroon)
    return m.group(0)

icoon = pak(r"<!--icoon-->.*?<!--/icoon-->")
hero = pak(r'<section class="hero".*?</section>')
# volgorde = volgorde van de strips op de homepage
KAMERS = [
    ("proef-voor-wie.html", "Voor wie is HEAR", pak(r'<section class="samen".*?</section>')),
    ("nieuwjaarsborrel.html", "Organiseer je een nieuwjaarsborrel?", None),  # campagnestrook: bestaande actiepagina
    ("proef-cases.html", "Bekijk de cases", pak(r'<section class="werk".*?</section>\s*<script>.*?</script>')),
    ("proef-producten.html", "Hoogwaardige producten en diensten", pak(r'<section class="productlijst".*?\n  </section>')),
    ("proef-nieuws.html", "Recent nieuws en achtergronden", pak(r"<!--nieuws-home-->.*?<!--/nieuws-home-->")),
    ("proef-over.html", "Over HEAR", pak(r'<section class="over".*?</section>')),
]

KOP = """<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">{icoon}
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{titel}</title>
<link rel="stylesheet" href="home.css"><link rel="stylesheet" href="doelgroep.css"><link rel="stylesheet" href="proef.css">
</head>
"""

links = "".join(
    f'<a class="kamer-link{" kamer-actie" if inhoud is None else ""}" href="{bestand}"><span>{naam}</span><i aria-hidden="true">→</i></a>'
    for bestand, naam, inhoud in KAMERS
)
home = (
    KOP.format(icoon=icoon, titel="HEAR · proef: home als vertrekpunt")
    + '<body class="home proef">\n'
    + '<a class="proef-plan" href="aanvraag.html">Plan een gesprek</a>\n<main>\n'
    + hero
    + f'\n<nav class="kamers" aria-label="Kies een onderdeel">{links}</nav>\n</main>\n</body>\n</html>\n'
)
(site / "proef-home.html").write_text(home, encoding="utf-8")

for bestand, naam, inhoud in KAMERS:
    if inhoud is None:
        continue
    pagina = (
        KOP.format(icoon=icoon, titel=f"HEAR · proef: {naam}")
        + '<body class="home kamer">\n<header class="kamer-top">'
        + '<a class="kamer-terug" href="proef-home.html"><i aria-hidden="true">←</i><span>Terug naar home</span></a>'
        + '<a class="kamer-merk" href="proef-home.html" aria-label="HEAR, terug naar home"><img src="img/logo-white.png" alt="HEAR"></a>'
        + '<a class="proef-plan" href="aanvraag.html">Plan een gesprek</a></header>\n<main>\n'
        + inhoud
        + "\n</main>\n</body>\n</html>\n"
    )
    (site / bestand).write_text(pagina, encoding="utf-8")
print("proef-home.html en", sum(1 for k in KAMERS if k[2]), "kamers gebouwd")
