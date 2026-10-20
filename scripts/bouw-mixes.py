"""Bouwt site/dj-mixes.html: alle SoundCloud-sets van Maarten, ingeframed, uit content/mixes.json.
Niet in het menu; gelinkt vanaf de dj-pagina (artiesten.html). Kop en voet uit index.html. Draaien vóór bouw-en.py."""
import json, pathlib, html, urllib.parse
root = pathlib.Path(__file__).resolve().parent.parent
site = root / "site"
idx = (site / "index.html").read_text()
kop = idx[idx.index('<header class="top">'):idx.index('</script>') + 9]
voet = idx[idx.index('<footer class="voet">'):idx.index('</footer>') + 9]
e = lambda t: html.escape(t, quote=True)
data = json.loads((root / "content" / "mixes.json").read_text())

TITEL = "Dj-mixes"
INTRO = "Alle dj-sets op SoundCloud: soulful house, deephouse, afro, latin, disco en garage. Please enjoy!"
KLASSIEK = "Classic vinyl mixes"
KLASSIEK_TEKST = "Livesets van vroeger, alleen met platen gedraaid."

def speler(s):
    src = "https://w.soundcloud.com/player/?url=" + urllib.parse.quote(s["url"], safe="") + "&color=%23D47763&auto_play=false&hide_related=true&show_comments=false&show_user=false&show_reposts=false&show_teaser=false&visual=true"
    jaar = f' <span class="jaar">{e(s["jaar"])}</span>' if s.get("jaar") else ""
    return (f'<figure class="mix"><iframe title="{e(s["titel"])}" width="100%" height="240" scrolling="no" frameborder="no" allow="autoplay" loading="lazy" src="{src}"></iframe>'
            f'<figcaption>{e(s["titel"])}{jaar}</figcaption></figure>')

recent = [s for s in data["sets"] if not s.get("klassiek")]
klassiek = [s for s in data["sets"] if s.get("klassiek")]
main = f'''<main class="wrap">
<section class="casehead"><a class="crumb" href="artiesten.html"><span class="sectie">Producten</span><span class="scheiding" aria-hidden="true">|</span><span class="huidig">Dj's</span></a><h1>{e(TITEL)}</h1><p class="lead">{e(INTRO)}</p></section>
<section class="mixen" aria-label="Sets">{"".join(speler(s) for s in recent)}</section>
<section class="mixen klassiek" aria-label="{e(KLASSIEK)}"><h2 class="kopje">{e(KLASSIEK)}</h2><p class="mixen-uitleg">{e(KLASSIEK_TEKST)}</p>{"".join(speler(s) for s in klassiek)}</section>
<nav class="verwijzingen" aria-label="Verder"><a href="artiesten.html">← Dj's, vocalisten en instrumentalisten</a><a href="https://soundcloud.com/maartenversteeg" target="_blank" rel="noopener">Volg op SoundCloud ↗</a></nav>
</main>'''
doc = f'''<!doctype html><html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{e(INTRO)}"><title>{e(TITEL)} · HEAR</title><link rel="stylesheet" href="home.css"><link rel="stylesheet" href="styles.css"></head><body class="pagina">
{kop}
{main}
{voet}
</body></html>'''
(site / "dj-mixes.html").write_text(doc)
print(f"ok dj-mixes.html ({len(recent)} sets, {len(klassiek)} klassiek)")
