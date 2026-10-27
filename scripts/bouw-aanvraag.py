"""Bouwt site/aanvraag.html: het aanvraagformulier (besluit 28 okt 2026, na feedback van een eventcoördinator bij de overheid:
WhatsApp is op werkplekken vaak geblokkeerd; een formulier is laagdrempeliger).
Opbouw: wat we nodig hebben (verplicht) → telefoonnummer voor terugbellen → "wil je verder nog iets kwijt" → handig voor ons, niet verplicht.
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
INTRO_HTML = "Vul in wat je al weet. Na je aanvraag bellen we je terug, meestal dezelfde werkdag. Liever mailen? Dat kan ook: " + MAIL + "."
paren.append((INTRO_HTML, "Fill in what you already know. After your request we call you back, usually the same working day. Prefer email? That works too: " + MAIL + "."))

def veld(naam, nl, en, type="text", verplicht=False, extra=""):
    req = " required" if verplicht else ""
    return f'<label class="veld"><span>{T(nl, en)}</span><input type="{type}" name="{naam}"{req}{extra}></label>'
def tekstvak(naam, nl, en, rijen=4, verplicht=False):
    req = " required" if verplicht else ""
    return f'<label class="veld veld-breed"><span>{T(nl, en)}</span><textarea name="{naam}" rows="{rijen}"{req}></textarea></label>'

# 4×4 diensten uit de catalogus
DIENSTEN = [
    ("Geluid", "Sound", [
        ("Sprekersversterking en microfoons", "Speech amplification and microphones"),
        ("Geluid voor borrel of feest", "Sound for a reception or party"),
        ("Dansvloersysteem", "Dance floor system"),
        ("Technicus ter plekke", "Technician on site"),
    ]),
    ("Licht", "Light", [
        ("Sfeerverlichting", "Atmospheric lighting"),
        ("Dansvloerverlichting en lichtshow", "Dance floor lighting and light show"),
        ("90's vintage lichteffecten", "90s vintage light effects"),
        ("Theaterlicht voor product of spreker", "Theatre lighting for product or speaker"),
    ]),
    ("Muziek", "Music", [
        ("Dj", "DJ"),
        ("Vocalist, saxofonist of percussionist", "Vocalist, saxophonist or percussionist"),
        ("Playlist op maat", "Custom playlist"),
        ("Dj-booth en gear voor je eigen dj", "DJ booth and gear for your own DJ"),
    ]),
    ("Extra", "Extra", [
        ("Online uitzending", "Online broadcast"),
        ("Videoschermen en presentatie", "Video screens and presentation"),
        ("Videoproductie of aftermovie", "Video production or aftermovie"),
        ("Advies over concept en programma", "Advice on concept and programme"),
    ]),
]
def diensten():
    kol = ""
    for knl, ken, items in DIENSTEN:
        kol += f'<fieldset class="dienstkolom"><legend>{T(knl, ken)}</legend>' + "".join(
            f'<label class="vink"><input type="checkbox" name="diensten" value="{e(nl)}"><span>{T(nl, en)}</span></label>' for nl, en in items) + '</fieldset>'
    return (f'<fieldset class="diensten"><legend>{T("Wat heb je nodig?", "What do you need?")}</legend><div class="dienstgrid">{kol}</div>'
            f'<label class="veld veld-breed"><span>{T("Anders, namelijk", "Other, namely")}</span><input type="text" name="diensten_anders"></label></fieldset>')

soort = (f'<fieldset class="keuze"><legend>{T("Soort event", "Type of event")}</legend>'
         f'<label class="vink"><input type="radio" name="soort" value="zakelijk" required><span>{T("Zakelijk event", "Corporate event")}</span></label>'
         f'<label class="vink"><input type="radio" name="soort" value="dance"><span>{T("Dance event", "Dance event")}</span></label>'
         f'<label class="vink"><input type="radio" name="soort" value="anders"><span>{T("Anders", "Other")}</span></label>'
         f'<input type="text" name="soort_anders" class="inline" aria-label="{A("Anders, namelijk", "Other, namely")}" placeholder="{A("namelijk…", "namely…")}"></fieldset>')

budget = (f'<fieldset class="budget"><legend>{T("Richtbudget voor licht, geluid en muziek", "Indicative budget for light, sound and music")}</legend>'
          f'<p class="uitleg">{T("Een range is genoeg; je hoeft geen bedrag te noemen.", "A range is enough; you don\'t have to name a figure.")}</p>'
          f'<div class="slider" id="budget"><input type="range" name="budget_van" min="1000" max="25000" step="500" value="2500" aria-label="{A("Van", "From")}">'
          f'<input type="range" name="budget_tot" min="1000" max="25000" step="500" value="7500" aria-label="{A("Tot", "To")}"><output id="budget_uit"></output></div>'
          f'<label class="vink"><input type="checkbox" name="budget_onbekend" value="ja"><span>{T("Weet ik nog niet", "I don\'t know yet")}</span></label></fieldset>')

form = f'''<form class="aanvraag" method="post" action="/api/aanvraag" id="aanvraag">
<input type="text" name="website" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<section class="formblok"><h2>{T("Wat we nodig hebben", "What we need")}</h2>
<div class="velden">
{veld("naam", "Naam", "Name", verplicht=True, extra=' autocomplete="name"')}
{veld("organisatie", "Organisatie", "Organisation", verplicht=True, extra=' autocomplete="organization"')}
{veld("email", "E-mail", "Email", "email", True, ' autocomplete="email"')}
{veld("telefoon", "Telefoonnummer, dan bellen we je terug", "Phone number, so we can call you back", "tel", True, ' autocomplete="tel"')}
{soort}
{veld("datum", "Datum van het event", "Date of the event", "date", True)}
{veld("gasten", "Aantal gasten", "Number of guests", "number", True, ' min="1" inputmode="numeric"')}
</div>
{diensten()}
</section>
<section class="formblok zacht"><h2>{T("Wil je verder nog iets kwijt?", "Anything else you want to tell us?")}</h2>
{tekstvak("bericht", "Je bericht", "Your message", 5)}
</section>
<section class="formblok optioneel"><h2>{T("Handig voor ons, niet verplicht", "Useful for us, not required")}</h2>
<div class="velden">
{veld("functie", "Je functie", "Your role")}
{veld("event", "Naam van het event", "Name of the event")}
{veld("tijd", "Tijd, van tot", "Time, from to", extra=' placeholder="16:00 – 23:00"')}
{veld("doelgroep", "Doelgroep", "Audience")}
{tekstvak("concept", "Het concept of het programma", "The concept or programme", 4)}
{veld("m2", "Ruimte in m²", "Room size in m²", "number", extra=' min="1" inputmode="numeric"')}
{veld("diepte", "Diepte van de ruimte in meters", "Depth of the room in metres", "number", extra=' min="1" inputmode="numeric"')}
{tekstvak("ruimte", "Beschrijving van de ruimte", "Description of the room", 3)}
</div>
{budget}
</section>
<p class="formvoet"><button type="submit" class="wa knop">{T("Verstuur je aanvraag", "Send your request")}<i aria-hidden="true">→</i></button>
<span class="uitleg"><span>{T("We gebruiken je gegevens alleen om je aanvraag te beantwoorden.", "We only use your details to answer your request.")}</span> <a href="privacy.html">Privacyverklaring</a></span></p>
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
  var q=location.search;if(/verzonden=1/.test(q)){{m.hidden=false;m.textContent=f.dataset.dank;m.className='formmelding ok'}}else if(/fout=1/.test(q)){{m.hidden=false;m.textContent=f.dataset.fout;m.className='formmelding fout'}}
  f.addEventListener('submit',function(ev){{
    if(!window.fetch)return;ev.preventDefault();var b=f.querySelector('button');b.disabled=true;
    fetch(f.action,{{method:'POST',body:new FormData(f),headers:{{'Accept':'application/json'}}}}).then(function(r){{return r.json()}}).then(function(r){{
      m.hidden=false;if(r.ok){{m.textContent=f.dataset.dank;m.className='formmelding ok';f.reset();toon&&toon()}}else{{m.textContent=f.dataset.fout;m.className='formmelding fout';b.disabled=false}}
    }}).catch(function(){{m.hidden=false;m.textContent=f.dataset.fout;m.className='formmelding fout';b.disabled=false}});
  }});
}})();
</script>'''
main = main.replace('<form class="aanvraag"', f'<form class="aanvraag" data-dank="{A("Dank je. We bellen je terug, meestal dezelfde werkdag.", "Thank you. We will call you back, usually the same working day.")}" data-fout="{A("Versturen lukte niet. Mail ons op maarten@hear.nl of bel +31 6 24560220.", "Sending failed. Email us at maarten@hear.nl or call +31 6 24560220.")}"')

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
