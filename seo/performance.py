"""What actually happened, and what it should change about tomorrow.

Without this file the rest of the loop is a content schedule with a keyword tool
attached: it would publish the same ranked list of guesses forever and never find
out whether any of them worked. This is the part that reads the scoreboard.

Three things come out of a Search Console pull that a keyword tool cannot tell
you, because they are about this site rather than about the market.

  Striking distance   A query where a page already sits between 4 and 20.
                      Google has decided the page is a reasonable answer. The
                      cheapest traffic on the site is here, and it needs an
                      edit rather than a new page.

  A near-miss cluster A page picking up many related queries, all of them deep.
                      The first real pull showed reading-a-syringe surfacing for
                      sixteen distinct queries about where a given millilitre
                      mark sits on a 1mL barrel, every one between position 73
                      and 89. That is not sixteen failures, it is Google saying
                      the page is on the right subject and does not answer the
                      specific question. Expand the page, do not write a new one.

  Silence             A page live long enough to be crawled, with no impressions
                      at all. Google is not considering it. That is a signal
                      about the whole shape of the page and it should cost its
                      topic weight something.

The weights are how the loop learns. Every opportunity score in
opportunities.py is multiplied by the weight of the intent it serves, and those
weights move a little each run on measured evidence, inside bounds, with the
reason written down. Bounded and logged because an unbounded feedback loop
finds one lucky day and spends a month on it.

    python seo/performance.py --from-file seo/gsc-snapshot.json   # offline, free
    python seo/performance.py                                     # needs credentials

Credentials, for a run that pulls live:
    GSC_SERVICE_ACCOUNT_JSON   the whole service account key, as one string.
                               Add the service account's email as a user on the
                               property in Search Console first, with Full or
                               Restricted access. The value is never printed.
    GSC_PROPERTY               defaults to sc-domain:goodpracticesupply.com.au
"""

import argparse
import collections
import datetime
import json
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
HISTORY = ROOT / 'seo' / 'performance.json'
WEIGHTS = ROOT / 'seo' / 'weights.json'
SNAPSHOT = ROOT / 'seo' / 'gsc-snapshot.json'

PROPERTY = os.getenv('GSC_PROPERTY', 'sc-domain:goodpracticesupply.com.au')
SCOPE = 'https://www.googleapis.com/auth/webmasters.readonly'

# A query at 4 to 20 is worth an edit today. Below 3 it is already won. Past 20
# it is a topic signal rather than a near win.
STRIKING = (4, 20)

# A page needs this many deep queries before a shared theme counts as a cluster
# rather than as noise. Three queries about the same thing is a coincidence.
CLUSTER_MIN = 4

# How far a weight can travel in one run, and the range it can ever occupy. Small
# because the input is small: sixty impressions is not evidence of much, and the
# loop should take weeks to change its mind, not one morning.
STEP = 0.05
FLOOR, CEILING = 0.5, 2.0

INTENTS = ('informational', 'commercial', 'transactional', 'local')

# Words that carry no subject, so a theme resting on one of these is not a theme.
DULL = {'a', 'an', 'the', 'and', 'or', 'of', 'for', 'to', 'in', 'on', 'at', 'is',
        'it', 'how', 'what', 'where', 'why', 'which', 'when', 'who', 'do', 'does',
        'my', 'your', 'you', 'i', 'me', 'much', 'many', 'look', 'like', 'much',
        'read', 'reading', 'near', 'be', 'with', 'from', 'can', 'should'}


def path_of(url):
    path = re.sub(r'^https?://[^/]+', '', url).split('?')[0].split('#')[0]
    return (path.rstrip('/') or '/')


def fetch_live():
    """Search Console, last 28 complete days, by query and page."""
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    raw = os.getenv('GSC_SERVICE_ACCOUNT_JSON')
    if not raw:
        raise RuntimeError('GSC_SERVICE_ACCOUNT_JSON is not set')
    info = json.loads(raw)
    creds = service_account.Credentials.from_service_account_info(info, scopes=[SCOPE])
    api = build('searchconsole', 'v1', credentials=creds, cache_discovery=False)

    # Search Console finalises data two to three days late, so the window ends
    # three days ago. Asking for yesterday returns a number that changes.
    end = datetime.date.today() - datetime.timedelta(days=3)
    start = end - datetime.timedelta(days=27)
    rows, start_row = [], 0
    while True:
        body = {'startDate': start.isoformat(), 'endDate': end.isoformat(),
                'dimensions': ['query', 'page'], 'rowLimit': 25000,
                'startRow': start_row, 'dataState': 'all'}
        resp = api.searchanalytics().query(siteUrl=PROPERTY, body=body).execute()
        got = resp.get('rows', [])
        rows.extend(got)
        if len(got) < 25000:
            break
        start_row += len(got)
    return {'property': PROPERTY, 'start': start.isoformat(), 'end': end.isoformat(),
            'rows': rows}


def load_snapshot(path):
    data = json.loads(pathlib.Path(path).read_text(encoding='utf-8'))
    if isinstance(data, list):           # a bare rows array is accepted too
        return {'property': PROPERTY, 'start': None, 'end': None, 'rows': data}
    return data


def tidy(snapshot):
    """Search Console rows into flat records, dropping anything unusable."""
    out = []
    for row in snapshot.get('rows', []):
        keys = row.get('keys') or []
        if len(keys) < 2:
            continue
        out.append({
            'query': keys[0],
            'path': path_of(keys[1]),
            'clicks': row.get('clicks') or 0,
            'impressions': row.get('impressions') or 0,
            'position': round(row.get('position') or 0, 1),
        })
    return out


def themes(queries):
    """The words a group of queries keeps returning to, most common first."""
    counter = collections.Counter()
    for q in queries:
        for word in re.split(r'[^a-z0-9.]+', q.lower()):
            if len(word) > 1 and word not in DULL and not word.isdigit():
                counter[word] += 1
    return [w for w, n in counter.most_common(6) if n >= 2]


def analyse(records):
    """Per page: what it earns, and the one thing to do about it."""
    by_page = collections.defaultdict(list)
    for r in records:
        by_page[r['path']].append(r)

    pages = {}
    for path, rows in sorted(by_page.items()):
        impressions = sum(r['impressions'] for r in rows)
        clicks = sum(r['clicks'] for r in rows)
        striking = sorted((r for r in rows if STRIKING[0] <= r['position'] <= STRIKING[1]),
                          key=lambda r: r['position'])
        deep = [r for r in rows if r['position'] > STRIKING[1]]
        best = min((r['position'] for r in rows), default=None)

        cluster = None
        if len(deep) >= CLUSTER_MIN:
            words = themes([r['query'] for r in deep])
            if words:
                cluster = {'words': words,
                           'queries': [r['query'] for r in
                                       sorted(deep, key=lambda r: r['position'])[:10]],
                           'count': len(deep),
                           'median_position': sorted(r['position'] for r in deep)[len(deep) // 2]}

        if striking:
            action = 'optimise'
            because = ('%d quer%s already between %d and %d, best at %.0f'
                       % (len(striking), 'y' if len(striking) == 1 else 'ies',
                          STRIKING[0], STRIKING[1], striking[0]['position']))
        elif cluster:
            action = 'expand'
            because = ('%d deep queries circling %s, median position %.0f'
                       % (cluster['count'], ', '.join(cluster['words'][:3]),
                          cluster['median_position']))
        elif impressions:
            action = 'watch'
            because = '%d impressions, nothing within reach yet' % impressions
        else:
            action = 'silent'
            because = 'no impressions at all'

        pages[path] = {
            'impressions': impressions, 'clicks': clicks, 'queries': len(rows),
            'best_position': best, 'striking': [r['query'] for r in striking[:10]],
            'cluster': cluster, 'action': action, 'because': because,
        }
    return pages


def blank_weights():
    return {'updated': None, 'runs': 0,
            'intent': {k: 1.0 for k in INTENTS},
            'pages': {}, 'log': []}


def load_weights():
    if WEIGHTS.exists():
        data = json.loads(WEIGHTS.read_text(encoding='utf-8'))
        for k in INTENTS:
            data.setdefault('intent', {}).setdefault(k, 1.0)
        return data
    return blank_weights()


def clamp(v):
    return round(max(FLOOR, min(CEILING, v)), 3)


def learn(weights, pages, keywords, today):
    """Move the intent weights on measured evidence, and say why in the log.

    The mapping from a page to an intent runs through the keyword file: a query
    the site earned impressions for, that appears in keywords-au.json, carries
    the intents Ahrefs assigned it. So the weights are not a guess about what
    kind of page works, they are a count of which kinds of search this site is
    actually being shown for.
    """
    earned = collections.Counter()
    for path, page in pages.items():
        for q in page['striking']:
            row = keywords.get(q.lower())
            if row:
                for intent in row.get('intents') or []:
                    if intent in INTENTS:
                        earned[intent] += 3        # a near win counts triple
        if page['cluster']:
            for q in page['cluster']['queries']:
                row = keywords.get(q.lower())
                if row:
                    for intent in row.get('intents') or []:
                        if intent in INTENTS:
                            earned[intent] += 1

    notes = []
    total = sum(earned.values())
    if total:
        share = {k: earned[k] / total for k in INTENTS}
        best = max(share, key=share.get)
        for intent in INTENTS:
            before = weights['intent'][intent]
            # Above its equal share, the intent is pulling its weight. Below, it
            # is not. One step either way, never more.
            direction = 1 if share[intent] > 1.0 / len(INTENTS) else -1
            if earned[intent] == 0:
                direction = -1
            after = clamp(before + direction * STEP)
            weights['intent'][intent] = after
            if after != before:
                notes.append('%s %s %.2f to %.2f (%d of %d signals)'
                             % (intent, 'up' if after > before else 'down',
                                before, after, earned[intent], total))
        notes.append('strongest intent this run: %s' % best)
    else:
        notes.append('no measured query matched the keyword file, so no weight moved')

    silent = sorted(p for p, v in pages.items() if v['action'] == 'silent')
    if silent:
        notes.append('%d page%s with no impressions: %s'
                     % (len(silent), '' if len(silent) == 1 else 's',
                        ', '.join(silent[:5])))

    for path, page in pages.items():
        weights['pages'][path] = {
            'impressions': page['impressions'], 'clicks': page['clicks'],
            'queries': page['queries'], 'best_position': page['best_position'],
            'action': page['action'],
        }

    weights['runs'] += 1
    weights['updated'] = today
    weights['log'] = ([{'date': today, 'notes': notes}] + weights.get('log', []))[:60]
    return notes


def keyword_index():
    data = json.loads((ROOT / 'seo' / 'keywords-au.json').read_text(encoding='utf-8'))
    return {k['keyword'].lower(): k for k in data['keywords']}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--from-file', default='',
                    help='read Search Console rows from a committed snapshot '
                         'instead of calling the API. Offline and free.')
    ap.add_argument('--dry-run', action='store_true',
                    help='analyse and print, write nothing')
    args = ap.parse_args()

    if args.from_file:
        snapshot = load_snapshot(args.from_file)
    elif SNAPSHOT.exists() and not os.getenv('GSC_SERVICE_ACCOUNT_JSON'):
        print('No credentials set, falling back to the committed snapshot at %s.'
              % SNAPSHOT.relative_to(ROOT))
        snapshot = load_snapshot(SNAPSHOT)
    else:
        try:
            from dotenv import load_dotenv
            load_dotenv(ROOT / '.env.local')
        except ImportError:
            pass
        try:
            snapshot = fetch_live()
        except ImportError as exc:
            print('The Google API client is not installed: %s' % exc, file=sys.stderr)
            return 4
        except Exception as exc:                      # noqa: BLE001
            print('Could not read Search Console: %s' % exc, file=sys.stderr)
            return 3

    records = tidy(snapshot)
    pages = analyse(records)
    keywords = keyword_index()
    today = datetime.date.today().isoformat()

    impressions = sum(r['impressions'] for r in records)
    clicks = sum(r['clicks'] for r in records)
    print('%s, %s to %s: %d quer%s, %d impressions, %d click%s across %d pages\n'
          % (snapshot.get('property', PROPERTY), snapshot.get('start') or '?',
             snapshot.get('end') or '?', len(records),
             'y' if len(records) == 1 else 'ies', impressions,
             clicks, '' if clicks == 1 else 's', len(pages)))

    order = {'optimise': 0, 'expand': 1, 'watch': 2, 'silent': 3}
    print('%-40s %-9s %5s %4s %6s  %s'
          % ('page', 'action', 'impr', 'q', 'best', 'why'))
    for path, page in sorted(pages.items(),
                             key=lambda kv: (order[kv[1]['action']], -kv[1]['impressions'])):
        print('%-40s %-9s %5d %4d %6s  %s'
              % (path[:40], page['action'], page['impressions'], page['queries'],
                 ('%.0f' % page['best_position']) if page['best_position'] else '-',
                 page['because']))

    todo = [(p, v) for p, v in pages.items() if v['action'] in ('optimise', 'expand')]
    if todo:
        print('\n== What to do, in order ==\n')
        for path, page in sorted(todo, key=lambda kv: order[kv[1]['action']]):
            print('%s  %s' % (page['action'].upper(), path))
            if page['striking']:
                print('    within reach: %s' % ', '.join(page['striking'][:5]))
            if page['cluster']:
                print('    the page is being shown for these and answering none of them:')
                for q in page['cluster']['queries'][:6]:
                    print('      %s' % q)

    weights = load_weights()
    notes = learn(weights, pages, keywords, today)
    print('\n== What this changes about tomorrow ==\n')
    for note in notes:
        print('  %s' % note)
    print('\n  intent weights now: %s'
          % ', '.join('%s %.2f' % (k, weights['intent'][k]) for k in INTENTS))

    if args.dry_run:
        print('\nDry run, nothing written.')
        return 0

    history = {'snapshots': []}
    if HISTORY.exists():
        history = json.loads(HISTORY.read_text(encoding='utf-8'))
    history['snapshots'] = ([{
        'date': today, 'start': snapshot.get('start'), 'end': snapshot.get('end'),
        'queries': len(records), 'impressions': impressions, 'clicks': clicks,
        'pages': pages,
    }] + history.get('snapshots', []))[:90]
    HISTORY.write_text(json.dumps(history, indent=1) + '\n', encoding='utf-8')
    WEIGHTS.write_text(json.dumps(weights, indent=1) + '\n', encoding='utf-8')
    print('\nWritten to %s and %s'
          % (HISTORY.relative_to(ROOT), WEIGHTS.relative_to(ROOT)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
