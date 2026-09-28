"""Which rival terms are worth taking, and which are theirs to keep.

Competitor research usually produces a list of everything the other side ranks
for, which is a list of things to feel bad about rather than a plan. The useful
question is narrower: of the terms a rival holds, which ones could a page of
ours actually be the better answer to, and which are somebody else's by right.

Three kinds of rival came out of the first sweep and they need different
treatment, so lane is a field in competitors.json rather than a judgement:

  retailer     Sells what we sell. Contest term by term. medshop.com.au holds
               insulin needles at 11,000 a month on difficulty 3, from one
               collection page. That is not a moat, it is a page.
  authority    A state health department or a peak body. diabetesaustralia
               takes 1,678 visits a month from one sharps resource at domain
               rating 77. A commercial page will not outrank it on disposal
               advice and should not try. Link to it and take the product term
               sitting next to it instead.
  marketplace  Amazon and eBay. Beatable on specificity and on being local.
  adjacent     Ranks in our SERPs selling something we do not sell. The most
               instructive row in the file is a peptide retailer at domain
               rating 0 sitting second for bacteriostatic water, which proves a
               new domain can win here and simultaneously marks the one lane
               this business will not enter.

Ranking stays in code. What the model is asked is the pair of judgements a
spreadsheet cannot make: whether our page would genuinely be the better answer,
and whether the term is really somebody's brand being searched for, in which
case ranking for it buys a visitor who wanted a different shop.

    python seo/competitors.py --dry-run     # offline, free
    python seo/competitors.py               # needs TYPESAFE_API_KEY
"""

import argparse
import json
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
RIVALS = ROOT / 'seo' / 'competitors.json'
KEYWORDS = ROOT / 'seo' / 'keywords-au.json'
OUT = ROOT / 'seo' / 'competitor-gaps.json'

# How much of a term's value survives the lane it sits in. Not a measure of the
# rival's quality: a state health department is a better page than anything we
# will write, which is exactly why its head term scores near zero here.
LANE_FACTOR = {
    'retailer': 1.0,
    'marketplace': 0.8,
    'adjacent': 0.6,
    'authority': 0.15,
}

# Where the rival sits tells us something about the page, not about our odds,
# so this is deliberately shallow. Position one on a difficulty 0 term means a
# page nobody has bothered to contest, which is an opportunity rather than a
# wall.
def headroom(position):
    if position is None:
        return 0.7
    if position <= 3:
        return 0.85
    if position <= 6:
        return 1.0
    return 1.1


def load_rivals():
    data = json.loads(RIVALS.read_text(encoding='utf-8'))
    return data, {c['domain']: c for c in data['competitors']}


def load_keywords():
    data = json.loads(KEYWORDS.read_text(encoding='utf-8'))
    return {k['keyword'].lower(): k for k in data['keywords']}


def our_pages():
    """The pages allowed to rank, with their text. Reused from the link mapper."""
    sys.path.insert(0, str(ROOT / 'seo'))
    import internal_links
    return internal_links.load()


# Words that carry no product meaning, so a term matching the catalogue on one
# of these has not matched the catalogue.
NOISE = {'the', 'a', 'an', 'and', 'or', 'of', 'for', 'to', 'in', 'on', 'at',
         'is', 'it', 'what', 'how', 'why', 'near', 'me', 'best', 'buy', 'cheap',
         'australia', 'au', 'online', 'free', 'chart', 'size', 'sizes',
         'medical', 'supplies', 'supply', 'shop', 'store', 'kit', 'pack'}


def catalogue_words():
    """Every meaningful word in our category and product names.

    A term naming a product we do not stock is not a gap, it is a different
    business. stethoscope and fob watch both score well on volume and difficulty
    and neither belongs to us, and deciding that is lookup work rather than a
    judgement worth paying a model for.
    """
    sys.path.insert(0, str(ROOT / 'gen'))
    from catalogue import CATEGORIES
    words = set()
    for cat in CATEGORIES:
        names = [cat['name']] + [p['name'] for p in cat['products']]
        for name in names:
            for word in re.split(r'[^a-z0-9]+', name.lower()):
                if len(word) > 2 and word not in NOISE:
                    words.add(word)
                    if word.endswith('s'):
                        words.add(word[:-1])
    return words


def in_our_catalogue(term, words):
    """True when every meaningful word of the term names something we stock."""
    parts = [w for w in re.split(r'[^a-z0-9]+', term.lower())
             if len(w) > 2 and w not in NOISE]
    if not parts:
        return False
    return all(w in words or w.rstrip('s') in words for w in parts)


def covered_by(term, pages):
    """Which of our pages already say this term, longest match first.

    A term our own copy never uses is a term we have no page for, whatever the
    catalogue says. This is string work and stays string work: a model asked
    whether a page mentions a phrase will sometimes say yes about a phrase that
    is not there.
    """
    needle = term.lower()
    hits = []
    for rel, page in pages.items():
        haystack = (page['title'] + ' ' + page['desc'] + ' ' + page['text']).lower()
        if needle in haystack:
            hits.append((haystack.count(needle), rel))
    hits.sort(key=lambda h: -h[0])
    return [rel for _, rel in hits]


def gaps(data, keywords, pages):
    """Every term a rival holds, scored, with what we have for it today."""
    rows = []
    seen = {}
    stocked = catalogue_words()
    for rival in data['competitors']:
        lane = rival['lane']
        for hold in rival['holds']:
            term = hold['keyword']
            known = keywords.get(term.lower(), {})
            volume = hold.get('volume') or known.get('volume') or 0
            kd = hold.get('difficulty')
            if kd is None:
                kd = known.get('difficulty')
            if kd is None:
                kd = 50  # unknown difficulty is not free difficulty
            ours = covered_by(term, pages)
            score = round(volume * (1 - kd / 100.0)
                          * LANE_FACTOR.get(lane, 0.6)
                          * headroom(hold.get('position')), 1)
            row = {
                'keyword': term,
                'volume': volume,
                'difficulty': kd,
                'held_by': rival['domain'],
                'lane': lane,
                'their_position': hold.get('position'),
                'their_url': hold.get('url'),
                'their_traffic': hold.get('traffic'),
                'our_pages': ours,
                'we_have_a_page': bool(ours),
                'contest_score': score,
                'in_keyword_file': term.lower() in keywords,
                'in_our_catalogue': in_our_catalogue(term, stocked),
            }
            # A term for something we do not sell, and have written nothing about,
            # is not a gap. It stays in the file, scored, so the reason it was
            # passed over is on the record rather than lost. A term outside the
            # catalogue that we do already have a page for keeps its score: the
            # gauge chart is not a product and the page is still ours to rank.
            if not row['in_our_catalogue'] and not ours:
                row['contest_score'] = round(score * 0.05, 1)
            # One rival per term, the one worth taking it from: the highest
            # scoring lane. Two rows for sharps container held by a health
            # charity and by a waste company is one decision, not two.
            prior = seen.get(term.lower())
            if prior is None or score > prior['contest_score']:
                seen[term.lower()] = row
                rows.append(row)
                if prior is not None:
                    rows.remove(prior)
    rows.sort(key=lambda r: -r['contest_score'])
    return rows


def build_questions(Noul):
    return {
        'we_can_answer_better': Noul(
            instructions='An Australian retailer of medical consumables is considering '
                         'writing a page to compete for this search term. The page that '
                         'currently ranks is described below. Would a page from a '
                         'consumables supplier, written to explain the equipment plainly '
                         'and to show what is in stock, be a genuinely better answer for '
                         'this searcher than what ranks now?',
            criteria={
                'true': 'The searcher wants to understand or obtain a physical '
                        'consumable and the ranking page is a thin product listing, a '
                        'marketplace result, an overseas page, or a page about something '
                        'adjacent. A supplier who explains the item properly would serve '
                        'them better.',
                'false': 'The ranking page is already the right answer and better placed '
                         'to give it, such as a government or health service page on '
                         'disposal or safety, or the searcher wants something a '
                         'consumables supplier does not have.',
            }),
        'brand_term_is_theirs': Noul(
            instructions='Is this search term a person looking for one specific named '
                         'shop, chain or brand, rather than looking for the product '
                         'itself?',
            criteria={
                'true': 'The term names a retailer, chain or manufacturer and the person '
                        'wants that one. A different shop appearing in the results is not '
                        'the answer they asked for.',
                'false': 'The term is about the product, the category or the task. Any '
                         'supplier with the right page can answer it. A brand name used '
                         'generically for the product, the way people say a brand when '
                         'they mean the item, counts as false.',
            }),
    }


def report(rows, judged=False):
    print('%-38s %8s %6s %5s %-24s %s'
          % ('term', 'contest', 'vol', 'kd', 'held by', 'ours today'))
    for r in rows:
        ours = r['our_pages'][0] if r['our_pages'] else '-'
        print('%-38s %8.1f %6s %5s %-24s %s'
              % (r['keyword'][:38], r['contest_score'], r['volume'],
                 r['difficulty'], r['held_by'][:24], ours))
        if judged:
            print('%-38s          better %.2f  theirs %.2f'
                  % ('', r.get('we_can_answer_better', 0), r.get('brand_term_is_theirs', 0)))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--dry-run', action='store_true', help='offline, no key, no cost')
    ap.add_argument('--threshold', type=float, default=0.75)
    args = ap.parse_args()

    data, _ = load_rivals()
    keywords = load_keywords()
    pages = our_pages()
    rows = gaps(data, keywords, pages)

    missing = [r for r in rows if not r['we_have_a_page']]
    unlisted = [r for r in rows if not r['in_keyword_file']]

    print('%d rivals, %d contested terms, pulled %s\n'
          % (len(data['competitors']), len(rows), data['pulled']))
    report(rows)
    offrange = [r for r in rows if not r['in_our_catalogue'] and not r['our_pages']]
    print('\n%d of %d have no page of ours saying the term at all.' % (len(missing), len(rows)))
    if offrange:
        print('%d name something outside the range, so they are scored down to near '
              'nothing rather than dropped: %s'
              % (len(offrange), ', '.join(r['keyword'] for r in offrange)))
    if unlisted:
        print('%d are not in keywords-au.json yet: %s'
              % (len(unlisted), ', '.join(r['keyword'] for r in unlisted[:6])))

    if args.dry_run:
        print('\nTypeSafe would then be asked, per term, whether our page would be the '
              'better answer and whether the term belongs to a brand.')
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

    questions = build_questions(Noul)
    try:
        with TypeSafeClient() as client:
            for row in rows:
                state = {
                    'search_term': row['keyword'],
                    'monthly_searches_in_australia': row['volume'],
                    'ranking_page_url': row['their_url'],
                    'ranking_page_owner': row['held_by'],
                    'ranking_page_kind': row['lane'],
                    'ranking_position': row['their_position'],
                }
                result = client.system_one(state=state, questions=questions)
                row['we_can_answer_better'] = round(result.nouls['we_can_answer_better'].noul, 3)
                row['brand_term_is_theirs'] = round(result.nouls['brand_term_is_theirs'].noul, 3)
    except TypeSafeAPIConnectionError as exc:
        print('Could not reach the TypeSafe API: %s' % exc, file=sys.stderr)
        return 3
    except TypeSafeError as exc:
        print('TypeSafe rejected the request: %s' % exc, file=sys.stderr)
        return 1

    take = [r for r in rows
            if r['we_can_answer_better'] >= args.threshold
            and r['brand_term_is_theirs'] < args.threshold]
    leave = [r for r in rows if r not in take]
    for r in rows:
        r['worth_contesting'] = r in take

    print('\n== Worth taking ==\n')
    report(take, judged=True)
    if leave:
        print('\n== Leave alone ==\n')
        for r in leave:
            reason = ('the term belongs to a brand' if r['brand_term_is_theirs'] >= args.threshold
                      else 'what ranks is already the better answer')
            print('  %-38s %s' % (r['keyword'][:38], reason))

    OUT.write_text(json.dumps({'pulled': data['pulled'], 'threshold': args.threshold,
                               'gaps': rows}, indent=1) + '\n', encoding='utf-8')
    print('\n%d of %d worth contesting. Written to %s'
          % (len(take), len(rows), OUT.relative_to(ROOT)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
