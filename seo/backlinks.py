"""Track whether the link profile is moving, because nothing else here will.

Every other number in seo/ is about what the site says. This one is about whether
anybody else says anything about it, and on 2 November 2026 the answer was nobody
at all: zero backlinks, zero referring domains, all time.

That matters more than it looks. Google crawled this domain once, on 22 September,
and had not returned six weeks later. Fifty-seven product pages were opened to
search in that window and Google has not been back to see any of them. A page
nothing links to is a page nothing arrives at, including a crawler.

The file this reads, backlinks.json, also carries a correction worth keeping. The
strategy had been resting on two rivals with low domain ratings outranking better
sites, read as proof that links were not the constraint. Both have hundreds of
referring domains. The low rating does not stop them, which was the right half.
Neither has an empty profile, which was the half that was wrong.

    python seo/backlinks.py                 # the targets, and what we have
    python seo/backlinks.py --check         # live count, needs AHREFS_API_KEY

The live check is one call and costs almost nothing. It belongs in the daily loop
so that "we should get some links" stops being a sentence in a meeting and starts
being a number that is either moving or not.
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
DATA = ROOT / 'seo' / 'backlinks.json'
DOMAIN = 'goodpracticesupply.com.au'
BASE = 'https://api.ahrefs.com/v3/site-explorer/backlinks-stats'


def load():
    return json.loads(DATA.read_text(encoding='utf-8'))


def live_count(key):
    params = {'target': DOMAIN, 'mode': 'subdomains',
              'date': datetime.date.today().isoformat()}
    url = '%s?%s' % (BASE, urllib.parse.urlencode(params))
    req = urllib.request.Request(url, headers={
        'Authorization': 'Bearer %s' % key, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode('utf-8')).get('metrics', {})


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--check', action='store_true',
                    help='ask Ahrefs for the live count and write it back')
    args = ap.parse_args()

    data = load()
    recorded = data['our_position']
    print('Referring domains: %s. Backlinks: %s. Recorded %s.\n'
          % (recorded['referring_domains'], recorded['backlinks'], data['pulled']))

    for channel in data['channels']:
        print('%s  (%s)' % (channel['channel'], channel['effort']))
        for t in channel['targets']:
            dr = t['domain_rating']
            print('   %-30s %s  %s'
                  % (t['domain'], ('DR %-3s' % dr) if dr else '      ',
                     t['evidence']))
        print()

    # The sequencing, printed every time, because the four channels above all
    # ask a third party to list this business as a supplier and none of them is
    # honest to pursue until there is something to supply. A constraint recorded
    # in a file nobody prints is not recorded.
    blocked = data.get('blocked_on')
    if blocked:
        print('Blocked on: %s' % blocked['what'])
        print('  %s\n' % blocked['why'])
        for i, step in enumerate(blocked['so_the_order_is'], 1):
            print('  %d. %s' % (i, step))
        print('\n  Before then: %s\n' % blocked['what_is_available_before_then'])

    if not args.check:
        print('%s\n' % data['the_correction'])
        return 0

    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / '.env.local')
    except ImportError:
        pass
    key = os.getenv('AHREFS_API_KEY')
    if not key:
        print('AHREFS_API_KEY is not set, so the live count was not fetched. The '
              'recorded figure above is what it was on %s.' % data['pulled'],
              file=sys.stderr)
        return 0

    try:
        metrics = live_count(key)
    except (urllib.error.HTTPError, urllib.error.URLError) as exc:
        print('Could not reach Ahrefs: %s' % exc, file=sys.stderr)
        return 3

    now = {'referring_domains': metrics.get('live_refdomains', 0),
           'backlinks': metrics.get('live', 0),
           'all_time': metrics.get('all_time', 0)}
    moved = now['referring_domains'] - recorded['referring_domains']
    print('Live: %d referring domains, %d backlinks. %s since %s.'
          % (now['referring_domains'], now['backlinks'],
             ('up %d' % moved) if moved > 0 else
             ('down %d' % -moved) if moved < 0 else 'no change',
             data['pulled']))
    if now['referring_domains'] == 0:
        print('::warning::Still zero referring domains. Nothing links to this site, '
              'which is why it is crawled once every several weeks. The targets '
              'above are the cheapest fix and none of them need permission.')

    data['our_position'] = now
    data['pulled'] = datetime.date.today().isoformat()
    DATA.write_text(json.dumps(data, indent=1) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
