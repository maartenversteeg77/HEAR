"""Bouwt site/prijs.html: wat bepaalt de prijs (geen prijslijst). Kop en voet uit index.html, teksten hieronder.
Engels via content/en.json (paginas → prijs.html). Draaien vóór bouw-en.py."""
import pathlib, html, sys, importlib.util
root = pathlib.Path(__file__).resolve().parent.parent
site = root / "site"
idx = (site / "index.html").read_text()
kop = idx[idx.index('<header class="top">'):idx.index('</script>') + 9]
voet = idx[idx.index('<footer class="voet">'):idx.index('</footer>') + 9]
e = lambda t: html.escape(t, quote=True)
spec = importlib.util.spec_from_file_location("bd", root / "scripts" / "bouw-diensten.py")
# waknop hergebruiken zonder de hele bouw te draaien: zelfde markup als elders
import urllib.parse
SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2c0 1.3.9 2.5 1.1 2.7.1.2 1.8 2.8 4.4 3.9 1.7.7 2.3.8 3.1.7.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2l-.8-.3Z"/></svg>'
def waknop(tekst, bericht):
    return (f'<span class="wa-plus"><a class="wa" href="https://wa.me/31624560220?text={urllib.parse.quote(bericht)}" target="_blank" rel="noopener" data-whatsapp>{SVG}<span>{e(tekst)}</span><i aria-hidden="true">→</i></a>'
            f'<a class="mail-ook" href="mailto:maarten@hear.nl">mailen mag ook</a></span>')

TITEL = "Wat bepaalt de prijs"
KERNZIN = "Wat de prijs bepaalt: de ruimte, het licht en de uren"
BESCHRIJVING = "Wat de prijs van licht en geluid voor een event bepaalt: de ruimte, het licht, de uren. Met uurtarieven en een dj-tarief vanaf."
BEELD = "img/systeem-breed.jpg"
BEELD_ALT = "Een geluidssysteem opgebouwd in een zaal, klaar voor een event"
INTRO = "Bij een dance event betaal je vooral voor techniek. Bij een zakelijk event vooral voor uren en aandacht."

# Blokken: (label, [alinea's], extra html)
BLOKKEN = [
    ("Techniek of uren", [
        "Bij dance events zit de prijs vooral in de techniek: een geluidssysteem dat bij de ruimte past, licht, en de uren om het op te bouwen en te bedienen.",
        "Bij zakelijke events zit de prijs vooral in uren: afstemming vooraf, een draaiboek en handen aan de knoppen op de dag zelf. De apparatuur is er wel, maar is zelden de grootste post.",
    ], "GRAFIEK"),
    ("Dance events", [
        "Vooral de ruimte. Een heel diepe zaal betekent extra speakers. Een forward dj-booth ook. Een heel brede zaal of meerdere zones vraagt extra delays.",
        "Verder: wil je vooral sfeerverlichting, of ook dansvloerverlichting en eventueel vintage licht, inclusief programmering en lichtjockey? En moet er een trussconstructie gebouwd worden, of kan het licht al ergens hangen?",
        "Optioneel, via partners in ons netwerk: videoschermen met vj's (animaties) of videoclips (officiële muziekvideo's).",
    ], "LINKS_LICHT"),
    ("Zakelijke events", [
        "Stel: een CEO heeft een week lang een speech voorbereid, of een expert een TED-talk. En een microfoon blijkt niet opgeladen. Of een galmende zaal waarin je de helft verstaat, of een microfoon die rondzingt. Dat soort dingen maakt dat een event valt of staat.",
        "Daarom gaan er meer uren in dan apparatuur: de afstemming over het eventconcept en de doelstelling, het samen opstellen en uitvoeren van een draaiboek, aanwezigheid ter plekke voor vragen en troubleshooting. Technici ter plekke, soms meerdere breakout rooms bij seminars, presentaties en video's die vertoond moeten worden.",
    ], "TABEL"),
    ("Tarieven", [], "TARIEVEN"),
    ("Opbouwtijd", [
        "Onze technologie, zoals draadloos licht, vraagt een hogere voorinvestering, maar zorgt voor een efficiënte opbouwtijd. Minder uren op locatie, minder uren op de factuur.",
    ], ""),
    ("Dry hire", [
        "Losse apparatuur verhuren zonder technicus doen we niet, behalve voor bestaande partners.",
    ], ""),
]

# tabel: wat bepaalt de prijs, dance versus zakelijk
TABEL = [
    ("Grootste post", "Techniek: geluidssysteem en licht", "Uren: voorbereiding en bediening"),
    ("Bepaald door", "Diepte en breedte van de zaal, aantal zones, soort licht, truss", "Programma, aantal zalen, sprekers en video, mate van ontzorging"),
    ("Op de dag", "Opbouw, soundcheck, lichtjockey", "Technici bij elke zaal, handen aan de knoppen"),
    ("Via partners", "Videoschermen met vj's of videoclips", "Online uitzending, registratie"),
]

def blok_html(label, ps, extra):
    body = "".join(f"<p>{e(t)}</p>" for t in ps)
    if extra == "GRAFIEK":
        body += '''<figure class="verdeling" aria-label="Waar de prijs in zit, indicatief">
<div class="rij"><span class="naam">Dance events</span><span class="balk"><i class="techniek" style="--w:68%">techniek</i><i class="uren" style="--w:32%">uren</i></span></div>
<div class="rij"><span class="naam">Zakelijke events</span><span class="balk"><i class="techniek" style="--w:35%">techniek</i><i class="uren" style="--w:65%">uren</i></span></div>
<figcaption>Indicatief: de verhouding verschilt per event.</figcaption></figure>'''
    elif extra == "LINKS_LICHT":
        body += ('<p class="dj-links"><a href="atmospheric-lighting.html">Sfeerverlichting →</a><a href="dancefloor-lighting.html">Dansvloerverlichting →</a>'
                 '<a href="vintage-lighting.html">90\'s vintage licht →</a><a href="high-end-audio.html">Geluidssystemen →</a></p>')
    elif extra == "TABEL":
        rijen = "".join(f"<tr><th scope=\"row\">{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td></tr>" for a, b, c in TABEL)
        body += f'<div class="tabelwrap"><table class="prijstabel"><thead><tr><th scope="col"></th><th scope="col">Dance events</th><th scope="col">Zakelijke events</th></tr></thead><tbody>{rijen}</tbody></table></div>'
    elif extra == "TARIEVEN":
        body = ('<dl class="tarieven">'
                '<div><dt>Communicatie-uren</dt><dd><strong>100 euro</strong> per uur</dd><dd class="uitleg">Afstemming, draaiboek en voorbereiding.</dd></div>'
                '<div><dt>Techniek-uren</dt><dd><strong>70 tot 100 euro</strong> per uur</dd><dd class="uitleg">Op de dag zelf, afhankelijk van senioriteit.</dd></div>'
                '<div><dt>Dj</dt><dd><strong>vanaf 750 euro</strong> per avond</dd><dd class="uitleg">Afhankelijk van de duur van de avond en of het een professionele dj zonder gevestigde naam is of een dj met bekendheid. Aanvullende artiesten op aanvraag.</dd></div>'
                '</dl><p class="klein">Exclusief btw.</p>')
    return f'<article class="case-section"><h2>{e(label).upper()}</h2><div>{body}</div></article>'

secties = "".join(blok_html(*b) for b in BLOKKEN)
cta = f'<section class="cta-brug"><p>Wat vraagt jouw event?</p>{waknop("Stuur je ruimte en wensen", "Hoi Maarten, ik wil graag weten wat licht en geluid voor mijn event vraagt.")}</section>'

main = f'''<main class="wrap">
<section class="casehead"><a class="crumb" href="diensten.html"><span class="sectie">Producten</span><span class="scheiding" aria-hidden="true">|</span><span class="huidig">Wat bepaalt de prijs</span></a><h1 class="kernzin">{e(KERNZIN)}</h1><p class="eyebrow page-kicker">PRIJS</p></section>
<figure class="detail-image"><img src="{BEELD}" alt="{e(BEELD_ALT)}"></figure>
<section class="quick quick-breed"><p>{e(INTRO)}</p></section>
<section class="case-sections">{secties}</section>
{cta}
<nav class="verwijzingen" aria-label="Verder"><a href="diensten.html">Alle producten en diensten →</a><a href="cases.html">Bekijk voorbeelden uit onze cases →</a></nav>
</main>'''
doc = f'''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(BESCHRIJVING)}"><meta name="robots" content="noindex"><title>{e(TITEL)} · HEAR</title><link rel="stylesheet" href="home.css"><link rel="stylesheet" href="styles.css"></head><body class="pagina">
{kop}
{main}
{voet}
</body></html>'''
(site / "prijs.html").write_text(doc)
print("ok prijs.html")
