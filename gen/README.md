# Page generators

The site is static HTML in `docs/`, but most of it is generated. Fifty-one of
the fifty-eight pages come out of these scripts, so a change made by hand in
`docs/` is lost the next time one of them runs. Change it here and rebuild.

| script | writes | notes |
| --- | --- | --- |
| `style.py` | nothing | the locked human photography prompt, see `brand/PHOTOGRAPHY.md` |
| `seo.py` | nothing | head tags, structured data, and the written copy behind every shop page |
| `catalogue.py` | nothing | the eight categories, their products and their shots |
| `catalogue_extra.py` | nothing | the launch range from the sourcing shortlist, merged into `catalogue.py` |
| `content.py` | nothing | the six protocol pages: copy, kit tuples, imagery |
| `prodmap.py` | nothing | kit item name to product URL |
| `shop.py` | 43 shop pages | also exports the shared head, header and footer, which it reads out of `docs/about.html` |
| `build.py` | 6 `for/*` pages | imports `shop.py`, so importing it rebuilds the shop too |
| `tools.py` | calculator, gauge chart | imports `shop.py`, same |
| `footer.py` | all 81 | applies the sitewide footer |
| `sitemap.py` | `sitemap.xml`, `robots.txt` | run it after anything that adds or removes a page |

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
