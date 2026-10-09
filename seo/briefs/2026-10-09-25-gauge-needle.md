# Expand /learn/needle-gauge-chart

Generated 2026-10-09 by seo/opportunities.py. Every number here came from seo/keywords-au.json, seo/competitor-gaps.json or seo/gsc-snapshot.json. Nothing in it is a guess.

## The job

- **Action**: expand
- **Target term**: 25 gauge needle
- **Page**: `/learn/needle-gauge-chart`
- **Why**: /learn/needle-gauge-chart is already about this, and Google has not shown it for anything yet
- **Cluster score**: 1912.5, from 2900 monthly searches across 12 terms

## The market terms this cluster covers

| term | volume | difficulty | our position |
| --- | --- | --- | --- |
| 25 gauge needle | 350 | 0 | not ranking |
| 23 gauge needle | 300 | 0 | not ranking |
| 18 gauge needle | 250 | 0 | not ranking |
| 27 gauge needle | 250 | 0 | not ranking |
| needle gauge | 250 | 10 | not ranking |
| 29 gauge needle | 150 | 0 | not ranking |
| 22 gauge needle | 200 | 0 | not ranking |
| 16 gauge needle | 200 | 0 | not ranking |
| 21 gauge needle | 200 | 0 | not ranking |
| 19 gauge needle | 150 | 0 | not ranking |
| 31 gauge needle | 150 | 0 | not ranking |
| 14 gauge needle | 150 | 0 | not ranking |

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
python checks/compliance.py --only /learn/needle-gauge-chart          # the TGA language gate
node checks/seocheck.mjs && node checks/depth.mjs && node checks/linkcheck.mjs
```

A compliance finding blocks publication. It is not advisory.
