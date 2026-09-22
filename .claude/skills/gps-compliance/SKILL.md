---
name: gps-compliance
description: >
  Check or write customer-facing copy for Good Practice Supply against the rules
  that keep a consumables business out of trouble: consumables only and never a
  medicine, no dose or site or frequency, regulatory claims only from a real
  per-product value, no therapeutic outcome claims, and nothing said about the
  business that is not true yet. Use this before publishing or editing any page
  copy, product description, guide, form message, email or meta description in
  this repo, and use it as a review pass when asked to check whether wording is
  safe, accurate, defensible or on brand. Reach for it even when the task looks
  like pure layout, because copy tends to arrive alongside layout.
---

# Copy and compliance

This site sells medical consumables in Australia to people who are often mid-way
through a prescribed treatment. Two failure modes matter, and they are different:

1. **Saying something about medicine.** The business supplies syringes, needles,
   swabs and dressings. It does not supply peptides, hormones, or any
   prescription medicine, and copy that implies otherwise invites a regulator who
   will not be charmed by the distinction being unintentional.
2. **Saying something untrue about the business.** Ordering is not open. There is
   no warehouse shift, no staffed phone line, and no order to chase. Copy written
   in the voice of a going concern is a lie that a real customer will catch first.

Both have happened here and been fixed. The list below is mostly a list of things
that were once on the live site.

## The rules

**Consumables only.** Never imply the business supplies a medicine, a peptide or
a hormone, in any form, including by implication from page structure. A category
called "Peptide reconstitution" sells the syringes and the bacteriostatic water,
which is fine, and the copy has to keep making that obvious.

**Technique is described as equipment, never as treatment.** Gauge, length and
angle are equipment properties and are fair game. A dose, a site for a named
drug, or a frequency is clinical direction and is not. "A 4mm needle rarely
reaches muscle whatever your build" is equipment. "Inject 0.25mg into the abdomen
weekly" is not, and is not made acceptable by hedging around it.

**The prescriber comes first, and is said to come first.** Guides carry a note to
that effect. It is not boilerplate to be trimmed for length: it is the sentence
that makes the rest of the page a description of equipment rather than advice.

**Regulatory claims come from a real value or they do not appear.** `REGULATORY`
in `gen/catalogue.py` is deliberately empty, and `shop.py` renders an ARTG or
country-of-origin row only where a value exists. The site once printed
`ARTG: Listed, see carton` and `Country of origin: Malaysia` on all fifty-seven
products, cotton wool and facial tissues included, which was neither true nor
defensible. Never restore a blanket claim, and never add a site-wide one. A claim
about specific goods needs a value from a real supplier for those goods.

**No therapeutic outcome claims, and no before-and-after imagery.** Not for a
product, not for a protocol page, not as a testimonial.

**Never claim capability the business does not have.** No phone number that does
not ring, no staffed hours, no dispatch or warehouse that does not exist, no
email address on a domain that is not theirs, and no form that says a message was
sent when it was not. All five of those were live at some point. The forms now
return a 503 and display a message that is true when no key is configured.

**Prices can be shown, orders cannot be taken.** `PURCHASABLE` in `gen/seo.py` is
off. While it is off, buy buttons read "Coming soon" and are genuinely disabled,
and Product structured data carries no `offers` block. A price in structured data
is a machine-readable offer to sell at that price. Do not reintroduce one while
every price in the catalogue is invented.

**Gauge Finder privacy promises are commitments.** The page tells people their
answers stay in the browser, are never stored, and never feed advertising. If a
change would make any of those false, the promise comes off the page in the same
commit, or the change does not land.

## House style

- Australian spelling and Australian conventions throughout.
- **No em dashes.** Use a comma, a colon, or a full stop. This is a house rule
  the owner has stated repeatedly and it applies to every customer-facing string.
- No emoji.
- "Always Stocked" and "Gauge Finder" are product names and are always
  capitalised.
- The three footer statements live in `gen/footer.py` and appear on all pages:
  consumables only, nothing here is medical advice, follow your prescriber. They
  are the site's standing disclosure. Do not shorten or relocate them.
- Write plainly. The existing copy explains a thing and then says why it matters,
  in short sentences, without salesmanship. Match that.

## How to run a review pass

Read the copy as three different people in turn. This catches more than a keyword
scan, because the failures here have been failures of implication rather than of
vocabulary.

- **A regulator.** Does any sentence read as a claim about a medicine, a
  therapeutic outcome, or an approval status? Is any claim about specific goods
  backed by a real value?
- **A customer mid-treatment.** Does anything here read as instruction they might
  follow instead of their prescriber's? Does anything promise a service that will
  not answer?
- **A journalist looking for a story.** Is anything here overstated in a way that
  would be embarrassing to defend in public?

Then check the mechanical things: em dashes, spelling, the two capitalised product
names, and whether anything asserts the business can do something it cannot yet.

Report what you found and where, by file and line. If you found nothing, say that
plainly rather than manufacturing a finding, and say which of the rules you
actually checked against.

A lawyer will review the terms and privacy copy before it goes live. Do not write
review-pending language into the pages themselves.
