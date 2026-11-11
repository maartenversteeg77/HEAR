"""Bouwt site/partners.html (netwerkpartners) met de kop en voet uit index.html (11 nov).
Per partner een openklap met één zin wat zij doen (opgezocht op hun eigen site, 11 nov 2026) en een link.
Engels via content/en.json (paginas → partners.html). Draaien vóór bouw-en.py."""
import pathlib, html
root = pathlib.Path(__file__).resolve().parent.parent
site = root / "site"
idx = (site / "index.html").read_text()
kop = idx[idx.index('<header class="top">'):idx.index('</script>') + 9]
voet = idx[idx.index('<footer class="voet">'):idx.index('</footer>') + 9]
e = lambda t: html.escape(t, quote=True)

TITEL = "Netwerkpartners"
INTRO = "Zonder samenwerking bestaan we niet. Dit zijn de leveranciers, makers en vakgenoten met wie we werken."
GROEPEN = [
    ("Leveranciers", None, [
        ("Output Professional", "https://output.nl", "Distributeur van professionele audio, video en licht uit ’s-Hertogenbosch, en importeur van onder meer RCF."),
        ("Highlite", "https://www.highlite.com", "Fabrikant en groothandel in licht, geluid en video uit Kerkrade, het bedrijf achter onder meer Showtec."),
        ("Moonbears", "https://moonbears.eu", "Distributeur van licht en riggingmateriaal uit Breda, voor verhuurbedrijven, theaters en lichtontwerpers."),
        ("Chauvet Benelux", "https://chauvetprofessional.com", "De Benelux-tak van lichtmerk Chauvet: moving heads, washlights, effecten en besturing."),
        ("RCF", "https://www.rcf.it", "Italiaanse fabrikant van professionele luidsprekers en elektronica, sinds 1949."),
        ("Brooklyn Audio", "https://brooklyn-audio.com", "Nederlands merk van precisieluidsprekers."),
    ]),
    ("Muziek en media", None, [
        ("Architects in Music", "https://architectsinmusic.com", "Bureau voor muziek en entertainment in de hospitality, met artiestenboekingen, audio en AV."),
        ("IAMM Entertainment", "https://iammentertainment.com", "Entertainmentbureau uit Amsterdam dat dj’s en live muzikanten boekt voor clubs, festivals en bedrijfsevents."),
        ("Deep Radio", "https://deep.radio", "Online dance-radiostation dat 24 uur per dag uitzendt."),
        ("Ronald Pronk Photography", "https://ronaldpronk.com", "Event- en portretfotograaf, van corporate events tot festivals."),
    ]),
    ("Partners", "Met hen kunnen we opschalen voor grotere events.", [
        ("Base Events", "https://base-events.nl", "Full-service eventbureau uit Vianen met eigen licht, geluid, video en entertainment."),
        ("Biezema AV", "https://www.biezema-geluidsverhuur.nl", "Verhuur en verkoop van licht, beeld en geluid uit Stadskanaal, voor festivals, concerten en zakelijke events."),
        ("Luxonos", "https://luxonos.nl", "Audiovisuele dienstverlener uit Soest voor licht, geluid, video en podiumtechniek op beurzen en events."),
        ("Brandon AV", "https://brandon-av.nl", "Geluid, licht en video uit Hilversum voor festivals, beurzen en feesten."),
    ]),
]
EXTRA = "En diverse freelancers."
WEBSITE = "Naar de website →"

def groep(naam, sub, items, laatste):
    h = f'<h2 class="kopje">{e(naam)}</h2>'
    if sub: h += f'<p class="partner-sub">{e(sub)}</p>'
    h += '<div class="partner-lijst">' + "".join(
        f'<details class="partner"><summary>{e(n)}</summary><p>{e(t)} <a href="{u}" target="_blank" rel="noopener">{e(WEBSITE)}</a></p></details>'
        for n, u, t in items) + '</div>'
    if laatste: h += f'<p class="partner-extra">{e(EXTRA)}</p>'
    return h

blokken = "".join(groep(n, s, it, i == len(GROEPEN) - 1) for i, (n, s, it) in enumerate(GROEPEN))
main = f'''<main class="wrap">
<section class="casehead"><a class="crumb" href="over-hear.html"><span class="sectie">Over HEAR</span></a><h1>{e(TITEL)}</h1></section>
<article class="artikel"><p class="lead">{e(INTRO)}</p>{blokken}</article>
<nav class="verwijzingen" aria-label="Verder"><a href="over-hear.html">Founder story →</a><a href="principes.html">Waarden en uitgangspunten →</a></nav>
</main>'''
doc = f'''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(INTRO[:155])}"><title>{e(TITEL)} · HEAR</title><link rel="stylesheet" href="home.css"><link rel="stylesheet" href="styles.css"></head><body class="pagina">
{kop}
{main}
{voet}
</body></html>'''
(site / "partners.html").write_text(doc)
print("ok partners.html")
