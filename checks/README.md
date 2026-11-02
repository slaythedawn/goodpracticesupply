# Checks

Three scripts that have to pass before anything is pushed. They are the reason a
change across all eighty-one pages is a normal thing to do here rather than a
nervous one.

    cd docs && python3 -m http.server 8777 &
    node checks/linkcheck.mjs      # no server needed
    node checks/seocheck.mjs
    node checks/sweep.mjs
    node checks/depth.mjs

| script | what it catches |
| --- | --- |
| `sweep.mjs` | horizontal overflow, unfilled `{{ }}` holes, JavaScript errors, links that go nowhere, and the header showing both the nav and the burger at once |
| `seocheck.mjs` | title and description length, missing canonical or Open Graph, more or fewer than one `h1`, unparseable structured data, thin pages, duplicate titles |
| `linkcheck.mjs` | internal links pointing at pages that do not exist, and orphans |
| `depth.mjs` | pages more than three clicks from the home page, or with no path to it at all |

`sweep.mjs` samples every sixth page, and checks every hand-written page on each
run regardless, because four widths across ninety-one pages is slower than it is
useful. Widen the sample when touching the header or the footer, which are shared
by every page. A console error counts as a failure, not just an uncaught throw:
the component runtime swallows a bad logic class and logs it instead, so a dead
page looks fine until you read the console.

`browser.mjs` resolves Chromium rather than assuming where it lives. The three
browser checks each hardcoded an absolute path into one machine's global
`node_modules`, so they ran on that machine and nowhere else. Nothing noticed
until CI ran them on a GitHub runner and all three failed on the import. The
same bug, found the same way, as the absolute path in `gen/footer.py`.

Anything under `docs/internal/` is skipped. Those are working pages with no site
header and nothing linking to them, which is deliberate.

## Why the dead-link check lives in the sweep

`href="#"` is not an internal path, so `linkcheck.mjs` never looked at it, and
several of them are filled in by the page component rather than written into the
source, so grepping for them misses those too. Both together are how a Learn
index advertising nine guides, every one of them linking to nothing, sat on a
page open to search without anything noticing.

It is counted in the rendered DOM instead, which is the only place the real
answer exists. The header search control is excluded: it is a button that opens
an overlay, and the `href` is only there so it behaves like one.

It was red on `/learn` until the nine guides were written. It is green now, and
it stays green as long as every card on a page points at something that exists.

## The language gate, and what it covers

`compliance.py` asks seven rules of each block of copy through TypeSafe. Two
modes, both run in `daily-seo.yml` and both blocking:

    python checks/compliance.py --since-change        # the body of every page
    python checks/compliance.py --chrome --since-change   # chrome, titles, descriptions
    python checks/compliance.py --extraction-only     # offline, no key, no cost

Until 2 November the body gate ran with `--depth 2`, which is 26 of 91 pages:
the guides, the eight shop categories, the six `/for/` pages and the calculator.
Everything at depth 1 and depth 3 went unjudged, and that is the home page, the
shop index and all 57 product pages. The filter was written while the product
pages carried `noindex`. They are indexed now, so it had stopped matching the
risk, and the shop index still says you can order without an account on a site
with no checkout, which is the wording this gate reported on four `/for/` pages
in October.

The filter was there to control cost, so it is replaced by something that
controls cost rather than removed. `--since-change` judges a block only when its
text has changed since the last clean verdict, recorded in `checks/judged.json`.
The first run pays for all 91; a day after that costs whatever actually changed.
A block with a finding is never recorded, so it is re-judged every run until it
is fixed, and `RULES_VERSION` in the file retires every entry when a rule is
reworded.

One thing to know before running it by hand: the module default threshold is
0.7 and the workflow passes 0.75. A recorded pass is only reused at a threshold
no stricter than the one it passed at, so a hand run at the default re-judges
everything CI has cached. That is the safe direction, and it is not free. Pass
`--threshold 0.75` to reuse what CI recorded.

`--extraction-only` is the offline half and needs no key. It proves the text
reaches the rules, because a gate that reports nothing looks exactly like a gate
that sees nothing, and it proves the verdict cache skips and re-judges when it
should, because a bug there is a page silently never judged.
