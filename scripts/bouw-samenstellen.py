#!/usr/bin/env python3
"""Samensteller (20 nov): algemene aanvraagpagina waarop de klant zijn event samenstelt uit bouwstenen.
Begonnen als demo voor een partnerlocatie; op 20 nov algemeen gemaakt (Maarten): geen locatienamen meer, de klant vult zelf de locatie in.
Vorm ('route 3'): de foto blijft één foto; de blokjes zijn een eigen tekening, schuin van boven met ronde noppen.
Ze staan bij de knop bovenaan, op elke bouwsteen (wit, kleurt bij kiezen) en als stapel in 'Jouw event' die groeit met elke keuze.
Twee varianten: samenstellen.html (met prijzen) en samenstellen-zonder-prijzen.html.
Kop, menu en voet komen uit site/nieuwjaarsborrel.html (draai dit script dus na bouw-doelgroepen).
Niet gelinkt vanaf de site, noindex."""
import pathlib, re, sys, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from blokjes import KLEUR, iso_stapel, ISO_JS
site = pathlib.Path(__file__).resolve().parent.parent / "site"
basis = (site / "nieuwjaarsborrel.html").read_text(encoding="utf-8")
i = basis.index('<main class="wrap lp">')
kop = basis[:i]
voet = basis[basis.index('<footer class="actie-voet">'):]
utm_js = re.search(r'<script>\(function\(\)\{try\{var q=new URLSearchParams.*?</script>', basis, re.S)
if not utm_js:
    sys.exit("utm-script niet gevonden in nieuwjaarsborrel.html")
utm_js = utm_js.group(0)

TITEL = "Stel je event samen | HEAR"
OMSCHR = "Stel in twee minuten licht, geluid en dj samen voor je event."

def e(t):
    return html.escape(t, quote=True)

# (groep, waarde in de mail, titel, ondertitel, prijs, 'vanaf'?)
# geluid: prijs per grootte (intiem, midsize, groot), bedragen van Maarten (20 nov)
GROOTTES = ["intiem (tot 200 gasten)", "midsize (200 tot 500 gasten)", "groot (500 tot 1.000 gasten)"]
GELUID = [
    ("Geluid voor spraak", "Met handmicrofoons of reversmicrofoons", (600, 900, 1200)),
    ("Geluid voor spraak en muziek", "Met microfoons, dj-booth en dj-gear", (800, 1100, 1400)),
]
# personeel: per uur, het aantal uren kiest de klant in de zin bovenaan
TARIEF_TECHNICUS, TARIEF_DJ = 100, 150
LICHT = [
    ("Sfeerlicht", "De ruimte in kleur"),
    ("Decoratie", "Led-tubes, spiegelbollen en props"),
    ("Dansvloerlicht", "Bewegend licht boven de dansvloer"),
]
SOORTEN = ["congres of seminar", "vergadering of training", "borrel of cocktailparty", "diner", "bedrijfsfeest",
           "productpresentatie", "bruiloft of privéfeest", "iets anders"]

def eur(n):
    return "€ " + f"{n:,}".replace(",", ".")

def blok(naam, titel, sub, prijs, groep, soort, prijzen, vanaf=False, prijstekst=None):
    staffel = ""
    if isinstance(prijs, tuple):
        staffel = f' data-staffel="{",".join(str(x) for x in prijs)}"'
        prijs = prijs[0]
    p = f'<span class="cs-prijs">{"vanaf " if vanaf else ""}{eur(prijs)}</span>' if prijzen and prijs else ""
    if prijzen and prijstekst:
        p = f'<span class="cs-prijs">{prijstekst}</span>'
    return (f'<label class="cs-blok cs-{soort}"><input type="checkbox" name="{naam}" value="{e(titel)}" data-groep="{groep}" data-prijs="{prijs or 0}"{staffel} data-kleur="{KLEUR[soort]}">'
            f'<span class="cs-blok-in"><span class="cs-titel">{titel}</span><span class="cs-sub">{sub}</span>{p}'
            f'{iso_stapel([KLEUR["wit"]], 30, 2.2, "cs-ic cs-ic-uit")}{iso_stapel([KLEUR[soort]], 30, 2.2, "cs-ic cs-ic-aan")}</span></label>')

# De tekening van de blokjes staat in scripts/blokjes.py (gedeeld met de proef voor het aanvraagformulier).
HOOFDBEELD = ("img/case-prive-breed.jpg", "50% 88%", "Gasten op de dansvloer in een zaal met gekleurd licht en ballonnen")

def pagina(prijzen):
    variant = "met prijzen" if prijzen else "zonder prijzen"
    geluid = "".join(blok("geluid", t, s, p, "geluid", "geluid", prijzen) for t, s, p in GELUID)
    scherm = blok("scherm", "Ledscherm", "Voor presentatie of visuals, meerdere schermen mogelijk", 150, "", "scherm", prijzen, vanaf=True)
    def mens(veld, titel, sub, tarief):
        pr = f'<span class="cs-prijs" data-tarief="{eur(tarief)} per uur">{eur(tarief)} per uur</span>' if prijzen else '<span class="cs-prijs" data-tarief=""></span>'
        return (f'<label class="cs-blok cs-personeel cs-mens" for="cs-{veld}" data-veld="{veld}" data-naam="{e(titel)}" data-tarief="{tarief}" data-kleur="{KLEUR["personeel"]}">'
                f'<span class="cs-blok-in"><span class="cs-titel">{titel}</span><span class="cs-sub">{sub}</span>{pr}'
                f'{iso_stapel([KLEUR["wit"]], 30, 2.2, "cs-ic cs-ic-uit")}{iso_stapel([KLEUR["personeel"]], 30, 2.2, "cs-ic cs-ic-aan")}</span></label>')
    personeel = (mens("uren_dag", "Geluidstechnicus", "Tijdens je dagprogramma", TARIEF_TECHNICUS)
                 + mens("uren_dj", "Dj", "Voor je cocktail of feestavond", TARIEF_DJ))
    uren = lambda n: '<option value="0">geen</option>' + "".join(f'<option value="{i}">{i} uur</option>' for i in range(1, n + 1))
    licht = "".join(blok("licht", t, s, None, "", "licht", prijzen) for t, s in LICHT)
    logo = blok("logo", "Ledscherm met logo", "Je logo en mooie animaties op led-panelen", None, "", "licht", prijzen, prijstekst="op aanvraag")
    lichtprijs = '<p class="cs-noot">Sfeerlicht, decoratie en dansvloerlicht: één onderdeel € 350, twee € 600, alle drie € 800.</p>' if prijzen else ""
    totaal = ('<p class="cs-totaal"><span>Vanaf</span><b id="cs-som">€ 0</b><small>exclusief btw</small></p><p class="cs-voordeel" id="cs-voordeel" hidden></p>'
              if prijzen else '<p class="cs-totaal cs-zonder"><span>Je hoort dezelfde werkdag wat dit kost.</span></p>')
    main = f"""<main class="wrap lp cs" data-prijzen="{1 if prijzen else 0}">
<section class="casehead"><h1 class="kernzin">Stel je event samen</h1></section>
<div class="lp-held cs-held"><div class="cs-foto"><img src="{HOOFDBEELD[0]}" alt="{e(HOOFDBEELD[2])}" style="object-position:{HOOFDBEELD[1]}"><a class="cs-samen" href="#bouwstenen">{iso_stapel([KLEUR["geluid"], KLEUR["personeel"], KLEUR["licht"]], 40, 2)}<b>Stel je<br>event samen</b><i aria-hidden="true">→</i></a></div></div>
<section class="lp-band"><div class="lp-twee"><p class="lp-lead">Leuk dat je een event organiseert.</p><div class="lp-tekst"><p>Of het nou om een congres gaat, een cocktailparty met dj of misschien wel beide: wij verzorgen het voor je van A tot Z.</p><p>Vul hier je aanvraag in twee minuten in.</p><p class="cs-hulp"><a class="wa" href="https://wa.me/31624560220?text=Hoi%20Maarten%2C%20ik%20heb%20een%20vraag%20over%20mijn%20event." target="_blank" rel="noopener"><span>Weet je niet wat je moet invullen? Stuur me een appje</span><i aria-hidden="true">→</i></a></p></div></div></section>
<form class="cs-form" method="post" action="/api/aanvraag" data-dank="Dank je. Je hoort dezelfde werkdag van me." data-fout="Versturen lukte niet. Mail naar maarten@hear.nl of bel +31 6 24560220.">
<input type="hidden" name="bron" value="Pagina Samenstellen ({variant})"><input type="hidden" name="utm" value=""><input type="hidden" name="indicatie" value=""><input type="hidden" name="personeel" value=""><input type="text" name="website" class="lp-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<section class="lp-band cs-bouw" id="bouwstenen"><div class="cs-kolommen"><div class="cs-keuzes">
<fieldset class="cs-stap cs-zin"><legend class="lp-strip">Je event</legend>
<label class="cs-kies"><span>Ik organiseer een</span><select name="soort">{"".join(f"<option>{e(x)}</option>" for x in SOORTEN)}</select></label>
<label class="cs-kies"><span>in</span><input class="cs-locatie" name="locatie" placeholder="naam locatie" aria-label="Naam van de locatie" autocomplete="off"></label>
<label class="cs-kies"><span>voor</span><select name="gasten" id="cs-grootte" aria-label="Grootte van je event">{"".join(f"<option>{e(x)}</option>" for x in GROOTTES)}</select></label>
<label class="cs-kies cs-uren"><span>met</span><select name="uren_dag" id="cs-uren_dag" aria-label="Aantal uren dagprogramma">{uren(12)}</select><span>dagprogramma</span></label>
<label class="cs-kies cs-uren"><span>en</span><select name="uren_dj" id="cs-uren_dj" aria-label="Aantal uren dj">{uren(8)}</select><span>dj</span></label>
</fieldset>
<fieldset class="cs-stap"><legend class="lp-strip">Kies de bouwstenen van je event</legend>
<h3 class="cs-groep">Geluid</h3><p class="cs-intro">Hoogwaardig geluid, afgestemd op de ruimte.</p>
<div class="cs-blokken">{geluid}</div>
<h3 class="cs-groep">Personeel</h3>
<div class="cs-blokken">{personeel}</div>
<p class="cs-noot">Het aantal uren kies je bovenaan. Bij alleen muziek regelt de dj het geluid zelf.</p>
<h3 class="cs-groep">Licht en aankleding</h3>
<div class="cs-blokken">{licht}{scherm}{logo}</div>{lichtprijs}
</fieldset></div>
<aside class="cs-stapel" aria-live="polite"><h2 class="cs-stapel-kop">Jouw event</h2><div class="cs-toren" id="cs-toren" hidden><span id="cs-toren-beeld"></span><ul class="cs-stenen" id="cs-stenen"></ul></div><p class="cs-leeg" id="cs-leeg">Kies je eerste bouwsteen.</p>{totaal}<a class="cs-verder" href="#contact">Naar je gegevens <i aria-hidden="true">→</i></a></aside>
</div></section>
<section class="lp-band lp-contact" id="contact"><div class="lp-twee"><div><h2>Verstuur je aanvraag</h2><p>Laat je datum en gegevens achter, dan hoor je dezelfde werkdag van me of de datum vrij is.</p>
<div class="lp-wie"><img src="img/maarten-adviseur.jpg" alt="Maarten Versteeg" loading="lazy" style="object-position:50% 20%"><div><b>Maarten Versteeg</b><span>Oprichter HEAR</span></div></div></div>
<div class="lp-form">
<label>Datum van je event<input name="datum" type="date" required></label>
<label>Naam<input name="naam" autocomplete="name" required></label>
<label>Organisatie<input name="organisatie" autocomplete="organization"></label>
<label>E-mail<input name="email" type="email" autocomplete="email" required></label>
<label>Telefoon<input name="telefoon" type="tel" autocomplete="tel"></label>
<label>Wensen of vragen<textarea name="bericht"></textarea></label>
<button type="submit">Verstuur aanvraag</button><p class="lp-privacy">We gebruiken je gegevens alleen om je te antwoorden. <a href="privacy.html">Privacyverklaring</a></p>
<p class="lp-melding" hidden></p></div></div></section>
</form></main>"""
    js = """<script>(function(){
var f=document.querySelector('.cs-form'),P=document.querySelector('.cs').dataset.prijzen==='1',stenen=document.getElementById('cs-stenen'),leeg=document.getElementById('cs-leeg'),som=document.getElementById('cs-som'),vd=document.getElementById('cs-voordeel'),ind=f.querySelector('[name=indicatie]');
var LICHT=[0,350,600,800];
__ISO_JS__
var toren=document.getElementById('cs-toren'),torenbeeld=document.getElementById('cs-toren-beeld');
function eur(n){return '\\u20ac\\u00a0'+String(n).replace(/\\B(?=(\\d{3})+$)/g,'.')}
var gr=document.getElementById('cs-grootte'),pers=f.querySelector('[name=personeel]');
function reken(){var g=gr.selectedIndex,k=[],t=0,nl=0,h='',pt=[];
 [].forEach.call(f.querySelectorAll('.cs-blok'),function(b){var i=b.querySelector('input');
  if(!i){var u=+document.getElementById('cs-'+b.dataset.veld).value,pr=b.querySelector('.cs-prijs'),som=u*b.dataset.tarief;b.classList.toggle('is-aan',u>0);
   if(pr)pr.textContent=u?(P?u+' uur: '+eur(som):u+' uur'):pr.dataset.tarief;
   if(u){k.push({naam:b.dataset.naam+', '+u+' uur',kleur:b.dataset.kleur});t+=som;pt.push(b.dataset.naam+' '+u+' uur')}return}
  if(i.dataset.staffel){i.dataset.prijs=i.dataset.staffel.split(',')[g];var ps=b.querySelector('.cs-prijs');if(ps)ps.textContent=eur(+i.dataset.prijs)}
  b.classList.toggle('is-aan',i.checked);if(!i.checked)return;k.push({naam:i.value,kleur:i.dataset.kleur});if(i.name==='licht')nl++;else t+=+i.dataset.prijs});
 pers.value=pt.join(', ');k.forEach(function(x){h='<li style="--k:'+x.kleur+'">'+x.naam+'</li>'+h});
 t+=LICHT[nl];stenen.innerHTML=h;leeg.hidden=k.length>0;toren.hidden=!k.length;torenbeeld.innerHTML=k.length?isoStapel(k.map(function(x){return x.kleur})):'';
 if(P){som.textContent=eur(t);var b=nl*350-LICHT[nl];vd.hidden=!b;vd.textContent=b?'Je bespaart '+eur(b)+' op licht en aankleding.':'';ind.value=k.length?'vanaf '+eur(t).replace('\\u00a0',' ')+' excl. btw':''}}
f.addEventListener('change',function(ev){var i=ev.target;if(i.matches&&i.matches('.cs-zin select')){reken();return}if(!i.matches||!i.matches('.cs-blok input'))return;
 if(i.checked&&i.dataset.groep)[].forEach.call(f.querySelectorAll('input[data-groep="'+i.dataset.groep+'"]'),function(o){if(o!==i)o.checked=false});reken()});
reken();
var m=f.querySelector('.lp-melding');f.addEventListener('submit',function(ev){if(!window.fetch)return;ev.preventDefault();var k=f.querySelector('button[type=submit]');k.disabled=true;
fetch(f.action,{method:'POST',body:new FormData(f),headers:{'Accept':'application/json'}}).then(function(r){return r.json()}).then(function(r){m.hidden=false;
if(r.ok){m.textContent=f.dataset.dank;[].forEach.call(f.querySelectorAll('.lp-form label,.lp-form button,.lp-privacy'),function(x){x.hidden=true})}else{m.textContent=f.dataset.fout;k.disabled=false}}).catch(function(){m.hidden=false;m.textContent=f.dataset.fout;k.disabled=false})});
})();</script>"""
    k = kop
    k = re.sub(r"<title>.*?</title>", f"<title>{e(TITEL)}</title>", k, count=1, flags=re.S)
    k = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(OMSCHR)}">', k, count=1)
    k = re.sub(r'<meta name="deeltitel" content="[^"]*">', "", k, count=1)
    k = re.sub(r"<!--og-->.*?<!--/og-->", "", k, flags=re.S)
    k = k.replace('<link rel="stylesheet" href="doelgroep.css">', '<link rel="stylesheet" href="doelgroep.css"><link rel="stylesheet" href="samenstellen.css">', 1)
    if "samenstellen.css" not in k or 'content="noindex' not in k:
        sys.exit("kop van nieuwjaarsborrel.html is veranderd: stylesheet of noindex niet gevonden")
    return k + main + js.replace('__ISO_JS__', ISO_JS) + utm_js + voet

for prijzen, naam in ((True, "samenstellen.html"), (False, "samenstellen-zonder-prijzen.html")):
    (site / naam).write_text(pagina(prijzen), encoding="utf-8")
print("samenstellen.html en samenstellen-zonder-prijzen.html gebouwd")
