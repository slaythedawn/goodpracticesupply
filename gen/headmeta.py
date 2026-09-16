# Head tags and structured data for the seven hand-written pages.
#
# index, about, contact, learn, gauge-finder, always-stocked and clinic-portal
# are not generated, so nothing was putting a description, a canonical, Open
# Graph or any structured data on them. They were the only pages open to search,
# which made that the wrong way round.
#
# The block is fenced by a comment pair and replaced wholesale on every run, so
# running this twice is the same as running it once.

import io, os, pathlib, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pagemeta as META
import seo as SEO

DOCS = str(pathlib.Path(__file__).resolve().parent.parent / 'docs')
OPEN, CLOSE = SEO.HEADMETA_OPEN, SEO.HEADMETA_CLOSE

FILES = {
    'index.html': '/', 'about.html': '/about', 'contact.html': '/contact',
    'learn.html': '/learn', 'gauge-finder.html': '/gauge-finder',
    'always-stocked.html': '/always-stocked', 'clinic-portal.html': '/clinic-portal',
}


def main():
    for f, path in sorted(FILES.items()):
        p = os.path.join(DOCS, f)
        s = io.open(p, encoding='utf-8').read()
        s = SEO.strip_headmeta(s)
        block = '%s\n%s\n%s\n' % (OPEN, META.blocks(path, META.FIXED[path]), CLOSE)
        assert '</head>' in s, f
        s = s.replace('</head>', block + '</head>', 1)
        s = SEO.set_robots(s, path)
        io.open(p, 'w', encoding='utf-8').write(s)
        n = block.count('application/ld+json')
        print('%-22s %-34s %d json-ld block%s' % (f, path, n, '' if n == 1 else 's'))


if __name__ == '__main__':
    main()
