# docs/llms.txt — a plain-text map of the site for language models.
#
# llms.txt is a proposed convention (llmstxt.org), not a standard, and no major
# model provider has committed to reading it. It is here because it costs a few
# kilobytes and the downside is nil, not because it is known to do anything.
# The work that actually earns a citation is the answer-first copy on each guide
# and the structured data in the head.
#
# Only indexable pages are listed, for the same reason the sitemap lists only
# those: the shop is fifty-seven placeholder products at prices no factory has
# quoted, and pointing anything at it would be worse than pointing nothing.

import io, os, pathlib, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pagemeta as META
import seo as SEO
from content import PAGES
from guidecontent import GUIDES

DOCS = str(pathlib.Path(__file__).resolve().parent.parent / 'docs')

INTRO = """> Australian supplier of medical consumables to clinics and to people managing
> treatment at home. Every price is on the page and visible without an account,
> which is not true of the incumbents.

Good Practice Supply sells consumables only: syringes, needles, gloves, swabs,
dressings, diagnostics and clinical waste. We do not supply peptides, hormones
or any prescription medicine, in any form. Nothing on this site is medical
advice, and the directions of a prescriber or treating practitioner come first.

Ordering is not open yet. Prices shown are indicative and the catalogue is not
yet listed for search. Clinic account applications are open.
"""

SECTIONS = [
 ('Start here', ['/']),
 ('Tools', ['/gauge-finder', '/tools/reconstitution-calculator']),
 ('Guides', ['/learn/needle-gauge-chart', '/for/glp-1-injections',
             '/for/trt-injections', '/for/peptide-reconstitution',
             '/for/diabetes-at-home', '/for/wound-care-at-home',
             '/for/clinic-fit-out']
            + ['/learn/' + g['slug'] for g in GUIDES] + ['/learn']),
 ('About', ['/about', '/always-stocked', '/clinic-portal', '/contact']),
]


def main():
    meta = META.all_pages()
    answers = {'/for/' + p['slug']: p['answer'] for p in PAGES}
    answers.update({'/learn/' + g['slug']: g['answer'] for g in GUIDES})
    o = ['# %s' % SEO.BRAND, '', INTRO]
    for title, paths in SECTIONS:
        o.append('## %s' % title)
        o.append('')
        for path in paths:
            m = meta.get(path)
            if not m:
                raise SystemExit('llms: no metadata for ' + path)
            if not SEO.indexable(path):
                continue
            o.append('- [%s](%s%s): %s' % (m['title'], SEO.ORIGIN, path,
                                           answers.get(path) or m['desc']))
        o.append('')
    path = DOCS + '/llms.txt'
    io.open(path, 'w', encoding='utf-8').write('\n'.join(o).rstrip() + '\n')
    print('llms.txt: %d links, %d bytes' % (
        sum(len(p) for _, p in SECTIONS), os.path.getsize(path)))


if __name__ == '__main__':
    main()
