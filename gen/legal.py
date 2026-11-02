"""The six legal pages, from the text in legal/.

Does nothing while SEO.LEGAL_LIVE is False, which is its normal state. The
documents arrived from the lawyer as drafts on 27 October 2026 with highlighted
sections that are open questions about how the business actually operates, and
his covering email says they are to be settled before they go live. legal/ is
never served; this is the only thing that copies any of it into docs/.

Three ways this refuses to run, all of them deliberate:

  a missing source file      the switch is on and a document has not arrived
  a surviving !! highlight   an open question would reach a published page
  an empty document          a page that exists and says nothing is worse than
                             no page, because the footer links to it

A legal page is the one kind of page where being absent is better than being
wrong. So every failure here is a hard exit rather than a warning, and the build
stops instead of shipping half a policy.
"""

import io
import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import seo as SEO
import pagemeta as META
from shop import page, prose, WRAP, H1, MONO, crumbs, E

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / 'legal'
DOCS = str(ROOT / 'docs')

HIGHLIGHT = '!!'


def parse(text, slug):
    """Plain text to [(heading, [paragraph, ...])].

    `# ` opens a section, `## ` a subsection, a blank line separates paragraphs,
    and a line opening with !! is an unresolved highlight carried over from the
    Word document.
    """
    sections, heading, paras, buf, highlights = [], None, [], [], []

    def flush_para():
        if buf:
            paras.append(' '.join(buf).strip())
            del buf[:]

    def flush_section():
        flush_para()
        if heading is not None or paras:
            sections.append((heading or '', list(paras)))
        del paras[:]

    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith(HIGHLIGHT):
            highlights.append(line[len(HIGHLIGHT):].strip())
            continue
        if not line:
            flush_para()
            continue
        if line.startswith('## ') or line.startswith('# '):
            # Both open a section. prose() renders a heading and paragraphs and
            # nothing else: it escapes its input, so a "### Why" pushed into a
            # paragraph renders as the literal characters, which is what the
            # first version of this did. Legal documents are flat numbered
            # clauses in practice, so one heading level loses nothing.
            flush_section()
            heading = line.lstrip('#').strip()
            continue
        buf.append(line)
    flush_section()
    return sections, highlights


def build_one(slug, title, blurb):
    f = SRC / ('%s.txt' % slug)
    if not f.is_file():
        raise SystemExit(
            'legal: %s is missing. SEO.LEGAL_LIVE is on, so every one of the six '
            'documents has to be present. See legal/README.md for the format and '
            'for how to get the text out of the Word files.' % f)

    text = f.read_text(encoding='utf-8')
    sections, highlights = parse(text, slug)

    if highlights:
        raise SystemExit(
            'legal: %s still has %d unresolved highlight%s, and the first is:\n'
            '  %s\n'
            'These are the sections the lawyer marked for discussion because they '
            'have to match how the business actually works. Settle them and remove '
            'the !! lines. Publishing one is publishing a statement about this '
            'business that may not be true.'
            % (slug, len(highlights), '' if len(highlights) == 1 else 's',
               highlights[0][:160]))

    if not any(paras for _, paras in sections):
        raise SystemExit('legal: %s has no content. A page the footer links to '
                         'that says nothing is worse than no page.' % slug)

    path = '/' + slug
    m = []
    a = m.append
    a('<main>\n')
    a('    <section style="border-bottom:1px solid #E3E3E1">\n      <div style="%s">\n' % WRAP)
    a('        %s\n' % crumbs([('Home', '/'), (title, path)]))
    a('        <h1 style="%s;max-width:26ch">%s</h1>\n' % (H1, E(title)))
    a('        <p style="margin:16px 0 0;font-size:17px;line-height:1.6;color:#3A3A38;'
      'max-width:62ch">%s</p>\n' % E(blurb))
    a('      </div>\n    </section>\n\n')
    a(prose(sections))
    a('  </main>')

    return page(title, ''.join(m), '',
                head_extra=META.blocks(path, META.legal(title, blurb, path)),
                path=path)


def main():
    if not SEO.LEGAL_LIVE:
        print('legal: LEGAL_LIVE is off, so nothing was written. '
              'The six documents are drafts, see legal/README.md.')
        return 0
    # Build all six, then write all six. Two reasons, and the first one bit.
    #
    # io.open(path, 'w') truncates before the expression that produces the
    # content runs, so writing as it went left a zero byte docs/terms.html
    # behind when the first document was refused, and footer.py then died
    # trying to patch a page with no footer in it.
    #
    # The second is the real one: the footer links to all six, so six pages or
    # none. Five live policies and one 404 is worse than no policies.
    built = []
    for slug, title, blurb in SEO.LEGAL_PAGES:
        built.append((slug, title, build_one(slug, title, blurb)))
    for slug, title, html in built:
        io.open('%s/%s.html' % (DOCS, slug), 'w', encoding='utf-8').write(html)
        print('  %-14s %s' % (slug, title))
    print('legal: wrote %d pages' % len(built))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
