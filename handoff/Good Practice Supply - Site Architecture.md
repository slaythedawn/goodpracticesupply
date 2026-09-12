# Good Practice Supply — Site Architecture

Built against the four Australian incumbents (TeamMed, Medisa, Tomlin, Icon). Their structure is a deep B2B catalogue behind a login: 7 top categories, 9,000+ SKUs, register-to-see-pricing, and almost no editorial. That gives us two openings: **every page is indexable and priced**, and **we own the question layer they ignore entirely**.

---

## 1 · Primary navigation

```
[gp] goodpractice SUPPLY    Shop ▾   Kits   Learn ▾   For clinics ▾      ⌕  Sign in  Cart
```

A slim utility strip sits above: free delivery over $99 · same-day dispatch from Sydney · Help.

### Shop ▾ (four columns)
| By category | By need | By protocol | Featured |
|---|---|---|---|
| Injection & infusion | Self-injection at home | GLP-1 and weight loss | Specials & clearance |
| Diluents & skin prep | Treatment room restock | TRT and hormone therapy | New this month |
| Gloves, PPE & hygiene | Wound care at home | Peptide protocols | Bestsellers |
| Wound care & dressings | Diabetes management | Diabetes | Quick order by code |
| Diagnostics & consult room | First aid & home kit | Post-procedure care | Download catalogue |
| Recovery & everyday | Clinic fit-out | Vaccination clinics | Shop all 155 |

Two entry models on purpose: clinics browse by **category**, consumers browse by **need** or **protocol**. The protocol column is the SEO column.

### Learn ▾ (three columns)
| Getting started | Technique | Standards & disposal |
|---|---|---|
| Which needle do I need | How to inject subcutaneously | Sharps disposal by state |
| What the numbers mean | How to inject intramuscularly | What ARTG listing means |
| Your first injection | Reconstituting a powder | Storing supplies correctly |
| Reading a syringe | Rotating injection sites | Batch and expiry explained |

### For clinics ▾
Open an account · Trade pricing · Standing orders · Patient Direct · Practice setup · Invoicing and PO · Contact your account manager

---

## 2 · Page inventory

### Commerce
| Path | Type | Purpose |
|---|---|---|
| `/` | Home | Both audiences, category and need entry |
| `/shop` | All products | Faceted, indexable, priced |
| `/shop/{category}` | Category landing | 6 of these. Editorial intro, subcategory tiles, product grid |
| `/shop/{category}/{subcategory}` | Subcategory | ~30 of these. The main organic landing layer |
| `/shop/{category}/{subcategory}/{product}` | Product | Specs, variants, batch, guidance, related |
| `/kits` and `/kits/{slug}` | Bundles | Starter kit, restock kit, clinic room kit |
| `/specials`, `/clearance`, `/new` | Merchandising | Competitors all run these and they convert |
| `/brands` and `/brands/{brand}` | Brand | Clinics search by brand. Pure organic capture |
| `/quick-order` | Tool | Paste codes or upload a CSV. Trade convenience |

### Need and protocol landings — the SEO layer
| Path | Target |
|---|---|
| `/for/glp-1-injections` | "what do I need to inject ozempic at home" |
| `/for/trt-injections` | "trt injection supplies australia" |
| `/for/peptide-reconstitution` | "bacteriostatic water australia" |
| `/for/diabetes-at-home` | "insulin syringes australia" |
| `/for/wound-care-at-home` | "dressings for home use" |
| `/for/clinic-fit-out` | "setting up a medical practice supplies" |

Each is a real landing page: what you need, why, a shoppable kit, and links down into the products. This is where a consumer who has never heard of us arrives.

### Spec-level pages
`/shop/injection/insulin-syringes/29g-13mm` and siblings. Indexable filter combinations for the handful of specs people actually search by gauge and length. Everything else stays as a `noindex` facet.

### Learn — the question layer
| Path | Target query |
|---|---|
| `/learn/which-needle-do-i-need` | "what size needle for semaglutide" |
| `/learn/needle-gauge-chart` | "needle gauge chart australia" |
| `/learn/29g-vs-30g-vs-31g` | comparison intent |
| `/learn/how-to-reconstitute` | "how much bacteriostatic water to add" |
| `/learn/units-on-a-syringe` | "how many units is 0.25mg" |
| `/learn/your-first-injection` | "how to inject yourself" |
| `/learn/sharps-disposal/{state}` | 8 pages. "sharps disposal nsw" etc. Genuinely useful and locally targeted |
| `/learn/glossary` | long-tail definitions |

None of the four incumbents publish any of this.

### Trust, service and support
`/sourcing` · `/standards` · `/about` · `/for-clinics/*` · `/practice-setup` · `/help` · `/help/delivery` · `/help/returns` · `/help/faq` · `/contact` · `/account/*` · `/legal/*`

---

## 3 · SEO rules

- **Depth of three, maximum.** Home → category → subcategory → product. Never deeper.
- **Indexable**: categories, subcategories, products, kits, need and protocol landings, learn articles, brands, the chosen spec pages.
- **Noindex**: search results, cart and checkout, account, every unchosen facet combination, pagination beyond page one (canonical to page one).
- **One H1 per page**, matching the primary query in plain language.
- **Editorial intro on every category and subcategory** — 80 to 150 words above the grid, not filler below it.
- **Schema**: `Product` with `offers`, `sku`, `gtin`, `brand` and real availability; `BreadcrumbList` sitewide; `FAQPage` on product and learn pages; `Organization` with ABN and address.
- **Internal linking**: every product links up to its subcategory and across to its protocol landing; every learn article links to the kit that answers it. That reciprocal loop between advice and cart is the whole model.
- **Prices visible to crawlers.** The incumbents hide pricing behind login, so their product pages cannot rank on commercial queries. Ours can.
- **Per-product ARTG and batch data** as structured fields, never a blanket site claim.

---

## 4 · Gaps against the incumbents

**They have, we need:** specials and clearance, downloadable catalogue, quick order by code, practice setup service, seasonal hubs (flu and vaccine season), events and education, returns and credit form, delivery and handling charges page, FAQ, certification badges, named account managers, brand pages.

**We have, they do not:** visible pricing without an account, consumer purchasing, repeat delivery, plain packaging, batch and expiry before purchase, and an entire guidance layer.

**Nobody has:** protocol-based shopping (GLP-1, TRT, peptides, diabetes) as a first-class navigation axis. That is the wedge, and it should be built first.
