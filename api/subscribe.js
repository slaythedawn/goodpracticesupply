// POST /api/subscribe — the email sign-up on every guide.
//
// One field, one purpose: a list of people to tell when the range opens. The
// contact goes straight into Resend with two properties, the page it came from
// and what that page was about, because a list you cannot segment is a list you
// end up mailing all at once.
//
// Configuration, on the Vercel project:
//   RESEND_API_KEY      required. Server side, never shipped to the browser.
//   RESEND_SEGMENT_ID   optional. Defaults to this business's own segment.
//                       Only set it to move sign-ups somewhere else.
//
// Creating a contact does not need gpsupply.com.au verified in Resend. Sending
// to one does. So this works the moment the key is set, and the list quietly
// accumulates while the DNS records are still outstanding.
//
// With no key set it returns 503 and a message the form prints as written,
// rather than thanking somebody for an address that went nowhere.

const { clean, validEmail, guard } = require('./_lib.js');

// This account is shared with another brand, and it had two segments: that
// brand's promo list and "General". The default here used to be "General",
// which meant every sign-up from all 91 pages of this site would have been
// filed into a list another business also writes to. The sign-up box promises
// "we do not sell or share the address", and a shared general list is not
// obviously consistent with that promise.
//
// So this business has its own segment and that is the default. The env var is
// still read first, for moving the list later without a deploy.
const SEGMENT_DEFAULT = '4e04c0de-f82c-4ecb-a196-cc51c58700b3'; // "Good Practice Supply, website sign-ups"

// Both of these are written to the contact, so both are bounded. A source is a
// path on this site and nothing else: whatever the browser sends, only the path
// is kept, and anything that is not a path becomes the fallback.
function cleanPath(v) {
  const s = clean(v, 200);
  return /^\/[A-Za-z0-9\-/._]*$/.test(s) ? s : 'unknown';
}

function cleanInterest(v) {
  const s = clean(v, 60).toLowerCase();
  return /^[a-z0-9 \-]+$/.test(s) && s ? s : 'general';
}

module.exports = async function handler(req, res) {
  const body = guard(req, res);
  if (!body) return;

  const email = clean(body.email, 160);
  if (!validEmail(email)) {
    return res.status(400).json({ ok: false, message: 'That does not look like an email address.' });
  }

  const key = process.env.RESEND_API_KEY;
  if (!key) {
    return res.status(503).json({ ok: false,
      message: 'Sign-ups are not connected just yet. Try again shortly.' });
  }

  const source = cleanPath(body.source);
  const interest = cleanInterest(body.interest);

  let r;
  try {
    r = await fetch('https://api.resend.com/contacts', {
      method: 'POST',
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email,
        unsubscribed: false,
        properties: { source_page: source, interest },
        segmentIds: [process.env.RESEND_SEGMENT_ID || SEGMENT_DEFAULT],
      }),
    });
  } catch (err) {
    console.error('resend contact request failed', err);
    return res.status(502).json({ ok: false,
      message: 'We could not save that just now. Try again in a minute.' });
  }

  if (r.ok) {
    // The address is never logged. The page is, because knowing which guides
    // convert is the entire reason the source property exists.
    console.log('subscribe ok', JSON.stringify({ source, interest }));
    return res.status(200).json({ ok: true });
  }

  const text = await r.text().catch(() => '');

  // Somebody signing up twice has done nothing wrong and should not be shown an
  // error. Resend reports the clash differently depending on the endpoint
  // version, so match on the shape of the message rather than one status code.
  if (/already|exists|duplicate/i.test(text)) {
    return res.status(200).json({ ok: true });
  }

  console.error('resend rejected the contact', r.status, text);
  return res.status(502).json({ ok: false,
    message: 'We could not save that just now. Try again in a minute.' });
};
