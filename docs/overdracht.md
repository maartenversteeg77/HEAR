# HEAR-website: overdracht voor een nieuwe werkdraad

Dit document is bedoeld om in een nieuwe Claude-draad naadloos verder te werken aan hear.nl. Lees eerst dit, dan `docs/besluiten.md` (het besluitenlog, met onderaan de open actiepunten).

## 1. Wat het is

- Statische site (HTML/CSS, geen framework) voor HEAR, boutique event-audio en licht van Maarten Versteeg, Amsterdam.
- Repo: `github.com/maartenversteeg77/hear` (GitHub meldt verhuizing naar `maartenversteeg77/HEAR`; de oude naam werkt nog). Branch `main`. Elke push deployt automatisch naar Cloudflare Workers: **https://hear.maartenversteeg.workers.dev**. Domein hear.nl is nog niet gekoppeld (DNS open). `netlify.toml` is een restant; opruimen staat op de lijst.
- Maarten beoordeelt op de live link, meestal op telefoon én desktop, en geeft korte, snelle wijzigingsinstructies. Werkwijze: wijziging maken, committen, pushen, in één of twee zinnen melden wat er staat.

## 2. Werkwijze met Maarten

Zijn Relatieafspraken (in zijn voorkeuren) gelden volledig. Voor dit project in de praktijk:

- **Laten zien wat is aangekomen** voordat je ermee aan de slag gaat, zeker bij aangeleverde documenten of beelden.
- **Eén vraag bij twijfel**, geen aannames. Bij A/B-keuzes: beide tonen, hij kiest.
- **Pro's en cons, geen pleasen.** Als iets niet werkt (bv. een AI-beeld, een te vlakke tekst), zeg het.
- **Zijn stem bewaren.** Teksten corrigeren en losser maken mag, maar dicht bij het origineel blijven. De founder story is ik-vorm; de rest van de site wij-vorm.
- **Opzoekbare feiten opzoeken**, niet uit het hoofd: merknamen, modelnummers, specs. Onzeker? Markeren als "te verifiëren" in besluiten.md.
- **Loggen** in `docs/besluiten.md`: elk inhoudelijk besluit, met datum, kort. Open punten onder "TE VERIFIËREN" of als actiepunt.
- Hij werkt vaak 's nachts; gesprek eindigt pas als hij dat zegt.
- **Antwoord eerst, in zijn woorden.** Elke reactie begint met wat er voor hem veranderd is (wat staat er nu, waar), in gewone taal. Technische kanttekeningen over scripts, CSS of controles horen in het log of in dit document, niet in het gesprek, tenzij hij ernaar vraagt. Nooit Engels in de reactie.
- **Teksten: zijn versie wint.** Als hij een tekst aanlevert, die letterlijk plaatsen met hooguit interpunctie, koppeltekens en wij/we-consistentie; elke ingreep benoemen. Eigen voorstellen eerst inline tonen, niet live zetten, tenzij hij "zet maar neer"/GO zegt.
- **Slogans en "AI-taal"** (zie besluiten 17 okt): geen staccato fragmenten, geen van…naar / niet a maar b / wel…niet-figuren, geen zinnen die uitleggen wat iemand moet voelen, geen uitleg van de eigen grap. Een korte zin mag als hij zonder toelichting werkt en over iets concreets gaat. Zijn eigen slogans (Need we say more?, Klein maar groot, Zwitserse zakmes, oh ja/oh wow) blijven.
- Bij "beoordeel": criterium, pro's en cons, vergelijking, dan oordeel; ook zeggen wat ik niet zeker weet. Bij een vraag naar mijn "gevoel": eerlijk zeggen wat ik wel kan aanwijzen (bv. "had ik dit zonder hem kunnen verzinnen?").

Commit-conventie (altijd zo):
```
git -c user.name="Maarten Versteeg" -c user.email="maartenversteeg77@users.noreply.github.com" commit -q -m "<korte NL-omschrijving>

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
Claude-Session: <sessie-url>" && git push
```
Niet doen: `pkill -f http.server` (sluit de shell).

## 3. Inhoudelijke regels voor de site

- **Geen prijzen.** Nooit, ook geen indicaties in euro's.
- **Geen superlatieven**, geen reclametaal. Ingetogen, concreet, feitelijk. Merken en modelnummers mogen juist wel.
- **Geen cursief** sitewide (CSS forceert `font-style:normal`).
- **Geen AI-gegenereerde beelden.** Echte foto's, echte productfoto's. Gezichten van derden buiten beeld snijden tenzij toestemming.
- **Tone of voice**: expertise laten merken, niet uitleggen. Eén signaalwoord per tegel of alinea dat een vakgenoot herkent en waar een leek overheen leest (frontfill, delay, coherent, dual file management). Geen uitleg, geen spec-opsomming.
- Boutique, niet luxury. Het woord "boutique" hoogstens één keer (Over HEAR); verder voelbaar maken.
- Convergeren: geen nieuwe pagina's of categorieën zonder expliciet besluit. Abbey (analoge keten) pas noemen als het operationeel is.
- Taal: Nederlands; productcategorieën hebben Engelse namen (Booth & DJ-gear etc.), bewust nog niet beslist of dat zo blijft.

## 4. Huisstijl

- Zwart `#191A19`, wit `#F6F5F1` (homepage) / `#F4F5F5` (detailpagina's), turquoise `#7AC3C9`, koraal `#D47763`. Maximaal twee kleuren per vlak.
- Koppen: Advent Pro (Google Fonts; in de container geblokkeerd, valt terug op Helvetica, dus screenshots wijken af). Lopende tekst: Helvetica.
- Logo: `site/img/logo-white.png` / `logo-black.png`.
- Zwarte kopbalk met navigatie boven elke pagina; detailpagina's hebben een zwarte `.casehead` met kernzin en kruimelpad.

## 5. Sitestructuur

Navigatie (volgorde vast): **Cases · Voor wie · Producten · Waarden · Over HEAR · Nieuws**, plus taalknop EN/NL. De kop staat hardgecodeerd in alle handpagina's én wordt door de scripts uit index.html gekopieerd: bij een wijziging alle `site/*.html` aanpassen en alle scripts draaien.

| Pagina | Bestand | Bron |
|---|---|---|
| Home | `index.html` | hand; slider leest `cases.json` |
| Cases overzicht | `cases.html` | `scripts/bouw-cases.py` ← `site/cases.json` |
| 8 cases | `ade-dj`, `jubileum-ondernemersnetwerk`, `productpresentatie`, `gemeentelijk-netwerkevent`, `systeemadvies`, `dj-sets`, `prive-event`, `radio-mixes` | hand; vorige/volgende via bouw-en.py |
| Voor wie | `doelgroepen.html` → `corporate.html`, `venue-owners.html`, `dance-events.html` | hand; zijnav (pijlen + bolletjes) staat hardgecodeerd in de drie pagina's, bij een vierde doelgroep alle drie bijwerken |
| Waarden (nav "Waarden", pagina "Waarden en uitgangspunten", EN "Values") | `principes.html` (één pagina met jogwheel; volgorde Samen · Open · Vakmanschap · Warme sound, ankers `#samen` `#open` `#vakmanschap` `#warmte`; per waarde: titel op het display, statement (regel onder de titel), intro-alinea, dan direct de lijst zonder kop of lijn; op ≥900px wiel links en tekst rechts, daaronder gestapeld) | `scripts/bouw-principes.py` ← `content/principes.json` (velden `slug,titel,statement,intro,werkwijze[]`, optioneel `werkwijze_kop`); component `site/jog.css` + `site/jog.js` |
| Producten en diensten | `diensten.html` → 8 pagina's (`booth-dj-gear`, `high-end-audio`, `atmospheric-lighting`, `dancefloor-lighting`, `vintage-lighting`, `av-as-a-service`, `artiesten`, `special-projects`) | `scripts/bouw-diensten.py` ← `content/diensten.json` |
| Over HEAR | `over-hear.html` | hand (founder story, ik-vorm) |
| Engels | `site/en/*.html` | `scripts/bouw-en.py` ← `content/en.json` |
| Nieuws (artikelopbouw: kop, foto, optionele kopregel, vette lead, lopende tekst met `## `-tussenkopjes) | `site/nieuws/index.html` + `site/nieuws/<slug>.html` | `scripts/bouw-nieuws.py` ← `content/nieuws.json`; maakt ook `img/nieuws/<slug>-social.jpg` (1200×630, Open Graph) |

Overig: `merken.html`, `projectbrief.html/.md` (oud, niet in nav), `site/assets/` (oude beelden), `site/img/diensten/` (productfoto's), `scripts/verbreed.py` (portretfoto verbreden met vervaagde randen).

### Bouwregels
- **Gegenereerde pagina's nooit met de hand bewerken**: pas de JSON aan en draai het script. Opbouw productpagina: kernzin, intro over volle breedte, productrij, eventuele blokken, verwijzingen. Scripts kopiëren header/footer uit `index.html`, dus navigatie-wijzigingen eerst in index.html, dan alle scripts opnieuw draaien.
- Na elke wijziging aan een vertaalde pagina (index, cases, 8 cases, over-hear): `python3 scripts/bouw-en.py`. Het script eist dat elke NL-zin in `en.json` letterlijk in de bronpagina staat en stopt anders met de naam van de zin. Dan en.json bijwerken.
- Volgorde bij een volledige rebuild (sinds 18 okt): `bouw-cases.py`, `bouw-diensten.py`, `bouw-principes.py`, `bouw-relevant.py`, `bouw-en.py`, `bouw-nieuws.py`, `bouw-og.py`. bouw-nieuws leest de Engelse kop uit site/en/index.html, dus ná bouw-en; bouw-og altijd als laatste (zet deelmetadata en deelbeelden op alle pagina's).
- **Na elke CSS-wijziging** `python3 scripts/check-css.py`: meldt classes in de HTML zonder CSS-regel. Ingevoerd nadat de regels voor `.structuur` (Over HEAR) ongemerkt uit styles.css waren verdwenen. Alleen `.systeemadvies` is een bekende losse haak.
- Nieuwsbericht plaatsen: item toevoegen in `content/nieuws.json` (status `af`), beeld in `site/img/`, `python3 scripts/bouw-nieuws.py`, pushen. Deel-URL: `<basis>/nieuws/<slug>.html`. `basis` in nieuws.json omzetten naar https://hear.nl zodra het domein live is (anders wijzen de social-afbeeldingen naar workers.dev).
- `cases.json`: velden `titel`, `titel_en`, `tekst`, `tekst_en`, `beeld`, `alt`, `link`, `doelgroepen` (corporate/venue/dance), optioneel `positie` (object-position), `status: "af"`.

### CSS
- `home.css`: homepage en gedeelde kop/voet/nav, taalknop `.taal`.
- `styles.css`: detailpagina's (body `.pagina`): `.casehead`, `.casehero` (full-bleed beeld), `.ballon` (turquoise quotebubbel op het beeld, rechts; op mobiel eronder), `.case-overzicht`, `.producten` (productrij), `.quick-breed` (intro over volle breedte), `.knoprij`, `.kop-knop` (groene knop in de kop, bv. maartenversteeg.nl), per-beeld `object-position`-regels.

### Testen
Playwright headless in de container: `/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell`, `NODE_PATH=/home/claude/.npm-global/lib/node_modules/@playwright/mcp/node_modules`. Screenshots desktop (1728) en mobiel; absolute paden werken via een route van `http://hear.test/` naar de site-map. Fonts wijken af (zie 4). Uiteindelijk oordeel is Maartens blik op de live link.

## 6. Stand van zaken (18 okt 2026, 01:10)

Af en door Maarten gereviewd: homepage, cases, voor wie, producten (8), waarden (alle vier, teksten grotendeels van Maarten zelf), over HEAR (founder story + structuurkader), nieuws (2 berichten), Engels voor homepage/cases/over HEAR. Sitewide sloganscan gedaan (17 okt); vijf zinnen vervangen, rest bewust gelaten.

Laatste sessie (17–18 okt) in het kort: waarden Samen/Open/Vakmanschap/Warme sound herschreven; navigatie Cases · Voor wie · Producten · Waarden · Over HEAR · Nieuws; "Principes" heet overal "Waarden"; uurbasis nergens meer genoemd; corporate-slotalinea is een plaatsvervanger tot Maartens review; EN-knop op nieuws gaat naar de Engelse homepage; structuurkader-CSS hersteld en profielblok erin opgenomen; `scripts/check-css.py` toegevoegd.

Maarten loopt aan het eind de hele site nog een keer door. Open, zie `docs/besluiten.md` onderaan:
- Corporate-pagina reviewen: slotalinea ("twee dingen doen") is van mij; structuur Strategie → Beleving → AV-ontwerp → Uitvoering, blok over de communicatieachtergrond.
- Founder story langs de verhaallijn "uitbouw, geen carrièreswitch"; eventueel bedrijfsnaam adviespraktijk terug in het kader.
- Eén zin over het netwerkmodel (één aanspreekpunt, vast netwerk) ergens vroeg op de site.
- Homepage-lead ("Transformeer…") is bewust gelaten; "Thuis in uitgaan" blijft kandidaat.
- Engelse vertaling van voor wie, waarden, producten, nieuws.
- Te verifiëren: rechten op stockbeelden (gala, dansvloer, beams), toestemming saxofonist/dj op jubileumfoto, merk reversmicrofoons, WhatsApp-nummer (`wa.me/?text=` overal), hear.nl DNS + `basis` in nieuws.json, netlify.toml weg, Engelse categorienamen op Producten, "visuals" in Warme sound (bieden we nergens aan).
