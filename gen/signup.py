"""Put the sign-up on the pages no generator owns.

The email capture lived in guides.py and nowhere else, so it reached the eleven
guides and missed twenty-four other pages, among them the eight shop categories
and all six /for/ pages: the pages that are actually indexed and the highest
intent on the site. The generated pages are fixed where they are generated. These
five are hand-written HTML with no generator of their own, so the block is
injected here, between fences, the same way learnindex.py owns the Learn cards
inside a hand-written file.

Fenced and idempotent: a second run replaces what the first run wrote rather
than stacking another copy, which the build being idempotent depends on.

about.html is also the file shop.py reads the shared head, header and footer out
of. The block goes inside <main>, which is not part of that extraction, and the
build being idempotent across all ninety-one pages is what proves it.
"""

import io
import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import capture

DOCS = pathlib.Path(__file__).resolve().parent.parent / 'docs'

OPEN, CLOSE = '<!-- gen:signup -->', '<!-- /gen:signup -->'

# page, the source tag written to the contact, the interest tag.
#
# contact.html and clinic-portal.html are deliberately absent. Both already have
# a form, and neither is a sign-up: one is an enquiry and the other is a
# registration. Adding a third email field to either would be asking twice.
PAGES = [
    ('index.html', '/', 'general'),
    ('about.html', '/about', 'general'),
    ('always-stocked.html', '/always-stocked', 'always stocked'),
    ('gauge-finder.html', '/gauge-finder', 'gauge finder'),
    ('learn.html', '/learn', 'general'),
]


def main():
    n = 0
    for name, source, interest in PAGES:
        path = DOCS / name
        if not path.is_file():
            raise SystemExit('signup: %s does not exist' % path)
        s = path.read_text(encoding='utf-8')

        block = OPEN + '\n' + capture.block(source, interest) + '  ' + CLOSE + '\n  '

        if OPEN in s:
            i = s.index(OPEN)
            j = s.index(CLOSE, i) + len(CLOSE) + len('\n  ')
            new = s[:i] + block + s[j:]
        else:
            # The block goes last inside main, after the page has given the
            # reader something, because a sign-up above the content is a sign-up
            # that gets scrolled past.
            if '</main>' not in s:
                raise SystemExit('signup: %s has no </main> to insert before' % name)
            k = s.index('</main>')
            new = s[:k] + block + s[k:]

        if new != s:
            path.write_text(new, encoding='utf-8')
            n += 1
    print('signup: %d of %d hand-written pages updated' % (n, len(PAGES)))


if __name__ == '__main__':
    main()
