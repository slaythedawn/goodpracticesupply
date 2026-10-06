# New page for "sharps container disposal brisbane"

Generated 2026-10-06 by seo/opportunities.py. Every number here came from seo/keywords-au.json, seo/competitor-gaps.json or seo/gsc-snapshot.json. Nothing in it is a guess.

## The job

- **Action**: new
- **Target term**: sharps container disposal brisbane
- **Why**: nothing on the site covers this
- **Cluster score**: 2414.7, from 1190 monthly searches across 10 terms

## The market terms this cluster covers

| term | volume | difficulty | our position |
| --- | --- | --- | --- |
| sharps container disposal brisbane | 150 | 5 | not ranking |
| sharps disposal perth | 100 | 2 | not ranking |
| sharps bin chemist warehouse | 100 | 0 | not ranking |
| sharps kit | 250 | 1 | not ranking |
| sharps container chemist warehouse | 150 | 0 | not ranking |
| sharps disposal brisbane | 60 | 5 | not ranking |
| sharps disposal sydney | 100 | 1 | not ranking |
| sharps disposal chemist warehouse | 150 | 55 | not ranking |
| sharps disposal canberra | 70 | 1 | not ranking |
| sharps disposal adelaide | 60 | 50 | not ranking |

## The constraint on this subject

Describe how to find a drop-off point and who to ask. Never publish specific addresses, opening hours or council contact details. They go stale and a stale address sends somebody with used needles to a locked door.

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
python checks/compliance.py --only /learn/          # the TGA language gate
node checks/seocheck.mjs && node checks/depth.mjs && node checks/linkcheck.mjs
```

A compliance finding blocks publication. It is not advisory.
