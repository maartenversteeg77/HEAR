#!/usr/bin/env python3
"""Bouwt site/sitemap.xml en site/robots.txt (9 nov).
Alleen indexeerbare pagina's (geen noindex, geen doorverwijspagina), op het eindadres zonder .html."""
import pathlib, re
site = pathlib.Path(__file__).resolve().parent.parent / "site"
BASIS = "https://hear.nl"
OVERSLAAN = {"coffeecuts.html"}
urls = []
for p in sorted(site.rglob("*.html")):
    rel = p.relative_to(site).as_posix()
    if p.name in OVERSLAAN: continue
    s = p.read_text(encoding="utf-8", errors="ignore")
    if re.search(r'name="robots" content="[^"]*noindex', s): continue
    m = re.search(r'<link rel="canonical" href="([^"]+)"', s)
    if not m: continue
    urls.append(m.group(1))
urls = sorted(set(urls), key=lambda u: (u.count("/en/"), u))
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n"
(site / "sitemap.xml").write_text(xml, encoding="utf-8")
(site / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASIS}/sitemap.xml\n", encoding="utf-8")
print(len(urls), "adressen in sitemap.xml")
