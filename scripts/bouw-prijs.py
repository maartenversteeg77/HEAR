"""Bouwt site/prijs.html: wat kost audiovisuele ondersteuning van een evenement (geen prijslijst, wel uurtarieven).
Kop en voet uit index.html, teksten hieronder (Maarten, 20 okt 2026). Elk blok: links signaalwoord, rechts toelichting.
Engels via content/en.json (paginas → prijs.html). Draaien vóór bouw-en.py."""
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
BESCHRIJVING = "Wat audiovisuele ondersteuning van een evenement kost: techniek en dienstverlening. Met de uurtarieven van technici en projectmanagement en het verschil tussen dance events en zakelijke events."
BEELD = "img/systeem-breed.jpg"
BEELD_ALT = "Een geluidssysteem opgebouwd in een zaal, klaar voor een event"
INTRO = ["Bij HEAR verhuren we apparatuur alleen los aan relaties met eigen technici. Voor andere klanten is ons aanbod full service: advies, transport, op- en afbouw en bediening zijn inbegrepen.",
         "De prijs bestaat daarom uit twee delen: techniek en dienstverlening, van voorbereiding tot technici ter plekke."]

def regels(rijen):
    return '<dl class="regels">' + "".join(f'<div><dt>{e(k)}</dt><dd>{v}</dd></div>' for k, v in rijen) + '</dl>'
LINKS = ('<span class="dj-links"><a href="diensten.html">Producten en diensten →</a><a href="atmospheric-lighting.html">Sfeerverlichting →</a>'
         '<a href="dancefloor-lighting.html">Dansvloerverlichting →</a><a href="vintage-lighting.html">90\'s vintage licht →</a><a href="high-end-audio.html">Geluidssystemen →</a></span>')
prijs = lambda bedrag, eenheid: f'<strong class="bedrag">{e(bedrag)}</strong> <span class="eenheid">{e(eenheid)}</span><br>'

AANBOD = [
    # (naam, link, wat is het, voor wie, wat heb je eraan, wat kost het (html))
    ("Dry hire", "diensten.html", "Huur van losse apparatuur, zonder technicus.", "Alleen voor relaties met eigen professionele technici.",
     "Snel toegang tot gear van de nieuwste generatie, tegen scherpe prijzen.", e("Op aanvraag.") + ' <a href="diensten.html">Bekijk het assortiment →</a>'),
    ("Geluid en dj-set", "high-end-audio.html", "Geluidssysteem van RCF of Brooklyn Audio en desgewenst een rider-proof booth met CDJ-3000X, V10 of Euphonia en monitoring. Met transport, op- en afbouw en bediening.", "Elk type event, tot 1.500 personen.",
     "De nieuwste generatie versterking en DSP, nooit tweedehands. Helder tot achterin de zaal, zonder ruis of vervorming. Een dj komt binnen en kan meteen draaien.", 'Van <strong class="bedrag">500 euro</strong> voor een compacte cocktailparty tot <strong class="bedrag">1.500 euro</strong> voor de grootste dance stack in ons assortiment, met uitgebreide dj-booth en monitoring.'),
    ("Licht", "diensten.html", "Drie categorieën: sfeerverlichting, dansvloerverlichting en 90's vintage licht. Met transport, opbouw en programmering.", "Presentaties, zakelijke events en dansvloeren.",
     "Veelal draadloos: korte opbouw, geen kabels in zicht, geen versterkte stroom nodig.", e("Op aanvraag.") + ' <a href="diensten.html">Bekijk de drie categorieën →</a>'),
    ("Technicus", "high-end-audio.html", "Licht- of geluidstechnicus, van opbouw tot afbouw.", "Elk event met full service.",
     "Hij of zij heeft oog voor detail: of het geluid niet rondzingt, de microfoons geladen zijn en het draaiboek klopt. Ook met meerdere zalen tegelijk.", prijs("70 tot 100 euro", "per uur") + e("Afhankelijk van rol en ervaring.")),
    ("Communicatieadvies en projectmanagement", "corporate.html", "Meedenken over het concept, doorvertaling naar AV, draaiboek, aanspreekpunt op de dag.", "Vooral zakelijke events.",
     "Het doel van het event vertaald naar licht, geluid en programma, vastgelegd in een draaiboek. En op de dag één aanspreekpunt aanwezig, die zowel de communicatie als de techniek kent.", prijs("90 tot 120 euro", "per uur")),
    ("Dj", "artiesten.html", "Maarten of een dj uit ons netwerk.", "Zakelijke, privé- en dance events.",
     "Een dj die een avond kan opbouwen, van achtergrond bij de borrel tot een volle dansvloer. Muziek en techniek bij één partij.", prijs("vanaf 750 euro", "per avond") + e("Afhankelijk van de duur van de avond en de bekendheid van de dj.")),
    ("Vocalisten en instrumentalisten", "artiesten.html", "Saxofonist, zangeres of percussie bij de dj.", "Events waar live muziek iets toevoegt.",
     "Live muziek bij een dj-set geeft een event iets dat mensen onthouden.", e("Op aanvraag.")),
]
KOLOMMEN = ["Wat is het", "Voor wie", "Wat heb je eraan", "Wat kost het"]
rijen = "".join(
    f'<tr><th scope="row"><a href="{l}">{e(n)}</a></th>' + "".join(f'<td data-kop="{e(k)}">{v}</td>' for k, v in zip(KOLOMMEN, [e(a), e(b), e(c), d])) + '</tr>'
    for n, l, a, b, c, d in AANBOD)
tabel = ('<div class="tabelwrap aanbod"><table class="aanbodtabel"><thead><tr><th scope="col">Onderdeel</th>' + "".join(f'<th scope="col">{e(k)}</th>' for k in KOLOMMEN)
         + f'</tr></thead><tbody>{rijen}</tbody></table></div><p class="klein">Alle bedragen exclusief btw.</p>')

BLOKKEN = [
    ("Dance of zakelijk", [
        ("Dance events", e("Meestal meer grote (dure) systemen en technici, minder communicatie en projectmanagement.")),
        ("Zakelijke events", e("Vaak andersom: meer afstemming en coördinatie, en techniek die hoge eisen stelt aan verstaanbaarheid, maar minder aan volume.")),
        ("Verhouding", '<span class="verdeling" aria-label="Waar de prijs in zit, indicatief">'
                       '<span class="rij"><span class="naam">Dance</span><span class="balk"><i class="techniek" style="--w:68%">techniek</i><i class="uren" style="--w:32%">dienstverlening</i></span></span>'
                       '<span class="rij"><span class="naam">Zakelijk</span><span class="balk"><i class="techniek" style="--w:35%">techniek</i><i class="uren" style="--w:65%">dienstverlening</i></span></span>'
                       '<span class="bijschrift">Indicatief; het hoeft niet zo te zijn.</span></span>'),
    ]),
]

INVLOED = '<article class="case-section"><h2>WELKE ELEMENTEN HEBBEN INVLOED OP DE PRIJS?</h2><div><ul><li>de grootte, akoestiek en locatie van de ruimte</li><li>de grootte van de lichtshow en of er een trussconstructie nodig is</li><li>omvang en complexiteit van het programma: meerdere ruimtes, presentaties, video-instarts of andere zaken die vragen om aanwezigheid</li><li>de duur: hoe lang het event loopt en of het over meerdere dagen gaat</li></ul></div></article>'
secties = INVLOED + "".join(f'<article class="case-section"><h2>{e(l).upper()}</h2><div>{regels(r)}</div></article>' for l, r in BLOKKEN)
cta = f'<section class="cta-brug"><p class="lang">Geen intakeformulier: we horen liever in een gesprek wat je nodig hebt. Digitaal of op locatie.</p>{waknop("Vraag een intakegesprek aan", "Hoi Maarten, ik wil graag een intakegesprek over licht en geluid voor mijn event.")}</section>'

main = f'''<main class="wrap">
<section class="casehead"><a class="crumb" href="diensten.html"><span class="sectie">Producten</span><span class="scheiding" aria-hidden="true">|</span><span class="huidig">Wat kost het</span></a><h1 class="kernzin">{e(TITEL)}</h1><p class="eyebrow page-kicker">PRIJS</p></section>
<figure class="detail-image"><img src="{BEELD}" alt="{e(BEELD_ALT)}"></figure>
<section class="quick quick-breed">{"".join(f"<p>{e(t)}</p>" for t in INTRO)}</section>
<section class="aanbod-sectie">{tabel}</section>
<section class="case-sections">{secties}</section>
{cta}
<nav class="verwijzingen" aria-label="Verder"><a href="diensten.html">Alle producten en diensten →</a><a href="cases.html">Bekijk voorbeelden uit onze cases →</a></nav>
</main>'''
doc = f'''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(BESCHRIJVING)}"><meta name="robots" content="noindex"><title>Wat kost het · HEAR</title><link rel="stylesheet" href="home.css"><link rel="stylesheet" href="styles.css"></head><body class="pagina">
{kop}
{main}
{voet}
</body></html>'''
(site / "prijs.html").write_text(doc)
print("ok prijs.html")
