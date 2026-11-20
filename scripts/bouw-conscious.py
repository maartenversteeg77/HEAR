#!/usr/bin/env python3
"""Demo (20 nov): landingspagina voor eventklanten van Conscious Hotels en Hotel V.
Vorm ('route 3', gekozen door Maarten op 20 nov): de foto blijft één foto; de blokjes zijn een eigen tekening,
schuin van boven met ronde noppen, in de kleuren van de samensteller. Ze staan bij de knop bovenaan, op elke bouwsteen
(wit, kleurt bij kiezen) en als stapel in 'Jouw event' die groeit met elke keuze. Geen puzzelvormen, geen foto in blokjes.
Twee varianten om te vergelijken: conscious-met-prijzen.html en conscious-zonder-prijzen.html.
De definitieve pagina komt op hear.nl/conscious zodra Maarten een variant kiest.
Kop, menu en voet komen uit site/nieuwjaarsborrel.html (draai dit script dus na bouw-doelgroepen).
Niet gelinkt vanaf de site, noindex."""
import pathlib, re, sys, html
site = pathlib.Path(__file__).resolve().parent.parent / "site"
basis = (site / "nieuwjaarsborrel.html").read_text(encoding="utf-8")
i = basis.index('<main class="wrap lp">')
kop = basis[:i]
voet = basis[basis.index('<footer class="actie-voet">'):]
utm_js = re.search(r'<script>\(function\(\)\{try\{var q=new URLSearchParams.*?</script>', basis, re.S)
if not utm_js:
    sys.exit("utm-script niet gevonden in nieuwjaarsborrel.html")
utm_js = utm_js.group(0)

TITEL = "Licht, geluid en dj voor je event bij Conscious Hotels of Hotel V | HEAR"
OMSCHR = "Stel in twee minuten licht, geluid en dj samen voor je event bij Conscious Hotels of Hotel V."

def e(t):
    return html.escape(t, quote=True)

# (groep, waarde in de mail, titel, ondertitel, prijs, 'vanaf'?)
GELUID = [
    ("Geluid voor spraak", "Met mengtafel en tot vier handmicrofoons", 500),
    ("Geluid voor muziek", "Met dj-booth en dj-gear", 600),
    ("Geluid voor muziek en spraak", "Voor een event met sprekers en een dj", 700),
]
PERSONEEL = [
    ("Geluidsman", "Bij spraakversterking voor een seminar of workshop", 400),
    ("Dj", "Voor je cocktail of feestavond", 600),
    ("Geluidsman en daarna dj", "Voor een event met sprekers en een dj", 800),
]
LICHT = [
    ("Sfeerlicht", "De ruimte in kleur"),
    ("Decoratie", "Led-tubes, spiegelbollen en props"),
    ("Dansvloerlicht", "Bewegend licht boven de dansvloer"),
]
SOORTEN = ["congres of seminar", "vergadering of training", "borrel of cocktailparty", "diner", "bedrijfsfeest",
           "productpresentatie", "bruiloft of privéfeest", "iets anders"]
# namen uit de brochure Conscious Meetings & Events (2023) en hotelv.com/en/groups/meetings-and-events
LOCATIES = ["Bar Kantoor (Conscious Hotel Westerpark)", "Moer (The Tire Station)", "The Vondel Bar (Conscious Hotel Vondelpark)",
            "The Private (Hotel V)", "The Palm (Hotel V)", "een vergaderruimte", "een andere ruimte of nog niet bekend"]

def eur(n):
    return "€ " + f"{n:,}".replace(",", ".")

def blok(naam, titel, sub, prijs, groep, soort, prijzen, vanaf=False, prijstekst=None):
    p = f'<span class="cs-prijs">{"vanaf " if vanaf else ""}{eur(prijs)}</span>' if prijzen and prijs else ""
    if prijzen and prijstekst:
        p = f'<span class="cs-prijs">{prijstekst}</span>'
    return (f'<label class="cs-blok cs-{soort}"><input type="checkbox" name="{naam}" value="{e(titel)}" data-groep="{groep}" data-prijs="{prijs or 0}" data-kleur="{KLEUR[soort]}">'
            f'<span class="cs-blok-in"><span class="cs-titel">{titel}</span><span class="cs-sub">{sub}</span>{p}'
            f'{iso_stapel([KLEUR["wit"]], 30, 2.2, "cs-ic cs-ic-uit")}{iso_stapel([KLEUR[soort]], 30, 2.2, "cs-ic cs-ic-aan")}</span></label>')

# Blokjes, schuin van boven getekend met ronde noppen (20 nov, 'route 3'). Eigen tekening, in de kleuren van de samensteller.
# Dezelfde tekening staat in het script onderaan de pagina (functie isoStapel) voor de stapel die groeit; houd beide gelijk.
KLEUR = {"geluid": "#D47763", "personeel": "#7AC3C9", "licht": "#E9D36B", "scherm": "#C9C8C2", "wit": "#F6F5F1"}
HOOFDBEELD = ("img/case-prive-breed.jpg", "50% 88%", "Gasten op de dansvloer in een zaal met gekleurd licht en ballonnen")

def _tint(kleur, f):
    n = int(kleur[1:], 16)
    return "rgb(%d,%d,%d)" % tuple(round(v * f) for v in (n >> 16, (n >> 8) & 255, n & 255))

def iso_stapel(kleuren, u=40, dik=2, klasse=""):
    """SVG van op elkaar gestapelde blokjes (2 x 2 noppen), onderste eerst."""
    c, s_, h = 0.866, 0.5, u * 0.9
    W = D = 2 * u
    rr = u * 0.29
    rx, ry, sh = rr * 1.2247, rr * 0.7071, u * 0.2
    st = f'stroke="#191A19" stroke-width="{dik}" stroke-linejoin="round"'
    g = ""
    for i, k in enumerate(kleuren):
        z = i * h
        P = lambda x, y, zz: ((x - y) * c, (x + y) * s_ - zz - z)
        pts = lambda a: " ".join(f"{px:.1f},{py:.1f}" for px, py in a)
        g += (f'<polygon points="{pts([P(0, D, h), P(W, D, h), P(W, D, 0), P(0, D, 0)])}" fill="{_tint(k, .86)}" {st}/>'
              f'<polygon points="{pts([P(W, D, h), P(W, 0, h), P(W, 0, 0), P(W, D, 0)])}" fill="{_tint(k, .72)}" {st}/>'
              f'<polygon points="{pts([P(0, 0, h), P(W, 0, h), P(W, D, h), P(0, D, h)])}" fill="{k}" {st}/>')
        for a, b in sorted(((a, b) for a in (0, 1) for b in (0, 1)), key=lambda q: q[0] + q[1]):
            px, py = P((a + .5) * u, (b + .5) * u, h)
            g += (f'<path d="M{px - rx:.1f},{py - sh:.1f}V{py:.1f}A{rx:.1f},{ry:.1f} 0 0 0 {px + rx:.1f},{py:.1f}V{py - sh:.1f}Z" fill="{_tint(k, .8)}" {st}/>'
                  f'<ellipse cx="{px:.1f}" cy="{py - sh:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{k}" {st}/>')
    x0, x1 = -D * c - 3, W * c + 3
    y0, y1 = -h - (len(kleuren) - 1) * h - sh - ry - 3, (W + D) * s_ + 3
    return f'<svg class="{klasse}" viewBox="{x0:.1f} {y0:.1f} {x1 - x0:.1f} {y1 - y0:.1f}" aria-hidden="true" focusable="false">{g}</svg>'

def pagina(prijzen):
    variant = "met prijzen" if prijzen else "zonder prijzen"
    geluid = "".join(blok("geluid", t, s, p, "geluid", "geluid", prijzen) for t, s, p in GELUID)
    scherm = blok("scherm", "Ledscherm", "Voor presentatie of visuals, meerdere schermen mogelijk", 150, "", "scherm", prijzen, vanaf=True)
    personeel = "".join(blok("personeel", t, s, p, "personeel", "personeel", prijzen) for t, s, p in PERSONEEL)
    licht = "".join(blok("licht", t, s, None, "", "licht", prijzen) for t, s in LICHT)
    logo = blok("logo", "Ledscherm met logo", "Je logo groot in beeld", None, "", "licht", prijzen, prijstekst="op aanvraag")
    lichtprijs = '<p class="cs-noot">Sfeerlicht, decoratie en dansvloerlicht: één onderdeel € 350, twee € 600, alle drie € 800.</p>' if prijzen else ""
    totaal = ('<p class="cs-totaal"><span>Vanaf</span><b id="cs-som">€ 0</b><small>exclusief btw</small></p><p class="cs-voordeel" id="cs-voordeel" hidden></p>'
              if prijzen else '<p class="cs-totaal cs-zonder"><span>Je hoort dezelfde werkdag wat dit kost.</span></p>')
    main = f"""<main class="wrap lp cs" data-prijzen="{1 if prijzen else 0}">
<section class="casehead"><h1 class="kernzin">Jouw event bij Conscious Hotels of Hotel V</h1></section>
<div class="lp-held cs-held"><div class="cs-foto"><img src="{HOOFDBEELD[0]}" alt="{e(HOOFDBEELD[2])}" style="object-position:{HOOFDBEELD[1]}"><a class="cs-samen" href="#bouwstenen">{iso_stapel([KLEUR["geluid"], KLEUR["personeel"], KLEUR["licht"]], 40, 2)}<b>Stel je<br>event samen</b><i aria-hidden="true">→</i></a></div></div>
<section class="lp-band"><div class="lp-twee"><p class="lp-lead">Leuk dat je bij Conscious Hotels of Hotel V een event organiseert.</p><div class="lp-tekst"><p>Of het nou om een congres gaat, een cocktailparty met dj of misschien wel beide: wij verzorgen het voor je van A tot Z.</p><p>Vul hier je aanvraag in twee minuten in.</p><p class="cs-hulp"><a class="wa" href="https://wa.me/31624560220?text=Hoi%20Maarten%2C%20ik%20heb%20een%20vraag%20over%20mijn%20event%20bij%20Conscious%20Hotels%20of%20Hotel%20V." target="_blank" rel="noopener"><span>Weet je niet wat je moet invullen? Stuur me een appje</span><i aria-hidden="true">→</i></a></p></div></div></section>
<form class="cs-form" method="post" action="/api/aanvraag" data-dank="Dank je. Je hoort dezelfde werkdag van me." data-fout="Versturen lukte niet. Mail naar maarten@hear.nl of bel +31 6 24560220.">
<input type="hidden" name="bron" value="Landingspagina Conscious ({variant})"><input type="hidden" name="utm" value=""><input type="hidden" name="indicatie" value=""><input type="text" name="website" class="lp-hp" tabindex="-1" autocomplete="off" aria-hidden="true">
<section class="lp-band cs-bouw" id="bouwstenen"><div class="cs-kolommen"><div class="cs-keuzes">
<fieldset class="cs-stap cs-zin"><legend class="lp-strip">Je event</legend>
<label class="cs-kies"><span>Ik organiseer een</span><select name="soort">{"".join(f"<option>{e(x)}</option>" for x in SOORTEN)}</select></label>
<label class="cs-kies"><span>in</span><select name="locatie">{"".join(f"<option>{e(x)}</option>" for x in LOCATIES)}</select></label>
<label class="cs-kies cs-gasten"><span>voor</span><input name="gasten" type="number" min="1" inputmode="numeric" aria-label="Aantal gasten"><span>gasten</span></label>
</fieldset>
<fieldset class="cs-stap"><legend class="lp-strip">Kies de bouwstenen van je event</legend>
<h3 class="cs-groep">Geluid</h3><p class="cs-intro">Hoogwaardig geluid, afgestemd op de ruimte.</p>
<div class="cs-blokken">{geluid}{scherm}</div>
<p class="cs-noot">Meer dan vier sprekers of reversmicrofoons, bijvoorbeeld voor een rondetafelgesprek: op aanvraag.</p>
<h3 class="cs-groep">Personeel</h3>
<div class="cs-blokken">{personeel}</div>
<p class="cs-noot">Bij alleen muziek regelt de dj het geluid zelf.</p>
<h3 class="cs-groep">Licht en aankleding</h3>
<div class="cs-blokken">{licht}{logo}</div>{lichtprijs}
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
function tint(k,f){var n=parseInt(k.slice(1),16);return 'rgb('+[n>>16,(n>>8)&255,n&255].map(function(v){return Math.round(v*f)}).join(',')+')'}
function isoStapel(kl){var u=40,c=0.866,s=0.5,h=u*0.9,W=2*u,D=2*u,rr=u*0.29,rx=rr*1.2247,ry=rr*0.7071,sh=u*0.2,st='stroke="#191A19" stroke-width="2" stroke-linejoin="round"',g='';
 kl.forEach(function(k,i){var z=i*h;function P(x,y,zz){return [(x-y)*c,(x+y)*s-zz-z]}function pts(a){return a.map(function(p){return p[0].toFixed(1)+','+p[1].toFixed(1)}).join(' ')}
  g+='<polygon points="'+pts([P(0,D,h),P(W,D,h),P(W,D,0),P(0,D,0)])+'" fill="'+tint(k,.86)+'" '+st+'/><polygon points="'+pts([P(W,D,h),P(W,0,h),P(W,0,0),P(W,D,0)])+'" fill="'+tint(k,.72)+'" '+st+'/><polygon points="'+pts([P(0,0,h),P(W,0,h),P(W,D,h),P(0,D,h)])+'" fill="'+k+'" '+st+'/>';
  [[0,0],[0,1],[1,0],[1,1]].forEach(function(q){var p=P((q[0]+.5)*u,(q[1]+.5)*u,h);g+='<path d="M'+(p[0]-rx)+','+(p[1]-sh)+'V'+p[1]+'A'+rx+','+ry+' 0 0 0 '+(p[0]+rx)+','+p[1]+'V'+(p[1]-sh)+'Z" fill="'+tint(k,.8)+'" '+st+'/><ellipse cx="'+p[0]+'" cy="'+(p[1]-sh)+'" rx="'+rx+'" ry="'+ry+'" fill="'+k+'" '+st+'/>'})});
 var x0=-D*c-3,x1=W*c+3,y0=-h-(kl.length-1)*h-sh-ry-3,y1=(W+D)*s+3;return '<svg viewBox="'+x0+' '+y0+' '+(x1-x0)+' '+(y1-y0)+'" aria-hidden="true" focusable="false">'+g+'</svg>'}
var toren=document.getElementById('cs-toren'),torenbeeld=document.getElementById('cs-toren-beeld');
function eur(n){return '\\u20ac\\u00a0'+String(n).replace(/\\B(?=(\\d{3})+$)/g,'.')}
function reken(){var k=[].slice.call(f.querySelectorAll('.cs-blok input:checked')),t=0,nl=0,vanaf=false,h='';
 k.forEach(function(i){if(i.name==='licht')nl++;else t+=+i.dataset.prijs;h='<li style="--k:'+i.dataset.kleur+'">'+i.value+'</li>'+h});
 t+=LICHT[nl];stenen.innerHTML=h;leeg.hidden=k.length>0;toren.hidden=!k.length;torenbeeld.innerHTML=k.length?isoStapel(k.map(function(i){return i.dataset.kleur})):'';
 [].forEach.call(f.querySelectorAll('.cs-blok'),function(b){b.classList.toggle('is-aan',b.querySelector('input').checked)});
 if(P){som.textContent=eur(t);var b=nl*350-LICHT[nl];vd.hidden=!b;vd.textContent=b?'Je bespaart '+eur(b)+' op licht en aankleding.':'';ind.value=k.length?'vanaf '+eur(t).replace('\\u00a0',' ')+' excl. btw':''}}
f.addEventListener('change',function(ev){var i=ev.target;if(!i.matches||!i.matches('.cs-blok input'))return;
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
    k = k.replace('<link rel="stylesheet" href="doelgroep.css">', '<link rel="stylesheet" href="doelgroep.css"><link rel="stylesheet" href="conscious.css">', 1)
    if "conscious.css" not in k or 'content="noindex' not in k:
        sys.exit("kop van nieuwjaarsborrel.html is veranderd: stylesheet of noindex niet gevonden")
    return k + main + js + utm_js + voet

for prijzen, naam in ((True, "conscious-met-prijzen.html"), (False, "conscious-zonder-prijzen.html")):
    (site / naam).write_text(pagina(prijzen), encoding="utf-8")
print("conscious-met-prijzen.html en conscious-zonder-prijzen.html gebouwd")
