"""Bouwt site/prijs.html: wat kost audiovisuele ondersteuning van een evenement (geen prijslijst, wel uurtarieven).
Kop en voet uit index.html, teksten hieronder (van Maarten, 20 okt 2026). Engels via content/en.json (paginas → prijs.html). Draaien vóór bouw-en.py."""
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
BESCHRIJVING = "Wat audiovisuele ondersteuning van een evenement kost: huur van apparatuur en uren. Met de uurtarieven van technici en projectmanagement en het verschil tussen dance events en zakelijke events."
BEELD = "img/systeem-breed.jpg"
BEELD_ALT = "Een geluidssysteem opgebouwd in een zaal, klaar voor een event"
INTRO = ["Bij HEAR verhuren we apparatuur alleen los aan relaties met eigen technici. Voor andere klanten is ons aanbod full service: advies, transport, op- en afbouw en bediening zijn inbegrepen.",
         "De prijs bestaat daarom uit twee delen: de apparatuur en de uren."]

P = lambda t: f"<p>{e(t)}</p>"
blok_apparatuur = "".join(P(t) for t in [
    "Voor apparatuur rekenen we huurprijzen die gangbaar zijn in die categorie. Wat je daarvoor krijgt: hoogwaardige, storingsvrije apparatuur van de nieuwste generatie, modulair inzetbaar. We volgen de techniek en vervangen apparatuur zodra de technologie in een categorie een sprong maakt. Met RCF en Brooklyn Audio zitten we op de laatste stand van versterking en DSP; alle dj-gear is laatste generatie en bij nieuwe releases gaan we daarin mee. Tweedehands kopen we niet: draaiuren hoor je terug in ruis en vervorming.",
    "Verder bepaalt de prijs welk licht het event nodig heeft, of er truss nodig is en welk geluid. Daar adviseren we over; via ons netwerk is het aanbod uit te breiden.",
    "Bij dance events is vooral de ruimte bepalend. Een heel diepe zaal betekent extra speakers. Een forward dj-booth ook. Een heel brede zaal of meerdere zones vraagt extra delays. En moet er een trussconstructie gebouwd worden, of kan het licht al ergens hangen?",
]) + ('<p class="dj-links"><a href="diensten.html">Kijk alvast welke producten en diensten wij in huis hebben →</a>'
      '<a href="atmospheric-lighting.html">Sfeerverlichting →</a><a href="dancefloor-lighting.html">Dansvloerverlichting →</a><a href="vintage-lighting.html">90\'s vintage licht →</a><a href="high-end-audio.html">Geluidssystemen →</a></p>')

blok_uren = ('<dl class="tarieven">'
             '<div><dt>Technicus licht of geluid</dt><dd><strong>70 tot 100 euro</strong> per uur</dd><dd class="uitleg">Afhankelijk van rol en ervaring.</dd></div>'
             '<div><dt>Communicatieadvies of projectmanagement</dt><dd><strong>90 tot 120 euro</strong> per uur</dd><dd class="uitleg">Meedenken over het concept, doorvertaling naar AV, ontwikkelen van een draaiboek, aanspreekpunt op een bedrijfsevent.</dd></div>'
             '<div><dt>Dj</dt><dd><strong>vanaf 750 euro</strong> per avond</dd><dd class="uitleg">Afhankelijk van de duur van de avond en of het een professionele dj zonder gevestigde naam is of een dj met bekendheid. Aanvullende artiesten op aanvraag.</dd></div>'
             '</dl><p class="klein">Bedragen exclusief btw.</p>'
             + P("Waarom die uren tellen: stel, een CEO heeft een week lang een speech voorbereid, of een expert een TED-talk. En een microfoon blijkt niet opgeladen. Of een galmende zaal waarin je de helft verstaat, of een microfoon die rondzingt. Dat soort dingen maakt dat een event valt of staat. Technici ter plekke, soms meerdere breakout rooms bij seminars, presentaties en video's die vertoond moeten worden: dat vraagt om handen aan de knoppen."))

blok_verschil = P("Meestal vraagt een dance event meer van grote (dure) systemen en technici, en minder van communicatie en projectmanagement. Bij zakelijke events is het vaak andersom: meer afstemming en coördinatie, en techniek die hoge eisen stelt aan verstaanbaarheid, maar minder aan volume.") + '''<figure class="verdeling" aria-label="Waar de prijs in zit, indicatief">
<div class="rij"><span class="naam">Dance events</span><span class="balk"><i class="techniek" style="--w:68%">techniek</i><i class="uren" style="--w:32%">uren</i></span></div>
<div class="rij"><span class="naam">Zakelijke events</span><span class="balk"><i class="techniek" style="--w:35%">techniek</i><i class="uren" style="--w:65%">uren</i></span></div>
<figcaption>Indicatief: de verhouding verschilt per event.</figcaption></figure>'''

blok_efficiency = "".join(P(t) for t in [
    "Efficiënt zijn we op twee manieren. Met techniek die de opbouwtijd verkort, zoals draadloos licht. En door communicatie en licht en geluid in één hand te houden, of licht en geluid en dj's en artiesten.",
    "Daardoor kunnen we voor high-end gear en ondersteuning een concurrerende prijs vragen.",
])

def blok(label, body):
    return f'<article class="case-section"><h2>{e(label).upper()}</h2><div>{body}</div></article>'

secties = blok("Apparatuur", blok_apparatuur) + blok("Uren", blok_uren) + blok("Dance of zakelijk", blok_verschil) + blok("Efficiëntie", blok_efficiency)
cta = f'<section class="cta-brug"><p class="lang">Geen intakeformulier: we horen liever in een gesprek wat je nodig hebt. Digitaal of op locatie.</p>{waknop("Vraag een intakegesprek aan", "Hoi Maarten, ik wil graag een intakegesprek over licht en geluid voor mijn event.")}</section>'

main = f'''<main class="wrap">
<section class="casehead"><a class="crumb" href="diensten.html"><span class="sectie">Producten</span><span class="scheiding" aria-hidden="true">|</span><span class="huidig">Wat kost het</span></a><h1 class="kernzin">{e(TITEL)}</h1><p class="eyebrow page-kicker">PRIJS</p></section>
<figure class="detail-image"><img src="{BEELD}" alt="{e(BEELD_ALT)}"></figure>
<section class="quick quick-breed">{"".join(P(t) for t in INTRO)}</section>
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
