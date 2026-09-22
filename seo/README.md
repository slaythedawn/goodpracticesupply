# Keyword research and triage

Two tools doing what the other cannot.

**Ahrefs** knows what Australians search for and how hard each term is to rank.
It does not know that this business sells consumables and must never imply it
supplies a medicine, which is the constraint that decides whether a term is
usable at all.

**TypeSafe** makes that judgement, per keyword, as a yes/no with a probability.
It knows nothing about search volume.

So: Ahrefs produces `keywords-au.json`, TypeSafe judges each row, and the
arithmetic that ranks them stays in ordinary code where it can be read and
argued with. Nothing is scored by a model that a spreadsheet could score.

    python seo/triage.py --dry-run          # offline, free
    python seo/triage.py                    # needs TYPESAFE_API_KEY

Pulled 2026-09-22 for country `au`, seeded from insulin syringe, pen needles,
sharps container, bacteriostatic water, alcohol swabs, nitrile gloves, needle
gauge and reconstitution. Refresh it from Ahrefs rather than editing by hand.
