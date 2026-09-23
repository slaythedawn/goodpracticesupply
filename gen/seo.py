# Search data for the shop.
#
# Two things live here. The head tags and structured data that every category
# and product page emits, and the written copy that gives each page something
# worth ranking. Thin pages do not rank, and fifty-seven near-identical product
# pages are worse than none, so every page gets body copy and questions that are
# its own.
#
# The Target 10 from the sourcing shortlist, plus the starred items on tab 2,
# are written by hand because they are the launch range. The rest are composed
# from their own spec, variants and packs, which are different for every product,
# so no two pages come out the same.

import re

ORIGIN = 'https://goodpracticesupply.com.au'
BRAND = 'Good Practice Supply'

# Two switches, deliberately independent of each other.
#
# PURCHASABLE is whether anyone can complete an order. It is off: no factory has
# quoted, so every price in catalogue.py is invented. While it is off the buy
# button reads "Coming soon", nothing is added to a cart, and the Product
# structured data carries no offers block. A price in structured data is a
# machine-readable offer to sell at that price, and an offer you cannot honour
# is not a thing to publish.
PURCHASABLE = False

# Indexing is per section, because the content and the catalogue are ready at
# different times. The guides, the tools and the fixed pages are finished
# writing and are the pages that earn authority, so they index.
INDEX_CONTENT = True

# The shop splits in two, because the two halves have different problems.
#
# The eight category pages carry 380 to 616 words of copy written by hand, and
# their URLs survive any change to the catalogue: /shop/syringes-needles will
# still be the syringes page when the real syringes arrive. Indexing them now
# starts the clock on a new domain, and an aged, crawled URL is worth more on
# the day products land than a fresh one.
INDEX_SHOP_CATEGORIES = True

# The fifty-seven product pages are the opposite. Every price is invented, and
# every product is a placeholder that will be replaced, which means these slugs
# will not survive. Indexing them teaches Google to crawl URLs that are going to
# die, and publishes prices nobody can honour. Flip this the day the catalogue is
# real, together with PURCHASABLE.
INDEX_SHOP_PRODUCTS = False


def indexable(path):
    """Whether a path should carry an index directive.

    /shop and /shop/<category> follow INDEX_SHOP_CATEGORIES.
    /shop/<category>/<product> follows INDEX_SHOP_PRODUCTS.
    """
    if path == '/shop' or path == '/shop/':
        return INDEX_SHOP_CATEGORIES
    if path.startswith('/shop/'):
        rest = path[len('/shop/'):].strip('/')
        depth = len([seg for seg in rest.split('/') if seg])
        return INDEX_SHOP_CATEGORIES if depth <= 1 else INDEX_SHOP_PRODUCTS
    return INDEX_CONTENT


def robots(path):
    return ('index, follow, max-image-preview:large, max-snippet:-1'
            if indexable(path) else 'noindex, nofollow')


def robots_meta(path):
    return '<meta name="robots" content="%s">' % robots(path)


# headmeta.py fences the block it injects into the hand-written pages. Anything
# that slices a shell out of about.html has to strip it, or every generated page
# inherits About's canonical and About's structured data.
HEADMETA_OPEN, HEADMETA_CLOSE = '<!-- gen:headmeta -->', '<!-- /gen:headmeta -->'
_FENCE = re.compile(re.escape(HEADMETA_OPEN) + r'.*?' + re.escape(HEADMETA_CLOSE) + r'\n?', re.S)


def strip_headmeta(html):
    return _FENCE.sub('', html)


def set_robots(head, path):
    """Swap whatever robots meta a shell carries for the right one.

    The shell is sliced out of docs/about.html, which is itself a page with its
    own robots tag, so matching on one exact value breaks the moment that page
    changes. Match the tag, not its contents.
    """
    out, n = re.subn(r'<meta name="robots" content="[^"]*">', robots_meta(path), head, count=1)
    assert n == 1, 'no robots meta in shell for ' + path
    return out


def esc(t):
    return (str(t).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&quot;'))


def clamp(text, n=158):
    """Meta descriptions are cut at about 160 characters, so cut on a word."""
    text = ' '.join(str(text).split())
    if len(text) <= n:
        return text
    cut = text[:n]
    return cut[:cut.rfind(' ')].rstrip(' ,.;:') + '.'


# --------------------------------------------------------------- head tags
def head_tags(*, path, title, description, image=None, kind='website'):
    """Canonical, description, Open Graph and Twitter, as one block."""
    url = ORIGIN + path
    image = image or DEFAULT_OG
    o = []
    a = o.append
    a('<meta name="description" content="%s">' % esc(description))
    a('<link rel="canonical" href="%s">' % esc(url))
    a('<meta property="og:type" content="%s">' % kind)
    a('<meta property="og:site_name" content="%s">' % esc(BRAND))
    a('<meta property="og:locale" content="en_AU">')
    a('<meta property="og:title" content="%s">' % esc(title))
    a('<meta property="og:description" content="%s">' % esc(description))
    a('<meta property="og:url" content="%s">' % esc(url))
    if image:
        a('<meta property="og:image" content="%s">' % esc(image))
        a('<meta name="twitter:card" content="summary_large_image">')
        a('<meta name="twitter:image" content="%s">' % esc(image))
    else:
        a('<meta name="twitter:card" content="summary">')
    a('<meta name="twitter:title" content="%s">' % esc(title))
    a('<meta name="twitter:description" content="%s">' % esc(description))
    return '\n'.join(o)


def jsonld(obj):
    import json
    return ('<script type="application/ld+json">%s</script>'
            % json.dumps(obj, ensure_ascii=False, separators=(',', ':')))


def breadcrumbs(items):
    """items: [(name, path or None)] in order, root first."""
    return {
        '@context': 'https://schema.org',
        '@type': 'BreadcrumbList',
        'itemListElement': [
            dict(**{'@type': 'ListItem', 'position': i + 1, 'name': name},
                 **({'item': ORIGIN + path} if path else {}))
            for i, (name, path) in enumerate(items)
        ],
    }


def faq_schema(pairs):
    return {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        'mainEntity': [{
            '@type': 'Question',
            'name': q,
            'acceptedAnswer': {'@type': 'Answer', 'text': a},
        } for q, a in pairs],
    }


def product_schema(*, path, name, description, image, sku, price_cents, category, in_stock=True):
    d = {
        '@context': 'https://schema.org',
        '@type': 'Product',
        'name': name,
        'description': description,
        'image': image,
        'sku': sku,
        'category': category,
        'brand': {'@type': 'Brand', 'name': BRAND},
    }
    if not PURCHASABLE:
        # Everything above is a true description of the product. An offers block
        # would be a price we are not yet in a position to honour.
        return d
    d['offers'] = {
            '@type': 'Offer',
            'url': ORIGIN + path,
            'priceCurrency': 'AUD',
            'price': '%.2f' % (price_cents / 100.0),
            'availability': 'https://schema.org/%s' % ('InStock' if in_stock else 'OutOfStock'),
            'itemCondition': 'https://schema.org/NewCondition',
            'seller': {'@type': 'Organization', 'name': BRAND},
            'shippingDetails': {
                '@type': 'OfferShippingDetails',
                'shippingDestination': {'@type': 'DefinedRegion', 'addressCountry': 'AU'},
            },
    }
    return d


# ------------------------------------------------------- site-wide entities
LOGO = ORIGIN + '/icon-512.png'

# Shared links used to render as a grey box on eighteen pages: the ten guides,
# the tools and the hand-written pages all called head_tags without an image.
# A photograph of the range is a better default than nothing, and a page with
# something more specific to say still passes its own.
DEFAULT_OG = ('https://d8j0ntlcm91z4.cloudfront.net/user_302vtY04kC9nbtUjJJAhLoDVMFw/'
              'hf_20260912_014655_c87ec5d7-96f6-4729-b6ef-fc062184ab3f.png')


def organization():
    """The brand entity. One per site, on the homepage.

    No contactPoint and no sameAs: there is no mailbox answering yet and no
    social profile to point at. An entity that claims a contact channel nobody
    reads is worse than one that claims none.
    """
    return {
        '@context': 'https://schema.org',
        '@type': 'Organization',
        '@id': ORIGIN + '/#organization',
        'name': BRAND,
        'url': ORIGIN,
        'logo': LOGO,
        'description': ('Australian supplier of medical consumables to clinics and '
                        'to people managing treatment at home. Consumables only.'),
        'areaServed': {'@type': 'Country', 'name': 'Australia'},
    }


def website():
    """WebSite, with the search the header actually runs.

    The SearchAction target is a real URL: search.js reads ?q= on load and opens
    the overlay with it. Declaring a search endpoint that does not exist is the
    usual way this markup goes wrong.
    """
    return {
        '@context': 'https://schema.org',
        '@type': 'WebSite',
        '@id': ORIGIN + '/#website',
        'url': ORIGIN,
        'name': BRAND,
        'publisher': {'@id': ORIGIN + '/#organization'},
        'inLanguage': 'en-AU',
        'potentialAction': {
            '@type': 'SearchAction',
            'target': {'@type': 'EntryPoint',
                       'urlTemplate': ORIGIN + '/?q={search_term_string}'},
            'query-input': 'required name=search_term_string',
        },
    }


def web_page(*, path, kind, name, description, image=None):
    """AboutPage, ContactPage, CollectionPage or plain WebPage."""
    d = {
        '@context': 'https://schema.org',
        '@type': kind,
        'url': ORIGIN + path,
        'name': name,
        'description': description,
        'isPartOf': {'@id': ORIGIN + '/#website'},
        'inLanguage': 'en-AU',
    }
    if image:
        d['primaryImageOfPage'] = image
    return d


def article(*, path, headline, description, image=None):
    d = {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'url': ORIGIN + path,
        'headline': headline,
        'description': description,
        'inLanguage': 'en-AU',
        'isPartOf': {'@id': ORIGIN + '/#website'},
        'publisher': {'@id': ORIGIN + '/#organization'},
        'author': {'@id': ORIGIN + '/#organization'},
    }
    if image:
        d['image'] = image
    return d


def web_application(*, path, name, description, image=None):
    """The Gauge Finder and the calculator. They run in the browser and are free.

    No aggregateRating: there are no ratings, and inventing them is the single
    most common way this markup earns a manual action.
    """
    d = {
        '@context': 'https://schema.org',
        '@type': 'WebApplication',
        'url': ORIGIN + path,
        'name': name,
        'description': description,
        'applicationCategory': 'HealthApplication',
        'operatingSystem': 'Any',
        'browserRequirements': 'Requires JavaScript',
        'inLanguage': 'en-AU',
        'publisher': {'@id': ORIGIN + '/#organization'},
        'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'AUD'},
    }
    if image:
        d['image'] = image
    return d


def item_list(products, cat_slug):
    return {
        '@context': 'https://schema.org',
        '@type': 'ItemList',
        'itemListElement': [{
            '@type': 'ListItem',
            'position': i + 1,
            'name': p['name'],
            'url': '%s/shop/%s/%s' % (ORIGIN, cat_slug, p['slug']),
        } for i, p in enumerate(products)],
    }


# ------------------------------------------------- hand written, launch range
# slug -> title, desc, body sections, questions.
# body: list of (heading, [paragraph, ...])
# faq:  list of (question, answer)
PRODUCT_SEO = {

'u-100-insulin-syringes': dict(
 title='U-100 insulin syringes, box of 100',
 desc='U-100 insulin syringes with a fixed needle, 27G to 31G, graduated in units. Box of 100, priced on the page, no account needed. Dispatched from Sydney.',
 body=[
  ('What a U-100 insulin syringe is', [
   'U-100 means the barrel is graduated for insulin at a concentration of 100 units per millilitre. One hundred units fills one millilitre, so a unit mark is one hundredth of a millilitre. That is the whole reason these exist: at that scale a millilitre scale is unreadable, and a unit scale is not.',
   'The needle is fixed rather than screwed on, which removes the dead space where a luer fitting would be. On a small dose that dead space is a meaningful share of what you drew up, which is why a fixed needle syringe is the standard choice for anything measured in units rather than millilitres.',
   'These are single use and sterilised with ethylene oxide. They are consumables. Whatever goes in them comes from your pharmacy on a prescription, and we have nothing to do with that part.',
  ]),
  ('Which gauge and length to choose', [
   'Gauge is thickness and the scale runs backwards, so 31G is finer than 29G. A finer needle is noticeably more comfortable and draws more slowly, because you are pulling the same volume through a smaller hole. A thicker one fills faster and is easier to feel going in.',
   'Length decides what layer you land in. For an injection into the fat under the skin, the shortest needle available is the one to reach for, and Australian and international diabetes guidance has moved that way for exactly this reason: a short needle is very unlikely to reach muscle whatever your body size.',
   'If you are not certain which pair you want, the Gauge Finder asks three plain questions and tells you, without asking what you are injecting.',
  ]),
 ],
 faq=[
  ('Do I need a prescription to buy insulin syringes in Australia?',
   'No. Syringes and needles are consumables and you can buy them here without an account or a script. The medicine you are injecting is a different matter and comes from your pharmacy.'),
  ('What is the difference between U-100 and U-40 syringes?',
   'The graduations. A U-100 syringe is marked for insulin at 100 units per millilitre and a U-40 syringe for 40 units per millilitre. They are not interchangeable, and U-40 is mostly a veterinary concentration in Australia. Read the vial before you choose the syringe.'),
  ('Is 27G too thick for a subcutaneous injection?',
   '27G is a common and perfectly workable choice, and it is what the reference product for our launch range uses. Finer gauges from 29G to 31G are more comfortable and slower to draw. Comfort is the only thing that changes, provided the needle is long enough to clear the skin.'),
  ('How do I dispose of used insulin syringes?',
   'In a sharps container, never in household waste, anywhere in Australia. What happens to a full container depends on your state or territory, and our guide to sharps disposal covers each of them.'),
 ],
),

'bacteriostatic-water': dict(
 title='Bacteriostatic water for injection, 10mL and 30mL',
 desc='Bacteriostatic water for injection in 10mL and 30mL multi-dose glass vials, with 0.9% benzyl alcohol. Priced on the page, no account needed.',
 body=[
  ('What bacteriostatic water is', [
   'Sterile water with 0.9% benzyl alcohol added as a preservative. The preservative is what makes the vial multi-dose: it suppresses bacterial growth after the stopper has been punctured, so the vial can be entered more than once within the period its instructions allow.',
   'That is the entire difference between this and sterile water for injection, which has no preservative and is single use. Both are diluents. Neither is a medicine.',
  ]),
  ('10mL or 30mL', [
   'Pick on how much you will use before the vial expires after first entry rather than on price per millilitre. A 30mL vial that gets discarded half used is more expensive than two 10mL vials that get finished.',
   'The vial is glass with a rubber stopper and an aluminium crimp. Swab the stopper before every entry, and use a drawing-up needle rather than the needle you are injecting with, because coring the stopper blunts a needle fast.',
  ]),
 ],
 faq=[
  ('What is the difference between bacteriostatic water and sterile water for injection?',
   'Bacteriostatic water contains 0.9% benzyl alcohol as a preservative, which lets the vial be entered more than once. Sterile water for injection has no preservative and is single use. Which one you need is a question for your prescriber, not for us.'),
  ('How long does a bacteriostatic water vial last once opened?',
   'The instructions on the carton give the in-use period after first entry, and that is the number to follow. It is shorter than the printed expiry, which applies to an unopened vial.'),
  ('Do you sell peptides or any medicine to go with this?',
   'No. Good Practice Supply supplies consumables only. We do not stock peptides, hormones or any prescription medicine, and we have no view on what goes in the vial.'),
 ],
),

'alcohol-swabs': dict(
 title='Alcohol swabs, 70% isopropyl, box of 100 or 200',
 desc='70% isopropyl alcohol swabs, two ply non-woven, individually foil wrapped, about 65 x 30mm. Box of 100 or 200, priced on the page, no account needed.',
 body=[
  ('What is in the sachet', [
   'A two ply non-woven pad saturated with 70% isopropyl alcohol, sealed in its own foil sachet so it is still wet when you open it. About 65 by 30mm opened out, which is the size that covers a stopper top and a patch of skin without folding.',
   'Seventy per cent rather than higher is deliberate. Alcohol needs water present to work on a bacterial cell wall, and neat isopropyl evaporates before it has done the job. Stronger is not better here.',
  ]),
  ('Buying them', [
   'Two swabs per injection is the normal rate, one for the top of the vial or the pen and one for the skin, which is why these run out faster than anyone expects. The 200 box works out cheaper per swab than the 100 and takes up almost the same shelf.',
   'Let the skin dry before the needle goes in. Alcohol stings on a wet injection site, and it has not finished working until it has evaporated.',
  ]),
 ],
 faq=[
  ('Are alcohol swabs and alcohol wipes the same thing?',
   'For this purpose, yes. Both names describe a small individually wrapped pad of 70% isopropyl for skin and stopper prep. Larger surface wipes for benches are a different product and are in clinic and disposal.'),
  ('Why 70% isopropyl rather than a higher concentration?',
   'Alcohol needs water present to break down a bacterial cell wall, and above about 80% it evaporates before it has done that. Seventy per cent is the effective concentration, not the cheap one.'),
  ('Do I need to let the swab dry before injecting?',
   'Yes. It stings otherwise, and the alcohol has not finished working until it has evaporated.'),
 ],
),

'hypodermic-needles': dict(
 title='Hypodermic needles, 18G to 25G, ISO colour coded',
 desc='Sterile hypodermic needles in the gauges people actually use, 18G to 25G, ISO colour coded hubs, 1 to 1.5 inch. Box of 100, priced on the page.',
 body=[
  ('Reading a needle', [
   'Two numbers describe a needle and they do different jobs. Gauge is the outer diameter and the scale runs backwards, so 25G is finer than 23G. Length decides the layer you land in: under the skin, or through it into muscle.',
   'The hub colour follows ISO 6009, so 23G is blue and 25G is orange across every manufacturer that follows it. Manufacturers occasionally differ, so read the carton rather than trusting the colour alone. Our needle gauge chart lists every gauge with its outer diameter in millimetres.',
  ]),
  ('Intramuscular and subcutaneous', [
   'An intramuscular injection has to clear skin and fat to reach muscle, which is why 23G to 25G at one inch to one and a half is the usual range. Too short and it goes into fat instead of muscle; the right length depends on the site and on the person.',
   'Anything under the skin wants shorter and finer. If you are drawing from a vial and injecting with the same needle you are blunting it on the stopper, so draw up with an 18G and swap.',
  ]),
 ],
 faq=[
  ('What size needle is used for an intramuscular injection?',
   'Commonly 23G to 25G at one inch to one and a half inches, but the right length depends on the site and the person, and that is a question for your prescriber rather than for us.'),
  ('What does the colour of the needle hub mean?',
   'It encodes the gauge under ISO 6009. Read the carton rather than trusting the colour alone, because manufacturers occasionally differ.'),
  ('Can I buy needles without a prescription in Australia?',
   'Yes. Needles are consumables and there is no script and no account required to buy them here.'),
 ],
),

'drawing-up-needles': dict(
 title='Drawing-up needles, 18G, box of 100',
 desc='Sterile 18G drawing-up and reconstitution needles, blunt or sharp fill, box of 100. Priced on the page, no account needed, dispatched from Sydney.',
 body=[
  ('Why a separate needle to draw up', [
   'Pushing a needle through a rubber stopper blunts it and can core a plug of rubber out of the stopper. Doing that with the needle you are about to inject with is the single most avoidable cause of an injection hurting more than it needs to.',
   'An 18G draws fast, which matters when you are pulling a viscous diluent or a full millilitre. You swap it for the injecting needle before the needle goes anywhere near skin.',
  ]),
  ('Blunt fill or sharp fill', [
   'A blunt fill needle will not pierce an unvented stopper, so it is for vials with a pierceable septum designed for it, and for drawing from an ampoule. A sharp fill will go through a standard rubber stopper.',
   'If you are entering the same vial repeatedly, a vial access device is a better answer than either, because it seats once and gives you a luer port to attach to.',
  ]),
 ],
 faq=[
  ('Can I inject with a drawing-up needle?',
   'You can, but it is the wrong tool and it will hurt. An 18G is thick, and it is blunt after the stopper. Swap to the injecting needle before it touches skin.'),
  ('What is the difference between blunt fill and sharp fill?',
   'A blunt fill needle will not pierce a standard rubber stopper and is for ampoules and septa designed for it. A sharp fill will go through a stopper.'),
 ],
),

'luer-lock-syringes': dict(
 title='Luer-lock syringes, 1mL and 3mL, box of 100',
 desc='Three part luer-lock syringes in 1mL, 3mL, 5mL and 10mL, sterile single use, box of 100. Priced on the page, no account needed.',
 body=[
  ('What the lock is for', [
   'A luer-lock tip has a thread, so the needle screws on and stays on. A luer-slip pushes on by friction. The difference only matters under pressure, and under pressure it matters a great deal: a slip fitting can separate while you are pushing, which is exactly when you do not want it to.',
   'Three part means there is a rubber tip on the plunger, which is what makes the action smooth and the seal reliable. Two part syringes are cheaper and stickier.',
  ]),
  ('Choosing a volume', [
   'Pick the smallest barrel your dose fits in. A dose measured near the bottom of a 10mL barrel is far harder to read accurately than the same dose most of the way up a 1mL, because the graduations are further apart on the smaller barrel.',
   'For anything you are drawing from a vial, use a drawing-up needle to fill and swap to the injecting needle before you inject.',
  ]),
 ],
 faq=[
  ('What is the difference between luer-lock and luer-slip?',
   'A luer-lock needle screws on and cannot be pushed off. A luer-slip pushes on by friction. Use a lock for anything under pressure.'),
  ('Which syringe size should I use?',
   'The smallest one your dose fits in, because the graduations are further apart and easier to read accurately on a smaller barrel.'),
  ('Are these sterile?',
   'Yes, sterilised with ethylene oxide, single use, individually wrapped.'),
 ],
),

'sterile-water-for-injection': dict(
 title='Sterile water for injection, 10mL plastic ampoule',
 desc='Preservative-free sterile water for injection, 10mL plastic ampoule, box of 20 to 50. Priced on the page, no account needed, dispatched from Sydney.',
 body=[
  ('Preservative free, single use', [
   'Water for injection with nothing added. No preservative, which means no benzyl alcohol, which means the ampoule is single use: once it is open there is nothing in it suppressing bacterial growth, so what is left over gets discarded rather than kept.',
   'That is the difference between this and bacteriostatic water, and it is the only difference that matters. Which one you need is a question for your prescriber.',
  ]),
  ('Plastic ampoule rather than glass', [
   'A plastic ampoule twists open rather than snapping, so there is no glass to break off and no filter needed to draw past shards. It is the safer format for anyone doing this at a kitchen bench rather than at a bench with a sharps bin under it.',
  ]),
 ],
 faq=[
  ('Can I reuse a sterile water ampoule?',
   'No. There is no preservative in it, so once it is open it is single use. Bacteriostatic water is the multi-dose option.'),
  ('Is sterile water for injection the same as distilled water?',
   'No. Water for injection is manufactured and tested to a pharmacopoeial standard for particulates, endotoxins and sterility. Distilled water is not.'),
 ],
),

'chlorhexidine-skin-prep': dict(
 title='Chlorhexidine skin prep, 0.5% to 2% in 70% alcohol',
 desc='Chlorhexidine gluconate 0.5% to 2% in 70% alcohol, as swabsticks or a single-use applicator. Box of 30 to 100, priced on the page.',
 body=[
  ('Chlorhexidine in alcohol', [
   'Two antiseptics doing two different jobs in the same applicator. The alcohol acts fast and evaporates. The chlorhexidine keeps working after it has dried, which is why the combination is used where the site needs to stay clean for longer than the few seconds an alcohol swab covers.',
   'It has to dry to work. Rushing the needle in while the site is still wet defeats both halves of it, and stings.',
  ]),
  ('Swabstick or applicator', [
   'Swabsticks come in a sachet and suit a small site. A single use applicator holds more solution and is the better choice for a larger field where you want one pass rather than three.',
  ]),
 ],
 faq=[
  ('Chlorhexidine or an alcohol swab?',
   'An alcohol swab is the everyday choice for an injection site. Chlorhexidine in alcohol is used where the site needs to stay clean longer than alcohol alone manages. Follow whatever your prescriber or your practice protocol specifies.'),
  ('How long should chlorhexidine be left to dry?',
   'Until it is visibly dry. The carton gives a time, and that is the one to follow.'),
 ],
),

'sharps-container-bench': dict(
 title='Sharps container, 0.5L and 1.4L, yellow, AS 4031',
 desc='Puncture resistant yellow sharps containers in 0.5L and 1.4L with a finger guard and a lockable lid. Priced on the page, no account needed.',
 body=[
  ('Why a container and not a bottle', [
   'Used needles cannot go in household waste anywhere in Australia. A proper sharps container is rigid polypropylene, puncture resistant, yellow so it is recognisable to whoever handles it next, and it has a temporary closure you can operate one handed and a final closure that cannot be reopened.',
   'A drink bottle fails on every one of those. It is not a container, it is a hazard with a lid on it.',
  ]),
  ('Sizing and filling', [
   'Fill to the line and not past it. The line exists because an overfull container cannot be closed safely, and a container that cannot be closed safely is the problem it was bought to prevent.',
   '0.5L suits a bag or a bathroom cupboard. 1.4L is the bench size for someone injecting regularly. Wall mounted containers for a treatment room are in clinic and disposal.',
  ]),
 ],
 faq=[
  ('Where do I dispose of a full sharps container in Australia?',
   'It depends on your state or territory. Community pharmacies, council collection points and hospital services all play a part, and the arrangements differ. Our guide to sharps disposal sets out what each state does.'),
  ('Can I put needles in the household bin if I cap them first?',
   'No, and recapping is itself the most common way people get a needlestick injury. Use a sharps container.'),
  ('What size sharps container do I need?',
   '0.5L for a bag or a cupboard, 1.4L for a bench if you inject regularly, and a wall mounted container for a treatment room.'),
 ],
),

'vial-access-devices': dict(
 title='Vial access devices, needle-free, 13mm and 20mm',
 desc='Needle-free vial adapters with a luer-lock port, for 13mm and 20mm vial necks. Sterile, single use, priced on the page, no account needed.',
 body=[
  ('What an adapter replaces', [
   'A vial access device seats on the neck of the vial once, pierces the stopper once, and leaves you a luer-lock port to attach a syringe to. Every entry after that is needle free.',
   'That removes the two problems with entering a stopper repeatedly: the needle blunts, and each pass can core a small plug of rubber into the vial. It also removes a sharp from the part of the process where you are least likely to be paying attention to it.',
  ]),
  ('Getting the neck size right', [
   'Measure the neck, not the vial. 13mm and 20mm are the two common sizes and an adapter for one will not seat on the other. The number is usually on the carton the vial came in.',
   'Most have a vent with a filter, so pressure equalises as you draw rather than fighting you.',
  ]),
 ],
 faq=[
  ('How do I know if I need a 13mm or 20mm adapter?',
   'Measure across the metal crimp at the neck of the vial, or read it off the carton. They are not interchangeable.'),
  ('Can I leave a vial adapter in place between doses?',
   'That is what it is designed for, within the in-use period the vial instructions give. Keep the port capped and swab it before each connection.'),
 ],
),

# --- starred priority items from tab 2 -------------------------------------
'nitrile-examination-gloves': dict(
 title='Nitrile examination gloves, powder free, box of 100',
 desc='Powder-free blue nitrile examination gloves in S, M, L and XL. Box of 100, priced on the page, no account needed, dispatched from Sydney.',
 body=[
  ('Nitrile rather than latex', [
   'Nitrile is a synthetic rubber, so it carries none of the latex protein that causes latex allergy. That is the main reason it has become the default examination glove, in clinics and in the bathroom cupboard both.',
   'It is also more resistant to punctures and to most chemicals than latex, and it tears visibly when it fails rather than stretching, which is useful: you can see that a glove has gone.',
  ]),
  ('Sizing and fit', [
   'A glove that is too big snags and a glove that is too small tires your hand and splits at the web of the thumb. Most people are a size smaller in nitrile than they expect, because it has less give than latex.',
   'Powder free throughout. Powdered gloves have largely gone from Australian practice because the powder carries protein and irritates.',
  ]),
 ],
 faq=[
  ('Are nitrile gloves latex free?',
   'Yes. Nitrile is a synthetic rubber and contains no natural rubber latex protein.'),
  ('What is the difference between examination and surgical gloves?',
   'Examination gloves are non-sterile, ambidextrous and sized in a range. Surgical gloves are sterile, hand specific and sized more finely. For anything short of a sterile procedure, examination grade is the correct choice.'),
  ('Do I need an account to buy gloves by the carton?',
   'No. Carton pricing is on the page like everything else. A Clinic Portal account adds trade rates on top of it, but it is not a gate.'),
 ],
),

'latex-examination-gloves': dict(
 title='Latex examination gloves, powder free, box of 100',
 desc='Powder-free natural rubber latex examination gloves in S, M, L and XL. Box of 100, priced on the page, no account needed.',
 body=[
  ('Why latex is still stocked', [
   'Latex has better tactile sensitivity and more stretch than nitrile, and some people simply work better in it. It remains the preferred glove for a number of procedures for that reason.',
   'The trade off is latex protein, which causes allergy in a small but real proportion of people, wearers and patients both. Any practice stocking latex should also stock nitrile, and should know which of its people cannot wear this.',
  ]),
  ('Powder free', [
   'Powdered latex gloves have largely gone from Australian practice. The powder carries latex protein into the air, which turns a contact allergy into an airborne one.',
  ]),
 ],
 faq=[
  ('Should I stock latex or nitrile gloves?',
   'Nitrile as the default, because it removes the allergy question entirely. Latex where the tactile sensitivity is worth having and nobody involved has a latex allergy.'),
  ('Are these powdered?',
   'No. Powder free only.'),
 ],
),

'surgical-masks-level-2': dict(
 title='Surgical masks, Level 2, Type IIR, box of 50',
 desc='Level 2 (Type IIR) three ply surgical masks with earloops and a fluid resistant outer. Box of 50, priced on the page, no account needed.',
 body=[
  ('What Level 2 means', [
   'Mask levels describe fluid resistance and filtration, not fit. Level 1 is for short procedures with little fluid. Level 2, equivalent to Type IIR, adds a fluid resistant outer layer and is the general purpose clinical mask. Level 3 is for heavy fluid exposure.',
   'Three ply: a filter layer between an outer that resists fluid and an inner that sits against the face. The nose wire is what makes the difference between a mask that works and a mask that fogs your glasses.',
  ]),
  ('A mask is not a respirator', [
   'A surgical mask is a barrier against droplets and splash. It is not a fitted respirator and it does not seal to the face, so it does not do the job of a P2 or N95. The two are not substitutes for one another.',
  ]),
 ],
 faq=[
  ('What is the difference between Level 1, 2 and 3 masks?',
   'Fluid resistance and filtration. Level 2, also called Type IIR, is the general purpose clinical mask and has a fluid resistant outer layer.'),
  ('Is a Level 2 surgical mask the same as a P2 or N95?',
   'No. A surgical mask is a splash and droplet barrier that does not seal to the face. A P2 or N95 is a fitted respirator. They are not interchangeable.'),
 ],
),

'cotton-wool-balls': dict(
 title='Cotton wool balls, 100% cotton, bulk bag',
 desc='Plain 100% cotton wool balls in bulk bags of 500 and 1000, plus tipped applicators. Priced on the page, no account needed.',
 body=[
  ('What they are for', [
   'Pressure after a needle comes out, and prep where a saturated alcohol swab is more than the job needs. Plain cotton, nothing added, non-sterile.',
   'Bulk is the only sensible way to buy these. A jar of fifty from a supermarket costs several times what the same cotton costs in a bag, and a bag lasts a clinic a month.',
  ]),
 ],
 faq=[
  ('Are these sterile?',
   'No. Cotton wool balls are non-sterile. Where you need sterile, use a sterile gauze swab from a pouch.'),
  ('Cotton balls or gauze for pressure after an injection?',
   'Either works. Cotton is softer and cheaper, gauze sheds less and is the better choice on anything that is still open.'),
 ],
),

'adhesive-plasters': dict(
 title='Adhesive plasters, plastic and fabric, box of 100',
 desc='Assorted adhesive plasters in plastic and fabric, latex free adhesive, sterile and individually wrapped. Box of 100, priced on the page.',
 body=[
  ('Plastic, fabric and blue', [
   'Plastic plasters stay put in water and are the right choice for hands that get washed. Fabric plasters flex, so they survive a knuckle or an elbow that a plastic one peels straight off.',
   'Blue detectable plasters exist because a plaster that comes off in food needs to be findable, by eye and by a metal detector. They belong in any kitchen first aid kit and nowhere else.',
  ]),
  ('Buying them', [
   'Assorted rather than a single size, because the one you need is always the one the box has run out of. Latex free adhesive throughout, which matters more than it sounds: plaster adhesive is a common contact allergy.',
  ]),
 ],
 faq=[
  ('Are these plasters latex free?',
   'Yes. Latex free acrylic adhesive throughout.'),
  ('Why are some plasters blue?',
   'So they can be found if they come off in food, by eye and by a metal detector. They are for food handling areas.'),
 ],
),

'vaginal-speculum-disposable': dict(
 title='Vaginal speculum, single use, S, M and L',
 desc='Single-use vaginal speculums in small, medium and large, with or without an integral light. Priced on the page, no account needed.',
 body=[
  ('Single use rather than reprocessed', [
   'A single use speculum removes the reprocessing loop entirely: no soaking, no autoclave cycle, no tracking of how many cycles an instrument has been through. For a practice without a sterilising room that is not a convenience, it is the only workable option.',
   'Moulded polymer, smooth edges, with a locking mechanism that holds position without a thumbscrew to work one handed.',
  ]),
  ('With or without a light', [
   'An integral light source removes the need to position a lamp, which is most of the awkwardness. It adds cost per unit, so most practices stock both and use the lit ones where they help.',
  ]),
 ],
 faq=[
  ('What sizes do disposable speculums come in?',
   'Small, medium and large. Sizing is by blade width and length, and the right one depends on the examination.'),
  ('Can single-use speculums be sterilised and reused?',
   'No. They are single use and are not built to survive a reprocessing cycle.'),
 ],
),

'safety-lancets': dict(
 title='Safety lancets, 28G, single use, box of 100',
 desc='28G single-use safety lancets with a retracting needle that cannot be reused. Box of 100, priced on the page, no account needed.',
 body=[
  ('What makes it a safety lancet', [
   'The needle retracts and locks after it fires, so the lancet cannot be used twice and cannot stick anyone afterwards. That is the whole design, and it is why safety lancets have replaced the older reusable devices nearly everywhere.',
   'They still go in a sharps container. A retracted needle is safer, not absent.',
  ]),
  ('Gauge and depth', [
   'A finer lancet hurts less and yields a smaller drop. 28G is the common compromise. If you are not getting enough blood, warming the hand and letting it hang below heart level does more than going to a thicker lancet.',
  ]),
 ],
 faq=[
  ('Can safety lancets be reused?',
   'No, by design. The needle retracts and locks after firing.'),
  ('Do used lancets go in a sharps container?',
   'Yes. A retracted needle is still a sharp.'),
 ],
),

'incontinence-pads': dict(
 title='Incontinence pads and pants',
 desc='Shaped continence pads and pull-up pants, rated by absorbency rather than size. Packs and cartons priced on the page, no account needed.',
),

}


# ------------------------------------------------------------- categories
# Category pages rank for the broad term. They need a buying guide, not just a
# grid, because the person searching "insulin syringes australia" has not
# decided which one yet.
CATEGORY_SEO = {

'syringes-needles': dict(
 title='Syringes & needles',
 desc='Insulin syringes, luer-lock and luer-slip barrels, hypodermic and drawing-up needles, and vial access devices. Priced on the page, no account needed.',
 guide=[
  ('Gauge, length and why the scale runs backwards', [
   'Gauge is the outer diameter of the needle, and the number goes up as the needle gets finer. A 31G is thinner than a 29G, which is thinner than a 25G. Finer is more comfortable and slower to draw, because you are pulling the same volume through a smaller hole.',
   'Length is the separate question and it decides which layer you land in. Under the skin wants short. Into muscle wants long enough to clear skin and fat first. Our needle gauge chart lists every gauge from 14G to 34G with its outer diameter in millimetres and its ISO hub colour.',
  ]),
  ('Fixed needle or luer fitting', [
   'An insulin syringe has the needle fixed to the barrel, which removes the dead space a luer fitting leaves behind. On a dose measured in units that dead space is a meaningful share of what you drew, so a fixed needle is the standard choice at that scale.',
   'Anything you need to draw with one needle and inject with another wants a luer fitting. Lock where there is pressure, because a slip fitting can separate under it.',
  ]),
  ('Draw with one, inject with another', [
   'Pushing a needle through a rubber stopper blunts it. Draw up with an 18G, swap to the injecting needle, and the injection is noticeably more comfortable. If you are entering the same vial repeatedly, a vial access device does the job better than either.',
  ]),
 ],
 faq=[
  ('Can I buy syringes and needles without a prescription in Australia?',
   'Yes. Syringes, needles, swabs and sharps containers are consumables. You can buy them here without an account and without a script.'),
  ('Which needle gauge is finest?',
   'The highest number. 31G is finer than 29G, which is finer than 25G. The scale runs backwards.'),
  ('What is the difference between an insulin syringe and a luer-lock syringe?',
   'An insulin syringe has a fixed needle and a unit scale, for doses measured in units. A luer-lock syringe has a threaded tip and a millilitre scale, so the needle can be changed.'),
 ],
),

'diluents-swabs': dict(
 title='Diluents & swabs',
 desc='Bacteriostatic and sterile water for injection, 70% alcohol swabs, chlorhexidine and povidone iodine skin prep, saline and cotton wool.',
 guide=[
  ('Bacteriostatic or sterile water', [
   'Bacteriostatic water contains 0.9% benzyl alcohol as a preservative, which is what makes a vial multi-dose: it can be entered more than once within the in-use period its instructions give. Sterile water for injection has no preservative and is single use.',
   'That is the whole difference. Both are diluents, neither is a medicine, and which one you need is a question for your prescriber rather than for us.',
  ]),
  ('Skin prep, in order of how long it keeps working', [
   'An alcohol swab acts fast and stops working as soon as it has evaporated, which is fine for an injection site. Chlorhexidine in alcohol keeps working after it dries. Povidone iodine is the one to reach for where chlorhexidine is contraindicated.',
   'All three have to dry before the needle goes in. Wet prep stings and has not finished working.',
  ]),
 ],
 faq=[
  ('What is the difference between bacteriostatic and sterile water?',
   'Bacteriostatic water has 0.9% benzyl alcohol added as a preservative, so the vial can be entered more than once. Sterile water for injection has no preservative and is single use.'),
  ('Do you sell peptides or hormones?',
   'No. Good Practice Supply supplies consumables only, and that includes diluents. We do not stock peptides, hormones or any prescription medicine.'),
  ('Why 70% isopropyl and not stronger?',
   'Alcohol needs water present to break down a bacterial cell wall. Above about 80% it evaporates before it has done that.'),
 ],
),

'gloves-ppe': dict(
 title='Gloves & PPE',
 desc='Powder-free nitrile and latex examination gloves, Level 2 surgical masks, isolation gowns, aprons on a roll and alcohol hand rub.',
 guide=[
  ('Nitrile or latex', [
   'Nitrile is synthetic and contains no latex protein, which removes the allergy question for wearer and patient both. It is the sensible default. Latex has better tactile feel and more stretch, and is worth stocking alongside rather than instead.',
   'Most people take a smaller size in nitrile than they expect, because it has less give. A glove that is too big snags and one that is too small splits at the web of the thumb.',
  ]),
  ('Mask levels are about fluid, not fit', [
   'Level 1 for short procedures with little fluid, Level 2 (Type IIR) as the general purpose clinical mask with a fluid resistant outer, Level 3 for heavy exposure. None of them seal to the face, so none of them do the job of a fitted P2 or N95.',
  ]),
 ],
 faq=[
  ('Are nitrile gloves latex free?',
   'Yes. Nitrile is a synthetic rubber with no natural rubber latex protein in it.'),
  ('What does Level 2 mean on a surgical mask?',
   'Fluid resistance and filtration, equivalent to Type IIR. It is the general purpose clinical mask.'),
  ('Do you sell gloves by the carton?',
   'Yes, and the carton price is on the page. No account needed to see it.'),
 ],
),

'wound-care': dict(
 title='Wound care',
 desc='Sterile gauze, non-adherent and island dressings, hydrocolloid and foam, fixation tape, crepe and cohesive bandages, plasters, sutures and first aid kits.',
 guide=[
  ('Match the dressing to the moisture', [
   'A dry wound wants something that will not stick to it when it comes off, which is what a non-adherent dressing is for. A wound with light exudate suits hydrocolloid. More exudate than that wants foam, which absorbs and cushions at once.',
   'Gauze is for cleaning, packing and absorbing, not for sitting on a healing surface, because it dries into it and takes the surface with it when you pull.',
  ]),
  ('Holding it on', [
   'Tape for a flat surface, cohesive bandage for an awkward shape, crepe where you want light support as well. Cohesive sticks to itself and not to skin or hair, which is the reason to pay more for it.',
  ]),
 ],
 faq=[
  ('What is the difference between a non-adherent and an island dressing?',
   'A non-adherent dressing is a pad that will not stick to the wound surface and needs taping down. An island dressing has the pad and the adhesive border in one piece.'),
  ('When should I use a hydrocolloid dressing?',
   'On a shallow wound with light exudate, where it can stay in place for several days. Follow the instructions on the box for wear time.'),
  ('Do you sell sterile and non-sterile gauze?',
   'Both. Sterile in pouches for anything open, non-sterile in bulk for cleaning and padding.'),
 ],
),

'diagnostics': dict(
 title='Diagnostics',
 desc='Safety lancets, blood glucose meters and strips, urinalysis strips, thermometer probe covers, otoscope specula, speculums, ECG electrodes and ultrasound gel.',
 guide=[
  ('Meters and strips are a closed pair', [
   'A glucose meter only reads the strip it was designed for. A strip from another maker will not work in it, whatever the price looks like, so buy the strips that match the meter you already have rather than the cheapest strip on the page.',
   'Strips are also the consumable that expires quietly. Keep the tube closed, keep the desiccant in it, and check the date before you trust a reading.',
  ]),
  ('Single use where it touches a patient', [
   'Probe covers, ear specula and speculums are single use for the same reason: they are the part that goes near a patient, and reprocessing them costs more in time and risk than replacing them costs in money.',
   'Check fittings before you order a carton. Otoscope specula are not universal between manufacturers.',
  ]),
 ],
 faq=[
  ('Will any glucose strip work in my meter?',
   'No. Meters and strips are matched pairs. Buy the strips that match your meter.'),
  ('Are otoscope specula universal?',
   'No. Fittings differ between manufacturers, so check one against your otoscope head before ordering in quantity.'),
  ('Do lancets go in a sharps container?',
   'Yes, including safety lancets. A retracted needle is still a sharp.'),
 ],
),

'clinic-disposal': dict(
 title='Clinic & disposal',
 desc='Sharps containers for bench and wall, couch roll, blueys, clinical waste bags, surface wipes and continence products. Priced on the page.',
 guide=[
  ('Sharps containers, and the fill line', [
   'Rigid polypropylene, yellow, puncture resistant, with a temporary closure you can work one handed and a final closure that cannot be reopened. Fill to the line and not past it, because an overfull container cannot be closed safely.',
   'What happens to a full container depends on your state or territory. Our guide to sharps disposal sets out the arrangements in each.',
  ]),
  ('The things that stop a room working', [
   'Couch roll, blueys, waste bags and wipes are nobody’s job to order and everybody’s problem when they run out. This is exactly the category that belongs on a standing order rather than on someone’s memory.',
  ]),
 ],
 faq=[
  ('Can used needles go in the household bin?',
   'No, nowhere in Australia. They go in a sharps container, and recapping before disposal is itself a common cause of needlestick injury.'),
  ('What size sharps container do I need?',
   '0.5L for a bag or a cupboard, 1.4L for a bench, wall mounted for a treatment room.'),
 ],
),

'hygiene-cleaning': dict(
 title='Hygiene & cleaning',
 desc='Liquid hand wash, interleaved hand towels, facial tissues and cotton wool, in pump bottles and bulk refills. Priced on the page, no account needed.',
 guide=[
  ('Buy the refill, not the bottle', [
   'A 500mL pump and a 5L refill hold the same product. Buying pumps repeatedly is the expensive way to run a basin, and it produces a bottle a fortnight that nobody wanted.',
   'pH neutral for hands washed twenty times a day. Antibacterial where a protocol calls for it, not as a default, because it is harsher on skin that is already being washed constantly.',
  ]),
  ('Interleaved beats roll at a clinical basin', [
   'One towel comes out and the next one waits, so the dispenser is touched once with wet hands rather than turned with them. Slimfold fits the standard dispenser, which is most of them.',
  ]),
 ],
 faq=[
  ('What is the difference between slimfold and ultraslim hand towels?',
   'The fold and the dispenser they fit. Slimfold suits the standard dispenser, ultraslim the compact one. Check the dispenser before ordering a carton.'),
  ('Should I use antibacterial hand wash?',
   'Where a protocol calls for it. As a default, a pH neutral wash is kinder to hands that are being washed all day.'),
 ],
),

'taping-supports': dict(
 title='Taping & supports',
 desc='Rigid zinc oxide strapping tape, elastic adhesive bandage, kinesiology tape and Class 1 compression stockings. Priced on the page, no account needed.',
 guide=[
  ('Rigid anchors, elastic survives the session', [
   'Rigid zinc oxide tape does not stretch, which is the point of it: it is what stops a joint going where you do not want it to. Elastic adhesive bandage over the top lets the limb move without the strapping peeling off.',
   'They are bought together and used together. A rigid tape job with no elastic over it comes apart; an elastic job with no rigid anchor does not restrict anything.',
  ]),
  ('Kinesiology tape is a different job', [
   'Cotton elastic with a wave pattern adhesive, cut to shape, worn for days. It does not restrict a joint, which is the opposite of what strapping is for, so it is not a substitute for it.',
  ]),
  ('Compression is sized on measurement', [
   'Class 1 knee high stockings are sized on ankle and calf circumference, not on shoe size. A stocking that is too big does nothing and one that is too small does not get worn.',
  ]),
 ],
 faq=[
  ('What is the difference between rigid strapping tape and EAB?',
   'Rigid zinc oxide tape does not stretch and does the anchoring. Elastic adhesive bandage stretches and goes over the top so the strapping moves with the limb.'),
  ('Is kinesiology tape the same as strapping tape?',
   'No. Kinesiology tape stretches and does not restrict a joint. Strapping tape is rigid and does.'),
  ('How are compression stockings sized?',
   'On ankle and calf circumference, not shoe size.'),
 ],
),

}


# ----------------------------------------------- composed copy for the rest
def lower_name(name):
    """Lowercase a product name for mid-sentence use, without wrecking it.

    "Crepe bandages" wants lowercasing. "U-100 insulin syringes" and "ECG
    electrodes" do not, and "Questions about u-100 insulin syringes" is the kind
    of detail that makes a page look machine written.
    """
    first = name.split(' ', 1)[0]
    if first.isupper() or any(ch.isdigit() for ch in first):
        return name
    return name[0].lower() + name[1:]


def _sentence_list(items):
    items = list(items)
    if len(items) == 1:
        return items[0]
    return ', '.join(items[:-1]) + ' and ' + items[-1]


def compose(cat, p):
    """SEO copy for a product with no hand written entry.

    Everything here is built from that product's own spec, options, pack sizes
    and spec table, all of which differ product to product, so two pages never
    come out reading the same. It is thinner than the hand written launch range
    and it is meant to be.
    """
    seo = dict(PRODUCT_SEO.get(p['slug'], {}))
    if seo.get('body') and seo.get('faq'):
        seo.setdefault('title', p['name'])
        seo.setdefault('desc', clamp('%s. %s. Priced on the page, no account needed, dispatched from Sydney.'
                                     % (p['name'], p['spec'])))
        return seo

    extra = dict(p['extra'])
    opts = [v[0] for v in p['variants']]
    packs = [k[0] for k in p['packs']]

    title = seo.get('title') or '%s, %s' % (p['name'], p['spec'].split(',')[0].strip().lower())
    desc = seo.get('desc') or clamp('%s: %s. Available as %s. Priced on the page, no account needed, dispatched from Sydney.'
                                    % (p['name'], p['spec'].rstrip('.'), _sentence_list(packs).lower()))

    about = [p['blurb']]
    made = []
    for key in ('Material', 'Construction', 'Active', 'Adhesive'):
        if key in extra:
            made.append('%s is %s' % (key.lower(), extra[key].lower()))
    if made:
        about.append('The %s.' % _sentence_list(made))
    ster = extra.get('Sterility') or extra.get('Sterilisation')
    if ster:
        about.append('Supplied %s.' % ster.lower().rstrip('.'))

    body = [('About %s' % lower_name(p['name']), about)]
    if len(opts) > 1:
        lines = ['There %s %d to choose from: %s.' % ('are' if len(opts) > 1 else 'is', len(opts), _sentence_list(opts))]
        lines += ['%s: %s.' % (label, hint.lower().rstrip('.')) for label, hint in p['variants']]
        body.append(('Choosing between the options', lines))
    body.append(('Pack sizes', [
        'Available as %s. The larger packs work out cheaper per unit, and the price for every one of them is on this page rather than behind a login.'
        % _sentence_list(packs).lower(),
    ]))

    faq = list(seo.get('faq') or [])
    if len(opts) > 1:
        faq.append(('What options do %s come in?' % lower_name(p['name']),
                    'There are %d: %s.' % (len(opts), _sentence_list(opts))))
    if ster:
        faq.append(('Are %s sterile?' % lower_name(p['name']),
                    'Supplied %s. It is on the spec table on this page and on the carton.' % ster.lower().rstrip('.')))
    faq.append(('What pack sizes are available?',
                '%s. Every price is on the page, with no account required to see it.' % _sentence_list(packs)))

    return dict(title=title, desc=desc, body=seo.get('body') or body, faq=faq)
