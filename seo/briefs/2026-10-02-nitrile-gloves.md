# Expand /shop/gloves-ppe

Generated 2026-10-02 by seo/opportunities.py. Every number here came from seo/keywords-au.json, seo/competitor-gaps.json or seo/gsc-snapshot.json. Nothing in it is a guess.

## The job

- **Action**: expand
- **Target term**: nitrile gloves
- **Page**: `/shop/gloves-ppe`
- **Why**: /shop/gloves-ppe is already about this, and Google has not shown it for anything yet
- **Cluster score**: 4911.3, from 5400 monthly searches across 5 terms

## The market terms this cluster covers

| term | volume | difficulty | our position |
| --- | --- | --- | --- |
| nitrile gloves | 4100 | 1 | not ranking |
| black nitrile gloves | 800 | 43 | not ranking |
| blue nitrile gloves | 200 | 0 | not ranking |
| buy nitrile gloves | 150 | 0 | not ranking |
| nitrile gloves black | 150 | 0 | not ranking |

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
python checks/compliance.py --only /shop/gloves-ppe          # the TGA language gate
node checks/seocheck.mjs && node checks/depth.mjs && node checks/linkcheck.mjs
```

A compliance finding blocks publication. It is not advisory.
