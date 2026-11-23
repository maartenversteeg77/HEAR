#!/usr/bin/env python3
"""Bouwt site/coffeecuts-trial.html (23 nov 2026): landingspagina voor de LinkedIn-advertentie waarmee een zaak
(horeca of winkel) gratis één Coffee cuts- of Cocktail cuts-playlist kan bestellen.
Kop, menu, voet en de scripts voor het formulier en de herkomst (utm) komen uit site/nieuwjaarsborrel.html:
draai dit script dus na bouw-doelgroepen en vóór bouw-og. Niet in het menu, noindex, alleen Nederlands.
Het formulier post naar /api/aanvraag (src/index.js) met bron 'Landingspagina Coffee cuts trial'."""
import pathlib, re, sys, html
site = pathlib.Path(__file__).resolve().parent.parent / "site"
basis = (site / "nieuwjaarsborrel.html").read_text(encoding="utf-8")
i = basis.index('<main class="wrap lp">')
kop, staart = basis[:i], basis[basis.index("</main>") + 7:]
if "lp-form" not in staart or 'name="utm"' not in staart:
    sys.exit("formulier- of utm-script niet gevonden in nieuwjaarsborrel.html")

def e(t):
    return html.escape(t, quote=True)

TITEL = "Probeer gratis één playlist voor je zaak | HEAR"
OMSCHR = "Coffee cuts en Cocktail cuts: warme muziek die past bij je zaak. Bestel gratis één playlist op maat."
DEELTITEL = "Gratis playlist voor je zaak"

kop = re.sub(r"<title>.*?</title>", f"<title>{e(TITEL)}</title>", kop, count=1, flags=re.S)
kop = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(OMSCHR)}">', kop, count=1)
kop = re.sub(r'<meta name="deeltitel" content="[^"]*">', f'<meta name="deeltitel" content="{e(DEELTITEL)}">', kop, count=1)
kop = re.sub(r"<!--og-->.*?<!--/og-->", "<!--og--><!--/og-->", kop, flags=re.S)   # bouw-og vult dit opnieuw

SOORTEN = [("Coffee cuts", "voor overdag"), ("Cocktail cuts", "voor de avond")]
ZAKEN = ["Koffiebar", "Restaurant", "Cocktailbar", "Hotel", "Winkel", "Anders"]
DIENSTEN = ["Spotify", "Tidal"]

def keuze(naam, legenda, opties, verplicht=True):
    return (f'<fieldset class="lp-keuze"><legend>{e(legenda)}</legend>'
            + "".join(f'<label><input type="radio" name="{naam}" value="{e(w)}"{" required" if verplicht and n == 0 else ""}><span>{e(w)}{f" <small>{e(s)}</small>" if s else ""}</span></label>' for n, (w, s) in enumerate(opties))
            + '</fieldset>')

form = f"""<form class="lp-form" method="post" action="/api/aanvraag" data-dank="Dank je. Ik ga ermee aan de slag en je hoort van me." data-fout="Versturen lukte niet. Mail naar maarten@hear.nl of bel +31 6 24560220.">
<input type="hidden" name="bron" value="Landingspagina Coffee cuts trial"><input type="hidden" name="utm" value=""><input type="text" name="website" class="lp-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
{keuze("cc_soort", "Welke playlist wil je?", SOORTEN)}
<label>Naam van je zaak<input name="organisatie" autocomplete="organization" required></label>
<label>Soort zaak<select name="cc_zaak" required><option value="">Kies…</option>{"".join(f"<option>{e(z)}</option>" for z in ZAKEN)}</select></label>
<label>Capaciteit van je zaak (aantal gasten)<input name="cc_capaciteit" type="number" min="1" inputmode="numeric" required></label>
<label>Beschrijf de sfeer in je zaak, of noem een plek waar het op moet lijken<textarea name="cc_sfeer" required></textarea></label>
<label>Link naar een playlist met 10 favoriete nummers, ter inspiratie<input name="cc_playlist" type="url" inputmode="url" placeholder="https://open.spotify.com/playlist/…"></label>
{keuze("cc_dienst", "Waar wil je de playlist ontvangen?", [(d, "") for d in DIENSTEN])}
<label>Naam<input name="naam" autocomplete="name" required></label>
<label>E-mail<input name="email" type="email" autocomplete="email" required></label>
<label>Telefoon<input name="telefoon" type="tel" autocomplete="tel"></label>
<button type="submit">Bestel je gratis playlist</button><p class="lp-privacy">We gebruiken je gegevens alleen om je te antwoorden. <a href="privacy.html">Privacyverklaring</a></p>
<p class="lp-melding" hidden></p></form>"""

main = f"""<main class="wrap lp cct"><section class="casehead"><a class="crumb" href="custom-dj-mix.html#coffee-cuts"><span class="sectie">Coffee cuts en Cocktail cuts</span></a><h1 class="kernzin">Probeer gratis één playlist voor je zaak</h1></section>
<div class="lp-held"><div class="actie-beeld"><img src="img/diensten/coffee-cuts.jpg" alt="Coffee cuts: glas koffie op een vinylplaat in de zon"><span class="actie-label">Gratis proberen</span><a class="wa actie-knop" href="#contact"><span>Bestel je gratis playlist</span><i aria-hidden="true">→</i></a></div></div>
<section class="lp-band"><div class="lp-twee"><p class="lp-lead">Of je nu een koffiebar, een cocktailbar of een winkel hebt: je wilt warme muziek die past bij de identiteit van je zaak.</p><div class="lp-tekst"><p>Geen generieke (AI-&#8288;)tracks. Met Coffee cuts en Cocktail cuts stellen we een playlist samen voor jouw zaak, uit onze eigen collectie van nieuwe releases en classics.</p><p>Heb je een zakelijke streamingdienst zoals Soundtrack (voorheen Tunify), dan kun je de playlist daarin laden.</p></div></div></section>
<section class="lp-band"><h2 class="lp-strip">Hoe het werkt</h2><div class="lp-aanbod" style="--kol:1"><div class="lp-kaart"><ul class="lp-lijst"><li>Je vult het formulier in.</li><li>We stellen één playlist samen, afgestemd op je zaak.</li><li>Je ontvangt hem op Spotify of Tidal.</li></ul></div></div></section>
<section class="lp-band lp-contact" id="contact"><div class="lp-twee"><div><h2>Bestel je gratis playlist</h2><p>Vertel iets over je zaak, dan stel ik een playlist voor je samen.</p>
<div class="lp-wie"><img src="img/maarten-adviseur.jpg" alt="Maarten Versteeg" loading="lazy" style="object-position:50% 20%"><div><b>Maarten Versteeg</b><span>Oprichter HEAR</span></div></div></div>
{form}</div></section></main>"""

(site / "coffeecuts-trial.html").write_text(kop + main + staart, encoding="utf-8")
print("ok coffeecuts-trial.html")
