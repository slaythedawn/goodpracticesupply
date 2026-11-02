# What to ask a supplier for, and why the ARTG number cannot be borrowed

`supplier-data-request.csv` is one row per product, 57 of them, with the columns
a supplier fills in. Send it to each supplier being quoted and the answers close
three gaps at once: the regulatory rows, the 31 products still carrying an
invented price, and the sourcing detail the product pages are missing.

## The ARTG column is the important one

`REGULATORY` in `gen/catalogue.py` is empty and has to stay empty until these
answers come back. The reason is worth being precise about, because the instinct
to fill it from a market equivalent is a reasonable instinct and it is wrong.

A price is a fact about a market. If a box of a hundred nitrile gloves sells for
$9.80 in Australia, that is true no matter who sells it, so setting our price
from it is sound and that is exactly what was done for 26 products.

An ARTG number is not a fact about a market. It identifies one sponsor's specific
goods on the Australian Register of Therapeutic Goods. Printing Livingstone's
ARTG number against a product Good Practice Supply sells would assert that these
are those goods, under that sponsor's inclusion. They are not, and it would be a
false regulatory claim about specific goods.

This site has already made that mistake once, in the other direction. It printed
`ARTG: Listed, see carton` and `Country of origin: Malaysia` on all fifty seven
products, cotton wool balls and facial tissues included. Neither was true and
neither was defensible. The field was emptied and `shop.py` was changed to render
the row only where a value exists, so an unfilled product makes no claim rather
than a generic one. Filling it with somebody else's number would be the same
defect wearing a better disguise.

Country of manufacture has the same shape. It is a property of the goods actually
being bought, not of the category.

## The "Included medical device?" column

Write N/A where the line is not a therapeutic good. Several of these are plainly
not: facial tissues, hand towels, couch roll, hand soap. Asking a supplier to
produce an ARTG number for a box of tissues is how a wrong one ends up on a page.
Where the answer is yes, the ARTG number and the sponsor name as it appears on the
Register are what is needed, not a paraphrase.

## The price columns

31 products still carry an invented price, marked PLACEHOLDER in the sheet. Those
are the lines with no published Australian retail price to work from, which is a
real feature of that end of the market rather than a gap in the research: trade
account gates and "price on application". See `seo/pricing-research.json` for
what was searched and found.

For those 31, a cost price plus a margin beats a number reverse engineered from a
competitor who will not publish theirs. That is what the cost column is for.

The 26 already researched are marked as such. Those are set at 10% below the
lowest credible Australian retail price for the same pack size, GST inclusive.
Worth checking the cost against them, because a few of the placeholders they
replaced were out by a factor of two in both directions.
