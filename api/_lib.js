// Shared bits for the two form endpoints. Files under api/ that start with an
// underscore are not routes, so this is importable without being callable.
//
// One address, hello@gpsupply.com.au. Mail goes out from it, replies come back
// to it, and it is the only address printed on the site. Forward it to whatever
// inbox is already being read; there is no second mailbox to check.
//
// Configuration, on the Vercel project:
//   RESEND_API_KEY  the only one that is required. Server side, never shipped.
//   ENQUIRIES_TO    optional. Defaults to hello@gpsupply.com.au. Set it to a
//                   different address to receive somewhere else before the
//                   forwarder exists.
//   ENQUIRIES_FROM  optional. Defaults to the same address, which needs
//                   gpsupply.com.au verified in Resend.
//
// With no key set, send() returns a 503 and a message the form shows as
// written, rather than pretending a message was received.

const ADDRESS = 'hello@gpsupply.com.au';
const FROM_DEFAULT = `Good Practice Supply <${ADDRESS}>`;

function clean(v, max) {
  return typeof v === 'string' ? v.trim().slice(0, max) : '';
}

function validEmail(v) {
  return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v);
}

// ABN checksum, per the ATO's published algorithm: subtract one from the first
// digit, apply the weights, and the total is divisible by 89. Catches a
// transposed pair, which a length check does not.
function validAbn(raw) {
  const d = String(raw).replace(/\s/g, '');
  if (!/^\d{11}$/.test(d)) return false;
  const w = [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19];
  let sum = (Number(d[0]) - 1) * w[0];
  for (let i = 1; i < 11; i++) sum += Number(d[i]) * w[i];
  return sum % 89 === 0;
}

function esc(s) {
  return String(s).replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));
}

function readBody(req) {
  if (typeof req.body === 'string') { try { return JSON.parse(req.body || '{}'); } catch { return {}; } }
  return req.body || {};
}

function needList(problems) {
  // Join on "and" only between whole items. A problem string may contain its own
  // comma ("a valid ABN, or no ABN at all"), and a regex over the joined string
  // splices the "and" into the middle of it.
  if (problems.length === 1) return 'We need ' + problems[0] + '.';
  return 'We need ' + problems.slice(0, -1).join(', ')
    + ' and ' + problems[problems.length - 1] + '.';
}

async function send({ subject, rows, replyTo }) {
  const key = process.env.RESEND_API_KEY;
  const to = process.env.ENQUIRIES_TO || ADDRESS;
  if (!key) {
    return { status: 503,
      message: 'This form is not connected just yet. Try again shortly.' };
  }
  const html = '<table>' + rows.map(([k, v]) =>
    `<tr><th align="left" valign="top">${esc(k)}</th><td>${esc(v).replace(/\n/g, '<br>')}</td></tr>`
  ).join('') + '</table>';
  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: process.env.ENQUIRIES_FROM || FROM_DEFAULT,
        to: [to], reply_to: replyTo, subject,
        html, text: rows.map(([k, v]) => `${k}: ${v}`).join('\n'),
      }),
    });
    if (!r.ok) {
      console.error('resend rejected the message', r.status, await r.text());
      return { status: 502, message: 'We could not send that just now. Try again in a minute.' };
    }
  } catch (err) {
    console.error('resend request failed', err);
    return { status: 502, message: 'We could not send that just now. Try again in a minute.' };
  }
  return { status: 200 };
}

// Method guard plus the honeypot. A real person never fills a field they
// cannot see, so a filled one gets a cheerful 200 and goes nowhere.
function guard(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    res.status(405).json({ ok: false, message: 'Use POST.' });
    return null;
  }
  const body = readBody(req);
  if (clean(body.website, 80)) { res.status(200).json({ ok: true }); return null; }
  return body;
}

module.exports = { clean, validEmail, validAbn, esc, needList, send, guard };
