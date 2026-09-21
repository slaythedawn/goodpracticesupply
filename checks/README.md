# Checks

Three scripts that have to pass before anything is pushed. They are the reason a
change across all eighty-one pages is a normal thing to do here rather than a
nervous one.

    cd docs && python3 -m http.server 8777 &
    node checks/linkcheck.mjs      # no server needed
    node checks/seocheck.mjs
    node checks/sweep.mjs

| script | what it catches |
| --- | --- |
| `sweep.mjs` | horizontal overflow, unfilled `{{ }}` holes, JavaScript errors, links that go nowhere, and the header showing both the nav and the burger at once |
| `seocheck.mjs` | title and description length, missing canonical or Open Graph, more or fewer than one `h1`, unparseable structured data, thin pages, duplicate titles |
| `linkcheck.mjs` | internal links pointing at pages that do not exist, and orphans |

`sweep.mjs` samples every sixth page plus a fixed set, because four widths across
eighty-one pages is slower than it is useful. Widen the sample when touching the
header or the footer, which are shared by every page.

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

**This check is currently red on `/learn`.** That is the nine guides, and it is
a real defect rather than a broken check. It goes green when they are written.
