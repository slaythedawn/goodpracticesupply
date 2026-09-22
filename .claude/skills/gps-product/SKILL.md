---
name: gps-product
description: >
  Add, replace, reprice or restructure a product in the Good Practice Supply
  catalogue, including its category, variants, pack sizes, specs, photography key
  and search synonyms, then rebuild and re-export. Use this whenever asked to add
  a product or SKU to this site, swap a placeholder product for a real one, change
  prices or pack sizes, fix a product page, or prepare the catalogue for Shopify.
  Use it even when the request sounds like a small copy tweak to a product page,
  because product pages are generated and hand-editing them is thrown away on the
  next build.
---

# Changing the catalogue

Every product page on this site is generated from data. There is no HTML to edit:
fifty-seven products and 366 variants come out of `gen/catalogue.py` and
`gen/catalogue_extra.py`, and anything typed into `docs/shop/` is gone the next
time a generator runs.

The whole catalogue is currently placeholder. Prices are invented because no
factory has quoted, which is why `PURCHASABLE` in `gen/seo.py` is off and every
product will eventually be replaced. Treat a request to "add a product" as a
request to add a placeholder unless the user says the data is real, and say which
one you did.

## The shape of a product

`P()` in `gen/catalogue.py`:

    P(name, slug, tag, spec, blurb, family, variants, packs, extra=())

| argument | what it is |
| --- | --- |
| `name` | display name |
| `slug` | URL segment, lowercase, hyphenated, stable once published |
| `tag` | filter key, and it has to be one of the keys in the parent category's `filters` list or the product is unreachable by filter |
| `spec` | the one-line spec under the name |
| `blurb` | the card and page description, two sentences, plain |
| `family` | a key in `SHOTS`, which decides the gallery |
| `variants` | list of `(label, hint)`, e.g. `('29G × 13mm', 'Fills fastest')` |
| `packs` | list of `(label, cents)`. **Cents, not dollars** |
| `extra` | list of `(key, value)` spec rows |

Prices are integers in cents. `4776` is $47.76. Getting this wrong by a factor of
a hundred is the easiest mistake available here and it does not fail any check,
because both values are plausible integers.

A `hint` may be an empty string. `shop.py` only renders the hint line when at
least one variant on the product has a non-empty one, so a product with no hints
gets no blank row.

## Photography

Every image URL on the site is declared in the `I` dict in `gen/catalogue.py`,
and every one has passed the OCR gate described in `brand/PHOTOGRAPHY.md`. The
gate exists because generated product photography invents lettering, and invented
lettering on a medical product is a claim.

Adding a product with a new photograph means: generate it to the locked prompt in
`gen/style.py`, run it through the OCR gate, add the key to `I`, then add a
`SHOTS` family for it.

Prefer one honest photograph over four where three are something else in the same
box. The launch range deliberately uses single-shot families for exactly that
reason, and `shop.py` drops the thumbnail strip when a family has one image.

Reusing an existing family is acceptable for a placeholder, but say in the commit
that the photograph is not of the product.

## Regulatory data

`REGULATORY` in `gen/catalogue.py` is empty on purpose and product pages print
no ARTG or country-of-origin row as a result. Add an entry only when a real
supplier has given a real value for that specific product:

    REGULATORY = {'nitrile-examination-gloves':
                    [('ARTG', 'ARTG 123456'), ('Country of origin', 'Malaysia')]}

Never add a generic value to make the row appear. See `gps-compliance`.

## SKUs

`sku()` builds `GPS-<CAT>-<SLUG>-<VV><PP>` using the **whole** product slug, not
a truncation. `blood-glucose-meter` and `blood-glucose-test-strips` collide at
any sensible prefix length, which is how that was discovered. The cart carries
the SKU and the Shopify export emits it, so a code has to stay stable once it
exists.

## Everything you have to touch

1. **`gen/catalogue.py`** or **`gen/catalogue_extra.py`** for the launch range.
2. **The category's `count`** field, if you are changing how many products it
   has. It is displayed, so it is wrong the moment it disagrees.
3. **`I` and `SHOTS`** if there is a new photograph.
4. **`REGULATORY`** only if there is a real value.
5. **`gen/searchindex.py`**. Add a `SYNONYMS` entry whenever a product has a
   name customers do not use. People type "band aid", not "adhesive plasters",
   and "kt tape", not "kinesiology tape". A search that misses on the first try
   does not get a second one.
6. **`python3 gen/shopify_export.py`** if the catalogue needs re-exporting.
   Everything exports as draft and unpublished on purpose, because a draft
   product cannot be sold by accident while the prices are invented. Weights
   export as 0 grams and shipping is wrong until real weights exist.

Then rebuild and verify with `gps-preflight`. `seocheck.mjs` checks that every
shop page has a unique title and description, which is the check a copy-pasted
product trips.

## Replacing placeholders with real products

When the real catalogue arrives, the things that have to become real together
are prices, weights, ARTG and country of origin, and photography. A real price
with a placeholder photograph is worse than two placeholders, because it reads as
finished. Flipping `PURCHASABLE` and `INDEX_SHOP` is a separate decision and
`gen/README.md` describes what each one entails.
