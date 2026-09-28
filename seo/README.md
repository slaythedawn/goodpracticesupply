# The daily loop

Six files that each do one thing, wired into one scheduled workflow so the site
gets a little better at ranking every day without anybody sitting down to do it.

    refresh.py        today's numbers from Ahrefs
    performance.py    what Search Console says happened, and what that changes
    competitors.py    which rival terms are worth taking, and which are theirs
    triage.py         which terms this business is allowed to target at all
    opportunities.py  the one decision, with the reason attached
    internal_links.py the links that stop a new page being an orphan

`.github/workflows/daily-seo.yml` runs them in that order at 19:12 UTC, which is
just after five in the morning in Sydney.

## Why two tools and not one

**Ahrefs** knows what Australians search for, how hard each term is, and who is
currently holding the top of the page. It does not know that this business sells
consumables and must never imply it supplies a medicine.

**TypeSafe** makes that judgement, per term, as a yes or no with a probability
attached. It knows nothing about search volume.

**Search Console** is the only one of the three that knows anything about this
site. Volume and difficulty are facts about the market; position and impressions
are facts about us, and they are the only feedback in the system that can tell
the difference between a good plan and a plan that did not work.

The arithmetic that ranks anything stays in ordinary Python where it can be read
and argued with. Nothing is scored by a model that a spreadsheet could score.

## The order matters

    measure   ->  research  ->  judge  ->  decide  ->  write  ->  gate

Measuring comes first because today's ranking uses yesterday's evidence. The
intent weights in `weights.json` are multiplied into every opportunity score, and
they move a little each run on what Google actually showed the site for. That is
the whole of the self-improving part, and it is deliberately slow: one step of
0.05 per run, bounded to between 0.5 and 2.0, with the reason written into the
log. An unbounded feedback loop finds one lucky day and spends a month on it.

`weights.json` also records which pull it last learned from, and a run over the
same pull moves nothing and says so. Without that, the path where nobody would
notice is the one that breaks: with no Search Console credentials the loop falls
back to the committed snapshot every night, and the weights would walk to their
bounds over a fortnight on one morning's evidence.

Judging comes before deciding because `opportunities.py` refuses to queue a term
that has never been judged. A new term arrives from the Ahrefs refresh unjudged,
which holds it out of the publishing queue until the safety questions have been
answered. A loop that can publish faster than it can check is the failure mode
worth designing against on a site like this one.

Gating comes last and it is not advisory. `checks/compliance.py` is the TGA
language check and a finding fails the workflow before anything is committed.

## What the loop will not do

**Write a second page for something we already rank for.** A page sitting at
position 83 for fifteen different questions about reading a syringe barrel does
not need a rival page, it needs those fifteen questions answered.
`opportunities.py` clusters by the page that should serve a term, so a cluster
produces one brief that says expand, not five that say write.

**Brief the same page twice in a fortnight.** Without a cooldown the loop is
broken in a way that looks like it is working: the highest scoring cluster stays
the highest scoring cluster until the page actually improves, and a page does not
improve the morning after it is rewritten, because Search Console takes weeks to
move. `ledger.json` records what was briefed and `COOLDOWN` in
`opportunities.py` rests it for fourteen days, so the queue gets worked instead of
the top of it being rewritten every day.

**Chase somebody else's shop.** Around 4,000 searches a month in the keyword file
are a person trying to find a syringe at Chemist Warehouse, and on volume alone
those terms sit near the top. `triage.py` asks whether a term belongs to a named
brand and `opportunities.py` scores it to a quarter. Not blocked: a page can
honestly say what a chain stocks and what we stock instead. Scored down, because
the person asked for a different shop.

**Chase an authority.** `competitors.json` records a lane per rival. Against a
state health department on sharps disposal advice, the correct move is to link to
them and take the product term sitting next to it. Contesting it is a month spent
losing.

**Publish a list of council drop-off points.** The sharps guide keeps getting
shown for state and city variants and the obvious expansion is a directory of
addresses. It does not have one on purpose: those lists go stale, and sending
somebody holding used needles to a door that closed last year is a real harm
rather than a ranking problem. The constraint travels with the brief, in
`CONSTRAINTS` in `opportunities.py`.

## What the first real run found

Worth keeping, because it is the argument for the whole thing.

- `insulin needles`, 8,600 searches a month at difficulty 3, held at position one
  by a single Medshop collection page. It was not in the keyword file at all.
- `bacteriostatic water` moved from 5,700 to 7,100 searches in six days. A
  keyword file maintained by hand is stale the moment anybody looks away.
- Search Console showed `/learn/reading-a-syringe` surfacing for sixteen distinct
  queries about where a given millilitre mark sits on a 1mL barrel, every one
  between position 73 and 89. Google had already decided the page was on the
  subject. It simply does not answer the question.
- `needle gauge chart` looked like a vacancy: a US lab supplier at position two,
  a UK reseller at domain rating 11, and a Pinterest pin about knitting needles
  at position ten. Then the volume came back at twenty searches a month in
  Australia. The page is empty because nobody local is knocking. It stays in
  `competitors.json` as the worked example of a SERP that is weak and worthless
  at once.
- `allmedicalwaste.com.au` ranks seventh for `sharps container` at domain rating
  three. A page selling the thing can reach the first page of a product SERP with
  no domain strength at all, which is the bet this site is making.

## Running any of it by hand

Everything has a free offline mode, so the shape of a run can be checked without
spending anything.

    python seo/refresh.py --plan                        # the calls it would make
    python seo/performance.py --from-file seo/gsc-snapshot.json --dry-run
    python seo/competitors.py --dry-run
    python seo/triage.py --dry-run
    python seo/opportunities.py                         # ranks, writes nothing
    python seo/opportunities.py --write                 # queue and today's brief
    python seo/internal_links.py --dry-run

## Keys

Repository secrets, on the `slaythedawn/goodpracticesupply` repository under
Settings, Secrets and variables, Actions.

| secret | needed for | without it |
| --- | --- | --- |
| `TYPESAFE_API_KEY` | every safety judgement | the loop fails, by design |
| `AHREFS_API_KEY` | the market data | the loop fails, by design |
| `GSC_SERVICE_ACCOUNT_JSON` | reading Search Console | falls back to the committed snapshot, so the loop runs and stops learning |
| `ANTHROPIC_API_KEY` | writing the page without a person | the brief is opened as an issue instead |

For Search Console: create a service account in Google Cloud, enable the Search
Console API, download the JSON key, paste the whole file into the secret, then add
the service account's email address as a user on the property in Search Console
under Settings, Users and permissions. Read-only access is enough.

## The files this writes

| file | committed | what it is |
| --- | --- | --- |
| `keywords-au.json` | yes | every tracked term, refreshed daily |
| `competitors.json` | yes | who holds what, and which lane they are in |
| `competitor-gaps.json` | yes | the contested terms, scored and judged |
| `triage-result.json` | yes | the safety judgement per term. Committed on purpose: it is the record of what was cleared, and re-asking 120 questions every morning costs money to learn nothing |
| `gsc-snapshot.json` | yes | the last Search Console pull, so the analysis can be re-run offline |
| `performance.json` | yes | ninety days of snapshots, for trends |
| `weights.json` | yes | the learned weights and the log of every change |
| `queue.json` | yes | today's ranked clusters and which one was chosen |
| `ledger.json` | yes | what was briefed and when, which is what stops the loop briefing the same page every morning |
| `briefs/` | yes | one brief per published day |
