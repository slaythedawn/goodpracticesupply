# Good Practice Supply — Design System
> clinical supply, made ordinary

**Theme:** forest chrome, near-white page, photography-led

Good Practice Supply sells medical consumables to people who have never bought them and to practices that buy them every week. The design has to satisfy both without pandering to either: warm enough that a first-time buyer is not intimidated, exact enough that a practice manager trusts the batch number.

The system has three moves and repeats them relentlessly: a **near-white page**, **forest-green chrome and bands**, and **photography with glass laid over it**. Everything else is hairlines, one grotesque and a mono for data.

**This document describes what is built.** If the page and the document disagree, one of them is wrong and it gets fixed in the same turn. Do not re-decide settled things: the lockup, the colour roles, the photography types and the glass rule below are closed.

---

## 1 · Colour

### Ramp

| Name | Value | Token | Role |
|------|-------|-------|------|
| Forest | `#1C4034` | `--c-forest` | The brand. Dark bands, glass tint, wordmark, eyebrow text on light |
| Forest Deep | `#143026` | `--c-forest-deep` | Footer, nav glass base, image plates inside forest sections |
| Forest Line | `#2A5245` | `--c-forest-line` | Hairlines inside forest sections |
| Mint | `#8FBFA6` | `--c-mint` | Action and identity accent. gp tile, primary buttons on dark, eyebrow pills, step numerals on forest |
| Sage Text | `#B7CFC3` | `--c-sage-text` | Body copy and captions on forest. AA at 7.4:1 on Forest |
| Mist | `#DCE5E1` | `--c-mist` | Lead paragraphs on forest, one tier brighter than Sage Text |
| Ink | `#0E0E0E` | `--c-ink` | Body text on light, buttons on light, text inside mint pills |
| Ink Raised | `#3A3A38` | `--c-ink-raised` | Body copy under a heading on light |
| Graphite | `#59595A` | `--c-graphite` | Captions, counts, metadata on light. AA at 6.1:1 |
| Hairline | `#E3E3E1` | `--c-hairline` | Borders and separators on light |
| Surface | `#F2F2F1` | `--c-surface` | Cards and alternating light bands |
| Plate | `#EDEDEB` | `--c-plate` | Behind product photography. Matches the studio background so cards blend |
| Canvas | `#FAFAFA` | `--c-canvas` | Page ground and inverse text. Never pure white |

### Roles, fixed

- **Forest is the chrome.** Nav, glass tint, sourcing band, clinics band and footer are all forest. This is the brand's environment, not an accent.
- **Mint is the action colour.** The gp tile, primary buttons on dark grounds, eyebrow pills and numerals on forest. Always with Forest Deep text on top, never with white.
- **Ink is for reading and for light-surface buttons.** It no longer runs the chrome.
- **No colour outside this ramp.** No blue links, no red errors, no amber warnings. Error and warning states are ink or mint with a mono label and a hairline rule.
- Text on canvas: Ink primary, Ink Raised body, Graphite captions. Text on forest: Canvas primary, Mist lead, Sage Text body. Text on mint: Forest Deep only.

---

## 2 · Typography

One superfamily plus a mono. The wordmark is the heaviest cut of the body face, so the logo never reads as a guest.

### Archivo — everything · `--font-sans`
Weights **400 / 500 / 600**. Nothing lighter than 400.

| Role | Size | Weight | Line height | Tracking |
|------|------|--------|-------------|----------|
| display | `clamp(36px, 4.4vw, 62px)` | 600 | .98 | −.04em |
| heading | `clamp(28px, 3.4vw, 46px)` | 600 | 1.05 | −.03em |
| glass heading | `clamp(26px, 3.2vw, 42px)` | 600 | 1.05 | −.03em |
| card title | 16.5–19px | 600 | 1.3 | −.02em |
| lead | 17.5–18.5px | 400 | 1.45–1.55 | −.005em |
| body | 16px | 400 | 1.55 | −.005em |
| nav | 15px | 500 | 1 | −.005em |

### Archivo Black — wordmark and monogram · `--font-wordmark`
- **Monogram:** `gp` lowercase, −.07em, in a 38px circle with a 1.5px canvas outline, optically nudged 2px down for the descenders.
- **Full wordmark:** `goodpractice` at −.055em over **SUPPLY** at +.32em.
- **Nav lockup:** the outlined circular monogram sits to the left of the full stacked wordmark, both in canvas on the forest bar. The footer and in-page uses carry the wordmark alone.

### IBM Plex Mono — data and labels · `--font-mono`
Weight 500 only. Eyebrow pills (12px, +.16em, uppercase), product counts, step numerals, spec values, copyright. Never a sentence.

---

## 3 · Space, shape, layout

**Base unit 8px.** Page max-width **1440px**, gutters `clamp(20px, 5vw, 72px)`.

| Element | Radius |
|---------|--------|
| glass panels, image frames, feature cards | 28px |
| product and content cards | 22px |
| fact bars, dropdown panels | 20px |
| nav bar | 22px |
| monogram tile | 11px |
| buttons, pills, chips | 1000px |

**Section padding** `clamp(56px, 9vw, 120px)`. Photographic sections carry a floor height: hero `clamp(600px, 84vh, 860px)`, secondary `clamp(540px, 70vh, 760px)`.

### Grid rule, non-negotiable
Every track is `repeat(auto-fit, minmax(min(Npx, 100%), 1fr))`. The `min()` wrapper prevents overflow on small screens, and **N must be chosen so the intended count fits the real container**, not the viewport:

| Group | Count | Floor | Result at 832px |
|-------|-------|-------|-----------------|
| category cards | 6 | 260px | 3 + 3 |
| four-up cards | 4 | 190px | 4 × 1 |
| fact bar | 4 | 150px | 2 × 2 |
| dropdown columns | 3 | 200px | 3 × 1 |

A group that orphans one item on a second row is a bug, not a wrap.

**Elevation: none.** No shadows, no gradients. Depth comes from glass over photography, forest against canvas, and hairlines.

---

## 4 · Glass

Glass is the primary chrome. It has one hard constraint:

> **Glass only ever sits on photography. Never on flat colour.**

On a flat ground a blur has nothing to resolve and reads as a muddy panel. Sections without a photograph use solid `--c-surface` cards instead.

| Token | Value | Where |
|-------|-------|-------|
| **Nav glass** | `rgba(20,48,38,.72)`, blur 26px, saturate 1.6, border `rgba(143,191,166,.26)` | The fixed bar, always |
| **Card glass** | `rgba(20,48,38,.66)`, blur 30px, saturate 1.6, border `rgba(143,191,166,.3)` | Hero and secondary image sections |
| **Strip glass** | `rgba(20,48,38,.6)`, blur 26px, saturate 1.6, border `rgba(143,191,166,.28)` | Fact bars beneath a glass card |

Copy inside glass is always canvas white, with mint for eyebrows and numerals. The scrim under a glass card is a **flat** `rgba(14,14,14,.22–.28)` — never a gradient. Glass cards are capped at 62–64% of the container with a 320px floor so the photograph always reads beside them.

---

## 5 · Photography

**One grade, three types.** The grade is what makes a hybrid brand hold together: cool neutral daylight, white and pale-grey palette, **no warm amber cast, no timber, no props**, shallow depth of field, natural skin texture and fine grain, no logos, no writing.

| Type | What it is | Where it goes |
|------|-----------|---------------|
| **Portrait** | A person chest-up against a plain pale wall, calm, looking just past camera. Subject in one half, clean wall in the other for the glass card | Hero |
| **In-use** | A close crop of hands and product, no face | Secondary image section (how it works) |
| **Lifestyle & workplace** | A person with the product in a real setting: a kitchen bench for home, a clinic counter for practices. Face visible, mid-task, unposed | For home, For clinics |
| **Object** | Product centred on flat seamless pale grey, straight on at eye level, soft even light, one contact shadow, even margins | Category cards only |

**Rules**
- Object shots sit on a `--c-plate` background that matches the studio sweep, so the card blends instead of showing a seam.
- Never use the same photograph twice on one page.
- Match the source aspect to the frame. A landscape packshot in a 4:5 frame loses 40% of its composition.
- Full-bleed photographs are positioned so the subject is pinned visible: use `object-position` on the axis that actually has overflow, and prefer a two-column grid when the subject must never fall behind a card.
- **Never:** warm grading, dark dramatic falloff, plinths and pedestals, gloved hands to camera, needles touching skin, before-and-after, stock-photo smiles, lab coats.

---

## 6 · Components

**Nav** — fixed, 14px from the top, 1440px max, nav glass, 22px radius. Monogram lockup left, links centre at 15px/500 in canvas with a left-origin underline on hover, actions right, mint Shop button. The **Shop** link is a button that expands a dropdown panel *inside* the bar: a hairline rule, then three columns of category links with mono headings in mint. The caret rotates 180°.

**Glass card** — card glass, 28px radius, `clamp(28px, 3.6vw, 46px)` padding. Mint eyebrow pill, heading, lead, then either buttons or hairline-separated rows.

**Category card** — 22px radius, 1px hairline, 4:3 object photo on `--c-plate`, then a footer row with the name at 16.5px/600 and a mono count, `min-height: 62px` so a two-line name does not make its row taller. Hover: border to ink, card lifts 3px, image scales 1.04.

**Jump chip** — pill, `--c-surface` fill, 1px hairline, 15px/500. Hover inverts to ink. Used for the full category directory, without imagery.

**Filled button** — pill, 16px/600, padding 16×30. Mint with Forest Deep text on dark grounds; ink with canvas text on light.

**Outline button** — transparent, 1px border, matching text colour, same geometry.

**Spec row** — label left in Sage Text or Graphite, value right in mono, 14–16px vertical padding, hairline bottom border.

**Step row** — mono numeral in mint, title 18px/600, body 16px, hairline top border.

**Eyebrow** — mono 12px, +.16em, uppercase. Two variants: **mint pill with Forest Deep text** on dark or photographic grounds, **outlined forest pill** on light grounds. Always a pill, never bare text — bare small mono disappears.

**Footer** — Forest Deep ground, full wordmark, three link columns, compliance paragraph, mono copyright.

---

## 7 · Motion

```css
--ease-out: cubic-bezier(.2,.6,.2,1);
--dur-fast: 160ms;   /* press */
--dur-base: 260ms;   /* hover, colour, border, caret */
--dur-slow: 560ms;   /* scroll reveal, image scale */
```

| Pattern | Behaviour |
|---------|-----------|
| Hero entrance | Card rises 16px over 800ms, image fades over 1.1s, once per load |
| Scroll reveal | `IntersectionObserver` threshold .08, rootMargin `0 0 -12% 0`, 16px rise over 560ms, staggered 70ms, then unobserved |
| Card hover | Border to ink, 3px lift, contained image to 1.04 |
| Nav and footer links | Left-origin underline scales in over 260ms |
| Arrow links | `→` nudges 4px right |
| Button press | Scale .985 |

**Progressive enhancement is mandatory.** Content is visible by default; the animation lives on `.is-in`, which the observer adds. Never author content at `opacity: 0` — if the observer fails, the failure mode must be "no motion", never "no content". `prefers-reduced-motion` cancels animation and forces visibility.

---

## 8 · Named products

Two things are products, not features, and always take their capitalised name:

- **Always Stocked** — the repeat delivery service. A set list on a set cadence at 15% off, skippable and cancellable. Never written as auto-restock, standing order or subscription in customer-facing copy.
- **Gauge Finder** — the three-question consumer tool that returns a needle thickness, length and monthly quantity. Named plainly because it is also the search term.

Both appear in the primary nav. Any page that links to one uses the exact name.

---

## 9 · Voice

Plain, precise, unfussy. Consumer first: a first-time buyer should never feel they have wandered into a wholesaler.

- Say the useful thing. "29G, 0.5mL" not "precision-engineered injection solutions".
- Never euphemise. It is a needle, not a delivery device.
- **No em dashes.** Full stops and commas do the work.
- Plain word first, technical word second and only once.
- Never moralise about what a customer injects: *the peptides and hormones are between you and your prescriber, the supplies are on us.*

### Compliance, non-negotiable
- Consumables only. Never imply we supply peptides, hormones or any prescription medicine.
- TGA and ARTG claims are **per product**, from a real data field, never a blanket site claim.
- The footer always carries three statements: supplies only, not medical advice, follow your prescriber.
- No before-and-after imagery. No therapeutic outcome claims.

---

## 10 · Do and don't

**Do**
- Let forest be the chrome and mint be the action.
- Put glass only over photography.
- Keep every photograph on the one cool neutral grade.
- Use weight 600 for headings and titles. Size makes hierarchy, not lightness.
- Choose grid floors that fit the intended count in the real container.
- Give each section one idea and at most two sentences of setup.

**Don't**
- No shadows, no gradients, no elevation.
- No pure white, no pure black, no colour outside the ramp.
- No monogram used alone above favicon size, and no lockup without SUPPLY in it.
- No warm or brown photography, no plinths, no faked luxury for a box of gauze.
- No em dashes.
- No image used twice on one page.
- No content whose visibility depends on JavaScript.
- **Never put a `{{ }}` hole in an `img src`.** The browser resolves the literal string as a relative URL and fetches it during streaming, so the image breaks on every load. Image URLs are always literal markup: unroll the loop, and switch which image shows with opacity or display from state rather than swapping `src`. This has recurred three times; it is the single easiest bug to reintroduce.
