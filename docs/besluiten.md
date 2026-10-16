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
- ADE-case: bronvermelding wordt "Artist management Rivo".
- DJ-sets-case: het citaat is echt (Architects in Music). Bron vervangen door "Architects in Music — A full circle event company with a focus on hospitality" (16 okt).
- Privé-event (Ronald Pronk): blijft. Ronald heeft toestemming gegeven. De case laat ook zien dat privé de uitzondering is.
- Uitgelicht werk op de homepage = slider met alle afgeronde cases, gevoed vanuit `site/cases.json` (één regel per case; volgorde = volgorde op site; alleen status "af" wordt getoond). Dubbeling met de casespagina is akkoord: die is het visuele overzicht. Halve cases worden nergens getoond.
- Tuinfeest-case heet voortaan **Jubileum ondernemersnetwerk** (CreativeGrounds, 5-jarig bestaan, 150 ondernemers). Citaat binnen; naam van de spreker volgt. Tegel: dansvloerfoto; casepagina: dj en saxofonist (16 okt: saxofonist was te dominant op de tegel).

### Vormgeving
- Kleuren volgen het huisstijldocument (Branding DEF): zwart en gebroken wit als basis, accent mag hoofdkleur van een vlak zijn, max. twee kleuren per vlak. Geen crème/beige.
- Homepage v1 (15 okt): zwarte hero met booth-foto en groot HEAR-merk, koraal statementvlak, tegels op gebroken wit, koraal als WhatsApp-knop. Koraal alleen op donker of als vlak met zwarte tekst (op gebroken wit te weinig contrast voor kleine tekst).
- Homepage-opbouw (16 okt, herzien): topnavigatie vervangen door hamburgermenu; na het statement een compacte navigatiebalk met zes onderdelen + korte uitleg (Doelgroepen · Voorbeeldcases · Principes · Diensten en producten · Merken en techniek · Over HEAR). Variant met grote regels (B) afgewezen: te veel ruimte. Daarna: Uitgelicht werk (slider, zie Cases) · Over HEAR · afsluiter met WhatsApp · uitgebreide footer met alle onderdelen (laat diepte zien). Hero: één knop (WhatsApp); ondertitel staat onder het merk.
- Homepage-opbouw (16 okt, v3): hero · Uitgelicht werk (cases omhoog) · koraal blok met de overige onderdelen (Doelgroepen · Principes · Diensten en producten) · Over HEAR met press photo · afsluiter · footer. Statementtekst en de witte navigatiebalk vervallen (kleur koraal bleef). 'Merken en techniek' gaat op in 'Diensten en producten'; merken worden toegelicht op de pagina's over geluid/licht. Topnavigatie: Doelgroepen · Cases · Principes · Diensten · Over HEAR.
- 16 okt: 'Doelgroepen' heet op de homepage 'Voor wie is HEAR' (topnav: 'Voor wie'); doelgroepen is inside-out. Over HEAR-tekst homepage: "Als dj, corporate communicatieadviseur én eigenaar van HEAR verbind ik de corporate evenementenwereld met cutting-edge techniek en muziek uit de dancescene." ('daarnaast' was zwak). Casetitels in slider: Transformatie: van skatehal tot dansvloer · Seminar en netwerkevent · Een reis door 40 jaar elektronische muziek · Advies over het beste soundsystem voor jouw ruimte · Van industriële ruimte naar intieme sfeer.
- Logo-lockup teruggedraaid (16 okt): pay-off weer als losse kop "Hear the difference" (zonder punt); HEAR-logo linksboven in de hero, tekstblok onderin. (Lockup-proef staat in git.) Eerder: "Hear the difference" (zonder punt: het is logo) onder het logo, kleine letter, uitgevuld tot exact de breedte van het logo (SVG). Kop als aparte tekstregel vervalt (blijft onzichtbaar voor zoekmachines/schermlezers). Over HEAR: "eigenaar" wordt "founder".
- Typografie in reeksen (16 okt): koppen in kaarten en blokken krijgen de hoogte van twee regels, zodat de tekst eronder gelijk staat; woorden evenwichtig verdelen, geen los woord op de laatste regel.
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
