# docs/search-index.json — everything the header search can find.
#
# The whole site is static, so search is a small JSON file the browser fetches
# once and matches against locally. Fifty-seven products, eight categories and
# the fixed pages come to a few tens of kilobytes, which is smaller than one of
# the photographs and means no search backend to run, pay for or keep in sync.
#
# Rebuild after anything that adds, renames or removes a page.

import io, json, os, pathlib, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalogue import CATEGORIES

DOCS = str(pathlib.Path(__file__).resolve().parent.parent / 'docs')

# What people actually type. The left side is what someone searches for, the
# right side is the wording on the page. Without this, "band aid" finds nothing
# and "needles" misses half the category, which is how a search bar loses trust
# on the first try.
SYNONYMS = {
    'adhesive-plasters':        'band aid bandaid bandaids plaster sticking plaster cuts blister',
    'crepe-bandages':           'bandage wrap sprain strapping support',
    'cohesive-bandage':         'vet wrap self adhesive bandage coban sticks to itself',
    'elastic-adhesive-bandage': 'eab strapping sports tape ankle',
    'rigid-strapping-tape':     'zinc oxide strapping sports tape ankle taping rigid',
    'kinesiology-tape':         'kt tape k tape rocktape physio tape',
    'compression-stockings':    'ted stockings flight socks varicose travel',
    'alcohol-swabs':            'alcohol wipes prep pads isopropyl sterets',
    'nitrile-examination-gloves': 'disposable gloves exam gloves blue gloves',
    'latex-examination-gloves': 'disposable gloves exam gloves',
    'surgical-masks-level-2':   'face mask surgical mask',
    'hypodermic-needles':       'needle needles injection drawing up im intramuscular',
    'u-100-insulin-syringes':   'insulin syringe units subcutaneous sub q slin pin',
    'luer-lock-syringes':       'syringe barrel 1ml 3ml 5ml',
    'luer-slip-syringes':       'syringe barrel slip tip',
    'pen-needles':              'pen tips injector pen ozempic mounjaro saxenda',
    'drawing-up-needles':       'blunt fill needle draw up reconstitution',
    'vial-access-devices':      'vial adapter spike needle free',
    'bacteriostatic-water':     'bac water reconstitution diluent benzyl alcohol',
    'sterile-water-for-injection': 'wfi diluent reconstitution',
    'sharps-container-bench':   'sharps bin needle disposal yellow bin',
    'sharps-container-wall-mount': 'sharps bin needle disposal wall bracket',
    'blood-glucose-test-strips': 'bgl strips sugar test diabetes',
    'blood-glucose-meter':      'bgl meter glucometer sugar test diabetes',
    'safety-lancets':           'finger prick lancet pricker',
    'urinalysis-strips':        'urine dipstick urine test ph protein',
    'otoscope-ear-specula':     'ear tips otoscope speculum',
    'tongue-depressors':        'tongue depressor spatula icy pole stick',
    'incontinence-pads':        'continence pads pull ups adult nappies',
    'cotton-wool-balls':        'cotton balls cottonwool',
    'cotton-wool-rolls':        'cotton roll zig zag cottonwool',
    'hand-soap':                'hand wash soap liquid soap basin',
    'hand-towels':              'paper towel hand towel dispenser slimfold',
    'facial-tissues':           'tissues kleenex box of tissues',
    'sutures':                  'stitches suture nylon absorbable',
    'silicone-scar-gel':        'scar gel silicone scar treatment',
    'hydrocolloid-foam-dressings': 'hydrocolloid foam dressing blister dressing',
    'sterile-gauze-swabs':      'gauze swabs squares sterile',
    'ultrasound-gel':           'ultrasound gel conductive gel',
    'ecg-electrodes':           'ecg dots electrodes stickers',
}

PAGES = [
    ('Gauge Finder', 'Three questions, then the gauge and length that suit you',
     '/gauge-finder', 'Tools', 'needle gauge which needle size picker help choose'),
    ('Peptide reconstitution calculator', 'Work out the dose on the barrel from the vial and the water',
     '/tools/reconstitution-calculator', 'Tools', 'reconstitution calculator mixing bac water units dose maths'),
    ('Needle gauge chart', 'Every gauge, its colour and what it is used for',
     '/learn/needle-gauge-chart', 'Guides', 'gauge chart needle sizes colour code iso reference table'),
    ('Always Stocked', 'A standing order that arrives before you run out',
     '/always-stocked', 'Service', 'subscription standing order repeat delivery auto reorder never run out'),
    ('Clinic Portal', 'Accounts, tiered pricing and order support for practices',
     '/clinic-portal', 'Service', 'clinic account wholesale trade practice sign in login apply business'),
    ('All guides', 'Plain explanations of the things people get wrong',
     '/learn', 'Guides', 'guides articles help how to learn'),
    ('About', 'Who we are and why the prices are on the page',
     '/about', 'Company', 'about us company story'),
    ('Contact', 'Delivery, returns and how to reach a person',
     '/contact', 'Company', 'contact support delivery returns shipping refund phone email help'),
    ('GLP-1 injections', 'What to have on hand for a weekly injection',
     '/for/glp-1-injections', 'Guides', 'ozempic wegovy mounjaro saxenda semaglutide tirzepatide weekly'),
    ('TRT injections', 'Needles, barrels and swabs for testosterone therapy',
     '/for/trt-injections', 'Guides', 'testosterone trt intramuscular oil im'),
    ('Peptide reconstitution', 'Mixing, storing and drawing up',
     '/for/peptide-reconstitution', 'Guides', 'peptide reconstitution mixing bac water vial'),
    ('Diabetes at home', 'Testing and injecting day to day',
     '/for/diabetes-at-home', 'Guides', 'diabetes insulin bgl testing home'),
    ('Wound care at home', 'Cleaning, dressing and covering',
     '/for/wound-care-at-home', 'Guides', 'wound dressing cut graze burn first aid'),
    ('Clinic fit-out', 'The full list for a new treatment room',
     '/for/clinic-fit-out', 'Guides', 'new clinic fit out setup treatment room opening'),
    ('Shop', 'Every category and every price, no account needed',
     '/shop', 'Shop', 'shop all products catalogue browse'),
]


def build():
    rows = []
    for c in CATEGORIES:
        rows.append({'t': c['name'], 's': '%d products' % len(c['products']),
                     'u': '/shop/' + c['slug'], 'g': 'Category',
                     'k': c['name'].lower()})
        for p in c['products']:
            rows.append({'t': p['name'], 's': p['spec'],
                         'u': '/shop/%s/%s' % (c['slug'], p['slug']), 'g': c['name'],
                         'k': ' '.join([p['name'].lower(), p['spec'].lower(),
                                        c['name'].lower(),
                                        SYNONYMS.get(p['slug'], '')]).strip()})
    for t, s, u, g, k in PAGES:
        rows.append({'t': t, 's': s, 'u': u, 'g': g, 'k': (t + ' ' + s + ' ' + k).lower()})
    return rows


def main():
    rows = build()
    path = DOCS + '/search-index.json'
    io.open(path, 'w', encoding='utf-8').write(
        json.dumps(rows, ensure_ascii=False, separators=(',', ':')) + '\n')
    print('search index: %d entries, %d bytes' % (len(rows), os.path.getsize(path)))


if __name__ == '__main__':
    main()
