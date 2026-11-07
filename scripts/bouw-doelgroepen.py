"""Bouwt de vier doelgroeppagina's onder "Met wie we werken" (besluit 6 nov 2026) en het 2x2-blok
"Wij werken graag samen met…" op de homepage en op doelgroepen.html.
Teksten staan hieronder per pagina; concepten en besluiten in docs/concepten/doelgroep-*.md.
Opbouw per pagina: kop · beeld · intro · (eigen blokken) · aanbod · werkwijze (stappenkaart) · (vaste installatie) · contact · eerder werk.
Het contactformulier post naar /api/aanvraag (bron = de pagina). De Engelse versies maakt bouw-en.py
met de paren in content/en.json (paginas → de vier bestanden). Draaien vóór bouw-en.py en bouw-og.py: python3 scripts/bouw-doelgroepen.py"""
import json, re, html, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
site = root / "site"
e = lambda t: html.escape(t, quote=True)

# volgorde = volgorde in tegels, zijnav en voetmenu
DOEL = [
 dict(bestand="zakelijke-events.html", kort="Eventmanagers", tegel="Eventmanagers en communicatieprofessionals",
      uitleg="Die namens hun werkgever of opdrachtgever een netwerkdag, seminar of zakelijke borrel organiseren.",
      tegel_en="Event managers and communications professionals",
      uitleg_en="Who organise a networking day, seminar or business drinks on behalf of their employer or client.",
      beeld="img/doelgroepen/eventmanagers.jpg", pos="62% 40%", alt="Twee eventmanagers overleggen met laptop en tablet op het terras van een eventlocatie"),
 dict(bestand="dance-events.html", kort="Dance-events", tegel="Organisatoren van (dance)&nbsp;events",
      uitleg="Promotors of andere ondernemers die een feest met dj's en artiesten organiseren.",
      tegel_en="(Dance) event organisers", uitleg_en="Promoters and other entrepreneurs throwing a party with DJs and artists.",
      beeld="img/doelgroepen/dance.jpg", pos="50% 45%", alt="Twee dj's overleggen achter de booth in rood licht"),
 dict(bestand="merken-en-bureaus.html", kort="Merken en bureaus", tegel="Merken, creatieven en bureaus",
      uitleg="Die een merkactivatie, productlancering, collectiepresentatie, modeshow of in-store event organiseren.",
      tegel_en="Brands, stores, creatives and agencies",
      uitleg_en="Who organise a brand activation, product launch, collection presentation, fashion show or in-store event.",
      beeld="img/doelgroepen/merken.jpg", pos="78% 40%", alt="Een creatief en een projectleider in gesprek in een galerie"),
 dict(bestand="bijzondere-eventlocaties.html", kort="Eventlocaties", tegel="Eigenaren en exploitanten van eventlocaties",
      uitleg="Die steeds een andere klant moeten servicen: vandaag een modeshow, morgen een seminar, overmorgen een bedrijfsfeest met dj.",
      tegel_en="Event venue owners and operators",
      uitleg_en="Who serve a different client every time: a fashion show today, a seminar tomorrow, a company party with a DJ the day after.",
      beeld="img/doelgroepen/locaties.jpg", pos="72% 50%", alt="Een man bekijkt een lege industriële hal met hoge ramen"),
]

def tegels(en=False):
    t = ""
    for d in DOEL:
        kop = d["tegel_en"] if en else d["tegel"]; uit = d["uitleg_en"] if en else d["uitleg"]
        t += (f'<a class="samen-tegel" href="{d["bestand"]}"><span class="samen-beeld"><img src="{d["beeld"]}" alt="" loading="lazy" style="object-position:{d["pos"]}"></span>'
              f'<span class="samen-tekst"><span class="samen-kop">{kop}</span><span class="samen-uitleg">{e(uit)}</span>'
              f'<span class="samen-knop">{"What we do for you" if en else "Wat we voor je doen"} <i aria-hidden="true">→</i></span></span></a>')
    return t
def samenblok(kop="h2"):
    return (f'<section class="samen" aria-labelledby="samen-kop"><{kop} id="samen-kop">Wij werken graag samen met…</{kop}>'
            f'<div class="samen-raster">{tegels()}</div></section>')

# ---------- bouwstenen ----------
def lijst(items, cls="lp-lijst"):
    return f'<ul class="{cls}">' + "".join(f'<li>{a}' + (f'<small>{b}</small>' if b else '') + '</li>' for a, b in items) + '</ul>'
def kaart(titel, items, meer=None, wens=False):
    m = ""
    if meer: m = '<p class="lp-meer">Meer over ' + " en ".join(f'<a href="{h}">{t}</a>' for t, h in meer) + ' <span aria-hidden="true">→</span></p>'
    return f'<div class="lp-kaart"><h3>{titel}</h3>{lijst(items)}{m}' + ('<p class="lp-wens">Speciale wensen? Laat het weten.</p>' if wens else '') + '</div>'
def aanbod(kop, kaarten):
    return (f'<section class="lp-band"><p class="lp-label">Wat we leveren</p><h2>{kop}</h2>'
            f'<div class="lp-aanbod" style="--kol:{len(kaarten)}">{"".join(kaarten)}</div></section>')
def intro(lead, alineas):
    return (f'<section class="lp-band"><div class="lp-twee"><p class="lp-lead">{lead}</p>'
            f'<div class="lp-tekst">{"".join(f"<p>{a}</p>" for a in alineas)}</div></div></section>')
def filo(label, kop, alineas):
    return (f'<section class="lp-band"><div class="lp-twee"><p class="lp-label">{label}</p><h2>{kop}</h2>'
            f'<div class="lp-tekst">{"".join(f"<p>{a}</p>" for a in alineas)}</div></div></section>')
def momenten(label, kop, items, sub=None):
    s = f'<p class="lp-sub">{sub}</p>' if sub else ''
    return (f'<section class="lp-band"><div class="lp-twee"><p class="lp-label">{label}</p><div><h2>{kop}</h2>{s}</div>'
            f'{lijst([(i, None) for i in items], "lp-momenten")}</div></section>')
def paar(kolommen, kop=None):
    kk = f'<h2 class="lp-paarkop">{kop}</h2>' if kop else ''
    k = "".join(f'<div><img src="{b}" alt="{e(a)}" loading="lazy" style="object-position:{p}"><p class="lp-label">{l}</p><h2>{h}</h2><p>{t}</p></div>'
                for b, a, p, l, h, t in kolommen)
    return f'<section class="lp-band lp-donker">{kk}<div class="lp-paar">{k}</div></section>'
def split(beeld, alt, pos, label, kop, tekst):
    return (f'<section class="lp-split"><img src="{beeld}" alt="{e(alt)}" loading="lazy" style="object-position:{pos}">'
            f'<div><p class="lp-label">{label}</p><h2>{kop}</h2><p>{tekst}</p>'
            f'<p class="lp-meer"><a href="over-hear.html#partners">Zie hier onze partners</a> <span aria-hidden="true">→</span></p></div></section>')
def stappen(items):
    return (f'<section class="lp-band"><p class="lp-label">Werkwijze</p><h2>Zo werken we</h2>'
            f'<div class="lp-stappen"><h3 hidden>{items[0][0]}</h3><p hidden>{items[0][1]}</p>'
            f'<ol class="lp-stapjes">' + "".join(f'<li><b>{i+1}</b><div><b>{a}</b><br><span>{b}</span></div></li>' for i, (a, b) in enumerate(items)) + '</ol>'
            '<div class="lp-stapbal"></div></div></section>')
CASES = {c["link"]: c for c in json.loads((site / "cases.json").read_text())["cases"]}
TP = json.loads((site / "cases.json").read_text())["toepassingen"]
def eerder(kop, links, quote=None):
    t = ""
    for l in links:
        c = CASES[l]; chip = TP[c["toepassing"][0]]["naam"]
        t += (f'<a class="lp-case" href="{l}"><img src="{c.get("beeld_breed") or c["beeld"]}" alt="" loading="lazy"' + (f' style="object-position:{c["positie"]}"' if c.get("positie") and not c.get("beeld_breed") else "")
              + f'><div><span class="lp-chip">{chip}</span><h3>{e(c.get("tegel_titel") or c["titel"].replace(chr(10), " "))}</h3><p>{e(c.get("tegel_tekst") or c["tekst"])}</p></div></a>')
    if quote: t += f'<blockquote class="lp-quote"><p>“{quote}”</p><footer>De opdrachtgever</footer></blockquote>'
    kol = len(links) + (1 if quote else 0)
    return f'<section class="lp-band"><h2>{kop}</h2><div class="lp-cases" style="--kol:{max(2, kol)}">{t}</div></section>'
def contact(kop, bron, voorbeeld):
    return f'''<section class="lp-band lp-contact" id="contact"><div class="lp-twee"><div><h2>{kop}</h2><p>Laat je gegevens achter, dan neem ik contact met je op.</p>
<div class="lp-wie"><img src="img/maarten-adviseur.jpg" alt="Maarten Versteeg" loading="lazy" style="object-position:50% 20%"><div><b>Maarten Versteeg</b><span>Oprichter HEAR</span></div></div></div>
<form class="lp-form" method="post" action="/api/aanvraag" data-dank="Dank je. Ik neem contact met je op, meestal dezelfde werkdag." data-fout="Versturen lukte niet. Mail naar maarten@hear.nl of bel +31 6 24560220.">
<input type="hidden" name="bron" value="{e(bron)}"><input type="text" name="website" class="lp-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<label>Naam<input name="naam" autocomplete="name" required></label>
<label>E-mail<input name="email" type="email" autocomplete="email" required></label>
<label>Telefoon<input name="telefoon" type="tel" autocomplete="tel"></label>
<label>Waar gaat het over<textarea name="bericht" placeholder="{e(voorbeeld)}"></textarea></label>
<button type="submit">Verstuur</button><p class="lp-privacy">Ik reageer meestal dezelfde werkdag. We gebruiken je gegevens alleen om je te antwoorden. <a href="privacy.html">Privacyverklaring</a></p>
<p class="lp-melding" hidden></p></form></div></section>'''

# ---------- de vier pagina's ----------
P = {}
P["zakelijke-events.html"] = dict(titel="Eventmanagers en communicatieprofessionals", h1="Eventmanagers en<br> communicatie&shy;professionals",
 beschrijving="Licht, geluid en muziek voor netwerkdagen, seminars en jubilea. Eén aanspreekpunt, met 25 jaar ervaring in corporate communicatie.",
 delen=[
  intro("Een netwerkdag, seminar of jubileum is het visitekaartje van je organisatie. En het moment waarop je je relaties fysiek ontmoet.",
        ["Als eventmanager zorg je dat het programma soepel loopt: het dagdeel met sprekers, de omslag naar de borrel en het informele deel daarna.",
         "Wij zorgen dat de audiovisuele ondersteuning het verhaal volgt. Sprekers zijn goed verstaanbaar, en de cocktail hour die erop volgt krijgt licht en muziek die bij het moment passen. Alles afgestemd op de ruimte, ook als dat een kale industriële hal is die we ombouwen tot eventlocatie."]),
  aanbod("Dit kunnen we je bieden", [
   kaart("Concept en branding", [("Meedenken over concept en sfeer", "Met 25 jaar ervaring in corporate communicatie"),
     ("Je huisstijl in licht", "Sfeerlicht in je huisstijlkleuren en je logo geprojecteerd op wand of vloer"),
     ("Muziek die bij je merk past", "Een playlist of dj-set in de toon van je organisatie, en opkomstmuziek voor sprekers"),
     ("Boodschap en middelen", "Uitnodigingen, speeches en een aftermovie")], meer=[("communicatieadvies", "communicatieadvies.html")], wens=True),
   kaart("Organisatie en techniek", [("Je draaiboek vertaald naar een audiovisuele opzet", "Geluid, sfeerlicht, microfoons en wat er verder nodig is"),
     ("Eén aanspreekpunt voor de AV, ook op de dag zelf", None), ("Een technicus, als je die nodig hebt", None), ("Dj's en bijpassende artiesten", None)],
     meer=[("geluid", "high-end-audio.html"), ("atmosfeerlicht", "atmospheric-lighting.html")])]),
  split("img/maarten-adviseur.jpg", "Maarten Versteeg", "50% 25%", "Hoe we samenwerken", "Eén aanspreekpunt",
        "We zijn je vaste aanspreekpunt voor licht, geluid en muziek. Waar nodig werken we met professionals uit ons netwerk, om op te schalen of om je in contact te brengen met wie je nodig hebt."),
  stappen([("Intake", "Doel, doorloop, aantal gasten en budget. Hier bepalen we wat het event nodig heeft."),
   ("Locatiebezoek of foto's en plattegrond", "We bekijken vooraf de ruimte: akoestiek, stroom en opbouwtijden."),
   ("Voorstel", "Een opzet per programmaonderdeel, met een duidelijke prijs."),
   ("Afstemming", "Het draaiboek naast de techniek. Werkt er een technicus van de locatie mee, dan krijgt die vooraf een korte online briefing."),
   ("Opbouw en soundcheck", "Klaar voordat de eerste gast binnenkomt."),
   ("Op de dag zelf", "Eén aanspreekpunt voor alles wat met licht, geluid en muziek te maken heeft.")]),
  contact("Werk je aan een netwerkdag, seminar of zakelijke borrel?", "Landingspagina eventmanagers", "Bijvoorbeeld: seminar voor 120 gasten in maart, met borrel"),
  eerder("Deze opdrachtgevers gingen je voor", ["gemeentelijk-netwerkevent.html", "jubileum-ondernemersnetwerk.html"])])

P["dance-events.html"] = dict(titel="Organisatoren van (dance) events", h1="Organisatoren van<br> (dance)&nbsp;events",
 beschrijving="Clubgeluid op elke plek: een modulair, doorgerekend geluidssysteem van Brooklyn Audio en RCF, een rider-proof booth en licht dat bij het moment past.",
 delen=[
  intro("Je wilt dat je feest klinkt als een goede club. Ook als het plaatsvindt in een loods, een skatehal of een ruimte die maar één nacht van jou is.",
        ["Als promotor of collectief werk je met een andere locatie per avond, korte opbouwtijden en dj's met een rider. Geef je een eigen feest, dan wil je hetzelfde niveau als de clubs waar je zelf graag komt.",
         "Wij zorgen dat de dansvloer de hele avond werkt: geluid dat overal goed klinkt, een booth waar elke dj meteen kan draaien en licht dat past bij het moment."]),
  filo("Ons geluid", "Gelijkmatig, warm en doorgerekend", [
   "Een goed geluidssysteem is niet het hardste systeem. Het geluid ligt gelijkmatig over de dansvloer: vooraan niet te hard, achterin niet dun. Het geluid is vol, goed verstaanbaar en niet schel, zodat het voor bezoekers prettig blijft.",
   "Daarvoor werken we met twee merken die hun hele systeem zelf ontwerpen en bouwen. Brooklyn Audio uit Nederland ontwerpt al zijn kasten met dezelfde fasekarakteristiek. Daardoor kun je ze in elke combinatie inzetten zonder dat het geluid uit elkaar valt, en klinkt een kleine opstelling hetzelfde als een grote. Van RCF uit Italië gebruiken we de KX-serie, de nieuwe topserie van het merk, met tops die de directheid van een point source combineren met de worp van een line source.",
   "Het systeem is modulair: dezelfde familie speakers past in een compacte ruimte en in een zaal tot 35 meter diep. De opstelling rekenen we vooraf door op de afmetingen van jouw zaal."]),
  aanbod("Dit kunnen we je bieden", [
   kaart("Geluid en booth", [("Een modulair geluidssysteem", "Geschikt voor compacte tot grote ruimtes, doorgerekend op jouw zaal"),
     ("Subs in cardioïde opstelling", "Het laag blijft op de dansvloer en loopt niet het podium en de booth in"),
     ("Een rider-proof booth", "CDJ-3000X met V10 of Euphonia"),
     ("Een forward booth, als je dat wilt", "De dj staat meer de ruimte in, met een danszone om zich heen. De monitoring werkt daar als tweede PA.")],
     meer=[("geluid", "high-end-audio.html"), ("dj-gear", "booth-dj-gear.html")]),
   kaart("Licht", [("Moving heads die je op veel manieren inzet", "Sierlijk in de opbouw van de avond, impactvol op het hoogtepunt"),
     ("Sfeerlicht dat de ruimte vormgeeft", "Draadloze washlights op muren, pilaren en staal"),
     ("Vintage clublicht", "Opgeknapte verlichting uit de clubs van de jaren 90, zoals Astrodisco en Golden Scan")],
     meer=[("atmosfeerlicht", "atmospheric-lighting.html"), ("dansvloerlicht", "dancefloor-lighting.html")]),
   kaart("Line-up", [("Een complete line-up", "We stellen de hele avond samen, of vullen jouw line-up aan"),
     ("Live muzikanten bij een dj-set", "Percussie, saxofoon of vocals")], meer=[("dj's en artiesten", "artiesten.html")], wens=True)]),
  stappen([("Intake", "Concept, line-up, aantal gasten en de ruimte. Hier bepalen we wat de avond nodig heeft."),
   ("Locatiebezoek of foto's en plattegrond", "We bekijken vooraf de ruimte: akoestiek, stroom, opbouwtijden en de buren."),
   ("Voorstel", "Een opzet voor geluid, licht en booth, met een duidelijke prijs."),
   ("Riders en planning", "We leggen de riders van je dj's naast de booth en stemmen opbouw en changeovers af."),
   ("Opbouw en soundcheck", "Een korte soundcheck, ook als de tijd krap is."),
   ("Op de avond zelf", "Eén aanspreekpunt voor licht, geluid en booth, tot de laatste plaat.")]),
  contact("Organiseer je een clubnacht, pop&#8209;up of eigen feest?", "Landingspagina dance-events", "Bijvoorbeeld: pop-up voor 400 gasten in een loods, eind maart"),
  eerder("Deze organisatoren gingen je voor", ["ade-dj.html", "prive-event.html", "/en/nieuws/raw-drums-ade.html"])])

P["merken-en-bureaus.html"] = dict(titel="Merken, creatieven en bureaus", h1="Merken, creatieven<br> en bureaus",
 beschrijving="Licht, geluid en muziek rond je merk, product of catwalk. Samen met de creatieven van het merk of het bureau. Music for brands en music for retail.",
 delen=[
  intro("Je merk, je product of je catwalk is het vertrekpunt. Daaromheen bedenken we samen de hele beleving.",
        ["We werken graag samen met de creatieven van het merk of het bureau. Jullie brengen het concept en de merkidentiteit, wij de vertaling naar licht, geluid en muziek.",
         "Zo wordt een productdemo, een etalage of een catwalk een moment dat past bij de rest van de campagne."]),
  momenten("Samen vormgeven", "De momenten die het verschil maken", ["De reveal van een product of collectie", "Een demo-area waar het product centraal staat",
   "De etalage of het in-store moment", "De catwalk", "Een fotogenieke plek of branded backdrop", "Een interviewhoek voor pers en content",
   "De omslag naar een feest, als de avond daarom vraagt"]),
  aanbod("Dit kunnen we je bieden", [
   kaart("Licht en beeld", [("Productlicht met theaterspots", "Kleuren, materialen en details van de collectie naar voren"),
     ("Licht voor camera en social", "Een backdrop en interviewhoek die ook op een telefoon kloppen"),
     ("Kleur in de ruimte", "Draadloze washlights in de campagnekleuren, zonder zichtbare bekabeling"),
     ("Projectie", "Je logo of collectie groot geprojecteerd")], meer=[("atmosfeerlicht", "atmospheric-lighting.html"), ("dansvloerlicht", "dancefloor-lighting.html")]),
   kaart("Muziek", [("Muziek die bij het merk past", "Afgestemd op de collectie, de campagne of het moment"),
     ("Een dj-set of playlists per moment", "Voor de ontvangst, de reveal en het feest"),
     ("Live muzikanten", "Saxofoon, percussie of vocals")], meer=[("dj's en artiesten", "artiesten.html")]),
   kaart("Concept en uitvoering", [("Meedenken vanaf de conceptfase", "Met het merk of het bureau, met 25 jaar ervaring in corporate communicatie"),
     ("Een lichtplan per moment", "Locatiebezoek, lichtontwerp en programmering"),
     ("Geluid en dj-booth", "Verstaanbare sprekers bij de presentatie, een volle dansvloer daarna")], wens=True)]),
  paar([("img/maarten-mixer.jpg", "Maarten Versteeg met een rotary mixer in een industriële ruimte", "50% 74%", "De sound van je merk", "Music for brands",
         "Een merk heeft een eigen sound. Bij producten en collecties brengt Maarten een chique sound met wortels in warme elektronische muziek: verfijnd genoeg voor een presentatie, met genoeg groove voor de avond erna. Afgestemd op de collectie of de campagne, als dj-set of als playlist per moment."),
        ("img/doelgroepen/winkel.jpg", "Eigenaresse van een kledingwinkel bij de toonbank, met kledingrekken op de achtergrond", "60% 40%", "Retail en conceptstores", "Music for retail",
         "Ook in de winkel hoort de muziek bij je merk. Bij een in-store event, een lancering of een koopzondag met een dj wordt je winkel voor een middag of avond een plek waar mensen voor komen, met licht en geluid die bij je collectie passen.")], kop="Daarnaast bieden we ook muzikale ondersteuning"),
  stappen([("Briefing", "Merk, campagne, doelgroep en de momenten van de avond. Hier bepalen we wat het event nodig heeft."),
   ("Locatiebezoek of foto's en plattegrond", "We bekijken de ruimte, de looproute en waar het product komt te staan."),
   ("Voorstel", "Licht en muziek per moment, met een duidelijke prijs."),
   ("Afstemming met het bureau", "Draaiboek, timing van de reveal, campagnekleuren en muziek."),
   ("Opbouw en programmering", "Licht ingesteld en geluid gecheckt voordat de eerste gast binnenkomt."),
   ("Op de avond zelf", "Eén aanspreekpunt, ook bij de omslag naar het feest.")]),
  contact("Werk je aan een lancering, collectie&shy;presentatie of in&#8209;store event?", "Landingspagina merken en bureaus", "Bijvoorbeeld: collectiepresentatie voor 150 gasten in een showroom, april"),
  eerder("Voorbeeldcase", ["productpresentatie.html"], quote="De uitstraling was precies zoals we wilden: clean, licht industrieel maar ook warm.")])

P["bijzondere-eventlocaties.html"] = dict(titel="Eigenaren en exploitanten van eventlocaties", h1="Eigenaren en exploitanten<br> van eventlocaties",
 beschrijving="Eén aanspreekpunt voor licht, geluid en muziek op je locatie: per klantvraag een passende opzet, en een vaste installatie voor wat je zelf doet.",
 delen=[
  intro("Vandaag een modeshow, morgen een seminar, overmorgen een bedrijfsfeest met dj. Elke klant vraagt om een andere opzet.",
        ["Wij vertalen de vraag van je klant naar een passende opzet in licht, geluid en muziek. In overleg met jou loopt het contact met de eindklant via jou of via ons, en we houden je steeds op de hoogte. Als je wilt, koppelen we daar een digitale planner aan."]),
  momenten("Je klanten", "De vragen die op je afkomen", ["Een seminar met sprekers en een presentatie", "Een modeshow of collectiepresentatie",
   "Een bedrijfsfeest met dj", "Een productlancering", "Een diner met muziek op de achtergrond", "Een clubnacht of pop-up", "Een bruiloft of privéfeest"],
   sub="Je moet van alle markten thuis zijn. HEAR en ons netwerk kunnen die vragen voor je oppakken."),
  aanbod("Dit kunnen we je bieden bij events", [
   kaart("Per event", [("Een opzet per klantvraag", "Licht, geluid en muziek, afgestemd op het type event"),
     ("Contact met de eindklant", "Via jou of via ons, in overleg, met een digitale planner als je wilt"),
     ("Dj's en artiesten", "Voor een feest of borrel op jouw locatie")], meer=[("geluid", "high-end-audio.html"), ("atmosfeerlicht", "atmospheric-lighting.html")]),
   kaart("Netwerk", [("Opschalen voor grotere events", "Met professionals uit ons netwerk"), ("Andere vakmensen", "We brengen je in contact met wie je nodig hebt")], wens=True)]),
  split("img/maarten-adviseur.jpg", "Maarten Versteeg", "50% 25%", "Hoe we samenwerken", "Eén aanspreekpunt",
        "We zijn je vaste aanspreekpunt voor licht, geluid en muziek. Waar nodig werken we met professionals uit ons netwerk, om op te schalen of om je in contact te brengen met wie je nodig hebt."),
  stappen([("Kennismaking op de locatie", "De ruimte, je klanten en de soorten events die je draait."),
   ("De ruimte in kaart", "Akoestiek, stroom, ophangpunten en opbouwtijden."),
   ("Afspraken", "Hoe we samenwerken: per event, met vaste opzetten of met een installatie."),
   ("Per klantvraag een voorstel", "Wij vertalen de vraag van je klant, jij houdt het overzicht."),
   ("Op de dag zelf", "Wij bouwen op en zijn het aanspreekpunt, voor jou en voor je klant."),
   ("Terugkijken", "Na het event kort evalueren, zodat het de volgende keer nog soepeler loopt.")]),
  '''<section class="lp-band lp-donker"><div class="lp-inst"><div><p class="lp-label">Vaste installatie</p><h2>Zelf doen waar het kan, expertise als het nodig is</h2>
<div class="lp-tekst"><p>Sommige dingen kun je zelf doen, bijvoorbeeld met een eigen PA of basislicht. Wij geven je onafhankelijk advies bij de aanschaf. En we zorgen dat we daarop kunnen aansluiten als er meer nodig is.</p></div>'''
  + lijst([("Merkonafhankelijk advies", "Met de eigenschappen van de ruimte als vertrekpunt"), ("Begeleiding bij aanschaf en installatie", "Ook bij de ingebruikname"),
           ("AV as a service", "Een vast bedrag per maand in plaats van een grote investering")])
  + '''<p class="lp-meer">Meer over <a href="aankoopadvies.html">aankoopadvies</a> <span aria-hidden="true">→</span></p></div>
<img src="img/systeem-breed.jpg" alt="Speakers van een vaste geluidsinstallatie" loading="lazy" style="object-position:30% 50%"></div></section>''',
  contact("Zoek je een (vaste) partner voor licht en geluid op je locatie?", "Landingspagina eventlocaties", "Bijvoorbeeld: eventlocatie voor 300 gasten, zo'n vier events per maand"),
  eerder("Eerder werk op locatie", ["ade-dj.html", "systeemadvies.html"])])

# ---------- sjabloon uit een bestaande pagina ----------
sjabloon = (site / "over-hear.html").read_text()
kop_html = sjabloon[:sjabloon.index("<main")]
voet_html = sjabloon[sjabloon.index("</main>") + len("</main>"):]
kop_html = re.sub(r'<!--og-->.*?<!--/og-->', '', kop_html, flags=re.S)
kop_html = re.sub(r'<link rel="alternate"[^>]*>', '', kop_html)
kop_html = kop_html.replace('aria-current="page"', '')

JS = """<script>(function(){
document.querySelectorAll('.lp-stappen').forEach(function(k){var S=[].map.call(k.querySelectorAll('.lp-stapjes li'),function(li){var b=li.querySelectorAll('b');return [b[1].textContent,li.querySelector('span').textContent]}),i=0,alle=false,t=k.querySelector('h3'),x=k.querySelector('h3+p'),L=k.querySelector('.lp-stapjes'),b=k.querySelector('.lp-stapbal');
function r(){t.textContent=S[i][0];x.textContent=S[i][1];t.hidden=x.hidden=alle;L.hidden=!alle;
b.innerHTML=S.map(function(s,n){return '<button type="button" class="lp-n" data-n="'+n+'"'+(n===i&&!alle?' aria-current="step"':'')+' aria-label="Stap '+(n+1)+': '+s[0]+'">'+(n+1)+'</button>'}).join('')+'<button type="button" class="lp-alle">'+(alle?'Toon per stap':'Bekijk alle stappen')+'</button>'+(alle?'':'<button type="button" class="lp-volg">'+(i<S.length-1?'Volgende':'Opnieuw')+'</button>');}
b.addEventListener('click',function(ev){var o=ev.target.closest('button');if(!o)return;if(o.dataset.n){i=+o.dataset.n;alle=false}else if(o.classList.contains('lp-alle')){alle=!alle}else{i=i<S.length-1?i+1:0}r();});r();});
document.querySelectorAll('.lp-form').forEach(function(f){var m=f.querySelector('.lp-melding');f.addEventListener('submit',function(ev){if(!window.fetch)return;ev.preventDefault();var k=f.querySelector('button');k.disabled=true;
fetch(f.action,{method:'POST',body:new FormData(f),headers:{'Accept':'application/json'}}).then(function(r){return r.json()}).then(function(r){m.hidden=false;
if(r.ok){m.textContent=f.dataset.dank;[].forEach.call(f.querySelectorAll('label,button,.lp-privacy'),function(x){x.hidden=true})}else{m.textContent=f.dataset.fout;k.disabled=false}}).catch(function(){m.hidden=false;m.textContent=f.dataset.fout;k.disabled=false});});});
})();</script>"""

def zijnav(i):
    v, n = DOEL[i - 1], DOEL[(i + 1) % len(DOEL)]
    bol = "".join(f'<a href="{d["bestand"]}" title="{d["kort"]}"' + (' class="aan" aria-current="page"' if k == i else '') + '></a>' for k, d in enumerate(DOEL))
    return (f'<nav class="zijnav" aria-label="Andere doelgroepen"><a class="pijl" href="{v["bestand"]}" title="{v["kort"]}" aria-label="Vorige: {v["kort"]}">←</a>'
            f'<span class="bollen">{bol}</span><a class="pijl" href="{n["bestand"]}" title="{n["kort"]}" aria-label="Volgende: {n["kort"]}">→</a></nav>')

for i, d in enumerate(DOEL):
    p = P[d["bestand"]]
    k = kop_html.replace('<link rel="stylesheet" href="styles.css">', '<link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="doelgroep.css">')
    k = re.sub(r'<title>.*?</title>', f'<title>{e(p["titel"])} · HEAR</title>', k)
    k = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(p["beschrijving"])}">', k)
    k = re.sub(r'<a class="taal" href="[^"]*"', f'<a class="taal" href="/en/{d["bestand"]}"', k)
    k = k.replace('<a href="doelgroepen.html">', '<a href="doelgroepen.html" aria-current="page">', 1)
    main = (f'<main class="wrap lp"><section class="casehead"><a class="crumb" href="doelgroepen.html"><span class="sectie">Met wie we werken</span>'
            f'<span class="scheiding" aria-hidden="true">|</span><span class="huidig">{d["kort"]}</span></a>{zijnav(i)}<h1 class="kernzin">{p["h1"]}</h1></section>'
            f'<div class="lp-held"><img src="{d["beeld"]}" alt="{e(d["alt"])}" style="object-position:{d["pos"]}"></div>'
            + "".join(p["delen"]) + '</main>')
    (site / d["bestand"]).write_text(k + main + JS + voet_html)
    print("ok", d["bestand"])

# ---------- overzichtspagina en homepage ----------
ov = site / "doelgroepen.html"; s = ov.read_text()
nieuw = (f'<main class="wrap"><section class="casehead"><a class="crumb" href="index.html"><span class="sectie">HEAR</span><span class="scheiding" aria-hidden="true">|</span>'
         f'<span class="huidig">Met wie we werken</span></a><h1 class="kernzin">Met wie we werken</h1></section>{samenblok()}</main>')
s = re.sub(r'<main.*?</main>', lambda m: nieuw, s, count=1, flags=re.S)
if 'doelgroep.css' not in s: s = s.replace('<link rel="stylesheet" href="styles.css">', '<link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="doelgroep.css">', 1)
s = re.sub(r'<title>.*?</title>', '<title>Met wie we werken · HEAR</title>', s, count=1)
s = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="HEAR werkt graag samen met eventmanagers en communicatieprofessionals, organisatoren van dance-events, merken en bureaus, en eigenaren van eventlocaties.">', s, count=1)
ov.write_text(s); print("ok doelgroepen.html")

ix = site / "index.html"; s = ix.read_text()
s, n = re.subn(r'<section class="(?:verder doelgroepen-blok|samen)".*?</section>', lambda m: samenblok(), s, count=1, flags=re.S)
if 'doelgroep.css' not in s: s = s.replace('<link rel="stylesheet" href="home.css">', '<link rel="stylesheet" href="home.css"><link rel="stylesheet" href="doelgroep.css">', 1)
ix.write_text(s); print("ok index.html", n)
