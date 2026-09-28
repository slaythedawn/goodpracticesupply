"""The daily decision: one job, fully specified, with the reason attached.

Everything else in seo/ produces a list. Ahrefs says what Australia searches for.
competitors.py says which of those a rival is holding and which are theirs by
right. performance.py says what Google is already showing us and how close it is.
triage.py says which terms this business is allowed to touch at all. Four lists
and no decision.

This makes the decision. It merges the four, clusters what is left so the site
does not end up with five thin pages about millilitre markings competing with
each other, and writes one brief.

Two rules do most of the work.

Never write a second page for a cluster we already rank for. A page sitting at
position 83 for fifteen queries about reading a barrel does not need a rival
page, it needs those fifteen questions answered. Splitting the topic is how a
site competes with itself and loses to both.

Nothing is queued that the safety triage has not cleared. The judgement lives in
triage.py and the answer is read from its output, so a term nobody has judged is
held rather than published. A loop that can publish faster than it can check is
the failure mode worth designing against on a site like this.

    python seo/opportunities.py                 # rank and print, write nothing
    python seo/opportunities.py --write         # write the queue and today's brief
"""

import argparse
import collections
import datetime
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'seo'))
sys.path.insert(0, str(ROOT / 'gen'))

KEYWORDS = ROOT / 'seo' / 'keywords-au.json'
GAPS = ROOT / 'seo' / 'competitor-gaps.json'
TRIAGE = ROOT / 'seo' / 'triage-result.json'
WEIGHTS = ROOT / 'seo' / 'weights.json'
SNAPSHOT = ROOT / 'seo' / 'gsc-snapshot.json'
QUEUE = ROOT / 'seo' / 'queue.json'
LEDGER = ROOT / 'seo' / 'ledger.json'
BRIEFS = ROOT / 'seo' / 'briefs'

# Days before the same cluster can be briefed again.
#
# Without this the loop is broken in a way that looks like it is working. The
# highest scoring cluster stays the highest scoring cluster until the page
# actually improves, and a page does not improve the morning after it is
# rewritten: Search Console takes weeks to move. So the first run would brief
# reading-a-syringe, and so would the second, and the thirtieth, while everything
# behind it in the queue was never reached.
COOLDOWN = 14

# A term a rival already holds is worth more than an empty SERP of the same size:
# somebody has proved there is money in it, and the page doing it is a page.
RIVAL_BONUS = 1.3

# What a term is worth when the searcher was looking for a named shop. Around
# 4,000 searches a month in this keyword file are somebody trying to find a
# syringe at Chemist Warehouse, and on volume alone those terms rank near the top.
#
# Not blocked, because a page can honestly say what a chain stocks and what we
# stock instead, and that is a real answer. Scored down, because the person asked
# for a different shop and a page that pretends otherwise is a page they bounce
# off. The judgement comes from triage.py so the decision is visible rather than
# buried in a keyword blocklist.
BRAND_PENALTY = 0.25

# A page of ours inside the top 20 for a term has it. Queuing the term again buys
# a second page that splits the same clicks.
ALREADY_OURS = 20

# Below this, a term is held rather than queued, and the brief says why. Matches
# the threshold the triage and compliance runs default to.
SAFE_ENOUGH = 0.75

# Subjects where the obvious expansion is the wrong one. The sharps guide keeps
# getting shown for state and city variants, and the temptation is a list of
# council drop-off points. It is not an oversight that the guide has none: those
# lists go stale, and sending somebody holding used needles to an address that
# closed last year is a real harm rather than a ranking problem. So the brief
# for that cluster carries the constraint with it.
CONSTRAINTS = {
 'sharps': ('Describe how to find a drop-off point and who to ask. Never publish '
            'specific addresses, opening hours or council contact details. They go '
            'stale and a stale address sends somebody with used needles to a locked '
            'door.'),
 'disposal': ('Same as sharps: the method and the authority to ask, never a list of '
              'locations.'),
 'bacteriostatic': ('Sterile diluent, sold as a consumable. Never describe what it is '
                    'mixed with, never name a peptide, hormone or medicine, and never '
                    'imply we supply one.'),
 'reconstitution': ('Volumes and concentrations as arithmetic about liquid. Never a '
                    'dose, never a named drug, never a schedule.'),
 'insulin': ('The syringe and the needle, not the medicine. U-100 graduation is a fact '
             'about the barrel. Never a dose and never a site for a named product.'),
 'testosterone': ('Equipment only. Do not write a page targeting this term without '
                  'checking the triage judgement first.'),
}

DULL = {'a', 'an', 'the', 'and', 'or', 'of', 'for', 'to', 'in', 'on', 'at', 'is',
        'it', 'how', 'what', 'where', 'why', 'which', 'when', 'who', 'do', 'does',
        'my', 'your', 'you', 'buy', 'best', 'cheap', 'near', 'me', 'australia',
        'online', 'free', 'with', 'from', 'can', 'be', 'much', 'many', 'look',
        'like', 'size', 'sizes'}


def ledger():
    data = read(LEDGER, None) or {'entries': []}
    return data


def on_cooldown(led, today):
    """Clusters briefed recently enough that briefing them again is wasted."""
    cutoff = (datetime.date.fromisoformat(today)
              - datetime.timedelta(days=COOLDOWN)).isoformat()
    return {e['cluster']: e['date'] for e in led.get('entries', [])
            if e.get('date', '') >= cutoff}


def read(path, default=None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding='utf-8'))


def as_path(rel):
    path = rel[:-len('.html')] if rel.endswith('.html') else rel
    if path.endswith('/index'):
        path = path[:-len('/index')] or '/'
    return path or '/'


def words_of(term):
    return [w for w in re.split(r'[^a-z0-9.]+', term.lower())
            if len(w) > 1 and w not in DULL]


def measured(snapshot):
    """Per lowercase query: the best position one of our pages holds for it."""
    best = {}
    for row in (snapshot or {}).get('rows', []):
        keys = row.get('keys') or []
        if len(keys) < 2:
            continue
        query = keys[0].lower()
        path = re.sub(r'^https?://[^/]+', '', keys[1]).split('?')[0]
        path = path.rstrip('/') or '/'
        pos = row.get('position') or 999
        if query not in best or pos < best[query]['position']:
            best[query] = {'position': round(pos, 1), 'path': path,
                           'impressions': row.get('impressions') or 0}
    return best


# A size is a variant, not a subject. "2ml syringe" and "10ml syringe" are the
# same page with a different number in it, so the number is dropped when working
# out which page should serve the term and kept when listing what the page has to
# answer.
SIZE = re.compile(r'^\d+(?:\.\d+)?(?:ml|l|g|mg|mm|cm|in|oz)?$')

# Pages that exist to route rather than to answer. The all-products index and the
# persona landing pages mention everything the site sells, which made them win
# every routing contest they entered: the first live run put "sharps container"
# on the GLP-1 landing page, because four pages tied on score and the winner was
# decided by which filename sorted first.
HUBS = ('/index.html', '/shop.html', '/learn.html')
HUB_PENALTY = 0.6
LANDING_PENALTY = 0.75


def routing_words(term):
    return [w for w in words_of(term) if not SIZE.match(w)]


def page_impressions(seen):
    """Impressions per page, from what Search Console already showed."""
    out = collections.Counter()
    for row in seen.values():
        out[row['path']] += row['impressions']
    return out


def says(haystack, word):
    """Whether a page uses this word, as a word.

    A substring test looked reasonable and was not: it put "ear syringe", a bulb
    for ear wax, into the cluster about reading an insulin barrel, because "ear"
    appears inside "clear", "year" and "nearly". Short words are where this bites
    and short words are most of a search term.
    """
    return re.search(r'(?<![a-z0-9])%s(?:s|es)?(?![a-z0-9])' % re.escape(word),
                     haystack) is not None


def serving_page(term, pages, impressions=None):
    """Which of our pages is the best existing home for this term.

    Where a word appears matters more than how often. A term in the title is what
    the page is about; the same term in the body is a page that mentions it in
    passing, and on a site where every page footer lists the whole range, passing
    mentions are everywhere. So each word scores by the best place it appears and
    nothing else.

    Every meaningful word has to appear somewhere or the fit is zero. A page that
    says "container" and never says "sharps" is not the home for sharps
    containers.

    Ties are broken on evidence rather than on filename order: the page Search
    Console already shows for this kind of query wins, then the page with the
    tightest title.
    """
    wanted = list(dict.fromkeys(routing_words(term)))
    if not wanted:
        return None, 0.0
    impressions = impressions or {}
    ranked = []
    for rel, page in pages.items():
        title = page['title'].lower()
        desc = page['desc'].lower()
        body = page['text'].lower()
        if not all(says(title, w) or says(desc, w) or says(body, w) for w in wanted):
            continue
        hit = sum(3 if says(title, w) else (2 if says(desc, w) else 1) for w in wanted)
        fit = hit / (3.0 * len(wanted))
        if rel in HUBS:
            fit *= HUB_PENALTY
        elif rel.startswith('/for/'):
            fit *= LANDING_PENALTY
        ranked.append((round(fit, 3), impressions.get(as_path(rel), 0),
                       -len(title.split()), rel))
    if not ranked:
        return None, 0.0
    ranked.sort(reverse=True)
    fit, _, _, rel = ranked[0]
    return rel, fit


def constraint_for(term):
    hits = [text for word, text in CONSTRAINTS.items() if word in term.lower()]
    return hits[0] if hits else ''


def score_rows(keywords, gaps, weights, seen, pages):
    """Every keyword, scored, with what it would mean to act on it."""
    gap_by_term = {g['keyword'].lower(): g for g in (gaps or {}).get('gaps', [])}
    intent_weight = (weights or {}).get('intent', {})
    page_queries = collections.Counter(row['path'] for row in seen.values())
    rows = []
    for row in keywords['keywords']:
        term = row['keyword']
        low = term.lower()
        volume = row.get('volume') or 0
        kd = row.get('difficulty')
        if kd is None:
            kd = 50
        potential = row.get('traffic_potential') or 0
        reach = max(volume, potential * 0.5)
        base = reach * (1 - kd / 100.0)

        intents = [i for i in (row.get('intents') or []) if i in intent_weight]
        weight = (sum(intent_weight[i] for i in intents) / len(intents)) if intents else 1.0

        gap = gap_by_term.get(low)
        rival = RIVAL_BONUS if (gap and gap.get('lane') in ('retailer', 'marketplace')) else 1.0

        mine = seen.get(low)
        home, fit = serving_page(term, pages, page_impressions(seen))

        out = {
            'keyword': term, 'volume': volume, 'difficulty': kd,
            'traffic_potential': potential, 'intents': row.get('intents') or [],
            'intent_weight': round(weight, 3),
            'rival': gap['held_by'] if gap else None,
            'rival_lane': gap['lane'] if gap else None,
            'our_position': mine['position'] if mine else None,
            'our_page': mine['path'] if mine else None,
            'best_home': as_path(home) if home else None,
            'home_fit': fit,
            'safe_to_target': None,
            'brand_term_is_theirs': None,
            'constraint': constraint_for(term),
            'score': round(base * weight * rival, 1),
        }

        if mine and mine['position'] <= ALREADY_OURS:
            out['action'] = 'optimise'
            out['why'] = ('we already sit at %.0f for this on %s'
                          % (mine['position'], mine['path']))
        elif mine:
            out['action'] = 'expand'
            out['why'] = ('Google shows %s for this at %.0f, so the page is on the '
                          'subject and not answering it' % (mine['path'], mine['position']))
        elif fit >= 0.5:
            out['action'] = 'expand'
            shown = page_queries.get(out['best_home'], 0)
            out['why'] = ('%s is already about this%s'
                          % (out['best_home'],
                             (', and Google shows it for %d other quer%s already'
                              % (shown, 'y' if shown == 1 else 'ies')) if shown
                             else ', and Google has not shown it for anything yet'))
        else:
            out['action'] = 'new'
            out['why'] = 'nothing on the site covers this'
        rows.append(out)
    return rows


def apply_triage(rows, triage):
    """Attach the safety judgement. A term nobody judged is held, not assumed."""
    if not triage:
        return
    judged = {r['keyword'].lower(): r for r in triage}
    for row in rows:
        j = judged.get(row['keyword'].lower())
        if j is None:
            continue
        row['safe_to_target'] = j.get('safe_to_target')
        row['serves_a_buyer'] = j.get('serves_a_buyer')
        row['brand_term_is_theirs'] = j.get('brand_term_is_theirs')
        if (row['brand_term_is_theirs'] or 0) >= SAFE_ENOUGH:
            row['score'] = round(row['score'] * BRAND_PENALTY, 1)
            row['why'] = ('%s. The searcher wanted a named shop, so this is scored '
                          'down rather than chased' % row['why'])


def cluster(rows):
    """Group rows that one page should serve, so the site does not compete with itself.

    Rows already tied to one of our pages cluster on that page. Rows with no home
    cluster on their most distinctive shared word, which is crude and is meant to
    be: the point is to stop five near-identical terms each becoming a page, not
    to build a taxonomy.
    """
    groups = collections.defaultdict(list)
    for row in rows:
        if row['action'] in ('optimise', 'expand'):
            key = 'page:' + (row['our_page'] or row['best_home'] or '?')
        else:
            ws = words_of(row['keyword'])
            key = 'topic:' + (ws[0] if ws else row['keyword'])
        groups[key].append(row)

    out = []
    for key, members in groups.items():
        members.sort(key=lambda r: -r['score'])
        lead = members[0]
        unsafe = [m for m in members
                  if m['safe_to_target'] is not None and m['safe_to_target'] < SAFE_ENOUGH]
        unjudged = [m for m in members if m['safe_to_target'] is None]
        out.append({
            'key': key,
            'kind': 'page' if key.startswith('page:') else 'topic',
            'action': lead['action'],
            'target': lead['keyword'],
            'page': lead['our_page'] or lead['best_home'],
            'score': round(sum(m['score'] for m in members[:8]), 1),
            'lead_score': lead['score'],
            'volume': sum(m['volume'] for m in members),
            'terms': [m['keyword'] for m in members[:12]],
            'rivals': sorted({m['rival'] for m in members if m['rival']}),
            'constraint': next((m['constraint'] for m in members if m['constraint']), ''),
            'held': [m['keyword'] for m in unsafe],
            'unjudged': len(unjudged),
            'why': lead['why'],
            'members': members[:12],
        })
    out.sort(key=lambda c: -c['score'])
    return out


def ready(c, recent=None):
    """A cluster is only publishable when every term in it has been cleared."""
    recent = recent or {}
    if c['key'] in recent:
        return False, ('briefed on %s, and %d days have to pass before it is worth '
                       'briefing again' % (recent[c['key']], COOLDOWN))
    if c['held']:
        return False, 'the safety triage rejected %s' % ', '.join(c['held'][:3])
    if c['unjudged']:
        return False, ('%d term%s in this cluster have never been judged. Run '
                       'seo/triage.py first.'
                       % (c['unjudged'], '' if c['unjudged'] == 1 else 's'))
    if c['action'] == 'optimise':
        return False, 'already inside the top %d, so this is an edit rather than a brief' % ALREADY_OURS
    return True, ''


def near_misses(page, snapshot):
    """What Google already shows this page for and it does not answer.

    The most useful lines in a brief. Ahrefs says what the market searches; this
    says what the market searched, saw this page offered, and did not click.
    """
    if not page or not snapshot:
        return []
    import performance
    records = [r for r in performance.tidy(snapshot) if r['path'] == page]
    deep = [r for r in records if r['position'] > performance.STRIKING[1]]
    close = [r for r in records
             if performance.STRIKING[0] <= r['position'] <= performance.STRIKING[1]]
    return (sorted(close, key=lambda r: r['position'])
            + sorted(deep, key=lambda r: r['position']))[:20]


def brief(c, today, snapshot=None):
    """Everything the writer needs, so nothing is decided twice."""
    import feature

    page = c['page']
    known = feature.for_page(page) if page else None
    lines = []
    a = lines.append
    a('# %s' % ('Expand %s' % page if c['action'] == 'expand' else
                'New page for "%s"' % c['target']))
    a('')
    a('Generated %s by seo/opportunities.py. Every number here came from '
      'seo/keywords-au.json, seo/competitor-gaps.json or seo/gsc-snapshot.json. '
      'Nothing in it is a guess.' % today)
    a('')
    a('## The job')
    a('')
    a('- **Action**: %s' % c['action'])
    a('- **Target term**: %s' % c['target'])
    if page:
        a('- **Page**: `%s`' % page)
    a('- **Why**: %s' % c['why'])
    a('- **Cluster score**: %s, from %s monthly searches across %d terms'
      % (c['score'], c['volume'], len(c['terms'])))
    if c['rivals']:
        a('- **Held by**: %s' % ', '.join(c['rivals']))
    a('')
    misses = near_misses(page, snapshot)
    if misses:
        a('## What Google already shows this page for, and it does not answer')
        a('')
        a('These came out of Search Console, not out of a keyword tool. Every one is '
          'a real search where this page was offered and was not good enough. Answer '
          'them in the page, in plain words, and do not pad.')
        a('')
        a('| the actual search | position | impressions |')
        a('| --- | --- | --- |')
        for m in misses:
            a('| %s | %.0f | %d |' % (m['query'], m['position'], m['impressions']))
        a('')

    a('## The market terms this cluster covers')
    a('')
    a('| term | volume | difficulty | our position |')
    a('| --- | --- | --- | --- |')
    for m in c['members']:
        a('| %s | %s | %s | %s |'
          % (m['keyword'], m['volume'] or '-', m['difficulty'],
             ('%.0f' % m['our_position']) if m['our_position'] else 'not ranking'))
    a('')
    if c['constraint']:
        a('## The constraint on this subject')
        a('')
        a(c['constraint'])
        a('')
    a('## What the page must carry')
    a('')
    a('- **A photograph**, eager loaded, served through the Vercel optimiser. '
      'Add the key to `PHOTO` in `gen/guides.py` for a new guide.')
    a('- **One featured product or tool**, not a grid. %s'
      % ('Already set: `%s`.' % known if known else
         'Add an entry to `FEATURED` in `gen/feature.py` or the build fails.'))
    a('- **An email sign-up**, from `gen/capture.py`, with the interest tag set so '
      'the contact can be segmented later.')
    a('- **Inbound links from at least two pages that already rank.** Run '
      '`python seo/internal_links.py` after writing and apply what it suggests.')
    a('- **Australian spelling, no em dashes, no emoji.**')
    a('')
    a('## The house rules that apply to every page')
    a('')
    a('- Consumables only. Never imply this business supplies a peptide, a hormone '
      'or any prescription medicine.')
    a('- Technique described through the equipment: gauge, length, angle. Never a '
      'dose, never a site for a named drug, never a frequency.')
    a('- The directions that came with the medicine and the prescriber come first, '
      'and are said to come first.')
    a('- No therapeutic outcome claims.')
    a('')
    a('## Before it goes live')
    a('')
    a('```')
    a('python gen/build.py && python gen/guides.py    # or the full build order')
    a('python checks/compliance.py --only %s          # the TGA language gate'
      % (page or '/learn/'))
    a('node checks/seocheck.mjs && node checks/depth.mjs && node checks/linkcheck.mjs')
    a('```')
    a('')
    a('A compliance finding blocks publication. It is not advisory.')
    a('')
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--write', action='store_true',
                    help='write seo/queue.json and today the brief')
    ap.add_argument('--top', type=int, default=12, help='how many clusters to print')
    args = ap.parse_args()

    keywords = read(KEYWORDS)
    gaps = read(GAPS)
    weights = read(WEIGHTS)
    triage = read(TRIAGE)
    snapshot = read(SNAPSHOT)

    import internal_links
    pages = internal_links.load()

    seen = measured(snapshot)
    rows = score_rows(keywords, gaps, weights, seen, pages)
    apply_triage(rows, triage)   # may rescore, so cluster afterwards
    clusters = cluster(rows)
    today = datetime.date.today().isoformat()

    print('%d keywords, %d clusters. Inputs present: %s\n'
          % (len(rows), len(clusters),
             ', '.join(n for n, v in [('keywords', keywords), ('competitor gaps', gaps),
                                      ('weights', weights), ('triage', triage),
                                      ('search console', snapshot)] if v) or 'none'))

    print('%-9s %8s %7s %-34s %s' % ('action', 'score', 'volume', 'target', 'cluster'))
    led = ledger()
    recent = on_cooldown(led, today)
    for c in clusters[:args.top]:
        ok, _ = ready(c, recent)
        print('%-9s %8.1f %7d %-34s %s%s'
              % (c['action'], c['score'], c['volume'], c['target'][:34],
                 c['key'], '' if ok else '  (held)'))

    actionable = [c for c in clusters if ready(c, recent)[0]]
    blocked = [(c, ready(c, recent)[1]) for c in clusters if not ready(c, recent)[0]]

    if blocked:
        resting = [b for b in blocked if b[0]['key'] in recent]
        print('\n%d cluster%s held back%s:'
              % (len(blocked), '' if len(blocked) == 1 else 's',
                 (', %d of them resting after a recent brief' % len(resting))
                 if resting else ''))
        for c, reason in blocked[:8]:
            print('  %-34s %s' % (c['target'][:34], reason))

    if not actionable:
        print('\nNothing is ready to publish. The usual cause is that the safety '
              'triage has not been run over the newest keywords, which is a '
              'deliberate stop rather than a failure.')
        if args.write:
            QUEUE.write_text(json.dumps({'date': today, 'clusters': clusters,
                                         'actionable': []}, indent=1) + '\n',
                             encoding='utf-8')
        return 0

    job = actionable[0]
    print('\n== Today\'s job ==\n')
    print('%s: %s' % (job['action'].upper(), job['target']))
    print('%s' % job['why'])
    if job['constraint']:
        print('\nConstraint: %s' % job['constraint'])

    if args.write:
        BRIEFS.mkdir(exist_ok=True)
        slug = re.sub(r'[^a-z0-9]+', '-', job['target'].lower()).strip('-')
        out = BRIEFS / ('%s-%s.md' % (today, slug))
        out.write_text(brief(job, today, snapshot), encoding='utf-8')
        QUEUE.write_text(json.dumps({'date': today, 'job': job['key'],
                                     'brief': str(out.relative_to(ROOT)),
                                     'clusters': clusters,
                                     'actionable': [c['key'] for c in actionable]},
                                    indent=1) + '\n', encoding='utf-8')
        led['entries'] = ([{'date': today, 'cluster': job['key'],
                            'target': job['target'], 'action': job['action'],
                            'page': job['page'],
                            'brief': str(out.relative_to(ROOT)),
                            'score_when_chosen': job['score']}]
                          + led.get('entries', []))[:400]
        LEDGER.write_text(json.dumps(led, indent=1) + '\n', encoding='utf-8')
        print('\nBrief written to %s' % out.relative_to(ROOT))
        print('Queue written to %s' % QUEUE.relative_to(ROOT))
        print('Logged in %s, so it will not be briefed again for %d days'
              % (LEDGER.relative_to(ROOT), COOLDOWN))
    return 0


if __name__ == '__main__':
    sys.exit(main())
