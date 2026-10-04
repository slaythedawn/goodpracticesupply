# New page for "bd ultra fine pen needles 4mm chemist warehouse"

Generated 2026-10-04 by seo/opportunities.py. Every number here came from seo/keywords-au.json, seo/competitor-gaps.json or seo/gsc-snapshot.json. Nothing in it is a guess.

## The job

- **Action**: new
- **Target term**: bd ultra fine pen needles 4mm chemist warehouse
- **Why**: nothing on the site covers this
- **Cluster score**: 3079.1, from 1200 monthly searches across 4 terms

## The market terms this cluster covers

| term | volume | difficulty | our position |
| --- | --- | --- | --- |
| bd ultra fine pen needles 4mm chemist warehouse | 150 | 0 | not ranking |
| bd ultra fine insulin syringe 1ml | 450 | 0 | not ranking |
| bd ultra fine pen needles | 400 | 0 | not ranking |
| bd ultra fine pen needles 5mm chemist warehouse | 200 | 50 | not ranking |

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
python checks/compliance.py --only /learn/          # the TGA language gate
node checks/seocheck.mjs && node checks/depth.mjs && node checks/linkcheck.mjs
```

A compliance finding blocks publication. It is not advisory.
