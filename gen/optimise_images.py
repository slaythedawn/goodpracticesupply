"""Point every photograph at the image optimiser, sitewide.

A post-pass rather than an edit at each of the dozen places an <img> is written,
for the same reason footer.py is a post-pass: the tags are scattered across
shop.py, build.py, tools.py and five hand-written pages, and a rule applied in
one place cannot drift from a rule applied in another.

Run it after everything that writes HTML. It is idempotent: a src already
pointing at the optimiser is left alone.
"""

import glob
import io
import os
import pathlib
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from images import HOSTS, OPTIMISE, optimised, srcset

DOCS = str(pathlib.Path(__file__).resolve().parent.parent / 'docs')

# A photograph in a card or a gallery is never full width on a large screen, so
# telling the browser roughly how wide it will be stops it choosing the largest
# candidate every time.
SIZES_ATTR = ' sizes="(max-width: 700px) 100vw, (max-width: 1200px) 50vw, 33vw"'

_IMG = re.compile(r'<img\b[^>]*>')
_SRC = re.compile(r'src="(https://[^"]+)"')


def rewrite(tag):
    if 'srcset=' in tag or '/_vercel/image' in tag:
        return tag
    m = _SRC.search(tag)
    if not m:
        return tag
    url = m.group(1)
    if not any(h in url for h in HOSTS):
        return tag
    out = tag.replace(m.group(0), 'src="%s"' % optimised(url, 1080))
    ss = srcset(url)
    if ss:
        out = out[:-1].rstrip() + ss + SIZES_ATTR + '>'
    return out


def main():
    if not OPTIMISE:
        print('image optimisation off, nothing rewritten')
        return
    os.chdir(DOCS)
    pages = touched = tags = 0
    for pat in ['*.html', 'for/*.html', 'shop/*.html', 'shop/*/*.html',
                'tools/*.html', 'learn/*.html']:
        for f in sorted(glob.glob(pat)):
            s = io.open(f, encoding='utf-8').read()
            pages += 1
            n = [0]

            def sub(m):
                out = rewrite(m.group(0))
                if out != m.group(0):
                    n[0] += 1
                return out

            s2 = _IMG.sub(sub, s)
            if s2 != s:
                io.open(f, 'w', encoding='utf-8').write(s2)
                touched += 1
                tags += n[0]
    print('image optimiser: %d tags rewritten across %d of %d pages'
          % (tags, touched, pages))


if __name__ == '__main__':
    main()
