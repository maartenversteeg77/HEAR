"""Bouwt site/prijs.html: wat kost audiovisuele ondersteuning van een evenement.
Terug naar de basis (Maarten, 21 okt 2026): zakelijk als deel van het eventbudget, dance als marktconforme huur, plus uurtarieven.
Elk blok: links signaalwoord, rechts toelichting. Engels via content/en.json (paginas → prijs.html). Draaien vóór bouw-en.py."""
import pathlib, html, urllib.parse
root = pathlib.Path(__file__).resolve().parent.parent
site = root / "site"
idx = (site / "index.html").read_text()
kop = idx[idx.index('<header class="top">'):idx.index('</script>') + 9]
voet = idx[idx.index('<footer class="voet">'):idx.index('</footer>') + 9]
e = lambda t: html.escape(t, quote=True)
SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2c0 1.3.9 2.5 1.1 2.7.1.2 1.8 2.8 4.4 3.9 1.7.7 2.3.8 3.1.7.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2l-.8-.3Z"/></svg>'
def waknop(tekst, bericht):
    return (f'<span class="wa-plus"><a class="wa" href="https://wa.me/31624560220?text={urllib.parse.quote(bericht)}" target="_blank" rel="noopener" data-whatsapp>{SVG}<span>{e(tekst)}</span><i aria-hidden="true">→</i></a>'
            f'<a class="mail-ook" href="mailto:maarten@hear.nl">mailen mag ook</a></span>')

TITEL = "Wat kost audiovisuele ondersteuning van een evenement?"
BESCHRIJVING = "Wat licht en geluid voor een evenement kost: bij zakelijke events 10 tot 20 procent van het eventbudget, bij dance events een gangbare huurprijs. Met uurtarieven en dj-tarief."
BEELD = "img/systeem-breed.jpg"
BEELD_ALT = "Een geluidssysteem opgebouwd in een zaal, klaar voor een event"
INTRO = ["Elk event is maatwerk, dus een prijs maken we altijd op aanvraag. Waar het kan, vind je op deze pagina een indicatie."]

def regels(rijen):
    return '<dl class="regels">' + "".join(f'<div><dt>{e(k)}</dt><dd>{v}</dd></div>' for k, v in rijen) + '</dl>'
b = lambda t: f'<strong class="bedrag">{e(t)}</strong>'

BLOKKEN = [
    ("Zakelijke events", [
        ("Richtlijn", b("10 tot 20 procent") + e(" van het eventbudget.")),
        ("Basis", e("Rond 10 procent: licht, geluid en sprekersversterking.")),
        ("Uitgebreid", e("Rond 20 procent: met aanvullende dienstverlening, zoals een online uitzending, videoschermen, digitaal stemmen, een paneldiscussie, videoproductie, een aftermovie of fotografie.")),
        ("Ook bepalend", e("Hoe complex het draaiboek is, hoeveel ruimtes er zijn en hoeveel technici er nodig zijn.")),
    ]),
    ("Dance events", [
        ("Richtlijn", e("Een huurprijs die gebruikelijk is in de markt voor vergelijkbare apparatuur.")),
        ("Wat je krijgt", e("Apparatuur van de laatste generatie, per event zorgvuldig gekozen en samengesteld voor de ruimte en het type event.")),
    ]),
    ("Tarieven", [
        ("Technicus licht of geluid", b("70 tot 100 euro") + e(" per uur")),
        ("Communicatieadvies", b("90 tot 120 euro") + e(" per uur. Denkt mee over het eventconcept en het programma. Ook in te zetten voor strategische communicatie, zoals de boodschap, speechwriting, een storyline en de creatie van een video.")),
        ("AV-projectmanagement", b("90 tot 120 euro") + e(" per uur. Vertaalt het eventconcept naar een licht- en geluidsplan, plant de technici, maakt het draaiboek en is ter plekke het vaste aanspreekpunt.")),
        ("Eén persoon", e("Beide rollen kunnen door één persoon worden uitgevoerd.")),
        ("Dj", b("vanaf 750 euro") + e(" per avond")),
        ("Dj met (inter)nationale bekendheid", e("Op aanvraag")),
        ("Saxofonist, vocalist of percussionist", e("Op aanvraag")),
        ("Btw", e("Alle bedragen exclusief btw.")),
    ]),
]
LIJST = ["de grootte, akoestiek en locatie van de ruimte",
         "de grootte van de lichtshow en of er een trussconstructie nodig is",
         "omvang en complexiteit van het programma: meerdere ruimtes, presentaties, video-instarts of andere zaken die vragen om aanwezigheid",
         "de duur: hoe lang het event loopt en of het over meerdere dagen gaat"]
INVLOED = ('<article class="case-section"><h2>WELKE ELEMENTEN HEBBEN INVLOED OP DE PRIJS?</h2><div><ul>' + "".join(f"<li>{e(x)}</li>" for x in LIJST) + '</ul>'
           + '<p class="knoprij">' + waknop("Vraag een intakegesprek aan", "Hoi Maarten, ik wil graag een intakegesprek over licht en geluid voor mijn event.") + '</p></div></article>')

secties = "".join(f'<article class="case-section"><h2>{e(l).upper()}</h2><div>{regels(r)}</div></article>' for l, r in BLOKKEN) + INVLOED

main = f'''<main class="wrap prijspagina">
<section class="casehead"><a class="crumb" href="diensten.html"><span class="sectie">Producten</span><span class="scheiding" aria-hidden="true">|</span><span class="huidig">Wat kost het</span></a><h1 class="kernzin">{e(TITEL)}</h1><p class="eyebrow page-kicker">PRIJS</p></section>
<figure class="detail-image"><img src="{BEELD}" alt="{e(BEELD_ALT)}"></figure>
<section class="quick quick-breed">{"".join(f"<p>{e(t)}</p>" for t in INTRO)}</section>
<section class="case-sections">{secties}</section>
<nav class="verwijzingen" aria-label="Verder"><a href="diensten.html">Alle producten en diensten →</a><a href="cases.html">Bekijk voorbeelden uit onze cases →</a></nav>
</main>'''
doc = f'''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(BESCHRIJVING)}"><meta name="robots" content="noindex"><title>Wat kost het · HEAR</title><link rel="stylesheet" href="home.css"><link rel="stylesheet" href="styles.css"></head><body class="pagina">
{kop}
{main}
{voet}
</body></html>'''
(site / "prijs.html").write_text(doc)
print("ok prijs.html")
