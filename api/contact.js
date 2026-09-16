// POST /api/contact — a general enquiry.
//
// Practice name and ABN are optional here: plenty of people buying for
// themselves have neither, and asking for an ABN to ask a question is the sort
// of thing this site exists to avoid.

const { clean, validEmail, validAbn, needList, send, guard } = require('./_lib.js');

module.exports = async function handler(req, res) {
  const body = guard(req, res);
  if (!body) return;

  const name = clean(body.name, 100);
  const email = clean(body.email, 160);
  const practice = clean(body.practice, 120);
  const abn = clean(body.abn, 20);
  const message = clean(body.message, 4000);

  const problems = [];
  if (!name) problems.push('your name');
  if (!validEmail(email)) problems.push('a valid email');
  if (message.length < 10) problems.push('a message');
  if (abn && !validAbn(abn)) problems.push('a valid 11 digit ABN, or no ABN at all');
  if (problems.length) return res.status(400).json({ ok: false, message: needList(problems) });

  const r = await send({
    subject: `Enquiry: ${name}${practice ? ' (' + practice + ')' : ''}`,
    replyTo: email,
    rows: [['Name', name], ['Email', email], ['Practice', practice || '(none given)'],
           ['ABN', abn || '(none given)'], ['Message', message]],
  });
  return r.status === 200
    ? res.status(200).json({ ok: true })
    : res.status(r.status).json({ ok: false, message: r.message });
};
