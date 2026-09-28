"""The one product or tool a page points at.

A guide that answers a question and then stops is a guide that ranks and earns
nothing. A guide that ends in a wall of twelve products is a guide nobody reads
to the end. So: exactly one thing per page, chosen because it is what the reader
of that particular page would reach for next, with a picture of it.

The choice is a lookup, not a judgement. Which product answers "what do the
numbers on a needle mean" is a fact about the catalogue that somebody who knows
the catalogue can write down once, and a model asked the same question every day
would give a slightly different answer every day. FEATURED is that table. A
topic missing from it fails the build rather than silently rendering nothing,
for the same reason a guide missing from the Learn index fails the build.

While PURCHASABLE is off the card still shows the product and links to it. It
just does not say add to cart, because that button does nothing yet. The copy
around it is tense neutral so that flipping the switch does not mean rewriting
this file.
"""

import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import images
import seo as SEO
from catalogue import I

E = html.escape

MONO = "font-family:'IBM Plex Mono',monospace;font-weight:500"
WRAP = 'max-width:1440px;margin:0 auto;padding:clamp(44px,6vw,80px) clamp(20px,5vw,72px)'

# name, href, image key, the line that says why this and not something else.
# A tool has no image key, so it renders as a wide card instead of a photograph.
PRODUCTS = {
 'insulin-syringes': ('U-100 insulin syringes', '/shop/syringes-needles/u-100-insulin-syringes',
                      'syringe_box',
                      'Graduated in units rather than millilitres, which is the whole reason '
                      'they exist as a separate thing.'),
 'pen-needles': ('Pen needles, 32G 4mm', '/shop/syringes-needles/pen-needles', 'blister',
                 'The short, fine end of the range, for a pen rather than a syringe.'),
 'hypodermic-needles': ('Injecting needles, 25G 25mm', '/shop/syringes-needles/hypodermic-needles',
                        'needle_macro',
                        'Separate needle and syringe, so the gauge and the length are '
                        'chosen rather than inherited.'),
 'drawing-up-needles': ('Drawing-up needles, 21G 38mm',
                        '/shop/syringes-needles/drawing-up-needles', 'lengths',
                        'Thicker and longer, for getting liquid out of a vial rather than '
                        'for injecting.'),
 'luer-lock-syringes': ('Luer-lock syringes, 3mL', '/shop/syringes-needles/luer-lock-syringes',
                        'syringes',
                        'Graduated in millilitres, with a needle that screws on rather '
                        'than pushes on.'),
 'bacteriostatic-water': ('Bacteriostatic water, 10mL', '/shop/diluents-swabs/bacteriostatic-water',
                          'vial_swabs',
                          'Sterile water with a preservative, sold as a diluent. It is not '
                          'a medicine and nothing in it treats anything.'),
 'alcohol-swabs': ('Alcohol swabs, 70% isopropyl', '/shop/diluents-swabs/alcohol-swabs',
                   'vial_swabs',
                   'Seventy per cent isopropyl in a foil sachet, which is the standard '
                   'because it dries at the right speed.'),
 'sharps-container-bench': ('Sharps container, 1.4L', '/shop/clinic-disposal/sharps-container-bench',
                            'sharps',
                            'The size that sits on a bench at home. Yellow, lidded, and '
                            'made to be filled once and closed.'),
 'sharps-container-wall': ('Sharps containers, 5L', '/shop/clinic-disposal/sharps-container-wall-mount',
                           'sharps',
                           'The clinic size, for a room where more than one person is '
                           'filling it.'),
 'nitrile-gloves': ('Nitrile gloves, powder free', '/shop/gloves-ppe/nitrile-examination-gloves',
                    'gloves',
                    'Powder free nitrile, which is what most clinics moved to and stayed on.'),
 'non-adherent-dressings': ('Non-adherent dressings, 7.5 x 10cm',
                            '/shop/wound-care/non-adherent-dressings', 'dressings',
                            'A contact layer the tissue does not stick to, so it lifts off '
                            'rather than pulling.'),
 'gauze-swabs': ('Gauze swabs, sterile, 7.5cm', '/shop/wound-care/sterile-gauze-swabs',
                 'dressings',
                 'Sterile, individually wrapped, and the thing most dressing changes '
                 'actually run out of.'),
 'saline-sachets': ('Saline sachets, 30mL', '/shop/diluents-swabs/sodium-chloride-sachets',
                    'vial_swabs',
                    'Single use sodium chloride, so a sachet is opened for the job and '
                    'then finished with.'),
 'safety-lancets': ('Safety lancets, 28G', '/shop/diagnostics/safety-lancets', 'diagnostic',
                    'The needle retracts once it has fired, so the used end is never '
                    'exposed.'),
}

TOOLS = {
 'gauge-finder': ('Gauge Finder', '/gauge-finder',
                  'Three questions and it picks a thickness and a length. Nothing you '
                  'answer leaves the browser.'),
 'reconstitution-calculator': ('Reconstitution calculator', '/tools/reconstitution-calculator',
                               'Volume in, concentration out, and the mark on the barrel '
                               'that corresponds to it.'),
 'gauge-chart': ('Needle gauge chart', '/learn/needle-gauge-chart',
                 'Every gauge against its hub colour and the lengths it comes in, on one '
                 'page.'),
}

# The page, and what its reader reaches for next. One entry per page that carries
# a feature block. Anything asking for a key not in here is a mistake.
FEATURED = {
 '/learn/needle-numbers-explained': 'tool:gauge-chart',
 '/learn/gauge-comparison': 'tool:gauge-finder',
 '/learn/reading-a-syringe': 'product:insulin-syringes',
 '/learn/first-injection': 'product:alcohol-swabs',
 '/learn/subcutaneous-technique': 'product:pen-needles',
 '/learn/intramuscular-technique': 'product:hypodermic-needles',
 '/learn/reconstitution-basics': 'tool:reconstitution-calculator',
 '/learn/sharps-disposal-australia': 'product:sharps-container-bench',
 '/learn/artg-explained': 'product:nitrile-gloves',
 '/learn/storing-supplies': 'product:sharps-container-wall',
}


def resolve(key):
    kind, _, name = key.partition(':')
    if kind == 'product':
        if name not in PRODUCTS:
            raise KeyError('no product named %r in feature.PRODUCTS' % name)
        title, href, img, why = PRODUCTS[name]
        return 'product', title, href, I[img], why
    if kind == 'tool':
        if name not in TOOLS:
            raise KeyError('no tool named %r in feature.TOOLS' % name)
        title, href, why = TOOLS[name]
        return 'tool', title, href, None, why
    raise ValueError('feature key %r must start with product: or tool:' % key)


def for_page(path):
    """The feature key for a page, or None if that page carries no block."""
    return FEATURED.get(path.rstrip('/') or '/')


def interest_for(path):
    """A short tag for what the reader of this page was looking at.

    Derived from the thing already featured rather than from a second table, so
    the two can never disagree. A product gives its shop category, which is the
    grouping anything later would actually be sent about. A tool gives its own
    name.
    """
    key = for_page(path)
    if key is None:
        return 'general'
    kind, _, name = key.partition(':')
    if kind == 'tool':
        return name.replace('-', ' ')
    href = PRODUCTS[name][1]
    parts = [seg for seg in href.split('/') if seg]
    return parts[1].replace('-', ' ') if len(parts) > 1 else 'general'


def cta(kind):
    if kind == 'tool':
        return 'Open it'
    return 'See it' if SEO.PURCHASABLE else 'See the details'


def block(path, bg='background:#F2F2F1;'):
    """The one card. Raises if the page has no entry, so a miss is not silent."""
    key = for_page(path)
    if key is None:
        raise KeyError('no featured product or tool for %r. Add it to feature.FEATURED.' % path)
    kind, title, href, img, why = resolve(key)

    o = []
    a = o.append
    a('    <section style="%sborder-bottom:1px solid #E3E3E1">\n      <div style="%s">\n'
      % (bg, WRAP))
    a('        <div style="%s;font-size:11px;letter-spacing:.16em;text-transform:uppercase;'
      'color:#59595A;margin-bottom:18px">%s</div>\n'
      % (MONO, 'The tool for this' if kind == 'tool' else 'What this is about'))
    a('        <a href="%s" data-link style="display:grid;'
      'grid-template-columns:%s;gap:clamp(18px,3vw,32px);align-items:center;'
      'background:#FAFAFA;border:1px solid #E3E3E1;border-radius:22px;padding:%s;'
      'text-decoration:none;color:inherit">\n'
      % (E(href),
         'minmax(0,1fr)' if img is None else 'minmax(120px,190px) minmax(0,1fr)',
         '26px 24px' if img is None else '20px 24px 20px 20px'))
    if img is not None:
        a('          <span style="display:block;aspect-ratio:1;border-radius:16px;'
          'overflow:hidden;background:#EDEDEB">\n')
        a('            <img src="%s"%s alt="%s" loading="lazy" decoding="async" '
          'style="width:100%%;height:100%%;object-fit:cover">\n'
          % (images.optimised(img, 480), images.srcset(img, (320, 480, 640)), E(title)))
        a('          </span>\n')
    a('          <span style="display:block">\n')
    a("            <span style=\"display:block;font-family:'Archivo',sans-serif;"
      'font-weight:600;font-size:clamp(19px,2vw,24px);letter-spacing:-.025em;'
      'margin-bottom:8px">%s</span>\n' % E(title))
    a('            <span style="display:block;font-size:16px;line-height:1.55;'
      'color:#3A3A38;max-width:52ch">%s</span>\n' % E(why))
    a('            <span style="display:inline-block;margin-top:14px;font-size:15.5px;'
      'font-weight:600;color:#1C4034;border-bottom:1.5px solid #8FBFA6;padding-bottom:2px">'
      '%s <span data-arrow>&rarr;</span></span>\n' % E(cta(kind)))
    a('          </span>\n')
    a('        </a>\n      </div>\n    </section>\n\n')
    return ''.join(o)


def check():
    """Every entry resolves. Called by the build so a typo fails there, not live."""
    for path, key in sorted(FEATURED.items()):
        resolve(key)
    return len(FEATURED)


if __name__ == '__main__':
    print('%d pages have a featured product or tool, all resolving' % check())
