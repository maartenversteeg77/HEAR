"""Controleert of elke class die in site/*.html voorkomt ergens in de CSS staat.
Vangt het per ongeluk verdwijnen van CSS-regels (zoals .structuur op 17 okt). Draaien: python3 scripts/check-css.py"""
import re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent / "site"
css = "\n".join(f.read_text() for f in root.glob("*.css"))
# ook classes die alleen in JS worden gezet (jog.js) tellen als bekend
js = "\n".join(f.read_text() for f in root.glob("*.js"))
bekend = set(re.findall(r"\.([a-zA-Z][\w-]*)", css))
los = {}
for f in list(root.glob("*.html")) + list(root.glob("*/*.html")):
    s = f.read_text()
    for m in re.finditer(r'class="([^"]+)"', s):
        for c in m.group(1).split():
            if c not in bekend and c not in js:
                los.setdefault(c, set()).add(f.name)
if los:
    for c, fs in sorted(los.items()): print(f"ONBEKEND .{c}: {', '.join(sorted(fs)[:4])}")
else:
    print("ok: alle classes hebben CSS")
