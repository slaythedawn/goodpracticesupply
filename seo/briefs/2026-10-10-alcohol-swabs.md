# Expand /shop/diluents-swabs

Generated 2026-10-10 by seo/opportunities.py. Every number here came from seo/keywords-au.json, seo/competitor-gaps.json or seo/gsc-snapshot.json. Nothing in it is a guess.

## The job

- **Action**: expand
- **Target term**: alcohol swabs
- **Page**: `/shop/diluents-swabs`
- **Why**: /shop/diluents-swabs is already about this, and Google has not shown it for anything yet
- **Cluster score**: 1770.0, from 1950 monthly searches across 3 terms

## The market terms this cluster covers

| term | volume | difficulty | our position |
| --- | --- | --- | --- |
| alcohol swabs | 1300 | 0 | not ranking |
| alcohol swab | 350 | 0 | not ranking |
| bacteriostatic water for injection | 300 | 50 | not ranking |

## The constraint on this subject

Sterile diluent, sold as a consumable. Never describe what it is mixed with, never name a peptide, hormone or medicine, and never imply we supply one.

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
python checks/compliance.py --only /shop/diluents-swabs          # the TGA language gate
node checks/seocheck.mjs && node checks/depth.mjs && node checks/linkcheck.mjs
```

A compliance finding blocks publication. It is not advisory.
