"""Rank keyword opportunities, with the one judgement Ahrefs cannot make.

Ahrefs already labels intent, so asking a model to classify intent would be
paying twice for the same fact. What no SEO tool knows is the constraint this
business actually operates under: it supplies consumables and must never imply
it supplies a medicine. "bacteriostatic water" is squarely ours. "wegovy pen
needles" is a term where the searcher wants a drug and we sell the needle, and
whether a page can serve that without implying otherwise is a judgement.

So TypeSafe answers two questions per keyword and nothing else:

  safe_to_target   can we build a page for this without implying we supply a
                   medicine, a peptide or a hormone?
  serves_a_buyer   is the searcher trying to buy a physical consumable, as
                   opposed to researching a drug or hunting for a pharmacy?

The ranking arithmetic stays in code. A model that scores what a spreadsheet
can score is a model you cannot audit, and opportunity here is just volume,
difficulty and whether the page that would serve it is allowed to be indexed.

    python seo/triage.py --dry-run     # offline, free
    python seo/triage.py               # needs TYPESAFE_API_KEY
"""

import argparse
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / 'seo' / 'keywords-au.json'

# The shop is noindex until the catalogue is real, so a transactional term has
# nowhere to land today however easy it looks. Keeping that here rather than in
# a judgement means it changes the day INDEX_SHOP flips, by editing one line.
SHOP_IS_INDEXED = False


def opportunity(row):
    """Volume weighted against difficulty. Deliberately simple and arguable."""
    volume = row.get('volume') or 0
    difficulty = row.get('difficulty')
    if difficulty is None:
        difficulty = 50  # unknown difficulty is not free difficulty
    # Traffic potential matters more than the head term's own volume: it is what
    # the page ranking first actually receives across every term it holds.
    potential = row.get('traffic_potential') or 0
    reach = max(volume, potential * 0.5)
    return round(reach * (1 - difficulty / 100.0), 1)


def addressable(row):
    """Can anything on this site rank for it today?"""
    intents = set(row.get('intents') or [])
    if 'informational' in intents:
        return True, 'informational, a guide can serve it'
    if not SHOP_IS_INDEXED:
        return False, 'transactional only, and the shop is noindex'
    return True, 'commercial, a shop page can serve it'


def build_questions(Noul):
    return {
        'safe_to_target': Noul(
            instructions='Could an Australian retailer of medical consumables, such '
                         'as syringes, needles, swabs, sharps containers and sterile '
                         'diluent, publish a page targeting this search term without '
                         'implying it supplies a medicine, a peptide or a hormone?',
            criteria={
                'true': 'The term is about equipment, technique, disposal, or a '
                        'consumable the retailer genuinely sells, including sterile '
                        'water sold as a diluent. A page could answer it honestly '
                        'while selling only consumables.',
                'false': 'The term is about obtaining, dosing or using a prescription '
                         'medicine, peptide or hormone, so a page targeting it would '
                         'read as an offer to supply that drug or as advice about '
                         'taking it.',
            }),
        'serves_a_buyer': Noul(
            instructions='Is the person searching this term trying to obtain a '
                         'physical consumable product?',
            criteria={
                'true': 'The searcher wants to buy, find or choose a physical item '
                        'such as syringes, needles, gloves, swabs or a container.',
                'false': 'The searcher wants information, a definition, a technique, '
                         'a calculation, or is looking for a named pharmacy chain '
                         'rather than a product in its own right.',
            }),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--dry-run', action='store_true', help='offline, no key, no cost')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--threshold', type=float, default=0.7,
                    help='probability at or above which safe_to_target counts as yes')
    args = ap.parse_args()

    data = json.loads(DATA.read_text(encoding='utf-8'))
    rows = data['keywords']
    if args.limit:
        rows = rows[:args.limit]

    for row in rows:
        row['opportunity'] = opportunity(row)
        row['addressable'], row['why'] = addressable(row)

    if args.dry_run:
        ranked = sorted(rows, key=lambda r: -r['opportunity'])
        print('%d keywords, %d total monthly volume\n'
              % (len(rows), sum(r.get('volume') or 0 for r in rows)))
        print('Ranked before any judgement. TypeSafe would then be asked, per row,')
        print('whether it is safe to target and whether it serves a buyer.\n')
        print('%-48s %7s %5s %6s  %s' % ('keyword', 'opp', 'vol', 'kd', 'addressable'))
        for r in ranked[:20]:
            print('%-48s %7.1f %5s %6s  %s'
                  % (r['keyword'][:48], r['opportunity'], r.get('volume'),
                     r.get('difficulty'), 'yes' if r['addressable'] else 'no'))
        blocked = [r for r in rows if not r['addressable']]
        print('\n%d of %d cannot be served today: %s'
              % (len(blocked), len(rows), blocked[0]['why'] if blocked else '-'))
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
                state = {'search_term': row['keyword'],
                         'intents_reported_by_ahrefs': row.get('intents')}
                result = client.system_one(state=state, questions=questions)
                row['safe_to_target'] = round(result.nouls['safe_to_target'].noul, 3)
                row['serves_a_buyer'] = round(result.nouls['serves_a_buyer'].noul, 3)
    except TypeSafeAPIConnectionError as exc:
        print('Could not reach the TypeSafe API: %s' % exc, file=sys.stderr)
        return 3
    except TypeSafeError as exc:
        print('TypeSafe rejected the request: %s' % exc, file=sys.stderr)
        return 1

    go = [r for r in rows if r['safe_to_target'] >= args.threshold and r['addressable']]
    unsafe = [r for r in rows if r['safe_to_target'] < args.threshold]
    go.sort(key=lambda r: -r['opportunity'])

    print('\n== Worth writing for, ranked ==\n')
    print('%-46s %7s %5s %5s %6s' % ('keyword', 'opp', 'vol', 'kd', 'safe'))
    for r in go[:25]:
        print('%-46s %7.1f %5s %5s %6.2f'
              % (r['keyword'][:46], r['opportunity'], r.get('volume'),
                 r.get('difficulty'), r['safe_to_target']))

    if unsafe:
        print('\n== Judged unsafe to target, lowest first ==\n')
        for r in sorted(unsafe, key=lambda r: r['safe_to_target'])[:12]:
            print('  %-46s %.2f' % (r['keyword'][:46], r['safe_to_target']))

    out = ROOT / 'seo' / 'triage-result.json'
    out.write_text(json.dumps(rows, indent=1), encoding='utf-8')
    print('\n%d of %d worth pursuing. Full result written to %s'
          % (len(go), len(rows), out.relative_to(ROOT)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
