# The legal documents, and why they are not in docs/

Six documents arrived from Adam Mazzaferro on 27 October 2026 as drafts:

1. T&Cs, supply of goods
2. Website terms of use
3. Privacy policy, V4 October 2026
4. Refunds and returns policy
5. Payment information
6. Shipping policy

His covering email says two things that decide how they are handled here.

The first is that sections are highlighted in each document, and those highlights
are prompts to settle how the business actually operates before the wording is
fixed. The second is explicit: "These documents need to be finalised and settled
by us before they go live on the Website."

So the source text lives in this directory and this directory is never served.
`docs/` is the published site; nothing in `legal/` is copied into it until
`LEGAL_LIVE` in `gen/seo.py` is switched on. That switch is off.

That is not caution for its own sake. A privacy policy is a binding
representation about how data is handled, and a refunds or shipping policy is a
binding representation about how orders are handled. Publishing a draft whose
highlighted sections exist precisely because they do not yet match practice
means publishing statements about this business that are not true. It is the
same failure the language gate exists to catch, one layer up.

The other option would be to publish them with a note saying they are under
review. The compliance rules rule that out, and they are right to: a page that
says "this policy is not final" is not a policy.

## The format

One file per document, `<slug>.txt`, plain text:

    # A heading
    A paragraph. Blank line between paragraphs.

    ## A subheading
    Another paragraph.

    !! A highlighted section, carried through from the Word document so the open
    question stays visible in the source rather than being silently resolved.

`gen/legal.py` turns these into pages. A `!!` line is a hard error while
`LEGAL_LIVE` is on, because an unresolved highlight must not reach the site.

## Getting the text in

The `.docx` files cannot be pulled out of Gmail from a cloud session: there is no
attachment download tool, and the only other route is transcribing the raw MIME
by hand, which is not a safe way to move a zip archive. Either save the six files
to Google Drive, where they can be read directly, or commit them to this
directory and run the converter.
