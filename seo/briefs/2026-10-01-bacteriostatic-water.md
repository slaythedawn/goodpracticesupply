# Expand /learn/reconstitution-basics

Generated 2026-10-01 by seo/opportunities.py. Every number here came from seo/keywords-au.json, seo/competitor-gaps.json or seo/gsc-snapshot.json. Nothing in it is a guess.

## The job

- **Action**: expand
- **Target term**: bacteriostatic water
- **Page**: `/learn/reconstitution-basics`
- **Why**: /learn/reconstitution-basics is already about this, and Google has not shown it for anything yet
- **Cluster score**: 8686.5, from 6600 monthly searches across 5 terms
- **Held by**: livingstone.com.au

## The market terms this cluster covers

| term | volume | difficulty | our position |
| --- | --- | --- | --- |
| bacteriostatic water | 5700 | 0 | not ranking |
| bacteriostatic water australia | 250 | 54 | not ranking |
| buy bacteriostatic water | 200 | 0 | not ranking |
| what is bacteriostatic water | 300 | 9 | not ranking |
| bacteriostatic water 10ml | 150 | 0 | not ranking |

## The constraint on this subject

Sterile diluent, sold as a consumable. Never describe what it is mixed with, never name a peptide, hormone or medicine, and never imply we supply one.

## What the page must carry

- **A photograph**, eager loaded, served through the Vercel optimiser. Add the key to `PHOTO` in `gen/guides.py` for a new guide.
- **One featured product or tool**, not a grid. Already set: `tool:reconstitution-calculator`.
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
python checks/compliance.py --only /learn/reconstitution-basics          # the TGA language gate
node checks/seocheck.mjs && node checks/depth.mjs && node checks/linkcheck.mjs
```

A compliance finding blocks publication. It is not advisory.
