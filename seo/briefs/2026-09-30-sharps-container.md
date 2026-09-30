# Expand /learn/sharps-disposal-australia

Generated 2026-09-30 by seo/opportunities.py. Every number here came from seo/keywords-au.json, seo/competitor-gaps.json or seo/gsc-snapshot.json. Nothing in it is a guess.

## The job

- **Action**: expand
- **Target term**: sharps container
- **Page**: `/learn/sharps-disposal-australia`
- **Why**: /learn/sharps-disposal-australia is already about this, and Google shows it for 13 other queries already
- **Cluster score**: 11141.4, from 7020 monthly searches across 12 terms
- **Held by**: allmedicalwaste.com.au, diabetesaustralia.com.au

## What Google already shows this page for, and it does not answer

These came out of Search Console, not out of a keyword tool. Every one is a real search where this page was offered and was not good enough. Answer them in the page, in plain words, and do not pad.

| the actual search | position | impressions |
| --- | --- | --- |
| sharps container disposal nsw | 46 | 2 |
| sharps | 56 | 5 |
| dispose of sharps bin | 62 | 1 |
| sharps disposal | 66 | 1 |
| sharps container disposal | 70 | 3 |
| sharps bin disposal | 71 | 1 |
| sharps waste disposal | 71 | 1 |
| sharps container disposal qld | 75 | 1 |
| where to dispose of sharps containers brisbane | 77 | 1 |
| disposal of sharps | 81 | 1 |
| sharps waste | 81 | 1 |
| sharp container disposal | 87 | 1 |
| safe sharps | 89 | 1 |

## The market terms this cluster covers

| term | volume | difficulty | our position |
| --- | --- | --- | --- |
| sharps container | 2300 | 0 | not ranking |
| disposal of sharps containers | 200 | 0 | not ranking |
| sharps disposal melbourne | 40 | 0 | not ranking |
| sharps disposal | 300 | 1 | 66 |
| sharps container disposal melbourne | 150 | 1 | not ranking |
| sharps disposal near me | 450 | 1 | not ranking |
| sharps container disposal near me | 50 | 1 | not ranking |
| sharps waste disposal | 40 | 0 | 71 |
| sharps disposal container | 150 | 0 | not ranking |
| sharps disposal bin | 100 | 0 | not ranking |
| sharps container disposal | 300 | 2 | 70 |
| safe sharps disposal | 50 | 2 | not ranking |

## The constraint on this subject

Describe how to find a drop-off point and who to ask. Never publish specific addresses, opening hours or council contact details. They go stale and a stale address sends somebody with used needles to a locked door.

## What the page must carry

- **A photograph**, eager loaded, served through the Vercel optimiser. Add the key to `PHOTO` in `gen/guides.py` for a new guide.
- **One featured product or tool**, not a grid. Already set: `product:sharps-container-bench`.
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
python checks/compliance.py --only /learn/sharps-disposal-australia          # the TGA language gate
node checks/seocheck.mjs && node checks/depth.mjs && node checks/linkcheck.mjs
```

A compliance finding blocks publication. It is not advisory.
