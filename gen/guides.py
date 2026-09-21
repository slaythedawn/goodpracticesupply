# The ten guides under /learn/.
#
# The Learn index has been advertising nine of them as cards linking to "#",
# and the nav promised a tenth, on a page open to search. This builds them.
#
# Copy lives in guidecontent.py. This file is only the page.

import io, os, pathlib, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shop import (HEAD, FOOTER, LEARNCOLS, MENUCOLS, HEADER_VALS, REVEAL,
                  SCRIPT_OPEN, MONO, WRAP, H1, H2, LEAD, CARD, crumbs, page, E,
                  prose, faq_block)
import seo as SEO
from guidecontent import GUIDES, BY_SLUG, A_NOTE

DOCS = str(pathlib.Path(__file__).resolve().parent.parent / 'docs')


def path_of(g):
    return '/learn/' + g['slug']


def build_main(g):
    m = ['<main>\n']
    a = m.append
    a('    <section style="border-bottom:1px solid #E3E3E1">\n')
    a('      <div data-gp-pagehead style="max-width:1440px;margin:0 auto;'
      'padding:clamp(32px,5vw,64px) clamp(20px,5vw,72px) clamp(44px,6vw,80px)">\n')
    a(crumbs([('Home', '/'), ('Guides', '/learn'), (g['title'], None)]))
    a('        <div style="max-width:60ch">\n')
    a('          <div style="%s;font-size:11.5px;letter-spacing:.16em;text-transform:uppercase;'
      'color:#59595A;margin-bottom:16px">%s</div>\n' % (MONO, E(g['meta'])))
    a('          <h1 style="%s">%s</h1>\n' % (H1, E(g['title'])))
    # The answer first. A reader skimming and an assistant looking for something
    # to quote both want the sentence that answers the question in the title.
    a('          <div style="margin-top:22px;padding:18px 20px;background:#EDEDEB;'
      'border-radius:16px">\n')
    a('            <div style="%s;font-size:11px;letter-spacing:.16em;text-transform:uppercase;'
      'color:#1C4034;margin-bottom:8px">The short answer</div>\n' % MONO)
    a('            <p style="margin:0;font-size:16.5px;line-height:1.5;color:#0E0E0E">%s</p>\n'
      % E(g['answer']))
    a('          </div>\n')
    a('          <p style="margin:18px 0 0;font-size:14.5px;line-height:1.6;color:#59595A">%s</p>\n'
      % E(A_NOTE))
    a('        </div>\n      </div>\n    </section>\n\n')

    a(prose(g['body']))
    a(faq_block('Questions about this', g['faq']))

    # Where to go next, which is also what stops these being ten orphans.
    rel = [BY_SLUG[s] for s in g['related']]
    a('    <section style="border-bottom:1px solid #E3E3E1">\n      <div style="%s">\n' % WRAP)
    a('        <h2 style="%s">Read next</h2>\n' % H2)
    a('        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(280px,100%),1fr));'
      'gap:14px;margin-top:clamp(24px,3vw,36px)">\n')
    for r in rel:
        a('          <a href="%s" data-link style="%s;display:block">\n' % (path_of(r), CARD))
        a('            <div style="%s;font-size:11px;letter-spacing:.16em;text-transform:uppercase;'
          'color:#59595A;margin-bottom:10px">%s</div>\n' % (MONO, E(r['meta'])))
        a('            <div style="font-family:\'Archivo\',sans-serif;font-weight:600;font-size:17.5px;'
          'letter-spacing:-.02em;margin-bottom:8px">%s</div>\n' % E(r['title']))
        a('            <div style="font-size:15px;line-height:1.55;color:#3A3A38">%s</div>\n' % E(r['blurb']))
        a('          </a>\n')
    a('        </div>\n')
    a('        <div style="margin-top:clamp(28px,4vw,40px)">\n')
    a('          <a href="/learn" data-link style="font-size:16px;font-weight:600;'
      'border-bottom:1.5px solid #C4C4C2;padding-bottom:3px">All guides <span data-arrow>&rarr;</span></a>\n')
    a('        </div>\n      </div>\n    </section>\n\n')
    a('  </main>')
    return ''.join(m)


SCRIPT = """%s
class Component extends DCLogic {
  state = { menu: null };

%s
  renderVals() {
    return {
%s
%s
%s
    };
  }
}
</script>"""


def head_extra(g):
    path = path_of(g)
    return '\n'.join([
        SEO.head_tags(path=path, title=g['title'], description=g['desc'], kind='article'),
        SEO.jsonld(SEO.article(path=path, headline=g['title'], description=g['desc'])),
        SEO.jsonld(SEO.breadcrumbs([('Home', '/'), ('Guides', '/learn'), (g['title'], path)])),
        SEO.jsonld(SEO.faq_schema(g['faq'])),
    ])


def main():
    out = DOCS + '/learn'
    if not os.path.isdir(out):
        os.makedirs(out)
    script = SCRIPT % (SCRIPT_OPEN, REVEAL, HEADER_VALS, LEARNCOLS, MENUCOLS)
    for g in GUIDES:
        doc = page(g['title'], build_main(g), script, head_extra(g), path_of(g))
        io.open('%s/%s.html' % (out, g['slug']), 'w', encoding='utf-8').write(doc)
        print('%-28s %6d bytes' % (g['slug'], len(doc)))
    print('%d guides written' % len(GUIDES))


if __name__ == '__main__':
    main()
