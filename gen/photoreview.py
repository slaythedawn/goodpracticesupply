# docs/internal/photo-review.html — a side by side of the launch range photography
# against the shot each product used before it had one of its own.
#
# This is a working page, not part of the site: nothing links to it, it is not in
# the sitemap, and it can be deleted the moment the photography is settled. It
# exists because the images live on a CDN that cannot be reached from where the
# generators run, so the only way to judge them is in a browser.

import io, os, pathlib, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalogue import CATEGORIES, SHOTS, I

DOCS = str(pathlib.Path(__file__).resolve().parent.parent / 'docs')

# What each product used to show, before it had its own photograph.
BEFORE = {
    'cotton-wool-balls': 'vial_swabs', 'cotton-wool-rolls': 'vial_swabs',
    'adhesive-plasters': 'dressings', 'crepe-bandages': 'dressings',
    'cohesive-bandage': 'dressings', 'silicone-scar-gel': 'dressings',
    'sutures': 'dressings', 'rigid-strapping-tape': 'dressings',
    'elastic-adhesive-bandage': 'dressings', 'kinesiology-tape': 'dressings',
    'compression-stockings': 'dressings',
    'urinalysis-strips': 'diagnostic', 'otoscope-ear-specula': 'diagnostic',
    'tongue-depressors': 'diagnostic',
    'incontinence-pads': 'sharps',
    'hand-soap': 'gloves', 'hand-towels': 'gloves', 'facial-tissues': 'gloves',
}

ORIGINALS = [
    ('syringe_box', 'Syringe box'), ('gloves', 'Glove dispenser'),
    ('vial_swabs', 'Vial and swabs'), ('dressings', 'Dressings'),
    ('diagnostic', 'Diagnostic strips'), ('sharps', 'Sharps container'),
]

CSS = """
*{box-sizing:border-box}
body{margin:0;background:#FAFAFA;color:#0E0E0E;
 font-family:'Archivo',-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
 -webkit-font-smoothing:antialiased}
.mono{font-family:'IBM Plex Mono',ui-monospace,SFMono-Regular,Menlo,monospace;
 font-weight:500;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#59595A}
.wrap{max-width:1280px;margin:0 auto;padding:clamp(32px,5vw,72px) clamp(16px,4vw,48px)}
h1{font-size:clamp(28px,4vw,44px);letter-spacing:-.035em;line-height:1.05;margin:14px 0 16px;font-weight:600}
h2{font-size:clamp(20px,2.4vw,28px);letter-spacing:-.03em;margin:0 0 6px;font-weight:600}
p{font-size:16.5px;line-height:1.6;color:#3A3A38;max-width:64ch;margin:0 0 14px}
section{border-top:1px solid #E3E3E1;padding-top:clamp(28px,4vw,48px);margin-top:clamp(28px,4vw,48px)}
.strip{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(180px,100%),1fr));gap:14px;margin-top:22px}
.pairs{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(420px,100%),1fr));gap:26px;margin-top:26px}
.pair{border:1px solid #E3E3E1;border-radius:20px;background:#fff;overflow:hidden}
.pair header{padding:14px 18px;border-bottom:1px solid #E3E3E1}
.pair h3{margin:0;font-size:17px;font-weight:600;letter-spacing:-.01em}
.two{display:grid;grid-template-columns:1fr 1fr}
figure{margin:0}
figure img{display:block;width:100%;aspect-ratio:4/3;object-fit:cover;background:#EDEDEB}
figcaption{padding:9px 12px;border-top:1px solid #E3E3E1}
.two figure+figure{border-left:1px solid #E3E3E1}
.tile img{display:block;width:100%;aspect-ratio:1/1;object-fit:cover;
 background:#EDEDEB;border-radius:14px;border:1px solid #E3E3E1}
.tile div{margin-top:7px}
.note{background:#EDEDEB;border-radius:18px;padding:18px 22px;margin-top:22px}
.note p{margin:0;max-width:none;font-size:15px}
"""


def tile(src, label):
    return ('    <div class="tile"><img src="%s" alt="%s" loading="lazy">'
            '<div class="mono">%s</div></div>\n' % (src, label, label))


def fig(src, label, alt):
    return ('        <figure><img src="%s" alt="%s" loading="lazy">'
            '<figcaption class="mono">%s</figcaption></figure>\n' % (src, alt, label))


def main():
    products = []
    for c in CATEGORIES:
        for p in c['products']:
            if p['slug'] in BEFORE:
                products.append((c, p))

    o = ['<!DOCTYPE html>\n<html lang="en-AU">\n<head>\n<meta charset="utf-8">\n',
         '<meta name="viewport" content="width=device-width, initial-scale=1">\n',
         '<meta name="robots" content="noindex, nofollow">\n',
         '<title>Photography review | Good Practice Supply</title>\n',
         '<link rel="preconnect" href="https://fonts.googleapis.com">\n',
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n',
         '<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600'
         '&family=IBM+Plex+Mono:wght@500&display=swap" rel="stylesheet">\n',
         '<style>%s</style>\n</head>\n<body>\n<div class="wrap">\n' % CSS,
         '<div class="mono">Internal &middot; not linked, not indexed</div>\n',
         '<h1>Launch range photography</h1>\n',
         '<p>Sixteen new product shots against the picture each product showed before '
         'it had one of its own. The question is whether the new ones sit with the '
         'originals or read as a different set.</p>\n',
         '<div class="note"><p>Delete <code>gen/photoreview.py</code> and '
         '<code>docs/internal/</code> once this is settled.</p></div>\n']

    o.append('<section>\n<h2>The originals</h2>\n')
    o.append('<p>The six family shots the site was built on. Everything below should '
             'look like it came from the same afternoon as these.</p>\n<div class="strip">\n')
    for key, label in ORIGINALS:
        o.append(tile(I[key], label))
    o.append('</div>\n</section>\n')

    o.append('<section>\n<h2>New, against what it replaced</h2>\n')
    o.append('<p>Left is the new shot. Right is what the page showed before.</p>\n')
    o.append('<div class="pairs">\n')
    for c, p in products:
        new_key = SHOTS[p['family']][0][0]
        old_key = BEFORE[p['slug']]
        o.append('      <div class="pair">\n')
        o.append('        <header><h3>%s</h3><div class="mono">%s</div></header>\n'
                 % (p['name'], c['name']))
        o.append('        <div class="two">\n')
        o.append(fig(I[new_key], 'New', p['name']))
        o.append(fig(I[old_key], 'Was', 'The shot this page used before'))
        o.append('        </div>\n      </div>\n')
    o.append('</div>\n</section>\n</div>\n</body>\n</html>\n')

    out = DOCS + '/internal'
    if not os.path.isdir(out):
        os.makedirs(out)
    path = out + '/photo-review.html'
    io.open(path, 'w', encoding='utf-8').write(''.join(o))
    print('photo review: %d pairs, %d originals -> %s'
          % (len(products), len(ORIGINALS), path.replace(DOCS, 'docs')))


if __name__ == '__main__':
    main()
