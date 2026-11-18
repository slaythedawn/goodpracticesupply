"""Turn the solicitor's Word drafts into the plain text gen/legal.py reads.

    python3.13 legal/convert.py <directory of .docx> [output directory]

The input files are named for their slug: terms.docx, terms-of-use.docx,
privacy.docx, refunds.docx, shipping.docx, payment.docx. Output is one
<slug>.txt per document, in legal/ unless told otherwise.

Neither the .docx files nor the .txt output is committed while the documents are
drafts, and .gitignore enforces that. This repository is public. The drafts carry
highlighted passages that exist precisely because they do not yet describe how
the business operates, and a solicitor's unfinished work product does not belong
on GitHub any more than it belongs on the site. Once a document is settled and
LEGAL_LIVE is on, its text is on the public website anyway, and its .txt can be
committed then by taking it out of .gitignore.

What the conversion has to get right, because these are legal documents:

Clause numbers. Word stores "5.2" and "(a)" as automatic numbering, not as text,
so a naive export drops every one of them and leaves cross-references such as
"subject to clause 5.2" pointing at nothing. The numbering definitions are read
out of the document and the numbers are regenerated.

Highlights. Each highlighted passage is a question the solicitor is asking the
business. A paragraph containing one becomes a line opening with "!!", with the
highlighted words inside [[double brackets]], so the open question survives in
the source and gen/legal.py refuses to publish while any remain.

Headings. The drafts mark headings with bold alone rather than a heading style,
so a short paragraph that is bold throughout is treated as one.
"""

import pathlib
import re
import sys

from docx import Document
from docx.oxml.ns import qn

SLUGS = ('terms', 'terms-of-use', 'privacy', 'refunds', 'shipping', 'payment')
HEADING_MAX = 90


def roman(n):
    out = ''
    for v, s in ((1000, 'm'), (900, 'cm'), (500, 'd'), (400, 'cd'), (100, 'c'),
                 (90, 'xc'), (50, 'l'), (40, 'xl'), (10, 'x'), (9, 'ix'),
                 (5, 'v'), (4, 'iv'), (1, 'i')):
        while n >= v:
            out += s
            n -= v
    return out


def letters(n):
    out = ''
    while n > 0:
        n, r = divmod(n - 1, 26)
        out = chr(97 + r) + out
    return out


FORMATS = {
    'decimal': str,
    'lowerLetter': letters,
    'upperLetter': lambda n: letters(n).upper(),
    'lowerRoman': roman,
    'upperRoman': lambda n: roman(n).upper(),
}


class Numbering:
    """Regenerates Word's automatic clause numbers."""

    def __init__(self, doc):
        self.levels = {}      # numId -> {ilvl: (fmt, text, start)}
        self.counters = {}    # numId -> [count per level]
        try:
            root = doc.part.numbering_part.element
        except Exception:
            return
        abstract = {}
        for a in root.findall(qn('w:abstractNum')):
            lv = {}
            for l in a.findall(qn('w:lvl')):
                i = int(l.get(qn('w:ilvl')))
                fmt = l.find(qn('w:numFmt'))
                txt = l.find(qn('w:lvlText'))
                st = l.find(qn('w:start'))
                lv[i] = (fmt.get(qn('w:val')) if fmt is not None else 'decimal',
                         txt.get(qn('w:val')) if txt is not None else '%1.',
                         int(st.get(qn('w:val'))) if st is not None else 1)
            abstract[a.get(qn('w:abstractNumId'))] = lv
        for n in root.findall(qn('w:num')):
            ref = n.find(qn('w:abstractNumId'))
            if ref is not None:
                self.levels[n.get(qn('w:numId'))] = abstract.get(
                    ref.get(qn('w:val')), {})

    def label(self, p):
        ppr = p._p.pPr
        numpr = ppr.find(qn('w:numPr')) if ppr is not None else None
        if numpr is None:
            return ''
        nid = numpr.find(qn('w:numId'))
        lvl = numpr.find(qn('w:ilvl'))
        if nid is None:
            return ''
        nid = nid.get(qn('w:val'))
        ilvl = int(lvl.get(qn('w:val'))) if lvl is not None else 0
        levels = self.levels.get(nid)
        if not levels or nid == '0':
            return ''
        counts = self.counters.setdefault(nid, [0] * 9)
        fmt, text, start = levels.get(ilvl, ('decimal', '%1.', 1))
        counts[ilvl] = counts[ilvl] + 1 if counts[ilvl] else start
        for deeper in range(ilvl + 1, 9):
            counts[deeper] = 0
        if fmt == 'bullet':
            return ''

        def fill(m):
            i = int(m.group(1)) - 1
            f = levels.get(i, ('decimal',))[0]
            return FORMATS.get(f, str)(counts[i] or 1)

        return re.sub(r'%(\d)', fill, text).strip()


def is_marked(run):
    if run.font.highlight_color is not None:
        return True
    rpr = run._r.rPr
    return rpr is not None and rpr.find(qn('w:shd')) is not None


def is_bold(p):
    runs = [r for r in p.runs if r.text.strip()]
    return bool(runs) and all(
        r.bold or (r.bold is None and p.style.font.bold) for r in runs)


def render(p):
    """The paragraph's text with highlighted spans bracketed, and whether any."""
    parts, any_mark, open_ = [], False, False
    for r in p.runs:
        if not r.text:
            continue
        m = is_marked(r) and bool(r.text.strip())
        if m and not open_:
            parts.append('[[')
            open_ = True
        elif not m and open_ and r.text.strip():
            parts.append(']]')
            open_ = False
        any_mark |= m
        parts.append(r.text)
    if open_:
        parts.append(']]')
    text = ''.join(parts)
    # Runs miss text inside hyperlinks. Fall back rather than lose words.
    if len(re.sub(r'\s|\[\[|\]\]', '', text)) < len(re.sub(r'\s', '', p.text)):
        text = p.text
    text = re.sub(r'\]\](\s*)\[\[', r'\1', text)
    return text, any_mark


def convert(path):
    doc = Document(str(path))
    num = Numbering(doc)
    out, first, n_high = [], True, 0
    for p in doc.paragraphs:
        if not p.text.strip():
            continue
        text, marked = render(p)
        label = num.label(p)
        heading = (is_bold(p) and len(p.text.strip()) <= HEADING_MAX
                   and '\n' not in p.text.strip())
        if first:
            first = False
            if heading:
                continue          # the document title; the page supplies its own
        for i, piece in enumerate(s.strip() for s in text.split('\n')):
            if not piece:
                continue
            piece = re.sub(r'[ \t]+', ' ', piece)
            if i == 0 and label:
                piece = '%s %s' % (label, piece)
            if marked and '[[' in piece or (marked and '[[' not in text):
                kind = '(heading) ' if heading else ''
                full = piece.startswith('[[') and piece.endswith(']]') \
                    and piece.count('[[') == 1
                out.append('!! %s%s' % (kind, piece[2:-2] if full else piece))
                n_high += 1
            elif heading:
                out.append('# %s' % piece)
            else:
                out.append(piece)
            out.append('')
    return '\n'.join(out).rstrip() + '\n', n_high


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    src = pathlib.Path(sys.argv[1])
    dst = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else \
        pathlib.Path(__file__).resolve().parent
    missing = [s for s in SLUGS if not (src / (s + '.docx')).exists()]
    if missing:
        raise SystemExit('convert: missing %s in %s'
                         % (', '.join(m + '.docx' for m in missing), src))
    dst.mkdir(parents=True, exist_ok=True)
    total = 0
    for slug in SLUGS:
        text, n = convert(src / (slug + '.docx'))
        (dst / (slug + '.txt')).write_text(text, encoding='utf-8')
        total += n
        print('%-13s %5d words  %3d open passages' % (slug, len(text.split()), n))
    print('convert: %d open passages across %d documents. gen/legal.py will not '
          'publish any document while one remains.' % (total, len(SLUGS)))


if __name__ == '__main__':
    main()
