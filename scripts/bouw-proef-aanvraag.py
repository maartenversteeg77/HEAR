#!/usr/bin/env python3
"""Proef (20 nov): het aanvraagformulier van de site met twee ingangen.
  1. 'Ik plan een briefinggesprek'  -> het bestaande formulier (aanvraag.html), ongewijzigd.
  2. 'Ik weet al wat ik nodig heb'  -> zelf samenstellen met blokjes: wie je bent, het soort event, dan alle bouwstenen. Zonder prijzen.
Bouwt site/proef-aanvraag.html. Niet gelinkt vanaf de site, noindex; aanvraag.html blijft zoals hij is.
Kop, menu en voet komen uit site/index.html."""
import pathlib, sys, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from blokjes import KLEUR, iso_stapel, ISO_JS
site = pathlib.Path(__file__).resolve().parent.parent / "site"
idx = (site / "index.html").read_text(encoding="utf-8")
kop = idx[idx.index('<header class="top">'):idx.index('</script>') + 9]
voet = idx[idx.index('<footer class="voet">'):idx.index('</footer>') + 9]
icoon = idx[idx.index('<!--icoon-->'):idx.index('<!--/icoon-->') + len('<!--/icoon-->')]

def e(t):
    return html.escape(t, quote=True)

# de vier doelgroepen van de site, in de ik-vorm, plus 'anders'
IKBEN = ["eventmanager of communicatieprofessional", "van een merk, een creatief bureau of een agency", "organisator van een (dance) event",
         "eigenaar of exploitant van een eventlocatie", "iets anders, namelijk"]
# soorten events uit het bestaande formulier
SOORTEN = ["zakelijk (netwerk)event", "lezing of seminar", "personeelsfeest", "merkactivatie", "dance event", "iets anders, namelijk"]
# (groep, kleur, veldnaam, [bouwstenen]) – namen uit het bestaande formulier, aangevuld op 20 nov:
# ledschermen met VJ (bij het zakelijke deel), vocalist/percussionist/saxofonist elk apart, daarna de geuren-dj.
GROEPEN = [
    ("Geluid", "geluid", "diensten", ["Sprekersversterking en microfoons", "Geluid voor borrel of feest", "Dansvloer geluidsysteem",
                                      "Dj-booth en gear voor je eigen dj", "Technicus ter plekke"]),
    ("Licht en beeld", "licht", "diensten", ["Sfeerverlichting", "Theaterlicht voor product of spreker", "Videoschermen en presentatie",
                                             "Ledschermen met VJ", "Lichtshow", "Online uitzending"]),
    ("Dj's en artiesten", "personeel", "diensten", ["Dj", "Vocalist", "Percussionist", "Saxofonist", "Geuren-dj", "Playlist op maat", "Partyfotograaf"]),
    ("Communicatie rondom je event", "scherm", "communicatie", ["Communicatieadvies", "Uitnodigingen en andere middelen", "Speeches en presentaties",
                                                               "Bedrijfsvideo", "Aftermovie"]),
]

def blok(naam, titel, soort):
    return (f'<label class="cs-blok cs-kort"><input type="checkbox" name="{naam}" value="{e(titel)}" data-kleur="{KLEUR[soort]}">'
            f'<span class="cs-blok-in"><span class="cs-titel">{e(titel)}</span>'
            f'{iso_stapel([KLEUR["wit"]], 30, 2.2, "cs-ic cs-ic-uit")}{iso_stapel([KLEUR[soort]], 30, 2.2, "cs-ic cs-ic-aan")}</span></label>')

groepen = "".join(f'<h3 class="cs-groep">{e(g)}</h3><div class="cs-blokken">{"".join(blok(veld, t, soort) for t in items)}</div>'
                  for g, soort, veld, items in GROEPEN)
opties = lambda lijst: "".join(f"<option>{e(x)}</option>" for x in lijst)

pagina = f"""<!doctype html><html lang="nl"><head><meta charset="utf-8">{icoon}<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>HEAR · proef: plan je event</title>
<link rel="stylesheet" href="home.css"><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="doelgroep.css"><link rel="stylesheet" href="conscious.css"></head>
<body class="pagina">{kop}<main class="wrap lp cs" data-prijzen="0">
<section class="casehead"><h1 class="kernzin">Plan je event</h1></section>
<section class="lp-band pa-start"><div class="pa-keuzes">
<a class="pa-keuze" href="aanvraag.html"><span class="pa-kop">Ik plan een briefinggesprek</span><span class="pa-sub">Bel, Teams of Meet: vertel over je event</span><i aria-hidden="true">→</i></a>
<a class="pa-keuze pa-zelf" href="#samenstellen">{iso_stapel([KLEUR["geluid"], KLEUR["personeel"], KLEUR["licht"]], 40, 2)}<span class="pa-kop">Ik weet al wat ik nodig heb</span><span class="pa-sub">Stel je event zelf samen</span><i aria-hidden="true">→</i></a>
</div></section>
<form class="cs-form" method="post" action="/api/aanvraag" data-dank="Dank je. Je hoort dezelfde werkdag van me." data-fout="Versturen lukte niet. Mail naar maarten@hear.nl of bel +31 6 24560220.">
<input type="hidden" name="bron" value="Aanvraag met blokjes (proef)"><input type="hidden" name="utm" value=""><input type="text" name="website" class="lp-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<section class="lp-band cs-bouw" id="samenstellen" hidden><div class="cs-kolommen"><div class="cs-keuzes">
<fieldset class="cs-stap cs-zin"><legend class="lp-strip">Over jou en je event</legend>
<label class="cs-kies"><span>Ik ben</span><select name="rol" data-anders="rol_anders">{opties(IKBEN)}</select></label>
<input class="pa-anders" name="rol_anders" aria-label="Ik ben iets anders, namelijk" hidden>
<label class="cs-kies"><span>en organiseer een</span><select name="soort" data-anders="soort_anders">{opties(SOORTEN)}</select></label>
<input class="pa-anders" name="soort_anders" aria-label="Soort event, anders namelijk" hidden>
<label class="cs-kies cs-gasten"><span>voor</span><input name="gasten" type="number" min="1" inputmode="numeric" aria-label="Aantal gasten"><span>gasten</span></label>
</fieldset>
<fieldset class="cs-stap"><legend class="lp-strip">Kies de bouwstenen van je event</legend>
{groepen}
</fieldset></div>
<aside class="cs-stapel" aria-live="polite"><h2 class="cs-stapel-kop">Jouw event</h2><div class="cs-toren" id="cs-toren" hidden><span id="cs-toren-beeld"></span><ul class="cs-stenen" id="cs-stenen"></ul></div><p class="cs-leeg" id="cs-leeg">Kies je eerste bouwsteen.</p><p class="cs-totaal cs-zonder"><span>Je hoort dezelfde werkdag van me.</span></p><a class="cs-verder" href="#contact">Naar je gegevens <i aria-hidden="true">→</i></a></aside>
</div></section>
<section class="lp-band lp-contact" id="contact" hidden><div class="lp-twee"><div><h2>Verstuur je aanvraag</h2><p>Laat je datum en gegevens achter, dan hoor je dezelfde werkdag van me.</p>
<div class="lp-wie"><img src="img/maarten-adviseur.jpg" alt="Maarten Versteeg" loading="lazy" style="object-position:50% 20%"><div><b>Maarten Versteeg</b><span>Oprichter HEAR</span></div></div></div>
<div class="lp-form">
<label>Datum van je event<input name="datum" type="date"></label>
<label>Locatie<input name="locatie"></label>
<label>Naam<input name="naam" autocomplete="name" required></label>
<label>Organisatie<input name="organisatie" autocomplete="organization"></label>
<label>E-mail<input name="email" type="email" autocomplete="email" required></label>
<label>Telefoon<input name="telefoon" type="tel" autocomplete="tel"></label>
<label>Wil je verder nog iets kwijt?<textarea name="bericht"></textarea></label>
<button type="submit">Verstuur aanvraag</button><p class="lp-privacy">We gebruiken je gegevens alleen om je aanvraag te beantwoorden. <a href="privacy.html">Privacyverklaring</a></p>
<p class="lp-melding" hidden></p></div></div></section>
</form></main>
<script>(function(){{
{ISO_JS}
var f=document.querySelector('.cs-form'),bouw=document.getElementById('samenstellen'),contact=document.getElementById('contact'),stenen=document.getElementById('cs-stenen'),leeg=document.getElementById('cs-leeg'),toren=document.getElementById('cs-toren'),beeld=document.getElementById('cs-toren-beeld');
function open(){{bouw.hidden=contact.hidden=false;document.querySelector('.pa-zelf').classList.add('is-gekozen')}}
document.querySelector('.pa-zelf').addEventListener('click',open);if(location.hash==='#samenstellen'||location.hash==='#contact')open();
function reken(){{var k=[].slice.call(f.querySelectorAll('.cs-blok input:checked')),h='';
 k.forEach(function(i){{h='<li style="--k:'+i.dataset.kleur+'">'+i.value+'</li>'+h}});stenen.innerHTML=h;leeg.hidden=k.length>0;toren.hidden=!k.length;beeld.innerHTML=k.length?isoStapel(k.map(function(i){{return i.dataset.kleur}})):'';
 [].forEach.call(f.querySelectorAll('.cs-blok'),function(b){{b.classList.toggle('is-aan',b.querySelector('input').checked)}})}}
f.addEventListener('change',function(ev){{var i=ev.target;if(i.matches&&i.matches('.cs-blok input'))reken();
 if(i.dataset&&i.dataset.anders){{var a=f.querySelector('[name='+i.dataset.anders+']');a.hidden=i.value.indexOf('anders')<0;if(!a.hidden)a.focus()}}}});
reken();
var m=f.querySelector('.lp-melding');f.addEventListener('submit',function(ev){{if(!window.fetch)return;ev.preventDefault();var k=f.querySelector('button[type=submit]');k.disabled=true;
fetch(f.action,{{method:'POST',body:new FormData(f),headers:{{'Accept':'application/json'}}}}).then(function(r){{return r.json()}}).then(function(r){{m.hidden=false;
if(r.ok){{m.textContent=f.dataset.dank;[].forEach.call(f.querySelectorAll('.lp-form label,.lp-form button,.lp-privacy'),function(x){{x.hidden=true}})}}else{{m.textContent=f.dataset.fout;k.disabled=false}}}}).catch(function(){{m.hidden=false;m.textContent=f.dataset.fout;k.disabled=false}})}});
}})();</script>
{voet}</body></html>
"""
(site / "proef-aanvraag.html").write_text(pagina, encoding="utf-8")
print("proef-aanvraag.html gebouwd")
