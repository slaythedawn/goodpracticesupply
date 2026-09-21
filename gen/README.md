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
| `sitemap.py` | `sitemap.xml`, `robots.txt`, `gen/lastmod.json` | run it last, after every page is written |
| `llms.py` | `llms.txt` | plain-text site map for language models |
| `shopify_export.py` | `export/shopify-products.csv`, `export/variant-map.json` | the catalogue in Shopify import format |
| `pagemeta.py` | nothing | title, description and structured data for every page that is not a shop page |
| `headmeta.py` | rewrites the 7 hand-written pages | injects the head block, fenced so it is safe to re-run |
| `photoreview.py` | `docs/internal/photo-review.html` | on demand only, not part of a build |

`shop.py` runs its `main()` on import, so `python3 gen/build.py` rebuilds 72
pages, not 6. That is intended. Run from anywhere: the output path is resolved
from the script's own location.

## Going live in search

Two switches in `gen/seo.py`, deliberately independent:

- `PURCHASABLE` is whether anyone can complete an order. Off. While it is off the
  buy button reads "Coming soon" and is disabled, the stock pill says the same,
  the cart chip is gone from the header, and the Product structured data carries
  no `offers` block. A price in structured data is a machine-readable offer to
  sell at that price, and an offer you cannot honour is not a thing to publish.
- `INDEX_CONTENT` and `INDEX_SHOP` control indexing per section. Content is on,
  the shop is off. The guides, the tools, the six `/for/` pages and the fixed
  pages are finished writing and are what earns authority. The shop is
  fifty-seven products that will be replaced, at prices no factory has quoted.

Turning the shop on later is two changes made together:

1. `INDEX_SHOP = True` in `gen/seo.py`, then rebuild.
2. Remove the `/shop` rules from `vercel.json`. The header overrides the meta
   tag, so leaving them makes step 1 do nothing.

`sitemap.py` lists only indexable URLs, because pointing a crawler at a page
that then tells it to forget what it found wastes crawl budget a new domain does
not have. `robots.txt` still allows everything on purpose: a crawler has to be
able to fetch `/shop` to read the noindex on it.

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

## Structured data

Every indexable page carries a description, a canonical, Open Graph, Twitter and
at least one JSON-LD block. Which block depends on the page:

| page | entities |
| --- | --- |
| `/` | `Organization`, `WebSite` with a `SearchAction` |
| `/for/*` | `Article`, `BreadcrumbList`, `FAQPage` |
| `/learn/needle-gauge-chart` | `Article`, `BreadcrumbList` |
| `/gauge-finder`, `/tools/*` | `WebApplication`, `BreadcrumbList` |
| `/about`, `/contact`, `/learn` | `AboutPage`, `ContactPage`, `CollectionPage` |
| `/shop/*` | `Product`, `BreadcrumbList`, `FAQPage`, `CollectionPage`, `ItemList` |

Two things deliberately absent. The `Organization` carries no `contactPoint` and
no `sameAs`, because there is no mailbox answering yet and no social profile to
point at. The `WebApplication` blocks carry no `aggregateRating`, because there
are no ratings, and inventing them is the most reliable way to earn a manual
action.

The `SearchAction` target is `/?q={search_term_string}`, and `search.js` reads
that parameter on load and opens the overlay with it. Declaring a search
endpoint that does not exist is how this markup usually goes wrong.

### The shell trap

`shop.py` and `build.py` slice their page shell out of `docs/about.html`, which
is itself a page with its own canonical and its own structured data. Both strip
the `gen:headmeta` fence first. Without that, every generated page on the site
inherits About's canonical, which is the sort of thing that is invisible in a
browser and fatal in a search console.

## Build order

    python3 gen/build.py        # shop + /for/, imports shop.py
    python3 gen/tools.py        # calculator, gauge chart
    python3 gen/headmeta.py     # head block on the 7 hand-written pages
    python3 gen/footer.py       # sitewide footer
    python3 gen/searchindex.py  # search-index.json
    python3 gen/llms.py         # llms.txt
    python3 gen/sitemap.py      # sitemap.xml, robots.txt, lastmod.json

`headmeta.py` after `build.py`, because `build.py` reads `about.html` for its
shell and `headmeta.py` writes to it.

## The two forms

The site is static except for two Vercel serverless functions in `api/`, which
exist because ordering is not open yet but enquiries and clinic accounts are.

| endpoint | form | required |
| --- | --- | --- |
| `POST /api/contact` | `/contact` | name, valid email, a message. ABN optional, checksummed if given |
| `POST /api/apply` | `/clinic-portal` | practice, contact, valid work email, valid ABN |

Both validate server side, carry an off-screen honeypot field, and post through
Resend. ABNs are checked against the ATO checksum rather than a length test, so
a transposed pair is caught.

One address does everything: **hello@gpsupply.com.au**. Mail goes out from it,
replies come back to it, and it is the only address printed on the site. Forward
it to whatever inbox is already being read. There is no second mailbox.

One required environment variable on the Vercel project:

    RESEND_API_KEY   server side only, never in the repo

Two optional ones, both defaulting to the address above:

    ENQUIRIES_TO     where mail lands. Point it somewhere else to receive
                     before the forwarder exists
    ENQUIRIES_FROM   who it comes from. Needs gpsupply.com.au verified in Resend

With no key set, both endpoints return 503 and a message the form displays as
written. They never claim a message was received when it was not.

`checks/config.mjs` validates `vercel.json` against the fields Vercel accepts.
It exists because an unknown key in a headers rule took production down for two
deploys, and because Vercel rejects the config before building, so the failure
arrives with no build log to read.

## lastmod

`gen/lastmod.json` records a content hash and a date per indexable page, and is
committed. `sitemap.py` hashes each built page, and only moves its date when the
hash moves.

Stamping every URL with the build date is the usual way this goes wrong. Google
uses `lastmod` when it can trust it, and a sitemap that claims fifteen pages all
changed today, every day, teaches it not to. The build is idempotent, so an
untouched page hashes the same and keeps the date it had.

It runs last, after every generator has written its pages, and it fails loudly
if a listed URL has no file behind it. Pages that stop being listed are dropped
from the file rather than accumulating.

## Being quoted rather than ranked

Three things, in descending order of how much they matter.

**The answer sits at the top.** Each `/for/` guide opens with a one-sentence
answer to the question its headline asks, from `answer` in `content.py`. It used
to be halfway down the page, under the marketing lead. An assistant looking for
something to quote takes the sentence that answers the question, and so does a
reader skimming. It is now about eight per cent into the page text.

**The structured data.** `Organization`, `Article`, `FAQPage`, `WebApplication`
and `BreadcrumbList`, per page. That is the machine-readable version of the same
claim and it is what grounding actually consumes.

**`robots.txt` names the assistant crawlers.** Same effect as the wildcard
already had, but the decision is on the record so nobody later tidies it into a
block. `Google-Extended` is listed separately on purpose: it governs AI
Overviews and Gemini grounding, and it is independent of Googlebot and Search.

`llms.txt` is a proposed convention, not a standard, and no major provider has
committed to reading it. It is here because it costs four kilobytes. Do not
expect it to do anything on its own.

None of this creates authority. A new domain with no inbound links will not be
cited any more than it will rank. This makes the site citable for when that
changes.
