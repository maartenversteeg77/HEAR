"""Bouwt het casesoverzicht (site/cases.html) uit site/cases.json.
Eén bron: titels, labels, teksten en beelden pas je aan in cases.json; daarna dit script draaien.
Alleen cases met status 'af' komen in het overzicht, in de volgorde van cases.json."""
import json, html, re, pathlib
site = pathlib.Path(__file__).resolve().parent.parent / "site"
data = json.loads((site / "cases.json").read_text())
e = lambda t: html.escape(t, quote=True)
tegels = "".join(
    f'<a class="case-tegel" href="{e(c["link"])}"><img src="{e(c["beeld"])}" alt="{e(c["alt"])}" loading="lazy"{(' style="object-position:'+e(c["positie"])+'"') if c.get("positie") else ""}>'
    f'<div class="case-tekst"><span class="label">{e(c["label"])}</span><h2>{e(c["titel"])}</h2>'
    f'<p>{e(c["tekst"])}</p><span class="pijl" aria-hidden="true">→</span></div></a>'
    for c in data["cases"] if c.get("status") == "af")
p = site / "cases.html"
s = p.read_text()
s, n = re.subn(r'<section class="[^"]*(?:case-index-grid|case-overzicht)[^"]*">.*?</section>',
               lambda m: f'<section class="case-overzicht"><!-- gegenereerd uit cases.json door scripts/bouw-cases.py -->{tegels}</section>',
               s, count=1, flags=re.S)
p.write_text(s)
print("tegels:", tegels.count("case-tegel"), "vervangen:", n)
