"""Bouwt site/privacy.html (privacyverklaring) met de kop en voet uit index.html.
Tekst staat hieronder; Engels via content/en.json (paginas → privacy.html). Draaien vóór bouw-en.py."""
import pathlib, html
root = pathlib.Path(__file__).resolve().parent.parent
site = root / "site"
idx = (site / "index.html").read_text()
kop = idx[idx.index('<header class="top">'):idx.index('</script>') + 9]
voet = idx[idx.index('<footer class="voet">'):idx.index('</footer>') + 9]
e = lambda t: html.escape(t, quote=True)

TITEL = "Privacyverklaring"
INTRO = "HEAR is een handelsnaam van Maarten Versteeg communicatieadvies (KvK 42181393, Van Kinsbergenstraat 54, 1057 PT Amsterdam). We gaan zorgvuldig om met je gegevens. Hieronder staat wat we verwerken en waarom."
BLOKKEN = [
    ("Wat we verwerken", [
        "Als je ons een bericht stuurt via WhatsApp, e-mail of het aanvraagformulier: je naam, organisatie, telefoonnummer, e-mailadres en wat je over je event invult. We gebruiken dit alleen om je vraag te beantwoorden en, bij een opdracht, voor de uitvoering en administratie daarvan. Het formulier wordt als e-mail aan ons bezorgd via Resend en niet op de website opgeslagen.",
        "Bij een opdracht: de gegevens die nodig zijn voor offerte, overeenkomst en factuur. Facturen bewaren we zeven jaar, zoals de wet voorschrijft. Andere gegevens bewaren we niet langer dan nodig voor het doel waarvoor je ze gaf.",
        "Deze website plaatst zelf geen cookies en gebruikt geen bezoekersstatistieken of trackers. Op de pagina over dj's staat een ingebouwde SoundCloud-player; die wordt door SoundCloud geleverd en kan cookies van SoundCloud plaatsen zodra je hem gebruikt.",
    ]),
    ("Technische dienstverleners", [
        "De website wordt gehost door Cloudflare. Bij het laden van een pagina ziet Cloudflare je IP-adres en de opgevraagde pagina, zoals elke hostingpartij.",
        "Berichten via WhatsApp (Meta) en e-mail (iCloud Mail van Apple) worden door die diensten verwerkt volgens hun eigen voorwaarden.",
        "We verkopen geen gegevens en delen ze niet met anderen, behalve als dat nodig is voor de uitvoering van een opdracht, bijvoorbeeld met een technicus of artiest uit ons netwerk, of als de wet dat verplicht.",
    ]),
    ("Je rechten", [
        "Je kunt inzage, correctie of verwijdering van je gegevens vragen via maarten@hear.nl. Ben je het niet eens met hoe we met je gegevens omgaan, dan kun je een klacht indienen bij de Autoriteit Persoonsgegevens.",
    ]),
]
DATUM = "Laatst bijgewerkt: 28 oktober 2026."

blokken = "".join(f'<h2 class="kopje">{e(k)}</h2>' + "".join(f"<p>{e(t)}</p>" for t in ts) for k, ts in BLOKKEN)
main = f'''<main class="wrap">
<section class="casehead"><a class="crumb" href="index.html"><span class="sectie">HEAR</span></a><h1>{e(TITEL)}</h1></section>
<article class="artikel"><p class="lead">{e(INTRO)}</p>{blokken}<p class="datum">{e(DATUM)}</p></article>
<nav class="verwijzingen" aria-label="Verder"><a href="index.html">Naar de homepage →</a></nav>
</main>'''
doc = f'''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(INTRO[:155])}"><title>{e(TITEL)} · HEAR</title><link rel="stylesheet" href="home.css"><link rel="stylesheet" href="styles.css"></head><body class="pagina">
{kop}
{main}
{voet}
</body></html>'''
(site / "privacy.html").write_text(doc)
print("ok privacy.html")
