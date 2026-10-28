"""Bouwt site/aanvraag.html: het aanvraagformulier (besluit 28 okt 2026, na feedback van een eventcoördinator bij de overheid:
WhatsApp is op werkplekken vaak geblokkeerd; een formulier is laagdrempeliger).
Opbouw in drie stappen (28 okt): 1/3 kennismaken (hoe bespreken: bellen/Teams/Meet, voorkeursdatum en dagdeel, contactgegevens), 2/3 over je event, 3/3 wat je nodig hebt (diensten, budget, vrij veld). Zonder JavaScript staan de stappen onder elkaar.
Het formulier post naar /api/aanvraag (src/index.js), dat de inzending mailt naar maarten@hear.nl. Geen opslag.
Schrijft ook de Engelse paren naar content/en.json (paginas → aanvraag.html). Draaien vóór bouw-en.py."""
import json, pathlib, html
root = pathlib.Path(__file__).resolve().parent.parent
site = root / "site"
idx = (site / "index.html").read_text()
kop = idx[idx.index('<header class="top">'):idx.index('</script>') + 9]
voet = idx[idx.index('<footer class="voet">'):idx.index('</footer>') + 9]
e = lambda t: html.escape(t, quote=True)

paren = [("<title>Aanvraag · HEAR</title>", "<title>Request · HEAR</title>")]  # (nl, en) als tekst tussen tags; attributen apart
def T(nl, en):
    paren.append((f'>{e(nl)}<', f'>{e(en)}<')); return e(nl)
def A(nl, en):  # attribuutwaarde (placeholder, aria-label)
    paren.append((f'="{e(nl)}"', f'="{e(en)}"')); return e(nl)

TITEL = "Aanvraag"
KOP = "Vertel over je event"
MAIL = '<a href="mailto:maarten@hear.nl">maarten@hear.nl</a>'
INTRO_HTML = "In drie korte stappen. Vul in wat je al weet; weet je iets nog niet, laat het veld dan leeg. Liever mailen? Dat kan ook: " + MAIL + "."
paren.append((INTRO_HTML, "In three short steps. Fill in what you already know; if you don't know something yet, leave the field empty. Prefer email? That works too: " + MAIL + "."))

def veld(naam, nl, en, type="text", verplicht=False, extra=""):
    req = " required" if verplicht else ""
    return f'<label class="veld"><span>{T(nl, en)}</span><input type="{type}" name="{naam}"{req}{extra}></label>'
def tekstvak(naam, nl, en, rijen=4, verplicht=False, breed=True):
    req = " required" if verplicht else ""
    return f'<label class="veld{" veld-breed" if breed else ""}"><span>{T(nl, en)}</span><textarea name="{naam}" rows="{rijen}"{req}></textarea></label>'

# diensten uit de catalogus, vier kolommen
DIENSTEN = [
    ("Geluid", "Sound", [
        ("Sprekersversterking en microfoons", "Speech amplification and microphones"),
        ("Geluid voor borrel of feest", "Sound for a reception or party"),
        ("Dansvloer geluidsysteem", "Dance floor sound system"),
        ("Dj-booth en gear voor je eigen dj", "DJ booth and gear for your own DJ"),
        ("Technicus ter plekke", "Technician on site"),
    ]),
    ("Licht en audiovisueel", "Light and audiovisual", [
        ("Sfeerverlichting", "Atmospheric lighting"),
        ("Lichtshow", "Light show"),
        ("Theaterlicht voor product of spreker", "Theatre lighting for product or speaker"),
        ("Videoschermen en presentatie", "Video screens and presentation"),
        ("Online uitzending", "Online broadcast"),
    ]),
    ("Artiesten", "Artists", [
        ("Dj", "DJ"),
        ("Vocalist, saxofonist of percussionist", "Vocalist, saxophonist or percussionist"),
        ("Playlist op maat", "Custom playlist"),
        ("Partyfotograaf", "Party photographer"),
    ]),
]
COMMUNICATIE = [
    ("Communicatieadvies", "Communication advice"),
    ("Uitnodigingen en andere middelen", "Invitations and other materials"),
    ("Speeches en presentaties", "Speeches and presentations"),
    ("Bedrijfsvideo", "Corporate video"),
    ("Aftermovie", "Aftermovie"),
]
def communicatie():
    return (f'<fieldset class="communicatie"><legend>{T("Wij kunnen je ook helpen met de communicatie rondom je event. Vink aan wat je interessant vindt.", "We can also help with the communication around your event. Tick what interests you.")}</legend><div class="keuzelijst">'
            + "".join(f'<label class="vink"><input type="checkbox" name="communicatie" value="{e(nl)}"><span>{T(nl, en)}</span></label>' for nl, en in COMMUNICATIE)
            + f'</div><label class="veld veld-breed"><span>{T("Anders, namelijk", "Other, namely")}</span><input type="text" name="communicatie_anders"></label></fieldset>')
def diensten():
    kol = ""
    for knl, ken, items in DIENSTEN:
        kol += f'<fieldset class="dienstkolom"><legend>{T(knl, ken)}</legend>' + "".join(
            f'<label class="vink"><input type="checkbox" name="diensten" value="{e(nl)}"><span>{T(nl, en)}</span></label>' for nl, en in items) + '</fieldset>'
    return (f'<fieldset class="diensten"><legend class="sr">{T("Diensten", "Services")}</legend><div class="dienstgrid">{kol}</div>'
            f'<label class="veld veld-breed"><span>{T("Anders, namelijk", "Other, namely")}</span><input type="text" name="diensten_anders"></label></fieldset>')

SOORTEN = [("zakelijk", "Zakelijk (netwerk)event", "Corporate (networking) event"), ("lezing", "Lezing of seminar", "Lecture or seminar"),
           ("personeelsfeest", "Personeelsfeest", "Staff party"), ("merkactivatie", "Merkactivatie", "Brand activation"), ("dance", "Dance event", "Dance event")]
soort = (f'<label class="veld"><span>{T("Soort event", "Type of event")}</span><select name="soort" id="soort"><option value="">{T("Kies…", "Choose…")}</option>'
         + "".join(f'<option value="{w}">{T(nl, en)}</option>' for w, nl, en in SOORTEN)
         + f'<option value="anders">{T("Anders, namelijk", "Other, namely")}</option></select></label>'
         f'<label class="veld" id="soort_anders_veld" hidden><span>{T("Anders, namelijk", "Other, namely")}</span><input type="text" name="soort_anders"></label>')

budget = (f'<fieldset class="budget"><legend>{T("Richtbudget voor licht, geluid en muziek", "Indicative budget for light, sound and music")}</legend>'
          f'<p class="uitleg">{T("Een range is genoeg; je hoeft geen bedrag te noemen.", "A range is enough; you don\'t have to name a figure.")}</p>'
          f'<div class="slider" id="budget"><input type="range" name="budget_van" min="1000" max="25000" step="500" value="2500" aria-label="{A("Van", "From")}">'
          f'<input type="range" name="budget_tot" min="1000" max="25000" step="500" value="7500" aria-label="{A("Tot", "To")}"><output id="budget_uit"></output></div>'
          f'<label class="vink"><input type="checkbox" name="budget_onbekend" value="ja"><span>{T("Weet ik nog niet", "I don\'t know yet")}</span></label></fieldset>')

GESPREK = [("bellen", "Bel mij", "Call me"), ("teams", "Microsoft Teams", "Microsoft Teams"), ("meet", "Google Meet", "Google Meet")]
DAGDEEL = [("ochtend", "Ochtend", "Morning"), ("middag", "Middag", "Afternoon"), ("eind van de middag", "Eind van de middag", "Late afternoon")]
gesprek = (f'<fieldset class="keuze veld-breed"><legend>{T("Hoe wil je je wensen bespreken?", "How would you like to discuss your plans?")}</legend><div class="keuzerij">'
           + "".join(f'<label class="vink"><input type="radio" name="gesprek" value="{w}"{" checked" if w == "bellen" else ""}><span>{T(nl, en)}</span></label>' for w, nl, en in GESPREK)
           + '</div></fieldset>'
           + veld("gesprek_datum", "Wanneer schikt het?", "When suits you?", "date")
           + f'<label class="veld"><span>{T("Dagdeel", "Time of day")}</span><select name="gesprek_dagdeel"><option value="">{T("Maakt niet uit", "No preference")}</option>'
           + "".join(f'<option value="{w}">{T(nl, en)}</option>' for w, nl, en in DAGDEEL) + '</select></label>')

def stap(n, kop_nl, kop_en, inhoud, laatste=False):
    vorige = f'<button type="button" class="stapknop terug" data-naar="{n-1}">{T("← Vorige", "← Back")}</button>' if n > 1 else ''
    volgende = (f'<button type="submit" class="wa knop">{T("Verstuur je aanvraag", "Send your request")}<i aria-hidden="true">→</i></button>'
                if laatste else f'<button type="button" class="wa knop stapknop vooruit" data-naar="{n+1}">{T("Volgende", "Next")}<i aria-hidden="true">→</i></button>')
    return (f'<section class="stap" data-stap="{n}"><p class="stapteller">{n}/3</p><h2>{T(kop_nl, kop_en)}</h2>{inhoud}'
            f'<p class="formvoet">{volgende}{vorige}</p></section>')

stap1 = stap(1, "Kennismaken", "Getting acquainted", f'''<div class="velden">
{gesprek}
{veld("naam", "Naam", "Name", verplicht=True, extra=' autocomplete="name"')}
{veld("organisatie", "Organisatie", "Organisation", extra=' autocomplete="organization"')}
{veld("email", "E-mail", "Email", "email", True, ' autocomplete="email"')}
{veld("telefoon", "Telefoonnummer", "Phone number", "tel", extra=' autocomplete="tel" id="telefoon"')}
{veld("functie", "Je functie", "Your role")}
</div>''')
stap2 = stap(2, "Over je event", "About your event", f'''<div class="velden">
{veld("event", "Naam van het event", "Name of the event")}
{soort}
{veld("locatie", "Locatie", "Venue")}
{tekstvak("ruimte", "Beschrijf de ruimte", "Describe the room", 2, breed=False)}
{veld("datum", "Datum van het event", "Date of the event", "date")}
{veld("tijd", "Tijd, van tot", "Time, from to", extra=' placeholder="16:00 – 23:00"')}
{veld("gasten", "Aantal gasten", "Number of guests", "number", extra=' min="1" inputmode="numeric"')}
{veld("doelgroep", "Doelgroep", "Audience")}
{tekstvak("concept", "Het concept of het programma", "The concept or programme", 4)}
</div>''')
stap3 = stap(3, "Wat heb je nodig?", "What do you need?", f'''{diensten()}
{communicatie()}
{budget}
{tekstvak("bericht", "Wil je verder nog iets kwijt?", "Anything else you want to tell us?", 5)}
<p class="uitleg privacyregel"><span>{T("We gebruiken je gegevens alleen om je aanvraag te beantwoorden.", "We only use your details to answer your request.")}</span> <a href="privacy.html">Privacyverklaring</a></p>''', laatste=True)

form = f'''<form class="aanvraag" method="post" action="/api/aanvraag" id="aanvraag">
<input type="text" name="website" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
{stap1}
{stap2}
{stap3}
<p class="formmelding" id="melding" hidden></p>
</form>'''

main = f'''<main class="wrap">
<section class="casehead"><a class="crumb" href="index.html"><span class="sectie">HEAR</span></a><h1 class="kernzin">{T(KOP, "Tell us about your event")}</h1></section>
<section class="quick quick-breed"><p>{INTRO_HTML}</p></section>
{form}
</main>
<script>
(function(){{
  var f=document.getElementById('aanvraag'),m=document.getElementById('melding');
  var s=document.getElementById('budget');if(s){{var a=s.querySelectorAll('input'),o=document.getElementById('budget_uit');
    function eur(n){{return '€ '+Number(n).toLocaleString('nl-NL')}}
    function toon(){{var v=+a[0].value,t=+a[1].value;if(v>t){{if(this===a[0])a[1].value=v;else a[0].value=t;v=+a[0].value;t=+a[1].value}}o.textContent=eur(v)+' – '+eur(t)+(t>=25000?'+':'')}}
    a[0].addEventListener('input',toon);a[1].addEventListener('input',toon);toon()}}
  var so=document.getElementById('soort'),sa=document.getElementById('soort_anders_veld');if(so&&sa){{so.addEventListener('change',function(){{sa.hidden=so.value!=='anders'}})}}
  var st=f.querySelectorAll('.stap');f.classList.add('in-stappen');
  function ga(n){{st.forEach(function(x){{x.hidden=+x.dataset.stap!==n}});var h=st[n-1].querySelector('h2');window.scrollTo({{top:f.getBoundingClientRect().top+window.scrollY-120,behavior:'smooth'}});h&&h.focus&&h.setAttribute('tabindex','-1');h&&h.focus({{preventScroll:true}})}}
  f.querySelectorAll('.stapknop').forEach(function(k){{k.addEventListener('click',function(){{var n=+k.dataset.naar,huidig=k.closest('.stap');
    if(k.classList.contains('vooruit')){{var ok=true;huidig.querySelectorAll('input,select,textarea').forEach(function(i){{if(ok&&!i.checkValidity()){{i.reportValidity();ok=false}}}});if(!ok)return}}ga(n)}})}});
  var tel=document.getElementById('telefoon');function telv(){{var g=f.querySelector('input[name=gesprek]:checked');tel.required=!!g&&g.value==='bellen'}}
  f.querySelectorAll('input[name=gesprek]').forEach(function(r){{r.addEventListener('change',telv)}});telv();ga(1);
  var q=location.search;if(/verzonden=1/.test(q)){{m.hidden=false;m.textContent=f.dataset.dank;m.className='formmelding ok'}}else if(/fout=1/.test(q)){{m.hidden=false;m.textContent=f.dataset.fout;m.className='formmelding fout'}}
  f.addEventListener('submit',function(ev){{
    if(!window.fetch)return;ev.preventDefault();var b=f.querySelector('button');b.disabled=true;
    fetch(f.action,{{method:'POST',body:new FormData(f),headers:{{'Accept':'application/json'}}}}).then(function(r){{return r.json()}}).then(function(r){{
      m.hidden=false;if(r.ok){{m.textContent=f.dataset.dank;m.className='formmelding ok';f.reset();st.forEach(function(x){{x.hidden=true}})}}else{{m.textContent=f.dataset.fout;m.className='formmelding fout';b.disabled=false}}
    }}).catch(function(){{m.hidden=false;m.textContent=f.dataset.fout;m.className='formmelding fout';b.disabled=false}});
  }});
}})();
</script>'''
main = main.replace('<form class="aanvraag"', f'<form class="aanvraag" data-dank="{A("Dank je. We nemen contact met je op om het gesprek in te plannen, meestal dezelfde werkdag.", "Thank you. We will get in touch to schedule the conversation, usually the same working day.")}" data-fout="{A("Versturen lukte niet. Mail ons op maarten@hear.nl of bel +31 6 24560220.", "Sending failed. Email us at maarten@hear.nl or call +31 6 24560220.")}"')

BESCHRIJVING = "Vraag licht, geluid, dj of advies aan voor je event. Vul in wat je al weet; we bellen je terug."
doc = f'''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{A(BESCHRIJVING, "Request light, sound, a DJ or advice for your event. Fill in what you already know; we call you back.")}"><title>{TITEL} · HEAR</title><link rel="stylesheet" href="home.css"><link rel="stylesheet" href="styles.css"></head><body class="pagina">
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
