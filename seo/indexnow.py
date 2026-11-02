# Tell Bing and Yandex that a page changed.
#
# Google does not participate in IndexNow and has said so, so this does nothing
# for the ranking that matters most. It is here for two narrower reasons.
#
# The first is that Bing's index is what ChatGPT search reads, and on a domain
# with no authority a citation in an assistant answer is more reachable than a
# position in Google. robots.txt already lets those crawlers in deliberately;
# this is the other half of that decision.
#
# The second is that it costs nothing and needs no credential. The key is not a
# secret: the protocol works by making you publish it at the site root, so that
# anyone submitting URLs for this host has demonstrably written to it. It is in
# the repository on purpose. Do not move it to a secret, and do not .gitignore
# the key file, because the submission fails the moment the file stops being
# fetchable.
#
# What this does NOT do is re-submit everything daily. IndexNow asks you to send
# changed URLs only, and a daily ping of 91 unchanged pages is the documented way
# to have your submissions discounted. The sitemap generator already records a
# content hash per page in gen/lastmod.json, so "changed" is a real question with
# a real answer, and the state file below records what was last sent for each.
#
# Usage:
#   python seo/indexnow.py            submit whatever changed since last time
#   python seo/indexnow.py --dry-run  print what would be sent, send nothing
#   python seo/indexnow.py --all      resubmit every indexable URL (first run)

import io, os, sys, json, pathlib, urllib.request, urllib.error

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'gen'))
import seo as SEO

KEY = 'ff96f1785ed213b9701cc8c01e681cb1'
KEY_FILE = ROOT / 'docs' / (KEY + '.txt')
STAMPS = ROOT / 'gen' / 'lastmod.json'
STATE = ROOT / 'seo' / 'indexnow-state.json'
ENDPOINT = 'https://api.indexnow.org/indexnow'

# One request covers every participating engine, so submitting to each of them
# separately would be the same URLs three times.
HOST = SEO.ORIGIN.split('://', 1)[1]


def load(path, default):
    try:
        return json.load(io.open(str(path), encoding='utf-8'))
    except (IOError, ValueError):
        return default


def changed(everything=False):
    """[(url, hash)] for pages whose content differs from what was last sent."""
    stamps = load(STAMPS, {})
    if not stamps:
        raise SystemExit('indexnow: gen/lastmod.json is empty, run the build first')
    sent = load(STATE, {})
    out = []
    for path in sorted(stamps):
        h = stamps[path].get('hash')
        if not h:
            continue
        if everything or sent.get(path) != h:
            # SEO.ORIGIN + path, exactly as the sitemap builds it, so the
            # home page is submitted as the trailing-slash form its own
            # canonical uses rather than as a bare origin.
            out.append((SEO.ORIGIN + path, h, path))
    return out


def submit(urls):
    body = json.dumps({
        'host': HOST,
        'key': KEY,
        'keyLocation': '%s/%s.txt' % (SEO.ORIGIN, KEY),
        'urlList': [u for u, _, _ in urls],
    }).encode('utf-8')
    req = urllib.request.Request(ENDPOINT, data=body, method='POST',
                                 headers={'Content-Type': 'application/json; charset=utf-8'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read(400).decode('utf-8', 'replace')


def main():
    args = sys.argv[1:]
    dry = '--dry-run' in args
    everything = '--all' in args

    if not KEY_FILE.is_file():
        raise SystemExit('indexnow: %s is missing, so a submission would be '
                         'rejected. The key file is public by design and belongs '
                         'in the repository.' % KEY_FILE)
    if KEY_FILE.read_text(encoding='utf-8').strip() != KEY:
        raise SystemExit('indexnow: %s does not contain the key this script '
                         'sends, so a submission would be rejected.' % KEY_FILE)

    urls = changed(everything)
    if not urls:
        print('indexnow: nothing changed, nothing submitted')
        return 0

    # 10,000 is the protocol limit and this site is nowhere near it, but a
    # surprise is better caught than truncated silently.
    if len(urls) > 10000:
        raise SystemExit('indexnow: %d URLs exceeds the per-request limit' % len(urls))

    print('indexnow: %d changed URL%s' % (len(urls), '' if len(urls) == 1 else 's'))
    for u, _, _ in urls[:25]:
        print('  ' + u)
    if len(urls) > 25:
        print('  ... and %d more' % (len(urls) - 25))

    if dry:
        print('indexnow: --dry-run, nothing sent and state not advanced')
        return 0

    try:
        status, body = submit(urls)
    except urllib.error.HTTPError as e:
        # 422 is the documented answer to a URL that does not belong to the host
        # or a key that does not match, and it is a defect here rather than a
        # transient failure, so it is worth saying loudly.
        print('indexnow: HTTP %s %s' % (e.code, e.read(400).decode('utf-8', 'replace')))
        return 1
    except (urllib.error.URLError, OSError) as e:
        # The loop should not fail because an external endpoint is unreachable.
        # Nothing is recorded, so the next run sends the same URLs again.
        print('indexnow: could not reach the endpoint (%s), state not advanced' % e)
        return 0

    print('indexnow: HTTP %s %s' % (status, body.strip() or '(empty body, which is normal)'))
    if status not in (200, 202):
        print('indexnow: unexpected status, state not advanced')
        return 1

    # Only advance once the submission is accepted, so a failure retries instead
    # of silently skipping a page for good.
    sent = load(STATE, {})
    for _, h, path in urls:
        sent[path] = h
    # Drop paths that are no longer in the sitemap, same as the sitemap does.
    live = {path for _, _, path in urls} | set(load(STAMPS, {}))
    for gone in [k for k in sent if k not in live]:
        del sent[gone]
    io.open(str(STATE), 'w', encoding='utf-8').write(
        json.dumps(sent, indent=1, sort_keys=True) + '\n')
    print('indexnow: recorded %d submitted URLs' % len(urls))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
