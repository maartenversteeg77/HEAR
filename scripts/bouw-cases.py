"""Bouwt het casesoverzicht (site/cases.html) uit site/cases.json, met filter op toepassing.
Eén bron: titels, toepassingen, teksten en beelden pas je aan in cases.json; daarna dit script draaien
(en bouw-en.py voor de Engelse versie, die tegels() hieruit hergebruikt).
Alleen cases met status 'af' komen in het overzicht, in de volgorde van cases.json.
toepassing = soort werk (label + filter). nieuws=true: tegel linkt naar een nieuwsbericht."""
import json, html, re, pathlib
site = pathlib.Path(__file__).resolve().parent.parent / "site"
data = json.loads((site / "cases.json").read_text())
TP = data["toepassingen"]
e = lambda t: html.escape(t, quote=True)
lbl = lambda c: f'<img class="werk-label" src="{c["label"]}" alt="">' if c.get("label") else ""
def tegels(taal="nl"):
    en = taal == "en"; v = lambda c, k: (c.get(k + "_en") if en else None) or c[k]
    gebruikt = [k for k in TP if any(k in c.get("toepassing", []) for c in data["cases"] if c.get("status") == "af")]
    filt = ('<nav class="case-filter" aria-label="' + ("Filter by type" if en else "Filter op soort werk") + '">'
            + f'<button type="button" data-f="" class="aan">{"All" if en else "Alles"}</button>'
            + "".join(f'<button type="button" data-f="{k}">{e(TP[k]["naam_en"] if en else TP[k]["naam"])}</button>' for k in gebruikt) + '</nav>')
    out = ""
    af = [c for c in data["cases"] if c.get("status") == "af"]
    af = sorted([c for c in af if c.get("datum")], key=lambda c: c["datum"], reverse=True) + [c for c in af if not c.get("datum")]
    for c in af:
        pos = f' style="object-position:{e(c["positie"])}"' if c.get("positie") else ""
        t = c.get("toepassing", [])
        labels = "".join(f'<span>{e(TP[k]["naam_en"] if en else TP[k]["naam"])}</span>' for k in t)
        bek = ("Read the post" if en else "Lees het bericht") if c.get("nieuws") else ("View the case" if en else "Bekijk de case")
        ext = c.get("extern"); pl = "↗" if ext else "→"
        if ext: bek = ("Read on maartenversteeg.nl" if en else "Lees op maartenversteeg.nl")
        doel = ' target="_blank" rel="noopener"' if ext else ""
        out += (f'<article class="case-tegel" data-t="{" ".join(t)}"><div class="case-beeld"><img src="{e(c["beeld"])}" alt="{e(c["alt"])}" loading="lazy"{pos}>{lbl(c)}<span class="bekijk-case">{bek} <i aria-hidden="true">{pl}</i></span></div>'
                f'<div class="case-tekst"><p class="labels">{labels}</p>'
                f'<h2><a class="tegel-link" href="{e(c["link"])}"{doel}>{e(v(c, "titel"))}{"<span class=\"vh\"> (" + ("opens in a new window" if en else "opent in een nieuw venster") + ")</span>" if ext else ""}</a></h2>'
                f'<p>{e(v(c, "tekst"))}</p><span class="pijl" aria-hidden="true">{pl}</span></div></article>')
    js = ("<script>(function(){var b=document.querySelectorAll('.case-filter button'),t=document.querySelectorAll('.case-overzicht .case-tegel');"
          "function zet(f){b.forEach(function(x){x.classList.toggle('aan',x.dataset.f===f)});t.forEach(function(x){x.hidden=!!f&&(' '+x.dataset.t+' ').indexOf(' '+f+' ')<0});}"
          "b.forEach(function(x){x.addEventListener('click',function(){zet(x.dataset.f);history.replaceState(null,'',x.dataset.f?'#'+x.dataset.f:location.pathname)})});"
          "var h=location.hash.slice(1);if(h&&document.querySelector('.case-filter [data-f=\"'+h+'\"]'))zet(h);})();</script>")
    return filt, out, js
def plaats(s, taal):
    filt, out, js = tegels(taal)
    s = re.sub(r'<nav class="case-filter".*?</nav>', '', s, flags=re.S)
    s = re.sub(r'<script>\(function\(\)\{var b=document.querySelectorAll\(\'\.case-filter button\'\).*?</script>', '', s, flags=re.S)
    s, n = re.subn(r'<section class="[^"]*(?:case-index-grid|case-overzicht)[^"]*">.*?</section>',
                   lambda m: f'{filt}<section class="case-overzicht"><!-- gegenereerd uit cases.json door scripts/bouw-cases.py -->{out}</section>{js}',
                   s, count=1, flags=re.S)
    return s, n
if __name__ == "__main__":
    p = site / "cases.html"
    s, n = plaats(p.read_text(), "nl")
    p.write_text(s)
    print("tegels:", s.count("case-tegel\""), "vervangen:", n)
