"""Zet favicon- en apple-touch-links in de head van alle pagina's (11 nov). Draaien na bouw-nieuws/bouw-en, vóór bouw-sitemap."""
import pathlib, re
site = pathlib.Path(__file__).resolve().parent.parent / "site"
TAGS = ('<!--icoon--><link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">'
        '<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png"><!--/icoon-->')
n = 0
for p in site.rglob("*.html"):
    s = p.read_text()
    s2 = re.sub(r'<!--icoon-->.*?<!--/icoon-->', '', s, flags=re.S)
    if '<meta charset="utf-8">' not in s2: print("geen charset:", p); continue
    s2 = s2.replace('<meta charset="utf-8">', '<meta charset="utf-8">' + TAGS, 1)
    if s2 != s: p.write_text(s2); n += 1
print("ok icoon", n)
