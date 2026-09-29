# Expand /shop/syringes-needles

Generated 2026-09-29 by seo/opportunities.py. Every number here came from seo/keywords-au.json, seo/competitor-gaps.json or seo/gsc-snapshot.json. Nothing in it is a guess.

## The job

- **Action**: expand
- **Target term**: insulin needles
- **Page**: `/shop/syringes-needles`
- **Why**: /shop/syringes-needles is already about this, and Google has not shown it for anything yet
- **Cluster score**: 12990.3, from 10320 monthly searches across 6 terms
- **Held by**: medshop.com.au

## The market terms this cluster covers

| term | volume | difficulty | our position |
| --- | --- | --- | --- |
| insulin needles | 8600 | 3 | not ranking |
| syringe needle | 800 | 0 | not ranking |
| insulin needles australia | 200 | 0 | not ranking |
| needle syringe | 350 | 0 | not ranking |
| insulin pen needles | 300 | 7 | not ranking |
| pen needles | 70 | 0 | not ranking |

## The constraint on this subject

The syringe and the needle, not the medicine. U-100 graduation is a fact about the barrel. Never a dose and never a site for a named product.

## What the page must carry

- **A photograph**, eager loaded, served through the Vercel optimiser. Add the key to `PHOTO` in `gen/guides.py` for a new guide.
- **One featured product or tool**, not a grid. Add an entry to `FEATURED` in `gen/feature.py` or the build fails.
- **An email sign-up**, from `gen/capture.py`, with the interest tag set so the contact can be segmented later.
- **Inbound links from at least two pages that already rank.** Run `python seo/internal_links.py` after writing and apply what it suggests.
- **Australian spelling, no em dashes, no emoji.**

## The house rules that apply to every page

- Consumables only. Never imply this business supplies a peptide, a hormone or any prescription medicine.
- Technique described through the equipment: gauge, length, angle. Never a dose, never a site for a named drug, never a frequency.
- The directions that came with the medicine and the prescriber come first, and are said to come first.
- No therapeutic outcome claims.

## Before it goes live

```
python gen/build.py && python gen/guides.py    # or the full build order
python checks/compliance.py --only /shop/syringes-needles          # the TGA language gate
node checks/seocheck.mjs && node checks/depth.mjs && node checks/linkcheck.mjs
```

A compliance finding blocks publication. It is not advisory.
