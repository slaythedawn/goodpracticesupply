# sitemap.xml and robots.txt.
#
# robots.txt deliberately does not disallow anything, even while the site is
# unlisted. A crawler that is blocked in robots.txt cannot read the noindex on
# the page, so blocking it is the one way to end up with URLs in an index that
# you have no way to remove. Let them crawl; the noindex does the work.

import io, os, pathlib, datetime, sys
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


def urls():
    today = datetime.date.today().isoformat()
    out = [(p, pr, cf, today) for p, pr, cf in STATIC]
    for c in CATEGORIES:
        out.append(('/shop/' + c['slug'], '0.8', 'weekly', today))
        for p in c['products']:
            out.append(('/shop/%s/%s' % (c['slug'], p['slug']), '0.7', 'weekly', today))
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

    robots = ['# %s' % SEO.ORIGIN, 'User-agent: *']
    if SEO.INDEXABLE:
        robots.append('Allow: /')
    else:
        # Still Allow, on purpose. See the note at the top of this file: the
        # pages carry noindex, and a crawler has to be able to fetch them to
        # see it.
        robots += ['Allow: /',
                   '# Every page currently carries a noindex meta tag and a matching',
                   '# X-Robots-Tag header. Crawling is allowed so that is readable.']
    robots += ['', 'Sitemap: %s/sitemap.xml' % SEO.ORIGIN, '']
    io.open(DOCS + '/robots.txt', 'w', encoding='utf-8').write('\n'.join(robots))
    print('sitemap: %d urls, robots.txt written (indexable=%s)' % (len(rows), SEO.INDEXABLE))


if __name__ == '__main__':
    main()
