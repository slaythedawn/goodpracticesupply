# Title, description and structured data for every page that is not a shop page.
#
# The shop had all of this and the rest of the site had none of it, which was the
# wrong way round the moment the content went indexable and the shop did not.
#
# Descriptions are written, not generated. They are the sentence under the link
# in a search result, and a machine-assembled one reads like a machine assembled
# it. Keep them between about 120 and 165 characters.

import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo as SEO
from content import PAGES

HERO = ('https://d8j0ntlcm91z4.cloudfront.net/user_302vtY04kC9nbtUjJJAhLoDVMFw/'
        'hf_20260914_230224_9a313bac-1e72-4681-ae86-93b0d6fd46f8.png')

# path -> title, description, schema kind, image
FIXED = {
 '/': dict(
   title='Medical supplies for clinics and home',
   desc=('Syringes, needles, gloves, dressings and diagnostics, with every price '
         'on the page and no account needed. Dispatched from Sydney, Australia wide.'),
   kind='home', image=HERO),

 '/about': dict(
   title='About Good Practice Supply',
   desc=('Why we put every price on the page when nobody else in Australian medical '
         'consumables does, and what we will and will not supply.'),
   kind='AboutPage'),

 '/contact': dict(
   title='Contact us',
   desc=('How to reach a person about an order, delivery or a clinic account. '
         'Consumables questions answered seven days, from Sydney.'),
   kind='ContactPage'),

 '/learn': dict(
   title='Guides',
   desc=('Plain explanations of the things people get wrong about needles, gauges, '
         'reconstitution and sharps disposal in Australia. No product pitch.'),
   kind='CollectionPage'),

 '/gauge-finder': dict(
   title='Gauge Finder',
   desc=('Three plain questions and you have the needle gauge and length that suit '
         'you. Nothing is stored, nothing is sent, and we never ask what you inject.'),
   kind='WebApplication'),

 '/always-stocked': dict(
   title='Always Stocked',
   desc=('A standing order that arrives before you run out. Set the cadence, change '
         'or skip any delivery, and stop paying attention to the boring things.'),
   kind='WebPage'),

 '/clinic-portal': dict(
   title='Clinic Portal',
   desc=('Tiered pricing, one login for the whole practice and order support seven '
         'days. Apply with an ABN and we set your pricing from there.'),
   kind='WebPage'),

 '/learn/needle-gauge-chart': dict(
   title='Needle gauge chart',
   desc=('Every needle gauge with its hub colour, outer diameter in millimetres and '
         'what it is actually used for. The scale runs backwards, and here is why.'),
   kind='Article'),

 '/tools/reconstitution-calculator': dict(
   title='Peptide reconstitution calculator',
   desc=('Enter the vial strength and the water you added, and read the dose off the '
         'barrel in units. Works for any U-100 syringe. Nothing is stored.'),
   kind='WebApplication'),
}

CRUMBS = {
 '/about': [('Home', '/'), ('About', '/about')],
 '/contact': [('Home', '/'), ('Contact', '/contact')],
 '/learn': [('Home', '/'), ('Guides', '/learn')],
 '/gauge-finder': [('Home', '/'), ('Gauge Finder', '/gauge-finder')],
 '/always-stocked': [('Home', '/'), ('Always Stocked', '/always-stocked')],
 '/clinic-portal': [('Home', '/'), ('Clinic Portal', '/clinic-portal')],
 '/learn/needle-gauge-chart': [('Home', '/'), ('Guides', '/learn'),
                               ('Needle gauge chart', '/learn/needle-gauge-chart')],
 '/tools/reconstitution-calculator': [('Home', '/'), ('Guides', '/learn'),
                                      ('Reconstitution calculator',
                                       '/tools/reconstitution-calculator')],
}


# Written rather than clipped from the lead paragraph. A description cut at the
# first full stop reads like a description cut at the first full stop.
GUIDE_DESC = {
 'glp-1-injections':
   'Pen needles or syringes, swabs and a sharps container, and how to tell which '
   'you need. The medicine comes from your pharmacy; this is everything else.',
 'trt-injections':
   'Drawing needles, injecting needles and the gauges that suit an oil. Why you '
   'draw with one needle and inject with another, and what length to use.',
 'peptide-reconstitution':
   'Mixing, storing and drawing up, including how much water to add and what the '
   'number on the barrel means afterwards. With a calculator that does the maths.',
 'diabetes-at-home':
   'Testing and injecting day to day: strips and lancets that match your meter, '
   'U-100 syringes or pen needles, and where the used ones are meant to go.',
 'wound-care-at-home':
   'Cleaning, dressing and covering a wound at home. Which dressing suits which '
   'wound, when to change it, and when it is time to see somebody instead.',
 'clinic-fit-out':
   'The full consumables list for a new treatment room, by category, with the '
   'quantities a practice actually gets through in the first month.',
}


def guide(p):
    """A /for/ page. Title, image and FAQ come from content.py so they cannot
    drift from the copy on the page; the description is written here."""
    path = '/for/' + p['slug']
    return path, dict(title=p['title'], desc=GUIDE_DESC[p['slug']],
                      kind='Article', image=p['img'], faq=p['faq'])


def all_pages():
    out = dict(FIXED)
    for p in PAGES:
        path, d = guide(p)
        out[path] = d
    return out


def blocks(path, meta):
    """Head tags plus every piece of structured data this page should carry."""
    kind = meta['kind']
    image = meta.get('image')
    og_kind = 'article' if kind == 'Article' else 'website'
    o = [SEO.head_tags(path=path, title=meta['title'], description=meta['desc'],
                       image=image, kind=og_kind)]
    if path == '/':
        o.append(SEO.jsonld(SEO.organization()))
        o.append(SEO.jsonld(SEO.website()))
    elif kind == 'Article':
        o.append(SEO.jsonld(SEO.article(path=path, headline=meta['title'],
                                        description=meta['desc'], image=image)))
    elif kind == 'WebApplication':
        o.append(SEO.jsonld(SEO.web_application(path=path, name=meta['title'],
                                                description=meta['desc'], image=image)))
    else:
        o.append(SEO.jsonld(SEO.web_page(path=path, kind=kind, name=meta['title'],
                                         description=meta['desc'], image=image)))
    crumbs = CRUMBS.get(path)
    if crumbs is None and path.startswith('/for/'):
        crumbs = [('Home', '/'), ('Guides', '/learn'), (meta['title'], path)]
    if crumbs:
        o.append(SEO.jsonld(SEO.breadcrumbs(crumbs)))
    faq = meta.get('faq')
    if faq:
        o.append(SEO.jsonld(SEO.faq_schema(faq)))
    return '\n'.join(o)
