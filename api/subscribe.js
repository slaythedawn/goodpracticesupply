// POST /api/subscribe — the email sign-up on every guide.
//
// One field, one purpose: a list of people to tell when the range opens. The
// contact goes straight into Resend with two properties, the page it came from
// and what that page was about, because a list you cannot segment is a list you
// end up mailing all at once.
//
// Configuration, on the Vercel project:
//   RESEND_API_KEY      required. Server side, never shipped to the browser.
//   RESEND_SEGMENT_ID   optional. Defaults to the General segment on the
//                       account. Set it to file sign-ups somewhere else.
//
// Creating a contact does not need gpsupply.com.au verified in Resend. Sending
// to one does. So this works the moment the key is set, and the list quietly
// accumulates while the DNS records are still outstanding.
//
// With no key set it returns 503 and a message the form prints as written,
// rather than thanking somebody for an address that went nowhere.

const { clean, validEmail, guard } = require('./_lib.js');

const SEGMENT_DEFAULT = 'bcf7acc8-2da5-411a-9d66-497eca350dee'; // "General"

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
