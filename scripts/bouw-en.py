"""Bouwt de Engelse pagina's in site/en/ uit de Nederlandse pagina's en content/en.json.
Elke Nederlandse tekst in en.json moet letterlijk in de bronpagina staan; anders stopt het script
met een melding, zodat NL en EN niet uit elkaar kunnen lopen.
Ook: vorige/volgende-links op de casepagina's (NL én EN) uit de volgorde van cases.json.
Draaien na elke wijziging aan een vertaalde pagina: python3 scripts/bouw-en.py"""
import json, re, html, pathlib, sys
root = pathlib.Path(__file__).resolve().parent.parent
site = root / "site"; out = site / "en"; out.mkdir(exist_ok=True)
en = json.loads((root / "content" / "en.json").read_text())
cases = json.loads((site / "cases.json").read_text())
vertaald = set(en["vertaald"])
e = lambda t: html.escape(t, quote=True)
AAN = ' class="aan" aria-current="page"'
fouten = []

# --- vorige/volgende op casepagina's, uit cases.json (NL), radio-mixes achteraan ---
keten = [c for c in cases["cases"] if c.get("status") == "af"]
keten.append({"link": "radio-mixes.html", "titel": "Radio-mixes voor Deep Radio", "titel_en": "Radio mixes for Deep Radio"})
def kort(c, taal):
    t = (c.get("titel_en") if taal == "en" else c["titel"]) or c["titel"]
    return t.replace("\n", " ")
def zijnav(i, taal):
    v, n = keten[i - 1], keten[(i + 1) % len(keten)]
    bollen = "".join(f'<a href="{it["link"]}" title="{e(kort(it, taal))}"{AAN if k == i else ""}></a>' for k, it in enumerate(keten))
    return (f'<nav class="zijnav" aria-label="Andere cases"><a class="pijl" href="{v["link"]}" title="{e(kort(v, taal))}" aria-label="Vorige: {e(kort(v, taal))}">←</a>'
            f'<span class="bollen">{bollen}</span><a class="pijl" href="{n["link"]}" title="{e(kort(n, taal))}" aria-label="Volgende: {e(kort(n, taal))}">→</a></nav>')
def plaats_zijnav(s, i, taal):
    s = re.sub(r'<nav class="bottomnav">.*?</nav>', '', s, flags=re.S)
    s = re.sub(r'<nav class="zijnav"[^>]*>.*?</nav>', '', s, flags=re.S)
    kr = f'<a class="crumb" href="cases.html"><span class="sectie">Cases</span><span class="scheiding" aria-hidden="true">|</span><span class="huidig">{e(kort(keten[i], taal))}</span></a>'
    return re.sub(r'<section class="casehead">\s*<a class="crumb"[^>]*>.*?</a>', lambda m: '<section class="casehead">' + kr + zijnav(i, taal), s, count=1, flags=re.S)
for i, c in enumerate(keten):
    p = site / c["link"]; s = p.read_text()
    s2 = plaats_zijnav(s, i, "nl")
    if s2 != s: p.write_text(s2)

# --- paden herschrijven voor /en/ ---
def paden(s, naam):
    def href(m):
        h = m.group(1)
        if h.startswith(("http", "mailto:", "#", "/")): return m.group(0)
        basis, _, anker = h.partition("#")
        if basis.endswith(".html"):
            doel = f"/en/{basis}" if basis in vertaald else f"/{basis}"
            return f'href="{doel}{"#" + anker if anker else ""}"'
        if h.startswith("nieuws/"): return f'href="/en/{h}"'
        return f'href="/{h}"'
    s = re.sub(r'href="([^"]+)"', href, s)
    s = s.replace('href="/nieuws/', 'href="/en/nieuws/')
    s = re.sub(r'src="(?!http|/)([^"]+)"', r'src="/\1"', s)
    s = s.replace("fetch('cases.json')", "fetch('/cases.json')")
    # taalwissel: terug naar NL
    s = re.sub(r'<a class="taal"[^>]*>EN</a>', f'<a class="taal" href="/{naam}" lang="nl" hreflang="nl" aria-label="Schakel naar Nederlands">NL</a>', s)
    # hreflang-links in head
    s = s.replace("</title>", f'</title><link rel="alternate" hreflang="nl" href="/{naam}"><link rel="alternate" hreflang="en" href="/en/{naam}">', 1)
    return s


import urllib.parse
def wa_en(s):
    def r(m):
        nl = urllib.parse.unquote(m.group(1))
        return "wa.me/?text=" + urllib.parse.quote(en.get("whatsapp", {}).get(nl, "Hi Maarten, I have a question about HEAR."))
    return re.sub(r'wa\.me/\?text=([^"]*)', r, s)

def vertaal(s, paren, naam, verplicht=True):
    for nl, eng in paren:
        if nl not in s:
            if verplicht: fouten.append(f"{naam}: niet gevonden: {nl[:70]}")
            continue
        s = s.replace(nl, eng)
    return s

for naam in en["vertaald"]:
    s = (site / naam).read_text()
    s = vertaal(s, en["globaal"], naam, verplicht=False)
    s = vertaal(s, en["paginas"].get(naam, []), naam)
    if naam == "cases.html":
        # tegels opnieuw uit cases.json met EN-velden
        dg = cases["doelgroepen"]
        def tegel(c):
            pos = f' style="object-position:{e(c["positie"])}"' if c.get("positie") else ""
            labels = "".join(f'<a href="{e(dg[k]["link"])}">{e(dg[k].get("naam_en", dg[k]["naam"]))}</a>' for k in c["doelgroepen"])
            return (f'<article class="case-tegel"><div class="case-beeld"><img src="{e(c["beeld"])}" alt="{e(c["alt"])}" loading="lazy"{pos}><span class="bekijk-case">View the case <i aria-hidden="true">→</i></span></div>'
                    f'<div class="case-tekst"><p class="labels">{labels}</p>'
                    f'<h2><a class="tegel-link" href="{e(c["link"])}">{e(c.get("titel_en", c["titel"]))}</a></h2>'
                    f'<p>{e(c.get("tekst_en", c["tekst"]))}</p><span class="pijl" aria-hidden="true">→</span></div></article>')
        tegels = "".join(tegel(c) for c in cases["cases"] if c.get("status") == "af")
        s = re.sub(r'<section class="case-overzicht">.*?</section>', lambda m: f'<section class="case-overzicht">{tegels}</section>', s, count=1, flags=re.S)
    # vorige/volgende in het Engels
    for i, c in enumerate(keten):
        if c["link"] == naam:
            s = plaats_zijnav(s, i, "en")
    s = paden(s, naam)
    s = wa_en(s)
    (out / naam).write_text(s)
    print("ok en/" + naam)

for naam in en["vertaald"]:
    p = site / naam; s = p.read_text()
    s2 = re.sub(r'<a class="taal" href="[^"]*"', f'<a class="taal" href="/en/{naam}"', s, count=1)
    if s2 != s: p.write_text(s2)

if fouten:
    print("\nNIET VERTAALD (NL-tekst gewijzigd?):"); print("\n".join(fouten)); sys.exit(1)
