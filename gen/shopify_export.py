# export/shopify-products.csv — the catalogue, in Shopify's product import format.
#
# The repo stays the source of truth. Shopify holds a copy so it can price, take
# money and manage orders; it never becomes the place products are authored. That
# is the whole point of the headless arrangement: one file to edit, one diff to
# review, and the store follows.
#
# Everything imports as DRAFT and unpublished, on purpose. Every price in
# catalogue.py is invented until a factory quotes, and a draft product cannot be
# bought by accident.
#
# After importing, pull the variant IDs back out of Shopify and write them into
# export/variant-map.json. The storefront needs those IDs to build a cart; SKUs
# are not addressable through the Storefront API.

import csv, io, json, os, pathlib, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalogue import CATEGORIES, SHOTS, I, sku
import seo as SEO

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'export'

COLUMNS = [
    'Handle', 'Title', 'Body (HTML)', 'Vendor', 'Type', 'Tags', 'Published',
    'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value',
    'Variant SKU', 'Variant Grams', 'Variant Inventory Tracker',
    'Variant Inventory Qty', 'Variant Inventory Policy',
    'Variant Fulfillment Service', 'Variant Price', 'Variant Requires Shipping',
    'Variant Taxable', 'Image Src', 'Image Position', 'Image Alt Text',
    'SEO Title', 'SEO Description', 'Status',
]

# What the first option axis is actually called, per product. Shopify shows this
# label on the buy form, so "Gauge and length" beats "Option 1". Inference covers
# most of the range; the overrides are for the ones it reads wrong.
OPTION_OVERRIDES = {
    'surgical-masks-level-2': 'Barrier level',
    'incontinence-pads': 'Absorbency',
    'compression-stockings': 'Size',
    'hypodermic-needles': 'Gauge and length',
    'pen-needles': 'Gauge and length',
    'u-100-insulin-syringes': 'Gauge and length',
    'drawing-up-needles': 'Tip',
    'vial-access-devices': 'Neck size',
    'urinalysis-strips': 'Parameters',
    'otoscope-ear-specula': 'Tip size',
    'blood-glucose-meter': 'Kit',
    'sutures': 'Gauge',
    'isolation-gowns': 'Size', 'aprons-on-a-roll': 'Grade',
    'alcohol-hand-rub': 'Format', 'chlorhexidine-skin-prep': 'Format',
    'povidone-iodine-swabsticks': 'Format', 'cotton-wool-balls': 'Format',
    'first-aid-kit-workplace': 'Workplace size', 'silicone-scar-gel': 'Tube size',
    'blood-glucose-test-strips': 'Vial size', 'thermometer-probe-covers': 'Fit',
    'ecg-electrodes': 'Patient', 'tongue-depressors': 'Patient',
    'ultrasound-gel': 'Format', 'sharps-container-bench': 'Capacity',
    'sharps-container-wall-mount': 'Capacity', 'clinical-waste-bags': 'Capacity',
    'surface-wipes-clinical': 'Formulation', 'hand-soap': 'Formulation',
    'alcohol-swabs': 'Formulation', 'hand-towels': 'Fold',
    'facial-tissues': 'Box', 'cotton-wool-rolls': 'Roll size',
    'kinesiology-tape': 'Colour or cut', 'adhesive-plasters': 'Backing',
}

SIZE_WORDS = {'small', 'medium', 'large', 'extra large', 'x-large'}


def option_name(p):
    if p['slug'] in OPTION_OVERRIDES:
        return OPTION_OVERRIDES[p['slug']]
    labels = [l for l, _ in p['variants']]
    low = [l.lower() for l in labels]
    if all(l in SIZE_WORDS for l in low):
        return 'Size'
    if any(re.search(r'\d+\s*G\b', l) for l in labels):
        return 'Gauge and length'
    if all('ml' in l.lower() for l in low):
        return 'Volume'
    if any(re.search(r'\d+\s*(cm|mm|m)\b', l) for l in labels):
        return 'Size'
    return 'Type'


def body_html(cat, p, ps):
    o = ['<p>%s</p>' % SEO.esc(p['blurb'])]
    for heading, paras in ps['body']:
        o.append('<h2>%s</h2>' % SEO.esc(heading))
        o.extend('<p>%s</p>' % SEO.esc(t) for t in paras)
    if p['extra']:
        o.append('<h2>Specifications</h2><table>')
        for k, v in p['extra']:
            o.append('<tr><th>%s</th><td>%s</td></tr>' % (SEO.esc(k), SEO.esc(v)))
        o.append('</table>')
    return ''.join(o)


def rows():
    out, manifest, skus = [], [], set()
    for cat in CATEGORIES:
        for p in cat['products']:
            ps = SEO.compose(cat, p)
            opt1 = option_name(p)
            img = I[SHOTS[p['family']][0][0]]
            tags = ','.join([cat['slug'], p['tag'], p['family'], 'launch-range'])
            entries = []
            first = True
            for vi, (vlabel, _) in enumerate(p['variants']):
                for pi, (plabel, cents) in enumerate(p['packs']):
                    code = sku(cat, p, vi, pi)
                    assert code not in skus, 'duplicate SKU %s' % code
                    skus.add(code)
                    r = dict.fromkeys(COLUMNS, '')
                    r['Handle'] = p['slug']
                    r['Option1 Name'] = opt1
                    r['Option1 Value'] = vlabel
                    r['Option2 Name'] = 'Pack'
                    r['Option2 Value'] = plabel
                    r['Variant SKU'] = code
                    r['Variant Grams'] = '0'
                    r['Variant Inventory Tracker'] = 'shopify'
                    r['Variant Inventory Qty'] = '0'
                    r['Variant Inventory Policy'] = 'deny'
                    r['Variant Fulfillment Service'] = 'manual'
                    r['Variant Price'] = '%.2f' % (cents / 100.0)
                    r['Variant Requires Shipping'] = 'TRUE'
                    r['Variant Taxable'] = 'TRUE'
                    if first:
                        r['Title'] = p['name']
                        r['Body (HTML)'] = body_html(cat, p, ps)
                        r['Vendor'] = SEO.BRAND
                        r['Type'] = cat['name']
                        r['Tags'] = tags
                        r['Published'] = 'FALSE'
                        r['Image Src'] = img
                        r['Image Position'] = '1'
                        r['Image Alt Text'] = p['name']
                        r['SEO Title'] = ps['title']
                        r['SEO Description'] = ps['desc']
                        r['Status'] = 'draft'
                        first = False
                    out.append(r)
                    entries.append({'sku': code, 'option1': vlabel,
                                    'option2': plabel, 'price_cents': cents,
                                    'variant_id': None})
            manifest.append({'handle': p['slug'], 'name': p['name'],
                             'category': cat['slug'], 'product_id': None,
                             'variants': entries})
    return out, manifest


def main():
    data, manifest = rows()
    OUT.mkdir(exist_ok=True)
    with io.open(OUT / 'shopify-products.csv', 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(data)
    io.open(OUT / 'variant-map.json', 'w', encoding='utf-8').write(
        json.dumps(manifest, indent=1, ensure_ascii=False) + '\n')
    handles = len(manifest)
    print('shopify export: %d products, %d variants -> export/shopify-products.csv'
          % (handles, len(data)))
    print('variant map stub written, %d ids to fill after import' % len(data))


if __name__ == '__main__':
    main()
