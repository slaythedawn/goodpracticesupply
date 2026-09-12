# Handoff: Good Practice Supply

## Overview

Good Practice Supply is an Australian medical consumables store with a hybrid model: it sells the same stock to **clinics** (trade pricing, invoicing, standing orders) and to **people buying for use at home** (no account, no minimum, prices visible without logging in). Every incumbent in this market (TeamMed, Medisa, Tomlin, Icon) hides pricing behind an approved trade account and does not serve consumers at all — open pricing and consumer access are the strategic wedge, so **prices must be visible to anonymous visitors and to crawlers**.

This bundle contains a nine-page prototype covering the consumer path (home → category → product → gauge finder → learn), the trade path (clinic portal), and the supporting pages (always stocked, contact, about).

## About the design files

The files in this bundle are **design references created in HTML**. They are prototypes showing intended look and behaviour, **not production code to copy directly**.

They are authored in a proprietary streaming component format (`.dc.html`) that pairs an inline-styled template with a small logic class, and they depend on `support.js` (included, for local viewing only). Do not port that runtime.

**The task is to recreate these designs in the target codebase's existing environment** — React, Next.js, Vue, Astro, Shopify Liquid, whatever is in play — using its established patterns, component library and styling approach. If no codebase exists yet, this is a commerce site with a content layer and strong SEO requirements, so **Next.js (App Router) or Shopify Hydrogen** are the natural choices.

### Reading a `.dc.html` file

- Markup lives between `<x-dc>` tags. Everything is inline-styled; there are no classes.
- `{{ name }}` are template holes filled by the `renderVals()` return in the `<script data-dc-script>` block at the bottom.
- `<sc-for list="{{ items }}" as="item">` is a loop; `<sc-if value="{{ flag }}">` is a conditional.
- `style-hover="..."` is a hover state. Translate to `:hover` in CSS.
- Ignore `data-reveal`, `data-card`, `data-cta`, `data-link` except as markers for the motion behaviour described below.

## Fidelity

**High fidelity.** Colours, typography, spacing, radii, motion timings and copy are final and intentional. Recreate the UI faithfully using the target codebase's libraries. `Good Practice Supply - Design System.md` is the authoritative spec and should be treated as the source of truth over anything inferred from the markup.

---

## Design tokens

### Colour

| Token | Hex | Role |
|---|---|---|
| `--c-forest` | `#1C4034` | Brand. Dark bands, glass tint, eyebrow text on light |
| `--c-forest-deep` | `#143026` | Footer, nav glass base, image plates on forest |
| `--c-forest-line` | `#2A5245` | Hairlines inside forest sections |
| `--c-mint` | `#8FBFA6` | Action accent. Primary buttons on dark, eyebrow pills, numerals on forest |
| `--c-sage-text` | `#B7CFC3` | Body copy on forest (7.4:1) |
| `--c-mist` | `#DCE5E1` | Lead paragraphs on forest |
| `--c-ink` | `#0E0E0E` | Body text on light, buttons on light, text inside mint pills |
| `--c-ink-raised` | `#3A3A38` | Body copy under a heading on light |
| `--c-graphite` | `#59595A` | Captions, counts, metadata (6.1:1) |
| `--c-hairline` | `#E3E3E1` | Borders and separators on light |
| `--c-surface` | `#F2F2F1` | Cards and alternating light bands |
| `--c-plate` | `#EDEDEB` | Behind product photography (matches the studio sweep) |
| `--c-canvas` | `#FAFAFA` | Page ground and inverse text |

**Rules that matter:** forest is the *chrome* (nav, dark bands, footer), mint is the *action* colour and always carries `#143026` text, ink is for reading and light-surface buttons. No colour outside this ramp — error and warning states use ink or mint with a mono label, never red or amber. Never pure white or pure black.

### Typography

- **Archivo** (Google Fonts), weights 400 / 500 / 600. Nothing lighter than 400.
- **Archivo Black** for the wordmark and monogram only.
- **IBM Plex Mono**, weight 500, for eyebrow pills, counts, step numerals, spec values, prices in spec rows.

| Role | Size | Weight | Line height | Tracking |
|---|---|---|---|---|
| display | `clamp(32px, 3.8vw, 52px)` | 600 | 1.02 | −.035em |
| heading | `clamp(26px, 3vw, 40px)` | 600 | 1.05 | −.03em |
| subheading | `clamp(22px, 2.4vw, 30px)` | 600 | 1.1 | −.025em |
| card title | 17–19px | 600 | 1.25 | −.02em |
| lead | 17.5px | 400 | 1.55 | −.005em |
| body | 16px | 400 | 1.55 | −.005em |
| nav | 15px | 500 | 1 | −.005em |
| mono label | 11–12px | 500 | 1 | +.16em, uppercase |

### Space, shape, layout

- Base unit 8px. Page max-width **1440px**, gutters `clamp(20px, 5vw, 72px)`.
- Section padding `clamp(48px, 7vw, 96px)`.
- Radii: glass panels and image frames **28px**; cards **22px**; nav bar **22px**; inputs **12px**; buttons, pills and chips **1000px**. Only these.
- **No shadows and no gradients anywhere.** Depth comes from glass over photography, forest against canvas, and hairlines. Image scrims are flat `rgba(14,14,14,.2–.28)`.

### The grid rule — read this before writing any grid

Every track is `repeat(auto-fit, minmax(min(Npx, 100%), 1fr))`. The `min()` wrapper prevents overflow on small screens. **N must be chosen so the intended count fits the real container width, not the viewport.** Container is typically 832px at a 924px viewport.

| Group | Items | Floor | Result |
|---|---|---|---|
| Hero fact bar | 4 | 210px | 2 × 2 |
| Popular categories | 6 | 320px | 3 + 3 |
| Four-up card rows | 4 | 190px | 4 × 1 |
| Three-up card rows | 3 | 260px | 3 × 1 |
| Product grid | 6 | 280px | 3 × 2 |
| Dropdown columns | 3–4 | 200px | one row |

A group that strands one item on a second row is a bug, not a wrap. This was the single most common defect during design.

---

## Screens

### 1. Home — `Good Practice Supply Homepage.dc.html`

**Purpose:** serve both audiences without the trade side scaring consumers off. Consumer content leads; clinic content sits near the bottom.

**Layout, top to bottom:**
1. **Utility strip + nav**, together inside one `position: fixed` wrapper at `top: 0`. The strip is forest-deep with three centred items (free delivery over $99 · same-day dispatch from Sydney · Help). The nav is a floating glass pill below it. **Do not hard-code the header's top offset** — the strip's height is content-dependent and wraps to two or three rows on phones; they must stack in normal flow inside the fixed wrapper.
2. **Hero** — full-bleed portrait photograph, flat `rgba(14,14,14,.2)` scrim, a forest glass card at `width: min(620px, 64%); min-width: min(320px, 100%)` holding a mint eyebrow pill, `clamp(36px, 4.4vw, 62px)/600` headline ("Better medical supplies, for everyone."), lead, and two buttons. A matching glass fact bar sits 12px below at the same width.
3. **Popular categories** — six photo cards (4:3 image on `--c-plate`, then a footer row with name and mono count, `min-height: 62px` so a two-line name doesn't unbalance the row).
4. **Jump to a category** — 22 pill chips, no imagery.
5. **Always Stocked** — three numbered steps.
6. **Sourcing & standards** — ink band, four numbered rows.
7. **For home** — four cards.
8. **Clinic Portal** — forest band, trade terms table, CTA.
9. **Footer** — forest-deep, three link columns, compliance paragraph.

**Nav:** Shop ▾ · Gauge Finder · Always Stocked · Learn ▾ · Clinic Portal, plus search, sign in and a mint Shop button. Shop and Learn are dropdown panels that open *inside* the nav pill and are mutually exclusive.

### 2. Category — `Good Practice Category.dc.html`
Breadcrumb, category hero with mono product count and editorial intro, filter chips that filter the grid and update a result count, six product cards (spec / name / price / pack size), load more, forest CTA band pointing at the Gauge Finder.

### 3. Product — `Good Practice Product.dc.html`
Gallery of four views of **the product being sold** with selectable thumbnails, gauge and pack-size selectors, one-time versus repeat delivery (15% off), quantity stepper, live total, add-to-cart that increments the header count, a spec sheet that updates with the selected variant, and a related-products row.

### 4. Gauge Finder — `Good Practice Gauge Finder.dc.html`
The consumer differentiator. Full-bleed macro hero, a three-question tool (what you're injecting / where / how often) returning thickness, length, syringe, injections per month and wipes required, **three privacy assurance cards** (answers are not stored, we never ask what it's for, no tracking or profiling), an education block on gauge and length, and three article cards into Learn.

### 5. Always Stocked — `Good Practice Always Stocked.dc.html`
Positioned as **software, not a subscription**: connects to practice software or a manual rhythm, watches consumption, ships before a line runs low. Cadence selector (4/6/8/12 weeks) driving a live schedule and price panel, editable list, four no-lock-in cards.

### 6. Clinic Portal — `Good Practice Clinic Portal.dc.html`
Forest hero with a sign-in panel, **three** capability cards (buy at trade / never run out / send it to patients), account terms table, and an application form with an ABN field.

### 7. Learn — `Good Practice Learn.dc.html`
Gauge Finder promo card, then nine guides in three groups of three.

### 8. Contact — `Good Practice Contact.dc.html`
Five enquiry types (trade pricing, my order, product question, Always Stocked, media and partnerships). Selecting one changes the form fields (trade adds practice name and ABN), the message label and placeholder, the submit label, and the routing note. Alongside: direct contacts per team, a deflection panel, and a panel stating we cannot advise on medicines.

### 9. About — `Good Practice About.dc.html`
The gatekeeping argument, four principles, business facts.

---

## Interactions and behaviour

### Motion tokens
```css
--ease-out: cubic-bezier(.2,.6,.2,1);
--dur-fast: 160ms;   /* press */
--dur-base: 260ms;   /* hover, colour, border, caret */
--dur-slow: 560ms;   /* scroll reveal, image scale */
```

| Pattern | Behaviour |
|---|---|
| Hero entrance | Card rises 16px over 800ms, image fades over 1.1s, once per load |
| Scroll reveal | `IntersectionObserver`, threshold .08, `rootMargin: 0 0 -12% 0`, 16px rise over 560ms, staggered 70ms, then unobserved |
| Card hover | Border to ink, 3px lift, contained image scales to 1.04 |
| Nav / footer links | Left-origin underline scales in over 260ms |
| Arrow links | `→` nudges 4px right |
| Button press | Scale .985 |

**Progressive enhancement is mandatory.** Content is visible by default; the animation is applied by a class the observer adds. Never author content at `opacity: 0` — if the observer fails the failure mode must be "no motion", never "no content". `prefers-reduced-motion` cancels animation and forces visibility.

### State

| Page | State | Notes |
|---|---|---|
| Home | `menu: 'shop' \| 'learn' \| null` | Dropdowns mutually exclusive |
| Category | `filter` | Filters by toggling visibility on rendered cards |
| Product | `img, gauge, pack, mode, qty, cart, added` | Price = pack × qty, × 0.85 when `mode === 'sub'` |
| Gauge Finder | `what, where, often` | All null initially; result fills progressively |
| Always Stocked | `weeks` | Drives schedule dates and price |
| Contact | `reason, sent` | Reason drives fields, labels and routing |
| Clinic Portal | `applied` | Button and note copy |

---

## Assets

All photography is AI-generated placeholder imagery hosted on CloudFront (`d8j0ntlcm91z4.cloudfront.net`), referenced by absolute URL. **These are placeholders and must be replaced with licensed or commissioned photography before launch.** The people shown are AI-generated; Australian advertising rules are strict about implied practitioner endorsement, so any clinical figure must be a clearly identified model or a real consenting customer.

The photography system is three types on one grade — cool neutral daylight, white and pale-grey palette, no warm cast, no timber, shallow depth of field:

1. **Portrait** — a person chest-up against a plain pale wall. Hero only.
2. **Lifestyle and workplace** — a person with the product in a real setting. Face visible, mid-task, unposed.
3. **Object** — product centred on flat seamless pale grey, straight on at eye level, soft even light, one contact shadow. Category and product cards only. These sit on a `--c-plate` background that matches the sweep, so the card blends with no seam.

Never: warm grading, dark dramatic falloff, plinths, gloved hands to camera, needles touching skin, before-and-after, stock-photo smiles, lab coats.

No icon set is used. The three SVG icons (search, account, cart) are inline 18×18 strokes at 1.6px.

---

## Compliance — non-negotiable

- **Consumables only.** Never imply the business supplies peptides, hormones or any prescription medicine.
- **TGA and ARTG claims are per product**, from a real data field, never a blanket site claim. Build the data model accordingly.
- The footer must always carry three statements: supplies only, not medical advice, follow your prescriber.
- No before-and-after imagery, no therapeutic outcome claims.
- The Gauge Finder's privacy promises are commitments, not copy: answers must stay client-side, must not be persisted or attached to an order, and must not feed advertising or profiling.

---

## Implementation notes

- **Prices must render server-side and be visible to anonymous users and crawlers.** This is the commercial differentiator.
- Architecture is three levels deep maximum: home → category → subcategory → product. `Good Practice Supply - Site Architecture.md` has the full page inventory, the protocol-landing SEO layer (`/for/glp-1-injections` etc.), URL patterns, and the index / noindex rules.
- Schema: `Product` with `offers`, `sku`, `brand` and real availability; `BreadcrumbList` sitewide; `FAQPage` on product and learn pages; `Organization` with ABN.
- No em dashes in customer-facing copy — this is a house rule, applied throughout.
- **Always Stocked** and **Gauge Finder** are product names. Always capitalised, never written as "auto-restock", "standing order" or "subscription" in customer-facing copy.

## Files

| File | Contents |
|---|---|
| `Good Practice Supply Homepage.dc.html` | Home |
| `Good Practice Category.dc.html` | Category listing with filters |
| `Good Practice Product.dc.html` | Product detail |
| `Good Practice Gauge Finder.dc.html` | Gauge Finder tool |
| `Good Practice Always Stocked.dc.html` | Always Stocked |
| `Good Practice Clinic Portal.dc.html` | Clinic Portal |
| `Good Practice Learn.dc.html` | Learn hub |
| `Good Practice Contact.dc.html` | Contact with routing |
| `Good Practice About.dc.html` | About |
| `Good Practice Supply - Design System.md` | **Authoritative** design spec |
| `Good Practice Supply - Site Architecture.md` | Sitemap, URL patterns, SEO rules |
| `support.js` | Prototype runtime, for local viewing only. Do not port |

To view the prototypes: keep all files in one folder and open the homepage in a browser. Navigation between pages works via relative links.
