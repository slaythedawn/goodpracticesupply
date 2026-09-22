"""The house copy rules, asked as typed judgements instead of read by eye.

Every other script in checks/ tests something a machine can decide by looking:
a link resolves or it does not, a description is under 170 characters or it is
not. The rules that actually carry risk here are not like that. "Does this
passage read as instruction for a medicine" has no regex, which is why it has
always been checked by a person reading, which means inconsistently and
sometimes not at all.

Things that were live on this site at some point and were caught late by a
human: a blanket ARTG claim printed on cotton wool, a phone number that did not
ring, staffed hours nobody staffed, a dispatch warehouse that did not exist, and
forms that said a message had been sent when it had not. This is the check that
would have caught them.

Each rule is a Noul, a yes/no judgement returning a probability. They are
independent questions over the same state, so all of them go in one request per
page and are answered together.

    ./.venv/bin/python checks/compliance.py --dry-run     # offline, no key, no cost
    ./.venv/bin/python checks/compliance.py               # live, needs a key

Credentials come from TYPESAFE_API_KEY, read out of the environment or
.env.local. The key is never printed, logged or written anywhere by this script.
"""

import argparse
import os
import pathlib
import re
import sys
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / 'docs'

# Only the page's own copy is judged. The shared footer carries the standing
# disclosure, which says in terms that we do not supply peptides, hormones or
# any prescription medicine. Feeding that to a question asking whether the page
# implies we supply a medicine is asking for a false positive on all 91 pages.
MAIN_ONLY = True

# Probability above which a rule counts as tripped. Deliberately not 0.5: a Noul
# near 0.5 means the model genuinely cannot tell, and treating that as a finding
# produces noise that gets the whole check ignored. Tune it against real output
# rather than trusting this number.
THRESHOLD = 0.7


# Negative controls.
#
# A clean site scoring low proves the rules do not false-positive. It proves
# nothing about whether they ever fire, and identical numbers would appear if
# every rule were broken and always returned near zero. These passages each
# breach exactly one rule on purpose, so a run over them says whether the check
# can detect anything at all.
#
# NOT SITE COPY. Invented, deliberately non-compliant, never rendered, never
# imported by anything in gen/. They exist only to be failed.
CONTROLS = [
    ('states_a_dose',
     'Once you have drawn up, start at 0.25mg and hold there for four weeks '
     'before increasing to 0.5mg. Most people settle between 1mg and 2mg.'),
    ('names_a_site_for_a_drug',
     'Semaglutide goes into the abdomen, at least five centimetres away from '
     'the navel. Rotate to the outer thigh if the abdomen is tender.'),
    ('states_a_frequency',
     'Take it once a week, on the same day each week. If you miss a day, take '
     'it as soon as you remember and carry on weekly from there.'),
    ('implies_supplies_medicine',
     'We stock pharmaceutical grade semaglutide and tirzepatide alongside our '
     'consumables, shipped from our Sydney warehouse with the syringes '
     'included in the price.'),
    ('therapeutic_outcome_claim',
     'Our alcohol swabs cut infection rates and help injection sites heal '
     'faster, so your treatment works better from the first week.'),
    ('unbacked_regulatory_claim',
     'Every product in our range is ARTG listed, see carton for details. '
     'Country of origin: Malaysia.'),
    ('claims_unavailable_capability',
     'Order before 2pm and we dispatch the same day from our Sydney warehouse. '
     'Our team is on 1300 555 123, Monday to Friday, 8.30am to 5pm AEST.'),
]


class MainText(HTMLParser):
    """Collect visible text, from <main> only when MAIN_ONLY is set.

    A flag rather than a depth counter. Counting nesting looks more careful and
    is actually wrong here: void elements such as <br> and <img> raise a start
    tag and never an end tag, so a depth counter drifts, </main> stops matching,
    and the footer is swallowed into every page. <main> is not nested, so a flag
    is both simpler and correct.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.skip = 0
        self.in_main = False
        self.main_done = False

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'svg'):
            self.skip += 1
        elif tag == 'main' and not self.main_done:
            self.in_main = True

    def handle_startendtag(self, tag, attrs):
        pass  # self-closing tags carry no text and must not touch skip

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'svg') and self.skip:
            self.skip -= 1
        elif tag == 'main' and self.in_main:
            self.in_main = False
            self.main_done = True

    def handle_data(self, data):
        if self.skip:
            return
        if MAIN_ONLY and not self.in_main:
            return
        text = data.strip()
        if text:
            self.parts.append(text)

    def text(self):
        joined = ' '.join(self.parts)
        # Unfilled component holes are the sweep's job, not this one, and they
        # read as gibberish to a judgement.
        joined = re.sub(r'\{\{[^}]*\}\}', ' ', joined)
        return re.sub(r'\s+', ' ', joined).strip()


def page_text(path):
    parser = MainText()
    parser.feed(path.read_text(encoding='utf-8'))
    return parser.text()


def pages():
    out = []
    for path in sorted(DOCS.rglob('*.html')):
        rel = '/' + str(path.relative_to(DOCS))
        if rel.startswith('/internal/'):
            continue
        out.append((rel, path))
    return out


# The rules. Each one states the yes and the no explicitly, because a bare
# question leaves the boundary to the model and the boundary is the whole point.
# Wording follows the gps-compliance skill, which is the source of truth.
def build_questions(Noul):
    return {
        'states_a_dose': Noul(
            instructions='Does this page state a dose, an amount, a strength or a '
                         'quantity of a medicine that a reader should take?',
            criteria={
                'true': 'The text gives a dose, amount, strength or number of units '
                        'of a medicine, drug, peptide or hormone that a person '
                        'should take or inject.',
                'false': 'The text only describes equipment, such as needle gauge, '
                         'needle length, syringe volume, barrel graduations, or how '
                         'much liquid a syringe holds. Describing the capacity or '
                         'markings of a syringe is equipment, not a dose.',
            }),
        'names_a_site_for_a_drug': Noul(
            instructions='Does this page tell the reader where on the body to inject '
                         'a specific named medicine?',
            criteria={
                'true': 'The text pairs a named medicine, drug, peptide or hormone '
                        'with a place on the body to inject it.',
                'false': 'The text discusses injection sites only in general terms of '
                         'tissue layer or technique, without tying them to a named '
                         'medicine, or does not discuss sites at all.',
            }),
        'states_a_frequency': Noul(
            instructions='Does this page tell the reader how often to take or inject '
                         'a medicine?',
            criteria={
                'true': 'The text states a schedule or frequency for taking or '
                        'injecting a medicine, such as daily or weekly.',
                'false': 'Any frequency mentioned is about equipment rather than a '
                         'medicine, such as how often to replace a sharps container '
                         'or change a dressing.',
            }),
        'implies_supplies_medicine': Noul(
            instructions='Does this page imply the business sells or supplies a '
                         'peptide, a hormone, or any prescription medicine?',
            criteria={
                'true': 'The text presents a medicine, peptide or hormone as '
                        'something the business stocks, sells, ships or can obtain.',
                'false': 'The text mentions medicines only as something the reader '
                         'already has from their own prescriber or pharmacy, and the '
                         'goods offered are consumables such as syringes, needles, '
                         'swabs, dressings, gloves or diluent.',
            }),
        'therapeutic_outcome_claim': Noul(
            instructions='Does this page claim a health or therapeutic outcome?',
            criteria={
                'true': 'The text claims that using something will improve a health '
                        'condition, produce a clinical result, or make a treatment '
                        'more effective.',
                'false': 'The text describes physical properties, comfort, '
                         'convenience or handling of equipment without claiming a '
                         'health outcome. Saying a finer needle is more comfortable '
                         'is a property, not a therapeutic claim.',
            }),
        'unbacked_regulatory_claim': Noul(
            instructions='Does this page make a general or blanket claim about '
                         'regulatory approval, ARTG listing, or country of origin?',
            criteria={
                'true': 'The text asserts approval status or country of origin as a '
                        'sweeping claim covering the range, or in vague terms such '
                        'as "see carton", rather than a specific value for a '
                        'specific product.',
                'false': 'Approval status is either absent, explained as a general '
                         'concept without being claimed for these goods, or given as '
                         'a specific value for a specific named product.',
            }),
        'claims_unavailable_capability': Noul(
            instructions='Does this page claim the business can do something it '
                         'cannot currently do?',
            criteria={
                'true': 'The text claims orders can be placed now, or promises a '
                        'phone line, staffed hours, dispatch times, shipping or '
                        'returns handling as though they are operating.',
                'false': 'The text either makes no such claim, or says plainly that '
                         'ordering is not open yet and these things are coming.',
            }),
    }


def self_test(TypeSafeClient, questions, threshold):
    """Check that each rule fires on a passage written to breach it."""
    print('%d controls, one per rule, threshold %.2f\n' % (len(CONTROLS), threshold))
    passed = 0
    with TypeSafeClient() as client:
        for expected, passage in CONTROLS:
            result = client.system_one(state=passage, questions=questions)
            scored = {name: answer.noul for name, answer in result.nouls.items()}
            hit = scored[expected]
            others = sorted(((p, n) for n, p in scored.items() if n != expected),
                            reverse=True)
            fired = hit >= threshold
            passed += fired
            print('%-4s %-32s %.3f' % ('ok' if fired else 'MISS', expected, hit))
            print('       loudest other rule: %s %.3f' % (others[0][1], others[0][0]))
    print('\n%d of %d controls fired. A miss means that rule cannot detect its own '
          'breach and needs rewording, not a lower threshold.' % (passed, len(CONTROLS)))
    return 0 if passed == len(CONTROLS) else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--dry-run', action='store_true',
                    help='print what would be sent and exit. No key, no network, no cost.')
    ap.add_argument('--limit', type=int, default=0, help='check only the first N pages')
    ap.add_argument('--threshold', type=float, default=THRESHOLD)
    ap.add_argument('--only', default='', help='substring filter on the page path')
    ap.add_argument('--self-test', action='store_true',
                    help='run the rules against passages written to breach one rule '
                         'each, and report whether each one fires. This is the only '
                         'evidence that the check detects anything at all.')
    ap.add_argument('--show-all', action='store_true',
                    help='print every rule and its probability, not just the ones that '
                         'trip. Without this a clean page prints nothing, which tells '
                         'you it passed but not whether it passed by a mile or by a '
                         'whisker, and the margin is what the threshold is tuned on.')
    args = ap.parse_args()

    targets = [(rel, p) for rel, p in pages() if args.only in rel]
    if args.limit:
        targets = targets[:args.limit]

    if not targets:
        print('no pages matched', file=sys.stderr)
        return 2

    if args.dry_run:
        # Import lazily so a dry run works with the SDK absent.
        try:
            from typesafe_sdk import Noul
        except ImportError:
            print('typesafe-sdk is not installed. pip install -r requirements.txt',
                  file=sys.stderr)
            return 2
        questions = build_questions(Noul)
        rel, path = targets[0]
        text = page_text(path)
        print('would ask %d questions of each of %d pages, one request per page\n'
              % (len(questions), len(targets)))
        print('questions: %s\n' % ', '.join(sorted(questions)))
        print('example state, from %s (%d chars):' % (rel, len(text)))
        print('  %s...\n' % text[:300])
        print('example question, states_a_dose:')
        q = questions['states_a_dose']
        print('  instructions: %s' % q.instructions)
        print('  true : %s' % q.criteria['true'])
        print('  false: %s' % q.criteria['false'])
        print('\nshortest page: %s' % min(
            ((len(page_text(p)), r) for r, p in targets))[1])
        return 0

    try:
        from dotenv import load_dotenv
        load_dotenv(ROOT / '.env.local')
    except ImportError:
        pass

    if not os.getenv('TYPESAFE_API_KEY'):
        print('TYPESAFE_API_KEY is not set. Put it in .env.local, which is gitignored.',
              file=sys.stderr)
        return 2

    from typesafe_sdk import Noul, TypeSafeClient
    from typesafe_sdk import TypeSafeAPIConnectionError, TypeSafeError

    questions = build_questions(Noul)
    findings = 0

    if args.self_test:
        return self_test(TypeSafeClient, questions, args.threshold)

    try:
        with TypeSafeClient() as client:
            for rel, path in targets:
                text = page_text(path)
                if not text:
                    print('SKIP %s (no text in <main>)' % rel)
                    continue

                result = client.system_one(state=text, questions=questions)

                scored = sorted((name, answer.noul) for name, answer in result.nouls.items())
                tripped = [(n, p) for n, p in scored if p >= args.threshold]

                if tripped:
                    findings += 1

                if args.show_all:
                    print('%-4s %s' % ('FAIL' if tripped else 'ok', rel))
                    for name, p in scored:
                        mark = '  <-- trips' if p >= args.threshold else ''
                        print('       %-32s %.3f%s' % (name, p, mark))
                    print('       %-32s %.3f' % ('highest', max(p for _, p in scored)))
                elif tripped:
                    print('FAIL %s' % rel)
                    for name, p in tripped:
                        print('       %-32s %.3f' % (name, p))
    except TypeSafeAPIConnectionError as exc:
        print('Could not reach the TypeSafe API: %s' % exc, file=sys.stderr)
        return 3
    except TypeSafeError as exc:
        print('TypeSafe rejected the request: %s' % exc, file=sys.stderr)
        return 1

    print('\nchecked %d page%s against %d rules, %d with findings'
          % (len(targets), '' if len(targets) == 1 else 's', len(questions), findings))
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main())
