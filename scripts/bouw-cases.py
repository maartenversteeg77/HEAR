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
def feiten(t):
    return '<span class="p-stip" aria-hidden="true"></span>'.join(f'<span>{e(x.strip())}</span>' for x in t.split("|"))
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
        tt = (v(c, "tegel_titel") if c.get("tegel_titel") else v(c, "titel")).replace(chr(10), " ")
        tk = v(c, "tegel_tekst") if c.get("tegel_tekst") else v(c, "tekst")
        out += (f'<article class="case-tegel poster" data-t="{" ".join(t)}"><div class="case-beeld"><img src="{e(c["beeld"])}" alt="{e(c["alt"])}" loading="lazy"{pos}>{lbl(c)}'
                f'<p class="p-chips">{labels}</p><div class="p-onder"><h2><a class="tegel-link" href="{e(c["link"])}"{doel}>{e(tt)}{"<span class=\"vh\"> (" + ("opens in a new window" if en else "opent in een nieuw venster") + ")</span>" if ext else ""} <i aria-hidden="true">{pl}</i></a></h2>'
                f'<p class="p-feiten">{feiten(tk)}</p></div></div></article>')
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

def werkrij(taal="nl"):
    """Statische carrousel 'Uitgelicht werk' en filterknoppen voor de homepage (eerder met script gevuld; nu leesbaar zonder JS)."""
    en = taal == "en"; v = lambda c, k: (c.get(k + "_en") if en else None) or c[k]
    af = [c for c in data["cases"] if c.get("status") == "af"]
    gebruikt = [k for k in TP if any(k in c.get("toepassing", []) for c in af)]
    filt = "".join(f'<a href="cases.html#{k}">{e(TP[k]["naam_en"] if en else TP[k]["naam"])}</a>' for k in gebruikt)
    kaarten = ""
    for c in af:
        if not c.get("uitgelicht"): continue
        pos = f' style="object-position:{e(c["positie"])}"' if c.get("positie") else ""
        lab = "".join(f'<span>{e(TP[k]["naam_en"] if en else TP[k]["naam"])}</span>' for k in c.get("toepassing", []))
        tt = (v(c, "tegel_titel") if c.get("tegel_titel") else v(c, "titel")).replace(chr(10), " ")
        tk = v(c, "tegel_tekst") if c.get("tegel_tekst") else v(c, "tekst")
        kaarten += (f'<a class="werk-kaart poster" href="{e(c["link"])}"><span class="werk-beeld"><img loading="lazy" src="{e(c["beeld"])}" alt="{e(c["alt"])}"{pos}>{lbl(c)}'
                    f'<span class="p-chips">{lab}</span><span class="p-onder"><h3>{e(tt)} <i aria-hidden="true">→</i></h3><span class="p-feiten">{feiten(tk)}</span></span></span></a>')
    return filt, kaarten
def plaats_werk(s, taal):
    filt, kaarten = werkrij(taal)
    s = re.sub(r'<nav class="werk-filter"([^>]*)>.*?</nav>', lambda m: f'<nav class="werk-filter"{m.group(1)}>{filt}</nav>', s, count=1, flags=re.S)
    s = re.sub(r'(<div class="werk-rij" id="werk-rij">).*?(<a class="werk-kaart werk-alle")', lambda m: m.group(1) + kaarten + m.group(2), s, count=1, flags=re.S)
    s = re.sub(r"fetch\('/?cases\.json'\)\.then.*?rij\.scrollLeft=0;\s*\}\);", "", s, count=1, flags=re.S)
    return s
if __name__ == "__main__":
    p = site / "cases.html"
    s, n = plaats(p.read_text(), "nl")
    p.write_text(s)
    print("tegels:", s.count("case-tegel\""), "vervangen:", n)
    ix = site / "index.html"; ix.write_text(plaats_werk(ix.read_text(), "nl"))
