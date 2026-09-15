# Page generators

The site is static HTML in `docs/`, but most of it is generated. Fifty-one of
the fifty-eight pages come out of these scripts, so a change made by hand in
`docs/` is lost the next time one of them runs. Change it here and rebuild.

| script | writes | notes |
| --- | --- | --- |
| `style.py` | nothing | the locked human photography prompt, see `brand/PHOTOGRAPHY.md` |
| `seo.py` | nothing | head tags, structured data, and the written copy behind every shop page |
| `catalogue.py` | nothing | the eight categories, their products and their shots |
| | | every image URL on the site is declared in `I` here, and every one has passed the OCR gate in `brand/PHOTOGRAPHY.md` |
| `catalogue_extra.py` | nothing | the launch range from the sourcing shortlist, merged into `catalogue.py` |
| `content.py` | nothing | the six protocol pages: copy, kit tuples, imagery |
| `prodmap.py` | nothing | kit item name to product URL |
| `shop.py` | 43 shop pages | also exports the shared head, header and footer, which it reads out of `docs/about.html` |
| `build.py` | 6 `for/*` pages | imports `shop.py`, so importing it rebuilds the shop too |
| `tools.py` | calculator, gauge chart | imports `shop.py`, same |
| `footer.py` | all 81 | applies the sitewide footer |
| `searchindex.py` | `search-index.json` | what the header search matches against, including the synonym list |
| `sitemap.py` | `sitemap.xml`, `robots.txt` | run it after anything that adds or removes a page |
| `shopify_export.py` | `export/shopify-products.csv`, `export/variant-map.json` | the catalogue in Shopify import format |
| `photoreview.py` | `docs/internal/photo-review.html` | working page, delete once the photography is settled |

`shop.py` runs its `main()` on import, so `python3 gen/build.py` rebuilds 72
pages, not 6. That is intended. Run from anywhere: the output path is resolved
from the script's own location.

## Going live in search

Every shop page already carries a canonical, a unique title and description,
Open Graph and Twitter tags, and Product, BreadcrumbList, FAQPage and
CollectionPage structured data. None of it is indexable yet, on purpose:
prices are placeholders until a factory quotes, and the copy has not been
through legal review.

Turning it on is two changes made together:

1. `INDEXABLE = True` in `gen/seo.py`, then rebuild. Every page swaps its
   noindex for `index, follow, max-image-preview:large`, and `robots.txt` is
   rewritten to match.
2. Remove the `X-Robots-Tag: noindex, nofollow` header from `vercel.json`. The
   header overrides the meta tag, so leaving it in place makes step 1 do
   nothing.

Do not add a `Disallow` to `robots.txt` as a way of staying unlisted. A crawler
that cannot fetch a page cannot read the noindex on it, which is how URLs end up
in an index with no way to remove them.

The seven hand-written pages are `index`, `about`, `always-stocked`,
`clinic-portal`, `contact`, `gauge-finder` and `learn`. `shop.py` reads the
shared header and footer out of `about.html`, so a header change made there
propagates to every generated page on the next build. Make it in all 58 at once
or make it in `about.html` and rebuild.

## Search

The header magnifier opens an overlay served by `docs/search.js`, which is plain
DOM rather than a page component: every page here is a hydrated component, and
an overlay inside the component tree would have to be added to all eighty-one of
them. It delegates from `document`, so it attaches to the control whenever the
page renders it.

It matches against `docs/search-index.json` (`gen/searchindex.py`), fetched once
on first open. Eighty entries, seventeen kilobytes, no search backend.

The part worth maintaining is `SYNONYMS` in `gen/searchindex.py`. People type
"band aid", not "adhesive plasters", and "kt tape", not "kinesiology tape". A
search that misses on the first try does not get a second one. Add to it
whenever a product has a name customers do not use.

Run `searchindex.py` after anything that adds, renames or removes a page.

## Shopify

Headless: this repo stays the storefront and the source of truth for the
catalogue. Shopify holds a copy so it can price, take money, and manage orders.
Products are never authored in the Shopify admin, because then the catalogue
stops being reviewable and a diff stops being the record.

    python3 gen/shopify_export.py

writes `export/shopify-products.csv` (57 products, 366 variants) and
`export/variant-map.json`. Everything imports as **draft and unpublished** on
purpose: every price in `catalogue.py` is invented until a factory quotes, and a
draft product cannot be sold by accident.

After importing, pull the variant IDs back out of Shopify and fill them into
`variant-map.json`. The storefront needs those IDs to build a cart, because SKUs
are not addressable through the Storefront API.

Still to fill before anything is published:

- **Variant Grams.** Exported as 0. Shipping rates are wrong until real weights
  are in, and 0 grams reads as free freight.
- **Prices.** Placeholders, in cents, in `catalogue.py`.
- **ARTG and country of origin.** See `REGULATORY` in `catalogue.py`.

## Regulatory claims

`REGULATORY` in `catalogue.py` is empty and product pages print nothing for ARTG
or country of origin as a result. That is deliberate. Those are claims about
specific goods and they need a real value from a real supplier per product. The
site used to print `ARTG: Listed, see carton` and `Country of origin: Malaysia`
on all fifty-seven products, cotton wool and facial tissues included, which was
neither true nor defensible.
