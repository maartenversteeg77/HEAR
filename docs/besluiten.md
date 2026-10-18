# Besluitenlog hear.nl

Wat is besloten, met datum. Nieuwste bovenaan. Open punten staan onderaan.

## 15 oktober 2026

### Werkwijze en infrastructuur
- De site wordt zelf gebouwd en beheerd, zonder extern bureau.
- GitHub-repo `maartenversteeg77/hear` is de enige bron. ChatGPT bouwt niet meer parallel.
- Hosting (16 okt): verhuisd van Netlify naar Cloudflare (Workers, gratis). Reden: Netlify gratis = 300 credits/maand, 15 per publicatie (~20 publicaties); tegoed was op en publiceren stond stil. Werkadres: hear.maartenversteeg.workers.dev. hear.nl (DNS bij TransIP) later hierheen; e-mail (MX) dan bij TransIP laten.
- Het ChatGPT-geraamte is het uitgangspunt. Daarna vullen we pagina voor pagina.

### Positionering
- Bereik op de site: **150–1.500 gasten**. Capaciteit begint feitelijk bij 100–150, maar de site moet het niet klein laten ogen.
- Pay-off (16 okt): **HEAR. The difference.** / HEAR the difference. Engels alleen in een kernachtige pay-off met eenvoudige woorden; de rest van de site Nederlands. "The difference" mag verder gaan dan geluid (ook licht, aanpak).
- Transformatie is het onderliggende principe (niet in de pay-off): muziek → beleving, ruimte → dansvloer, geluid → omgeving, event → herinnering; ook de aanpak zelf is een transformatie.
- Maarten houdt van het woord "difference"; kan elders op de site terugkomen (16 okt).
- Afgewezen: "Festivalkwaliteit, op de schaal van jouw event" (te instrumenteel en uitleggerig); abstracte/AI-achtige koppen ("de avond", "wij horen"); Engelse inspiratieslogans ("more than a moment"); Nederlands-instrumentele ("alles goed geregeld"); slogans met alleen 'sound' (HEAR doet licht én geluid).
- Hero v3c (16 okt): headerbeeld = verbrede dansvloerfoto; HEAR-logo middelgroot (ongeveer halve schermbreedte, max 760px); desktop krijgt topnavigatie (Doelgroepen · Cases · Principes · Diensten · Merken · Over HEAR), hamburger alleen op mobiel.
- Hero v3b (16 okt): pay-off als "Hear the difference." (geen allcaps, botst anders met het logo), meer ruimte onder het logo, uitleg op twee regels, klein: "Voor midsize events (150 tot 1.500 personen)".
- Hero v3 (16 okt): beeld over de volle breedte, groot logo eroverheen, klein logo linksboven op de homepage verborgen (niet twee keer het logo). Headerbeeld (16 okt): eigen foto dansvloer met dj, geanonimiseerd (gezichten in nevel, venuenaam op de decks weg); publiek op de rug, rood door het blauw. Liggend gemaakt door links en rechts nevel bij te verzinnen (niet opgerekt): 2132×1200. Tekst als v2.
- Hero (werkversie 16 okt, v2): groot merk onder de foto verwijderd. Kop = pay-off "HEAR the difference." (gewone tekst, geen logo met driehoek; tekstblok even breed als de kop). Daaronder: "Transformeer een locatie in een dansvloer, een event in een belevenis, een dj in een muzikale reis." Klein: "Van 150 tot 1.500 personen". Amsterdam weg. Vorige variant (merk groot met payoff eronder; kop 'Van zaal naar dansvloer…') staat in git.
- "Binnen bereik" ging niet over prijs maar over schaal: wat je op festivals ziet, kan ook bij een event voor 200 gasten.
- "Festivalwaardig" / "festival grade" betekent: hoge kwaliteit die tegen een stootje kan. Het betekent niet schreeuwerig.
- Geen prijzen op de site.

### Stem
- Founder story in de ik-vorm.
- De rest in de wij-vorm. "Wij" = Maarten met een netwerk van professionals en partners. Dat moet ergens in de content worden uitgelegd.

### Structuur
- Verzamelpagina's met deepdive-pagina's eronder. Wie de verzamelpagina leest, weet genoeg. Wie doorklikt, toont interesse en mag een langer verhaal krijgen (bijv. geluid gelijkmatig over een zaal verdelen met delays en frontfills).
- Deepdive-pagina's zijn los deelbaar op socials en kunnen een video krijgen.
- Lege pagina's zijn placeholders, geen signaal dat drie regels volstaan. Tempo: richting twee pagina's per dag.
- Contentkeuze: evergreen boven tijdgebonden; always on boven campagnes.
- Op termijn YouTube-video's op product- en systeempagina's: waarom een systeem goed is en hoe je het gebruikt (dubbelt als instructievideo).

### CTA
- WhatsApp-knop als CTA, op meerdere plekken.

### Diensten
- De propositie: ik kijk wat jouw ruimte nodig heeft om goed te klinken en te ogen. Kopen, huren of leasen is daarna de invulling.
- AV as a service blijft, maar als optie, niet als propositie.
- Mogelijke rollen: puur betaald advies (advies en product gescheiden), voordeel via een leaseconstructie, of verkoop met marge.
- Wat de klant belangrijk vindt: iemand denkt mee, heeft er verstand van, zoekt de goede oplossing en heeft opties om het toegankelijk te maken.

### Cases
- Elke case krijgt een label (doelgroep/type).
- "Cases" op de verzamelpagina wordt een klein navigatie-element (rode kleine letter), geen grote kop.
- Resultaat en citaat inhoudelijk en qua toon uit elkaar halen. Het citaat is spreektaal, uit iemands mond.
- **Indeling casepagina: In het kort · Opdracht · Aanpak · Resultaat · Citaat.** De beoogde klantbeleving (voorheen "Experience") valt onder Opdracht. Aanpak = wat wij deden. Resultaat = wat er feitelijk gebeurde, zakelijke toon. Citaat = hoe het voelde, spreektaal van de klant, met naam en rol.
- ADE-case: bronvermelding wordt "Artist management Rivo". Citaat (16 okt) begint nu met "Tijdens Amsterdam Dance Event organiseerden we een pop-up event. Vanuit Frankrijk aangekomen rekenden we op soundchecktijd…"; slot ("Warm, vol en de dj's waren …") door Claude aangevuld met het bestaande vervolg — te bevestigen door Maarten.
- DJ-sets-case: het citaat is echt (Architects in Music). Bron vervangen door "Architects in Music — A full circle event company with a focus on hospitality" (16 okt).
- Privé-event (Ronald Pronk): blijft. Ronald heeft toestemming gegeven. De case laat ook zien dat privé de uitzondering is.
- Uitgelicht werk op de homepage = slider met alle afgeronde cases, gevoed vanuit `site/cases.json` (één regel per case; volgorde = volgorde op site; alleen status "af" wordt getoond). Dubbeling met de casespagina is akkoord: die is het visuele overzicht. Halve cases worden nergens getoond.

### Vormgeving
- Kleuren volgen het huisstijldocument (Branding DEF): zwart en gebroken wit als basis, accent mag hoofdkleur van een vlak zijn, max. twee kleuren per vlak. Geen crème/beige.
- Homepage v1 (15 okt): zwarte hero met booth-foto en groot HEAR-merk, koraal statementvlak, tegels op gebroken wit, koraal als WhatsApp-knop. Koraal alleen op donker of als vlak met zwarte tekst (op gebroken wit te weinig contrast voor kleine tekst).
- Homepage-opbouw (16 okt, herzien): topnavigatie vervangen door hamburgermenu; na het statement een compacte navigatiebalk met zes onderdelen + korte uitleg (Doelgroepen · Voorbeeldcases · Principes · Diensten en producten · Merken en techniek · Over HEAR). Variant met grote regels (B) afgewezen: te veel ruimte. Daarna: Uitgelicht werk (slider, zie Cases) · Over HEAR · afsluiter met WhatsApp · uitgebreide footer met alle onderdelen (laat diepte zien). Hero: één knop (WhatsApp); ondertitel staat onder het merk.
- Homepage-opbouw (16 okt, v3): hero · Uitgelicht werk (cases omhoog) · koraal blok met de overige onderdelen (Doelgroepen · Principes · Diensten en producten) · Over HEAR met press photo · afsluiter · footer. Statementtekst en de witte navigatiebalk vervallen (kleur koraal bleef). 'Merken en techniek' gaat op in 'Diensten en producten'; merken worden toegelicht op de pagina's over geluid/licht. Topnavigatie: Doelgroepen · Cases · Principes · Diensten · Over HEAR.
- 16 okt: 'Doelgroepen' heet op de homepage 'Voor wie is HEAR' (topnav: 'Voor wie'); doelgroepen is inside-out. Over HEAR-tekst homepage: "Als dj, corporate communicatieadviseur én eigenaar van HEAR verbind ik de corporate evenementenwereld met cutting-edge techniek en muziek uit de dancescene." ('daarnaast' was zwak). Casetitels in slider: Transformatie: van skatehal tot dansvloer · Seminar en netwerkevent · Een reis door 40 jaar elektronische muziek · Advies over het beste soundsystem voor jouw ruimte · Van industriële ruimte naar intieme sfeer.
- Logo-lockup teruggedraaid (16 okt): pay-off weer als losse kop "Hear the difference" (zonder punt); HEAR-logo linksboven in de hero, tekstblok onderin. (Lockup-proef staat in git.) Eerder: "Hear the difference" (zonder punt: het is logo) onder het logo, kleine letter, uitgevuld tot exact de breedte van het logo (SVG). Kop als aparte tekstregel vervalt (blijft onzichtbaar voor zoekmachines/schermlezers). Over HEAR: "eigenaar" wordt "founder".
- Typografie in reeksen (16 okt): koppen in kaarten en blokken krijgen de hoogte van twee regels, zodat de tekst eronder gelijk staat; woorden evenwichtig verdelen, geen los woord op de laatste regel.
- Kleur (16 okt): citaatblokken op casepagina's en de kaart 'Alle cases' worden turquoise (#7AC3C9) met zwarte tekst, i.p.v. zwart; koraal zit al in het blok op de homepage. ADE-citaat: bron 'Artist management Rivo'.
- Detailpagina's (oude stijl) proef 16 okt: koeler gebroken wit #F4F5F5 met neutrale grijzen; homepage blijft #F6F5F1. Eerder: achtergrond overal #F6F5F1 (gebroken wit, licht warm-grijs); de beige tinten van het ChatGPT-geraamte (#f3f0e9 e.a.) vervangen op alle oude pagina's (16 okt).
- Letters: Advent Pro voor koppen, Helvetica/Arial voor lopende tekst.
- Referentie die aanspreekt: musicandpower.com (zwarte basis, groot merk over beeld, gelaagde blokken).
- Eén consistente letter, tenzij die voor bezoekers niet goed leesbaar is.
- Beeldgebruik wordt nog volledig herzien: nu te veel dubbelingen.
- Productpresentatie-case: geanonimiseerd beeld (16 okt): matte vloer, collectie herkleurd naar jonger en kleurrijker. Oorspronkelijke merkfoto van de site gehaald.

## Open punten
- Casepagina Jubileum ondernemersnetwerk: beeld blijft voorlopig zoals het is. Maarten vraagt de saxofonist om toestemming; daarna uitsnede met gezichten van dj en saxofonist (vergelijking 16 okt: gezichten-uitsnede vertelt het verhaal beter dan sax-detail).
- Uitleg van "wij" (Maarten + netwerk) stond in het statementvlak en is daarmee van de homepage verdwenen; nieuwe plek kiezen (bijv. Over HEAR).
- Labelset voor cases.
- Founder story noemt nog "100 tot 1.500 personen"; aanpassen naar 150–1.500?
- Plek van DJ-sets, radio-mixes en eigen producties (bij Cases of apart). DJ-sets hoort bij Cases (16 okt): een corporate klant kan ook een dj zoeken, en wie voor microfoons komt moet op het idee komen er een dj bij te huren. Het gaat om hoe je de case brengt. In de slider direct na het gemeentelijk netwerkevent (overgang naar borrel). Radio-mixes: nog open.
- WhatsApp-nummer nog nodig (knoppen staan er, zonder nummer).
- Overige pagina's nog in de oude stijl; worden een voor een omgezet.

## 16 okt — Alle onderliggende pagina's in de homepagestijl
- Kop, menu (hamburger op mobiel) en uitgebreide voet van de homepage nu op alle pagina's; actieve rubriek in koraal.
- Paginakop loopt door in zwart (terug-link, titel, ondertitel); inhoud op #F4F5F5.
- Koppen in Advent Pro, tekst in Helvetica; labels zwart (het bruinrood #a25e49 is weg).
- Citaten turquoise vlak; casesoverzicht als kaarten zoals de slider; Merken blijft bestaan maar staat niet in de navigatie.
- Terug-links van cases wijzen naar cases.html; "Doelgroepen" heet in de terug-link "Voor wie".
- Productlancering: uitgelichte quote zonder naam als turquoise band over de volle breedte.
- Homepage: zwarte kopbalk boven de hero; de foto begint eronder in plaats van eronder door te lopen (16 okt).
- Proef netwerkevent: klantquote als turquoise tekstballon midden tussen de tekst, buiten de lijnenstructuur, naam eronder (16 okt).
- Kopbeelden op alle contentpagina's: los onder de zwarte balk met witruimte ertussen, binnen de paginamarges, verhouding 3:2 (portretten van dj-sets en radio-mixes onbijgesneden) (16 okt).
- Proef netwerkevent: tekstballon met klantnaam erin, rechts naast het kopbeeld; op mobiel onder het beeld (16 okt).
- Teruggedraaid: kopbeelden weer vullend over de volle breedte (losse foto afgewezen). Tekstballon zonder puntje, licht transparant turquoise, op de rechterkant van het kopbeeld; op mobiel half over de onderrand (16 okt).
- Alle klantquotes als transparante turquoise ballon op het kopbeeld, met een uitgesneden aanhalingsteken (beeld schijnt erdoorheen); naam in de ballon; productlancering zonder naam. Het citaat van Architects in Music op dj-sets was bij de tekstwissel weggevallen en is teruggezet (16 okt).
- Casesoverzicht wordt gebouwd uit cases.json (scripts/bouw-cases.py): zelfde titels, labels en volgorde als de homepage-slider; alleen status "af". Tegel = beeld met turquoise tekstvak eronder als één geheel. Radio-mixes staat daardoor niet meer in het overzicht (16 okt).
- Landingspagina's (cases en onderliggende pagina's van diensten, principes, voor wie): aparte kop, ondertitel en "In het kort" samengevoegd tot één kernzin, groot in de zwarte kop. Overzichtspagina's houden hun titel (16 okt).
- Productlancering: AI-beeld met zichtbare artefacten vervangen door nieuw beeld van Maarten (sneakers op plateaus onder theaterspots); ook gebruikt op Uitstraling, Sfeerverlichting, Diensten, Principes en in de tegels (16 okt).
- Kernzinnen ingekort tot max. twee regels, zonder punt; netwerkevent: "Business & pleasure: van inhoudelijke seminars tot cocktail hour met dj" (Maarten). Kopbeeld netwerkevent uitgesneden op de bovenkant zodat hoofden zichtbaar blijven op brede schermen (16 okt).
- Drie doelgroepen: Corporate en reclamebureaus, Venue owners, Dance events. "Dj's en live instrumentalisten" is een dienst, geen doelgroep: weg van Voor wie en uit de voet (djs-live.html bestaat nog, niet gelinkt). Pagina heet Voor wie; geen nummers/"Doelgroepen" op de beelden (16 okt).
- Labels in het casesoverzicht = doelgroepen, met link naar de Voor wie-pagina; bron cases.json. Indeling: productlancering, jubileum, netwerkevent → Corporate; ADE → Dance events + Venue owners; dj-sets → Dance events + Corporate (Maarten); systeemadvies (AV-partij) → Dance events (Maarten); privé-event → Dance events (16 okt).
- ADE-kopbeeld: hele foto zichtbaar door zijkanten aan te vullen met een sterk vervaagde versie van dezelfde foto (img/ade-breed.jpg); spiegelen gaf zichtbare dubbele speakers en is niet gebruikt (16 okt).
- Systeemadvies-kopbeeld idem verbreed met vervaagde zijkanten (img/systeem-breed.jpg, scripts/verbreed.py). Kopbeelden groeien mee op brede schermen (hoogte max. 44vw/78vh i.p.v. 640px), zodat er minder wordt afgesneden (16 okt).
- ADE: nieuw breed beeld van Maarten (img/ade-park.jpg) als kopbeeld en tegel; verbrede versie vervalt (16 okt).
- Jubileum-kopbeeld: hele foto met dj en saxofonist zichtbaar (img/jubileum-breed.jpg, vervaagde zijkanten). Gezichten in beeld; Maarten vraagt de saxofonist om toestemming vóór de site live gaat — OPEN PUNT (16 okt).
- Dj-sets: nieuwe brede portretfoto van Maarten (img/dj-maarten-breed.jpg) als kopbeeld en tegel, vullend zoals de andere cases (16 okt).
- Geen cursief op de hele site; citaten rechtop in Advent Pro, zonder extra aanhalingstekens (het uitgesneden teken volstaat) (16 okt).
- Homepage: zwarte kop met groot logo en ondertitel "High End Audio Rental"; foto met payoff, lead en WhatsApp-knop eronder (16 okt).
- Homepage-kop met groot logo in zwarte balk teruggedraaid (balk te groot). Nu A = vorige versie (index.html); proef B = klein logo in balk, payoff groot op de plek van het logo (home-b.html) (16 okt).
- Homepage: gekozen voor A (groot logo op de foto). Logo op desktop ca. 13% kleiner (max 660px); op mobiel minder ruimte tussen logo en payoff. Proefpagina B verwijderd (16 okt).
- Headerbeeld homepage: lichter blauwe versie met lichtbundels (img/hero-dansvloer-blauw.jpg); op mobiel uitsnede naar links zodat het felle punt naast de payoff valt (16 okt).
- Over HEAR: kop "Founder story – Maarten Versteeg", ondertitel "DJ sinds 1993 · Communicatiespecialist sinds 2000 · Founder HEAR"; hoofdfoto met mixer en koptelefoon (img/maarten-mixer.jpg), adviseursfoto bij de alinea over communicatieadvies (img/maarten-adviseur.jpg). Oude foto (442px, onscherp) niet meer gebruikt (16 okt).
- Founder story: tekst losser gemaakt op stijl, inhoud gelijk (akkoord Maarten); opening "Ik ben Maarten." (16 okt).

## 16 okt — Dienstenpagina's gevuld
- Acht dienstenpagina's gebouwd uit content/diensten.json (scripts/bouw-diensten.py): kernzin, vullend kopbeeld, intro, blokken per merk/product/werkwijze, productrij met beelden, verwijzingen onderaan. Geen vaste drietrap meer.
- Bronnen: Concept assortiment-presentatie (zonder prijzen), RCF KX-filosofie en KXL 4-A/SUB 9000-handleidingen, Brooklyn Audio-ontwerpfilosofie en Prospect-spec, ADJ-specs (Par Z150 RGBA Plus, ElectraPix Par 7, Focus CMY Compact), J-torenontwerp.
- Beelden rechtgezet: vintage lighting toont nu de Astrodisco (was dj-foto); booth toont de booth van bovenaf; artiesten toont dj + saxofonist; AV as a service toont een gala-opstelling. Productbeelden uit de presentatie staan in img/diensten/.
- Producten (navigatie) / Producten en diensten (paginakop en koraalblok), was Diensten (17 okt). Dienstenoverzicht: nummers "01 · DIENSTEN" van de tegels; ondertitel vervangen; "In het kort" (dubbel) weg.
- djs-live.html (oude doelgroeppagina, nergens meer gelinkt) verwijderd; inhoud zit in artiesten.html.
- TE VERIFIËREN door Maarten: ADJ Focus CMY Compact en Chauvet "Force X" als eigen assortiment; herkomst/rechten van gala.jpg, dansvloer.jpg (Holland Festival), beams.jpg; tegeltitels nog Engels (footer Nederlands).
- Dienstenpagina's: openen met de productrij (geen vullend kopbeeld), intro over de volle breedte; RCF-beelden van Maarten toegevoegd (KXL 4-A, KX-serie) (16 okt).
- Principepagina's gevuld uit content/principes.json (scripts/bouw-principes.py), zelfde opbouw als diensten; Nederlandse namen: Partnership, Uitstraling, Slimme oplossingen, Warm geluid. Bronnen: presentatie-filosofie, Lighting Plan-ontwerpprincipes, Abbey-propositie, Maartens website-uitgangspunten (17 okt).
- Hoofdnavigatie: Cases eerst, dan Voor wie, Principes, Producten, Over HEAR (ook mobiel menu). Reden: sluit aan op homepage die met werk begint (17 okt).

## 17 okt — Engelse versie
- Engelse pagina's onder /en/ voor homepage, casesoverzicht, 8 cases en Over HEAR. Bron: content/en.json (exacte NL→EN paren) + titel_en/tekst_en/naam_en in cases.json; scripts/bouw-en.py bouwt site/en/ en stopt als een NL-tekst niet meer gevonden wordt (bewaking tegen uit elkaar lopen).
- Taalwissel NL/EN rechts in de kopbalk op alle pagina's; op nog niet vertaalde pagina's leidt EN naar de Engelse homepage. Engelse pagina's linken voor niet-vertaalde onderdelen naar de Nederlandse pagina.
- hreflang-links in de head van vertaalde pagina's.
- Vorige/volgende op casepagina's volgt nu de volgorde en titels van cases.json (NL en EN); radio-mixes sluit de keten.
- Werkwijze: na elke wijziging aan een vertaalde NL-pagina ook en.json bijwerken en bouw-en.py draaien.

- 2026-10-17: Technics-tegel: onderschrift "Need we say more?" (grap, legendarisch apparaat behoeft geen uitleg). Producten-overzicht: nieuwe boothfoto (booth-verlicht.jpg); detailpagina houdt de foto van bovenaf.
- 2026-10-17: Boothfoto op productenoverzicht vervangen door echte foto (skatehal), bijgesneden zodat gezichten buiten beeld blijven. Geen AI-beelden op de site.

## Actiepunten na gesprek positionering (2026-10-17, nog niet uitgevoerd)
Besluiten van Maarten:
- Positionering: boutique, niet luxury. Het woord één keer op Over HEAR, verder voelbaar maken.
- Communicatieachtergrond alleen op de corporate-pagina; inhoudelijke bijdrage mogelijk, HEAR wordt geen evenementenbureau.
- Convergeren: geen nieuwe pagina's of categorieën. Abbey pas als het operationeel is.
- HEAR niet presenteren als technische backend van de twee netwerken.
- Listening bars: toekomstige niche onder Venue owners, geen eigen pagina.
Te wegen bij redactie principes en founder story:
- Zes overtuigingen als onderlaag voor de vier principes (doel voor middelen; techniek dient beleving; kwaliteit door bewuste keuzes; esthetiek en functie versterken elkaar; samenhang en ontwikkeling; warmte en karakter als rode draad).
- Uit dj-bio: curatie, ontwikkeling (van geel naar rood via de tussenkleuren), eigen signatuur.
- Founder story: verhaallijn van "carrièreswitch" naar "uitbouw van wat er al was" (catwalks, beurzen, congressen met bureaus). Toon van de huidige tekst behouden.
- Corporate-pagina: Strategie → Gewenste beleving → AV-ontwerp → Uitvoering, met blok "Verder kijken dan de techniek".
- 2026-10-17: Homepage-slider: doelgroepen als losse labeltjes (kapitaal, dunne rand, afgerond). Doelgroepnaam "Corporate klanten" → "Corporate" (NL en EN, overal).
- 2026-10-17: Boothpagina: nieuwe tekst van Maarten (intro, Zo werken we, Monitoring, De booth, Spelregels). Standaard booth: drie CDJ-3000X + V10 of Euphonia. Monitoring: 808+515 op oorhoogte of KXM-25 wedges. Lijststijl in secties toegevoegd.
- 2026-10-17: Boothpagina: RCF KXM 25-A toegevoegd aan productrij (15" coax, 137 dB; geverifieerd op rcf.it). Schrijfwijze "KXM 25-A" zoals RCF.
- 2026-10-17: TONE OF VOICE (Maarten): expertise laten merken via signaalwoorden, niet uitleggen. Eén vakterm per tegel of alinea die een vakgenoot herkent en waar een leek overheen leest zonder te struikelen (frontfill, delay, coherent, dual file management). Geen uitleg erbij, geen opsomming van specs. Niet uitleggen, wel laten merken.

- 2026-10-17: Productpagina's: intro nu boven de productrij (was eronder), geldt voor alle acht.
- 2026-10-17: Dansvloerverlichting: twee producten met elk twee foto's naast elkaar in één tegel (veld `beelden`), met videolink (veld `link`, opent in nieuw venster). Programmeertekst omgedraaid: "Indien nodig programmeren we vooraf een show die past bij het event".
- 2026-10-17: Vintage licht: Astrodisco- en scannertekst van Maarten. TE VERIFIËREN: lamptype in de scanners (Philips MSR of Osram HMI); "warme kleuren" vervangen door "rijke, verzadigde kleuren" omdat HMI/MSR koud wit (±5600 K) is.
- 2026-10-17: Vintage licht: Golden Scan staat in de blokkop maar is niet in bezit; bij vraag in te huren of te kopen. Aankoop afgewezen (accent-rol, stroom, lampkosten). Robozap afgewezen (zaalvuller zonder tekening). Feiten voor de tekst: Roboscan = Philips MSD 250/2 (8500 K), Golden Scan = HMI/MSR 575 (±6000 K); gasontlading is NIET warmer dan led, wel vol spectrum en kleine bron → claim is "rijke, verzadigde kleuren", nooit "warm".
- 2026-10-17: Scannerbeeld vervangen door fabrieksfoto met blauw/gele bundel. WENS: eigen foto van de scanners in een zaal, bundels door nevel achter de booth.
- 2026-10-17: Adviespagina herschreven naar drie treden (gratis tips via WhatsApp / begeleid inkooptraject op uurbasis, merkonafhankelijk / AV as a service, vast maandbedrag, minimaal 3 jaar). Geen merknamen meer op deze pagina (onafhankelijkheid); wel productspecialisten. Inkooptraject als stappenflow (ruimtescan → advies → demonstratie → training). Chauvet-vermelding daarmee weg.
- 2026-10-17: Over HEAR: structuurkader onder het profiel (oprichter, techniek, leveranciers, partners). NL en EN.
- 2026-10-17: Artiestenpagina in ik-vorm (bewust ingeleid in de intro, zoals de founder story); smaakbewaker/tussenpersoon, rechtstreeks + artiestenbureaus, één aanspreekpunt, WhatsApp-knop. Architects in Music hier weg (staat in structuurkader Over HEAR).
- 2026-10-17: Adviespagina visueel: blokkoppen (Even sparren? / Van vraag naar de juiste installatie. / Wel de kwaliteit. Niet de aanschaf.), stappen als witte kaarten met turquoise bovenrand en groot nummer, AV as a service als zwart blok. Overgenomen uit Maartens A4-ontwerp; de vier pastelkleuren niet (huisstijl: één accentkleur). Bouwscript: blok-velden `kop` en `donker`.

- 2026-10-17: WhatsApp-knop sitewide in één vorm: pil, icoon links, "Stel je vraag via WhatsApp", pijl rechts, koraal met dunne zwarte rand (naar Maartens buttonsheet). Tekst overal gelijk, ook EN. SoundCloud- en maartenversteeg.nl-knop zelfde vorm in turquoise.
- 2026-10-17: Nieuws: template en overzicht (content/nieuws.json → scripts/bouw-nieuws.py). Niet in de navigatie; bereikbaar via de link. Elk bericht krijgt Open Graph-metadata en een deelbeeld 1200×630 (foto + zwarte balk met HEAR-logo, turquoise lijn) zodat de link op LinkedIn/Facebook als kaart met beeld, titel en domein verschijnt. Eerste bericht: KXM 25-A (voorbeeld, door Maarten te reviewen of verwijderen). TE DOEN: basis-URL naar hear.nl bij livegang.
- 2026-10-17: Nieuws toch in de hoofdnavigatie (rechts, naast EN), in het menu en in de voet onder Werk. Ritme: één bericht per maand. Nieuws = stroom, cases = selectie; een goed eventverslag kan later case worden en een zwakkere case vervangen.
- 2026-10-17: CTA-beleid: productpagina's "Vraag een voorstel aan" onder de intro (voorstel, niet offerte); cases, Voor wie en Over HEAR een brugzin + "Stel je vraag via WhatsApp"; adviespagina houdt de vraagknop in het tipblok. Eén kanaal: WhatsApp (geen mailknop; adres staat in de voet). Elke knop heeft een voorgevuld bericht per pagina, zodat Maarten ziet vanaf welke pagina iemand komt. NA LIVEGANG: CRM/marketingflow/onboarding pas bouwen als het verkeer bekend is; Cloudflare Web Analytics overwegen.
- 2026-10-17: Principes = één pagina met jogwheel (CDJ-achtig bedieningselement): tik/swipe/bolletjes wisselen van principe, titel op het display, statement + intro + "Waar merk je dit aan?" eronder. Geen labels op de ring (aantal principes kan groeien), geen doorklik (geen sales in die laag). Vier subpagina's verwijderd; links in voet/menu wijzen naar ankers. Teksten volgen van Maarten. Jog NIET op producten (overzicht is daar belangrijker; test afgewezen).
- 2026-10-17: Nieuwsbericht 808+515: tekst van Maarten. GECORRIGEERD: KX 515-A heeft 2.000 W piek (600 HF + 1.400 LF), niet 1.000 W; dekking 100°×70° (H×V); 9,8 kg klopt. SUB 808-AS 2.000 W piek klopt. Bron: RCF-datasheet.
- 2026-10-17: Vorige/volgende binnen hetzelfde niveau (producten, cases) als subtiele links rechtsboven in de zwarte kop, naast het kruimelpad; op mobiel alleen pijlen. De bottomnav onderaan is vervallen. Niet op principes (wiel) en niet op nieuws.
- 2026-10-17: Kruimelpad zonder pijl, als sectielabel "Sectie | Pagina" (op mobiel alleen de sectie). Zijnav rechtsboven: pijlen met positiebolletjes (één per pagina op dat niveau, klikbaar), zodat zichtbaar is dat er meer is. Geldt voor producten en cases.
- 2026-10-17: Eén knop per pagina (WhatsApp). SoundCloud, maartenversteeg.nl en interne verwijzingen in nieuwsberichten zijn inline links (kleine kapitalen, onderstreept, icoon + pijl). Turquoise knop afgeschaft.
- 2026-10-17: Principes herzien naar hiërarchie waarden → principes → waar merk je dit aan. Vier waarden op het wiel: Samen, Warmte ("Je gaat uit, maar je bent toch thuis"), Vakmanschap, Open. Uitstraling en Slimme oplossingen zijn principes onder Vakmanschap geworden; Gelijkwaardig onder Samen; "with a twist" is de pagina-intro. AFGEWEZEN door Maarten: "Hard is makkelijk. Warm is moeilijk." (voelt niet menselijk geschreven). BEWAARD voor later: "Thuis in uitgaan" als mogelijke HEAR-regel (homepage/logo). Communicatieachtergrond hier één bijzin; uitwerking op corporate-pagina.
- 2026-10-17: Principes-structuur definitief: waarde (statement + intro) → "Voor onze manier van werken betekent dit:" (één lijst; principes en waarnemingen samengevoegd, niets dubbel). Samen: statement "Zonder samenwerking bestaan we niet", lijst van Maarten + gelijkwaardig als gedrag met verwachting.

## 17 okt 2026 — sloganscan

Hele site gescand op slogans. Maarten kreeg alleen jeuk van: "Van vraag naar de juiste installatie.", "Wel de kwaliteit. Niet de aanschaf.", de noot "Geen merkenlijst als vertrekpunt…", de corporate-slotalinea ("…vergroten de impact van het moment") en "Een knipoog mag, als er een gedachte achter zit." Alle vijf vervangen/geschrapt; de knipoog-bullet is helemaal weg (je eigen grap uitleggen is dezelfde jeuk). De nieuwe corporate-slotalinea ("twee dingen doen") is een plaatsvervanger: Maarten weet niet of dat dé twee dingen zijn, de corporate-sectie wordt nog gereviewd. "Business & pleasure" blijft als kop, samengevoegd met de concretere ondertitel. De rest (Hear the difference, Transformeer-lead, Klein maar groot, Best of both worlds, industry standard, Zwitserse zakmes, oh ja/oh wow, Who knows, Need we say more?) blijft bewust staan.
Patroon (Maartens woorden): het zit in het trucje, van…naar en niet a maar b. Die zinnen zijn te uitleggerig: alsof je moet uitleggen wat iemand moet voelen of ervaren, of alsof je het uitlegt aan iemand die het niet snapt. Regel: een slogan mag als hij zonder toelichting werkt (Klein, maar groot; Need we say more?); hij valt af zodra hij het denkwerk voor de lezer doet. Bijzonder geval van de tone-of-voice-regel "expertise laten merken, niet uitleggen".

## 17 okt 2026 — principes: Open af

Display "Met een open vizier". Waarde: dansvloer als vrijplaats (zijn wie je bent, de ander diezelfde ruimte gunnen). Kop boven de lijst is per waarde instelbaar (`werkwijze_kop` in principes.json); bij Open: "Die openheid vinden wij belangrijk, en je ziet haar terug in kleine dingen". Vier punten: nieuwsgierig, kritiek om van te leren, niet oordelen zonder te bevragen, geen samenwerking met partijen die openlijk discrimineren. Tekst van Maarten; alleen tot volzinnen gemaakt en wij/we gelijkgetrokken.

## 18 okt 2026 — principes: volgorde en bullets

Volgorde waarden: Samen, Open, Vakmanschap, Warmte (ook in de voet, NL en EN). Open: kop boven de lijst weg, zin is onderdeel van de alinea (`werkwijze_kop: null`). Warmte: "artiest zie en hoor je" → "Afhankelijk van de wens van de opdrachtgever is het ontwerp opvallend of juist afwezig"; "avond heeft een verloop" → "Licht, geluid en visuals zijn afgestemd op de energie van het moment"; "na afloop hoor je nog" weg. Vakmanschap: "weinig lampen en kasten" → "multi-inzetbare en modulaire systemen"; "opbouw klaar voor de gasten" en "merknamen en modelnummers" weg. Uurbasis komt nergens meer voor (klant mag ook een losse som betalen). Open: naam/statement/intro van Warmte in bespreking ("sfeer over spektakel").

Hoofdnavigatie (Maarten, 18 okt): Cases · Voor wie · Producten · Principes · Over HEAR · Nieuws. Van buiten naar binnen; Principes en Over HEAR vormen het HEAR-cluster rechts. Optie B (Producten voorop) afgewezen: "klassiek leverancierssite en dat zijn we niet". Homepage-blokken en mobiel menu in dezelfde volgorde. Warmte: "zodat je kunt dansen en toch een gesprek kunt voeren" weg (uitleggerig; warm kan ook diep op de dansvloer zijn); nu "We maken het geluid warm en vol op elk volume, met het midlaag erbij." en sprekersverstaanbaarheid als eigen bullet.

## 18 okt 2026 — Waarden i.p.v. Principes; Warme sound

Navigatie-item "Principes" heet nu "Waarden" (EN: Values); mobiel menu "Waarden — Wat wij belangrijk vinden"; pagina heet "Waarden en uitgangspunten" (EN: Values and principles); voetlabel "Waarden". URL blijft principes.html (ankers in voet en elders). Reden (Maarten): het zijn waarden, behalve Warme sound; "waarden en uitgangspunten" dekt een breder geheel; "wat wij belangrijk vinden" is de algemene noemer.
Vierde waarde heet "Warme sound" (was Warmte). Mijn herschrijving ("Het moet warm blijven klinken…", huiskamer-intro) resoneerde niet. Tekst van Maarten: statement "Wij geven om sfeer en warm geluid."; intro over geluid als onbewuste sfeerbepaler (schel → ongemakkelijk; onduidelijk → vermoeiend door compenserende hersenen; warm en verstaanbaar → sfeer omhoog zonder te weten waarom; licht spectaculair wanneer nodig, subtiel als dat beter past; uitgaan voelt als thuis, uren blijven). "Je gaat uit, maar je bent toch thuis" is daarmee van de site; "Thuis in uitgaan" blijft kandidaat voor de homepage.
Kop "Voor onze manier van werken betekent dit" en de lijn erboven overal weg: de lijst volgt direct op de alinea (scheelt ruimte, en was al niet consequent). Eerste bullet (Maarten): deephouse-achtergrond, warm/rond/vol, ook visuals moeten warmte hebben.
Nieuws: de EN-knop op nieuwspagina's leidt naar de Engelse homepage (ging naar de Nederlandse). Engels nieuws is er niet; staat bij de open vertaalpunten.

## 18 okt 2026 — stand na de nachtsessie

- Maarten heeft alle teksten zelf gemaakt of gereviewd, behalve alles onder "Voor wie is HEAR" (doelgroepen.html, corporate, venue-owners, dance-events). Dat is het enige onderdeel dat nog op zijn review wacht.
- Review van ChatGPT op de site volgt; nog te bespreken.
- Vanaf deze draad kan Claude de live site zelf bekijken (browser in de desktop-app, echte fonts, desktop en mobiel). De beperking uit de overdracht (geen zicht op workers.dev) geldt niet meer.
- ChatGPT-review (per pagina) ontvangen en opgeslagen als docs/review-chatgpt-2026-10-18.md. Nog niet besproken; bespreken op 18 okt overdag.

## 18 okt 2026 — ChatGPT-review, HOME

- Oprichter-zin op de homepage: "met cutting-edge techniek en muziek uit de dancescene" → "met techniek en muziek" (NL en EN).
- Doelgroepomvang overal 150–1.500 (founder story NL/EN stond op 100).
- Propositie-alinea op de homepage (ChatGPT's hoofdaanbeveling): GEPARKEERD. Hypothese van Maarten: wat ChatGPT mist komt deels doordat de brug "Voor wie" nog niet goed is ingevuld; eerst een sterke corporate-tekst onder doelgroepen, dan opnieuw kijken of de homepage nog iets nodig heeft.
- Corporate zichtbaarder op de homepage: nog niet besproken (4 van de 7 slidercases zijn corporate; het gaat om volgorde/beeld, niet om inhoud).
- Hero-lead "Transformeer…" blijft (bevestigd door de review).
- Slidervolgorde: Seminar en netwerkevent geruild met Skatehal, zodat de eerste drie tegels corporate zijn (Productlancering, Seminar, Jubileum). Volgorde geldt ook voor het cases-overzicht en vorige/volgende op de casepagina's.

## 18 okt 2026 — ChatGPT-review, CASES

- DJ-sets, resultaat: "een connaisseur met" weg → "toont een brede platenkennis en gevoel voor samenhang."
- Systeemadvies, resultaat (tekst Maarten): "Goed advies verkleint de kans op een kostbare verkeerde aanschaf, bijvoorbeeld wanneer later blijkt dat je systeem niet schaalbaar is als je verder groeit." De oude tweede helft ("…opdrachten van vandaag én de groei van morgen") is vervallen, dubbelde met de nieuwe bijzin.
- Privéfeest, uitvoering (tekst Maarten): "Door een mix van washlights en zwarte doeken was er niks meer te zien van al het metaal in de ruimte en werd het geluid minder weerkaatst." Vervangt de eerste zin die de kop herhaalde. Resultaat-alinea herhaalt de kop nog; niet aangepast.
- CreativeGrounds/Jubileum lege citaatkop: was al weg (nacht 17/18 okt). Overige cases bewust ongemoeid.
- Engels van alle drie mee.
- Over HEAR, structuurkader Partners: Ronald Pronk Photography toegevoegd (NL en EN).
- 2026-10-18: Producttegels sitewide maximaal 3 per rij (desktop), 2 per rij op mobiel (≤700px; was 1). Boothpagina houdt de verdeling 3-2-2 via optie `rijen` in diensten.json (productrij-blok). Brede tegels met twee foto's (dansvloerlicht) blijven over de volle breedte.

## 18 okt 2026 — Special projects → Custom dj-sets, playlists en remixes

- Categorie hernoemd (Maarten): pagina/voet "Custom dj-sets, playlists en remixes", overzichtstegel "Custom DJ sets, playlists & remixes" (Engelse tegelnamen zoals de rest), EN-voet "Custom DJ sets, playlists and remixes". URL blijft special-projects.html.
- Kernzin: "Dj-sets, playlists en remixes op maat". Intro: "Naast events werken we aan muziek zelf: dj-sets op maat, radio-uitzendingen, eigen edits en remixes, en playlists voor horeca." De zin "Het houdt ons oor scherp…" is weg (ChatGPT-punt; met de hernoeming is ook de vraag "moet dit een categorie zijn" beantwoord).
- Nieuw blok "Playlists op maat" (naar aanwijzing Maarten, formulering van mij): "Voor een koffiebar, café of andere horecazaak stellen we een playlist samen die past bij jouw zaak. Met de hand geselecteerd uit onze eigen collectie, zonder vervuiling door generieke AI-muziek."
- Boothpagina: tegel Dj-booth krijgt nieuwe foto (CDJ-3000X-opstelling met camera op gorillapod, img/diensten/booth-cdj-camera.jpg); booth-bovenaf.jpg blijft in de map.
- 2026-10-18 (Maarten, n.a.v. ChatGPT-review): luisterervaring (warm/helder/dekking) blijft op Waarden, niet herhalen op High-end audio. Privéfeest resultaat-alinea blijft. Boothtegel-tekst blijft bij de nieuwe foto. Boothpagina houdt 3-2-2 (geluid staat dan bij elkaar). Spotify-stockbeeld voor de Custom-tegel afgewezen; Deep Radio-beeld blijft.
- 2026-10-18: Custom dj-sets: blok "Edits en producties", tekst Maarten: "Eigen edits, remixes en producties, analoog gemasterd, duiken op in sets, in het netwerk van dj's waarmee we werken en in de toekomst ook in releases." (alleen komma na "gemasterd" toegevoegd).

## 18 okt 2026 — Productenoverzicht als doorklikpagina

- Aanleiding (Maarten): Luxonos houdt de merksite vrij van gear en zet verhuur op een aparte site; bij HEAR mag het overzicht geen galerij zijn waar je blijft hangen. Tegels heten nu als actie: "Bekijk alle dj-gear", "Bekijk alle high-end audio", "Bekijk al het sfeerlicht", "Bekijk al het dansvloerlicht", "Bekijk al het 90's vintage licht", "Bekijk advies en AV as a service", "Bekijk dj's, vocalisten en instrumentalisten", "Bekijk custom dj-sets, playlists en remixes", elk met koraalkleurige pijl die bij hover verschuift. Daarmee zijn de Engelse categorienamen op het overzicht vervallen (stond op de te-verifiëren-lijst).
- Dj-geartegel toont de Euphonia (was de verlichte booth). Overige tegelbeelden ongewijzigd.
- 2026-10-18: Waarden-intro, tekst Maarten: "Achter alles wat we doen zit een intentie. Dat is althans wel de bedoeling :-) Die bepaalt wat voor keuzes we maken, bijvoorbeeld in ons assortiment of onze manier van samenwerken. Twee waarden en twee uitgangspunten bepalen die keuzes." Ingrepen: "naken"→"maken", "Die bepalen"→"Die bepaalt" (verwijst naar intentie), komma voor "bijvoorbeeld", "of manier"→"of onze manier". Op desktop staat de intro nu in dezelfde kolom als de waardentekst rechts van het wiel.
- 2026-10-18: Overzichtstegels zonder "al/alle": Bekijk dj-gear · Bekijk high-end audio · Bekijk sfeerlicht · Bekijk dansvloerlicht · Bekijk 90's vintage licht · (rest ongewijzigd).
- 2026-10-18: Samen, intro (tekst Maarten): "HEAR is een netwerk van professionals, leveranciers en artiesten in muziek, geluid en licht. Zo kijken we ook naar opdrachtgevers: als partners in ons netwerk, die alleen samen iets moois kunnen maken." Regel (Maarten): op een verzamelpagina moet zichtbaar zijn dat de bezoeker kiest; doorklik-tegels op Producten bevallen; Voor wie en Cases nog te bekijken.
- 2026-10-18: Verzamelpagina-regel toegepast: Cases-overzicht krijgt "Bekijk de case →" licht in kapitalen linksonder op het beeld (ook EN: "View the case"); Voor wie krijgt het label "Dit is wat wij doen" linksboven op de drie tegels (bestaande kicker-stijl).
- 2026-10-18: "Bekijk de case →" ook op de beelden in de homepage-slider (EN: View the case), zelfde stijl als het cases-overzicht.
- 2026-10-18: Custom dj-sets: knop "Vraag een mix of playlist aan" (Maarten dicteerde "mix op playlist", gelezen als "of"); voorgevuld bericht "Hoi Maarten, ik wil graag een mix of playlist op maat aanvragen." Bouwscript: velden cta_tekst/cta_bericht per pagina.
- Over HEAR, Partners: Biezema AV en Deep Radio toegevoegd (NL en EN).
- 2026-10-18: Over HEAR: structuurkader verplaatst naar onder de foto. Desktop: linkerkolom naast het verhaal, plakt aan de onderkant van het scherm zodat foto + kader in beeld blijven tijdens het lezen. Mobiel: foto → kader → verhaal (Maarten: kader maakt de naam als founder duidelijk vóór de ik-intro, en toont meteen het netwerk). Engels mee.
- 2026-10-18: Over HEAR, kader: Leveranciers en Partners samengevoegd tot "Partners en leveranciers" (EN: Partners and suppliers), volgorde Maarten: Output Professional, Highlite, Moonbears, Chauvet Benelux, RCF, Brooklyn Audio, Architects in Music, AIMM Entertainment, Base Events, Biezema AV, Luxonos, Brandon AV, Deep Radio, Ronald Pronk Photography en anderen. Reden: scheiding is kunstmatig (Output wil partner zijn, Luxonos is verhuurbron én relatie). TE VERIFIËREN: Luxonos en Brandon AV melden dat ze op de site staan.
- 2026-10-18: Over HEAR, CTA: knoptekst "Stuur me een appje" (EN: Send me a message); brugzin "Kennismaken?" blijft. Enige pagina met afwijkende knoptekst, past bij de ik-vorm.
- 2026-10-18: Case Systeemadvies, CTA: brugzin "Meer weten over audio-advies?" (was "Zoiets voor jouw event?"; EN: Want to know more about audio advice?), knop blijft "Stel je vraag via WhatsApp"; voorgevuld bericht aangepast naar advies voor de eigen ruimte. Schrijfwijze "audio-advies" met koppelteken.
