"""Pull today's numbers from Ahrefs, so the loop is not ranking last month's market.

Search volume moves, and it moves enough to change decisions. Between the first
pull on 22 September and the next one six days later, bacteriostatic water went
from 5,700 monthly searches to 7,100 and insulin needles turned up at 8,600 on
difficulty 3, which was the largest single opportunity on the site and was not in
the file at all. A keyword file that is refreshed by hand is a keyword file that
is six weeks stale the moment anybody stops thinking about it.

Three things it can do, and the daily run does the first two:

  --keywords   Re-read volume, difficulty, cost per click, traffic potential and
               intent for every term already tracked, and report what moved.
  --discover   Ask for new matching terms around the seeds and add any that clear
               the volume and difficulty floors. New terms arrive unjudged, which
               holds them out of the publishing queue until triage runs.
  --serps      Re-read who holds the top of the page for the terms that matter,
               and update the positions in competitors.json. Expensive, so weekly
               rather than daily.

Everything is written back into the committed JSON, so a run is a diff somebody
can read, and a bad refresh is one revert away.

    python seo/refresh.py --keywords --discover     # needs AHREFS_API_KEY
    python seo/refresh.py --plan                    # offline, prints the calls

Credentials come from AHREFS_API_KEY, out of the environment or .env.local. The
key is never printed, logged or written anywhere by this script.
"""

import argparse
import datetime
import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
KEYWORDS = ROOT / 'seo' / 'keywords-au.json'
RIVALS = ROOT / 'seo' / 'competitors.json'

BASE = 'https://api.ahrefs.com/v3'

# The two paths the daily run uses are confirmed against the published reference.
# The SERP one follows the same base-plus-report shape but the reference states
# the base and the path separately, so a wrong guess is possible: the request
# helper prints the status and the response body on any non-200, which means the
# first run says exactly what is wrong rather than failing quietly.
PATHS = {
    'overview': '/keywords-explorer/overview',
    'matching': '/keywords-explorer/matching-terms',
    'serp': '/serp-overview/serp-overview',
}

COUNTRY = 'au'

# Keywords per request. The endpoint takes a comma separated list; a term
# containing a comma would split in two, so that is checked rather than hoped.
BATCH = 50

# Floors for anything --discover adds. Below these a term is a rounding error
# that still costs a safety judgement to clear.
MIN_VOLUME = 100
MAX_DIFFICULTY = 35

FIELDS = 'keyword,volume,difficulty,cpc,traffic_potential,intents'

# What counts as a move worth printing. Ahrefs rounds volume hard at the low end,
# so a 150 to 200 step is noise and a doubling is not.
MOVED = 0.2


def key_or_die():
    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / '.env.local')
    except ImportError:
        pass
    key = os.getenv('AHREFS_API_KEY')
    if not key:
        print('AHREFS_API_KEY is not set.', file=sys.stderr)
        raise SystemExit(2)
    return key


def get(path, params, key):
    url = '%s%s?%s' % (BASE, path, urllib.parse.urlencode(params))
    req = urllib.request.Request(url, headers={
        'Authorization': 'Bearer %s' % key,
        'Accept': 'application/json',
    })
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode('utf-8', 'replace')[:800]
        # The URL is printed without the key, which lives in a header.
        print('Ahrefs returned %s for %s\n%s' % (exc.code, path, body), file=sys.stderr)
        raise
    except urllib.error.URLError as exc:
        print('Could not reach the Ahrefs API: %s' % exc, file=sys.stderr)
        raise


def intents_list(value):
    """Ahrefs returns intents as an object here and a list elsewhere. Normalise."""
    if isinstance(value, dict):
        return sorted(k for k, v in value.items() if v)
    if isinstance(value, list):
        return sorted(value)
    return []


def chunks(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]


def refresh_keywords(data, key, plan=False):
    terms = [row['keyword'] for row in data['keywords']]
    bad = [t for t in terms if ',' in t]
    if bad:
        raise ValueError('these terms contain a comma and cannot be batched: %s' % bad)

    calls = list(chunks(terms, BATCH))
    if plan:
        print('%d calls to %s, %d terms' % (len(calls), PATHS['overview'], len(terms)))
        return []

    fresh = {}
    for batch in calls:
        resp = get(PATHS['overview'],
                   {'country': COUNTRY, 'select': FIELDS, 'keywords': ','.join(batch)},
                   key)
        for row in resp.get('keywords', []):
            if row.get('keyword'):
                fresh[row['keyword'].lower()] = row

    moves = []
    for row in data['keywords']:
        new = fresh.get(row['keyword'].lower())
        if not new:
            continue
        before = row.get('volume') or 0
        after = new.get('volume') or 0
        if before and after and abs(after - before) / before >= MOVED:
            moves.append((row['keyword'], before, after))
        elif not before and after:
            moves.append((row['keyword'], before, after))
        row['volume'] = after
        row['difficulty'] = new.get('difficulty')
        row['cpc'] = new.get('cpc')
        row['traffic_potential'] = new.get('traffic_potential')
        intents = intents_list(new.get('intents'))
        if intents:
            row['intents'] = intents

    missing = [r['keyword'] for r in data['keywords'] if r['keyword'].lower() not in fresh]
    if missing:
        print('%d term%s came back with no data and kept its old numbers: %s'
              % (len(missing), '' if len(missing) == 1 else 's', ', '.join(missing[:6])))
    return moves


def discover(data, key, plan=False):
    seeds = data['seeds']
    if plan:
        print('1 call to %s, %d seeds' % (PATHS['matching'], len(seeds)))
        return []

    where = json.dumps({'and': [
        {'field': 'volume', 'is': ['gte', MIN_VOLUME]},
        {'field': 'difficulty', 'is': ['lte', MAX_DIFFICULTY]},
    ]})
    resp = get(PATHS['matching'], {
        'country': COUNTRY, 'select': FIELDS, 'keywords': ', '.join(seeds),
        'match_mode': 'terms', 'where': where, 'order_by': 'volume:desc',
        'limit': 100,
    }, key)

    have = {r['keyword'].lower() for r in data['keywords']}
    added = []
    for row in resp.get('keywords', []):
        term = (row.get('keyword') or '').strip()
        if not term or term.lower() in have or ',' in term:
            continue
        data['keywords'].append({
            'keyword': term,
            'volume': row.get('volume'),
            'difficulty': row.get('difficulty'),
            'cpc': row.get('cpc'),
            'traffic_potential': row.get('traffic_potential'),
            'intents': intents_list(row.get('intents')),
        })
        have.add(term.lower())
        added.append(term)
    return added


def refresh_serps(rivals, data, key, top, plan=False):
    """Who holds the top of the page, for the terms worth the most."""
    ranked = sorted(data['keywords'], key=lambda r: -(r.get('volume') or 0))[:top]
    terms = [r['keyword'] for r in ranked]
    if plan:
        print('%d calls to %s, one per term' % (len(terms), PATHS['serp']))
        return []

    by_domain = {c['domain']: c for c in rivals['competitors']}
    changes = []
    for term in terms:
        try:
            resp = get(PATHS['serp'], {
                'country': COUNTRY, 'keyword': term, 'top_positions': 10, 'type': 'organic',
                'select': 'position,url,domain_rating,traffic,title',
            }, key)
        except (urllib.error.HTTPError, urllib.error.URLError):
            print('  skipped %s' % term)
            continue
        for pos in resp.get('positions', []):
            url = pos.get('url') or ''
            host = urllib.parse.urlparse(url).netloc.replace('www.', '')
            rival = by_domain.get(host)
            if not rival:
                continue
            existing = next((h for h in rival['holds'] if h['keyword'] == term), None)
            if existing is None:
                rival['holds'].append({'keyword': term, 'position': pos.get('position'),
                                       'url': url, 'traffic': pos.get('traffic')})
                changes.append('%s took %s at %s' % (host, term, pos.get('position')))
            elif existing.get('position') != pos.get('position'):
                changes.append('%s moved on %s, %s to %s'
                               % (host, term, existing.get('position'), pos.get('position')))
                existing['position'] = pos.get('position')
                existing['url'] = url
                existing['traffic'] = pos.get('traffic')
            if pos.get('domain_rating') is not None:
                rival['domain_rating'] = pos['domain_rating']
    return changes


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--keywords', action='store_true', help='refresh the tracked terms')
    ap.add_argument('--discover', action='store_true', help='look for new terms')
    ap.add_argument('--serps', action='store_true', help='refresh who holds the top')
    ap.add_argument('--serp-top', type=int, default=12,
                    help='how many terms to re-check the SERP for')
    ap.add_argument('--plan', action='store_true',
                    help='print the calls that would be made and stop. Free.')
    args = ap.parse_args()

    if not (args.keywords or args.discover or args.serps):
        args.keywords = args.discover = True

    data = json.loads(KEYWORDS.read_text(encoding='utf-8'))
    rivals = json.loads(RIVALS.read_text(encoding='utf-8'))
    today = datetime.date.today().isoformat()
    key = None if args.plan else key_or_die()

    moves, added, changes = [], [], []
    if args.keywords:
        moves = refresh_keywords(data, key, args.plan)
    if args.discover:
        added = discover(data, key, args.plan)
    if args.serps:
        changes = refresh_serps(rivals, data, key, args.serp_top, args.plan)

    if args.plan:
        print('\nNothing was called and nothing was written.')
        return 0

    if moves:
        print('\n== Volume moved ==\n')
        for term, before, after in sorted(moves, key=lambda m: -abs(m[2] - m[1]))[:20]:
            print('  %-44s %6s to %-6s %+d' % (term[:44], before, after, after - before))
    else:
        print('\nNo tracked term moved by %d per cent or more.' % int(MOVED * 100))

    if added:
        print('\n== New terms, %d of them ==\n' % len(added))
        for term in added[:20]:
            print('  %s' % term)
        print('\nThese arrive unjudged, which keeps them out of the publishing queue '
              'until seo/triage.py has cleared them.')

    if changes:
        print('\n== The competition moved ==\n')
        for line in changes[:25]:
            print('  %s' % line)

    data['keywords'].sort(key=lambda r: -(r.get('volume') or 0))
    data['pulled'] = today
    KEYWORDS.write_text(json.dumps(data, indent=1) + '\n', encoding='utf-8')
    if args.serps:
        rivals['pulled'] = today
        RIVALS.write_text(json.dumps(rivals, indent=1) + '\n', encoding='utf-8')

    total = sum(r.get('volume') or 0 for r in data['keywords'])
    print('\n%d keywords tracked, %d total monthly volume. Written to %s'
          % (len(data['keywords']), total, KEYWORDS.relative_to(ROOT)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
