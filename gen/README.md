# Page generators

The site is static HTML in `docs/`, but most of it is generated. Fifty-one of
the fifty-eight pages come out of these scripts, so a change made by hand in
`docs/` is lost the next time one of them runs. Change it here and rebuild.

| script | writes | notes |
| --- | --- | --- |
| `style.py` | nothing | the locked human photography prompt, see `brand/PHOTOGRAPHY.md` |
| `catalogue.py` | nothing | the six categories, thirty-six products and their shots |
| `content.py` | nothing | the six protocol pages: copy, kit tuples, imagery |
| `prodmap.py` | nothing | kit item name to product URL |
| `shop.py` | 43 shop pages | also exports the shared head, header and footer, which it reads out of `docs/about.html` |
| `build.py` | 6 `for/*` pages | imports `shop.py`, so importing it rebuilds the shop too |
| `tools.py` | calculator, gauge chart | imports `shop.py`, same |
| `footer.py` | all 58 | applies the sitewide footer |

`shop.py` runs its `main()` on import, so `python3 gen/build.py` rebuilds 49
pages, not 6. That is intended. Run from anywhere: the output path is resolved
from the script's own location.

The seven hand-written pages are `index`, `about`, `always-stocked`,
`clinic-portal`, `contact`, `gauge-finder` and `learn`. `shop.py` reads the
shared header and footer out of `about.html`, so a header change made there
propagates to every generated page on the next build. Make it in all 58 at once
or make it in `about.html` and rebuild.
