"""Bouwt site/aanvraag.html: het aanvraagformulier (besluit 28 okt 2026, na feedback van een eventcoördinator bij de overheid:
WhatsApp is op werkplekken vaak geblokkeerd; een formulier is laagdrempeliger).
Opbouw sinds 20 nov 2026 (snelle route naast het gesprek): 1/5 je event, 2/5 je programma (poortvragen: pas na aanvinken
verschijnen de keuzes die erbij horen), 3/5 budget en een vrij veld, 4/5 hoe verder (vrijblijvend voorstel of call) en contactgegevens,
5/5 controleer je aanvraag (het overzicht met per onderdeel 'Wijzig') en versturen.
Zonder JavaScript staan de stappen onder elkaar en zijn alle keuzes zichtbaar.
Het formulier post naar /api/aanvraag (src/index.js), dat de inzending mailt naar maarten@hear.nl. Geen opslag.
Schrijft ook de Engelse paren naar content/en.json (paginas → aanvraag.html). Draaien vóór bouw-en.py."""
import json, pathlib, html
root = pathlib.Path(__file__).resolve().parent.parent
site = root / "site"
idx = (site / "index.html").read_text()
kop = idx[idx.index('<header class="top">'):idx.index('</script>') + 9]
voet = idx[idx.index('<footer class="voet">'):idx.index('</footer>') + 9]
e = lambda t: html.escape(t, quote=True)

paren = [("<title>Aanvraag · HEAR</title>", "<title>Request · HEAR</title>"), ('<html lang="nl">', '<html lang="en">')]  # (nl, en) als tekst tussen tags; attributen apart
def T(nl, en):
    paren.append((f'>{e(nl)}<', f'>{e(en)}<')); return e(nl)
def A(nl, en):  # attribuutwaarde (placeholder, aria-label)
    paren.append((f'="{e(nl)}"', f'="{e(en)}"')); return e(nl)

TITEL = "Aanvraag"
KOP = "Vertel over je event"
MAIL = '<a href="mailto:maarten@hear.nl">maarten@hear.nl</a>'
TEL = '<a class="heel" href="tel:+31624560220">+31 6 24560220</a>'
WA = "https://wa.me/31624560220?text=Hoi%20Maarten%2C%20ik%20heb%20een%20vraag%20over%20HEAR%20voor%20mijn%20event."

def veld(naam, nl, en, type="text", verplicht=False, extra=""):
    req = " required" if verplicht else ""
    ster = '<b class="ster" aria-hidden="true"> *</b>' if verplicht else ""
    return f'<label class="veld"><span>{T(nl, en)}{ster}</span><input type="{type}" name="{naam}"{req}{extra}></label>'
def tekstvak(naam, nl, en, rijen=4, verplicht=False, breed=True):
    req = " required" if verplicht else ""
    return f'<label class="veld{" veld-breed" if breed else ""}"><span>{T(nl, en)}</span><textarea name="{naam}" rows="{rijen}"{req}></textarea></label>'

# Programma: per onderdeel een poortvraag; de keuzes eronder verschijnen pas als het onderdeel is aangevinkt.
# Samen dekken ze alles uit de catalogus (content/diensten.json) en de productkiezer op de homepage; aankoopadvies hoort hier niet (geen eventdienst).
WEBCAST = ("Online uitzending (webcast)", "Online broadcast (webcast)")
AFTERMOVIE = ("Aftermovie", "Aftermovie")
LOGO = ("Logoprojectie", "Logo projection")
SFEER = ("Sfeerverlichting", "Atmospheric lighting")
DECO = ("Decoratie: led-tubes, spiegelbollen en props", "Decoration: LED tubes, mirror balls and props")
GELUID = ("Geluidssysteem", "Sound system")
PLAYLIST = ("Maatwerk playlist, zonder live dj", "Bespoke playlist, without a live DJ")
DJ = ("Dj", "DJ")
BOOTH = ("Dj-booth en dj-gear", "DJ booth and DJ gear")
SCHERM = ("Videoschermen en presentatie", "Video screens and presentation")
PROGRAMMA = [
    ("sprekers", "Congres, seminar of speeches", "Conference, seminar or speeches", [
        ("Microfoons en geluid voor sprekers", "Microphones and sound for speakers"),
        SCHERM,
        ("Licht op de spreker", "Lighting on the speaker"),
        WEBCAST,
        ("Technicus ter plekke", "Technician on site"),
    ]),
    ("merk", "Productlancering, merkactivatie of modeshow", "Product launch, brand activation or fashion show", [
        GELUID, DJ, BOOTH,
        ("Muziek die past bij het merk (vooraf afgestemd)", "Music that fits the brand (agreed in advance)"),
        PLAYLIST,
        ("Licht in huisstijlkleuren", "Lighting in brand colours"),
        ("Licht op het product", "Lighting on the product"),
        LOGO, DECO, SCHERM,
    ]),
    ("borrel", "Netwerkborrel of diner met muziek", "Networking drinks or dinner with music", [
        GELUID, DJ, BOOTH, PLAYLIST, SFEER, DECO,
    ]),
    ("feest", "Feest met dansvloer", "Party with a dance floor", [
        GELUID, DJ, BOOTH,
        ("Lichtshow (o.a. moving heads)", "Light show (including moving heads)"),
        ("90's vintage licht", "90s vintage lighting"),
        SFEER, DECO,
    ]),
]
# 'exoten': los van het programma, altijd zichtbaar, als inspiratie
EXTRAS = [
    ("Ledschermen met VJ", "LED screens with a live VJ"),
    ("Vocalist, saxofonist of percussionist", "Vocalist, saxophonist or percussionist"),
    ("Geuren-dj", "Scent DJ"),
    ("Partyfotograaf", "Party photographer"),
    LOGO, AFTERMOVIE, WEBCAST,
]
COMMUNICATIE = [
    ("Meedenken over eventconcept", "Help shaping the event concept"),
    ("Communicatieadvies", "Communication advice"),
    ("Uitnodigingen en andere communicatiemiddelen", "Invitations and other communication materials"),
    ("Speeches en presentaties schrijven", "Writing speeches and presentations"),
    ("Bedrijfsvideo", "Corporate video"),
    AFTERMOVIE,
]
def poort(sleutel, nl, en, opties):
    return (f'<fieldset class="poort"><legend class="sr">{T(nl, en)}</legend>'
            f'<label class="vink poortvraag"><input type="checkbox" name="programma" value="{e(nl)}" data-poort="{sleutel}"><span>{T(nl, en)}</span></label>'
            f'<div class="poort-opties" id="poort-{sleutel}">{opties}</div></fieldset>')
def programma():
    # keuzes die op meer dan één plek staan (sfeerlicht, decoratie, aftermovie, webcast) lopen gelijk en tonen op de andere plek 'reeds gekozen'
    telling = {}
    for groep in [items for _, _, _, items in PROGRAMMA] + [COMMUNICATIE, EXTRAS]:
        for inl, _ in groep: telling[inl] = telling.get(inl, 0) + 1
    reeds = f'<em class="reeds-tag">{T("reeds gekozen", "already chosen")}</em>'
    # dj, booth en playlist gelden per programmadeel (dj op het feest, playlist bij de borrel kan) en lopen dus niet gelijk;
    # binnen één deel sluiten dj en playlist elkaar uit
    per_deel = {DJ[0]: "dj", BOOTH[0]: "booth", PLAYLIST[0]: "playlist"}
    def vink(naam, inl, ien):
        g = telling.get(inl, 0) > 1 and inl not in per_deel
        if per_deel.get(inl):
            return f'<label class="vink"><input type="checkbox" name="{naam}" value="{e(inl)}" data-of="{per_deel[inl]}"><span>{T(inl, ien)}{reeds}</span></label>'
        return f'<label class="vink"><input type="checkbox" name="{naam}" value="{e(inl)}"{" data-gedeeld" if g else ""}><span>{T(inl, ien)}{reeds if g else ""}</span></label>'
    comm_namen = {nl for nl, _ in COMMUNICATIE}
    blokken = ""
    for sleutel, nl, en, items in PROGRAMMA:
        opties = "".join(vink("diensten", inl, ien) for inl, ien in items)
        opties += f'<label class="veld veld-breed"><span>{T("Anders, namelijk", "Other, namely")}</span><input type="text" name="diensten_anders"></label>'
        blokken += poort(sleutel, nl, en, opties)
    comm = ("".join(vink("communicatie", nl, en) for nl, en in COMMUNICATIE)
            + f'<label class="veld veld-breed"><span>{T("Anders, namelijk", "Other, namely")}</span><input type="text" name="communicatie_anders"></label>')
    communicatie = poort("communicatie", "Hulp bij de communicatie rondom je event", "Help with the communication around your event", comm)
    extras = (f'<details class="extras"><summary><span>{T("Inspiratie: heb je hier al eens aan gedacht?", "Inspiration: have you thought about this?")}</span></summary><div class="extras-opties">'
              + "".join(vink("communicatie" if nl in comm_namen else "diensten", nl, en) for nl, en in EXTRAS) + '</div></details>')
    weetniet = (f'<label class="vink poortvraag poort-los"><input type="checkbox" name="programma" id="weetniet" value="Weet nog niet wat nodig is, bespreekt dit graag in een call">'
                f'<span>{T("Ik weet nog niet wat ik nodig heb en bespreek dit graag in een call", "I don\'t know what I need yet and would like to discuss it in a call")}</span></label>')
    return (f'<div class="programma">{blokken}</div>{extras}<div class="programma na-extras">{communicatie}</div>'
            f'<label class="veld veld-breed"><span>{T("Iets anders nodig? Namelijk", "Need something else? Namely")}</span><input type="text" name="diensten_anders" id="anders-los"></label>'
            f'<div class="weetniet-rij">{weetniet}</div>')

# relatieve schaal (Maarten, 21 nov): tot 2.000 per 250, tot 5.000 per 500, daarna grotere stappen; de hoogste stand is '20.000+'
BUDGETSTAPPEN = [1000, 1250, 1500, 1750, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 6000, 7500, 10000, 12500, 15000, 20000]
budget = (f'<fieldset class="budget"><legend>{T("Richtbudget voor licht, geluid en muziek", "Indicative budget for light, sound and music")}</legend>'
          f'<p class="uitleg">{T("Schuif naar je richtbudget. Dan zoeken we de meeste beleving binnen die kaders.", "Slide to your indicative budget. We will then look for the most impact within those limits.")}</p>'
          f'<div class="slider leeg" id="budget" data-leeg="{A("Nog niet ingevuld", "Not filled in yet")}"><input type="hidden" name="budget_ingevuld" value=""><input type="hidden" name="budget_van" value=""><input type="hidden" name="budget_tot" value=""><input type="range" min="0" max="{len(BUDGETSTAPPEN) - 1}" step="1" value="{BUDGETSTAPPEN.index(2500)}" aria-label="{A("Van", "From")}">'
          f'<input type="range" min="0" max="{len(BUDGETSTAPPEN) - 1}" step="1" value="{BUDGETSTAPPEN.index(7500)}" aria-label="{A("Tot", "To")}"><output id="budget_uit"></output></div>'
          f'<label class="vink"><input type="checkbox" name="budget_onbekend" value="ja"><span>{T("Weet ik nog niet", "I don\'t know yet")}</span></label></fieldset>')

GESPREK = [("bellen", "Telefonisch", "By phone"), ("teams", "Microsoft Teams", "Microsoft Teams"), ("meet", "Google Meet", "Google Meet")]
DAGDEEL = [("ochtend", "Ochtend", "Morning"), ("middag", "Middag", "Afternoon"), ("eind van de middag", "Eind van de middag", "Late afternoon")]
gesprek = (f'<div class="velden callvelden" id="callvelden"><fieldset class="keuze veld-breed"><legend>{T("Hoe wil je de call doen?", "How would you like to have the call?")}</legend><div class="keuzerij">'
           + "".join(f'<label class="vink"><input type="radio" name="gesprek" value="{w}"{" checked" if w == "bellen" else ""}><span>{T(nl, en)}</span></label>' for w, nl, en in GESPREK)
           + '</div></fieldset>'
           + veld("gesprek_datum", "Wanneer schikt het?", "When suits you?", "date", False, ' id="gesprek-datum"')
           + f'<label class="veld"><span>{T("Dagdeel", "Time of day")}</span><select name="gesprek_dagdeel"><option value="">{T("Maakt niet uit", "No preference")}</option>'
           + "".join(f'<option value="{w}">{T(nl, en)}</option>' for w, nl, en in DAGDEEL) + '</select></label></div>')
route = (f'<fieldset class="route"><legend class="sr">{T("Hoe verder?", "What next?")}</legend><div class="routekaarten">'
         f'<label class="routekaart"><input type="radio" name="route" value="voorstel" required><strong>{T("Stuur me een vrijblijvend voorstel", "Send me a no-obligation proposal")}</strong><span>{T("Je hoort meestal binnen 1 werkdag van ons", "You will usually hear from us within 1 working day")}</span></label>'
         f'<label class="routekaart"><input type="radio" name="route" value="call"><strong>{T("Plan een call", "Schedule a call")}</strong><span>{T("Telefoon, Teams of Meet", "Phone, Teams or Meet")}</span></label>'
         f'</div></fieldset>'
         f'<p class="formmelding fout" id="mist" hidden><span id="mist-tekst"></span> <button type="button" class="stapknop terug" id="mist-knop" data-naar="1">{T("Vul aan", "Complete it")}</button></p>')

def stap(n, kop_nl, kop_en, inhoud, laatste=False, terug=None, verder=None):
    vorige = f'<button type="button" class="stapknop terug" data-naar="{terug or n-1}">{T("← Vorige", "← Back")}</button>' if n > 1 else ''
    volgende = (f'<button type="submit" class="wa knop">{T("Verstuur je aanvraag", "Send your request")}<i aria-hidden="true">→</i></button>'
                if laatste else f'<button type="button" class="wa knop stapknop vooruit" data-naar="{verder or n+1}">{T("Volgende", "Next")}<i aria-hidden="true">→</i></button>')
    return (f'<section class="stap" data-stap="{n}"><p class="stapteller">{n}/5</p><h2>{T(kop_nl, kop_en)}</h2>{inhoud}'
            f'<p class="formvoet">{volgende}{vorige}</p></section>')

stap1 = stap(1, "Je event", "Your event", inhoud=f"""<p class="stapuitleg">{T("Vul in wat je al weet. Voor een voorstel hebben we de datum, de locatie en het aantal gasten nodig.", "Fill in what you already know. For a proposal we need the date, the venue and the number of guests.")}</p><div class="velden">
{veld("datum", "Datum van het event", "Date of the event", "date", extra=' id="v-datum"')}
{veld("tijd", "Tijd, van tot", "Time, from to", extra=' placeholder="16:00 – 23:00"')}
{veld("locatie", "Locatie", "Venue", extra=' id="v-locatie"')}
{veld("gasten", "Aantal gasten", "Number of guests", "number", extra=' min="1" inputmode="numeric" id="v-gasten"')}
</div>""")
stap2 = stap(2, "Je programma", "Your programme", f"""<p class="stapuitleg">{T("Vink aan wat er op het programma staat. Dan zie je wat we kunnen verzorgen.", "Tick what is on the programme. You will then see what we can take care of.")}</p>
{programma()}""")
stap3 = stap(3, "Budget en toelichting", "Budget and details", f"""{budget}
<label class="veld veld-breed"><span>{T("Wil je iets toelichten?", "Anything you would like to add?")}</span><small class="veldhulp">{T("Bijvoorbeeld de doelgroep, het concept, de gewenste beleving of de ruimte. Dit veld is niet verplicht.", "For example the audience, the concept, the experience you are after or the room. This field is optional.")}</small><textarea name="bericht" rows="5"></textarea></label>""")
stap4 = stap(4, "Hoe verder?", "What next?", f"""{route}
{gesprek}
<p class="stapuitleg tussenkop">{T("Velden met * zijn nodig om contact op te nemen.", "Fields marked * are needed to get in touch.")}</p><div class="velden">
{veld("naam", "Naam", "Name", verplicht=True, extra=' autocomplete="name"')}
{veld("organisatie", "Organisatie", "Organisation", extra=' autocomplete="organization"')}
{veld("email", "E-mail", "Email", "email", True, ' autocomplete="email"')}
{veld("telefoon", "Telefoonnummer", "Phone number", "tel", True, ' autocomplete="tel" id="telefoon"')}
</div>""")
stap5 = stap(5, "Controleer je aanvraag", "Check your request", f"""<p class="stapuitleg">{T("Klopt alles? Dan kun je versturen.", "All correct? Then you can send it.")}</p>
<div id="controle"></div><input type="hidden" name="overzicht" value="">
<p class="uitleg privacyregel"><span>{T("We gebruiken je gegevens alleen om je aanvraag te beantwoorden.", "We only use your details to answer your request.")}</span> <a href="privacy.html">Privacyverklaring</a></p>""", laatste=True)

def dankblok(sleutel, nl, en):
    return (f'<div class="dank" id="dank-{sleutel}" hidden><h2>{T("Bedankt voor je aanvraag!", "Thank you for your request!")}</h2><p>{T(nl, en)}</p>'
            f'<h3>{T("Heb je foto\'s van de ruimte?", "Do you have photos of the room?")}</h3><p><span>{T("Mail ze naar", "Email them to")}</span> {MAIL}</p></div>')
dank = (dankblok("voorstel", "We gaan ermee aan de slag. Je hoort meestal binnen 1 werkdag van ons.", "We are on it. You will usually hear from us within 1 working day.")
        + dankblok("call", "We nemen contact met je op om de call in te plannen, meestal binnen 1 werkdag.", "We will get in touch to schedule the call, usually within 1 working day."))

form = f"""<form class="aanvraag" method="post" action="/api/aanvraag" id="aanvraag">
<input type="text" name="website" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
{stap1}
{stap2}
{stap3}
{stap4}
{stap5}
<p class="formmelding" id="melding" hidden></p>
<div class="kortevraag" id="kortevraag"><span>{T("Korte vraag?", "Quick question?")}</span><a class="kv-knop" href="{WA}">WhatsApp</a><a class="kv-knop" href="mailto:maarten@hear.nl">{T("Mail", "Email")}</a></div>
{dank}
</form>"""

main = f"""<main class="wrap">
<section class="casehead"><a class="crumb" href="index.html"><span class="sectie">HEAR</span></a><h1 class="kernzin">{e(KOP)}</h1></section>
<div class="aanvraag-kolommen">
{form}
<aside class="samenvatting" id="samenvatting" aria-live="polite" data-leeg="{A("Nog niets gekozen.", "Nothing chosen yet.")}" data-gasten="{A(" gasten", " guests")}" data-budget="{A("Richtbudget", "Indicative budget")}" data-onbekend="{A("Weet ik nog niet", "I don\'t know yet")}" data-event="{A("Je event", "Your event")}" data-programma="{A("Je programma", "Your programme")}" data-anders="{A("Iets anders nodig", "Something else")}" data-toelichting="{A("Toelichting", "Details")}" data-verder="{A("Hoe verder", "What next")}" data-gegevens="{A("Je gegevens", "Your details")}" data-wijzig="{A("Wijzig", "Change")}"><h2 id="sv-kop" data-voorstel="{A("Ik ontvang graag een vrijblijvend voorstel voor", "I would like a no-obligation proposal for")}" data-call="{A("Ik bespreek graag in een call", "I would like to discuss in a call")}">{T("Ik ontvang graag een vrijblijvend voorstel voor", "I would like a no-obligation proposal for")}</h2><div id="sv-inhoud"></div></aside>
</div>
</main>
<script>
(function(){{
  var f=document.getElementById('aanvraag'),m=document.getElementById('melding');
  /* budget: zolang de schuif niet is aangeraakt, telt hij niet als antwoord */
  var s=document.getElementById('budget'),a=s.querySelectorAll('input[type=range]'),o=document.getElementById('budget_uit'),bi=f.querySelector('[name=budget_ingevuld]'),bo=f.querySelector('[name=budget_onbekend]'),budgetAan=false;
  function eur(n){{return '€ '+Number(n).toLocaleString('nl-NL')}}
  var BS=[1000,1250,1500,1750,2000,2500,3000,3500,4000,4500,5000,6000,7500,10000,12500,15000,20000],hv=f.querySelector('[name=budget_van]'),ht=f.querySelector('[name=budget_tot]');
  function toon(){{var i=+a[0].value,j=+a[1].value;if(i>j){{if(this===a[0])a[1].value=i;else a[0].value=j;i=+a[0].value;j=+a[1].value}}var v=BS[i],t=BS[j];hv.value=v;ht.value=t;
    s.classList.toggle('leeg',!budgetAan||bo.checked);bi.value=budgetAan?'ja':'';o.textContent=budgetAan&&!bo.checked?eur(v)+' – '+eur(t)+(j===BS.length-1?'+':''):(bo.checked?'':s.dataset.leeg)}}
  function raak(){{budgetAan=true;bo.checked=false;toon.call(this)}}
  [].forEach.call(a,function(x){{x.addEventListener('input',raak);x.addEventListener('pointerdown',raak);x.addEventListener('keydown',raak)}});bo.addEventListener('change',function(){{toon()}});toon();
  /* poortvragen: keuzes tonen als het onderdeel is aangevinkt; verborgen keuzes gaan niet mee */
  function poorten(){{[].forEach.call(f.querySelectorAll('[data-poort]'),function(p){{var b=document.getElementById('poort-'+p.dataset.poort);b.hidden=!p.checked;[].forEach.call(b.querySelectorAll('input'),function(i){{i.disabled=!p.checked}})}})}}
  [].forEach.call(f.querySelectorAll('[data-poort]'),function(p){{p.addEventListener('change',function(){{poorten();gedeeld();samenvat()}})}});poorten();
  /* gedeelde keuzes (bij meer dan één onderdeel) lopen gelijk; bij het andere onderdeel staat 'reeds gekozen' */
  var eigenaar={{}};
  function gedeeld(){{[].forEach.call(f.querySelectorAll('[data-gedeeld]'),function(i){{var e=eigenaar[i.value];i.closest('label').classList.toggle('reeds',i.checked&&!!e&&e!==i&&!e.disabled&&e.checked)}})}}
  [].forEach.call(f.querySelectorAll('[data-gedeeld]'),function(i){{i.addEventListener('change',function(){{if(i.checked)eigenaar[i.value]=i;else delete eigenaar[i.value];
    [].forEach.call(f.querySelectorAll('[data-gedeeld]'),function(x){{if(x!==i&&x.value===i.value)x.checked=i.checked}});gedeeld()}})}});
  /* dj, booth en playlist: binnen één programmadeel kan dj óf playlist; een keuze loopt mee naar de andere delen ('reeds gekozen'),
     behalve naar een deel waar al het andere is gekozen. Tussen delen zetten ze elkaar niet uit. */
  var OF=[].slice.call(f.querySelectorAll('[data-of]'));
  function tegen(k){{return k==='dj'?'playlist':k==='playlist'?'dj':''}}
  function heeft(blok,k){{return !!k&&[].some.call(blok.querySelectorAll('[data-of="'+k+'"]'),function(x){{return x.checked}})}}
  function ofTags(){{OF.forEach(function(x){{x.closest('label').classList.toggle('reeds',x.checked&&x.dataset.auto==='1')}})}}
  OF.forEach(function(i){{i.addEventListener('change',function(){{var k=i.dataset.of,blok=i.closest('.poort-opties'),wasAuto=i.dataset.auto==='1';i.dataset.auto='';
    if(i.checked){{
      [].forEach.call(blok.querySelectorAll('[data-of]'),function(x){{if(x===i)return;if(x.dataset.of===tegen(k)||(k==='playlist'&&x.dataset.of==='booth'&&x.dataset.auto==='1')){{var eigen=x.checked&&x.dataset.auto!=='1';x.checked=false;x.dataset.auto='';if(eigen)OF.forEach(function(y){{if(y!==x&&y.value===x.value&&y.dataset.auto==='1'){{y.checked=false;y.dataset.auto=''}}}})}}}});
      OF.forEach(function(x){{if(x===i||x.value!==i.value||x.checked)return;var b2=x.closest('.poort-opties');if(heeft(b2,tegen(k))||(k==='booth'&&heeft(b2,'playlist')))return;x.checked=true;x.dataset.auto='1'}});
    }}else if(!wasAuto){{OF.forEach(function(x){{if(x!==i&&x.value===i.value&&x.dataset.auto==='1'){{x.checked=false;x.dataset.auto=''}}}})}}
    ofTags()}})}});
  /* samenvatting rechts: wat er tot nu toe is ingevuld */
  var sv=document.getElementById('samenvatting'),svi=document.getElementById('sv-inhoud');
  function esc(t){{var d=document.createElement('div');d.textContent=t;return d.innerHTML}}
  var EN=location.pathname.indexOf('/en/')===0,ct=document.getElementById('controle');
  function tekst(i){{return i.closest('label').querySelector('span').firstChild.textContent}}
  function waarde(n){{var x=f.querySelector('[name='+n+']');return x&&!x.disabled?x.value.trim():''}}
  /* alles wat is ingevuld, als secties: {{k: kop, s: stap, items, kaal: zonder kop in het vlak rechts, c: alleen in de controlestap}} */
  function verzamel(){{var S=[],L=sv.dataset,ev=[];
    var dv=waarde('datum');if(dv)ev.push(new Date(dv+'T12:00:00').toLocaleDateString(EN?'en-GB':'nl-NL',{{day:'numeric',month:'long',year:'numeric'}}));
    var tv=waarde('tijd');if(tv)ev.push(tv);var lv=waarde('locatie');if(lv)ev.push(lv);var gv=waarde('gasten');if(gv)ev.push(gv+L.gasten);
    if(ev.length)S.push({{k:L.event,s:1,items:ev,kaal:true,event:true}});
    function deel(p){{var q=p.querySelector('[data-poort]');if(!q.checked)return;var it=[];[].forEach.call(p.querySelectorAll('.poort-opties input[type=checkbox]:checked'),function(i){{if(!i.closest('label').classList.contains('reeds'))it.push(tekst(i))}});
      var an=p.querySelector('.poort-opties input[type=text]');if(an&&an.value.trim())it.push(an.value.trim());S.push({{k:tekst(q),s:2,items:it}})}}
    [].forEach.call(f.querySelectorAll('.programma:not(.na-extras) .poort'),deel);
    var ex=[];[].forEach.call(f.querySelectorAll('.extras input:checked'),function(i){{if(!i.closest('label').classList.contains('reeds'))ex.push(tekst(i))}});
    if(ex.length)S.push({{k:f.querySelector('.extras summary').textContent,s:2,items:ex}});
    [].forEach.call(f.querySelectorAll('.programma.na-extras .poort'),deel);
    var da=document.getElementById('anders-los').value.trim();if(da)S.push({{k:L.anders,s:2,items:[da]}});
    if(document.getElementById('weetniet').checked)S.push({{k:L.programma,s:2,items:[tekst(document.getElementById('weetniet'))],kaal:true}});
    if(bo.checked)S.push({{k:L.budget,s:3,items:[L.onbekend]}});else if(budgetAan)S.push({{k:L.budget,s:3,items:[o.textContent]}});
    var be=waarde('bericht');if(be)S.push({{k:L.toelichting,s:3,items:[be],c:true}});
    var rk=f.querySelector('[name=route]:checked');if(rk){{var ri=[rk.closest('label').querySelector('strong').textContent];
      if(rk.value==='call'){{var gk=f.querySelector('[name=gesprek]:checked'),cd=[];if(gk)cd.push(tekst(gk));var gdv=waarde('gesprek_datum');if(gdv)cd.push(new Date(gdv+'T12:00:00').toLocaleDateString(EN?'en-GB':'nl-NL',{{day:'numeric',month:'long'}}));
        var dl=f.querySelector('[name=gesprek_dagdeel]');if(dl&&dl.value)cd.push(dl.options[dl.selectedIndex].text.toLowerCase());if(cd.length)ri.push(cd.join(', '))}}
      S.push({{k:L.verder,s:4,items:ri,route:true}})}}
    var pg=['naam','organisatie','email','telefoon'].map(waarde).filter(Boolean);if(pg.length)S.push({{k:L.gegevens,s:4,items:pg,c:true}});
    return S}}
  function lijst(it){{return it.length?'<ul>'+it.map(function(x){{return '<li>'+esc(x)+'</li>'}}).join('')+'</ul>':''}}
  function samenvat(){{var S=verzamel().filter(function(x){{return !x.c&&!x.route}}),h='',sk=document.getElementById('sv-kop'),rr=f.querySelector('[name=route]:checked');sk.textContent=rr&&rr.value==='call'?sk.dataset.call:sk.dataset.voorstel;
    S.forEach(function(x){{if(x.event)h+='<ul class="sv-event">'+x.items.map(function(y){{return '<li>'+esc(y)+'</li>'}}).join('')+'</ul>';else if(x.kaal)h+=x.items.map(function(y){{return '<p class="sv-regel">'+esc(y)+'</p>'}}).join('');else h+='<h3>'+esc(x.k)+'</h3>'+lijst(x.items)}});
    sv.classList.toggle('leeg',!h);svi.innerHTML=h||'<p class="sv-leeg">'+esc(sv.dataset.leeg)+'</p>'}}
  /* controlestap: hetzelfde overzicht, volledig, met per onderdeel een knop om te wijzigen */
  function controle(){{ct.innerHTML=verzamel().map(function(x){{return '<div class="ct-deel"><div class="ct-kop"><h3>'+esc(x.k)+'</h3><button type="button" class="ct-wijzig" data-naar="'+x.s+'">'+esc(sv.dataset.wijzig)+'</button></div>'+lijst(x.items)+'</div>'}}).join('')}}
  /* voor de mail: de keuzes per programmadeel, in het Nederlands (de waarden van de vinkjes), zodat zichtbaar blijft bij welk deel iets is gekozen */
  function voorMail(){{var D=[];function deel(p){{var q=p.querySelector('[data-poort]');if(!q.checked)return;var it=[].map.call(p.querySelectorAll('.poort-opties input[type=checkbox]:checked'),function(i){{return i.value}});
      var an=p.querySelector('.poort-opties input[type=text]');if(an&&an.value.trim())it.push('Anders: '+an.value.trim());D.push({{kop:q.value,items:it}})}}
    [].forEach.call(f.querySelectorAll('.programma:not(.na-extras) .poort'),deel);
    var ex=[].map.call(f.querySelectorAll('.extras input:checked'),function(i){{return i.value}});if(ex.length)D.push({{kop:'Inspiratie',items:ex}});
    [].forEach.call(f.querySelectorAll('.programma.na-extras .poort'),deel);
    var da=document.getElementById('anders-los').value.trim();if(da)D.push({{kop:'Iets anders nodig',items:[da]}});
    if(document.getElementById('weetniet').checked)D.push({{kop:'Weet nog niet wat nodig is',items:['Bespreekt dit graag in een call']}});
    f.querySelector('[name=overzicht]').value=JSON.stringify(D)}}
  f.addEventListener('input',samenvat);f.addEventListener('pointerdown',function(){{setTimeout(samenvat,0)}});f.addEventListener('change',samenvat);samenvat();
  /* route: bij een call de velden voor het contactmoment tonen */
  var cv=document.getElementById('callvelden'),gd=document.getElementById('gesprek-datum'),mist=document.getElementById('mist'),mt=document.getElementById('mist-tekst');
  function gekozen(){{var r=f.querySelector('[name=route]:checked');return r?r.value:''}}
  function route(){{var c=gekozen()==='call';cv.hidden=!c;gd.required=c;[].forEach.call(cv.querySelectorAll('input,select'),function(i){{i.disabled=!c}});mist.hidden=true;
    [].forEach.call(f.querySelectorAll('.routekaart'),function(k){{k.classList.toggle('aan',k.querySelector('input').checked)}})}}
  [].forEach.call(f.querySelectorAll('[name=route]'),function(r){{r.addEventListener('change',route)}});route();
  /* 'ik weet het nog niet': zet de call alvast als keuze klaar */
  var wn=document.getElementById('weetniet');wn.addEventListener('change',function(){{if(wn.checked){{f.querySelector('[name=route][value=call]').checked=true;route();samenvat()}}}});
  /* voor een voorstel is genoeg invoer nodig */
  function ontbreekt(){{var L=f.dataset,u=[];if(!document.getElementById('v-datum').value)u.push(L.mDatum);if(!document.getElementById('v-locatie').value.trim())u.push(L.mLocatie);if(!document.getElementById('v-gasten').value)u.push(L.mGasten);
    var stap=u.length?'1':'';if(!f.querySelector('[name=diensten]:checked:not(:disabled),[name=communicatie]:checked:not(:disabled)')&&![].some.call(f.querySelectorAll('[name=diensten_anders]'),function(i){{return !i.disabled&&i.value.trim()}})){{u.push(L.mKeuze);stap=stap||'2'}}if(!budgetAan&&!bo.checked){{u.push(L.mBudget);stap=stap||'3'}}return {{lijst:u,stap:stap}}}}
  var st=f.querySelectorAll('.stap');f.classList.add('in-stappen');
  function ga(n,geschiedenis){{n=String(n);if(geschiedenis!==false&&history.pushState){{var st0=history.state&&history.state.stap;if(st0!==n)history.pushState({{stap:n}},'','#stap-'+n)}}var doel;st.forEach(function(x){{var aan=x.dataset.stap===n;x.hidden=!aan;if(aan)doel=x}});sv.hidden=n==='5';if(n==='5')controle();document.getElementById('kortevraag').hidden=n!=='1';var h=doel.querySelector('h2');window.scrollTo({{top:f.getBoundingClientRect().top+window.scrollY-120,behavior:'smooth'}});h&&h.focus&&h.setAttribute('tabindex','-1');h&&h.focus({{preventScroll:true}})}}
  f.querySelectorAll('.stapknop').forEach(function(k){{k.addEventListener('click',function(){{var n=k.dataset.naar,huidig=k.closest('.stap');if(!n)return;
    if(k.classList.contains('vooruit')){{var ok=true;huidig.querySelectorAll('input,select,textarea').forEach(function(i){{if(ok&&!i.checkValidity()){{i.reportValidity();ok=false}}}});if(!ok)return;
      if(huidig.dataset.stap==='4'&&gekozen()==='voorstel'){{var o=ontbreekt();if(o.lijst.length){{mt.textContent=f.dataset.mKop+' '+o.lijst.join(', ')+'.';document.getElementById('mist-knop').dataset.naar=o.stap;mist.hidden=false;return}}}}}}ga(n)}})}});
  ct.addEventListener('click',function(ev){{var k=ev.target.closest&&ev.target.closest('.ct-wijzig');if(k)ga(k.dataset.naar)}});
  if(gd){{var nu=new Date();gd.min=nu.getFullYear()+'-'+String(nu.getMonth()+1).padStart(2,'0')+'-'+String(nu.getDate()).padStart(2,'0')}}
  function bedankt(r){{st.forEach(function(x){{x.hidden=true}});m.hidden=true;sv.hidden=true;document.getElementById('kortevraag').hidden=true;var d=document.getElementById(r==='call'?'dank-call':'dank-voorstel');d.hidden=false;window.scrollTo({{top:f.getBoundingClientRect().top+window.scrollY-120,behavior:'smooth'}})}}
  var q=location.search;
  if(/verzonden=1/.test(q)){{bedankt(/route=call/.test(q)?'call':'voorstel')}}
  else{{if(history.replaceState)history.replaceState({{stap:'1'}},'',location.pathname+location.search);ga(1,false);if(/fout=1/.test(q)){{m.hidden=false;m.textContent=f.dataset.fout;m.className='formmelding fout'}}}}
  window.addEventListener('popstate',function(ev){{var n=(ev.state&&ev.state.stap)||'1';if(f.querySelector('.stap[data-stap="'+n+'"]')&&document.getElementById('dank-voorstel').hidden&&document.getElementById('dank-call').hidden)ga(n,false)}});
  f.addEventListener('submit',function(ev){{
    var r=gekozen();
    if(r==='voorstel'){{var o=ontbreekt();if(o.lijst.length){{ev.preventDefault();mt.textContent=f.dataset.mKop+' '+o.lijst.join(', ')+'.';document.getElementById('mist-knop').dataset.naar=o.stap;mist.hidden=false;ga(4);return}}}}
    voorMail();
    if(!window.fetch)return;ev.preventDefault();var b={{set disabled(v){{[].forEach.call(f.querySelectorAll('button[type=submit]'),function(x){{x.disabled=v}})}}}};b.disabled=true;
    fetch(f.action,{{method:'POST',body:new FormData(f),headers:{{'Accept':'application/json'}}}}).then(function(x){{return x.json()}}).then(function(x){{
      if(x.ok){{f.reset();budgetAan=false;toon();poorten();OF.forEach(function(x){{x.dataset.auto=''}});bedankt(r)}}else{{m.hidden=false;m.textContent=f.dataset.fout;m.className='formmelding fout';b.disabled=false}}
    }}).catch(function(){{m.hidden=false;m.textContent=f.dataset.fout;m.className='formmelding fout';b.disabled=false}});
  }});
}})();
</script>"""
main = main.replace('<form class="aanvraag"', '<form class="aanvraag"'
    + f' data-fout="{A("Versturen lukte niet. Mail ons op maarten@hear.nl of bel +31 6 24560220.", "Sending failed. Email us at maarten@hear.nl or call +31 6 24560220.")}"'
    + f' data-m-kop="{A("Voor een voorstel hebben we nog nodig:", "For a proposal we still need:")}"'
    + f' data-m-datum="{A("de datum", "the date")}" data-m-locatie="{A("de locatie", "the venue")}" data-m-gasten="{A("het aantal gasten", "the number of guests")}"'
    + f' data-m-budget="{A("je richtbudget (of vink aan dat je het nog niet weet)", "your indicative budget (or tick that you don\'t know yet)")}"'
    + f' data-m-keuze="{A("minstens één keuze bij je programma", "at least one choice in your programme")}"')

BESCHRIJVING = "Vraag licht, geluid, dj of advies aan voor je event. Kies zelf: een vrijblijvend voorstel of een call."
doc = f'''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{A(BESCHRIJVING, "Request light, sound, a DJ or advice for your event. You choose: a no-obligation proposal or a call.")}"><title>{TITEL} · HEAR</title><link rel="stylesheet" href="home.css"><link rel="stylesheet" href="styles.css"></head><body class="pagina">
{kop}
{main}
{voet}
</body></html>'''
(site / "aanvraag.html").write_text(doc)

# Engelse paren
en_pad = root / "content" / "en.json"
en = json.loads(en_pad.read_text())
gezien, uniek = set(), []
for nl, eng in paren:
    if nl not in gezien: gezien.add(nl); uniek.append([nl, eng])
en["paginas"]["aanvraag.html"] = uniek
if "aanvraag.html" not in en["vertaald"]: en["vertaald"].append("aanvraag.html")
en_pad.write_text(json.dumps(en, ensure_ascii=False, indent=2))
print(f"ok aanvraag.html ({len(uniek)} paren)")
