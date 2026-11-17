"""Build the sourcing spreadsheet we send to the agent in China.

Not part of the site build. Run it on its own:

    python3.13 gen/sourcing_sheet.py     # writes export/sourcing-shortlist.xlsx

It is the successor to Priority_Sourcing_Shortlist.xlsx, sent 23 August, and it
deliberately keeps that file's shape: a tab of the items to quote first, a tab
of the rest, a numbered row per product, our columns on the left and hers on the
right, and green shading for the top priority. She has worked from that layout
once already, so changing it would cost her a re-read for no gain.

Three things are different.

It covers the whole range rather than the 45 items of the original, because the
catalogue has moved on and she should not be quoting against a list that is
three months stale.

It carries our proposed pack size, which the original did not, and then asks her
for the standard pack and the units per carton separately. That is the question
the first brief never actually put to her: it asked for "Pack / format" in a
single column and got back nothing, because one column cannot hold both what we
want and what the factory makes.

It asks her to rank what she can move on. The August brief told her which three
we wanted first and she replied that some of them, bacteriostatic water in
particular, she could not source at all. Ranking is hers to do, not ours, and
the column makes that explicit rather than leaving it in prose.

Product data comes from gen/catalogue.py and the proposed pack sizes from
gen/pricelist.py, so the sheet, the supply list and the site cannot disagree.
"""

import datetime
import os
import pathlib
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import catalogue
import pricelist

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'export' / 'sourcing-shortlist.xlsx'

FOREST = '1C4034'
MINT = 'E8F0EB'
GREEN = 'C6E0B4'      # the original's "top priority" shading
HERS = 'FFF2CC'       # the columns we want her to fill
GREY = '808080'

# Tab 1, in the order the August brief put them. The first three were shaded
# green there and stay green here.
PRIORITY = [
    'u-100-insulin-syringes',
    'bacteriostatic-water',
    'alcohol-swabs',
    'hypodermic-needles',
    'drawing-up-needles',
    'luer-lock-syringes',
    'sterile-water-for-injection',
    'chlorhexidine-skin-prep',
    'sharps-container-bench',
    'sharps-container-wall-mount',
    'vial-access-devices',
]
FIRST_THREE = PRIORITY[:3]

# Starred on tab 2 of the August brief as higher priority within the wider list,
# minus the ones that turned out to duplicate tab 1.
STARRED = [
    'nitrile-examination-gloves',
    'latex-examination-gloves',
    'cotton-wool-balls',
    'adhesive-plasters',
    'vaginal-speculum-disposable',
]

OURS = [
    ('#', 5),
    ('Product', 30),
    ('Sizes / variants we want', 34),
    ('Spec', 30),
    ('Pack size (our proposal)', 17),
    ('Our brand?', 10),
]
THEIRS = [
    ('Your priority\n(1 = can move first)', 15),
    ('Closest item you can supply', 28),
    ('Standard pack size', 16),
    ('Units per carton', 14),
    ('FOB / unit (USD)', 14),
    ('MOQ', 11),
    ('Lead time', 12),
    ('Own-brand pack?', 14),
    ('Notes', 26),
]

THIN = Side(style='thin', color='BFBFBF')
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def products():
    """Every product, with its category, keyed for lookup."""
    out = {}
    for cat in catalogue.CATEGORIES:
        for p in cat['products']:
            out[p['slug']] = (cat, p)
    return out


def own_brand(p):
    """Whether we would want this in our own packaging.

    The August brief answered this per row by hand. Rather than re-type a
    judgement nobody has revisited, say yes for the things the brand is built
    on and leave the rest for the conversation.
    """
    return 'Yes' if p['slug'] in set(PRIORITY) | set(STARRED) else 'Maybe'


def header(ws, row=4):
    cols = OURS + THEIRS
    for i, (label, width) in enumerate(cols, start=1):
        c = ws.cell(row=row, column=i, value=label)
        c.font = Font(bold=True, color='FFFFFF', size=10)
        c.fill = PatternFill('solid', fgColor=FOREST)
        c.alignment = Alignment(wrap_text=True, vertical='center')
        c.border = BOX
        ws.column_dimensions[get_column_letter(i)].width = width
    ws.row_dimensions[row].height = 34
    ws.freeze_panes = ws.cell(row=row + 1, column=1)


def write_rows(ws, slugs, lookup, start_row):
    r = start_row
    for n, slug in enumerate(slugs, start=1):
        cat, p = lookup[slug]
        packs = {pricelist.pack_for(p, v[0]) for v in p['variants']}
        vals = [
            n,
            p['name'],
            ', '.join(v[0] for v in p['variants']),
            p['spec'],
            ' / '.join(sorted(packs)),
            own_brand(p),
        ]
        for i, v in enumerate(vals, start=1):
            c = ws.cell(row=r, column=i, value=v)
            c.alignment = Alignment(wrap_text=True, vertical='top')
            c.border = BOX
            if slug in FIRST_THREE:
                c.fill = PatternFill('solid', fgColor=GREEN)
        for i in range(len(OURS) + 1, len(OURS) + len(THEIRS) + 1):
            c = ws.cell(row=r, column=i)
            c.fill = PatternFill('solid', fgColor=HERS)
            c.border = BOX
            c.alignment = Alignment(wrap_text=True, vertical='top')
        r += 1
    return r


def title(ws, heading, note):
    a = ws.cell(row=1, column=1, value=heading)
    a.font = Font(bold=True, size=14, color=FOREST)
    b = ws.cell(row=2, column=1, value=note)
    b.font = Font(size=10, color='404040')
    b.alignment = Alignment(wrap_text=True, vertical='top')
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=10)
    ws.row_dimensions[2].height = 30


def build():
    lookup = products()
    missing = [s for s in PRIORITY + STARRED if s not in lookup]
    if missing:
        raise SystemExit('sourcing_sheet: these slugs are not in the '
                         'catalogue any more: %s' % ', '.join(missing))

    rest = [s for s in lookup if s not in set(PRIORITY) | set(STARRED)]
    # Keep catalogue order within the remainder so related things sit together.
    order = [p['slug'] for cat in catalogue.CATEGORIES for p in cat['products']]
    rest.sort(key=order.index)

    wb = Workbook()

    ws = wb.active
    ws.title = 'Priority - quote these first'
    title(ws, 'Priority list, in order',
          'Please rank these in the yellow column by what you can move on '
          'first, then fill in the pack size, units per carton, FOB price, MOQ '
          'and lead time. The three shaded green are the ones we most want to '
          'start with. Closest match is fine, it does not have to be identical.')
    header(ws)
    end = write_rows(ws, PRIORITY, lookup, 5)
    ws.cell(row=end + 1, column=2,
            value='Green = the three we would most like to start with.'
            ).font = Font(italic=True, size=9, color=GREY)

    ws2 = wb.create_sheet('Full range')
    title(ws2, 'The rest of the range',
          'Same request: rank what you can move on, and fill in pack size, '
          'units per carton, FOB price, MOQ and lead time. The first five are '
          'the ones we would like next after the priority tab.')
    header(ws2)
    end2 = write_rows(ws2, STARRED + rest, lookup, 5)
    ws2.cell(row=end2 + 1, column=2,
             value='Rows 1 to %d are the next priority after the first tab.'
                   % len(STARRED)).font = Font(italic=True, size=9, color=GREY)

    OUT.parent.mkdir(exist_ok=True)
    wb.save(OUT)
    total = len(PRIORITY) + len(STARRED) + len(rest)
    print('sourcing_sheet: %s  (%d priority, %d in the full range, %d total)'
          % (OUT.relative_to(ROOT), len(PRIORITY),
             len(STARRED) + len(rest), total))
    if total != len(lookup):
        raise SystemExit('sourcing_sheet: %d products written but the '
                         'catalogue has %d. Something was dropped.'
                         % (total, len(lookup)))
    return OUT


if __name__ == '__main__':
    build()
