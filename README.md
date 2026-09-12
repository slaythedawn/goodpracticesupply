# Good Practice Supply, design prototype

A nine page clickable prototype for Good Practice Supply, an Australian medical
consumables store selling to clinics and to people buying for use at home.

This repository holds the design handoff bundle and a deployable copy of the
prototype for review.

## Layout

| Path | Contents |
|---|---|
| `handoff/` | The original handoff bundle, unmodified. Design system, site architecture, and the nine `.dc.html` artboards. |
| `site/` | The same nine pages prepared for hosting: clean filenames, rewritten internal links, page titles. |

## The prototype

| Page | File |
|---|---|
| Home | `site/index.html` |
| Category listing | `site/category.html` |
| Product detail | `site/product.html` |
| Gauge Finder | `site/gauge-finder.html` |
| Always Stocked | `site/always-stocked.html` |
| Clinic Portal | `site/clinic-portal.html` |
| Learn | `site/learn.html` |
| Contact | `site/contact.html` |
| About | `site/about.html` |

Every page is interactive. Filters, the gauge questionnaire, the cadence
selector, the quantity stepper and cart count, and the contact routing all work.

## Running it locally

```
cd site && python3 -m http.server 8000
```

Then open http://localhost:8000.

The pages depend on `support.js`, the prototype runtime that ships with the
handoff. It pulls React from unpkg at runtime, so the preview needs network
access.

## Important

These are design references, not production code. `support.js` and the
`.dc.html` format are a prototype runtime and should not be ported. The
photography is AI generated placeholder imagery on CloudFront and must be
replaced with licensed or commissioned work before launch.

`handoff/Good Practice Supply - Design System.md` is the authoritative spec.
