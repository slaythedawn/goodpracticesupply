---
name: gps-guide
description: >
  Write, edit or restructure a guide under /learn for Good Practice Supply,
  including the copy, the schema, the Learn index card, the navigation entry and
  the rebuild. Use this whenever asked to add a guide, article, explainer or
  how-to to this site, to rewrite or extend an existing one, to fix a Learn index
  card, or to produce content aimed at organic search or AI answer engines for
  this repo. Use it even for a request phrased as "write something about needle
  gauges" that does not mention guides at all, because /learn is where that
  belongs.
---

# Writing a Learn guide

The guides are the part of this site that earns authority. The shop is
`noindex` until the catalogue is real, so `/learn` and `/for` are doing all the
work in search, and they are the pages an AI answer engine will quote. That
shapes how they are written: answer the question in the first block, then earn
the rest of the page.

Read `gps-compliance` before writing a word of body copy. The house rules there
are not advisory for this content, they are the reason it is publishable. The
short version, because it governs every sentence here: technique is described as
equipment, never as a dose, a site for a named drug, or a frequency, and the
prescriber comes first and is said to come first.

## Where the content lives

All ten guides are data in `gen/guidecontent.py`, in the `GUIDES` list. Nothing
about a guide is written in HTML. `gen/guides.py` builds the pages from that
list.

Each entry carries:

| field | what it is |
| --- | --- |
| `slug` | URL segment. Lowercase, hyphenated, descriptive, stable once published |
| `title` | the `h1`, and the question the page answers |
| `meta` | the reading time shown on the index card, e.g. `Guide · 6 min` |
| `blurb` | the card body on the Learn index |
| `desc` | the search snippet. Keep it between 70 and 170 characters, which is what `checks/seocheck.mjs` enforces elsewhere on the site, and under 160 if you want it whole in a result |
| `answer` | one line answering the title's question, rendered first and quoted by assistants |
| `body` | list of `(heading, [paragraphs])` |
| `faq` | list of `(question, answer)`, emitted as FAQPage schema |
| `related` | slugs of other guides, rendered as "Read next" cards |

`A_NOTE` in the same file is the standing note that the equipment is not medical
advice and the prescriber comes first. Every guide carries it.

## The answer-first block earns its place

`answer` is the single most valuable field. It is rendered above the body and it
is what gets lifted into an AI answer or a featured snippet. Write it as a
complete, standalone answer to the exact question in the title, in two or three
sentences, with no preamble and no "it depends" unless the dependency is the
answer. If a reader got only that block they should have the real answer.

The body then earns the page: the detail, the exceptions, the reason the answer
is what it is. A guide whose body just restates the answer at greater length is
a thin page, and thin pages do not rank.

The existing ten run 391 to 670 words all up, counting the answer, the headings,
the body and the FAQ, with a median around 480. Match that rather than padding to
a target: `reading-a-syringe` is the shortest and it is not the weakest, because
the question it answers is genuinely smaller than the one `first-injection`
answers. Length should follow the question.

## Everything you have to touch

Adding a guide means more than the one file, and two of the steps are easy to
miss because nothing fails loudly when you skip them.

1. **`gen/guidecontent.py`**. Add the dict to `GUIDES`. `sitemap.py` and
   `llms.py` both import `GUIDES`, so the sitemap and `llms.txt` pick it up
   automatically. That part is handled.
2. **`docs/learn.html`**. The Learn index is one of the seven hand-written
   pages, so the card is not generated. Add it by hand, matching the existing
   cards. Skipping this leaves a published guide nothing links to, which
   `linkcheck.mjs` reports as an orphan.
3. **`docs/about.html`**. The navigation mega-menu lists are grabbed out of
   About by `shop.py` as `LEARNCOLS` and `MENUCOLS`. If the guide belongs in the
   nav, it goes in About and propagates on the next build. Editing the nav in a
   generated page is wasted work.
4. **`related`**. Point at slugs that exist. Nine cards pointing at `#` on the
   Learn index is the defect this whole area was built to stop, and it sat on a
   page open to search because `href="#"` is not an internal path and no link
   checker was looking at it.
5. **`gen/searchindex.py`**. Add a `SYNONYMS` entry if people search for the
   topic in words the title does not use.

Then rebuild and verify with `gps-preflight`. The relevant generators are
`guides.py`, `headmeta.py`, `footer.py`, `searchindex.py`, `llms.py` and
`sitemap.py`, but run the whole sequence rather than guessing the subset.

## Schema

`guides.py` emits three JSON-LD blocks per guide: `Article`, `BreadcrumbList`
and `FAQPage`. That is handled by the generator, so the thing to get right is the
input: `faq` entries have to be real questions with real answers, because
`FAQPage` markup on invented questions is the kind of thing that earns a manual
action. If a guide has no genuine FAQ, leave `faq` empty rather than padding it.

## Voice

Explain the thing, then say why it matters, in short sentences. No salesmanship,
no hype, no second-person cheerleading. The existing guides are the reference,
and `needle-numbers-explained` is the clearest example of the register.

Australian spelling. No em dashes. No emoji. "Always Stocked" and "Gauge Finder"
are capitalised.
