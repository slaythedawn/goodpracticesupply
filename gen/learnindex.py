# The guide cards on the Learn index.
#
# They used to be typed into docs/learn.html by hand while the guides themselves
# lived in guidecontent.py, which is two sources of truth for the same facts and
# they had already drifted: nine cards for ten guides, and the sharps card still
# advertised a reading time and a summary that had been rewritten.
#
# A missing card is not a small thing here. The Learn index is how a reader and
# a crawler reach a guide, and the site has been caught once before publishing a
# page that nothing linked to.
#
# The array is fenced by a comment pair and replaced wholesale on every run, so
# this is safe to run repeatedly. Everything outside the fence is left alone.

import io, os, pathlib, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guidecontent import GUIDES

DOCS = str(pathlib.Path(__file__).resolve().parent.parent / 'docs')
OPEN, CLOSE = '/* gen:learncards */', '/* /gen:learncards */'

# Which guides sit under which heading, in the order they should be read. A
# guide missing from here is a mistake rather than a choice, so the build fails
# rather than quietly dropping a card.
SECTIONS = [
    ('Getting started', ['needle-numbers-explained', 'gauge-comparison',
                         'reading-a-syringe', 'first-injection']),
    ('Technique', ['subcutaneous-technique', 'intramuscular-technique',
                   'reconstitution-basics']),
    ('Standards and disposal', ['sharps-disposal-australia', 'artg-explained',
                                'storing-supplies']),
]


def esc(s):
    return s.replace('\\', '\\\\').replace("'", "\\'")


def build():
    by_slug = {g['slug']: g for g in GUIDES}
    placed = [s for _, slugs in SECTIONS for s in slugs]
    missing = [g['slug'] for g in GUIDES if g['slug'] not in placed]
    assert not missing, 'guides with no card on the Learn index: %s' % missing
    unknown = [s for s in placed if s not in by_slug]
    assert not unknown, 'cards for guides that do not exist: %s' % unknown

    out = [OPEN]
    for title, slugs in SECTIONS:
        n = len(slugs)
        out.append("        { title: '%s', count: '%d guide%s', articles: ["
                   % (esc(title), n, '' if n == 1 else 's'))
        rows = []
        for slug in slugs:
            g = by_slug[slug]
            rows.append("          { meta: '%s', title: '%s', href: '/learn/%s', "
                        "body: '%s' }"
                        % (esc(g['meta']), esc(g['title']), g['slug'], esc(g['blurb'])))
        out.append(',\n'.join(rows))
        out.append('        ] },')
    out.append('      ' + CLOSE)
    return '\n'.join(out)


def main():
    path = DOCS + '/learn.html'
    s = io.open(path, encoding='utf-8').read()
    block = build()

    if OPEN in s:
        i = s.index(OPEN)
        j = s.index(CLOSE, i) + len(CLOSE)
        new = s[:i] + block + s[j:]
    else:
        # First run: swallow the hand-written array between "groups: [" and the
        # line that closes it, and fence what replaces it.
        start = s.index('      groups: [') + len('      groups: [\n')
        end = s.index('\n      ]\n', start) + 1
        new = s[:start] + block + s[end:]

    if new != s:
        io.open(path, 'w', encoding='utf-8').write(new)
    cards = sum(len(v) for _, v in SECTIONS)
    print('learn index: %d cards across %d sections%s'
          % (cards, len(SECTIONS), '' if new != s else ' (no change)'))


if __name__ == '__main__':
    main()
