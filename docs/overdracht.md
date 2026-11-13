# HEAR-website: overdracht voor een nieuwe werkdraad

Bijgewerkt op 13 november 2026. Lees eerst dit document, daarna de laatste 60 regels van `docs/besluiten.md`. Dit document vervangt de versie van 18 oktober; die klopte op veel punten niet meer.

## 1. Wat het is

- Statische site (HTML en CSS, geen framework) voor HEAR: licht, geluid en muziek voor events, van Maarten Versteeg, Amsterdam.
- Live op **https://hear.nl**. Repo `maartenversteeg77/HEAR`, branch `main`. Elke push deployt automatisch via Cloudflare Workers Builds.
- Maarten kijkt op de live site, meestal op zijn iPhone, en geeft korte wijzigingen. Werkwijze: aanpassen, bouwen, lokaal controleren, committen, pushen, wachten tot de deploy klaar is, en dan in gewone taal melden wat er staat.

## 2. Controleer dit vóór je een antwoord of tekst stuurt

Dit zijn de correcties die Maarten het vaakst heeft moeten herhalen. Loop ze elke keer na.

1. **Zijn tekst letterlijk.** Alleen spelling en interpunctie corrigeren, en elke correctie benoemen. Goedgekeurde tekst blijft staan.
2. **Vraag of opdracht?** Bij een vraag ("Beter zo?", "Kan dit?") eerst antwoorden en niet meteen bouwen. Bij een opdracht direct uitvoeren, zonder "zal ik…?".
3. **Niet uitleggerig.** Geen element te zwaar maken. Een advertentie brengt sfeer over, geen redenering.
4. **Geen avondverloop beschrijven** (binnenkomst, opbouw, "dansbaar als het zover is"). Dat hoort gewoon zo.
5. **Propositie, geen ding.** Niet "een microfoon", wel "de mogelijkheid om versterkt een speech te geven".
6. **Geen onzin-poëzie.** Geen zinnen die mooi klinken maar niets zeggen, geen verzonnen tegenstellingen, geen aannames over de avond van de klant.
7. **Geen van…naar en van…tot, niet openen met wat je niet doet, geen metatekst.**
8. **Engels: niet vertalen maar opnieuw schrijven.** Schrijf de Engelse zin vanuit de betekenis en lees hem daarna los van het Nederlands na. Toets: zou een Engelstalige tekstschrijver het zo opschrijven? Dit ging meerdere keren mis.
9. **Feiten opzoeken**, niet uit het hoofd. Lukt dat niet, dan zeggen dat het niet is geverifieerd.
10. **Pas zeggen dat iets live staat als het gecontroleerd is.** Na een CSS-wijziging de berekende waarde in de browser controleren (zie 6).
11. **Antwoord in het Nederlands, kernpunt eerst, pro's en cons met zekerheidsmarge, één vraag per keer, niet pleasen.**

## 3. Vaste regels

- **Privé:** privé-mail en privénummer nooit publiceren. Publiek zijn alleen maarten@hear.nl en +31 6 24560220. De Resend-sleutel staat alleen in Cloudflare.
- **Beeld:** geen AI-beelden. Stockbeeld alleen als je het er niet aan afziet.
- **Prijzen:** maatwerk. Geen prijspagina in het menu. De enige prijs op de site is de richtprijs op de actiepagina nieuwjaarsborrel.
- **Huisstijl:** zwart `#191A19`, wit `#F6F5F1`, koraal `#D47763`, turquoise `#7AC3C9` als steunkleur. Maximaal twee kleuren per onderdeel. Koppen in Advent Pro Light, lopende tekst Helvetica.
- **Loggen:** elk besluit met datum in `docs/besluiten.md`.

## 4. Structuur van de site

Menu: **Cases · Voor wie we werken · Producten · Nieuws · Over HEAR**, plus de knop "Plan een gesprek" en de taalknop.

| Onderdeel | Bron |
|---|---|
| Homepage `site/index.html` | met de hand; het blok "Voor wie is HEAR" wordt door `bouw-doelgroepen.py` ingevoegd |
| Doelgroeppagina's (zakelijke-events, merken-en-bureaus, dance-events, bijzondere-eventlocaties) en `doelgroepen.html` | `scripts/bouw-doelgroepen.py` |
| Actiepagina `nieuwjaarsborrel.html` | `CAMPAGNE` in `scripts/bouw-doelgroepen.py` |
| Cases | `scripts/bouw-cases.py` ← `site/cases.json` (volgorde van het bestand) |
| Producten en diensten | `scripts/bouw-diensten.py` ← `content/diensten.json` |
| Waarden | `scripts/bouw-principes.py` |
| Netwerkpartners | `scripts/bouw-partners.py` |
| Nieuws | `scripts/bouw-nieuws.py` ← `content/nieuws.json` |
| Engels `site/en/` | `scripts/bouw-en.py` ← `content/en.json` |
| Over HEAR `site/over-hear.html` | met de hand |
| 404-pagina's | `scripts/bouw-404.py` |
| Favicon-links | `scripts/bouw-icoon.py` |
| Sitemap en robots | `scripts/bouw-sitemap.py` (draait als laatste) |

**Koppen:** kleine koraal labels in hoofdletters (`strip-kop`, `lp-strip`), met op de landingspagina's soms een cursieve regel eronder (`lp-motto`). Regel: een werkwoord alleen waar je ergens heen gaat, een bijvoeglijk naamwoord alleen waar het iets zegt.

## 5. Bouwen en deployen

Volledige build, in deze volgorde:

```
for f in doelgroepen cases diensten principes relevant privacy partners prijs mixes aanvraag nieuws en og 404 icoon sitemap; do python3 scripts/bouw-$f.py; done
python3 scripts/check-css.py
```

Onschuldige waarschuwingen van check-css: cc-, nieuws-rij, systeemadvies, v2- en vb-classes.

- **Engels:** `content/en.json` bevat paren Nederlands → Engels per pagina. `bouw-en.py` stopt met "NIET VERTAALD" als de Nederlandse helft van een paar niet meer op de pagina staat. Wijzig je Nederlandse tekst, werk dan het paar bij.
- **Alleen-Nederlands op de homepage:** `bouw-en.py` haalt de campagnestrook (`nj-strip`) uit de Engelse homepage.
- **Statische pagina's** (zoals prive-event, radio-mixes, merken) hebben een eigen kopie van het menu. Een menuwijziging moet dus ook daar worden doorgevoerd.
- **Commit:** met `git -c user.name="Maarten Versteeg" -c user.email="maartenversteeg77@users.noreply.github.com"`, een korte Nederlandse omschrijving en de attributieregels die de sessie opgeeft. Daarna pushen en de deploy volgen met `gh api repos/maartenversteeg77/HEAR/commits/<sha>/check-runs`.
- **Begin van een draad:** eerst `git pull --rebase origin main`. Er kan vanuit een andere draad gepusht zijn.

## 6. Controleren

- **Lokaal:** `python3 -m http.server 8811` in `site/`, en Playwright met het iPhone 13-profiel en met een desktopvenster van 1440 breed.
- **hear.nl is vanuit de werkomgeving niet te openen** (de proxy geeft 403). Live controleren kan dus niet; zeg dat erbij.
- **Valkuil in de CSS:** op de homepage laadt `doelgroep.css` ná `home.css`. Een regel in `home.css` kan daardoor stil worden overschreven. Controleer na een CSS-wijziging de berekende waarde in de browser.
- **iPhone:** echte Safari wijkt soms af van de simulatie, bijvoorbeeld bij datumvelden. Vraag Maarten om te kijken als het om formuliervelden gaat.

## 7. Actiepagina nieuwjaarsborrel (campagne tot en met januari 2027)

- Adres: hear.nl/nieuwjaarsborrel. Niet in het menu, niet in de sitemap, niet in Google, alleen Nederlands.
- Opbouw: titel op twee regels ("Heb jij al een nieuwjaarsborrel gepland?" en "Wij helpen je graag!"), beeld met het turquoise label "Nog enkele data in januari vrij" en de knop "Vraag vrijblijvend een offerte aan", korte intro, vier punten aanbod, richtprijs, formulier met datum en aantal gasten. Onder het formulier staat alleen een juridische regel.
- Prijs: "Vanaf € 10 per gast, met een minimum van € 1.500", vanaf 500 gasten op aanvraag. Geen aantal uren, geen kortingsactie.
- Op de homepage staat een turquoise strook naar deze pagina, tussen "Voor wie is HEAR" en "Bekijk de cases". **Na januari weghalen.**
- LinkedIn toont bij gewone posts met een link alleen een kleine tegel. Daarom is er een los beeld voor de post gemaakt (staand, 4:5). De kop daarvan is nog niet gekozen.

## 8. Open punten

- Kop voor het LinkedIn-beeld. Kandidaten: "Laat je nieuwjaarsborrel klinken", "Maak van je nieuwjaarsborrel een event". Maarten vond "Jij: het nieuwjaarsfeest / Wij: de slingers" kort maar te facilitair.
- Scherper origineel van de borrelfoto (het huidige bestand is 1533 pixels breed).
- Een quote van een klant of klantlogo's op de actiepagina, zonder link.
- Artikel "Wanneer licht het geluid versterkt": Maarten schrijft de eerste versie zelf. Opzet en bronnen staan in het projectdocument `claude/artikel-licht-versterkt-geluid.md`. Als hij een versie indient: beoordelen, en zijn tekst met de patronen opslaan in een projectdocument "Content structuur en tone of voice".
- Nieuwe tekst voor Over HEAR komt van Maarten zelf.
- Contrast van de kleine koraal labels op een lichte achtergrond.
- Lege linkerkolom bij "De momenten die het verschil maken" op de pagina voor merken.
- Toestemming van mensen op foto's; een groter origineel van de dansers op het tuinfeest.
- Opruimen: `site/v2.html` en `site/voorbeeld-producten.html` (proefpagina's, niet gelinkt).
- Search Console: de lijst met niet-geïndexeerde adressen opnieuw bekijken zodra Google de sitemap heeft verwerkt.
