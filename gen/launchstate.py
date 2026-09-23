"""Flip the launch-state calls to action with the same switch as everything else.

The shop buttons already read "Coming soon" because SEO.PURCHASABLE is off, and
they will read the real thing the day it is on, without anyone editing copy. The
hand-written pages did not work that way: their buttons were typed in, so
launching meant remembering which pages had a button and what it used to say.
That is the kind of thing that gets missed, and the miss is a live site inviting
an order it cannot take, or a "Coming soon" sitting on a shop that opened weeks
ago.

Mark the element with the label it should carry once orders are open:

    <a href="..." data-gp-launch-cta="Start Always Stocked">Coming soon</a>

This pass writes the right one in. Run it after the other generators, before
the footer. It is idempotent either way.
"""

import glob
import io
import os
import pathlib
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo as SEO

DOCS = str(pathlib.Path(__file__).resolve().parent.parent / 'docs')
WAITING = 'Coming soon'

_CTA = re.compile(r'(data-gp-launch-cta="([^"]+)"[^>]*>)([^<]*)(<)')


def main():
    os.chdir(DOCS)
    changed = found = 0
    for pat in ['*.html', 'for/*.html', 'shop/*.html', 'shop/*/*.html',
                'tools/*.html', 'learn/*.html']:
        for f in sorted(glob.glob(pat)):
            s = io.open(f, encoding='utf-8').read()
            if 'data-gp-launch-cta' not in s:
                continue

            def sub(m):
                global_label = m.group(2) if SEO.PURCHASABLE else WAITING
                return m.group(1) + global_label + m.group(4)

            found += len(_CTA.findall(s))
            s2 = _CTA.sub(sub, s)
            if s2 != s:
                io.open(f, 'w', encoding='utf-8').write(s2)
                changed += 1
    print('launch state: %d marked buttons, %d files updated, purchasable=%s'
          % (found, changed, SEO.PURCHASABLE))


if __name__ == '__main__':
    main()
