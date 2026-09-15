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
| `sweep.mjs` | horizontal overflow, unfilled `{{ }}` holes, JavaScript errors, and the header showing both the nav and the burger at once |
| `seocheck.mjs` | title and description length, missing canonical or Open Graph, more or fewer than one `h1`, unparseable structured data, thin pages, duplicate titles |
| `linkcheck.mjs` | internal links pointing at pages that do not exist, and orphans |

`sweep.mjs` samples every sixth page plus a fixed set, because four widths across
eighty-one pages is slower than it is useful. Widen the sample when touching the
header or the footer, which are shared by every page.

Anything under `docs/internal/` is skipped. Those are working pages with no site
header and nothing linking to them, which is deliberate.
