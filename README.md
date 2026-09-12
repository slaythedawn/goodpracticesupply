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

Every page is interactive. Filters, the gauge questionnaire, the cadence
selector, the quantity stepper and cart count, and the contact routing all work.

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

The header height is measured at runtime rather than hard coded, because the
utility strip wraps to two rows on phones.

## Important

These are design references, not production code. `support.js` and the
`.dc.html` format are a prototype runtime and should not be ported. The
photography is AI generated placeholder imagery on CloudFront and must be
replaced with licensed or commissioned work before launch.

`handoff/Good Practice Supply - Design System.md` is the authoritative spec.
