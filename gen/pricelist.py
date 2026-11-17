"""Build the supplier-facing supply list as an A4 portrait document.

Not part of the site build. Nothing here writes into docs/ and the build order
in gen/README.md does not include it. Run it on its own when the range changes:

    python3 gen/pricelist.py          # writes export/supply-list.html + .pdf

It reads the one source of truth for the range, gen/catalogue.py, so the
document cannot drift from the site the way a hand-kept spreadsheet does. Every
size, variant and pack format on the page is the same string the product page
renders.

Two deliberate omissions.

There are no prices. The catalogue carries them in cents because the cart needs
them, but they are retail placeholders and no supplier has quoted a wholesale
price yet, so printing a number here would invent a commercial position. The
document says pricing is available on request instead, which is both true and
the normal thing for a trade list to say.

There are no regulatory claims. ARTG and TGA status is a per-product fact that
has to come from a real data field, and the catalogue does not carry one yet.
A trade document is exactly where a blanket claim would do damage, so there is
none, rather than a hedged one.

The order within a product leads with the size or variant, because that is the
line a buyer orders against. The product is the heading; the variant is the row.
"""

import datetime
import io
import os
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import catalogue

ROOT = pathlib.Path(__file__).resolve().parent.parent
EXPORT = ROOT / 'export'
LOCKUP = ROOT / 'brand' / 'svg' / 'gps-lockup-canvas.svg'

FOREST = '#143026'
DEEP = '#1C4034'
MINT = '#B7CFC3'
MINT_BRIGHT = '#8FBFA6'
CANVAS = '#FAFAFA'
INK = '#0E0E0E'
MUTED = '#59595A'
RULE = '#E3E3E1'

# Archivo is the brand face and is loaded from Google Fonts for anybody who
# opens the HTML. The PDF is rendered in a sandbox with no access to Google
# Fonts, so the stack falls through to Inter, which is a near neighbour and is
# installed. The lockup itself is outlined vector, so the brand mark is exact
# either way.
STACK = "'Archivo','Inter Display','Inter','Helvetica Neue',Arial,sans-serif"
BLACKSTACK = "'Archivo Black','Archivo','Inter Display','Inter',sans-serif"
MONO = "'IBM Plex Mono','DejaVu Sans Mono',monospace"

ON_REQUEST = 'On request'
PRICE_LINE = 'Wholesale pricing available on request'
# Proposed pack sizes.
#
# One per product, because a column offering "Box of 100, or carton" reads as a
# business that has not decided. These are proposals, not stock on hand, and the
# document says so once at the foot rather than hedging on every line.
#
# Grounded in the sourcing brief of 23 August wherever it named a format, with
# its ranges resolved to the single figure at the standard end: the brief said
# "Box of 20 to 50" for sterile water because it was asking a factory what it
# made, and a buyer reading that learns only that we do not know yet.
#
# A value may be a dict keyed on the variant label where a product's variants
# are different formats rather than different sizes. Chlorhexidine is the case
# that forced it: swabsticks and a 500mL bottle do not share a pack size, and
# printing "Box of 25" against a bottle is exactly the kind of detail that tells
# a buyer nobody checked. '*' is the fallback within such a dict.
PACK_SIZE = {
    'u-100-insulin-syringes': 'Box of 100',
    'luer-lock-syringes': 'Box of 100',
    'hypodermic-needles': 'Box of 100',
    'drawing-up-needles': 'Box of 100',
    'vial-access-devices': 'Box of 50',
    'pen-needles': 'Box of 100',
    'luer-slip-syringes': 'Box of 100',

    'nitrile-examination-gloves': 'Box of 100',
    'latex-examination-gloves': 'Box of 100',
    'surgical-masks-level-2': 'Box of 50',
    'isolation-gowns': 'Pack of 10',
    'aprons-on-a-roll': 'Roll of 200',
    'alcohol-hand-rub': 'Each',

    'alcohol-swabs': 'Box of 100',
    'bacteriostatic-water': 'Box of 25',
    'sterile-water-for-injection': 'Box of 50',
    'chlorhexidine-skin-prep': {'500mL bottle': 'Each', '*': 'Box of 25'},
    'povidone-iodine-swabsticks': 'Box of 50',
    'sodium-chloride-sachets': 'Box of 50',
    'cotton-wool-balls': 'Bag of 500',

    'non-adherent-dressings': 'Box of 50',
    'sterile-gauze-swabs': 'Box of 100',
    'fixation-tape': 'Box of 12',
    'conforming-bandages': 'Pack of 12',
    'island-dressings': 'Box of 50',
    'first-aid-kit-workplace': 'Each',
    'adhesive-plasters': 'Box of 100',
    'crepe-bandages': 'Box of 12',
    'cohesive-bandage': 'Box of 12',
    'hydrocolloid-foam-dressings': 'Box of 10',
    'silicone-scar-gel': 'Each',
    'sutures': 'Box of 12',

    'safety-lancets': 'Box of 100',
    'blood-glucose-test-strips': 'Each',
    'thermometer-probe-covers': 'Box of 100',
    'vaginal-speculum-disposable': 'Box of 25',
    'ecg-electrodes': 'Bag of 50',
    'ultrasound-gel': 'Each',
    'urinalysis-strips': 'Tube of 100',
    'otoscope-ear-specula': 'Bag of 100',
    'blood-glucose-meter': 'Each',
    'tongue-depressors': 'Box of 100',

    'sharps-container-bench': 'Each',
    'sharps-container-wall-mount': 'Each',
    'couch-roll': 'Carton of 6',
    'blueys-underpads': 'Box of 50',
    'clinical-waste-bags': 'Roll of 50',
    'surface-wipes-clinical': 'Tub of 200',
    'incontinence-pads': 'Pack of 14',

    'hand-soap': '500mL pump',
    'hand-towels': 'Carton of 2400',
    'facial-tissues': 'Carton of 24',
    'cotton-wool-rolls': 'Each',

    'rigid-strapping-tape': 'Box of 8',
    'elastic-adhesive-bandage': 'Box of 6',
    'kinesiology-tape': 'Roll',
    'compression-stockings': 'Pair',
}


def pack_for(product, variant_label):
    """The proposed pack size for one variant.

    A missing product is a build error rather than a blank cell. A line card
    that silently prints nothing in the pack column against a product somebody
    added last week is the failure this is here to prevent.
    """
    v = PACK_SIZE.get(product['slug'])
    if v is None:
        raise SystemExit('pricelist: no pack size for %r. Add it to PACK_SIZE '
                         'rather than letting the document go out with a gap.'
                         % product['slug'])
    if isinstance(v, dict):
        return v.get(variant_label, v['*'])
    return v


def lockup(height_px):
    """The brand lockup inline, scaled to a height, aspect preserved."""
    svg = LOCKUP.read_text(encoding='utf-8')
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    if not m:
        raise SystemExit('pricelist: %s has no viewBox, so it cannot be scaled '
                         'safely' % LOCKUP)
    w, h = float(m.group(1)), float(m.group(2))
    width_px = height_px * w / h
    svg = re.sub(r'\swidth="[\d.]+"', '', svg, count=1)
    svg = re.sub(r'\sheight="[\d.]+"', '', svg, count=1)
    return svg.replace(
        '<svg ', '<svg width="%.1f" height="%d" style="display:block" '
                 % (width_px, height_px), 1)


def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;'))


def rows_for(product):
    """One row per variant, which is the line a buyer orders against."""
    return [(label, note, pack_for(product, label))
            for label, note in product['variants']]


def build():
    cats = catalogue.CATEGORIES
    today = datetime.date.today()
    n_products = sum(len(c['products']) for c in cats)
    n_lines = sum(len(p['variants']) for c in cats for p in c['products'])

    a = []
    w = a.append
    w('<!doctype html>')
    w('<html lang="en-AU"><head><meta charset="utf-8">')
    w('<title>Good Practice Supply supply list</title>')
    w('<link rel="preconnect" href="https://fonts.googleapis.com">')
    w('<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;'
      '500;600;700&family=Archivo+Black&family=IBM+Plex+Mono:wght@400;500'
      '&display=swap" rel="stylesheet">')
    w('<style>')
    w('@page{size:A4 portrait;}')
    w('*{box-sizing:border-box;margin:0;padding:0}')
    w('body{font-family:%s;color:%s;font-size:9.1pt;line-height:1.45;'
      '-webkit-print-color-adjust:exact;print-color-adjust:exact}' % (STACK, INK))
    w('h1,h2,h3{font-family:%s;font-weight:900;letter-spacing:-.035em;'
      'line-height:1.04}' % BLACKSTACK)

    # Masthead. A rounded dark panel is the site's own header treatment, which
    # is why it is used here rather than a full bleed band: it survives the
    # printer's unprintable margin and still reads as the brand.
    w('.mast{background:%s;border:1px solid rgba(143,191,166,.3);'
      'border-radius:16px;padding:20px 22px;color:%s;margin-bottom:18px}'
      % (FOREST, CANVAS))
    w('.mast .top{display:flex;align-items:flex-start;'
      'justify-content:space-between;gap:24px}')
    w('.mast h1{font-size:23pt;color:%s;margin:16px 0 0}' % CANVAS)
    w('.mast .sub{font-size:9pt;color:rgba(250,250,250,.78);margin-top:7px;'
      'max-width:118mm}')
    w('.meta{font-family:%s;font-size:7.2pt;letter-spacing:.055em;'
      'text-transform:uppercase;color:%s;text-align:right;white-space:nowrap}'
      % (MONO, MINT))
    w('.meta b{display:block;color:%s;font-weight:500}' % CANVAS)
    w('.pricebar{margin-top:16px;padding-top:13px;'
      'border-top:1px solid rgba(143,191,166,.3);display:flex;'
      'align-items:baseline;justify-content:space-between;gap:16px}')
    w('.pricebar .line{font-family:%s;font-weight:700;font-size:11.5pt;'
      'letter-spacing:-.02em;color:%s}' % (BLACKSTACK, MINT_BRIGHT))
    w('.pricebar .note{font-size:8pt;color:rgba(250,250,250,.72);'
      'text-align:right;max-width:72mm}')

    # Category and table.
    w('.cat{break-inside:auto;margin-top:15px}')
    w('.cat:first-of-type{margin-top:0}')
    w('.cathead{display:flex;align-items:baseline;gap:10px;'
      'border-bottom:1.6px solid %s;padding-bottom:5px;margin-bottom:0;'
      'break-after:avoid}' % DEEP)
    w('.cathead h2{font-size:12.5pt;color:%s}' % DEEP)
    w('.cathead .n{font-family:%s;font-size:7.2pt;letter-spacing:.06em;'
      'text-transform:uppercase;color:%s;margin-left:auto;white-space:nowrap}'
      % (MONO, MUTED))
    w('table{width:100%;border-collapse:collapse}')
    w('thead th{font-family:%s;font-size:6.8pt;letter-spacing:.07em;'
      'text-transform:uppercase;color:%s;font-weight:500;text-align:left;'
      'padding:6px 8px 5px;border-bottom:1px solid %s}'
      % (MONO, MUTED, RULE))
    w('thead{display:table-header-group}')
    w('tr{break-inside:avoid}')
    # The product heading row and its first variant must not be split apart.
    w('tr.prod{break-after:avoid}')
    w('tr.prod td{padding:9px 8px 2px;border-top:1px solid %s}' % RULE)
    w('.cat tr.prod:first-of-type td{border-top:0}')
    w('.pname{font-family:%s;font-weight:700;font-size:9.6pt;color:%s;'
      'letter-spacing:-.015em}' % (BLACKSTACK, INK))
    w('.pspec{font-size:8pt;color:%s;margin-top:1px}' % MUTED)
    w('tbody td{padding:2.5px 8px;vertical-align:baseline}')
    w('td.size{font-weight:600;white-space:nowrap;width:30mm}')
    w('td.note{color:%s;font-size:8.3pt}' % MUTED)
    w('td.pack{font-size:8.3pt;color:%s;width:61mm}' % MUTED)
    w('td.price{font-family:%s;font-size:7.6pt;color:%s;text-align:right;'
      'white-space:nowrap;width:19mm}' % (MONO, MUTED))
    w('.tail{margin-top:20px;padding-top:12px;border-top:1.6px solid %s;'
      'font-size:8pt;color:%s;break-inside:avoid}' % (DEEP, MUTED))
    w('.tail b{color:%s}' % INK)
    w('</style></head><body>')

    # ---- masthead ----
    w('<div class="mast"><div class="top">')
    w(lockup(34))
    w('<div class="meta"><b>Supply list</b>%s</div>' % today.strftime('%d %B %Y'))
    w('</div>')
    w('<h1>Product supply list</h1>')
    # "Australian consumables" reads as a country-of-origin claim, and these
    # are being sourced overseas. Say who the market is, not where the goods
    # are made, because the second one is a claim and nobody has made it.
    w('<div class="sub">Medical and clinical consumables for the Australian '
      'market. Our full range, listed by size and variant.</div>')
    w('<div class="pricebar"><div class="line">%s</div>' % esc(PRICE_LINE))
    w('<div class="note">%d products across %d categories, %d size and variant '
      'lines. Pack sizes can be configured to your requirements.</div>'
      % (n_products, len(cats), n_lines))
    w('</div></div>')

    # ---- categories ----
    for cat in cats:
        w('<div class="cat">')
        w('<div class="cathead"><h2>%s</h2>' % esc(cat['name']))
        w('<span class="n">%d products</span></div>' % len(cat['products']))
        w('<table><thead><tr>'
          '<th>Size / variant</th><th>Detail</th>'
          '<th>Pack size</th><th style="text-align:right">Price</th>'
          '</tr></thead><tbody>')
        for p in cat['products']:
            w('<tr class="prod"><td colspan="4">'
              '<span class="pname">%s</span>'
              '<div class="pspec">%s</div></td></tr>'
              % (esc(p['name']), esc(p['spec'])))
            for size, note, packs in rows_for(p):
                w('<tr><td class="size">%s</td><td class="note">%s</td>'
                  '<td class="pack">%s</td><td class="price">%s</td></tr>'
                  % (esc(size), esc(note), esc(packs), ON_REQUEST))
        w('</tbody></table></div>')

    w('<div class="tail">')
    w('<b>Pricing.</b> %s.<br>' % esc(PRICE_LINE))
    w('<b>Pack sizes.</b> The pack sizes shown are the proposed trade sizes. '
      'Final pack and carton quantities are confirmed on quotation and can be '
      'configured to your requirements.<br>')
    w('<b>Specifications.</b> Sizes and gauges are as listed. Other sizes '
      'within each range can be quoted on request.<br>')
    # The site's standing disclosure says this on every page. A factory reading
    # a list with bacteriostatic water and sterile water on it is exactly the
    # reader who needs the boundary stated, so it is here too, in their terms.
    w('<b>Scope.</b> Good Practice Supply carries consumables only. We do not '
      'supply peptides, hormones or any prescription medicine, and we are not '
      'seeking quotes for them.')
    w('</div>')
    w('</body></html>')

    EXPORT.mkdir(exist_ok=True)
    html = '\n'.join(a)
    out_html = EXPORT / 'supply-list.html'
    io.open(out_html, 'w', encoding='utf-8').write(html)
    print('pricelist: %s  (%d products, %d lines, %d categories)'
          % (out_html.relative_to(ROOT), n_products, n_lines, len(cats)))
    return out_html


def to_pdf(src):
    """Render with the preinstalled Chromium. Fonts are blocked deliberately.

    Google Fonts is outside this environment's network allowlist, so the
    request would stall the render until it timed out and the output would be
    identical anyway. Aborting the request makes the render prompt and the
    fallback explicit rather than accidental.
    """
    script = ROOT / 'gen' / '_pricelist_pdf.mjs'
    out = EXPORT / 'supply-list.pdf'
    r = subprocess.run(['node', str(script), str(src), str(out)],
                       capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        raise SystemExit('pricelist: the PDF render failed, so no document was '
                         'written. The HTML above is still valid.')
    return out


if __name__ == '__main__':
    src = build()
    if '--html-only' not in sys.argv:
        to_pdf(src)
