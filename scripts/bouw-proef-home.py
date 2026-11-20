#!/usr/bin/env python3
"""Proef (15 nov): homepage als vast, beeldvullend vertrekpunt.
Bouwt site/proef-home.html en van vijf bestaande pagina's een proefkopie (proef-*.html)
waarin het menu is vervangen door een balk met 'Terug naar home'.
De kopieën worden uit de echte pagina's gemaakt, dus draai dit script als laatste in de build.
Niet gelinkt vanaf de site, noindex. De echte pagina's blijven ongewijzigd."""
import pathlib, re, sys
site = pathlib.Path(__file__).resolve().parent.parent / "site"
s = (site / "index.html").read_text(encoding="utf-8")

def pak(tekst, patroon, waar):
    m = re.search(patroon, tekst, re.S)
    if not m:
        sys.exit(f"NIET GEVONDEN in {waar}: {patroon}")
    return m

icoon = pak(s, r"<!--icoon-->.*?<!--/icoon-->", "index.html").group(0)
hero = pak(s, r'<section class="hero".*?</section>', "index.html").group(0)
# (bronpagina, proefkopie, linktekst = kop van de strip op de homepage), in de volgorde van de strips
KAMERS = [
    ("doelgroepen.html", "proef-doelgroepen.html", "Voor wie is HEAR"),
    ("cases.html", "proef-cases.html", "Bekijk de cases"),
    ("diensten.html", "proef-diensten.html", "Hoogwaardige producten en diensten"),
    ("nieuws/index.html", "proef-nieuws.html", "Recent nieuws en achtergronden"),
    ("over-hear.html", "proef-over-hear.html", "Over HEAR"),
]

links = "".join(f'<a class="kamer-link" href="/{doel}"><span>{naam}</span><i aria-hidden="true">→</i></a>' for _, doel, naam in KAMERS)
home = f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">{icoon}
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>HEAR · proef: home als vertrekpunt</title>
<link rel="stylesheet" href="home.css"><link rel="stylesheet" href="doelgroep.css"><link rel="stylesheet" href="proef.css">
</head>
<body class="home proef">
<a class="proef-plan" href="aanvraag.html">Vertel over je event</a>
<main>
{hero}
<nav class="kamers" aria-label="Kies een onderdeel">{links}</nav>
</main>
</body>
</html>
"""
(site / "proef-home.html").write_text(home, encoding="utf-8")

BALK = ('<header class="kamer-top"><a class="kamer-terug" href="/proef-home.html"><i aria-hidden="true">←</i><span>Terug naar home</span></a>'
        '<a class="kamer-merk" href="/proef-home.html" aria-label="HEAR, terug naar home"><img src="/img/logo-white.png" alt="HEAR"></a>'
        '<a class="proef-plan" href="/aanvraag.html">Vertel over je event</a></header>')
for bron, doel, naam in KAMERS:
    t = (site / bron).read_text(encoding="utf-8")
    m = pak(t, r'<header class="top">.*?</header>\s*<div class="menu" id="menu" hidden>.*?</div>\s*<script>.*?</script>', bron)
    t = t[:m.start()] + BALK + t[m.end():]
    t = re.sub(r"<!--og-->.*?<!--/og-->", "", t, flags=re.S)                      # geen canonical of deelgegevens
    t = re.sub(r'<meta name="robots"[^>]*>', "", t)
    t = t.replace("</head>", '<meta name="robots" content="noindex,nofollow"><link rel="stylesheet" href="/proef.css">\n</head>', 1)
    t = re.sub(r'<body class="([^"]*)"', r'<body class="\1 kamer"', t, count=1)
    t = re.sub(r'(<a class="crumb" href=")(?:/?index\.html|/)(")', r"\1/proef-home.html\2", t)
    (site / doel).write_text(t, encoding="utf-8")
print("proef-home.html en", len(KAMERS), "proefkopieën gebouwd")
