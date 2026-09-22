---
name: gps-preflight
description: >
  Rebuild and verify the Good Practice Supply site before committing or pushing.
  Runs the generators in the order that works, then the config, link, SEO and
  browser checks, then confirms the build is idempotent. Use this whenever
  anything under gen/, docs/, api/ or vercel.json has changed, and always before
  a commit or a push, including changes that look far too small to need it. Also
  use it when a check is already failing and you need to establish whether the
  failure is yours or was there before you started.
---

# Preflight

The site is live. Every push goes straight to production on a domain that is now
being indexed, and there is no staging environment in between. That is the whole
reason this sequence exists: the checks are not ceremony, they are the only thing
standing between a bad edit and a broken page in front of a customer.

Run it in full. The cheap checks have caught real defects that looked impossible,
and the expensive one has caught defects the cheap ones structurally cannot see.

## Rebuild first, then check

Most of `docs/` is generated. A change made by hand in `docs/` is gone the next
time a generator runs, so checking before rebuilding tells you about a site that
is about to stop existing.

The order is in `gen/README.md` under "Build order" and it is load bearing. Read
it there rather than trusting this file, because the generators change. The two
constraints behind the order, so you can reason about it rather than copying it:

- `shop.py` runs `main()` on import, so importing it rebuilds the shop. That is
  why `build.py` and `tools.py` each rebuild more than they appear to.
- `headmeta.py` writes to `docs/about.html`, and `build.py` reads its page shell
  out of `docs/about.html`. Run `headmeta.py` after `build.py` or generated pages
  inherit About's canonical, which is invisible in a browser and fatal in Search
  Console.

`sitemap.py` runs last, after every page exists, because it hashes each file to
decide whether `lastmod` should move.

## Then the checks

    cd docs && python3 -m http.server 8777 &
    node checks/config.mjs
    node checks/linkcheck.mjs
    node checks/seocheck.mjs
    node checks/sweep.mjs

`checks/README.md` says what each one catches. What matters when reading the
output:

- **`config.mjs` is not optional and not cosmetic.** Vercel validates
  `vercel.json` before it builds, so a bad key produces a failed deploy with no
  build log at all. An unknown `"comment"` key took production down for two
  deploys and presented as "Add to cart is still live", because the browser was
  being served the last good build.
- **`sweep.mjs` counts a console error as a failure**, not just an uncaught
  throw. The component runtime catches a bad logic class and logs
  `logic class eval FAILED` instead of throwing, so a completely dead page renders
  a plausible-looking shell. The contact page was dead for a commit and a half
  because nothing was reading the console.
- **Dead links are counted in the rendered DOM**, not in the source. Many hrefs
  are filled in by the page component, so grep misses them. `href="#"` is not an
  internal path, so `linkcheck.mjs` never sees it either.

Green means: `vercel.json: ok`, 0 broken links and 0 orphans, 0 shop pages with
problems and titles and descriptions all unique, and 0 sweep failures.

## Confirm the build is idempotent

    git status --short      # expect clean
    python3 gen/build.py && python3 gen/shop.py
    git status --short      # expect clean again

A generator that produces different output on a second run with no input change
means something non-deterministic is leaking into the pages, and the next person
to touch an unrelated file gets a diff they did not make. Do not push while this
is failing.

## Reporting the result

Say what you actually ran and what actually came back, with the numbers. If you
sampled rather than ran the full sweep, say that you sampled. Three times in this
repo's history a check was reported green when it had only been run over part of
the site, and each time the gap was where the defect was: source-only link
checking missed component-filled hrefs, a page sample missed the dead contact
page, and watching only `pageerror` missed every logged console error.

If a check is red, establish whether it is yours before fixing it. `git stash`
and re-run is usually the fastest answer. A pre-existing failure is still worth
fixing, but it is worth knowing which kind you are looking at, and worth saying
so to the user rather than quietly absorbing it into your change.

## Committing

Develop and push only on the branch the session was given. Commit messages in
this repo describe what changed and why in plain prose, present tense, no prefix
convention. Do not put a model name or identifier in a commit message, a PR, or a
code comment.

Do not open a pull request unless the user explicitly asks for one.
