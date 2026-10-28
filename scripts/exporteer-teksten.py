#!/usr/bin/env python3
"""Exporteert alle zichtbare tekst van de site (NL en EN naast elkaar) naar één Word-document
voor een redactieronde. Gebruik: python3 scripts/exporteer-teksten.py [uit.docx]

Per pagina een tabel: links NL, rechts EN, één rij per tekstblok (kop, alinea, bullet, knop).
WhatsApp-knoppen krijgen een extra rij met het vooringevulde bericht.
"""
import sys, re
from pathlib import Path
from urllib.parse import unquote, urlparse, parse_qs
from bs4 import BeautifulSoup
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / 'site'
UIT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / 'docs' / 'hear-teksten-redactieronde.docx'

# (bestand, label) in navigatievolgorde
PAGINAS = [
    ('index.html', 'Home'),
    ('doelgroepen.html', 'Voor wie (overzicht)'),
    ('corporate.html', 'Voor wie · Zakelijke events'),
    ('venue-owners.html', 'Voor wie · Bijzondere eventlocaties'),
    ('dance-events.html', 'Voor wie · Dance events'),
    ('diensten.html', 'Producten en diensten (overzicht)'),
    ('booth-dj-gear.html', 'Producten · Dj-gear'),
    ('high-end-audio.html', 'Producten · High-end audio'),
    ('atmospheric-lighting.html', 'Producten · Sfeerverlichting'),
    ('dancefloor-lighting.html', 'Producten · Dansvloerverlichting'),
    ('vintage-lighting.html', "Producten · 90's vintage licht"),
    ('av-as-a-service.html', 'Producten · Aankoopadvies licht en geluid'),
    ('artiesten.html', "Producten · Dj's, vocalisten en instrumentalisten"),
    ('special-projects.html', 'Producten · Custom dj-mix of playlist'),
    ('cases.html', 'Cases (overzicht)'),
    ('productpresentatie.html', 'Case · Productlancering'),
    ('gemeentelijk-netwerkevent.html', 'Case · Seminar / netwerkevent'),
    ('jubileum-ondernemersnetwerk.html', 'Case · Jubileum'),
    ('ade-dj.html', 'Case · Skatehal'),
    ('dj-sets.html', 'Case · 40 jaar'),
    ('systeemadvies.html', 'Case · Systeemadvies'),
    ('prive-event.html', 'Case · Privéfeest'),
    ('radio-mixes.html', 'Case · Radio mixes'),
    ('principes.html', 'Waarden en uitgangspunten'),
    ('over-hear.html', 'Over HEAR'),
    ('nieuws/index.html', 'Nieuws (overzicht)'),
    ('nieuws/twee-sets-808-515.html', 'Nieuws · Twee sets 808/515'),
    ('nieuws/kxm-25-a-floormonitor.html', 'Nieuws · KXM 25-A floormonitor'),
]

BLOK = ['h1', 'h2', 'h3', 'h4', 'p', 'li', 'figcaption', 'blockquote']
SKIP_CLASSES = {'crumb', 'pijl', 'eyebrow', 'page-kicker', 'sectie', 'scheiding', 'huidig', 'taal', 'taalknop'}


def tekst(el):
    return ' '.join(el.get_text(' ', strip=True).split())


def wa_bericht(href):
    if 'wa.me' not in href and 'whatsapp' not in href:
        return None
    q = parse_qs(urlparse(href).query)
    t = q.get('text', [''])[0]
    return unquote(t.replace('+', ' ')) if t else None


def blokken(html):
    """Lijst van (soort, tekst) in documentvolgorde uit header-nav, main en footer."""
    s = BeautifulSoup(html, 'html.parser')
    uit = []
    main = s.find('main') or s.body
    for el in main.find_all(BLOK + ['a', 'span']):
        cls = set(el.get('class') or [])
        if cls & SKIP_CLASSES:
            continue
        if el.name == 'span':
            if cls & {'bekijk-case', 'v-titel', 'bekijk-doel', 'bekijk'}:
                t = tekst(el).rstrip(' →')
                if t and (not uit or uit[-1] != ('knop', t)):
                    uit.append(('knop', t))
            continue
        if el.name == 'a':
            # alleen losse knoppen (niet in een p/li) en WhatsApp-berichten
            if el.find_parent(['p', 'li', 'h1', 'h2', 'h3', 'h4', 'figcaption']):
                continue
            if el.find(BLOK) or el.find('span', class_=lambda c: c in ('bekijk-case', 'v-titel', 'bekijk-doel')):
                continue
            t = tekst(el)
            if t and not re.fullmatch(r'[←→↗]+', t):
                uit.append(('knop', t))
            b = wa_bericht(el.get('href', ''))
            if b:
                uit.append(('whatsapp', b))
            continue
        if el.find(BLOK):  # container, kinderen komen apart
            continue
        t = tekst(el)
        if not t or re.fullmatch(r'[←→↗|]+', t):
            continue
        uit.append((el.name, t))
    # WhatsApp-berichten in links binnen alinea's
    for a in main.find_all('a', href=True):
        b = wa_bericht(a['href'])
        if b and ('whatsapp', b) not in uit:
            uit.append(('whatsapp', b))
    # jogwheel (waarden): tekst zit in window.JOG
    m = re.search(r'window\.JOG=\{.*?items:(\[.*?\])\};</script>', html, re.S)
    if m:
        import json
        for it in json.loads(m.group(1)):
            uit.append(('h2', it['titel']))
            uit.append(('p', it['statement']))
            uit.append(('p', it['intro']))
            for w in it.get('werkwijze', []):
                uit.append(('li', w))
    return [(s_, re.sub(r'\s+([,.;:])', r'\1', t_)) for s_, t_ in uit]


def slider(en=False):
    import json
    d = json.loads((SITE / 'cases.json').read_text(encoding='utf-8'))
    uit = [('p', '(slider, zelfde teksten als Cases-overzicht)' if not en else '(slider, same texts as Cases overview)')]
    for c in d['cases']:
        if c.get('status') != 'af':
            continue
        uit.append(('h3', ' '.join((c.get('titel_en') if en else c.get('titel', '')).split())))
        uit.append(('p', c.get('tekst_en') if en else c.get('tekst', '')))
    return uit


def globaal(html):
    """Menu, footer en titel: één keer opnemen."""
    s = BeautifulSoup(html, 'html.parser')
    uit = []
    t = s.find('title')
    if t:
        uit.append(('title', tekst(t)))
    gezien = set()
    for naam in ('header', 'footer'):
        for cont in s.find_all(naam):
            if cont.find_parent('main'):
                continue
            for el in cont.find_all(['a', 'p', 'li', 'h2', 'h3', 'span', 'small']):
                cls = set(el.get('class') or [])
                if cls & SKIP_CLASSES or el.find(['a', 'p', 'li', 'h2', 'h3', 'span', 'small']):
                    continue
                tx = tekst(el)
                if tx and not re.fullmatch(r'[←→↗|·]+', tx) and tx not in gezien:
                    gezien.add(tx)
                    uit.append((naam, tx))
    return uit


# ---------- Word ----------
def shade(cell, hexkleur):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), hexkleur)
    tcPr.append(shd)


def run_opmaak(p, t, soort):
    r = p.add_run(t)
    r.font.size = Pt(10)
    if soort in ('h1', 'h2', 'h3', 'h4', 'title'):
        r.bold = True
        r.font.size = Pt({'h1': 13, 'h2': 12, 'h3': 11, 'h4': 10.5, 'title': 11}[soort])
    if soort == 'li':
        p.paragraph_format.left_indent = Cm(0.5)
        p.text = ''
        r = p.add_run('•  ' + t); r.font.size = Pt(10)
    if soort in ('knop', 'whatsapp', 'header', 'nav', 'footer', 'title'):
        r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        if soort == 'knop':
            r.italic = True
        if soort == 'whatsapp':
            p.text = ''
            lab = p.add_run('[WhatsApp-bericht] '); lab.font.size = Pt(9); lab.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
            r = p.add_run(t); r.font.size = Pt(10); r.italic = True; r.font.color.rgb = RGBColor(0x55, 0x55, 0x55)


def tabel(doc, rijen):
    """rijen: lijst van (soort, nl, en)."""
    t = doc.add_table(rows=1, cols=2)
    t.style = 'Table Grid'
    t.autofit = False
    kop = t.rows[0].cells
    for c, lab in zip(kop, ('Nederlands', 'English')):
        c.text = ''
        r = c.paragraphs[0].add_run(lab); r.bold = True; r.font.size = Pt(9)
        shade(c, 'E8E8E8')
    for soort, nl, en in rijen:
        cells = t.add_row().cells
        for c, tx in zip(cells, (nl, en)):
            c.text = ''
            run_opmaak(c.paragraphs[0], tx or '', soort)
            if tx is None:
                shade(c, 'FFE9E9')
        if soort in ('h1', 'h2'):
            for c in cells:
                shade(c, 'F3F3F3')
    for row in t.rows:
        for c in row.cells:
            c.width = Cm(12.3)
    return t


def main():
    doc = Document()
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.LANDSCAPE
    sec.page_width, sec.page_height = Cm(29.7), Cm(21.0)
    for m in ('left_margin', 'right_margin', 'top_margin', 'bottom_margin'):
        setattr(sec, m, Cm(2))
    st = doc.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(10)

    doc.add_heading('HEAR · alle teksten van de site', 0)
    p = doc.add_paragraph()
    p.add_run('Redactieronde. ').bold = True
    p.add_run('Per pagina een tabel: links Nederlands, rechts Engels, één rij per tekstblok. '
              'Zet in Word "Wijzigingen bijhouden" aan en bewerk de tekst in de cellen. '
              'Wijzig je een Nederlandse zin, pas dan ook de Engelse ernaast aan. '
              'Opmerkingen (bijv. "blok verplaatsen" of "twijfel, kies jij") als Word-opmerking, niet als knip-en-plak. '
              'Knoppen staan cursief, WhatsApp-berichten zijn de vooringevulde teksten in de knoppen. '
              'Niet opgenomen: alt-teksten, meta-omschrijvingen, menu en footer staan één keer onderaan.')
    doc.add_paragraph(f'Stand: {Path(SITE / "index.html").stat().st_mtime and __import__("datetime").date.today().isoformat()} · bron: hear.nl')

    # inhoudsopgave-achtig lijstje
    doc.add_paragraph()
    for _, label in PAGINAS:
        doc.add_paragraph(label, style='List Bullet')

    mismatch = []
    for bestand, label in PAGINAS:
        nl_p = SITE / bestand
        en_p = SITE / 'en' / bestand
        if not nl_p.exists():
            print('ontbreekt', nl_p); continue
        nl = blokken(nl_p.read_text(encoding='utf-8'))
        en = blokken(en_p.read_text(encoding='utf-8')) if en_p.exists() else []
        if bestand == 'index.html':
            i = next(k for k, b in enumerate(nl) if b[0] == 'h2')
            nl = nl[:i + 1] + slider() + nl[i + 1:]
            j = next(k for k, b in enumerate(en) if b[0] == 'h2')
            en = en[:j + 1] + slider(True) + en[j + 1:]
        doc.add_page_break()
        doc.add_heading(label, 1)
        url_nl = 'https://hear.nl/' + bestand.replace('index.html', '')
        url_en = 'https://hear.nl/en/' + bestand.replace('index.html', '')
        q = doc.add_paragraph(); r = q.add_run(f'{url_nl}   ·   {url_en}'); r.font.size = Pt(8); r.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
        rijen = []
        n = max(len(nl), len(en))
        if len(nl) != len(en):
            mismatch.append((bestand, len(nl), len(en)))
        for i in range(n):
            s_nl, t_nl = nl[i] if i < len(nl) else (None, None)
            s_en, t_en = en[i] if i < len(en) else (None, None)
            rijen.append((s_nl or s_en, t_nl, t_en))
        tabel(doc, rijen)

    # globaal: menu, footer, titels
    doc.add_page_break()
    doc.add_heading('Menu, footer en paginatitels', 1)
    g_nl = globaal((SITE / 'index.html').read_text(encoding='utf-8'))
    g_en = globaal((SITE / 'en' / 'index.html').read_text(encoding='utf-8'))
    rijen = []
    for i in range(max(len(g_nl), len(g_en))):
        s, a = g_nl[i] if i < len(g_nl) else (None, None)
        _, b = g_en[i] if i < len(g_en) else (None, None)
        rijen.append((s or 'footer', a, b))
    tabel(doc, rijen)
    doc.add_heading('Paginatitels (browsertab)', 2)
    rijen = []
    for bestand, label in PAGINAS:
        a = BeautifulSoup((SITE / bestand).read_text(encoding='utf-8'), 'html.parser').find('title')
        bp = SITE / 'en' / bestand
        b = BeautifulSoup(bp.read_text(encoding='utf-8'), 'html.parser').find('title') if bp.exists() else None
        rijen.append(('title', tekst(a) if a else '', tekst(b) if b else None))
    tabel(doc, rijen)

    UIT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(UIT)
    print('geschreven', UIT)
    for m in mismatch:
        print('LET OP blokaantal NL/EN verschilt:', m)


if __name__ == '__main__':
    main()
