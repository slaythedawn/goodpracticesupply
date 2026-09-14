# Good Practice Supply, design prototype

A nine page clickable prototype for Good Practice Supply, an Australian medical
consumables store selling to clinics and to people buying for use at home.

This repository holds the design handoff bundle and a deployable copy of the
prototype for review.

## Layout

| Path | Contents |
|---|---|
| `handoff/` | The original handoff bundle, unmodified. Design system, site architecture, and the nine `.dc.html` artboards. |
| `docs/` | The same nine pages prepared for hosting: clean filenames, rewritten internal links, page titles. |

## The prototype

| Page | File |
|---|---|
| Home | `docs/index.html` |
| Category listing | `docs/category.html` |
| Product detail | `docs/product.html` |
| Gauge Finder | `docs/gauge-finder.html` |
| Always Stocked | `docs/always-stocked.html` |
| Clinic Portal | `docs/clinic-portal.html` |
| Learn | `docs/learn.html` |
| Contact | `docs/contact.html` |
| About | `docs/about.html` |

## Tools, and why these two

Built off Ahrefs keyword data rather than instinct. The finding that drove it:
the traffic is in the tools, not the product names.

| Keyword | Global / month | AU / month | Difficulty |
|---|---|---|---|
| peptide calculator | 224,000 | 15,000 | 0 |
| bacteriostatic water | 67,000 | 5,700 | 14 |
| bacteriostatic water chemist warehouse | 3,000 | 3,000 | 0 |
| needle gauge sizes | 5,500 | | 0 |
| 1 ml is equal to how many units in insulin syringe | 7,300 | | 26 |
| insulin syringes australia | 40 | 40 | 0 |
| sharps container australia | 30 | 30 | 0 |

`docs/tools/reconstitution-calculator.html` answers the 224,000 cluster and the
unit conversion cluster with one tool, and outputs the two things we sell:
bacteriostatic water and U-100 syringes.

`docs/learn/needle-gauge-chart.html` covers the gauge reference cluster and the
long tail of individual gauge searches, linking each to the product.

Both are featured on the home page directly under the hero.

The calculator takes the dose as an input rather than suggesting one. It is unit
conversion, not dosing advice, and it says so on the page. Good Practice Supply
supplies the water and the syringes, never the compound.

## The shop

43 generated pages forming the commerce spine, so every link on the site lands
somewhere real:

| Path | Count | What it is |
|---|---|---|
| `docs/shop.html` | 1 | All categories, plus protocol entry points |
| `docs/shop/{category}.html` | 6 | Editorial intro, working filters, six product cards |
| `docs/shop/{category}/{product}.html` | 36 | Gallery, variants, pack sizes, quantity, cart, spec sheet, related |

The catalogue lives in one data file and the pages are generated from it, so the
6 categories and 36 products share a single template each rather than 42 hand
edited copies.

The prices, product codes and batch numbers are invented placeholders. They are
plausible and internally consistent, but nothing here is a real product record.

## Protocol landings

Six pages under `/for/`, built from the site architecture doc, which calls
protocol based shopping "the wedge, and it should be built first":

| Page | Target query |
|---|---|
| `docs/for/glp-1-injections.html` | what do I need to inject a GLP-1 at home |
| `docs/for/trt-injections.html` | trt injection supplies australia |
| `docs/for/peptide-reconstitution.html` | bacteriostatic water australia |
| `docs/for/diabetes-at-home.html` | insulin syringes australia |
| `docs/for/wound-care-at-home.html` | dressings for home use |
| `docs/for/clinic-fit-out.html` | setting up a medical practice supplies |

Each carries a kit sized by a frequency selector, showing how long each pack
lasts at that rate rather than implying a box of 100 is a month's use. Each also
states plainly what Good Practice Supply sells and what comes from a pharmacy,
because the compliance line in the handoff is absolute: consumables only, never
peptides, hormones or any prescription medicine.

Every page is interactive. Filters, the gauge questionnaire, the cadence
selector, the quantity stepper and cart count, the protocol kit selectors and
the contact routing all work.

## Running it locally

```
cd docs && python3 -m http.server 8000
```

Then open http://localhost:8000.

The pages depend on `support.js`, the prototype runtime that ships with the
handoff. It pulls React from unpkg at runtime, so the preview needs network
access.

## Changes made to the prototype for hosting

The handoff was authored desktop first, and each page carried its own copy of the
header. Two problems followed from that, both fixed in `docs/`:

**The header was different on every page.** Home was `position: fixed` with a
utility strip above it; every other page was `position: sticky` with no strip.
The right hand cluster changed too: Sign in plus a Shop button on home, a cart
button on category and product, a lone Shop button elsewhere, and Open an account
on the clinic portal. Moving between pages shifted every nav element sideways.
All nine pages now share a byte identical header block. Shop and Learn open their
dropdown panels on every page, not just home, and the cart count lives in the
header sitewide.

**The header did not scale on phones.** The nav wrapped into four rows and stood
190 to 196px tall. Below 900px the links now collapse into a menu button that
opens a panel inside the nav pill, reusing the same pattern as the Shop and Learn
dropdowns. The header is 124px on a 390px screen and identical on every page.

**Headlines were not anchored.** The page head grids used `align-items: center`,
so the headline's vertical position depended on the height of whatever sat in the
opposite column, which differs per page. Combined with three different top
paddings, the headline landed anywhere from 114px to 203px below the header. The
text column is now pinned to the top and the top padding is shared, so the
headline sits 114px below the header on every page that uses that layout, and the
two breadcrumb pages anchor to each other. Home and the Gauge Finder keep their
own positions, since both open with full bleed imagery rather than a page head.

Below 360px the full nav lockup and the actions no longer fit on one row, so the
pill wrapped and the header grew to 174px. At that width the lockup falls back to
the gp monogram, which the design system already treats as a standalone mark. The
header is now a flat 124px from 280px up to 900px, and 107px above that.

The header height is measured at runtime rather than hard coded, because the
utility strip wraps to two rows on phones.

## Important

These are design references, not production code. `support.js` and the
`.dc.html` format are a prototype runtime and should not be ported. The
photography is AI generated placeholder imagery on CloudFront and must be
replaced with licensed or commissioned work before launch.

`handoff/Good Practice Supply - Design System.md` is the authoritative spec.
