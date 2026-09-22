"""Suggest internal links between the pages that are allowed to rank.

Measured before this was written: of 745 in-body internal links, 48% run
shop to shop, where both ends carry noindex, and only 11.5% connect the 25
content pages. Seven of those have two inbound links or fewer. On a domain with
no external authority, internal links are most of the authority there is to
distribute, and most of it is circulating somewhere Google has been told to
ignore.

The shape of the work suits the model exactly. Questions over one state run in
parallel and cannot see each other, so one request per source page carries one
yes/no per candidate target: would a reader of this page genuinely be helped by
a link to that one. Twenty-five pages, not the 8,190 ordered pairs the whole
site would imply, because the shop is excluded on purpose.

What stays in code: which pages are candidates, which links already exist, how
thin each target is, and how the suggestions are ranked. The judgement bought
from the model is only the part a person would otherwise have to make 600 times.

    python seo/internal_links.py --dry-run     # offline, free
    python seo/internal_links.py               # needs TYPESAFE_API_KEY
"""

import argparse
import collections
import json
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / 'docs'

# Shop pages are noindex until the catalogue is real. A link into one is not
# wasted exactly, but it does not build anything that can rank today.
EXCLUDE = ('/shop', '/internal/')

# Suggest at most this many new links out of any one page. A page that suddenly
# sprouts fifteen links reads as a link farm and helps nobody.
MAX_PER_PAGE = 4


def rel_of(path):
    return '/' + str(path.relative_to(DOCS))


def normalise(href):
    href = href.split('#')[0].split('?')[0].rstrip('/')
    if not href:
        return '/index.html'
    return href if href.endswith('.html') else href + '.html'


def load():
    """Content pages, their main text, their descriptions and their links."""
    pages = {}
    for path in sorted(DOCS.rglob('*.html')):
        rel = rel_of(path)
        if any(rel.startswith(p) for p in EXCLUDE):
            continue
        html = path.read_text(encoding='utf-8')
        main = re.search(r'<main.*?</main>', html, re.S)
        body = main.group(0) if main else ''
        text = re.sub(r'<(script|style|svg).*?</\1>', ' ', body, flags=re.S)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\{\{[^}]*\}\}', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        h1 = re.search(r'<h1[^>]*>(.*?)</h1>', body, re.S)
        desc = re.search(r'<meta name="description" content="([^"]*)"', html)
        links = {normalise(h) for h in re.findall(r'href="(/[^"]*)"', body)}
        pages[rel] = {
            'rel': rel,
            'title': re.sub(r'<[^>]+>', '', h1.group(1)).strip() if h1 else rel,
            'desc': desc.group(1) if desc else '',
            'text': text,
            'links': links,
        }
    # Only links that point at another content page count.
    for page in pages.values():
        page['links'] = {t for t in page['links'] if t in pages and t != page['rel']}
    return pages


def inbound_counts(pages):
    counts = collections.Counter({rel: 0 for rel in pages})
    for page in pages.values():
        for target in page['links']:
            counts[target] += 1
    return counts


def candidates(pages, counts, source):
    """Targets worth asking about: not self, not already linked, thinnest first.

    Thin targets are asked about first because a link is worth most to the page
    that has fewest, and because asking about every pair costs more than the
    answers are worth.
    """
    out = []
    for rel, page in pages.items():
        if rel == source['rel'] or rel in source['links']:
            continue
        out.append((counts[rel], rel, page))
    out.sort(key=lambda item: item[0])
    return out[:10]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--dry-run', action='store_true', help='offline, no key, no cost')
    ap.add_argument('--threshold', type=float, default=0.7)
    ap.add_argument('--limit', type=int, default=0, help='only this many source pages')
    args = ap.parse_args()

    pages = load()
    counts = inbound_counts(pages)
    sources = sorted(pages.values(), key=lambda p: p['rel'])
    if args.limit:
        sources = sources[:args.limit]

    if args.dry_run:
        print('%d content pages, %d links between them\n'
              % (len(pages), sum(len(p['links']) for p in pages.values())))
        print('thinnest targets, by inbound links from other content pages:')
        for rel, n in sorted(counts.items(), key=lambda kv: kv[1])[:10]:
            print('   %2d  %-42s %s' % (n, rel, pages[rel]['title'][:40]))
        example = sources[0]
        cands = candidates(pages, counts, example)
        print('\nexample request, source %s' % example['rel'])
        print('  state: %d characters of its own text' % len(example['text']))
        print('  %d questions in that one request, one per candidate:' % len(cands))
        for n, rel, page in cands[:5]:
            print('     %-40s (%d inbound)' % (rel, n))
        print('\n%d source pages, so %d requests, %d judgements in total.'
              % (len(sources), len(sources),
                 sum(len(candidates(pages, counts, s)) for s in sources)))
        return 0

    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / '.env.local')
    except ImportError:
        pass
    if not os.getenv('TYPESAFE_API_KEY'):
        print('TYPESAFE_API_KEY is not set.', file=sys.stderr)
        return 2

    from typesafe_sdk import Noul, TypeSafeClient
    from typesafe_sdk import TypeSafeAPIConnectionError, TypeSafeError

    suggestions = []
    try:
        with TypeSafeClient() as client:
            for source in sources:
                cands = candidates(pages, counts, source)
                if not cands:
                    continue
                questions = {}
                keys = {}
                for i, (n, rel, page) in enumerate(cands):
                    key = 'q%d' % i
                    keys[key] = (rel, page, n)
                    questions[key] = Noul(
                        instructions='Would a reader partway through this page have a '
                                     'genuine reason to follow a link to a separate '
                                     'page titled "%s", which covers: %s'
                                     % (page['title'], page['desc'][:200]),
                        criteria={
                            'true': 'This page raises a question, term or next step '
                                    'that the other page answers properly, so the '
                                    'link would help a reader rather than interrupt '
                                    'them.',
                            'false': 'The connection is only that both pages are about '
                                     'medical supplies. A link would be filler, or '
                                     'would repeat something this page already covers.',
                        })
                result = client.system_one(
                    state={'page_title': source['title'],
                           'page_text': source['text'][:6000]},
                    questions=questions)
                for key, answer in result.nouls.items():
                    rel, page, n = keys[key]
                    if answer.noul >= args.threshold:
                        suggestions.append({
                            'from': source['rel'], 'to': rel,
                            'to_title': page['title'],
                            'confidence': round(answer.noul, 3),
                            'target_inbound_before': n,
                        })
    except TypeSafeAPIConnectionError as exc:
        print('Could not reach the TypeSafe API: %s' % exc, file=sys.stderr)
        return 3
    except TypeSafeError as exc:
        print('TypeSafe rejected the request: %s' % exc, file=sys.stderr)
        return 1

    # A link is worth most to a page that has fewest, so rank by how thin the
    # target is first and how sure the model is second.
    suggestions.sort(key=lambda s: (s['target_inbound_before'], -s['confidence']))

    kept, per_page = [], collections.Counter()
    for s in suggestions:
        if per_page[s['from']] < MAX_PER_PAGE:
            kept.append(s)
            per_page[s['from']] += 1

    print('\n== Suggested internal links, thinnest targets first ==\n')
    for s in kept:
        print('%-40s -> %-40s %.2f  (target had %d)'
              % (s['from'], s['to'], s['confidence'], s['target_inbound_before']))

    out = ROOT / 'seo' / 'internal-links-suggested.json'
    out.write_text(json.dumps(kept, indent=1), encoding='utf-8')
    print('\n%d suggestions across %d pages, capped at %d per page. Written to %s'
          % (len(kept), len(per_page), MAX_PER_PAGE, out.relative_to(ROOT)))
    print('Nothing has been changed. These are for review, and the links belong in '
          'the generators in gen/, not in docs/.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
