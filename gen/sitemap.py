# sitemap.xml and robots.txt.
#
# robots.txt deliberately does not disallow anything, even while the site is
# unlisted. A crawler that is blocked in robots.txt cannot read the noindex on
# the page, so blocking it is the one way to end up with URLs in an index that
# you have no way to remove. Let them crawl; the noindex does the work.

import io, os, json, hashlib, pathlib, datetime, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from catalogue import CATEGORIES
import seo as SEO

DOCS = str(pathlib.Path(__file__).resolve().parent.parent / 'docs')

# Everything that is a real destination, roughly in order of how much we care.
# priority is a hint, not a ranking factor, but the shape of it documents intent.
STATIC = [
    ('/', '1.0', 'weekly'),
    ('/shop', '0.9', 'weekly'),
    ('/gauge-finder', '0.8', 'monthly'),
    ('/tools/reconstitution-calculator', '0.8', 'monthly'),
    ('/learn/needle-gauge-chart', '0.8', 'monthly'),
    ('/always-stocked', '0.7', 'monthly'),
    ('/clinic-portal', '0.7', 'monthly'),
    ('/learn', '0.6', 'monthly'),
    ('/about', '0.5', 'yearly'),
    ('/contact', '0.5', 'yearly'),
    ('/for/glp-1-injections', '0.8', 'monthly'),
    ('/for/trt-injections', '0.8', 'monthly'),
    ('/for/peptide-reconstitution', '0.8', 'monthly'),
    ('/for/diabetes-at-home', '0.8', 'monthly'),
    ('/for/wound-care-at-home', '0.8', 'monthly'),
    ('/for/clinic-fit-out', '0.8', 'monthly'),
]


# path -> {hash, date}. Committed, because it is the only record of when a page
# last actually changed.
STAMPS = str(pathlib.Path(__file__).resolve().parent / 'lastmod.json')


def page_file(path):
    return DOCS + ('/index.html' if path == '/' else path + '.html')


def stamps():
    try:
        return json.load(io.open(STAMPS, encoding='utf-8'))
    except (IOError, ValueError):
        return {}


def lastmod(path, store, today):
    """When this page last changed, not when the build last ran.

    Google uses lastmod when it can trust it, and stamping every page with
    today's date on every build is how you teach it not to. The build is
    idempotent, so an unchanged page hashes the same and keeps its date.
    """
    f = page_file(path)
    if not os.path.isfile(f):
        raise SystemExit('sitemap: %s is listed but %s does not exist' % (path, f))
    h = hashlib.sha256(io.open(f, 'rb').read()).hexdigest()[:16]
    was = store.get(path)
    if was and was.get('hash') == h:
        return was['date']
    store[path] = {'hash': h, 'date': today}
    return today


def urls():
    # Only pages that are actually indexable. Listing a noindexed URL in a
    # sitemap asks a crawler to fetch a page and then tells it to forget what it
    # found, which wastes crawl budget on a new domain that has little of it.
    today = datetime.date.today().isoformat()
    store = stamps()
    paths = [(p, pr, cf) for p, pr, cf in STATIC if SEO.indexable(p)]
    for c in CATEGORIES:
        if not SEO.indexable('/shop/' + c['slug']):
            continue
        paths.append(('/shop/' + c['slug'], '0.8', 'weekly'))
        for p in c['products']:
            paths.append(('/shop/%s/%s' % (c['slug'], p['slug']), '0.7', 'weekly'))
    out = [(p, pr, cf, lastmod(p, store, today)) for p, pr, cf in paths]
    # Drop pages that are no longer listed, so the file does not grow forever.
    live = {p for p, _, _, _ in out}
    for gone in [k for k in store if k not in live]:
        del store[gone]
    io.open(STAMPS, 'w', encoding='utf-8').write(
        json.dumps(store, indent=1, sort_keys=True) + '\n')
    return out


def main():
    rows = urls()
    o = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, pri, freq, lastmod in rows:
        o.append('  <url><loc>%s%s</loc><lastmod>%s</lastmod>'
                 '<changefreq>%s</changefreq><priority>%s</priority></url>'
                 % (SEO.ORIGIN, path, lastmod, freq, pri))
    o.append('</urlset>')
    io.open(DOCS + '/sitemap.xml', 'w', encoding='utf-8').write('\n'.join(o) + '\n')

    # Named explicitly rather than left to the wildcard, so that the decision is
    # on the record and nobody later "tidies" it into a block. These are the
    # crawlers behind assistant answers and AI search results, and being quoted
    # in one is worth more to a new domain than a ranking it will not get yet.
    #
    # Google-Extended is separate from Googlebot on purpose: it governs AI
    # Overviews and Gemini grounding, and blocking it does not affect Search.
    AI = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-User',
          'Claude-SearchBot', 'PerplexityBot', 'Perplexity-User',
          'Google-Extended', 'Applebot-Extended', 'CCBot', 'meta-externalagent']
    robots = ['# %s' % SEO.ORIGIN, 'User-agent: *', 'Allow: /']
    if not SEO.INDEX_SHOP:
        # Allow, not Disallow, on purpose. See the note at the top of this file:
        # /shop carries noindex, and a crawler has to fetch a page to read it.
        robots += ['',
                   '# /shop carries a noindex meta tag and a matching X-Robots-Tag',
                   '# header while its prices are placeholders. Crawling stays open so',
                   '# that the noindex is readable.']
    # One group with many user-agents, which is valid and reads better than
    # twelve near-identical groups.
    robots += ['', '# Assistant and AI search crawlers, allowed on purpose.']
    robots += ['User-agent: %s' % bot for bot in AI]
    robots += ['Allow: /', '',
               'Sitemap: %s/sitemap.xml' % SEO.ORIGIN,
               '',
               # A comment, not a directive: there is no LLMs: field in the
               # robots.txt spec and inventing one helps nobody. This is a
               # signpost for a human reading the file.
               '# llms.txt lives at %s/llms.txt' % SEO.ORIGIN, '']
    io.open(DOCS + '/robots.txt', 'w', encoding='utf-8').write('\n'.join(robots))
    today = datetime.date.today().isoformat()
    fresh = sum(1 for r in rows if r[3] == today)
    print('sitemap: %d urls (content=%s, shop=%s), %d with today\'s lastmod'
          % (len(rows), SEO.INDEX_CONTENT, SEO.INDEX_SHOP, fresh))


if __name__ == '__main__':
    main()
