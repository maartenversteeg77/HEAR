"""Bouwt site/aanvraag.html: het aanvraagformulier (besluit 28 okt 2026, na feedback van een eventcoördinator bij de overheid:
WhatsApp is op werkplekken vaak geblokkeerd; een formulier is laagdrempeliger).
Opbouw sinds 20 nov 2026 (snelle route naast het gesprek): 1/4 je event, 2/4 je programma (poortvragen: pas na aanvinken
verschijnen de keuzes die erbij horen), 3/4 budget en een vrij veld, 4/4 hoe verder (vrijblijvend voorstel of call) en contactgegevens.
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
TEL = '<a href="tel:+31624560220">+31 6 24560220</a>'
INTRO_HTML = "Vertel in een paar stappen wat je nodig hebt. Daarna kies je: een vrijblijvend voorstel of een call. Liever meteen bellen of appen? " + TEL + ". Mailen kan ook: " + MAIL + "."
paren.append((INTRO_HTML, "Tell us what you need in a few steps. Then choose: a no-obligation proposal or a call. Rather call or message straight away? " + TEL + ". Email works too: " + MAIL + "."))

def veld(naam, nl, en, type="text", verplicht=False, extra=""):
    req = " required" if verplicht else ""
    ster = '<b class="ster" aria-hidden="true"> *</b>' if verplicht else ""
    return f'<label class="veld"><span>{T(nl, en)}{ster}</span><input type="{type}" name="{naam}"{req}{extra}></label>'
def tekstvak(naam, nl, en, rijen=4, verplicht=False, breed=True):
    req = " required" if verplicht else ""
    return f'<label class="veld{" veld-breed" if breed else ""}"><span>{T(nl, en)}</span><textarea name="{naam}" rows="{rijen}"{req}></textarea></label>'

# Programma: per onderdeel een poortvraag; de keuzes eronder verschijnen pas als het onderdeel is aangevinkt.
# Samen dekken ze alles uit de catalogus (content/diensten.json) en de productkiezer op de homepage; aankoopadvies hoort hier niet (geen eventdienst).
DENKMEE = ("Weet ik nog niet, denk met me mee", "Not sure yet, help me decide")
SFEER = ("Sfeerverlichting", "Atmospheric lighting")
DECO = ("Decoratie: led-tubes, spiegelbollen en props", "Decoration: LED tubes, mirror balls and props")
PROGRAMMA = [
    ("sprekers", "Sprekers of presentaties", "Speakers or presentations", [
        ("Sprekersversterking en microfoons", "Speech amplification and microphones"),
        ("Videoschermen en presentatie", "Video screens and presentation"),
        ("Theaterlicht voor product of spreker", "Theatre lighting for product or speaker"),
        ("Online uitzending", "Online broadcast"),
        ("Technicus ter plekke", "Technician on site"),
    ]),
    ("borrel", "Borrel of diner met muziek", "Drinks or dinner with music", [
        ("Geluid voor borrel of feest", "Sound for a reception or party"),
        ("Playlist op maat", "Custom playlist"),
        SFEER, DECO,
    ]),
    ("feest", "Feest met dansvloer", "Party with a dance floor", [
        ("Soundsystem voor de dansvloer", "Sound system for the dance floor"),
        ("Dj", "DJ"),
        ("Dj-booth en dj-gear", "DJ booth and DJ gear"),
        ("Lichtshow", "Light show"),
        ("90's vintage licht", "90s vintage lighting"),
        SFEER, DECO,
        ("Partyfotograaf", "Party photographer"),
    ]),
]
# 'exoten': los van het programma, altijd zichtbaar, als inspiratie
EXTRAS = [
    ("Ledschermen met VJ", "LED screens with a live VJ"),
    ("Vocalist, saxofonist of percussionist", "Vocalist, saxophonist or percussionist"),
    ("Geuren-dj", "Scent DJ"),
]
COMMUNICATIE = [
    ("Communicatieadvies", "Communication advice"),
    ("Uitnodigingen en andere middelen", "Invitations and other materials"),
    ("Speeches en presentaties", "Speeches and presentations"),
    ("Bedrijfsvideo", "Corporate video"),
    ("Aftermovie", "Aftermovie"),
]
def poort(sleutel, nl, en, opties):
    return (f'<fieldset class="poort"><legend class="sr">{T(nl, en)}</legend>'
            f'<label class="vink poortvraag"><input type="checkbox" name="programma" value="{e(nl)}" data-poort="{sleutel}"><span>{T(nl, en)}</span></label>'
            f'<div class="poort-opties" id="poort-{sleutel}">{opties}</div></fieldset>')
def programma():
    # keuzes die bij meer dan één onderdeel horen (sfeerlicht, decoratie) lopen gelijk en tonen bij het tweede onderdeel 'reeds gekozen'
    telling = {}
    for _, _, _, items in PROGRAMMA:
        for inl, _ in items: telling[inl] = telling.get(inl, 0) + 1
    reeds = f'<em class="reeds-tag">{T("reeds gekozen", "already chosen")}</em>'
    blokken = ""
    for sleutel, nl, en, items in PROGRAMMA:
        opties = "".join(f'<label class="vink"><input type="checkbox" name="diensten" value="{e(inl)}"{" data-gedeeld" if telling[inl] > 1 else ""}><span>{T(inl, ien)}{reeds if telling[inl] > 1 else ""}</span></label>' for inl, ien in items)
        opties += f'<label class="vink"><input type="checkbox" name="diensten" value="{e(nl)}: weet ik nog niet, denk met me mee"><span>{T(*DENKMEE)}</span></label>'
        blokken += poort(sleutel, nl, en, opties)
    comm = ("".join(f'<label class="vink"><input type="checkbox" name="communicatie" value="{e(nl)}"><span>{T(nl, en)}</span></label>' for nl, en in COMMUNICATIE)
            + f'<label class="veld veld-breed"><span>{T("Anders, namelijk", "Other, namely")}</span><input type="text" name="communicatie_anders"></label>')
    blokken += poort("communicatie", "Hulp bij de communicatie rondom je event", "Help with the communication around your event", comm)
    extras = (f'<fieldset class="extras"><legend>{T("Heb je hier al eens aan gedacht?", "Have you thought about this?")}</legend><div class="extras-opties">'
              + "".join(f'<label class="vink"><input type="checkbox" name="diensten" value="{e(nl)}"><span>{T(nl, en)}</span></label>' for nl, en in EXTRAS) + '</div></fieldset>')
    return (f'<div class="programma">{blokken}</div>{extras}'
            f'<label class="veld veld-breed"><span>{T("Iets anders nodig? Namelijk", "Need something else? Namely")}</span><input type="text" name="diensten_anders"></label>')

SOORTEN = [("zakelijk", "Zakelijk (netwerk)event", "Corporate (networking) event"), ("lezing", "Lezing of seminar", "Lecture or seminar"),
           ("personeelsfeest", "Personeelsfeest", "Staff party"), ("merkactivatie", "Merkactivatie", "Brand activation"), ("dance", "Dance event", "Dance event")]
soort = (f'<label class="veld"><span>{T("Soort event", "Type of event")}</span><select name="soort" id="soort"><option value="">{T("Kies…", "Choose…")}</option>'
         + "".join(f'<option value="{w}">{T(nl, en)}</option>' for w, nl, en in SOORTEN)
         + f'<option value="anders">{T("Anders, namelijk", "Other, namely")}</option></select></label>'
         f'<label class="veld" id="soort_anders_veld" hidden><span>{T("Anders, namelijk", "Other, namely")}</span><input type="text" name="soort_anders"></label>')

budget = (f'<fieldset class="budget"><legend>{T("Richtbudget voor licht, geluid en muziek", "Indicative budget for light, sound and music")}</legend>'
          f'<p class="uitleg">{T("Een range is genoeg.", "A range is enough.")}</p>'
          f'<div class="slider" id="budget"><input type="range" name="budget_van" min="1000" max="25000" step="500" value="2500" aria-label="{A("Van", "From")}">'
          f'<input type="range" name="budget_tot" min="1000" max="25000" step="500" value="7500" aria-label="{A("Tot", "To")}"><output id="budget_uit"></output></div>'
          f'<label class="vink"><input type="checkbox" name="budget_onbekend" value="ja"><span>{T("Weet ik nog niet", "I don\'t know yet")}</span></label></fieldset>')

GESPREK = [("bellen", "Bel mij", "Call me"), ("teams", "Microsoft Teams", "Microsoft Teams"), ("meet", "Google Meet", "Google Meet")]
DAGDEEL = [("ochtend", "Ochtend", "Morning"), ("middag", "Middag", "Afternoon"), ("eind van de middag", "Eind van de middag", "Late afternoon")]
gesprek = (f'<div class="velden callvelden" id="callvelden"><fieldset class="keuze veld-breed"><legend>{T("Hoe wil je bellen?", "How would you like to talk?")}</legend><div class="keuzerij">'
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
    return (f'<section class="stap" data-stap="{n}"><p class="stapteller">{n}/4</p><h2>{T(kop_nl, kop_en)}</h2>{inhoud}'
            f'<p class="formvoet">{volgende}{vorige}</p></section>')

stap1 = stap(1, "Je event", "Your event", inhoud=f"""<p class="stapuitleg">{T("Vul in wat je al weet; weet je iets nog niet, laat het veld dan leeg.", "Fill in what you already know; if you don't know something yet, leave the field empty.")}</p><div class="velden">
{soort}
{veld("datum", "Datum van het event", "Date of the event", "date", extra=' id="v-datum"')}
{veld("tijd", "Tijd, van tot", "Time, from to", extra=' placeholder="16:00 – 23:00"')}
{veld("locatie", "Locatie", "Venue", extra=' id="v-locatie"')}
{veld("gasten", "Aantal gasten", "Number of guests", "number", extra=' min="1" inputmode="numeric" id="v-gasten"')}
</div>""")
stap2 = stap(2, "Je programma", "Your programme", f"""<p class="stapuitleg">{T("Vink aan wat er op het programma staat. Dan zie je wat we kunnen verzorgen.", "Tick what is on the programme. You will then see what we can take care of.")}</p>
{programma()}""")
stap3 = stap(3, "Budget en je verhaal", "Budget and your story", f"""{budget}
<label class="veld veld-breed"><span>{T("Vertel iets over je event", "Tell us about your event")}</span><small class="veldhulp">{T("Bijvoorbeeld de doelgroep, het concept, de gewenste beleving of de ruimte. Dit veld is niet verplicht.", "For example the audience, the concept, the experience you are after or the room. This field is optional.")}</small><textarea name="bericht" rows="5"></textarea></label>""")
stap4 = stap(4, "Hoe verder?", "What next?", f"""{route}
{gesprek}
<p class="stapuitleg tussenkop">{T("Velden met * zijn nodig om contact op te nemen.", "Fields marked * are needed to get in touch.")}</p><div class="velden">
{veld("naam", "Naam", "Name", verplicht=True, extra=' autocomplete="name"')}
{veld("organisatie", "Organisatie", "Organisation", extra=' autocomplete="organization"')}
{veld("email", "E-mail", "Email", "email", True, ' autocomplete="email"')}
{veld("telefoon", "Telefoonnummer", "Phone number", "tel", True, ' autocomplete="tel" id="telefoon"')}
</div>
<p class="uitleg privacyregel"><span>{T("We gebruiken je gegevens alleen om je aanvraag te beantwoorden.", "We only use your details to answer your request.")}</span> <a href="privacy.html">Privacyverklaring</a></p>""", laatste=True)

FOTO = f'<span class="dank-foto"><span>{T("Heb je foto\'s van de ruimte? Mail ze aan", "Do you have photos of the room? Email them to")}</span> {MAIL}</span>'
dank = (f'<div class="formmelding ok dank" id="dank-voorstel" hidden><strong>{T("Bedankt voor je aanvraag! We gaan ermee aan de slag. Je hoort meestal binnen 1 werkdag van ons.", "Thank you for your request! We are on it. You will usually hear from us within 1 working day.")}</strong>{FOTO}</div>'
        f'<div class="formmelding ok dank" id="dank-call" hidden><strong>{T("Bedankt voor je aanvraag! We nemen contact met je op om de call in te plannen, meestal binnen 1 werkdag.", "Thank you for your request! We will get in touch to schedule the call, usually within 1 working day.")}</strong>{FOTO}</div>')

form = f"""<form class="aanvraag" method="post" action="/api/aanvraag" id="aanvraag">
<input type="text" name="website" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
{stap1}
{stap2}
{stap3}
{stap4}
<p class="formmelding" id="melding" hidden></p>
{dank}
</form>"""

main = f"""<main class="wrap">
<section class="casehead"><a class="crumb" href="index.html"><span class="sectie">HEAR</span></a><h1 class="kernzin">{e(KOP)}</h1></section>
<section class="quick quick-breed"><p>{INTRO_HTML}</p></section>
<div class="aanvraag-kolommen">
{form}
<aside class="samenvatting" id="samenvatting" aria-live="polite" data-leeg="{A("Nog niets gekozen.", "Nothing chosen yet.")}" data-gasten="{A("gasten", "guests")}" data-budget="{A("Richtbudget", "Indicative budget")}" data-onbekend="{A("budget nog niet bekend", "budget not known yet")}"><h2>{T("Je aanvraag", "Your request")}</h2><div id="sv-inhoud"></div></aside>
</div>
</main>
<script>
(function(){{
  var f=document.getElementById('aanvraag'),m=document.getElementById('melding');
  var s=document.getElementById('budget');if(s){{var a=s.querySelectorAll('input'),o=document.getElementById('budget_uit');
    function eur(n){{return '€ '+Number(n).toLocaleString('nl-NL')}}
    function toon(){{var v=+a[0].value,t=+a[1].value;if(v>t){{if(this===a[0])a[1].value=v;else a[0].value=t;v=+a[0].value;t=+a[1].value}}o.textContent=eur(v)+' – '+eur(t)+(t>=25000?'+':'')}}
    a[0].addEventListener('input',toon);a[1].addEventListener('input',toon);toon()}}
  var so=document.getElementById('soort'),sa=document.getElementById('soort_anders_veld');if(so&&sa){{so.addEventListener('change',function(){{sa.hidden=so.value!=='anders'}})}}
  /* poortvragen: keuzes tonen als het onderdeel is aangevinkt; verborgen keuzes gaan niet mee */
  function poorten(){{[].forEach.call(f.querySelectorAll('[data-poort]'),function(p){{var b=document.getElementById('poort-'+p.dataset.poort);b.hidden=!p.checked;[].forEach.call(b.querySelectorAll('input'),function(i){{i.disabled=!p.checked}})}})}}
  [].forEach.call(f.querySelectorAll('[data-poort]'),function(p){{p.addEventListener('change',function(){{poorten();gedeeld();samenvat()}})}});poorten();
  /* gedeelde keuzes (bij meer dan één onderdeel) lopen gelijk; bij het andere onderdeel staat 'reeds gekozen' */
  var eigenaar={{}};
  function gedeeld(){{[].forEach.call(f.querySelectorAll('[data-gedeeld]'),function(i){{var e=eigenaar[i.value];i.closest('label').classList.toggle('reeds',i.checked&&!!e&&e!==i&&!e.disabled&&e.checked)}})}}
  [].forEach.call(f.querySelectorAll('[data-gedeeld]'),function(i){{i.addEventListener('change',function(){{if(i.checked)eigenaar[i.value]=i;else delete eigenaar[i.value];
    [].forEach.call(f.querySelectorAll('[data-gedeeld]'),function(x){{if(x!==i&&x.value===i.value)x.checked=i.checked}});gedeeld()}})}});
  /* samenvatting rechts: wat er tot nu toe is ingevuld */
  var sv=document.getElementById('samenvatting'),svi=document.getElementById('sv-inhoud'),budgetAan=false;
  function esc(t){{var d=document.createElement('div');d.textContent=t;return d.innerHTML}}
  function samenvat(){{var h='',ev=[],L=sv.dataset,so=document.getElementById('soort');
    if(so.value)ev.push(so.value==='anders'?(f.querySelector('[name=soort_anders]').value||so.options[so.selectedIndex].text):so.options[so.selectedIndex].text);
    var dv=document.getElementById('v-datum').value;if(dv){{var dd=new Date(dv+'T12:00:00');ev.push(dd.toLocaleDateString(location.pathname.indexOf('/en/')===0?'en-GB':'nl-NL',{{day:'numeric',month:'long',year:'numeric'}}))}}
    var tv=f.querySelector('[name=tijd]').value.trim();if(tv)ev.push(tv);var lv=document.getElementById('v-locatie').value.trim();if(lv)ev.push(lv);var gv=document.getElementById('v-gasten').value;if(gv)ev.push(gv+' '+L.gasten);
    if(ev.length)h+='<ul class="sv-event">'+ev.map(function(x){{return '<li>'+esc(x)+'</li>'}}).join('')+'</ul>';
    [].forEach.call(f.querySelectorAll('.poort'),function(p){{var q=p.querySelector('[data-poort]');if(!q.checked)return;var it=[];[].forEach.call(p.querySelectorAll('.poort-opties input[type=checkbox]:checked'),function(i){{if(!i.closest('label').classList.contains('reeds'))it.push(i.closest('label').querySelector('span').firstChild.textContent)}});
      var an=p.querySelector('.poort-opties input[type=text]');if(an&&an.value.trim())it.push(an.value.trim());
      h+='<h3>'+esc(q.closest('label').querySelector('span').textContent)+'</h3>'+(it.length?'<ul>'+it.map(function(x){{return '<li>'+esc(x)+'</li>'}}).join('')+'</ul>':'')}});
    var ex=[];[].forEach.call(f.querySelectorAll('.extras input:checked'),function(i){{ex.push(i.closest('label').querySelector('span').textContent)}});var da=f.querySelector('[name=diensten_anders]').value.trim();if(da)ex.push(da);
    if(ex.length)h+='<h3>'+esc(f.querySelector('.extras legend').textContent)+'</h3><ul>'+ex.map(function(x){{return '<li>'+esc(x)+'</li>'}}).join('')+'</ul>';
    if(f.querySelector('[name=budget_onbekend]').checked)h+='<p class="sv-regel">'+esc(L.onbekend)+'</p>';else if(budgetAan)h+='<p class="sv-regel">'+esc(L.budget)+': '+esc(document.getElementById('budget_uit').textContent)+'</p>';
    var rk=f.querySelector('[name=route]:checked');if(rk)h+='<p class="sv-regel sv-route">'+esc(rk.closest('label').querySelector('strong').textContent)+'</p>';
    sv.classList.toggle('leeg',!h);svi.innerHTML=h||'<p class="sv-leeg">'+esc(L.leeg)+'</p>'}}
  f.addEventListener('input',function(ev){{if(ev.target.name==='budget_van'||ev.target.name==='budget_tot')budgetAan=true;samenvat()}});f.addEventListener('change',samenvat);samenvat();
  /* route: bij een call de velden voor het contactmoment tonen */
  var cv=document.getElementById('callvelden'),gd=document.getElementById('gesprek-datum'),mist=document.getElementById('mist'),mt=document.getElementById('mist-tekst');
  function gekozen(){{var r=f.querySelector('[name=route]:checked');return r?r.value:''}}
  function route(){{var c=gekozen()==='call';cv.hidden=!c;gd.required=c;[].forEach.call(cv.querySelectorAll('input,select'),function(i){{i.disabled=!c}});mist.hidden=true;
    [].forEach.call(f.querySelectorAll('.routekaart'),function(k){{k.classList.toggle('aan',k.querySelector('input').checked)}})}}
  [].forEach.call(f.querySelectorAll('[name=route]'),function(r){{r.addEventListener('change',route)}});route();
  /* voor een voorstel is genoeg invoer nodig */
  function ontbreekt(){{var L=f.dataset,u=[];if(!document.getElementById('v-datum').value)u.push(L.mDatum);if(!document.getElementById('v-locatie').value.trim())u.push(L.mLocatie);if(!document.getElementById('v-gasten').value)u.push(L.mGasten);
    var stap=u.length?'1':'';if(!f.querySelector('[name=diensten]:checked:not(:disabled),[name=communicatie]:checked:not(:disabled)')&&!f.querySelector('[name=diensten_anders]').value.trim()){{u.push(L.mKeuze);stap=stap||'2'}}return {{lijst:u,stap:stap}}}}
  var st=f.querySelectorAll('.stap');f.classList.add('in-stappen');
  function ga(n,geschiedenis){{n=String(n);if(geschiedenis!==false&&history.pushState){{var st0=history.state&&history.state.stap;if(st0!==n)history.pushState({{stap:n}},'','#stap-'+n)}}var doel;st.forEach(function(x){{var aan=x.dataset.stap===n;x.hidden=!aan;if(aan)doel=x}});var h=doel.querySelector('h2');window.scrollTo({{top:f.getBoundingClientRect().top+window.scrollY-120,behavior:'smooth'}});h&&h.focus&&h.setAttribute('tabindex','-1');h&&h.focus({{preventScroll:true}})}}
  f.querySelectorAll('.stapknop').forEach(function(k){{k.addEventListener('click',function(){{var n=k.dataset.naar,huidig=k.closest('.stap');if(!n)return;
    if(k.classList.contains('vooruit')){{var ok=true;huidig.querySelectorAll('input,select,textarea').forEach(function(i){{if(ok&&!i.checkValidity()){{i.reportValidity();ok=false}}}});if(!ok)return}}ga(n)}})}});
  if(gd){{var nu=new Date();gd.min=nu.getFullYear()+'-'+String(nu.getMonth()+1).padStart(2,'0')+'-'+String(nu.getDate()).padStart(2,'0')}}
  function bedankt(r){{st.forEach(function(x){{x.hidden=true}});m.hidden=true;sv.hidden=true;var d=document.getElementById(r==='call'?'dank-call':'dank-voorstel');d.hidden=false;window.scrollTo({{top:f.getBoundingClientRect().top+window.scrollY-120,behavior:'smooth'}})}}
  var q=location.search;
  if(/verzonden=1/.test(q)){{bedankt(/route=call/.test(q)?'call':'voorstel')}}
  else{{if(history.replaceState)history.replaceState({{stap:'1'}},'',location.pathname+location.search);ga(1,false);if(/fout=1/.test(q)){{m.hidden=false;m.textContent=f.dataset.fout;m.className='formmelding fout'}}}}
  window.addEventListener('popstate',function(ev){{var n=(ev.state&&ev.state.stap)||'1';if(f.querySelector('.stap[data-stap="'+n+'"]')&&document.getElementById('dank-voorstel').hidden&&document.getElementById('dank-call').hidden)ga(n,false)}});
  f.addEventListener('submit',function(ev){{
    var r=gekozen();
    if(r==='voorstel'){{var o=ontbreekt();if(o.lijst.length){{ev.preventDefault();mt.textContent=f.dataset.mKop+' '+o.lijst.join(', ')+'.';document.getElementById('mist-knop').dataset.naar=o.stap;mist.hidden=false;return}}}}
    if(!window.fetch)return;ev.preventDefault();var b={{set disabled(v){{[].forEach.call(f.querySelectorAll('button[type=submit]'),function(x){{x.disabled=v}})}}}};b.disabled=true;
    fetch(f.action,{{method:'POST',body:new FormData(f),headers:{{'Accept':'application/json'}}}}).then(function(x){{return x.json()}}).then(function(x){{
      if(x.ok){{f.reset();poorten();bedankt(r)}}else{{m.hidden=false;m.textContent=f.dataset.fout;m.className='formmelding fout';b.disabled=false}}
    }}).catch(function(){{m.hidden=false;m.textContent=f.dataset.fout;m.className='formmelding fout';b.disabled=false}});
  }});
}})();
</script>"""
main = main.replace('<form class="aanvraag"', '<form class="aanvraag"'
    + f' data-fout="{A("Versturen lukte niet. Mail ons op maarten@hear.nl of bel +31 6 24560220.", "Sending failed. Email us at maarten@hear.nl or call +31 6 24560220.")}"'
    + f' data-m-kop="{A("Voor een voorstel hebben we nog nodig:", "For a proposal we still need:")}"'
    + f' data-m-datum="{A("de datum", "the date")}" data-m-locatie="{A("de locatie", "the venue")}" data-m-gasten="{A("het aantal gasten", "the number of guests")}"'
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
