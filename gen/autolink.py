"""Apply the approved internal links to the built pages.

seo/internal_links.py decides which links would help a reader. Applying them was
a manual job, done once by hand, which is why the link graph improved in one
afternoon in September and not since. This closes that gap: the loop suggests on
every run and this puts them in.

It works on built HTML rather than on the Python that generates it, for the same
reason footer.py and optimise_images.py do. The copy lives inside quoted strings
across guidecontent.py, catalogue.py and the CATEGORY_SEO table, and a script
that rewrites source strings to insert markup is a script that will one day put a
link inside a Python literal and take the build down. A post-pass over rendered
HTML can be read, re-run, and reverted by rebuilding.

Rules it will not break:

  Only inside <main>, and only inside a <p>. Headings, tables, nav, the footer
  and anything in an attribute are left alone.
  Never inside an existing <a>. Nested anchors are invalid and the second one
  silently swallows the first.
  One link per target per page. A page that mentions sharps four times gets one
  link, not four.
  Whole words only. The substring trap that put "ear syringe" in the wrong
  cluster applies here too, and here it would be visible.

Idempotent. A page that already links to the target is skipped, so running it
twice changes nothing and the build stays reproducible.
"""

import html
import io
import json
import os
import pathlib
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from inline import LINKSTYLE

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / 'docs'
SUGGESTED = ROOT / 'seo' / 'internal-links-suggested.json'

# Only links the model was confident about. The suggester's own default is 0.75
# and four suggestions once landed at exactly the threshold, so this sits above
# it rather than on it.
THRESHOLD = 0.8

# A page that sprouts links reads as a link farm and helps nobody.
MAX_PER_PAGE = 4

PARA = re.compile(r'(<p\b[^>]*>)(.*?)(</p>)', re.S)
ANCHOR_SPLIT = re.compile(r'(<a\b.*?</a>|<[^>]+>)', re.S)


def load():
    if not SUGGESTED.exists():
        return []
    data = json.loads(SUGGESTED.read_text(encoding='utf-8'))
    rows = data.get('suggestions', data) if isinstance(data, dict) else data
    out = []
    for r in rows:
        if (r.get('score') or r.get('helps') or 0) < THRESHOLD:
            continue
        if not (r.get('source') and r.get('target') and r.get('anchor')):
            continue
        out.append(r)
    return out


def as_path(rel):
    path = rel[:-len('.html')] if rel.endswith('.html') else rel
    if path.endswith('/index'):
        path = path[:-len('/index')] or '/'
    return path or '/'


def main_span(doc):
    m = re.search(r'<main\b.*?</main>', doc, re.S)
    return (m.start(), m.end()) if m else None


def link_once(main_html, anchor, href):
    """Wrap the first free occurrence of `anchor` inside a paragraph."""
    escaped = html.escape(anchor)
    pattern = re.compile(r'(?<![A-Za-z0-9])' + re.escape(escaped) + r'(?![A-Za-z0-9])')
    replacement = '<a href="%s" style="%s">%s</a>' % (href, LINKSTYLE, escaped)
    done = [False]

    def do_para(m):
        if done[0]:
            return m.group(0)
        open_tag, body, close_tag = m.groups()
        # Split so that existing anchors and tags are never touched, only the
        # text between them.
        parts = ANCHOR_SPLIT.split(body)
        for i, part in enumerate(parts):
            if part.startswith('<'):
                continue
            new, n = pattern.subn(replacement, part, count=1)
            if n:
                parts[i] = new
                done[0] = True
                break
        return open_tag + ''.join(parts) + close_tag if done[0] else m.group(0)

    out = PARA.sub(do_para, main_html)
    return (out, True) if done[0] else (main_html, False)


def main():
    rows = load()
    if not rows:
        print('autolink: no suggestions at or above %.2f, nothing to apply' % THRESHOLD)
        return 0

    by_source = {}
    for r in rows:
        by_source.setdefault(r['source'], []).append(r)

    applied = skipped = missed = 0
    touched = 0
    for source, items in sorted(by_source.items()):
        path = DOCS / source.lstrip('/')
        if not path.exists():
            print('  no such page: %s' % source)
            continue
        doc = io.open(path, encoding='utf-8').read()
        span = main_span(doc)
        if not span:
            continue
        head, main_html, tail = doc[:span[0]], doc[span[0]:span[1]], doc[span[1]:]
        before = main_html
        placed = 0
        for r in sorted(items, key=lambda r: -(r.get('score') or 0)):
            if placed >= MAX_PER_PAGE:
                break
            href = as_path(r['target'])
            if 'href="%s"' % href in main_html:
                skipped += 1
                continue
            main_html, ok = link_once(main_html, r['anchor'], href)
            if ok:
                applied += 1
                placed += 1
            else:
                missed += 1
        if main_html != before:
            io.open(path, 'w', encoding='utf-8').write(head + main_html + tail)
            touched += 1

    print('autolink: %d link%s applied across %d page%s, %d already present, '
          '%d anchor%s not found in the rendered copy'
          % (applied, '' if applied == 1 else 's', touched,
             '' if touched == 1 else 's', skipped, missed,
             '' if missed == 1 else 's'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
