"""Links inside body copy.

Every paragraph on this site is escaped before it is written, which is correct
and stays correct. The side effect was that a link could not be put into a
sentence at all: an <a> written into a string arrived on the page as visible
markup. So the site had no inline links anywhere, and the internal-link
suggester produced sixty-six suggestions that could not be applied to a single
page. That was found only after building the thing that produces them.

One restricted form is allowed, written in the content files:

    'Used needles go into a [sharps container](/shop/clinic-disposal).'

The text is escaped first and the pattern matched against the escaped string, so
nothing in the copy can inject markup, and the path is constrained to a relative
path on this site. An external link is deliberately impossible here.
"""

import html
import re

E = html.escape

LINKSTYLE = 'color:#1C4034;text-decoration:underline;text-underline-offset:2px'

_LINK = re.compile(r'\[([^\[\]]+)\]\((/[A-Za-z0-9\-/]*)\)')

# What a half-written link looks like after escaping, so a typo is caught by a
# check rather than published as visible brackets.
LEFTOVER = re.compile(r'\]\(/|\]\(')


def EL(text):
    """Escape, then turn [label](/path) into a link."""
    return _LINK.sub(
        lambda m: '<a href="%s" style="%s">%s</a>' % (m.group(2), LINKSTYLE, m.group(1)),
        E(text))
