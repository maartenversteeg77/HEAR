# Samensteller met blokjes (proef, 20 november 2026)

Bewaard op verzoek van Maarten: de pagina's zijn van de site gehaald, het ontwerp blijft.

## Wat het was
Een aanvraagpagina waarop de klant zijn event samenstelt uit bouwstenen. Begonnen als demo voor een partnerlocatie, daarna algemeen gemaakt op /samenstellen.

## Het ontwerp
- De foto blijft één foto. De blokjes zijn een eigen tekening: schuin van boven, 2 x 2 ronde noppen, lijn #191A19.
- Kleuren: geluid #D47763, personeel #7AC3C9, licht #E9D36B, scherm #C9C8C2, wit #F6F5F1. Wit = niet gekozen, kleur = gekozen.
- Op de foto een zwarte knop met een stapeltje en 'Stel je event samen'.
- Een zin bovenaan: 'Ik organiseer een ... in [naam locatie] voor ... met ... dagprogramma en ... dj'.
- Tegels per groep (Geluid, Personeel, Licht en aankleding, Ledscherm), elk met rechtsboven een blokje dat kleurt bij kiezen.
- Rechts een zwart vlak 'Jouw event' met een stapel die groeit met elke keuze en de namen ernaast; op de telefoon een vaste balk onderin.
- Geen puzzelvormen, geen foto in blokjes, het woord LEGO nergens.

## Waarom het weg is
Vaste prijzen per onderdeel klopten niet met maatwerk: bij grote events komen er een tweede bus, tilhulp, een ingehuurde technicus en bijhuur bij, en alles aangeklikt kwam op ongeveer 3.000 euro. Zonder prijzen deed de pagina hetzelfde als stap 2 en 3 van het aanvraagformulier, dat ook al naar het budget vraagt.

## Bestanden
- `blokjes.py`: de tekening in Python (`iso_stapel`) en JavaScript (`ISO_JS`).
- `bouw-samenstellen.py`: het bouwscript (verwacht `blokjes.py` naast zich en `site/nieuwjaarsborrel.html` voor kop en voet; schrijft naar `site/`).
- `samenstellen.css`: de opmaak.
- `voorbeeld-met-prijzen.html`, `voorbeeld-zonder-prijzen.html`: de laatste gebouwde pagina's (paden naar css en beeld kloppen alleen vanuit `site/`).

Terugzetten: de drie bronbestanden terug naar `scripts/` en `site/`, het script weer in de bouwvolgorde.
