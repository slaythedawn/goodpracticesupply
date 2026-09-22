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

# Only pages that can rank are worth linking between. The shop categories index
# now and the product pages do not, so the answer comes from seo.py rather than
# from a path prefix, and it changes on its own when the catalogue is real.
sys.path.insert(0, str(ROOT / 'gen'))
import seo as SEO


def rankable(rel):
    path = rel[:-len('.html')] if rel.endswith('.html') else rel
    if path.endswith('/index'):
        path = path[:-len('/index')] or '/'
    return not rel.startswith('/internal/') and SEO.indexable(path)

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
        if not rankable(rel):
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


# Anchor phrases are looked up, not judged. Finding whether a form of words
# already appears in a page is exact string work, and a model asked to do it
# would sometimes say yes about a phrase that is not there.
# A phrase may not begin or end on any of these. Articles and prepositions
# because they read as a stray word; verbs because a span can be contiguous and
# still straddle a grammatical boundary. "What the numbers on a needle mean"
# contains "needle mean" as two adjacent words, and the first live run suggested
# wrapping it in two pages, which would have published nonsense.
STOP = {'the', 'a', 'an', 'and', 'or', 'of', 'for', 'to', 'in', 'on', 'at',
        'is', 'it', 'what', 'how', 'why', 'which', 'who', 'when', 'where',
        'your', 'you', 'that', 'with', 'step', 'by', 'actually',
        'mean', 'means', 'meant', 'explained', 'do', 'does', 'go', 'goes',
        'get', 'gets', 'need', 'needs', 'should', 'can', 'will', 'are', 'was'}


def _spans(words):
    """Contiguous runs of two or three words, never starting or ending on a stopword.

    The first version filtered stopwords out and then took n-grams of what was
    left, which joins words that were never next to each other. From "What the
    numbers on a needle mean" it produced "needle mean", and the first live run
    duly suggested wrapping that phrase in two pages. An anchor has to be a
    thing someone actually wrote.
    """
    out = []
    for n in (3, 2):
        for i in range(len(words) - n + 1):
            span = words[i:i + n]
            if span[0] in STOP or span[-1] in STOP:
                continue
            if any(len(w) < 3 for w in span):
                continue
            out.append(' '.join(span))
    return out


def phrases_for(page):
    """Forms of words that would honestly introduce this page."""
    slug = page['rel'].rsplit('/', 1)[-1][:-len('.html')].split('-')
    title = re.sub(r'[^a-z0-9 ]', ' ', page['title'].lower()).split()
    seen, uniq = set(), []
    for phrase in _spans(slug) + _spans(title):
        if phrase not in seen and len(phrase) > 8:
            seen.add(phrase)
            uniq.append(phrase)
    return uniq


def anchor_in(source_text, target):
    """The phrase already sitting in the copy that should become the link."""
    low = source_text.lower()
    for phrase in phrases_for(target):
        i = low.find(phrase)
        if i >= 0:
            return source_text[i:i + len(phrase)]
    return None


def candidates(pages, counts, source):
    """Every page this one does not already link to.

    Formerly the ten thinnest. At roughly two hundredths of a cent per
    judgement, shortlisting saved nothing and hid the links it did not ask
    about. Thinnest first still, because that decides what gets read when there
    is more here than anyone wants to apply.
    """
    out = [(counts[rel], rel, page) for rel, page in pages.items()
           if rel != source['rel'] and rel not in source['links']]
    out.sort(key=lambda item: item[0])
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--dry-run', action='store_true', help='offline, no key, no cost')
    # 0.75, not 0.70. The first live run returned four suggestions pointing at
    # /contact at exactly 0.70, which is the model saying it cannot tell rather
    # than saying yes, and counting those as yes is how a useful list turns into
    # a list nobody reads.
    ap.add_argument('--threshold', type=float, default=0.75)
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
        total = sum(len(candidates(pages, counts, s)) for s in sources)
        example = sources[0]
        cands = candidates(pages, counts, example)
        print('\nexample source %s' % example['rel'])
        print('  state: %d characters of its own text' % len(example['text']))
        print('  %d candidates, asked in batches of 20:' % len(cands))
        for n, rel, page in cands[:4]:
            anchor = anchor_in(example['text'], page)
            print('     %-40s %d inbound, anchor: %s'
                  % (rel, n, ('"%s"' % anchor) if anchor else 'none in copy'))
        print('\n%d source pages, %d judgements in the full matrix.'
              % (len(sources), total))
        with_anchor = sum(1 for src in sources
                          for _, _, tgt in candidates(pages, counts, src)
                          if anchor_in(src['text'], tgt))
        print('%d of those already have anchor text sitting in the source copy.'
              % with_anchor)
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

    # Questions over one state run in parallel, but a request carrying every
    # candidate at once is a large body and one failure loses the lot, so they
    # go in batches.
    BATCH = 20
    suggestions = []
    asked = 0
    try:
        with TypeSafeClient() as client:
            for source in sources:
                cands = candidates(pages, counts, source)
                for start in range(0, len(cands), BATCH):
                    chunk = cands[start:start + BATCH]
                    questions, keys = {}, {}
                    for i, (n, rel, page) in enumerate(chunk):
                        key = 'q%d' % i
                        keys[key] = (rel, page, n)
                        questions[key] = Noul(
                            instructions='Would a reader partway through this page '
                                         'have a genuine reason to follow a link to a '
                                         'separate page titled "%s", which covers: %s'
                                         % (page['title'], page['desc'][:200]),
                            criteria={
                                'true': 'This page raises a question, term or next '
                                        'step that the other page answers properly, '
                                        'so the link would help a reader rather than '
                                        'interrupt them.',
                                'false': 'The connection is only that both pages are '
                                         'about medical supplies. A link would be '
                                         'filler, or would repeat something this page '
                                         'already covers.',
                            })
                    result = client.system_one(
                        state={'page_title': source['title'],
                               'page_text': source['text'][:6000]},
                        questions=questions)
                    asked += len(questions)
                    for key, answer in result.nouls.items():
                        rel, page, n = keys[key]
                        if answer.noul >= args.threshold:
                            suggestions.append({
                                'from': source['rel'], 'to': rel,
                                'to_title': page['title'],
                                'confidence': round(answer.noul, 3),
                                'target_inbound_before': n,
                                'anchor': anchor_in(source['text'], page),
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

    ready = [s for s in kept if s['anchor']]
    needs_copy = [s for s in kept if not s['anchor']]

    print('\n== Links with anchor text already in the copy ==\n')
    for s in ready:
        print('%-38s -> %-38s %.2f' % (s['from'], s['to'], s['confidence']))
        print('%s wrap: "%s"' % (' ' * 38, s['anchor']))

    if needs_copy:
        print('\n== Judged useful, but nothing in the copy to wrap ==')
        print('   These need a sentence written rather than a word linked.\n')
        for s in needs_copy:
            print('%-38s -> %-38s %.2f' % (s['from'], s['to'], s['confidence']))

    out = ROOT / 'seo' / 'internal-links-suggested.json'
    out.write_text(json.dumps(kept, indent=1), encoding='utf-8')
    print('\n%d judgements asked, %d suggestions across %d pages, capped at %d each.'
          % (asked, len(kept), len(per_page), MAX_PER_PAGE))
    print('%d have anchor text already in the copy, %d need a sentence written.'
          % (len(ready), len(needs_copy)))
    print('Written to %s' % out.relative_to(ROOT))
    print('Nothing has been changed. These are for review, and the links belong in '
          'the generators in gen/, not in docs/.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
