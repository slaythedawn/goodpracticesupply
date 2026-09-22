"""Serve the photography through Vercel's image optimiser.

Every product photograph on this site is a raw PNG from CloudFront, delivered at
full size to every device, in a format meant for screenshots rather than
photographs. 611 image tags across the site, 44 distinct files.

Vercel optimises images for any project, not only Next ones: a request to
/_vercel/image?url=...&w=...&q=... returns AVIF or WebP at the requested width,
cached at the edge. The source host has to be listed in the images.remotePatterns
block of vercel.json or the request is refused.

This is the one change in the set that cannot be verified from here, because the
optimiser only exists on Vercel. If the images break on the live site, set
OPTIMISE to False, rebuild, and every src returns to the original CloudFront URL
exactly as before.
"""

import os
import urllib.parse

OPTIMISE = True

# The widths actually used by the layouts on this site. A width not listed in
# vercel.json is refused by the optimiser, so the two lists have to agree.
SIZES = [320, 480, 640, 828, 1080, 1440, 1920]

QUALITY = 75

HOSTS = ('d8j0ntlcm91z4.cloudfront.net', 'd2ol7oe51mr4n9.cloudfront.net')


def optimised(url, width=1080):
    """A CloudFront photograph, resized and re-encoded by the edge."""
    if not OPTIMISE or not url.startswith('https://'):
        return url
    if not any(h in url for h in HOSTS):
        return url
    if width not in SIZES:
        raise ValueError('width %r is not in SIZES, so Vercel will refuse it' % width)
    return '/_vercel/image?url=%s&w=%d&q=%d' % (
        urllib.parse.quote(url, safe=''), width, QUALITY)


def srcset(url, widths=(480, 828, 1440)):
    """A srcset so a phone does not download a desktop image."""
    if not OPTIMISE:
        return ''
    if not any(h in url for h in HOSTS):
        return ''
    return ' srcset="%s"' % ', '.join(
        '%s %dw' % (optimised(url, w), w) for w in widths)
